from bs4 import BeautifulSoup, Comment, NavigableString
#import unidecode
import re
from utils.langdetect import detect
from utils.helpers import crawl, get_crawling_results
from utils.elastic import get_pages_from_elastic, get_single_page_from_elastic
from utils.visualization import visual 
import jsonlines, json
import random
import string
import pandas as pd
from tqdm import tqdm
from urllib.parse import unquote

from settings import ELASTIC_PRODUCT_INDEX

import argparse

parser = argparse.ArgumentParser(description='Arguments for HTML parser')
parser.add_argument("-p", "--prefix", help="Define the prefix to the labels", default="")
parser.add_argument("-m", "--min_length", help="Define the min number of words for each line", default=1, type=int)
args = parser.parse_args()
prefix = args.prefix
min_length = args.min_length

def content_str(content):
    content = (' ').join(list(content))
    content = re.sub('\n', ' ', content)
    content = re.sub('\t', ' ', content)
    content = re.sub('\s', ' ', content)
    content = re.sub('\r', ' ', content)
    content = re.sub(' \.', '.', content)
    content = re.sub(' +', ' ', content)
    content = re.sub('\( +', '(', content)
    content = re.sub(' +\)', ')', content)
    content = re.sub('\[ +', '[', content)
    content = re.sub(' +\]', ']', content)
    return content

def containsLetterOrNumber(input):
    has_letter = False
    has_number = False
    for x in input:
        if x.isalpha():
            has_letter = True
        elif x.isnumeric():
            has_number = True
        if has_letter or has_number:
            return True
    return False

def get_inside_embeded(tag, embed_text_list, i):
    for subtag in tag.children:
        if subtag.name in ['strong', 'em', 'b', 'i', 'u', 'sup', 'mark', 'del', 'ins', 'span', 'a']:

            info_inside = False
            if subtag.name in ['a', 'span']:
                for des in subtag.descendants:
                    if str(type(des)) == "<class 'bs4.element.Tag'>" and des.name in ['div', 'p', 'footer', 'img']:
                        info_inside = True
                        break

            if info_inside == False:            
                embed_text = subtag.get_text(' ')
                # if subtag.name in ['a'] and containsLetterOrNumber(embed_text) is False:
                #     embed_text = '#ICON#' 

                if containsLetterOrNumber(embed_text) is True:
                    span_meta = False
                    get_child = "<<" + str(subtag.name) + ">>" + '\t'*(i) + content_str([embed_text.strip()])
                    if subtag.name in ['span']:
                        span_style = subtag.get('style')
                        span_class = subtag.get('class')
                        if 'font-weight:bold' in str(span_style) or 'font-weight:bolder' in str(span_style):
                            get_child = "<<b>>" + '\t'*(i) + content_str([embed_text.strip()])
                        elif 'color:' in str(span_style):
                            get_child = "<<em>>" + '\t'*(i) + content_str([embed_text.strip()])
                        elif span_class != None and 'italic' in (' ').join(span_class):
                            get_child = "<<i>>" + '\t'*(i) + content_str([embed_text.strip()]) 
                        elif span_style != None:
                            span_meta = True

                    if subtag.name == 'a' and subtag.get('href') != None:
                        embed_text_list.append([get_child, ['hyperlink', unquote(subtag.get('href'))] ])
                    elif subtag.name == 'span' and span_meta == True:
                        embed_text_list.append([get_child, ['span', span_style] ])
                    else:
                        embed_text_list.append(get_child)

                get_inside_embeded(subtag, embed_text_list, i+1)

    return embed_text_list

