#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Python2里处理文件编码自动转换的万能钥匙
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# 处理json文件的模块
import json
# 处理csv文件的模块
import csv


# 创建json文件对象
json_file = file("zhihu_json.json", "r")
# json.load()读取json文件里的数据并返回Python数据类型
content_list = json.load(json_file)
print content_list[0]

# 创建csv文件对象
csv_file = file("zhihu_data.csv", "w")
# 创建csv文件读写对象
csv_writer = csv.writer(csv_file)


# keys() 取出字典所有的键 []，做为csv文件的表头
head_list = content_list[0].keys()
print head_list
# values() 取出字典所有的值， 列表推导式, [[], [], [], []],做为csv文件的数据
data_list = [content.values() for content in content_list]

# writerow() 写一行数据,给单层列表
csv_writer.writerow(head_list)

# writerows() 写多行数据,给多层嵌套列表
csv_writer.writerows(data_list)


csv_file.close()
json_file.close()


#data_list = []
#for content in content_list:
#    data_list.append(content)





