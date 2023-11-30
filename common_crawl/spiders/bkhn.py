from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import sys
import jsonlines as jsonl
from bs4 import BeautifulSoup
from scrapy.loader import ItemLoader
sys.path.append("./")
from items import CommonCrawlItem
# from colorama import Fore, Back, Style
#from urllib.parse import urlparse

class BKHNConfig:

  def __init__(self):
    self.title_css = ".title"
    self.content_css = "#news-bodyhtml"


class BKHNSpider(CrawlSpider):
    name = "bkhn"
    allowed_domains = ["hust.edu.vn"]
    start_urls = ["https://hust.edu.vn/"]
    rules = [
      Rule(LinkExtractor(allow=r"https://hust\.edu\.vn/.*"), callback='parse_item', follow=True),
      Rule(LinkExtractor(allow=r"https://www\.hust\.edu\.vn/.*"), callback='parse_item', follow=True)
    ]

    def __init__(self, *a, **kw):
      super(BKHNSpider, self).__init__(*a, **kw)
      self.config = BKHNConfig()
      print("Init")

    @property
    def header(self):
       return {
          'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
      }

    def parse_item(self, response):
      soup = BeautifulSoup(response.body, 'html.parser')
      soup.attrs.clear()
      item = ItemLoader(item=CommonCrawlItem())
      # config
      title = soup.select_one(self.config.title_css)
      content = soup.select_one(self.config.content_css)

      item.add_value('id', response.url)
      item.add_value('url', response.url)
      item.add_value('title', title.text)
      item.add_value('content', content.text)
      item.add_value('html', str(content))
      item.add_value('domain', str(self.allowed_domains[0]))
      yield item.load_item()

    def log_info(self, text):
      self.logger.info(text)
      print("Text:",text)
      # print(Back.GREEN,text,Style.RESET_ALL)

    def log_error(self, text):
      self.logger.info(text)
      print("Error:",text)
      # print(Back.RED,text,Style.RESET_ALL)