def walker(soup, i, res):
    if soup.name is not None:
        #printnote = False
        '''inspect the child nodes of the current node (soup) '''
        # children = [child.name for child in soup.children]
        # print(soup.name, children)
        for child in soup.children:
            printnote = False
            content = ""
            get_child = ""
            embed_text_list = []
            
            '''if the child name in the following list, we crawl nothing, else we decide whether to inspect this child tag'''
            if str(type(child)) == "<class 'bs4.element.Tag'>" and child.name not in ['html', 'body', 'script', 'noscript', 'style', 'title', 'head', 'meta', 'th', 'td', 'table']:
                inspect_flag = True # the default flag is True
                
                '''if the child tag have children like <div> or <p>, which means we don't inspect it now'''
                for grandchild in child.children:
                    if 'div' == grandchild.name or 'p' == grandchild.name:
                        if content_str([grandchild.get_text(' ')]).strip() != "": 
                            inspect_flag = False
                            break
                
                # if child.name == 'div' and content_str(child.find_all(text=True, recursive=False)).strip() != "":
                #     print(content_str(child.find_all(text=True, recursive=False)))
                if (child.name == 'div' or child.name == 'p') and content_str(child.find_all(text=True, recursive=False)).strip() == "":
                    inspect_flag = False

                if inspect_flag:
                    
                    '''if the child tag can be inspected now, we check if the grandchildren in the embeded tag list
                    if true, we first deal with the embeded text list!
                    we need to make the embeded text get involved (e.g., <p> xxx <a> yyy <\a> <\p> TOBE 'xxx yyy')'''
                    for grandchild in child.children:
                        if grandchild.name in ['strong', 'em', 'b', 'i', 'u', 'sup', 'mark', 'del', 'ins', 'span', 'a']:
                            
                            '''then we check if there is something complicated structures inside the embeded tag
                            we need to pay special attention to <a> and <span> tag 
                            if ['div', 'p', 'footer', 'img'] in <a> or <span>, they are not embeded tag, e.g., <a> xxx <p> xxx <\p> <\a>
                            they should not be treated as an embeded tag but an independent sector
                            '''
                            info_inside = False # the default flag is False
                            if grandchild.name in ['a', 'span']:
                                for des in grandchild.descendants:
                                    if str(type(des)) == "<class 'bs4.element.Tag'>" and des.name in ['div', 'p', 'footer', 'img']:
                                        info_inside = True
                                        break
                            
                            '''if the embeded tag is clean, we extract the embeded text'''
                            if not info_inside:
                                ii = i + 1
                                embed_text = grandchild.get_text(' ') # get_text() will extract all the text from the tag and beneath
                                '''if the embeded text contains no letters/number and the tag is <a>, we put #ICON# to the embeded text'''
                                if grandchild.name in ['a'] and containsLetterOrNumber(embed_text) == False:
                                    embed_text = '#ICON#' 

                                '''1. if the embeded text is contains letter/number, write the text of grandchild to get_child.
                                **if tag is <b> or <i> but not emphasizing text, rename the tag name as <<content>>.
                                **if tag is <span> and has emphasizing style, rename the tag accordingly
                                **if tag is <span> and not emphasizing style, includ the style to metadata
                                **if tag is <a>, include its 'href' attr to metadata
                                2. append get_child to embed_text_list.
                                3. check if there is embeded tags inside embeded tags
                                4. replace the source embeded tag with the plain text (remove the tag info, etc...)
                                '''
                                if containsLetterOrNumber(embed_text):
                                    span_meta = False
                                    if grandchild.name in ['b', 'i', 'sup', 'mark', 'del', 'ins',] and (len(embed_text)/len(child.get_text(' '))> 0.9):
                                        get_child = "<<content>>" + '\t'*(ii) + content_str([embed_text.strip()])
                                    else:
                                        get_child = "<<" + str(grandchild.name) + ">>" + '\t'*(ii) + content_str([embed_text.strip()])
                                    
                                    if grandchild.name in ['span']:
                                        span_style = grandchild.get('style')
                                        span_class = grandchild.get('class')
                                        if 'font-weight:bold' in str(span_style) or 'font-weight:bolder' in str(span_style):
                                            get_child = "<<b>>" + '\t'*(ii) + content_str([embed_text.strip()])
                                        elif 'color:' in str(span_style):
                                            get_child = "<<em>>" + '\t'*(ii) + content_str([embed_text.strip()])
                                        elif span_class != None and 'italic' in (' ').join(span_class):
                                            get_child = "<<i>>" + '\t'*(ii) + content_str([embed_text.strip()]) 
                                        elif span_style != None:
                                            span_meta = True
                                    
                                    if grandchild.name == 'a' and grandchild.get('href') != None:
                                        embed_text_list.append([get_child, ['hyperlink', unquote(grandchild.get('href'))] ])
                                    elif grandchild.name == 'span' and span_meta == True:
                                        embed_text_list.append([get_child, ['span', span_style] ])
                                    else:
                                        embed_text_list.append(get_child)

                                embed_text_list = get_inside_embeded(grandchild, embed_text_list, ii+1)
                                grandchild.replaceWith(embed_text + ' ')

                '''1. if the tag is <div> or <p>, get the text
                2. if the tag is <a> (NOTES: the embeded <a> tag has been processed above, here the <a> tag is not embedded)
                **if <img> in its children, replace <img> tag as placeholder #IMAGE#
                **if ['div', 'p', 'footer', 'img'] in <a>, then is a block, add a dividing line #BLOCK#
                **if ['div', 'p', 'footer', 'img'] not in <a>, get text from the tag, if there is no text, give a placeholder #ICON#
                3. if tag name is <tr> (table row), get the organized table row with '|'
                4. if tag name is <li>, get the text with the beginning of '*'
                5. if tag name is <footer>, add a dividing line #FOOTER#
                6. if tag name is <img>, add placeholder #IMAGE#
                7. if tag name is <h1-h6>, get the text of title
                8. for other tags, just get the text '''
                if child.name in ['div', 'p']: 
                    content = content + content_str(child.find_all(text=True, recursive=False)) 
                elif child.name in ['a']:
                    is_a_block = False
                    for des in child.descendants:
                        if str(type(des)) == "<class 'bs4.element.Tag'>" and des.name in ['div', 'p', 'footer', 'img']:
                            is_a_block = True
                            break
                    if is_a_block == False:
                        content = content_str([child.get_text(' ').strip()])
                        if containsLetterOrNumber(content) == False:
                            content = '#ICON#' 
                    else:
                        #content = '#BLOCK#'  + '\n' + \
                        #        content_str([child.get_text(' ').strip()])
                        if content_str([child.get_text(' ').strip()]) != "":
                            content = '#BLOCK#'  + '\n' + content_str(child.find_all(text=True, recursive=False))
                        
                elif child.name in ['tr']:
                    for grandchild in child.children:
                        if grandchild.name in ['th', 'td']:
                            td_content = content_str([grandchild.get_text(' ').strip()])
                            if td_content == "":
                                td_content = "#ICON#"
                            content = content + '|' + td_content
                    content = content + '|'

                elif child.name in ['li']:
                    content = content_str(child.find_all(text=True, recursive=False)).strip()
                    content = '* ' + content.strip()  
                
                elif child.name in ['footer']:
                    content = '#FOOTER#' + '\n' + content_str(child.find_all(text=True, recursive=False))

                elif child.name in ['img']:
                    content = '#IMAGE#'
                elif child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    content = content_str(child.find_all(text=True, recursive=False)).strip()
                else:
                    content = content_str(child.find_all(text=True, recursive=False)).strip()

            '''form get_child with tag name with extract content
            **if tag name is <a> or <img>, include the metadata
            append get_child to res(ult)'''
            if containsLetterOrNumber(content) is True:
                contents = content.split('\n')
                for line in contents: # if '\n' included in content, we should split it now
                    if (str(child.name) == 'footer' or 'a') and content_str([line.strip()]) not in ['#IMAGE#', '#FOOTER#']:
                        get_child = "<<" + str(child.name) + ">>" + '\t'*(i+1) +  content_str([line.strip()])
                    else:
                        get_child = "<<" + str(child.name) + ">>" + '\t'*(i) +  content_str([line.strip()])
                    if child.name in ['a'] and child.get('href') != None:
                        get_child = [get_child, ['hyperlink', unquote(child.get('href'))]]
                    if child.name in ['img'] and child.get('alt') != None:
                        get_child = [get_child, ['image', unquote(child.get('alt'))]]
                    res.append(get_child)
                # if len(contents) == 2 and (contents[0].strip() == '#BLOCK#' and contents[1].strip() == ''):
                #     printnote = False
                # elif len(contents) == 1 and (contents[0].strip() == '#FOOTER#'):
                #     printnote = False
                # else:    
                printnote = True
            
            '''if embed_text_list is not empty, append the item to res(ult)'''
            if embed_text_list != []:
                for get_child_embed in embed_text_list:
                    res.append(get_child_embed)
                printnote = True
            
            '''if there is nothing print out, we should reduce the current level by 1'''
            j = i + 1
            if printnote == False:
                j = j - 1

            '''walker the child if child name is not <th>, <td>'''
            if child.name not in ['th', 'td']:
                walker(child, j, res)
        return res


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Process results<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #

