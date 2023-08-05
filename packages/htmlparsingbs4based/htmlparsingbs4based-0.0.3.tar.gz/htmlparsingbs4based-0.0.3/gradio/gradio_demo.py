import gradio as gr
from description_extraction.crawling.helpers import crawl, get_crawling_results
from description_extraction.models.parser_ import parsing_html
from description_extraction.keywords.phrase_matching import extract_keywords
from description_extraction.summarization.extract_generator import ExtractGenerator
from description_extraction.summarization.abstract_generator import AbstractGenerator
from description_extraction.models.usefulness_classifier import TrainedUsefulnessClassifier
import os
import torch
import sys
import spacy
import mlflow
import pandas as pd
import networkx as nx
from transformers import BertTokenizer
from description_extraction.settings import CUDA_DEVICE_NAME
from description_extraction.settings import MLFLOW_S3_ENDPOINT_URL
from description_extraction.settings import MLFLOW_TRACKING_URI
from description_extraction.settings import MLFLOW_URI_CUSTOM_NER
from description_extraction.settings import MLFLOW_RUN_ID_MULTI_PASSAGE_CLASSIF
from description_extraction.settings import DEFAULT_MAX_SUMMARY_LENGTH
from credentials.credential_env import AWS_ACCESS_KEY_ID
from credentials.credential_env import AWS_SECRET_ACCESS_KEY

os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY


custom_spacy_model, generic_spacy_model, bert_tokenizer, sent_usefulness_classifier = None, None, None, None
self_promotion_adjs, demonym_list, df_supra_national_level, df_country_level, dfs_adm_levels, tr_cl_hierarchy_graph = None, None, None, None, None, None

# -------------------------------------------------------------------------------------
if 'AWS_ACCESS_KEY_ID' not in os.environ or 'AWS_SECRET_ACCESS_KEY' not in os.environ:
    print('Set env variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and re-run')
else:
    #use_trained_usefulness_classifier = '--use-cls' in sys.argv 
    use_trained_usefulness_classifier = 1 
    print('Loading custom spacy model...')
    
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = MLFLOW_S3_ENDPOINT_URL
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    custom_spacy_model = mlflow.spacy.load_model(MLFLOW_URI_CUSTOM_NER)
    generic_spacy_model = spacy.load('en_core_web_lg')

    if use_trained_usefulness_classifier:
    
        print('Loading sentence usefulness classifier...')
        
        bert_tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

        #try:
        sent_usefulness_classifier = TrainedUsefulnessClassifier(
            torch.device(CUDA_DEVICE_NAME if torch.cuda.is_available() else 'cpu'),
            bert_tokenizer,
            mlflow_model_run_id=MLFLOW_RUN_ID_MULTI_PASSAGE_CLASSIF
        )
        # except BaseException as exc:
        #     sent_usefulness_classifier = None
        #     bert_tokenizer = None
        #     print(f'Exception occurred while loading the sentence usefulness classifier: {exc}. Rule-based method will be used')

    else:
        print('Using rule-based sentence usefulness classifier')
        bert_tokenizer = None
        sent_usefulness_classifier = None
# -------------------------------------------------------------------------------------

    # Load list of self-promotion adjectives
    if os.path.exists('description_extraction/summarization/self_promotion_adjs.txt'):
        with open('description_extraction/summarization/self_promotion_adjs.txt', 'rt') as f:
            self_promotion_adjs = list(ln.strip() for ln in f.readlines())
    else:
        self_promotion_adjs = []

    # Load demonym list
    if os.path.exists('description_extraction/summarization/demonyms.txt'):
        with open('description_extraction/summarization/demonyms.txt', 'rt') as f:
            demonym_list = dict((ln.split(',')[0], ln.split(',')[1].strip()) for ln in f.readlines())
    else:
        demonym_list = dict({})
    
    print('Loading GeoNames resources...')

    # Load GeoNames resources if available
    NECESSARY_ADM_LVL_FILES = ['description_extraction/summarization/geonames_adm1_level.tsv', 'description_extraction/summarization/geonames_adm2_level.tsv', 'description_extraction/summarization/geonames_adm3_level.tsv']
    if all(os.path.exists(p) for p in ['description_extraction/summarization/geonames_supra_national_entities.tsv', 'description_extraction/summarization/geonames_country_level.tsv', 'description_extraction/summarization/geonames_hierarchy_transitive_closure.txt'] + NECESSARY_ADM_LVL_FILES):
        df_supra_national_level = pd.read_csv('description_extraction/summarization/geonames_supra_national_entities.tsv', delimiter='\t')
        df_country_level = pd.read_csv('description_extraction/summarization/geonames_country_level.tsv', delimiter='\t')
        dfs_adm_levels = [pd.read_csv(path, delimiter='\t') for path in NECESSARY_ADM_LVL_FILES]
        tr_cl_hierarchy_graph = nx.read_edgelist('description_extraction/summarization/geonames_hierarchy_transitive_closure.txt', nodetype=int, create_using=nx.DiGraph)
    else:
        df_supra_national_level = None
        df_country_level = None
        dfs_adm_levels = None
        tr_cl_hierarchy_graph = None

