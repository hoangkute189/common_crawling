from scrapy.exceptions import DropItem

import re
import sqlite3


class CommonCrawlPipeline:
    def process_item(self, item, spider):
        try:
            input_text = re.sub(r'\n{1,}|\s+', ' ', item['content'])
            num_word = len(input_text.split(' '))

            if num_word < 150:
                raise DropItem("This is a home page. Item excluded. ")
            
            return item
        except:
            raise DropItem("This is a home page. Item excluded. ")


class SaveToDatabasePipeline:
    def __init__(self):
        self.con = sqlite3.connect('common_crawl.db')
        self.cur = self.con.cursor()

    def open_spider(self, spider):
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

    def process_item(self, item, spider):
        self.con.execute("""
        INSERT INTO common_crawl (id, url, title, content, html, domain) VALUES (?, ?, ?, ?, ?, ?)
        """, (item["id"], item["url"], item["title"], item["content"], item['html'], item['domain']))
        self.con.commit()

    def clode_spider(self, spider):
        self.con.close()


class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()
        self.con = sqlite3.connect('common_crawl.db')
        self.cur = self.con.cursor()

    def open_spider(self, spider):
        ids = self.cur.execute("""SELECT id FROM common_crawl""").fetchall()
        self.ids_seen = set(i[0] for i in ids)

    def process_item(self, item, spider):
        if item["id"] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(item["id"])
            return item