def find_useful_root(all_tag_info, level, i, r_tag):
    while i > 0:
        lst_tag = all_tag_info[i-1][0] 
        lst_level = all_tag_info[i-1][1]

        if lst_level < level:
            if lst_level == 0:
                return i - 1
            else:
                if lst_tag in ['strong', 'em', 'b', 'i', 'u', 'sup', 'mark', 'del', 'ins', 'a', 'span']:
                    return find_useful_root(all_tag_info, lst_level, i-1, r_tag)
                else:
                    return i - 1
        else:
            i = i - 1

def get_metacontent(meta_info, html_url):
    meta_content = ""
    if meta_info is not None:
        if meta_info[0] == 'hyperlink' and type(meta_info[1]) is str:
            website = meta_info[1]
            if len(website) > 0 and website[0] == '#':
                website = html_url
            if len(website) > 0 and 'javascript' not in website and containsLetterOrNumber(website):
                website = re.sub('\n', '', website)
                website = re.sub('\t', '', website)
                website = re.sub('\r', '', website)
                website = re.sub('\s', '', website)
                website = re.sub(' \.', '.', website)
                website = re.sub(' +', ' ', website)
                if website[0] == '/':
                    domain = get_domain(html_url)
                    website = domain + website
                meta_content = website
        elif meta_info[0] == 'span' and type(meta_info[1]) is str:
            span_text = meta_info[1]
            span_text = re.sub('\n', '', span_text)
            span_text = re.sub('\t', '', span_text)
            span_text = re.sub('\r', '', span_text)
            span_text = re.sub(' \.', '.', span_text)
            span_text = re.sub(' +', ' ', span_text)
            meta_content = span_text
    return meta_content

