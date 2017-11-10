#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib
import urllib2
# 我乃lxml 的etree
# 导入lxml的etree，将html字符串转为HTML DOM
from lxml import etree


def send_request(url):
    """
        作用：发送url地址的请求，返回响应
    """
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    request = urllib2.Request(url, headers = headers)
    try:
        response = urllib2.urlopen(request)
        # print "zhe:%s"%response.read()
        return response.read()
    except:
        pass
    #requests.get().content 返回都是字节码

def write_image(image_data, filename):
    """
        作用：将图片数据写入到磁盘文件
        image_data : 每个图片二进制数据
        filename: 需要保存的图片名
    """
    print "[INFO] 正在保存 %s ..." % filename
    with open(filename, "wb") as f:
        f.write(image_data)



def load_image(html):
    """
        作用：提取每个帖子里的所有图片链接
        html: 每个帖子的html源码字符串
    """
    html_obj = etree.HTML(html)

    link_list = html_obj.xpath("//img[@class='BDE_Image']/@src")
    for link in link_list:
        image_data = send_request(link)
        write_image(image_data, link[-10:])


def load_page(html):
    """
        作用：提取帖子列表页的每一条帖子的链接
        html：每个帖子列表页的html源码
    """
    #print "[INFO] 正在爬取 %s ..." % filename
    html_obj = etree.HTML(html)
    #link_list = html_obj.xpath("//a[@class='j_th_tit']/@href")
    #link_list = html_obj.xpath("//div[@class='threadlist_title pull_left j_th_tit']/a/@href")
    link_list = html_obj.xpath("//div[@class='t_con cleafix']//div/a/@href")

    #print link_list

    for link in link_list:
        full_url = "http://tieba.baidu.com" + link
        html = send_request(full_url)
        load_image(html)




def start_work(tieba_name, start_page, end_page):
    """
        作用：贴吧爬虫的调度器，用来处理url地址
        tieba_name: 爬取的贴吧名
        start_page: 爬取的起始页
        end_page: 爬取的结束页
    """
    # 固定的url地址
    base_url = "http://tieba.baidu.com/f?"

    for page in range(start_page, end_page + 1):
        # 根据page值计算pn值
        pn = (page - 1) * 50

        # 查询字符串参数
        dict_kw = {"kw" : tieba_name, "pn" : pn}

        # 将参数进行url编码处理
        str_kw = urllib.urlencode(dict_kw)
        #urllib.parse.urlencode(dict_kw)

        # 拼接为完整的url地址，贴吧帖子列表页
        full_url = base_url + str_kw

        filename = tieba_name + "NO." + str(page) + ".html"
        # 传递url地址发送请求，返回响应
        html = send_request(full_url)
        load_page(html)

    print "\n爬取完成，谢谢使用!"



if __name__ == "__main__":
    tieba_name = raw_input("请输入需要爬取的贴吧名:")
    start_page = int(raw_input("请输入爬取的起始页:"))
    end_page = int(raw_input("请输入爬取的结束页:"))

    start_work(tieba_name, start_page, end_page)

