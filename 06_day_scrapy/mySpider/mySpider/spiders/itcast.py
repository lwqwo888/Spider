# -*- coding: utf-8 -*-

from mySpider.items import ItcastItem
import scrapy
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class ItcastSpider(scrapy.Spider):
    name = "itcast"
    allowed_domains = ["itcast.cn"]
    start_urls = [ 'http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        with open('teacher.html','w') as f:
            f.write(response.text.decode())

        teacher_all = response.xpath("//div[@class='li_txt']")
        items = []
        for i in teacher_all:
            # 创建字段类对象,进行存储
            ii = ItcastItem()
            # .extract返回的都是unicode对象
            name = i.xpath("h3/text()").extract().strip()
            level = i.xpath("h4/text()").extract().strip()
            info = i.xpath("p/text()").extract().strip()
            ii['name'] = name[0]
            ii['level'] = level[0]
            ii['info'] = info[0]
            items.append(ii)
        return items