def get_domain(link):
    domain = ""
    if '//' in link:
        link = link.split('//')[1]
    if '/' in link:
        domain = link.split('/')[0]
    return domain

def traverse_html_with_bs(html, html_url, min_length, prefix):
    # Remove the tag <br/> to <br> as <br/> will not be recognize in BS4
    html = html.replace(' />', '>')
    html = html.replace('/>', '>')
    html = html.replace('<![', '<!--[')
    html = html.replace('&lt;', '<')
    html = html.replace('&gt;', '>')
    soup = BeautifulSoup(html, "html.parser")

    # Remove tags and comments like <style>, <script>, <noscript>, which should not display in the scrapped text
    for data in soup(['style', 'script', 'noscript']):
        data.decompose()
    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()

    # Run walker function, which is to go through the entire tree of the source html
    res = walker(soup=soup, i=0, res=[])

    '''get all tag infomation with tags and corresponding levels
    if the element in res is str, which means tag w.o. metadata
    if the element in res is list, which means the tag with metadata
    all_tag_info = [tag_name, tag_level, line_id, metadata]'''
    all_tag_info = []
    for i, r in enumerate(res):
        if type(r) is str:
            r_tag = r.split('>>')[0][2:]
            level = r.count('\t')
            all_tag_info.append([r_tag, level, i, None])
        else:
            r_tag = r[0].split('>>')[0][2:]
            level = r[0].count('\t')
            all_tag_info.append([r_tag, level, i, r[1]])

    label_list = [[]] * len(res)
    meta_list = [[]] * len(res)
    for ti in all_tag_info:
        r_tag, level, i, meta_info = ti[0], ti[1], ti[2], ti[3]
        #print(r_tag, level, res[i])
        if meta_info != None:
            meta_content = get_metacontent(meta_info, html_url)
        else:
            meta_content = ""
        '''group the tags'''
        if r_tag in ['strong', 'em', 'b', 'i', 'u', 'sup', 'mark', 'del', 'ins',]:
            r_tag_group = prefix + 'highlight'
        elif r_tag in ['a']:
            if get_domain(meta_content) == get_domain(html_url):
                r_tag_group = prefix + 'intralink'
            else:
                r_tag_group = prefix + 'outerlink'
        elif r_tag in ['div', 'p', 'br']:
            r_tag_group = prefix + 'content'
        elif r_tag in ['li', 'ul', 'ol']:
            r_tag_group = prefix + 'list'
        elif r_tag in ['tr']:
            r_tag_group = prefix + 'table_row'
        elif r_tag in ['img']:
            r_tag_group = prefix + 'image'
        elif r_tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            r_tag_group = prefix + 'heading'
        else:
            r_tag_group = prefix + r_tag

        '''if tag in ['strong', 'em', 'b', 'i', 'u', 'a', 'span', 'img'], they may have root
        if they have root, we fill the label_list/meta_list with root_id not the original id,
        if the root_id doesn't exist, we fill the the label_list/meta_list with the original id'''
        if r_tag in ['strong', 'em', 'b', 'i', 'u', 'sup', 'mark', 'del', 'ins', 'a', 'span'] and level > 0:
            if type(res[i]) is str:
                tag_text = res[i].split('>>')[1].strip()
            else:
                tag_text = res[i][0].split('>>')[1].strip()
            if containsLetterOrNumber(tag_text):
                id_root = find_useful_root(all_tag_info, level, i, r_tag)

                if id_root == None or len(tag_text) == 1:
                    label_list[i] = [list([0, len(tag_text), r_tag_group])]
                    if meta_content != "":
                        meta_list[i] = [list([0, len(tag_text), r_tag_group, meta_content])]
                else:
                    if type(res[id_root]) is str:
                        root_text = res[id_root].split('>>')[1].strip()
                    else:
                        root_text = res[id_root][0].split('>>')[1].strip()
                
                    if '#BLOCK#' in tag_text:
                        label_list[i] = [list([0, len(tag_text), prefix + 'blocklink'])]
                    else:
                        start_char = root_text.find(tag_text)
                        # search if span for already exists
                        root_text_ = root_text
                        repeated_flag = True
                        while repeated_flag:
                            for label in label_list[id_root]:
                                if label[0] == start_char and label[2] == r_tag_group:
                                    root_text_ = root_text_[:label[0]] + (label[1]-label[0]) * '#' + root_text_[label[1]:]
                                    start_char = root_text_.find(tag_text)
                                repeated_flag = False

                        if start_char == -1:
                            label_list[i] = [list([0, len(tag_text), r_tag_group])]
                            if meta_content != "":
                                meta_list[i] = [list([0, len(tag_text), r_tag_group, meta_content])]
                            continue
                            
                        end_char = start_char + len(tag_text)
                                                
                        if r_tag not in ['a'] or meta_content != "":
                            if label_list[id_root] == []:
                                label_list[id_root] = [list([start_char, end_char, r_tag_group])]
                            else:
                                label_list[id_root].append(list([start_char, end_char, r_tag_group]))
                        
                        if meta_content != "":
                            if meta_list[id_root] == []:
                                meta_list[id_root] = [list([start_char, end_char, r_tag_group, meta_content])]
                            else:
                                meta_list[id_root].append(list([start_char, end_char, r_tag_group, meta_content]))
                    
        else:
            if type(res[i]) is str:
                text = res[i].split('>>')[1].strip()
            else:
                text = res[i][0].split('>>')[1].strip()
            if '#BLOCK#' in text:
                label_list[i] = [list([0, len(text), prefix + 'blocklink'])]
            elif '#FOOTER#' in text:
                if level == 0:
                    label_list[i] = [list([0, len(text), prefix + 'footer'])]
                else:
                    label_list[i] = [list([0, len(text), prefix + 'local_footer'])]
            else:
                start_char = 0
                end_char = len(text)
                if label_list[i] == []:
                    label_list[i] = [list([start_char, end_char, r_tag_group])]
                else:
                    label_list[i].append(list([start_char, end_char, r_tag_group]))

                meta_content = get_metacontent(meta_info, html_url)
                if meta_content != "":
                    if meta_list[i] == []:
                        meta_list[i] = [list([start_char, end_char, r_tag_group, meta_content])]
                    else:
                        meta_list[i].append(list([start_char, end_char, r_tag_group, meta_content]))


    
    doc = ""
    label_assemble = []
    meta_assemble = []
    section_id, footer_id = [], []
    r_text_last = ""
    level_last = 0
    for i, r in enumerate(res):
        if label_list[i] != []:
            level = all_tag_info[i][1]
            if type(r) is str:
                r_text = r.split('>>')[1].strip()
            else:
                r_text = r[0].split('>>')[1].strip()
            if (r_text in r_text_last and level > level_last) or (r_text.strip('*').strip() == r_text_last.strip('*').strip()):
              continue
            '''set the min_length'''
            if len(r_text.split(' ')) < min_length:
                continue

            if containsLetterOrNumber(r_text):

                if section_id != []:
                    if level <= section_id[-1][1]:
                        sec_id = section_id[-1][0]
                        label_list[sec_id][0][1] = len(doc)
                        section_id.pop()
                        if label_list[sec_id][0][0] != label_list[sec_id][0][1]:
                            label_assemble.append(label_list[sec_id][0])
                if footer_id != []:
                    if level <= footer_id[-1][1]:
                        ft_id = footer_id[-1][0]
                        label_list[ft_id][0][1] = len(doc)
                        footer_id.pop()
                        if label_list[ft_id][0][0] != label_list[ft_id][0][1]:
                            label_assemble.append(label_list[ft_id][0])

                if '#BLOCK#' in r_text:
                    label_list[i][0][0] = len(doc)
                    label_list[i][0][1] = len(doc)
                    section_id.append(list([i,level]))
                elif '#FOOTER#' in r_text:
                    label_list[i][0][0] = len(doc)
                    label_list[i][0][1] = len(doc)
                    footer_id.append(list([i,level]))

                else:
                    for j, lb in enumerate(label_list[i]):
                        label_list[i][j][0],  label_list[i][j][1] = lb[0]+level+len(doc), lb[1]+level+len(doc)
                        label_assemble.append(label_list[i][j])

                    if meta_list[i] != []:
                        for j, lb in enumerate(meta_list[i]):
                            meta_list[i][j][0],  meta_list[i][j][1] = lb[0]+level+len(doc), lb[1]+level+len(doc)
                            meta_assemble.append(meta_list[i][j])

                doc = doc + '\t'*level + r_text + '\n'
                r_text_last = r_text
                level_last = level
    

    if section_id != []:
        sec_id = section_id[-1][0]
        label_list[sec_id][0][1] = len(doc)
        section_id.pop()
        if label_list[sec_id][0][0] != label_list[sec_id][0][1]:
            label_assemble.append(label_list[sec_id][0])
    if footer_id != []:
        ft_id = footer_id[-1][0]
        label_list[ft_id][0][1] = len(doc)
        footer_id.pop()
        if label_list[ft_id][0][0] != label_list[ft_id][0][1]:
            label_assemble.append(label_list[ft_id][0])


    for i, lbel in enumerate(label_assemble):
        try:
            if doc[lbel[1]-1] == '\n':
                label_assemble[i] = [lbel[0], lbel[1]-1, lbel[2]]
        except:
            print(html_url)

    doc_dict = {'text': doc, 'labels': label_assemble, 'metadata': meta_assemble}
    return doc_dict





