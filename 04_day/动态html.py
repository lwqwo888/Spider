#!/usr/bin/env python
#-*- coding:utf-8 -*-# 导入 webdriver

from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
)

# 调用环境变量指定的PhantomJS浏览器创建浏览器对象
driver = webdriver.PhantomJS(desired_capabilities=dcap)
# 如果没有在环境变量指定PhantomJS位置

# get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择 time.sleep(2)
driver.get("https://www.zhihu.com/#signin")
# i = driver.get_cookies()
# print (i)
time.sleep(1)
driver.save_screenshot("login.png")
driver.find_element_by_class_name('signin-switch-password').click()
time.sleep(1)
driver.save_screenshot("login1.png")
driver.find_element_by_name("account").send_keys(17512078876)
driver.find_element_by_name("password").send_keys(950325)
driver.find_element_by_class_name('sign-button').click()
time.sleep(2)
driver.save_screenshot("login2.png")
driver.find_element_by_class_name('Captcha-image').click()
driver.save_screenshot('login3.png')
# driver.send.Event(100,100)
driver.moveByOffset(100,0).click()
driver.save_screenshot('login4.png')





# c1 = {u'domain': u'www.zhihu.com',
#       u'name': u'aliyungf_tc',
#       u'value': u'AQAAAE62338HeQEARkDtty0GGGB3aQMg',
#       u'path': u'/',
#       u'httponly': True,
#       u'secure': False}
# c2 = {u'domain': u'www.zhihu.com',
#       u'name': u'aliyungf_tc',
#       u'value': u'AQAAAKLm7myWtAoA3lnpt+z1soS0AvdJ',
#       u'path': u'/',
#       u'httponly': True,
#       u'secure': False}
# driver.add_cookie(c1)
# driver.add_cookie(c2)


