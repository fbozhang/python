# -*- coding:utf-8 -*-
# @Time : 2022/4/17 22:57
# @Author: fbz
# @File : proxiesTest.py

import requests

# 127.0.0.1:57215  网上找的免费代理ip
proxies = {
    "https": "https://127.0.0.1:57215"
}
resp = requests.get("https://www.baidu.com/", proxies=proxies)  # 使用代理
resp.encoding = resp.apparent_encoding
print(resp.text)
