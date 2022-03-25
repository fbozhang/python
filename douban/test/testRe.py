# -*- coding:utf-8 -*-
# @Time : 2022/3/25 21:09
# @Author: fbz
# @File : testRe.py

# 正则表达式：字符串模式（判断字符串是否符合一定标准）
import re

# 创建模式对象

pat = re.compile("AA")  # 此处AA是正则表达式用来去验证其他字符串
# m = pat.search("CBA")  #search字符串被校验的内容

# m = pat.search("ABCAA")
# m = pat.search("ABCAADDCCAAA")      #search方法进行比对查找

# 没有模式对象
# m = re.search("asd", "Aasd")    #前面的字符串是规则（模板） ，后面的字符串是校验对象

# print(m)


# print(re.findall("a","ASDaDFGAa"))    #前面字符串是规则（正则表达式），后面的字符串是校验的字符串

# print(re.findall("\\b[A-Z][a-z]*\\b","It Is Am a Boy AAAAAAa"))

# print(re.findall("[A-Z]+","ASDaDFGAa"))

# sub

# print(re.sub("a","A","asdabc"))   #找到a用A来替换，在第三个字符串中查找


# 建议在正则表达式中被比较的字符串前面加上r， 不用担心转义字符的问题
# a = r"\aabd-\'"
# print(a)
