# -*- coding:utf-8 -*-
# @Time : 2022/3/19 0:24
# @Author: fbz
# @File : helicalLine.py

import turtle

turtle.setup(1000,500,200,200)
for i in range(60):
    turtle.fd(5*i)
    turtle.seth(90 * i)

turtle.exitonclick()
