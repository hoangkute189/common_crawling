import re
import hashlib

import scrapy
from itemloaders.processors import TakeFirst, MapCompose

from w3lib.html import remove_tags, remove_tags_with_content, remove_comments


def remove_unnessary_tags(doc):
    clean_docs = remove_tags_with_content(
        doc, which_ones=('footer', 'header', 'h1', 'h3', 'a', 'script', 'style', 'form')
    )
    return clean_docs


def keep_table_tags(doc):
    text_content = remove_tags(
        doc, keep=('table', 'tr', 'td', 'th')
    )
    return text_content


def clean_text(text):
    return re.sub(r'\n{3,}', '\n\n', text)


def format_text(input_text):
    text = ' '.join([i.strip() for i in input_text.split('\n')])
    return '\n\n'.join(text.strip().split('  '))


def try_string(value):
    try:
        return str(value)
    except ValueError:
        return value


def make_id(url):
    return hashlib.sha256(url.encode('utf-8')).hexdigest()


def delete_white_space(text):
    return re.sub(r'[^\S\r\n]+', ' ', text)


class CommonCrawlItem(scrapy.Item):
    id = scrapy.Field(
        input_processor=MapCompose(
            make_id,
            try_string
        ),
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        input_processor=MapCompose(
            try_string
        ),
        output_processor=TakeFirst()
    )
    title = scrapy.Field(
        input_processor=MapCompose(
            try_string
        ),
        output_processor=TakeFirst()
    )
    content = scrapy.Field(
        input_processor=MapCompose(
            remove_unnessary_tags,
            remove_comments,
            keep_table_tags,
            clean_text,
            delete_white_space,
            format_text,
            try_string
        ),
        output_processor=TakeFirst()
    )
    html = scrapy.Field(
        input_processor=MapCompose(
            try_string
        ),
        output_processor=TakeFirst()
    )
    domain = scrapy.Field(
        input_processor=MapCompose(
            try_string
        ),
        output_processor=TakeFirst()
    )
    metadata = scrapy.Field()
