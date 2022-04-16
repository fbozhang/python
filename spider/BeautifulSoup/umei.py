# -*- coding:utf-8 -*-
# @Time : 2022/4/15 0:09
# @Author: fbz
# @File : umei.py

import re
import requests
from bs4 import BeautifulSoup
import time
import os
from PIL import Image  # 安装的是Pillow包，发现PIL较多用于2.7版本的Python中，到python3版本已经用Pillow代替PIL了

def removeImg(path):
    file_list = os.listdir(path)
    for file in file_list:
        filename = path + '\\' + file
        # print(filename)
        img = Image.open(filename)
        imgSize = img.size
        img.close()
        # print(imgSize)
        if imgSize[1] > 799 or imgSize[1] < 600:
            os.remove(filename)  # 删除文件
            print("图片{}尺寸为{},已删除".format(file, imgSize))


url = "https://www.umeitu.com/bizhitupian/diannaobizhi/"
resp = requests.get(url)
resp.encoding = "utf-8"

# print(resp.text)
bs = BeautifulSoup(resp.text, "html.parser")
alist = bs.find("ul", class_="pic-list after").find_all("a")
# print(alist)
path = re.compile(r"/bizhitupian/diannaobizhi/(?P<num>.*)", re.S)
child_page_list = []
for a in alist:
    href = a.get("href")  # 直接通过get就可以拿到属性的值
    # print(href)
    href = path.findall(href)
    # print(href)
    # 拿到子页面的源代码
    for child_page in href:
        child_page_list.append(url + child_page)
# print(child_page_list)

for href in child_page_list:
    child_resp = requests.get(href)
    child_resp.encoding = "utf-8"
    # 从子页面中拿到图片的下载路径
    child_page = BeautifulSoup(child_resp.text, "html.parser")
    p = child_page.find("section", class_="img-content")
    img = p.find("img")
    src = img.get("src")
    # print(src)
    # 下载图片
    img_resp = requests.get(src)
    # img_resp.content    # 这里拿到的是字节
    img_name = src.split("/")[-1]  # 拿到url中的最后一个/以后的内容
    with open("img/" + img_name, mode="wb") as f:
        f.write(img_resp.content)  # 图片内容写入文件

    print("over!", img_name)
    time.sleep(1)

print("allover!!")
path = "../img"
removeImg(path)

# def asd(url):
#     resp = requests.get(url)
#     resp.encoding = resp.apparent_encoding
#
#     # print(resp.text)
#     bs = BeautifulSoup(resp.text, "html.parser")
#     alist = bs.find("ul", class_="clearfix").find_all("a")
#     # print(alist)
#     child_page_list = []
#     for a in alist:
#         href = a.get("href")  # 直接通过get就可以拿到属性的值
#         # print(href)
#         page = "https://pic.netbian.com"
#         # 拿到子页面的源代码
#         child_page = page + href
#         child_resp = requests.get(child_page)
#         child_resp.encoding = child_resp.apparent_encoding
#         # 从子页面中拿到图片的下载路径
#         child_page = BeautifulSoup(child_resp.text, "html.parser")
#         p = child_page.find("div", class_="photo-pic")
#         img = p.find("img")
#         src = img.get("src")
#         # print(src)
#         # 下载图片
#         img_resp = requests.get(page + src)
#         # img_resp.content    # 这里拿到的是字节
#         img_name = src.split("/")[-1]  # 拿到url中的最后一个/以后的内容
#         with open("img/" + img_name, mode="wb") as f:
#             f.write(img_resp.content)  # 图片内容写入文件
#
#         print("over!", img_name)
#         time.sleep(1)
#
#     print("allover!!")
#
# for i in range(10, 15):
#     url = "https://pic.netbian.com/4kmeinv/index_" + str(i) + ".html"
#     asd(url)
#     time.sleep(3)
# path = "img"
# removeImg(path)
