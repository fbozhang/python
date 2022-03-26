# -*- coding:utf-8 -*-
# @Time : 2022/3/24 21:13
# @Author: fbz
# @File : testBs4.py

from bs4 import BeautifulSoup

file = open("./baidu.html", "rb")
html = file.read().decode("utf-8")
bs = BeautifulSoup(html, "html.parser")

# 1. Tag   标签及其内容：拿到他所找到的第一个内容

'''
print(bs.title.string)

print(type(bs.title.string))
'''

# 2.  NavigableString  标签里的内容（字符串）

# print(bs.a.attrs)           #获取a标签的所有属性，返回一个字典

# print(type(bs))

# 3.BeautifulSoup   表示整个文档

# print(bs.name)
# print(bs)

# print(bs.a.string)

# 4.Comment   是一个特殊的NavigableString  ，输出不包含注释符号

# -------------------------------------------------------------
# 文檔的遍歷
# print(bs.head.contents)
# print(bs.head.contents[1/])

# 文檔的搜索

# (1)find_all()
# 字符串過濾：會查找與字符串完全匹配的内容
# t_list = bs.find_all("a")


import re

# 正則表達式搜索：使用search（）方法來匹配内容
# t_list = bs.find_all(re.compile("a"))


# 方法：傳入一個函數（方法），根據函數的要求來搜索
# def name_is_exists(tag):
#     return tag.has_attr("name")
# t_list = bs.find_all(name_is_exists)
#
# for i in t_list:
#     print(i)

# 2.kwargs  參數

# t_list = bs.find_all(id="head")

# t_list = bs.find_all(class_=True)
# for i in t_list:
#     print(i)

# 3.text參數

# t_list = bs.find_all(text=["hao123","地图"])
t_list = bs.find_all(text=re.compile("\d"))  # 应用正则表达式来查找包含特定文本的内容（标签里的字符串）

# 4.limit 参数
# t_list = bs.find_all(text=re.compile("\d"),limit=3)
#
# for i in t_list:
#     print(i)

# css选择器

# t_list = bs.select('title')     # 通过标签来查找

# t_list = bs.select('.mnav')     # 通过类名来查找

# t_list = bs.select('#u1')       # 通过id来查找

# t_list = bs.select("a[class='text-color']")   #通过属性来查找

# t_list = bs.select("head > meta")     #通过子标签来查找

# t_list = bs.select(".mnav ~ .bri")

# print(t_list[0].get_text())  # 通过兄弟节点查找，get_text()拿到他的文本。

# for item in t_list:
#        print(item)
