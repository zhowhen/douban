# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # 标题
    title = scrapy.Field()
    # 导演 主演
    bd = scrapy.Field()
    # 评分
    star = scrapy.Field()
    # 描述
    quote = scrapy.Field()

