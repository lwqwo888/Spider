# coding=utf-8
import requests
import time
import re
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

start = time.time()

# for url in url_list:
# time.sleep(1)
proxy = {"http": "616353084:j57da14r@43.226.164.60:16816"}
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36", }

huati_html = requests.get(url='https://www.zhihu.com/topic/19550994', headers=headers, proxies=proxy).content
print "[info222----%f]" % (time.time() - start)

zhihu_dict = {}
# xpath匹配出话题名
xpobj = etree.HTML(huati_html)

huati_name = xpobj.xpath("//div[@class='zu-main-content-inner']//div[@class='topic-info']//h1[@class='zm-editable-content']/text()")
# print huati_name
# 正则匹配出话题名和关注量
print "[info----%f]"%(time.time()-start)
zhihu_list = []
pattern = re.compile(r'>\s*<strong>(.*?)</strong>')
huati_sum = pattern.findall(huati_html)
zhihu_dict['话题'] = huati_name[0]
zhihu_dict['关注量'] = huati_sum[0]
zhihu_list.append(zhihu_dict)
print "[info----%f]"%(time.time()-start)