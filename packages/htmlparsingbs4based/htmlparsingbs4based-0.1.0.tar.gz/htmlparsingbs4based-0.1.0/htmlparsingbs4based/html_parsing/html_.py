from typing import List, Set

from boilerpy3.extractors import ArticleExtractor
from bs4 import BeautifulSoup, Comment, NavigableString
import unidecode
import re
from description_extraction.utils.langdetect import detect
from googletrans import Translator
from description_extraction.crawling.helpers import crawl, get_crawling_results

googlemt_model = Translator() # google translation model api configure
cookie_keywords = set(
    ['accept', 'policy', 'analytics', 'agree', 'collect', 'site', 'experience', 'data', 'help', 'traffic',
     'information', 'setting', 'performance', 'read', 'change', 'preference', 'enable',
     'security', 'analys', 'improve', 'use', 'gather', 'find', 'advertis', 'click', 'consent', 'enhance',
     'provide', '3rd', 'third', 'terms', 'statement', 'review', 'store', 'deliver', 'technolog', 'disclaim'])

need_tags = ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'img', 'table']
ignored_tags = ['title', 'script', 'noscript', 'style']

def trim_space(s):
    if s.startswith(' ') or s.endswith(' '):
        return re.sub(r"^(\s+)|(\s+)$", "", s)
    else:
        return s

def append_links(tag, current_text):
    try:
        cur_tag_text = current_text[-1].split('\n')
        link_list = []
        for subtag in tag.findAll("a", href=True):
            link_list.append([subtag.get_text(), subtag.get("href")])
        deleted_list = []
        for i in range(len(cur_tag_text)):
            for j in range(len(link_list)):
                if link_list[j][0] in cur_tag_text[i] and j not in deleted_list:
                    start_index = cur_tag_text[i].find(link_list[j][0])
                    end_index = start_index + len(link_list[j][0])
                    if link_list[j][0].strip() != '' and start_index != -1 and '<a>:' not in cur_tag_text[i][start_index-5:start_index]:
                        cur_tag_text[i] = cur_tag_text[i][:start_index] + '<a>: ' + cur_tag_text[i][start_index:end_index] + ' (<' + link_list[j][1] + '>)' + cur_tag_text[i][end_index:]
                        deleted_list.append(j)
        cur_tag_text = '\n'.join(cur_tag_text)
        current_text[-1] = cur_tag_text
    except:
        pass


