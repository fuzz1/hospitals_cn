# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    #省
    province = scrapy.Field()
    #市
    city = scrapy.Field()
    #区
    region = scrapy.Field()
    #名称
    name = scrapy.Field()
    #等级
    level = scrapy.Field()
    #性质
    character = scrapy.Field()
    #电话
    contact = scrapy.Field()
