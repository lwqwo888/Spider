#!/usr/bin/env python
# coding=utf-8
import requests
import time
import Queue
# import threading
import gevent
from gevent import monkey
monkey.patch_all()
from lxml import etree

class DouBanTop(object):
    def __init__(self):
        # 创建一个队列,用于存储电影标题以及电影评分
        self.data_queue = Queue.Queue()
        self.url = 'https://movie.douban.com/top250?start='
        self.uesr_agent = {'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
        self.proxy = {"http": "616353084:j57da14r@43.226.164.60:16816"}
        self.num = 0
    # //div[@id="content"]//span[@class='title'][1]     电影名
    # //div[@id="content"]//div[@class='star']/span[2]  评分
    # //div[@id="content"]//span[@class='next']/a       尾页特征,取反
    # 创建url    # 发送请求并返回html
    def send_request(self,url):
            print '正在爬取%s'%url
            html = requests.get(url,headers = self.uesr_agent).content
            return html

    def analysis(self,url):
        # 获取每个url的html
        html = self.send_request(url)
        # 解析html
        tophtml = etree.HTML(html)
        mname_list = tophtml.xpath('''//div[@id="content"]//span[@class='title'][1]/text()''')
        score_list = tophtml.xpath('''//div[@id="content"]//div[@class='star']/span[2]/text()''')
        # 打印结果
        movie_list = [i for i in zip(score_list, mname_list)]

        for movie in movie_list:
            sum = movie[0] + movie[1]
            self.data_queue.put(sum)

    def main(self):
        # 构造所有url存到列表
        url_list = [self.url + str(num) for num in range(0,226,25)]
        # 把列表传给发送请求函数
        # thread_list = []
        # for url in url_list:
        #     thread = threading.Thread(target=self.analysis,args=[url])
        #     thread.start()
        #     thread_list.append(thread)
        #
        # for thread in thread_list:
        #     thread.join()

        job_list = [gevent.spawn(self.analysis, url) for url in url_list]
        gevent.joinall(job_list)

        while not self.data_queue.empty():
            print self.data_queue.get()

if __name__ == '__main__':
    dbs = DouBanTop()
    start = time.time()
    dbs.main()
    print time.time()-start

# 网络良良好情况下单线程无队列耗时3.2秒,平均15秒 多线程平均4秒





















# count = 0
# while True:
#     count += 1
#     print '正在抓取第%s页' % count
#     respones = requests.get(self.url + str(self.num), headers=self.uesr_agent, proxies=self.proxy)
#     tophtml = etree.HTML(respones.content)
#     mname_list = tophtml.xpath('''//div[@id="content"]//span[@class='title'][1]/text()''')
#     score_list = tophtml.xpath('''//div[@id="content"]//div[@class='star']/span[2]/text()''')
#     next_page = tophtml.xpath('''//div[@id="content"]//span[@class='next']/a''')
#     movie_list = [i for i in zip(score_list, mname_list)]
#
#     for movie in movie_list:
#         print movie[0], movie[1]
#     print '我是翻页编号%s' % self.num
#     self.num += 25
#     if not next_page:
#         break