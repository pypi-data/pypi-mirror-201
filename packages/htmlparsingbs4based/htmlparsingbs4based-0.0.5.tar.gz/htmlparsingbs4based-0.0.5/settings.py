import os

ROOT = os.path.abspath(os.path.dirname(__file__))
DEBUG = bool(int(os.environ.get('DEBUG', '1')))
CACHE = bool(int(os.environ.get('CACHE', '0')))

PHRASE_MATCHER_FILE = os.path.join(ROOT, 'models', 'bin', 'phrase_matcher.pickle')

LOGGER_NAME = 'description_extract'

CRAWLER_USER_AGENT = os.environ.get(
    'CRAWLER_USER_AGENT',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 '
    'Safari/537.36'
)

CRAWLER_RESULTS_DIR = os.environ.get('CRAWLER_RESULTS_DIR', os.path.join(ROOT, 'results'))
"""str: Directory to save crawling results and reading results from, defaults to 'results' under project root.

You may update this setting by setting the environment variable, e.g.: ``CRAWLER_RESULTS_DIR=/tmp/results``.
"""

CRAWLER_DEPTH_LIMIT = int(os.environ.get('CRAWLER_DEPTH_LIMIT', '2'))
"""int: The max depth our crawler with crawl for any website.

You may update this setting by setting the environment variable, e.g.: ``CRAWLER_DEPTH_LIMIT=3``.
"""

CRAWLER_PAGE_LIMIT = int(os.environ.get('CRAWLER_PAGE_LIMIT', '200'))
"""int: The max number of pages our crawler with crawl for any website.

You may update this setting by setting the environment variable, e.g.: ``CRAWLER_PAGE_LIMIT=100``.
"""

REQUEST_QUEUE_NAME = os.environ.get('REQUEST_QUEUE_NAME', 'Learning.DescriptionExtractionRequests')
REQUEST_EXCHANGE_NAME = os.environ.get('REQUEST_EXCHANGE_NAME', REQUEST_QUEUE_NAME)
RESPONSE_EXCHANGE_NAME = os.environ.get('RESPONSE_EXCHANGE_NAME', 'Learning.DescriptionExtractionResponses')

MESSAGE_RESPONSE_TYPENAME = os.environ.get(
    'MESSAGE_RESPONSE_TYPENAME', "urn:message:FinQuest.Rabbit.Interfaces:IProcessDescriptionExtraction"
)

PROBABILITY_THRESHOLD = float(os.environ.get('PROBABILITY_THRESHOLD', '0.5'))

ELASTIC_USER = os.environ.get('ELASTIC_USER', "readwrite")
ELASTIC_URI = os.environ.get('ELASTIC_URI', "http://p-elscrawling-001.elinkapp.com:9200/,http://p-elscrawling-002.elinkapp.com:9200/,http://p-elscrawling-003.elinkapp.com:9200/").split(',')
ELASTIC_PRODUCT_INDEX = os.environ.get('ELASTIC_PRODUCT_INDEX', "webpages1")
ELASTIC_TEST_INDEX = os.environ.get('ELASTIC_TEST_INDEX', "test002")
HOME_DIR = os.environ.get('HOME', '.')
LANGUAGE_DETECTION_MODEL_PATH = os.path.join(HOME_DIR, 'descriptionextraction', 'description_extraction', 'models', 'bin', 'langdetect.bin')
ANNOTATORS_WORK_DIR = os.path.join(HOME_DIR, 'descriptionextraction', 'description_extraction', 'annotators_work_dir')

MLFLOW_S3_ENDPOINT_URL = 'http://d-gpu-002.elinkapp.com:9000'
MLFLOW_TRACKING_URI = 'http://d-gpu-002.elinkapp.com:5100'
MLFLOW_URI_CUSTOM_NER = 'runs:/609b4dfc1862435d892a3f8469ecb8c3/model'   # The same model being used in annotation_ws (BiLSTM)
MLFLOW_RUN_ID_MULTI_PASSAGE_CLASSIF = '4aed9f17441041769918159ee5bee4c7'   # Latest conditional model trained
DEFAULT_SETTINGS_MULTI_PASSAGE_CLASSIF = {
    "MULTI_PASSAGE_CLASSIF_MODEL_IS_SEQUENTIAL": True,
    "MULTI_PASSAGE_CLASSIF_MODEL_IS_CONDITIONAL": True,
    "MULTI_PASSAGE_CLASSIF_WINDOW_SIZE": 5,
    "MULTI_PASSAGE_CLASSIF_WINDOW_IS_CENTERED": False,
    "MULTI_PASSAGE_CLASSIF_MODEL_NB_PREV_CLASS_TO_CONSIDER": 1
}

CUDA_DEVICE_NAME = os.environ.get('CUDA_DEVICE_NAME', 'cuda:1')

# Most recent version of fine-grained NER labels

