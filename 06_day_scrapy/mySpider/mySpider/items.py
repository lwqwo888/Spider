# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 定义结构化数据字段
class ItcastItem(scrapy.Item):
    # 讲师姓名
    name = scrapy.Field()
    # 讲师职称
    level = scrapy.Field()
    # 讲师信息
    info = scrapy.Field()