def parse_single_page(input_url, visualization):
    get_pages_from = 'local' # 'elasticsearch' or 'local' 
    file_exist = True
    if get_pages_from == 'local':
        itera = get_crawling_results(input_url)
        try:
            for url, page in itera:
                if url: 
                    html_url = url
                    html_page = page
                break # only get one page for each input
        except:
            print('ERROR:cannot get html ', input_url)
            file_exist = False
        
    elif get_pages_from == 'elasticsearch':
        f = get_single_page_from_elastic(index=ELASTIC_PRODUCT_INDEX, url=input_url)
        if len(f) > 0:
            for i, item in enumerate(f[0]):
                try:
                    html_page = item['_source']['content']
                    html_url = item['_source']['pageUri']
                    print(html_url)
                except:
                    print('Html content missing: %s'%input_url)
                    file_exist = False
                break # only get one page for each input
    
    if file_exist:
        doc_dict = traverse_html_with_bs(html_page, html_url, min_length, prefix)
        text = doc_dict["text"]
        #print(text)
        my_file = open('my_file.txt', 'w')
        my_file.write(text)
        my_file.close()
        print(doc_dict["labels"])
        #print(text[7117:7470])
        meta_cont = doc_dict["metadata"]
        meta_conta = []
        for itema in meta_cont:
            meta_conta.append([itema[0], itema[1], itema[3]])
        if visualization:
            visual(text, doc_dict["labels"], "./v_example1.html")
            visual(text, meta_conta, "./v_example_m1.html")


