# -*- coding:utf-8 -*-
# @Time : 2022/4/23 1:29
# @Author: fbz
# @File : 91kanju.py

import requests
import re

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

obj = re.compile(r"url: '(?P<url>.*?)',", re.S)     # 用来提取m3u8的url地址

url = "https://91kanju.com/vod-play/54812-1-1.html"

resp = requests.get(url, headers=headers)
m3u8_url = obj.search(resp.text).group("url")   # 拿到m3u8的地址
print(m3u8_url)
resp.close()

# 下载m3u8文件
resp2 = requests.get(m3u8_url, headers=headers)

with open("temp.m3u8", mode="wb") as f:
    f.write(resp2.content)
resp2.close()
print("over")

