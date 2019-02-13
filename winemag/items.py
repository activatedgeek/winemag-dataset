# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.loader.processors import TakeFirst


def price_processor(value):
    """
    Some prices may be unavailable.
    """
    for price in value:
        price = price.split(',')[0]
        price = price[1:] if price[0] == '$' else 'nan'
        yield float(price)


def alcohol_processor(value):
    for alcohol in value:
        alcohol = alcohol[:-1] if alcohol[-1] == '%' else 'nan'
        yield float(alcohol)


def vintage_processor(value):
    vintage_regex = re.compile('\s([0-9]{4})\s')
    for title in value:
        search = vintage_regex.search(title)
        if search:
            yield int(search.group().strip())


class ReviewItem(scrapy.Item):
    meta_url = scrapy.Field(output_processor=TakeFirst())

    title = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())

    price = scrapy.Field(input_processor=price_processor, output_processor=TakeFirst())
    designation = scrapy.Field(output_processor=TakeFirst())
    varietal = scrapy.Field(output_processor=TakeFirst())
    country = scrapy.Field(output_processor=TakeFirst())
    region = scrapy.Field(output_processor=TakeFirst())
    subregion = scrapy.Field(output_processor=TakeFirst())
    subsubregion = scrapy.Field(output_processor=TakeFirst())
    winery = scrapy.Field(output_processor=TakeFirst())
    vintage = scrapy.Field(input_processor=vintage_processor, output_processor=TakeFirst())

    alcohol = scrapy.Field(input_processor=alcohol_processor, output_processor=TakeFirst())
    category = scrapy.Field(output_processor=TakeFirst())
