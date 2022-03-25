# -*- coding:utf-8 -*-
# @Time : 2022/3/24 16:18
# @Author: fbz
# @File : testURLlib.py


import urllib.request,urllib.error

# 獲取一個get請求
# response = urllib.request.urlopen("http://www.baidu.com/")
# print(response.read().decode("utf-8"))  # 對獲取到的網頁源碼進行utf-8解碼

# 獲取一個post請求

# import urllib.parse
# data = bytes(urllib.parse.urlencode({"asd":"123"}),encoding="utf-8")
# response = urllib.request.urlopen("http://httpbin.org/post",data=data)
# print(response.read().decode("utf-8"))


#超時處理
# try:
#     response = urllib.request.urlopen("http://httpbin.org/get",timeout=0.1)
#     print(response.read().decode("utf-8"))
# except urllib.error.URLError as err:
#     print(err)

# response = urllib.request.urlopen("http://www.baidu.com")
# print(response.status)      #狀態碼
# print(response.getheaders())    #得到response.headers
# print(response.getheader('Bdpagetype'))     #得到一個response.getheader

import urllib.parse

# url = "http://httpbin.org/post"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
# }
# data = bytes(urllib.parse.urlencode({'asd':"13"}),encoding="utf-8")
# request = urllib.request.Request(url=url,data=data,headers=headers,method="POST")
# response = urllib.request.urlopen(request)
# print(response.read().decode("utf-8"))


url = "https://www.douban.com"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}
request = urllib.request.Request(url,headers=headers)
response = urllib.request.urlopen(request)
print(response.read().decode("utf-8"))
