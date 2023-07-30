# -*- coding:utf-8 -*-
# @Time : 2023/7/30 19:47
# @Author: fbz
# @File : main.py
from scrapy.cmdline import execute
import os
import sys

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'small_game'])  # 把最后的参数换成你自己的爬虫名字
