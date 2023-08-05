import os

ROOT = os.path.abspath(os.path.dirname(__file__))

ELASTIC_USER = os.environ.get('ELASTIC_USER', "readwrite")
ELASTIC_URI = os.environ.get('ELASTIC_URI', "http://p-elscrawling-001.elinkapp.com:9200/,http://p-elscrawling-002.elinkapp.com:9200/,http://p-elscrawling-003.elinkapp.com:9200/").split(',')
ELASTIC_PRODUCT_INDEX = os.environ.get('ELASTIC_PRODUCT_INDEX', "webpages1")
ELASTIC_TEST_INDEX = os.environ.get('ELASTIC_TEST_INDEX', "test002")
ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD', "")