# HTML Parser

extracts/parses information from source HTML.

# construct a Pypi package

* python3 setup.py sdist bdist_wheel
* twine upload dist/*

# install package

* python3 -m pip install htmlparsingbs4based

# create CLI from dist

* python3 -m pip install /home/yaxiong/html_parsing/dist/htmlparsingbs4based-0.0.8.tar.gz

# run CLI

* mode1: eleasticsearch
* PARSE -i 'http://www.mineracamargo.com/MCA_Investors.html' -gpf elasticsearch -esusr readwrite -espw ''

* mode2: local
* PARSE -i 'http://www.mineracamargo.com/MCA_Investors.html' -f /home/yaxiong/crawled_websites2