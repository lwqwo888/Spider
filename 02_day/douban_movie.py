#!/usr/bin/env python
#-*- coding:utf-8 -*-
import urllib2
import urllib
from lxml import etree
import re
def douban(num):

	if num == '1':
		tmp = '5'

	elif num == '2':
		tmp = '13'

	dict_value = {
        "type" : tmp,
        "interval_id" : "100:90",
        "action" : "",
        "start" : "0", # 起始排名，默认从第一名开始显示，０代表第一个
        "limit" : "20", # 截止位置,显示到第几名
    }

	str_value = urllib.urlencode(dict_value)
        print str_value
	url = 'https://movie.douban.com/j/chart/top_list?' + str_value
        print url
	headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
	requset = urllib2.Request(url,headers = headers)
	respons = urllib2.urlopen(requset)
	with open ('douban.json','w') as f:
		f.write(respons.read())


def doubanNum(num,tmpnum):
    if num == '1':
        tmp = '5'

    elif num == '2':
        tmp = '13'

    elif num == '3':
        tmp = '11'

    # 构建url
    dict = {
        # "type_name" : "动作",
        "type" : tmp,
        "interval_id" : "100:90",
        "action" : "",
        "start" : "0",
        "limit" : tmpnum,
    }
    str_value = urllib.urlencode(dict)
    url = 'https://movie.douban.com/j/chart/top_list?'+ str_value
    print url
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    request = urllib2.Request(url,headers=headers)
    respons = urllib2.urlopen(request).read()
    # print respons
    # with open('douban1.json', 'w') as f:
    #     f.write(respons)
    # print type(respons)
    # pattern = re.compile(r'''title.*?,''')
    pattern = re.compile(r'"title":"(.*?)"',re.S)
    m = pattern.findall(respons)
    # print type(m)
    # print m

    for i in m:

        # pattern1 = re.compile(r"(.*?):(.*?),")

        # m1 = pattern1.sub("\2",i)
        # print type(i)
        # for x in i:
        #     print x
        # str = '78940'
        # print str[0:3]
        # print i[8:29]
        b = i.replace('''title":"''','')
        c = b.replace('''",''','')
        with open('douban2.json', 'a') as f:
            f.write(c+"\n")

if __name__ == '__main__':
    num = raw_input('请输入要查看的电影分类——1为动作，2为爱情,3为剧情：')
    tmpnum = raw_input('请输入要查看的电影排名量：')
	# douban(type1)
    doubanNum(num,tmpnum)