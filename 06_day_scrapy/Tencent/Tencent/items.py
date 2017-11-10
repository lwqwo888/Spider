# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # 职位名称
    position_name = scrapy.Field()
    # 职位类别
    position_sort = scrapy.Field()
    # 招聘人数
    demand_people = scrapy.Field()
    # 工作地点
    work_location = scrapy.Field()
    # 发布时间
    release_times = scrapy.Field()
