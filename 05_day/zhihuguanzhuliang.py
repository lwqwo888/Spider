#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
import time
import requests
import json
import jsonpath

def get_Verification_code(data):
    with open('yanzhengma.png','wb') as f:
        f.write(data)
    img = Image.open('yanzhengma.png')
    text = pytesseract.image_to_string(img)
    print text
    i = raw_input("输入Y代表验证码识别正确,输入其他转到手动输入:")
    if i == 'Y':
        return text
    else:
        return raw_input('请您输入验证码:')

def login():
    '''创建登录链接'''
    url = 'https://www.zhihu.com/#signin'
    proxy = {"http": "616353084:j57da14r@43.226.164.60:16816"}
    user_agent = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36", "Cookie" : '''q_c1=8822fd524acf43f3ba26df83683803fc|1507259746000|1507259746000; d_c0="AGDCllH_ewyPTuwF2_k1qQ3e8Ca4ry-arXY=|1507259750"; _zap=8e83447f-28bb-421a-b0de-f3cd5bc38747; r_cap_id="ZDJjOGJjOTk3YjRkNGRhZGE5NjU0NTEzYTk4NDM0ZTE=|1507387602|dc88467e3f3a08ea25df523ac7af2b764c93c96f"; cap_id="MWViN2NjNTJkMTkzNGVkMDk3YzA1Mzg4MDhjMjc3Y2E=|1507387602|acfe0b703556e9a3920789238329023979f335bb"; z_c0=Mi4xaDFvY0JnQUFBQUFBWU1LV1VmOTdEQmNBQUFCaEFsVk42WGNBV2dDYUNBdm1vUUxDS2ViZnlMWjhib25HeE4yZHl3|1507388137|4c36a8661107147981f88aefb716c37bf7767eac; aliyungf_tc=AQAAAMyEaxRMEAAARkDtt+XgbYT5trCK; _xsrf=c077faec-7a23-4d27-a284-c96e798110d8; __utma=51854390.695349185.1507388898.1507422145.1507461319.3; __utmb=51854390.0.10.1507461319; __utmc=51854390; __utmz=51854390.1507422145.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20171004=1^3=entry_date=20171004=1'''}
    # 创建session对象，可以保存Cookie值
    requests1 = requests.session()
    '''发送请求'''
    respones = requests1.get(url,headers=user_agent,proxies = proxy)
    html = respones.content
    print html
    soup = BeautifulSoup(html,'lxml')
    _xsrf = soup.find('input',attrs={'name':'_xsrf'}).get('value')
    # 创建验证码链接
    Verification_code_url = "https://www.zhihu.com/captcha.gif?r=%d&type=login"%(time.time()*1000)
    print Verification_code_url
    # 请求验证码链接
    Verification_code_respones = requests1.get(Verification_code_url,headers = user_agent)
    # 把图片链接传给光学识别函数,注意这里传递的是字节流!!!!
    mycode = get_Verification_code(Verification_code_respones.content)
    # 构造data数据(在浏览器phone_num中的form data里可以得到post轻轻所需的数据键.
    data = {
        "_xsrf" : _xsrf,
        "phone_num":"17512078876",
        "password":"950325",
        "captcha": mycode,
    }
    # 发送post请求,为什么用这个url????因为检查网页可发现post请求接受地址就是这个url
    respones = requests1.post('https://www.zhihu.com/login/phone_num',headers = user_agent,data = data)
    # print respones.content.encode('GBK')
    html = requests1.get('https://www.zhihu.com/people/liu-wen-qiang-77-78',headers = user_agent)
    # print html.content
'''登录后获取话题总数量'''

# 话题名xpath            //div[@class='blk']/a[@target='_blank']/strong
# 话题名所有的链接          //div[@class='blk']/a[@target='_blank']/@href
# 每个话题的关注量          //div[@class='zm-topic-side-followers-info']//strong
# ajax的post请求地址和数据     https://www.zhihu.com/node/TopicsPlazzaListV2
#                   method:next
#      params:{"topic_id":253,"offset":60,"hash_id":"5b32b8619d166187c5d79a0629be6867"}   offset 0 20 40 60
def huati():
    pass
'''获取每个话题关注度'''
'''排序'''
'''爬取知乎所有话题并统计话题数量,以及每个话题的关注数量,从高到低排序'''
if __name__ == '__main__':
    login()