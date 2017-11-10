#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import time
from lxml import etree
def main():
    # print time.time()
    s = repr(time.time())
    s=s[:-1]
    print s
    url = "https://search.jd.com/s_new.php?keyword=%E6%B6%82%E6%96%99&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=4&s=81&scrolling=y&log_id="+s
    headers = {"Accept":"*/*",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Connection":"keep-alive",
                "Cookie":"ipLoc-djd=1-72-2799-0; qrsc=3; user-key=63b523f9-d0f7-483d-ab04-03fd7431ad3b; cn=0; unpl=V2_ZzNtbREDFBUnARZSKRkJVWJUEA0SBUsTcw9CXHkbD1A3V0cIclRCFXMURlVnGlsUZwQZWEpcRxJFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2V3odWgduABVaQ2dzEkU4dlN7GV0AbjMTbUNnAUEpDk9SfBleSGQCFltAXkAScgl2VUsa; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_bef1c8a7c1da4f3aac97765933bdaedd|1509008132466; __jda=122270672.2057382660.1508933146.1509026125.1509028041.8; __jdb=122270672.21.2057382660|8.1509028041; __jdc=122270672; xtest=5066.cf6b6759; rkv=V0700; __jdu=2057382660; 3AB9D23F7A4B3C9B=Z4JY6VMQNV4CTIPDKVUP6UPJIX2N7WFL7OXX3QNJMZJ7MG3LYOWA2EK3W342YN6ZSBYELUVHY4NEYD767Z2FEUTJUM",
                "Host":"search.jd.com",
                "Referer":"https://search.jd.com/Search?keyword=%E6%B6%82%E6%96%99&enc=utf-8",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
                "X-Requested-With":"XMLHttpRequest"}
    html = requests.get(url,headers=headers).content
    # print html
    htmlobj = etree.HTML(html)
    dlist = htmlobj.xpath("//*[@id='J_goodsList']/ul/li/div/div/strong/i")
    for i in dlist:
        print i
    print len(dlist)
if __name__ == '__main__':
    main()