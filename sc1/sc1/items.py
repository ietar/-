# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Sc1Item(scrapy.Item):
    num = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
