import re

d = {'Help | Privacy Statement | Personal Information Collection Statement | Disclaimer Statement | Site Map | Our Apps | Useful Link | Bookmark Page': {'Help  |': [None, '("/Help.html")'], 'Privacy Statement  |': [None, '("/Privacy-Statement.html")'], 'Personal Information Collection Statement  |': [None, '("/PICS.html")'], 'Disclaimer Statement  |': [None, '("/Disclaimer-Statement.html")'], 'Site Map  |': [None, '("/Sitemap.html")'], 'Our Apps  |': [None, '("/app/hk-iit/")'], 'Useful Link  |': [None, '("/Useful-Links.html")'], 'Bookmark Page': [None, '("javascript:window.external.AddFavorite(location.href,\'【Conpak CPA Limited.】\'+document.title);")']}}
d = {'© 1998-2022 Conpak CPA Ltd. All rights reserved.': {'Conpak CPA Ltd.  All rights reserved.': [None, '("/")']}}
entities_list = []
highlight_text = ''
i = 0
for txt, label in d.items():
    print(txt, '\n')
    if label in ['tit', 'img', 'li', 'tab', 'ft', 'eft']:
        highlight_text = highlight_text + ' ' + txt + '$'
        entities_list.append({'entity': label, 'start': i, 'end': i+1})
        i = len(highlight_text)
    elif type(label) is dict:
        j = 0
        end_logger = 0
        for subtxt, sublabel in label.items():
            subtxt = re.sub(" +", " ", subtxt)
            if j == 0:
                highlight_text = highlight_text + ' '
                entities_list.append({'entity': sublabel[0], 'start': i, 'end': i+1})
                i = len(highlight_text)
            
            start_index = end_logger + txt[end_logger:].find(subtxt)
            end_logger = start_index + len(subtxt)
            end_index = start_index + len(subtxt) + len(' ' + sublabel[1])

            #end_logger = len(txt[:end_index] + ' ' + sublabel[1])
            txt = txt[:end_logger] + ' ' + sublabel[1] + txt[end_logger:]
            start_index_plus_i = i + start_index
            end_index_plus_i = i + end_index
            entities_list.append({'entity': 'url', 'start': start_index_plus_i, 'end': end_index_plus_i})
            j += 1
        highlight_text = highlight_text + txt + '$'
        i = len(highlight_text)

print(highlight_text)