#!/usr/bin/env python
#-*- coding:utf-8 -*-
import urllib2
import urllib



def tieba():
    baming = raw_input('请输入要进入的贴吧名：')
    page = raw_input('请输入要查看的页数：')
    print  type(page)
    print 1111111111111111111111111
    page2 = int(page)
    print type(page)
    # 由于贴吧一页显示５０条，所以这里需要把页数转换为条数才能在ｕｒｌ里通过条数翻页
    page3 = (page2-1)*50
    # https: // tieba.baidu.com / f?kw = % E5 % 88 % 98 % E6 % 96 % 87 % E5 % BC % BA & fr = index & fp = 0 & ie = utf - 8
    url = 'https://tieba.baidu.com/f?'
    # 需要拼接的字符,要存为字典类型才能转码
    kw = {"kw":baming}
    # pn = 200
    # 把字符转码
    kw2 = urllib.urlencode(kw)
    # 拼接ｕｒｌ
    newurl = url + kw2 +'&pn='+ str(page3)
    print newurl
    # 构造请求
    req = urllib2.Request(newurl)
    # 发送请求
    res = urllib2.urlopen(req)
    print res.read()

def csgo():
    baming = raw_input("请输入吧名：")
    page = int(raw_input('请输入页数：'))
    print baming
    # 根据不同网站不同的字符键，修改字典中的键
    baming1 = urllib.urlencode({"kw":baming})
    print '吧名：%s'%baming1
    page1 = (page-1)*50
    url = 'https://tieba.baidu.com/f?'
    url1 = url + baming1 + '&pn=' + str(page1)
    print '网址：%s'%url1
    user_agent = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"}
    requset = urllib2.Request(url1,headers=user_agent)
    respons = urllib2.urlopen(requset)
    print respons.read()


# 爬取内容
def requsets(url,dname,headers):
    print dname
    print '正在爬取%s'%dname
    requset = urllib2.Request(url,headers=headers)
    return urllib2.urlopen(requset).read()
# 写入内容
def wdisk(html,dname):
    print '正在写入%s'%dname
    # 已写方式打开dname文件并重命名为ｆ
    with open(dname,'wb') as f:
        f.write(html)

# 处理url
def tieba_spider(baming,startpage,endpage,url):
    for i in range(startpage,endpage+1):
        page = (i-1)*50
        dict = {'kw':baming,'pn':page}
        dict1 = urllib.urlencode(dict)
        newurl = url + dict1
        print newurl
        user_agent = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"}
        dname = (baming + '吧第%s页' + '.html')%i
        html = requsets(newurl,dname,user_agent)
        wdisk(html,dname)
        # newurl1 = urllib2.Request(newurl,headers=user_agent)
        # res = urllib2.urlopen(newurl1)
        # print res.read()
    print '操作完成！'

if __name__ == '__main__':
    # tieba()
    # csgo()
    baming = raw_input("请输入吧名：")
    startpage = int(raw_input('请输入要爬取的起始页：'))
    endpage = int(raw_input('请输入要爬取的结束页：'))
    url = 'http://tieba.baidu.com/f?'
    tieba_spider(baming,startpage,endpage,url)