def generate_jl(file_path):
    with open(file_path) as f:
        lines = f.read().splitlines()
    my_dict = {}
    for i, line in enumerate(lines):
        try:
            my_dict[i] = json.loads(line)
        except:
            pass
    df = pd.DataFrame.from_dict(my_dict).T
    #df = df[:10]
    num = 1
    get_pages_from = 'local' # 'elasticsearch' or 'local' 
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        if get_pages_from == 'local':
            itera = get_crawling_results(row['data'])
            try:
                for url, page in itera:
                    if url: 
                        html_url = url
                        html_page = page
                    break # only get one page for each input
            except:
                print('ERROR:cannot get html ', row['data'])
                continue
        
        elif get_pages_from == 'elasticsearch':
            f = get_single_page_from_elastic(index=ELASTIC_PRODUCT_INDEX, url=row['data'])
            if len(f) > 0:
                for i, item in enumerate(f[0]):
                    try:
                        html_page = item['_source']['content']
                        html_url = item['_source']['pageUri']
                        print(html_url)
                    except:
                        print('Html content missing: %s'%row['data'])
    
        try:
            doc_dict = traverse_html_with_bs(html_page, html_url, min_length, prefix)
            text = doc_dict["text"]
            if len(text) >= 10:
                doc_dict["doc_id"] = num
                doc_dict["finquest_id"] = row['finquest_id']
                doc_dict["company_name"] = row['company_name']
                doc_dict["original_url"] = html_url
                doc_dict["english"] = row['english']  
            
                with jsonlines.open('./html_parsing.jl', mode='a') as writer:
                    writer.write(doc_dict)
                num += 1
        
        except:
           print('ERROR:parsing problem ', row['data'])
           continue


