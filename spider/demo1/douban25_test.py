# -*- coding:utf-8 -*-
# @Time : 2022/4/13 19:35
# @Author: fbz
# @File : douban25_test.py


import requests
import re
import csv

url = "https://movie.douban.com/top250"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
}

response = requests.get(url=url, headers=headers)
html = response.text
# print(html)

obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)'
                 r'</span>.*?<p class="">.*?<br>(?P<year>.*?)&nbsp.*?'
                 r'<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
                 r'<span>(?P<num>.*?)人评价</span>', re.S)

result = obj.finditer(html)
f = open("data.csv",mode="w",encoding="utf-8")
writer = csv.writer(f)

for i in result:
    # print(i.group("name"))
    # print(i.group("score"))
    # print(i.group("num"))
    # print(i.group("year").strip())  # .strip()去掉空白
    dict = i.groupdict()
    dict["year"] = dict["year"].strip()
    writer.writerow(dict.values())

f.close()
print("over!")
