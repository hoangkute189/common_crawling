from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import sys
import jsonlines as jsonl
from bs4 import BeautifulSoup
from scrapy.loader import ItemLoader
sys.path.append("./")
from items import CommonCrawlItem

class FTUConfig:

  def __init__(self):
    self.title_css = [".article-title"]
    self.content_css = [".article-full"]

  def get_config(self, index = 0):
    try:
      title = self.title_css[index]
      content = self.content_css[index]
    except:
      return None, None
    return title, content

class FTUSpider(CrawlSpider):
    name = "ftu"
    allowed_domains = ["ftu.edu.vn"]
    start_urls = ["https://www.ftu.edu.vn/"]
    rules = [
      Rule(LinkExtractor(allow=r"https://.*ftu\.edu\.vn/.*"),\
       callback='parse_item', follow=True),
    ]

    def __init__(self, *a, **kw):
      super(FTUConfig, self).__init__(*a, **kw)
      self.config = FTUConfig()
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
      title = None
      content = None
      # config
      index = -1
      while(title == None or content == None):
        index += 1
        title_css, content_css = self.config.get_config(index)
        if title_css == None:
          break
        # get soup
        title = soup.select_one(title_css)
        content = soup.select_one(content_css)
      item.add_value('id', response.url)
      item.add_value('url', response.url)
      item.add_value('title', title.text)
      item.add_value('content', content.text)
      item.add_value('html', str(content))
      item.add_value('domain', str(self.allowed_domains[0]))
      yield item.load_item()
