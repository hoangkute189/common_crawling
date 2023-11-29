import scrapy
from ..items import CommonCrawlItem
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from bs4 import BeautifulSoup

import re
import hashlib
import requests
import sqlite3
import os

class ConnectDatabase:
    def __init__(self):
        self.ids_seen = set()
        self.con = sqlite3.connect(
            'common_crawl.db')
        self.cur = self.con.cursor()

    def get_ids(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS common_crawl
        (
            id TEXT PRIMARY KEY,
            url TEXT,
            title TEXT,
            content TEXT,
            html TEXT,
            domain TEXT
        );
        """)
        self.con.commit()
        ids = self.cur.execute("""SELECT id FROM common_crawl""").fetchall()
        self.ids_seen = set(i[0] for i in ids)
        return self.ids_seen


class TdtuSpider(CrawlSpider):
    name = "edu"
    rules = [
        Rule(
            LinkExtractor(allow=[r"/.*"]),
            callback="parse",
            follow=True,
        )
    ]
    
    custom_settings = {
        'DEPTH_LIMIT': 10
    }

    def __init__(self, *args, **kwargs):
        super(TdtuSpider, self).__init__(*args, **kwargs)
        self.start_urls = [self.surl]
        self.allowed_domains = [self.domain]
        self.ids_seen = ConnectDatabase().get_ids()

    @property
    def header(self):
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }
        
    def download_pdf(self, links):
        for link in links:
            path = re.sub(r'^(\.\/|\/)', 'https://' + self.allowed_domains[0] + '/', link)
            response = requests.get(path, verify=False)
            if response.status_code == 200:
                self.save_pdf(path, response)
                
    def create_folder_domain(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            self.logger.info('Folder creates.')
            
    def save_pdf(self, path, response):
        path = path.split('/')[-1]
        folder_path = 'pdf_file/' + self.allowed_domains[0]
        path_destination = 'pdf_file/' + self.allowed_domains[0] + '/' + path
        
        if os.path.exists(path_destination):
            self.logger.info('File exists.')
        else:
            self.create_folder_domain(folder_path)
            self.logger.info('Saving PDF %s', path_destination)
            with open(path_destination, 'wb') as f:
                f.write(response.content)
    
    # def is_binary_content_pdf(self, content):
    #     pdf_signature = b'%PDF'
    #     return content.startswith(pdf_signature)

    def parse(self, response):
        id = hashlib.sha256(response.url.encode('utf-8')).hexdigest()

        if id in self.ids_seen:
            return
        
        # # Use a CSS selector to extract href attributes from <a> tags
        # hrefs = response.css('a::attr(href)').extract()
        # pdf_links = [i for i in hrefs if i.endswith('.pdf')]
        # if pdf_links:
        #     self.download_pdf(pdf_links)

        soup = BeautifulSoup(response.body, 'html.parser')
        soup.attrs.clear()

        item = ItemLoader(item=CommonCrawlItem())
        item.add_value('id', response.url)
        item.add_value('url', response.url)
        item.add_value('title', soup.title)
        item.add_value('content', str(soup.body))
        item.add_value('html', str(soup.body))
        item.add_value('domain', str(self.allowed_domains[0]))

        yield item.load_item()
