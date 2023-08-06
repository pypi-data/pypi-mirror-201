# HTML Parser

extracts/parses information from source HTML.

# construct a Pypi package

* python3 setup.py sdist bdist_wheel
* twine upload dist/*

# create CLI from dist (if you has .dist file)

* python3 -m pip install /home/yaxiong/html_parsing/dist/htmlparsingbs4based-1.1.0.tar.gz

# install package and CLI

* pip install htmlparsingbs4based
* OR python3 -m pip install htmlparsingbs4based

# run from script

* from htmlparsingbs4based.html_parsing.html_parser_custombs4_script import parse_single_page
* parse_single_page(input_url='https://bryansfuel.on.ca/about/',  path_to_crawled_files='/home/yaxiong/data_crawled_websites/crawled_websites_first_batch', min_length=1,  prefix="")

# run CLI (examples)

* mode_1: eleasticsearch
* PARSE -gpf elasticsearch -i 'http://www.mineracamargo.com/MCA_Investors.html' -esusr readwrite -espw ''

* mode_2: local
* PARSE -gpf local -i 'https://bryansfuel.on.ca/about/' -fo /home/yaxiong/data_crawled_websites/crawled_websites_first_batch
* PARSE -gpf local -i 'http://www.mineracamargo.com/MCA_Investors.html' -fo /home/yaxiong/data_crawled_websites/crawled_websites_first_batch
* PARSE -gpf local -i 'https://www.conpak.com/About-Conpak/' -fo /home/yaxiong/data_crawled_websites/crawled_websites_first_batch

* mode_3: html
* PARSE -gpf html -fi /home/yaxiong/html_parsing/html_example/parsed_html.json