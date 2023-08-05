from elasticsearch import Elasticsearch
import re
from settings import ELASTIC_URI, ELASTIC_USER
from settings import ELASTIC_PASSWORD

# Create the client instance
es = Elasticsearch(
    ELASTIC_URI,
    basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    request_timeout=120
)

def get_pages_from_elastic(index, url):
    # wildcard query with website.keyword, to find *.domain* or */domain*, limit find maximum 20 pages
    
    try:
        url = url.split('//')[1]
    except:
        pass
    url = url.split('/')[0]
    domain = re.sub('^www\.', '', url)

    html = es.options(request_timeout=120, max_retries=5).search(
    index=index,
    size= "20",
    query={
            "term": {
            "website.keyword": {
                    "value": url
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
                        "value": "*.%s*"%domain
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
                        "value": "*/%s*"%domain
                        }
                    }
                })
            pages = html['hits']['hits']
    return pages


def get_single_page_from_elastic(index, url):
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