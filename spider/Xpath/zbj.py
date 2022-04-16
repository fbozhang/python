# -*- coding:utf-8 -*-
# @Time : 2022/4/16 18:52
# @Author: fbz
# @File : zbj.py

import requests
from lxml import etree

url = "https://shenzhen.zbj.com/search/f/?kw=saas"
response = requests.get(url)
# print(response.text)

html = etree.HTML(response.text)
# 拿到每一个服务商的div
divs = html.xpath("/html/body/div[6]/div/div/div[2]/div[5]/div[1]/div")
for div in divs:
    price = div.xpath("./div/div/a[2]/div[2]/div[1]/span[1]/text()")[0].strip("¥")
    title = "saas".join(div.xpath("./div/div/a[2]/div[2]/div[2]/p/text()"))
    com_name = div.xpath("./div/div/a[1]/div[1]/p/text()")[1].strip("\n")
    location = div.xpath("./div/div/a[1]/div[1]/div/span/text()")[0]
    print(price,title)

