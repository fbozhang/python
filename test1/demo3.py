# -*- coding:utf-8 -*-
# @Time : 2022/3/18 21:11
# @Author: fbz
# @File : demo3.py

import time
# \r的作用是把游标移到最前面，及再次输入的内容会覆盖前一个
for i in range(101):
    time.sleep(0.05)
    print('\rStarting...... {}%'.format(i), end='')

print("\rStarting......Done!")
