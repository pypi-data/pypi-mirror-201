import os
import re
import sys
from typing import Iterable, Tuple

import json
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from settings import CRAWLER_USER_AGENT, CRAWLER_DEPTH_LIMIT, CRAWLER_PAGE_LIMIT, CRAWLER_RESULTS_DIR

def get_domain(website: str) -> str:
    """Get domain of a website.

    Example:
        >>> get_domain('https://www.example.com/index.html')
        'example.com'

    Args:
        website (str): the URL of a website
    Returns:
        str: the domain name of the website URL
    """
    if '//' in website:
        website = website.split('//')[1]
    if '/' in website:
        website = website.split('/')[0]
    return re.sub(r'^www\.', '', website)


def crawl(website: str) -> None:
    """Crawl website and save HTML pages to local disk.

    Notes: this function can also be used from a Shell environment. You can use `xargs` to enable multiprocess crawling
    (one website per process) (see example below).

    Shell usage example:
        ``cat websites.txt |xargs -P 50 -I WEBSITE python -m description_extraction.crawling.helpers WEBSITE``

    Args:
        website (str): the URL of a website
    """
    domain = get_domain(website)

    class MySpider(CrawlSpider):
        name = domain
        allowed_domains = [domain]
        start_urls = [website]
        
        file_name = website.split('//')[1]
        file_name = file_name.replace('/','{')
        file_name = file_name.replace('?','}')
        # http://doc.scrapy.org/en/latest/topics/settings.html
        custom_settings = {
            'USER_AGENT': CRAWLER_USER_AGENT,
            'FEED_EXPORTERS': {
                'json': 'scrapy.exporters.JsonItemExporter',
            },
            'FEED_FORMAT': 'json',
            'FEED_URI': '/home/yaxiong/crawled_websites2/%s.json' % file_name,
            'FEED_EXPORT_ENCODING': 'utf-8',
            'ROBOTSTXT_OBEY': True,
            'COOKIES_ENABLED': True,
            'DOWNLOAD_DELAY': 0.5,
            'RANDOMIZE_DOWNLOAD_DELAY': True,
            'AUTOTHROTTLE_ENABLED': True,
            'HTTPCACHE_ENABLED': False,
            'DEPTH_LIMIT': CRAWLER_DEPTH_LIMIT,
            'LOG_LEVEL': 'INFO',
            'CONCURRENT_ITEMS': 100,
            'CONCURRENT_REQUESTS': 16,
            'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
            'LOG_SHORT_NAMES': True,
            'COOKIES_ENABLED': True,
            'DEPTH_PRIORITY' : 1,
            'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
            'SCHEDULER_MEMORY_QUEUE' : 'scrapy.squeues.FifoMemoryQueue',
            # http://doc.scrapy.org/en/latest/topics/extensions.html
            'EXTENSIONS': {
                'scrapy.extensions.telnet.TelnetConsole': None,
            },
            'DOWNLOADER_MIDDLEWARES': {
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
            },
            # https://doc.scrapy.org/en/latest/topics/extensions.html#closespider-pagecount
            'CLOSESPIDER_PAGECOUNT': CRAWLER_PAGE_LIMIT,
            'DOWNLOAD_TIMEOUT': 10,
        }

        rules = (
            # Rule(LinkExtractor(allow=('\.*/',)), callback='save_page', follow=True),
            Rule(LinkExtractor(allow=(), deny=('^.{500,}$', r'\?', '.*login.*')), callback='save_page', follow=True),
        )

        def save_page(self, response):
            if response.url == website: # !!only get the entry page
                yield {response.url: response.body.decode('utf-8')}

    process = CrawlerProcess()

    process.crawl(MySpider)
    process.start()
    # process.start(stop_after_crawl=False)


def get_crawling_results(website: str) -> Iterable[Tuple[str, str]]:
    """Read crawling results from local disk.

    Args:
        website (str): website of interest
    Raises:
        FileNotFoundError: when crawled results are not available
    Yields:
        Tuple[str, str]: tuple composed of: URL of page and HTML content of the corresponding page
    """
    domain = get_domain(website)

    file_name = website.split('//')[1]
    file_name = file_name.replace('/','{')
    file_name = file_name.replace('?','}')

    json_file = os.path.join('/home/yaxiong/crawled_websites2', f'{file_name}.json')
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

if __name__ == '__main__':
    #crawl(sys.argv[1])
    crawl("https://vincoconstruction.com/")


# To crawl the websites in parallel, run the following codes in terminal
# cat /home/yaxiong/descriptionextraction/to_be_crawled2.txt |xargs -t -P 50 -I WEBSITE python3 /home/yaxiong/descriptionextraction/description_extraction/crawling/helpers.py WEBSITE