def content_from_html_with_bs(html: str, tag_remove, ignore_elements, accepted_languages: Set[str] = {'en'}) -> str:
    """Extract text from HTML page while ignoring specific HTML tags.

    Args:
        html (str): HTML text in string
        ignored_tags (list): HTML tags to ignore

    Returns:
        str: text in HTML after removing all relevant tags
    """

    #print(html)
    non_english = False
    soup = BeautifulSoup(html, "html.parser")
    footer_tags = []
    for script in soup(['footer']):
        footer_tag = script.extract()
        footer_tags.append(footer_tag)
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    
    # get clean html
    #clean_html = soup.prettify()
    # print(clean_html)

    # # get all links 
    # for link in soup.find_all('a'):
    #    print(link.get('href'))

    texts = []
    tag_texts_last, tag_lists_last = '', ''
    #to be done: 'header', 'section', 'footer'
    
    # get all paragraphs    
    texttags = soup.find_all(need_tags)
    #print(paragraphs)

    num_tot_tags, num_tags, num_p_tags, num_ne_tags = len(texttags), 0, 0, 0
    text_chunk = '' # for tmp translation
    ii = 0 # iter
    for tag in texttags:
        ii += 1
        #print(tag.name)
        #print(tag.contents)

        if tag.name == 'ul' or tag.name == 'ol':
            for script in tag(['p', 'table']):
                script.extract()
            tag_text = tag.get_text("\n<li>: ", strip=True) if tag_remove == 0 else tag.get_text("\n", strip=True)
        elif tag.name == 'div':
            tag_text_list = tag.find_all(text=True, recursive=False)
            tag_text_list = [trim_space(s) for s in tag_text_list]
            tag_text =  ' '.join(tag_text_list)
        elif tag.name == 'table':
            for script in tag(['p', 'ul', 'ol']):
                script.extract()
            tag_text = tag.get_text(" ", strip=True)
        elif tag.name == 'img':
            tag_text = tag.get("alt")
        else:
            tag_text = tag.get_text(" ", strip=True)

        # if trim_space(tag_text) in temp:
        #     continue
        # else:
        #     temp.append(trim_space(tag_text))

        # conditions for skipping tags
        try:
            if (tag_text in tag_texts_last) or (tag_text in tag_lists_last):
                continue
            else:
                pass
        except:
            continue
        
        if tag.name=='p' or tag.name=='div':
            tag_texts_last = tag_text
        else:
            tag_lists_last = tag_text
        num_tags += 1
        
        tag_lines = tag_text.split('\n')
        num_lines, num_ne_lines = len(tag_lines), 0

        sub_texts = []
        for line in tag_lines:
            line = ' '.join(line.split())
            if tag.name == 'p' or tag.name == 'div':
                if len(line) < 50:
                    continue
            if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol']:
                if len(line) < 2:
                    continue
            #line = re.sub(r' +', ' ', line)
            #line = line.strip(' ')
            lang = detect(line)
            if lang not in accepted_languages:
                num_ne_lines += 1
                #continue
                sub_texts.append(line)
            else:
                sub_texts.append(line)

        if len(sub_texts) > 0:
            sub_texts =  ' '.join(sub_texts) if (tag.name != 'ul' and tag.name != 'ol') else '\n'.join(sub_texts)
            sub_texts = unidecode.unidecode(sub_texts)
            
            # translation
            if num_lines > 0 and num_ne_lines/num_lines > 0.2: #non-English tag
                num_ne_tags += 1
            
            if tag.name == 'ul' or tag.name == 'ol':
                texts.append('<li>: ' + sub_texts) if tag_remove == 0 else texts.append(sub_texts)
                append_links(tag, texts) if (ignore_elements == 0 and tag_remove == 0) else 0
            elif tag.name == 'p' or tag.name == 'div':
                texts.append('<txt>: ' + sub_texts) if tag_remove == 0 else texts.append(sub_texts)
                append_links(tag, texts) if (ignore_elements == 0 and tag_remove == 0) else 0
                num_p_tags += 1
            elif tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                texts.append('<tit>: ' + sub_texts) if tag_remove == 0 else texts.append(sub_texts)
                append_links(tag, texts) if (ignore_elements == 0 and tag_remove == 0) else 0
            elif tag.name == 'table' and ignore_elements == 0:
                texts.append('<tab>: ' + sub_texts) if tag_remove == 0 else texts.append(sub_texts)
                append_links(tag, texts) if (ignore_elements == 0 and tag_remove == 0) else 0
            elif tag.name == 'img' and ignore_elements == 0:
                texts.append('<img>: ' + sub_texts) if tag_remove == 0 else texts.append(sub_texts)
                append_links(tag, texts) if (ignore_elements == 0 and tag_remove == 0) else 0
            # to be continue: add <a> and <img>

    if len(footer_tags) > 0:
        for tag in footer_tags[0]:
            if isinstance(tag, NavigableString):
                continue
            tag_text = tag.get_text(" ", strip=True)
            tag_lines = tag_text.split('\n')
            sub_texts = []
            for line in tag_lines:
                line = ' '.join(line.split())
                lang = detect(line)
                if lang not in accepted_languages:
                    continue
                sub_texts.append(line)
            if len(sub_texts) >= 0:
                sub_texts =  ' '.join(sub_texts)
                sub_texts = unidecode.unidecode(sub_texts)
                texts.append('<ft>: ' + sub_texts) if tag_remove == 0 else texts.append(sub_texts)
                append_links(tag, texts) if (ignore_elements == 0 and tag_remove == 0) else 0


    if num_tags > 0 and num_p_tags > 0 and num_ne_tags/num_tags < 0.2:
        texts =  '\n'.join(texts)
        texts = unidecode.unidecode(texts)
    else:
        non_english = True
        texts =  '\n'.join(texts)
        texts = unidecode.unidecode(texts)



    # https://stackoverflow.com/a/24618186
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    # for script in soup(ignored_tags):
    #     script.extract()
    # text = soup.get_text()
    # text = '\n'.join([line for line in text.split('\n') if line.strip()])
    return texts, non_english


def extract_content_from_html_with_boilerpipe(html: str, accepted_languages: Set[str] = {'en'}) -> str:
    """Extract relevant/important texts from HTML pages using Boilerpipe.

    Args:
        html (str): webpage content in HTML format
        accepted_languages (set): paragraphs in languages not specified in this set are disregarded

    Returns:
        str: extracted text concatenated by a new line
    """
    # extractor = Extractor(extractor='CanolaExtractor', html=html)
    extractor = ArticleExtractor()
    texts = []
    non_en = False
    try:
        text = str(extractor.get_content(html))
        non_en_count = 0
        for line in text.split('\n'):
            lang = detect(line)
            if not line:
                continue
            if lang not in accepted_languages:
                non_en_count += 1
                continue
            if len(line.strip()) < 20:
                continue
            lower = line.lower()
            cookie = False
            if 'cookie' in lower or 'privacy' in lower:
                for kw in cookie_keywords:
                    if kw in lower:
                        cookie = True
                        break
            if not cookie:
                texts.append(line)
        non_en = (non_en_count/len(text.split('\n'))>0.5)
    except UnicodeDecodeError:
        return ''
    except:
        pass
    texts =  '\n'.join(texts)
    texts = unidecode.unidecode(texts)
    return texts
            
