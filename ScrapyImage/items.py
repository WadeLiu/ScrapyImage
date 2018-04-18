# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyimageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ItemPerson(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    folder = scrapy.Field()

class ItemImage(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    download = scrapy.Field()
    filepath = scrapy.Field()