def extract_summary(original_desc, company_name_db, length):
    summarizer = ExtractGenerator(custom_spacy_model, generic_spacy_model, bert_tokenizer, sent_usefulness_classifier)
    desc_extraction, spacy_out = summarizer.create_summary(text=original_desc, company_name_from_db=company_name_db, max_length=length)

    return desc_extraction, spacy_out

def abstract_generate(original_desc, length):
    summarizer = AbstractGenerator(custom_spacy_model, generic_spacy_model, self_promotion_adjs, demonym_list, df_supra_national_level, df_country_level, dfs_adm_levels, tr_cl_hierarchy_graph)

    Tabular_summary = summarizer.create_tabular_summary(text=original_desc, max_length=length)
    Textual_summary_woas, _ = summarizer.create_textual_summary(text=original_desc, max_length=length, link_sents_with_and=False)
    Textual_summary_was, spacy_out = summarizer.create_textual_summary(text=original_desc, max_length=length, link_sents_with_and=True)
    return Tabular_summary, Textual_summary_woas, Textual_summary_was, spacy_out


def parser_integrated(input_url, parsing_tool, only_text, post_process, ignore_elements, min_linewords, description_summary, length_ds, abstract_summary, length_as):
    
    """
    - parsing_tool:
        1. beautifulsoup    (call 'get_text()' to retrieve all the text and ignore all tags)
        2. costomized_bs4   (costomized parser based on bs4, keep tags <p>,<div>,<a>,<li>,<h>,<f>,<img>,etc., with costomized format)
        3. boilerpipe   (call 'ArticleExtractor()' to retrieve the content with largest text block and ignore all tags)
        4. readability  (call 'readability.Document.summary()' to extract one <div> content with highest score, keep the original html, not recommended)
        5. html2text    (traverse all tags, get the text from the most inside tag, can get all texts and keep structure, with markdown format)
        6. inscriptis   (traverse all tags, get the text from the most inside tag, can get all texts and keep structure, with costomized format)
        7. inscriptis_annotated (find all 1-level tags, and get the text, with costomized format)
        8. lxml (get all text, ignore tags and format)
    - only_text: remove the tag indicator like '<p>' and the format, like [..(..)], applicable for 'costomized_bs4' and 'inscriptis_annotated'
    - post_process: strip whitespace, remove noise, deduplicate
    - ignore_element: to ignore <a>, <img> and <t> (only keep <div>, <p>, <li>, <f>),
                    applicable for 'costomized_bs4', 'inscriptis_annotated', 'inscriptis' and 'html2text'
    - min_lineword: remove lines shorter than 'min_linewords' 
    """

    itera = get_crawling_results(input_url)
    for url, page in itera:
        if url:             
            original_desc = parsing_html(page, input_url, parsing_tool, only_text, post_process, ignore_elements, min_linewords)
            #highlight = {'text': highlight_text, 'entities': entities_list}
    
    if description_summary == 1:
        company_name_db = 'ABD'
        desc_extraction, _ = extract_summary(original_desc, company_name_db, length_ds)
    else:
        desc_extraction = 'Not applicable ...'

    if abstract_summary == 1:
        _, _, textual_summary_was, _ = abstract_generate(original_desc, length_as)
    else:
        textual_summary_was = 'Not applicable ...'
    
    return original_desc, desc_extraction, textual_summary_was


# if __name__ == '__main__':
#     # original_desc, highlight, desc_extraction, textual_summary_was = parser_integrated(url='https://www.kempen.com/en/about-kempen', \
#     #     parsing_tool='html2text', only_text=1, post_process=1, ignore_elements=1, min_linewords=8, description_summary=1,\
#     #          length_ds=1000, abstract_summary=0, length_as=1000)
#     # print(desc_extraction)

