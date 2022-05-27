# -*- coding:utf-8 -*-
# @Time : 2022/5/27 16:02
# @Author: fbz
# @File : demo5.py

import os  # 系统

path = r'./'


# 定义函数
def print_files(path):
    lsdir = os.listdir(path)
    dirs = [i for i in lsdir if os.path.isdir(os.path.join(path, i))]
    files = [i for i in lsdir if os.path.isfile(os.path.join(path, i))]
    if files:
        for f in files:
            print(os.path.join(path, f))
    if dirs:
        for d in dirs:
            print_files(os.path.join(path, d))  # 递归查找
    # return 0


# 执行
print_files(path)
