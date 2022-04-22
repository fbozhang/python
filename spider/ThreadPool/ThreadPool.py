# -*- coding:utf-8 -*-
# @Time : 2022/4/21 0:09
# @Author: fbz
# @File : ThreadPool.py
# 1. 提取单个页面的数据
# 2. 用线程池，多个页面同时抓取
import csv

import requests
import csv
from concurrent.futures import ThreadPoolExecutor

f = open("data.csv", mode="w", encoding="utf-8")
csvwriter = csv.writer(f)


def html(current):
    url = "http://www.xinfadi.com.cn/getPriceData.html"
    data = {
        "limit": "20",
        "current": current,
        "pubDateStartTime": "",
        "pubDateEndTime": "",
        "prodPcatid": "",
        "prodCatid": "",
        "prodName": ""
    }
    resp = requests.post(url, data=data)
    dic = resp.json()
    lists = dic['list']
    for list in lists:
        data_list = []
        prodName = list['prodName']
        lowPrice = list['lowPrice']
        avgPrice = list['avgPrice']
        highPrice = list['highPrice']
        place = list['place']
        pubDate = list['pubDate']
        data_list.append(prodName)
        data_list.append(lowPrice)
        data_list.append(avgPrice)
        data_list.append(highPrice)
        data_list.append(place)
        data_list.append(pubDate)
        # 把数据存放在文件中
        # print(data_list)
        csvwriter.writerow(data_list)
    print(url, "提取完毕")


if __name__ == '__main__':
    # for i in range(1, 14900):   # 单线程效率极低
    #     html(i)

    # 创建线程池
    with ThreadPoolExecutor(50) as t:
        for i in range(1, 100):  # 99*20个数据
            # 把下载任务提交给线程池
            t.submit(html, i)
    print("over!!")
