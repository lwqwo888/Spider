# -*- coding: utf-8 -*-
import scrapy
import re
from Tencent.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = "tencent"
    allowed_domains = ["tencent.com"]
    count = 0
    start_urls = (
        'http://hr.tencent.com/position.php?&start=%s'%str(count),
    )

    def parse(self, response):
        all_info = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        for i in all_info:
            item = TencentItem()
            name = i.xpath("./td/a/text()")[0].extract()
            detailLink = i.xpath('./td[1]/a/@href').extract()[0]
            sort = i.xpath("./td[2]/text()")[0].extract()
            people = i.xpath("./td[3]/text()")[0].extract()
            location = i.xpath("./td[4]/text()")[0].extract()
            times = i.xpath("./td[5]/text()")[0].extract()
            item['position_name'] = name.encode('utf-8')
            item['position_sort'] = sort.encode('utf-8')
            item['demand_people'] = people.encode('utf-8')
            item['detail_Link'] = detailLink.encode('utf-8')
            item['work_location'] = location.encode('utf-8')
            item['release_times'] = times.encode('utf-8')

            url_num = re.search(('\d+'),response.url).group(0)

            yield item