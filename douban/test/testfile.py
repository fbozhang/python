# -*- coding:utf-8 -*-
# @Time : 2022/3/27 1:40
# @Author: fbz
# @File : testfile.py

import os

# if os.path.exists("test.db"):
#     print("qwqe")
# else:
#     print("123")

filename = "../temp/1.txt"
with open(filename, 'w',encoding="utf-8") as file:
    file.write("html")