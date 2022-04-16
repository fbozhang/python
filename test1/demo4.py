# -*- coding:utf-8 -*-
# @Time : 2022/4/3 16:30
# @Author: fbz
# @File : demo4.py

import os
from PIL import Image

path = r'E:\桌面\img'
file_list = os.listdir(path)

for file in file_list:
    filename = path + '\\' + file
    # print(filename)
    img = Image.open(filename)
    imgSize = img.size
    img.close()
    # print(imgSize)
    if imgSize[1] > 1 or imgSize[1] < 600:
        print("图片{}尺寸为{},已删除".format(file, imgSize))
        os.remove(filename)  # 删除文件

# filename = r'E:\photo\微信图片_20190408114202.jpg'
# img = Image.open(filename)
# imgSize = img.size  # 图片的长和宽
# print("图片尺寸是：{},宽：{}，长：{}".format(imgSize, imgSize[0], imgSize[1]))
# w = img.width
# h = img.height
# f = img.format
# print(w, h, f)
