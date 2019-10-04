# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SgcnItem(scrapy.Item):
    name = scrapy.Field()
    image_Path = scrapy.Field()
    type = scrapy.Field()