NER_LBL_ORG_FOCUS = 'Organization.focus'
NER_LBL_ORG_BRAND = 'Organization.brand'
NER_LBL_ORG_SUBSIDIARY = 'Organization.subsidiary'
NER_LBL_ORG_PARENT = 'Organization.parent'
NER_LBL_ORG_CLIENT_PARTNER = 'Organization.client/partner'
NER_LBL_ORG_COMPETITOR = 'Organization.competitor'
NER_LBL_ORG_MISC = 'Organization.miscellaneous'
NER_LBL_ORG_NOISE = 'Organization.noise'
NER_LBL_PER_FOCUS = 'Person.focus'
NER_LBL_PER_FOUNDER = 'Person.founder'
NER_LBL_PER_EMPLOYEE = 'Person.employee'
NER_LBL_PER_CLIENT_PARTNER = 'Person.client/partner'
NER_LBL_PER_MISC = 'Person.miscellaneous'
NER_LBL_PER_NOISE = 'Person.noise'
NER_LBL_DAT_CREATION = 'Date.creation'
NER_LBL_DAT_DEFUNCTION = 'Date.defunction'
NER_LBL_DAT_ACQUISITION = 'Date.acquisition'
NER_LBL_DAT_MISC = 'Date.miscellaneous'
NER_LBL_DAT_NOISE = 'Date.noise'
NER_LBL_LOC_HEADQUARTERS = 'Location.headquarters'
NER_LBL_LOC_COVERAGE = 'Location.coverage'
NER_LBL_LOC_MISC = 'Location.miscellaneous'
NER_LBL_LOC_NOISE = 'Location.noise'
NER_LBL_QTY_REVENUE = 'Quantity.revenue'
NER_LBL_QTY_PROFIT = 'Quantity.profit'
NER_LBL_QTY_DEBT = 'Quantity.debt'
NER_LBL_QTY_MISC = 'Quantity.miscellaneous'
NER_LBL_QTY_NOISE = 'Quantity.noise'
NER_LBL_SRV_SENTENCE = 'Service.sentence'
NER_LBL_SRV_MAIN = 'Service.main'
NER_LBL_SRV_FACILITIES = 'Service.facilities'
NER_LBL_SRV_CLIENT_PARTNER_TYPE = 'Service.type_client/partner'
NER_LBL_SRV_INDUSTRY = 'Service.industry'
NER_LBL_SRV_MISC = 'Service.miscellaneous'

# Most recent version of coarse-grained NER labels

COARSE_NER_LBL_FOCUS = 'Focus'
COARSE_NER_LBL_BRAND = 'Brand'
COARSE_NER_LBL_PARENT_OR_SUBSIDIARY = 'Parent_or_Subsidiary'
COARSE_NER_LBL_RELATED_ORG = 'Related_Org'
COARSE_NER_LBL_NON_FOCUS_PERSON = 'Non_Focus_Person'
COARSE_NER_LBL_DATE = 'Date'
COARSE_NER_LBL_COVERAGE = 'Coverage'
COARSE_NER_LBL_MISC_LOCATION = 'Misc_Location'
COARSE_NER_LBL_QUANTITY = 'Quantity'
COARSE_NER_LBL_PROD_SRV = 'Product_or_Service'
COARSE_NER_LBL_INDUSTRY = 'Industry'
COARSE_NER_LBL_TARGET = 'Target'
COARSE_NER_LBL_MISC_PROD_SRV = 'Misc_Prod_Srv'
COARSE_NER_LBL_NOISE = 'Noise'

# For generality, we include in the mapping the correspondence of the coarse labels to themselves
# Thus, this mapping may be applied to the output of any NER model