if __name__ == '__main__':
    '''
    example urls:
    https://www.kempen.com/en/about-kempen
    https://www.userbrain.com/en/pricing/
    https://www.conpak.com/About-Conpak/
    https://www.kaiko.com/pages/about-kaiko
    https://www.momentum.co.za/momentum/home
    https://www.nanyanglaw.com/practices/corporate-secretarial-service/
    https://www.asiacititrust.com/contact/contact-singapore/ # desc.supp
    https://www.rexlot.com.hk/en/business # desc.supp+general
    https://www.sarlbrillaud-combustibles.fr/vente-gnr-bois-chauffage-aulnay.html # no english case

    problematic urls:
    https://www.colosseumdental.com/who-we-are/meet-our-team # for any tag if only <ul>,<ol>,<li> in chidren, then recrusive = False
    https://www.tradewindsnwi.org/contact/ # address
    https://www.kempen.com/en/corporate-finance # more than one footer
    https://www.thailandwastemanagement.com/about-us/ # non-latin lang
    https://www.wittur.com/en/wittur-group/sustainability-environment-health--safety-and-quality.aspx
    https://www.talaviation.com/News
    https://vincoconstruction.com/
    https://www.mineexcellence.com/
    https://www.felcaroroldan.com/ # order/level problem

    https://www.metex.it/it/azienda
    '''
    #parse_single_page(input_url='http://www.mineracamargo.com/MCA_Investors.html', visualization=False)
    generate_jl(file_path='/home/yaxiong/backupfiles/descriptionextraction_data/description_annotation_final_dontdelete.jl')