#     text = "Bashar means “People” in arabic and people. BasharSoft is a high-tech company whose mission it is to build efficient employment marketplaces and employment ecosystems. We enable social sustainability and positive economics by helping individuals and businesses at scale. We achieve this through technology-enabled platforms and services, partnerships, and thought leadership. Our focus is on the emerging markets and we want to help people and businesses with anything related to employment whether it's business growth, education, mentoring, career opportunities or otherwise. We want to improve people’s lives through sustainable employment. BasharSoft is the proud developer of the best employment platforms in the market. Millions of job seekers and thousands of employers use our platforms every day to meet their career and employment needs. No matter where you are in your career path or the type of business you run, BasharSoft has the solution for you. WUZZUF is an online recruitment platform that helps employers hire the right talent, and connects professionals with the right career opportunities. WUZZUF excels in matchmaking and creating transparency for job seekers and recruiters, in addition to providing dedicated full lifecycle recruitment support. WUZZUF has the largest database of job seekers & employers in Egypt—all in a full-fledged employment marketplace. FORASNA is Egypt’s first and most reliable online employment marketplace for Arabic speakers. Given that blue-collar workers alone represent 66.8% of the total active labor force in Egypt, we built FORASNA so we could play an active role in helping people of all walks of life to find jobs and to help businesses of all kinds find the employees they need. In order to maximize our economic impact, our scope is not just about jobs and recruitment but about everything that is employment related: career and work opportunities, education, career employment, and even how companies manage employees after hiring. We bui Bashar means “People” in arabic and people. BasharSoft is a high-tech company whose mission it is to build efficient employment marketplaces and employment ecosystems. We enable social sustainability and positive economics by helping individuals and businesses at scale. We achieve this through technology-enabled platforms and services, partnerships, and thought leadership. Our focus is on the emerging markets and we want to help people and businesses with anything related to employment whether it's business growth, education, mentoring, career opportunities or otherwise. We want to improve people’s lives through sustainable employment. BasharSoft is the proud developer of the best employment platforms in the market. Millions of job seekers and thousands of employers use our platforms every day to meet their career and employment needs. No matter where you are in your career path or the type of business you run, BasharSoft has the solution for you. WUZZUF is an online recruitment platform that helps employers hire the right talent, and connects professionals with the right career opportunities. WUZZUF excels in matchmaking and creating transparency for job seekers and recruiters, in addition to providing dedicated full lifecycle recruitment support. WUZZUF has the largest database of job seekers & employers in Egypt—all in a full-fledged employment marketplace. FORASNA is Egypt’s first and most reliable online employment marketplace for Arabic speakers. Given that blue-collar workers alone represent 66.8% of the total active labor force in Egypt, we built FORASNA so we could play an active role in helping people of all walks of life to find jobs and to help businesses of all kinds find the employees they need. In order to maximize our economic impact, our scope is not just about jobs and recruitment but about everything that is employment related: career and work opportunities, education, career employment, and even how companies manage employees after hiring. We bui BasharSoft is the proud developer of the best employment platforms in the market. No matter your employment needs, BasharSoft has the solution for you. In total, we have helped over 4 million job seekers in Egypt search for jobs at 50,000 companies. WUZZUF is Egypt’s #1 online career destination platform that targets white collar and highly educated professionals. WUZZUF is an online recruitment platform that helps employers hire the right talent and connects professionals with the right career opportunities. WUZZUF excels in its matchmaking, transparency to its job seekers, its dedicated full lifecycle recruitment support, and the largest database of job seekers and employers in Egypt all in a full-fledged employment marketplace. WUZZUF has a range of sub-categories including:. FORASNA is Egypt’s #1 and most reliable online employment marketplace for blue and white-collar Arabic speakers. The platform services help connect job seekers to employment opportunities with thousands of businesses. Given that blue-collar workers alone represent 66.8% of the total active labor force in Egypt, we built FORASNA so we could play an active role in helping people of all walks of life find jobs and businesses of all kinds find the employees they need. Keep on the lookout because there is always more to come from BasharSoft BasharSoft is a technology firm specialized in developing innovative web-based online employment marketplaces and platforms. We provide the business community with the next generation of talent management and recruitment software systems using the best people, tools and technologies. We achieve this through technology-enabled platforms and services, partnerships, investors and thought leadership. We want to help people and businesses with anything related to employment be it business growth, education, mentoring, career opportunities or otherwise. We want to make people’s lives better through all things employment. Our online recruitment solutions and services have received multiple innovation awards from Egypt and abroad since our humble beginning in 2009. To build ‘efficient employment’ marketplaces and employment ecosystems while enabling social sustainability and positive economics by helping individuals and businesses at scale. We achieve this through technology-enabled platforms and services, partnerships, and thought leadership. Impact: We positively impact society and economy at large. We are purpose driven and work for the greater good. We Care: We truly care about people’s success, happiness, and empathize with their needs. We also care about our work, team, and environment and act like owners – in the best interest of the organization, and follow-through on our actions and decisions."

