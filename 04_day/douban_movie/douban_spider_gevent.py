#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import Queue
import time

# 导入多线程的线程池
# multiprocessing.dummy 是多进程提供的多线程库
#from multiprocessing.dummy import Pool

#import threading
from lxml import etree

# Python的协程库
import gevent
from gevent import monkey
# 猴子补丁
monkey.patch_all()
# gevent 让我们可以用同步的逻辑，来写异步的程序。
# monkey.patch_all() 在Python程序执行的时候，会动态的将底层的网络库（socket，select）打个补丁，变成异步的库。
# 让程序在执行网络操作的时候，按异步的方式去执行。


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


        # 单线程
        #for url in url_list:
        #    self.parse_page(url)

        # 多线程1
        """
        thread_list = []
        for url in url_list:
            # 创建一个线程，并指定执行的任务
            thread = threading.Thread(target = self.parse_page, args = [url])
            # 启动线程
            thread.start()
            thread_list.append(thread)
            # thread.join()

        # 让主线程阻塞，等待所有的子线程结束，再继续执行。
        for thread in thread_list:
            thread.join()
        """

        # 多线程2
        """
        # 创建10个线程的线程池
        pool = Pool(len(url_list))
        # map()高阶函数，用来批量处理函数传参
        pool.map(self.parse_page, url_list)
        # 关闭线程池
        pool.close()
        # 阻塞主线程，等待子线程结束
        pool.join()
        """

        # 协程
        """
        job_list = []
        for url in url_list:
            # 创建协程任务并执行
            job = gevent.spawn(self.parse_page, url)
            job_list.append(job)

        # 等待所有协程任务完成
        gevent.joinall(job_list)
        """


        job_list = [gevent.spawn(self.parse_page, url) for url in url_list]
        gevent.joinall(job_list)

        # Pythonic
        # gevent.joinall([gevent.spawn(self.parse_page, url) for url in url_list])



        while not self.data_queue.empty():
            print self.data_queue.get()

        print self.num

if __name__ == "__main__":
    douban = DoubanSpider()
    start = time.time()
    douban.main()
    print "[INFO]: Useing time %f seconds." % (time.time() - start)
    # 3.92

