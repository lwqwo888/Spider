#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Python 的单元测试模块
import unittest
from selenium import webdriver
from bs4 import BeautifulSoup


# 继承父类为unittest.TestCase
class DouyuSpider(unittest.TestCase):
    # 初始化方法（函数名固定写法）
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.num = 0

    # 自定义的测试方法（必须以test开头）
    def testDouyu(self):
        self.driver.get("https://www.douyu.com/directory/all")

        while True:
            html = self.driver.page_source
            soup = BeautifulSoup(html, "lxml")

            all_node = soup.find("div", {"id" : "live-list-content"})

            # 120 个房间名的列表
            room_list = all_node.find_all("h3", {"class" : "ellipsis"})
            # 120 个主播名的列表
            name_list = all_node.find_all("span", {"class" : "dy-name ellipsis fl"})
            # 120 个观众人数的列表
            people_list = all_node.find_all("span", {"class" : "dy-num fr"})

            for room, name, people in zip(room_list, name_list, people_list):
                print u"房间名：" + room.get_text().strip()
                print u"主播名：" + name.get_text().strip()
                print u"观众人数：" + people.get_text().strip()
                print "\n\n"

                self.num += 1


            # 找到了指定的子串，则返回索引值，结果不等于-1，表示到了最后一页，就退出循环
            if html.find("shark-pager-disable-next") != -1:
                print "\n总共主播人数: %d" % self.num
                break

            self.driver.find_element_by_class_name("shark-pager-next").click()

    # 结束方法（函数名固定）
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    #douyu = DouyuSpider()
    unittest.main()
