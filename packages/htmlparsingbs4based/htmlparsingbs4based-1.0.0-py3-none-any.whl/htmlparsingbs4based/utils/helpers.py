import os
import json

def get_crawling_results(website, file_path):

    file_name = website.split('//')[1]
    file_name = file_name.replace('/','{')
    file_name = file_name.replace('?','}')

    json_file = os.path.join(file_path, f'{file_name}.json')
    if not os.path.exists(json_file):
        raise FileNotFoundError(str(json_file))
    
    #-----------------------------------------------
    # if the json file format is incorrect
    w_index = 0
    w_line = 0
    with open(json_file, encoding='utf-8') as f:
        mylist = [line.rstrip('\n') for line in f]
        for i in range(len(mylist)):
            if mylist[i] == '][':
                #print('found:', i)
                w_index = 1
                w_line = i
    
    if w_index == 1:
        with open(json_file, encoding='utf-8') as f:
            data = f.readlines()
        data[w_line-1] = data[w_line-1] + ','
        data[w_line] = ''
        with open(json_file, 'w') as f:
            f.writelines( data )
            #print('successfully writing...')
    #--------------------------------------------------

    with open(json_file, encoding='utf-8') as f:
        for row in json.load(f):
            for url, html in row.items():
                yield url, html