# -*- coding:utf-8 -*-
# @Time : 2022/3/28 20:11
# @Author: fbz
# @File : request.py

import urllib.request
import requests

# GET
url = f"https://www.douban.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}
# request = requests.get(url, headers=headers)
# print(request)
# # print(request.apparent_encoding)  # 从内容中分析出响应内容的编码方式
# # request.encoding = "utf-8"    # 指定字符集<meta charset="UTF-8">
# print(request.text)

request = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(request)
print(response)
print(response.read().decode("utf-8"))

# POST
# url = "https://fanyi.baidu.com/sug"
# s = input("请输入要翻译的英文单词：")
# data = {
#     "kw": s
# }

# 发送POST请求,发送的数据必须放在字典中，通过data参数进行传参
# request = requests.post(url=url, data=data)
# print (request.apparent_encoding)
# # request.encoding = "ASCII"
# # print(request.text)
# print(request.json())  # 将服务器返回的内容直接处理成json() => dict


# import urllib.parse
#
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
# }
# data = bytes(urllib.parse.urlencode({'kw':s}),encoding="utf-8")
# request = urllib.request.Request(url=url,data=data,headers=headers,method="POST")
# response = urllib.request.urlopen(request)
#
# print(response.read().decode("ascii"))



'''
# url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start=0&genres=喜剧"      # 原网址
url = "https://movie.douban.com/j/new_search_subjects"

# 重新封装
param = {
    "sort": "U",
    "range": "0,10",
    "tags": "",
    "start": "0",
    "genres": "喜剧",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

response = requests.get(url=url, params=param, headers=headers)
print(response.request.url)

print(response.json())
response.close()  # 关掉response
'''


