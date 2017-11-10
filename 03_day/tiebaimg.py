#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests
import urllib
import urllib2
from lxml import etree
from bs4 import BeautifulSoup
import time

# 图片写入
def save_img(img_data,filename):
    global now_page
    sum = '%.6f'%time.time()
    sum = sum[-6:]
    now_page = 1
    page = sum + '第'+ str(now_page) + '页' + filename
    print page
    print "[INFO] 正在保存 %s..." % page
    with open('img/'+page, "wb") as f:
        f.write (img_data)

# 循环读取图片url列表

def load_img(imgurl_list):

    for i in imgurl_list:
        img_data = request_url(i)
        save_img(img_data,i[-10:])
# 拼接每个帖子编号
def tiezi(list_id):
    for i in list_id:
        # 拼接帖子链接# https: // tieba.baidu.com / p / 5263400193
        url = 'https://tieba.baidu.com'+i # /p/5263400193  i
        print '此时的url%s'%url

        #解析帖子页面,返回整个页面的字符串
        tiezi_html = request_url(url)
        return tiezi_html,url
# 构造url请求
def request_url(url):
    # 用户名：616353084
    # 密码：j57da14r
    # 颜肖斌:43.226.164.60:16816江苏省南京市有效2017 - 10 - 24

    # proxyauth_handler = urllib2.ProxyHandler({"http": "616353084:j57da14r@43.226.164.60:16816"})
    # opener = urllib2.build_opener(proxyauth_handler)
    user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    request = urllib2.Request(url, headers=user_agent)
    try:
        respons = urllib2.urlopen(request)
        return respons.read()
    except:
        print '请求失败...........'
        pass
        # .text返回Unicode格式数据,.content返回字节流

# 把每个帖子html页面的img解析出来,然后继续解析下一页链接,
# 如果有下一页返回下一页链接然后请求,
# 拿到html内容再次解析img,继续解析下一页链接,如此反复
li = {}
def page_in_page(html,url):
    # if html 中有下一页的特征 就提取出下一页url  <a href="/p/5263400193?pn=4">尾页</a>
    # https: // tieba.baidu.com / p / 5263400193?pn = 2
    # https: // tieba.baidu.com / p / 5263400193       i

    soup = BeautifulSoup(html, 'lxml')
    # 查找下一页特征
    now_page = soup.find('span', attrs={'class': 'tP'}).get_text()
    # 制作下一页的页码
    next_page = int(now_page) + 1
    # 制作下一页的编号
    kw = url + '?pn=%s' % next_page
    # print kw
    # 查找下一页标签是否存在
    next_link = soup.find('a', attrs={'href': kw})
    # 如果存在即为真
    if next_link:
        # 拼接下一页链接
        next_link = url + '?pn=%s' % next_page
        # 把下一页链接追加到列表
        li['key'] = next_link


        # 获取下一页的html字符串
        # next_link_html = request_url(next_link)
        # 匹配出所有符合条件的图片url
        # list_id = img_page(next_link_html,)
        # 读取列表中所有图片并保存
        # tiezi(list_id)

    else:
        print '当前帖子图片提取完毕'
        li['key'] = None
        return
        # print next_link

# 使用Xpath匹配出所有符合条件的图片url
def img_page(html,url):#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # print html
    print type(html)

    # 创建Xpath对象
    tieziurl = etree.HTML(html)

    # 查找页面里所有img链接
    img_id = tieziurl.xpath("//img[@class='BDE_Image']/@src")

    # 调用页中页函数,把从远方传过来的两个参数传走,目的是查看当前帖子页中还有没有下一页
    page_in_page(html, url)  # 如果li里有内容则提取里面的下一页链接

    # if li['key']:
    #     # 获取下一页html内容
    #     html = request_url(li[0])
    #
    #     # 创建Xpath对象
    #     tieziurl = etree.HTML(html)
    #
    #     # 查找页面里所有img链接
    #     img_id = tieziurl.xpath("//img[@class='BDE_Image']/@src")

        # 调用页中页函数,把从远方传过来的两个参数传走,目的是查看当前帖子页中还有没有下一页
        # page_in_page(html, url)
        # print len(list_id)
        # return img_id
    return img_id

# 使用Xpath匹配出所有符合条件的帖子url
def list_page(html):
    tieziurl = etree.HTML(html)
    list_id = tieziurl.xpath("//div[@class='col2_right j_threadlist_li_right ']/div[@class='threadlist_lz clearfix']//a[@class='j_th_tit ']/@href")
    return list_id
    # 返回页面所有帖子编号,列表形式




def main_tieba(baname,start_page,end_page):
    for i in range(start_page,end_page+1):
        page = (i-1)*50
        wd = {'pn':page,'kw':baname}
        wd = urllib.urlencode(wd)
        url='https://tieba.baidu.com/f?'+wd

        # 构建url请求,返回字符串
        tieziurl = request_url(url)

        # print tieziurl

        # 贴吧帖子列表页接收页面数据解析出每个帖子的编号,返回编号列表
        list_id = list_page(tieziurl)


        # 帖子接收编号列表循环取出每个帖子编号并调用拼接然后返回html内容
        tiezi_html,url = tiezi(list_id)

        while True:

            # 返回的是图片链接列表
            img_link_list = img_page(tiezi_html,url)

            # 请求每个图片地址并保存
            load_img(img_link_list)

            if li['key']:
                # 取到下一页html页面
                tiezi_html = request_url(li['key'])
            else:
                break


if __name__ == '__main__':
    baming = raw_input("请输入要爬取的贴吧名:")
    start_page = int(raw_input("请输入要爬取的起始页:"))
    end_page = int(raw_input("请输入要爬取的截至页:"))
    main_tieba(baming,start_page,end_page)