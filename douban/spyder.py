# -*- coding:utf-8 -*-
# @Time : 2022/3/24 15:51
# @Author: fbz
# @File : spyder.py

from bs4 import BeautifulSoup  # 網頁解析，獲取數據
import re  # 正則表達式，進行文字匹配
import urllib.request, urllib.error  # 制定URL，獲取網頁數據
import xlwt  # 進行excel操作
import sqlite3  # 進行SQLite數據庫操作


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 爬取網頁
    datalist = getData(baseurl)
    savepath = ".\\豆瓣.xls"
    # 保存數據
    saveData(savepath)


# 爬取網頁
def getData(baseurl):
    datalist = []
    for i in range(0,10):
        url = baseurl + str(i*25)
        html = (url)
         # 逐一解析數據

    return datalist


# 得到指定一個URL的網頁内容
def askURL(url):
    head = {  # 模擬瀏覽器頭部信息，向豆瓣服務器發送消息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }  # 用戶代理，表示告訴豆瓣服務器，我們是什麽類型的機器、瀏覽器（本質上是告訴瀏覽器，我們可以接收什麽水平的文件内容）
    request = urllib.request.Request(url=url, headers=head)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as err:
        if hasattr(err, "code"):
            print(err.code)
        if hasattr(err, "reason"):
            print(err.reason)

    return html


# 保存數據
def saveData(savepath):
    print("save")


if __name__ == "__main__":
    # 調用函數
    main()
