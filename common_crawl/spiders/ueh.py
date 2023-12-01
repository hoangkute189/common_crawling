from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import sys
import jsonlines as jsonl
from bs4 import BeautifulSoup
from scrapy.loader import ItemLoader
sys.path.append("./")
from items import CommonCrawlItem

class UEHConfig:

  def __init__(self):
    self.title_css = [".col-md-8 > h3:nth-child(1)",\
     ".elementor-element-b0c0783 > div:nth-child(1) > h2:nth-child(1)",\
      "h2.elementor-heading-title",\
       ".col-md-12 > p:nth-child(4) > span:nth-child(1) > strong:nth-child(1)"]
    self.content_css = [".col-md-8",\
     "div.elementor-element:nth-child(5)",\
      "div.elementor-widget-theme-post-content",\
      ".col-md-12"]

  def get_config(self, index = 0):
    try:
      title = self.title_css[index]
      content = self.content_css[index]
    except:
      return None, None
    return title, content

class UEHSpider(CrawlSpider):
    name = "ueh"
    allowed_domains = ["ueh.edu.vn"]
    start_urls = ["https://www.ueh.edu.vn/", "https://tuyensinh.ueh.edu.vn/"]
    rules = [
      Rule(LinkExtractor(allow=r"https://.*ueh\.edu\.vn/.*"),\
       callback='parse_item', follow=True),
    ]

    def __init__(self, *a, **kw):
      super(UEHSpider, self).__init__(*a, **kw)
      self.config = UEHConfig()
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
