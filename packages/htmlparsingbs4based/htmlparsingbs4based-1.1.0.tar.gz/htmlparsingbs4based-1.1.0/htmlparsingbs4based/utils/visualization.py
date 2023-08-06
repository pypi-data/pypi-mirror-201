import spacy
from spacy import displacy
from spacy.tokens import Span
import json
from pathlib import Path


def visual(document, labels, output_path):
    colors = {
        'highlight': "#eb3434",
        'intralink': "#db34eb",
        'outerlink': "#11A0E7",
        'content': "#345beb",
        'list': "#34ebcf",
        'table_row': "#6beb34",
        'image': "#d5eb34",
        'heading': "#eb9534",
        'span': "#9534eb",
        'button': "#349beb",
        'section': "#11E79F",
        'footer': '#E75511'
    }
    options = {"ents": colors.keys(), "colors": colors} 


    text = document.replace('\t', '⮞')
    nlp = spacy.blank("en")
    #doc = nlp(text)
    cursor = 0
    for ln in text.split('\n'):
        doc = nlp(str(ln))
        list_spans = []
        for label in labels:
            start_char_position = label[0]
            end_char_position = label[1]
            label_name = label[2]
            if (start_char_position >= cursor) and (end_char_position <= (cursor + len(ln))):
                span = doc.char_span(label[0] - cursor, label[1] - cursor, label[2])
                # span = Span(doc, label[0] - cursor, label[1] - cursor, label[2])
                list_spans.append(span)
        doc.spans["sc"] = list_spans
        #print(list_spans)
        #displacy.render(doc, style='span', jupyter=True, options=options)
        html = displacy.render(doc, style="span", options=options)
        output_path = Path(output_path)
        output_path.open("a", encoding="utf-8").write(html)
        cursor += (len(ln) + 1)
        #break

def check_file(doc_id):
    with open("/home/yaxiong/descriptionextraction/html_parsing.jl") as f:
        lines = f.read().splitlines()
    for i, line in enumerate(lines):
        try:
            if i == doc_id-1:
                #print(line)
                my_dict = json.loads(line)
                text = my_dict["document"]
                print(text)
                my_file = open('my_file.txt', 'w')
                my_file.write(text)
                my_file.close()
                langua = my_dict["english"]
                
                print('*'*50)
                print(f"company_name: \t {my_dict['company_name']}")
                print(f"original_url: \t {my_dict['original_url']}")
                print(f"doc_id: \t {my_dict['doc_id']}")
                print(f"finquest_id: \t {my_dict['finquest_id']}")
                print(f"english: \t {my_dict['english']}")
                print('*'*50)
                
                meta_cont = my_dict["metadata"]
                meta_conta = []
                for itema in meta_cont:
                    meta_conta.append([itema[0], itema[1], itema[3]])
                visual(text, my_dict["labels"], "./visualization_labels_%i.html" %i)
                visual(text, meta_conta, "./visulization_metadata_%i.html" %i)
                break
        except:
            print(i)
            pass
            break

if __name__ == '__main__':
    check_file(doc_id=1)