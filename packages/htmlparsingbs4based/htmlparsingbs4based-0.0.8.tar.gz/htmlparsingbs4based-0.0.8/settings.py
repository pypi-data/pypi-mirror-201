import os

ROOT = os.path.abspath(os.path.dirname(__file__))

ELASTIC_URI = os.environ.get('ELASTIC_URI', "http://p-elscrawling-001.elinkapp.com:9200/,http://p-elscrawling-002.elinkapp.com:9200/,http://p-elscrawling-003.elinkapp.com:9200/").split(',')
ELASTIC_PRODUCT_INDEX = os.environ.get('ELASTIC_PRODUCT_INDEX', "webpages1")
