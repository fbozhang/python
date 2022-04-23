# -*- coding:utf-8 -*-
# @Time : 2022/4/13 20:11
# @Author: fbz
# @File : ddtt_.py

import requests
import re

url = "https://www.dytt89.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
}
# resp = requests.get(url, verify=False)  # verify=False去掉安全验证verify_ssl=False防止ssl验证
# 发现不关安全验证传入header也可以
resp = requests.get(url, headers)
resp.encoding = "gb2312"  # 指定字符集
# print(resp.text)

# 拿到ul里的li
obj1 = re.compile(r"2022必看热片.*?<ul>(?P<ul>.*?)</ul>", re.S)
obj2 = re.compile(r"<a href='(?P<href>.*?)'", re.S)
obj3 = re.compile(r'◎片　　名　(?P<movieName>.*?)<br />.*?'
                  r'<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<download>.*?)">', re.S)

result1 = obj1.finditer(resp.text)
child_href_list = []
for i in result1:
    ul = i.group("ul")
    # print(ul)

    # 提取子页面链接
    result2 = obj2.finditer(ul)
    for j in result2:
        href = j.group("href")
        # print(href)
        child_href = url + href.strip("/")  # .strip("/")去掉/
        child_href_list.append(child_href)

# 提取子页面内容
for href in child_href_list:
    # child_resp = requests.get(url, verify=False)
    child_resp = requests.get(href, headers)
    child_resp.encoding = "gb2312"
    result3 = obj3.search(child_resp.text)
    print(result3.group("movieName"))
    print(result3.group("download"))
    # break
    # result3 = obj3.finditer(child_resp.text)
    # for i in result3:
    #     print(i.group("movieName"))
    #     print(i.group("download"))
    #     break
