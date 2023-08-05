import gradio as gr
import os
#os.system('python -m spacy download en_core_web_sm')
import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")

def text_analysis(text):
    doc = nlp(text)
    html = displacy.render(doc, style="dep", page=True)
    html = (
        ""
        + html
        + ""
    )
    pos_count = {
        "char_count": len(text),
        "token_count": 0,
    }
    pos_tokens = []

    for token in doc:
        pos_tokens.extend([(token.text, token.pos_), (" ", None)])

    return pos_tokens, pos_count, html


def text_analysis2(texts):

    # te_li = text.split(' ')
    # fi_li = []
    # for i in te_li:
    #     if 'a' in i:
    #         fi_li.append((i, 'word'))
    #         fi_li.append(('\n', 'change'))
    #     else:
    #         fi_li.append((i, 'word2'))
    #     fi_li.append((' ', None))
    if texts == 'abc':
        se = "What a beautiful \n morning for a walk!"
    fi_li = {'text': se, 'entities': [{'entity': 'word', 'start': 1, 'end': 3}, {'entity': 'word2', 'start': 7, 'end': 9}]}

    return fi_li, se
        
        

# a = text_analysis2("What a beautiful \n morning for a walk!")
# print(a)


demo = gr.Interface(
    text_analysis2,
    [gr.Textbox(placeholder="Enter sentence here...")],
    #["highlight", "json", "html"],
    [gr.HighlightedText(
        label="Highlighted",
        combine_adjacent=True,),
    gr.Textbox(value='original')],
    examples=[
        ["What a beautiful morning for a walk!"],
        ["It was the best of times, it was the worst of times."],
    ],
)

demo.launch()