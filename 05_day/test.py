# coding=utf-8
import requests
import re
import csv
from bs4 import BeautifulSoup
from lxml import etree
import time
from multiprocessing.dummy import Pool
import threading
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# 话题url
class ZhiHu(object):
    def __init__(self):
        self.url = 'https://www.zhihu.com/node/TopicsPlazzaListV2'
        self.huatiurl = 'https://www.zhihu.com'
        self.proxy = {"http": "616353084:j57da14r@43.226.164.60:16816"}
        self.headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",}
        self.count = 0
        self.zhihu_list = []
        self.count1 = 0

    def request(self):
        # 注意params的值为字典,同样要加引号,post请求只能发送字符串
        self.data = {"method": "next",
                     "params": '''{"topic_id":253,"offset":%d,"hash_id":"5b32b8619d166187c5d79a0629be6867"}'''%self.count1}
        huati_list_json = requests.post(self.url,data = self.data, headers = self.headers, proxies=self.proxy).content
        print huati_list_json
        return self.re_huatinum(huati_list_json)

    def re_huatinum(self,huati_list_json):
        # 正则匹配所有话题名
        # pattern = re.compile(r'<strong>(.*?)<\\/strong>')
        # title_list = pattern.findall(huati_list)
        # for i in title_list:
        # print j.decode("unicode-escape")# unicode转码

        # 正则匹配出所有话题编号ee
        pattern1 = re.compile(r'''blank\\" href=\\"(.*?)"''')
        self.url_json = pattern1.findall(huati_list_json)
        # print len(url_json)

        url_numlist = []
        for j in self.url_json:
            pattern = re.compile(r'\\')
            urlnum = pattern.sub(r'',j)
            url_numlist.append(self.huatiurl+urlnum)

        print url_numlist
        return url_numlist # 或者直接调用html_respones

    # 请求url
    def html_respones(self,url):
        #start = 0
        start = time.time()
        print(start)

        # for url in url_list:
        # time.sleep(1)
        huati_html = requests.get(url=url,headers=self.headers,proxies=self.proxy).content
        print "[info222----%f]" % (time.time() - start)
        print(time.time())
        # print huati_html
        self.count += 1
        self.huati_num(huati_html)

    # 根据url拿到关注量   注意一点!!!!!!!!!!!!!!!!知乎登录状态和非登录状态html内容不一样!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def huati_num(self,huati_html):
        start=time.time()

        zhihu_dict = {}
        # xpath匹配出话题名
        xpobj = etree.HTML(huati_html)
        huati_name = xpobj.xpath("//div[@class='zu-main-content-inner']//div[@class='topic-info']//h1[@class='zm-editable-content']/text()")
        # print huati_name
        # 正则匹配出话题名和关注量
        print "[info----%f]"%(time.time()-start)

        pattern = re.compile(r'>\s*<strong>(.*?)</strong>')
        huati_sum = pattern.findall(huati_html)

        zhihu_dict['话题'] = huati_name[0]
        zhihu_dict['关注量'] = huati_sum[0]
        self.zhihu_list.append(zhihu_dict)
        print "[info----%f]"%(time.time()-start)


        print '正在爬取第%d个话题'%self.count

        # 正则匹配出话题名
        # pattern1 = re.compile(r'<h1 class="zm-editable-content" data-disabled="1">(.*?)</h1>')
        # huati_name = pattern1.findall(huati_html)

        # BeautifulSoup不适合本网页,因为有些页面同名标签很多,BeautifulSoup语法不方便提取标签的文本内容
        # soup = BeautifulSoup(huati_html,"lxml")
        # huati_sum = soup.strong.get_text()

        # xpobj = etree.HTML(huati_html)
        # huati_sum = xpobj.xpath("//div[@class='zu-main-sidebar']//div[@class='clearfix']/div//strong/text()")

    def zhihu_csv(self):
        print '正在存储csv文件......'
        print 'zhihu_list',self.zhihu_list
        zhihu_json = json.dumps(self.zhihu_list)
        print 'zhihu_json',zhihu_json
        with open('zhihu_json.json','w') as f:
            f.write(zhihu_json)

        json_file = file('zhihu_json.json','r')
        # 把json文件转换成python类型对象
        pytype_list = json.load(json_file)
        print 'pytype_list',pytype_list
        # 写模式打开csv文件
        csv_file = file('zhihu_data.csv','w')
        # 创建csv写入对象
        csv_writer = csv.writer(csv_file)

        print pytype_list[0]
        # 拿出列表里第一个元素,也就是第一个字典,里面有两个键值对,并拿出所有键作为表头,而且返回的还是一个列表
        head_list = pytype_list[0].keys()
        print head_list
        # 从python类型列表中循环拿出每个字典,再提取出字典里所有的值(每个值都为一个列表)存放到列表里
        data_list = [i.values() for i in pytype_list]
        print 'data_list',data_list
        csv_writer.writerow(head_list)
        # writerows() 写多行数据,给多层嵌套列表
        csv_writer.writerows(data_list)

        csv_file.close()
        json_file.close()
        print '执行成功!'

    def main(self):

        while True:
            url_list = self.request()

            pool = Pool(5)
            pool.map(self.html_respones,url_list)
            pool.close()
            pool.join()

            # thread_list = []
            # for i in range(5):
            #     start= time.time()
            #
            #     url = url_list[i]
            #     thread = threading.Thread(target=self.html_respones,args=[url])
            #     thread.start()
            #     # thread.join()
            #     thread_list.append(thread)
            #     end_time=time.time()
            #     print end_time - start
            #
            # for thread in thread_list:
            #     thread.join()


            print '话题总量为%d'%self.count
            self.zhihu_csv()
            if len(self.url_json) < 20:
                break
            else:
                self.count1 += 20
                # print self.zhihu_list


if __name__ == '__main__':
    zh = ZhiHu()
    zh.main()