#     desc_extraction, _ = extract_summary(text, 'Basharsoft', 1000)
#     desc_extraction2, _ = extract_summary(text, None, 1000)

#     print(desc_extraction, '\n', desc_extraction2)

if __name__ == '__main__':
    input_url = gr.Textbox(label='input url')
    input_parse = gr.Dropdown(choices=["bs4getalltext", "bs4simple_customized", "bs4_customized", "costomized_bs4", "boilerpipe", "readability", \
        "html2text", "inscriptis", "inscriptis_annotated", "lxml"])
    input_only_text = gr.Checkbox(label='only_text (to remove format and labels)')
    input_post_process = gr.Checkbox(label='post_process (to clean text)')
    input_ignore_elements = gr.Checkbox(label='ingore_element (to ignore <a>, <img>, <t>)')
    input_min_linewords = gr.Slider(0, 10, value=4, step=1, label='min_linewords (warning: this may remove list items)')
    input_desc_summary = gr.Checkbox(label='description summary (to generate a description from the raw html texts)')
    input_length_descgenerator = gr.Slider(0, 1000, value=500, step=10, label='length of generated description')
    input_abs_summary = gr.Checkbox(label='abstract summary (to generate a abstract from the raw html texts)')
    input_length_absgenerator = gr.Slider(0, 1000, value=500, step=10, label='length of generated abstract')

    demo = gr.Interface(
        fn = parser_integrated,
        inputs = [input_url, input_parse, input_only_text, input_post_process, input_ignore_elements, input_min_linewords, \
            input_desc_summary, input_length_descgenerator, input_abs_summary, input_length_absgenerator],
        outputs=[gr.Textbox(label="original description"), 
                #gr.HighlightedText(label="Highlighted",combine_adjacent=False,),
                gr.Textbox(label="extracted summary"),
                gr.Textbox(label="generated abstract"),
                ])
    demo.launch(server_name = '192.168.61.11')

    # demo = gr.Interface(
    #     fn = list_parser_summary,
    #     inputs = ["text", input_only_text, input_post_process, input_ignore_elements, input_min_linewords, input_length_generator],
    #     outputs=[
    #     gr.Textbox(label="original beautifulsoup"), gr.Textbox(label="extracted description"),
    #     gr.Textbox(label="original costomized_bs4"), gr.Textbox(label="extracted description"),
    #     gr.Textbox(label="original boilerpipe"), gr.Textbox(label="extracted description"),
    #     gr.Textbox(label="original readability"), gr.Textbox(label="extracted description"),
    #     gr.Textbox(label="original html2text"), gr.Textbox(label="extracted description"),
    #     gr.Textbox(label="original inscriptis"), gr.Textbox(label="extracted description"),
    #     gr.Textbox(label="original inscriptis_annotated"), gr.Textbox(label="extracted description"),
    #     gr.Textbox(label="original lxml"), gr.Textbox(label="extracted description"),
    #     ])  
    # demo.launch()


    # web_page = 'https://www.kempen.com/en/about-kempen'
    # web_page = 'https://www.conpak.com/About-Conpak/'
    # web_page = 'https://www.kaiko.com/pages/about-kaiko'
    # web_page = 'https://www.nanyanglaw.com/practices/corporate-secretarial-service/' # desc.supp
    # web_page = 'https://www.asiacititrust.com/contact/contact-singapore/' # desc.supp
    # web_page = 'https://www.rexlot.com.hk/en/business' # desc.supp+general
    # web_page = 'https://www.momentum.co.za/momentum/home'  # difficulte to get desc
    # web_page = 'https://www.userbrain.com/en/pricing/'  # diffcicult to get desc (with table info)
    # web_page = 'https://www.sarlbrillaud-combustibles.fr/vente-gnr-bois-chauffage-aulnay.html' # no english case

    # x, y = greet('https://www.kempen.com/en/about-kempen', 'lxml',  \
    #     only_text=0, post_process=1, ignore_elements=0, min_linewords=0, length=500)
    # print(x, '\n')
    # print(y)
