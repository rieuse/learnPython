# -*- coding: utf-8 -*-
import scrapy


class DoutuItems(scrapy.Item):
    img_url = scrapy.Field()
    name = scrapy.Field()
