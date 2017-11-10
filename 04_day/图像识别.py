#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



def getcaptcha(data):

    #先把图片存起来
    with open("captcha.png","wb") as f:
        f.write(data)
    #提取图片
    img = Image.open("captcha.png")
    #ocr技术获取图片的文字
    txt = pytesseract.image_to_string(img)
    print txt
    # try:
    #     print eval(txt)
    # except Exception:
    #     print ("表达式为空，请检查")
    # txt=pytesseract.image_to_string(image=img)
    print "请比对本地图片的验证码和输出的验证码：%s"%txt

    sure = raw_input("如果验证码正确输入Y，否则任意键")
    if sure == 'Y':
        return txt
    else:
        return raw_input("输入验证码:")


def getZhihu():

    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
    #知乎登录页 获取 _xsrf
    url = "https://www.zhihu.com/#signin"
    # 创建session对象,可以保存cookie值
    sessionObj = requests.session()
    # 请求登录页面
    response = sessionObj.get(url,headers=header)
    # 获取字节流
    html = response.content
    # 创建bf4对象
    soup = BeautifulSoup(html,"lxml")
    # 查找xsrf
    _xsrf = soup.find("input",attrs={"name":"_xsrf"}).get("value")
    print(_xsrf)
    # https: // www.zhihu.com / captcha.gif?r = 1507298783444 & type = login
    # 创建验证码链接
    viefycodeUrl = "https://www.zhihu.com/captcha.gif?r=%d&type=login"%(time.time()*1000)
    # print(time.time())
    # print(viefycodeUrl)
    # 请求验证码链接
    viefycodeResponse = sessionObj.get(viefycodeUrl,headers=header)
    # 调用光学识别系统识别验证码并返回一个验证码
    mycode = getcaptcha(viefycodeResponse.content)
    print(mycode)
    # 构造data
    param = {
        "_xsrf" : _xsrf,
        "phone_num":"17512078876",
        "password":"950325",
        "captcha": mycode,
    }

    #发起登录请求 提交表单
    sessionObj.post("https://www.zhihu.com/login/phone_num",headers=header,data=param)

    #检查是否登录
    check = sessionObj.get("https://www.zhihu.com/people/cqcq-27",headers=header)


    print(check.content.decode())

if __name__ == '__main__':

    getZhihu()