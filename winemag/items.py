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
    meta_url = scrapy.Field()
    meta_page = scrapy.Field(
        output_processor=TakeFirst(),
    )
    meta_item = scrapy.Field(
        output_processor=TakeFirst(),
    )

    title = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field()

    price = scrapy.Field(
        input_processor=price_processor,
        output_processor=TakeFirst(),
    )
    designation = scrapy.Field()
    varietal = scrapy.Field()
    country = scrapy.Field()
    region = scrapy.Field()
    subregion = scrapy.Field()
    subsubregion = scrapy.Field()
    winery = scrapy.Field()
    vintage = scrapy.Field(
        input_processor=vintage_processor,
        output_processor=TakeFirst(),
    )

    alcohol = scrapy.Field(
        input_processor=alcohol_processor,
        output_processor=TakeFirst(),
    )
    category = scrapy.Field()
