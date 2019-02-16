# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags


REGEX_VINTAGE = re.compile('\s([0-9]{4})\s')


def price_processor(text):
    if text[0] == '$':
        yield text[1:].split(',')[0]


def varietal_processor(text):
    yield text.split(',')[0]


def vintage_processor(text):
    search = REGEX_VINTAGE.search(text)
    if search:
        yield search.group().strip()


def alcohol_processor(text):
    if text[-1] == '%':
        yield text[:-1]


class PageItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())

    title = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip),
                         output_processor=Join())
    vintage = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip, vintage_processor),
                           output_processor=Join())
    rating = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip),
                          output_processor=TakeFirst())
    description = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip),
                               output_processor=Join())

    price = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip, price_processor),
                         output_processor=TakeFirst())
    designation = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip),
                               output_processor=Join())
    varietal = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip, varietal_processor),
                            output_processor=Join())
    subsubregion = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip),
                             output_processor=Join())
    subregion = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip),
                             output_processor=Join())
    region = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip),
                          output_processor=Join())
    country = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip),
                           output_processor=Join())
    winery = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip),
                          output_processor=TakeFirst())

    alcohol = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip, alcohol_processor),
                           output_processor=Join())
    category = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip),
                            output_processor=Join())
