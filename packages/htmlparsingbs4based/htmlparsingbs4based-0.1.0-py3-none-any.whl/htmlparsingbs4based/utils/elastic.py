from elasticsearch import Elasticsearch
import re
from settings import ELASTIC_URI

def get_single_page_from_elastic(index, url, elastic_user, elastic_password):
    # Create the client instance
    es = Elasticsearch(
        ELASTIC_URI,
        basic_auth=(elastic_user, elastic_password),
        request_timeout=120
    )
    
    # wildcard query with website.keyword, to find *.domain* or */domain*, limit find maximum 20 pages
    if '//' in url:
        url = url.split('//')[1]
    url_main = re.sub('^www\.', '', url)
    url_domain = url_main.split('/')[0]
    #print(url)
    #print(url_main)

    html = es.options(request_timeout=120, max_retries=5).search(
    index=index,
    size= "20",
    query={
            "term": {
            "website.keyword": {
                    "value": url.split('/')[0]
                }
            }
        })
    pages = html['hits']['hits']    
    if len(pages) == 0:
        html = es.options(request_timeout=120, max_retries=5).search(
            index=index,
            size="20",
            query={
                    "wildcard": {
                    "website.keyword": {
                        "value": "*.%s*"%url_domain
                        }
                    }
                })
        pages = html['hits']['hits']
        if len(pages) == 0:
            html = es.options(request_timeout=120, max_retries=5).search(
            index=index,
            size= "20",
            query={
                    "wildcard": {
                    "website.keyword": {
                        "value": "*/%s*"%url_domain
                        }
                    }
                })
            pages = html['hits']['hits']
    return pages