MAPPING_ALL_NER_LABELS_TO_COARSE_LABELS = {
    COARSE_NER_LBL_FOCUS: COARSE_NER_LBL_FOCUS,
    NER_LBL_ORG_FOCUS: COARSE_NER_LBL_FOCUS,
    NER_LBL_PER_FOCUS: COARSE_NER_LBL_FOCUS,
    COARSE_NER_LBL_BRAND: COARSE_NER_LBL_BRAND,
    NER_LBL_ORG_BRAND: COARSE_NER_LBL_BRAND,
    COARSE_NER_LBL_PARENT_OR_SUBSIDIARY: COARSE_NER_LBL_PARENT_OR_SUBSIDIARY,
    NER_LBL_ORG_SUBSIDIARY: COARSE_NER_LBL_PARENT_OR_SUBSIDIARY,
    NER_LBL_ORG_PARENT: COARSE_NER_LBL_PARENT_OR_SUBSIDIARY,
    COARSE_NER_LBL_RELATED_ORG: COARSE_NER_LBL_RELATED_ORG,
    NER_LBL_ORG_CLIENT_PARTNER: COARSE_NER_LBL_RELATED_ORG,
    NER_LBL_ORG_COMPETITOR: COARSE_NER_LBL_RELATED_ORG,
    NER_LBL_ORG_MISC: COARSE_NER_LBL_RELATED_ORG,
    COARSE_NER_LBL_NON_FOCUS_PERSON: COARSE_NER_LBL_NON_FOCUS_PERSON,
    NER_LBL_PER_FOUNDER: COARSE_NER_LBL_NON_FOCUS_PERSON,
    NER_LBL_PER_EMPLOYEE: COARSE_NER_LBL_NON_FOCUS_PERSON,
    NER_LBL_PER_CLIENT_PARTNER: COARSE_NER_LBL_NON_FOCUS_PERSON,
    NER_LBL_PER_MISC: COARSE_NER_LBL_NON_FOCUS_PERSON,
    COARSE_NER_LBL_DATE: COARSE_NER_LBL_DATE,
    NER_LBL_DAT_CREATION: COARSE_NER_LBL_DATE,
    NER_LBL_DAT_DEFUNCTION: COARSE_NER_LBL_DATE,
    NER_LBL_DAT_ACQUISITION: COARSE_NER_LBL_DATE,
    NER_LBL_DAT_MISC: COARSE_NER_LBL_DATE,
    COARSE_NER_LBL_COVERAGE: COARSE_NER_LBL_COVERAGE,
    NER_LBL_LOC_HEADQUARTERS: COARSE_NER_LBL_COVERAGE,
    NER_LBL_LOC_COVERAGE: COARSE_NER_LBL_COVERAGE,
    COARSE_NER_LBL_MISC_LOCATION: COARSE_NER_LBL_MISC_LOCATION,
    NER_LBL_LOC_MISC: COARSE_NER_LBL_MISC_LOCATION,
    COARSE_NER_LBL_QUANTITY: COARSE_NER_LBL_QUANTITY,
    NER_LBL_QTY_REVENUE: COARSE_NER_LBL_QUANTITY,
    NER_LBL_QTY_PROFIT: COARSE_NER_LBL_QUANTITY,
    NER_LBL_QTY_DEBT: COARSE_NER_LBL_QUANTITY,
    NER_LBL_QTY_MISC: COARSE_NER_LBL_QUANTITY,
    COARSE_NER_LBL_PROD_SRV: COARSE_NER_LBL_PROD_SRV,
    NER_LBL_SRV_MAIN: COARSE_NER_LBL_PROD_SRV,
    NER_LBL_SRV_FACILITIES: COARSE_NER_LBL_PROD_SRV,
    COARSE_NER_LBL_INDUSTRY: COARSE_NER_LBL_INDUSTRY,
    NER_LBL_SRV_INDUSTRY: COARSE_NER_LBL_INDUSTRY,
    COARSE_NER_LBL_TARGET: COARSE_NER_LBL_TARGET,
    NER_LBL_SRV_CLIENT_PARTNER_TYPE: COARSE_NER_LBL_TARGET,
    COARSE_NER_LBL_MISC_PROD_SRV: COARSE_NER_LBL_MISC_PROD_SRV,
    NER_LBL_SRV_MISC: COARSE_NER_LBL_MISC_PROD_SRV,
    COARSE_NER_LBL_NOISE: COARSE_NER_LBL_NOISE,
    NER_LBL_ORG_NOISE: COARSE_NER_LBL_NOISE,
    NER_LBL_PER_NOISE: COARSE_NER_LBL_NOISE,
    NER_LBL_LOC_NOISE: COARSE_NER_LBL_NOISE,
    NER_LBL_DAT_NOISE: COARSE_NER_LBL_NOISE,
    NER_LBL_QTY_NOISE: COARSE_NER_LBL_NOISE
}

DEFAULT_MAX_SUMMARY_LENGTH = 1000

SENT_USEFULNESS_LBL_RELEVANT = 'Usefulness.relevant'
SENT_USEFULNESS_LBL_IRRELEVANT = 'Usefulness.irrelevant'
SENT_USEFULNESS_LBL_REDUNDANT = 'Usefulness.redundant'
SENT_USEFULNESS_LBL_NOISE = 'Usefulness.noise'

LABELS_SENT_USEFULNESS_CLASSIFIER = {
    0: SENT_USEFULNESS_LBL_IRRELEVANT,
    1: SENT_USEFULNESS_LBL_REDUNDANT,
    2: SENT_USEFULNESS_LBL_NOISE,
    3: SENT_USEFULNESS_LBL_RELEVANT
}

SENT_USEFULNESS_CLASSIFIER_LABEL_MAPPING = {
    SENT_USEFULNESS_LBL_IRRELEVANT: 0,
    SENT_USEFULNESS_LBL_REDUNDANT: 1,
    SENT_USEFULNESS_LBL_NOISE: 2,
    SENT_USEFULNESS_LBL_RELEVANT: 3
}

MULTI_PASSAGE_CLASSIF_DEFAULTS_MODEL_IS_SEQUENTIAL = True
MULTI_PASSAGE_CLASSIF_DEFAULTS_MODEL_IS_CONDITIONAL = True
MULTI_PASSAGE_CLASSIF_DEFAULT_NB_PREV_CLASS_TO_CONSIDER = 1
MULTI_PASSAGE_CLASSIF_DEFAULTS_APPLY_VITERBI = False
MULTI_PASSAGE_CLASSIF_DEFAULT_WINDOW_SIZE = 5
MULTI_PASSAGE_CLASSIF_DEFAULTS_WINDOW_IS_CENTERED = False

ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD', "")