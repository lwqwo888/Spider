#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import Queue
import time
from lxml import etree

class DoubanSpider(object):
    def __init__(self):
        self.data_queue = Queue.Queue()
        self.base_url = "http://movie.douban.com/top250?start="
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.num = 0

    def load_page(self, url):
        print "[INFO]: 正在抓取 %s " % url
        html = requests.get(url, headers = self.headers).content
        time.sleep(1)
        return html

    def parse_page(self, url):
        html = self.load_page(url)
        html_obj = etree.HTML(html)

        # 当前页面的所有电影结点的列表
        node_list = html_obj.xpath("//div[@class='info']")

        # 迭代每个结点，进行取值
        for node in node_list:
            # 电影标题
            title = node.xpath(".//span[@class='title']/text()")[0]
            # 电影评分
            score = node.xpath(".//span[@class='rating_num']/text()")[0]

            self.data_queue.put(score + "\t" + title)
            self.num += 1


    def main(self):
        url_list = [self.base_url + str(num) for num in range(0, 225 + 1, 25)]
        for url in url_list:
            self.parse_page(url)

        while not self.data_queue.empty():
            print self.data_queue.get()

        print self.num

if __name__ == "__main__":
    douban = DoubanSpider()
    start = time.time()
    douban.main()
    print "[INFO]: Useing time %f seconds." % (time.time() - start)
    # 3.92

