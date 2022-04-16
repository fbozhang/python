# -*- coding:utf-8 -*-
# @Time : 2022/3/18 18:08
# @Author: fbz
# @File : triangle.py
import turtle

turtle.setup(1000,500,200,200)
#等邊三角形
'''
for i in range(3):
    turtle.seth(120 * i)
    turtle.fd(200)
'''
#叠加等边三角形
'''
for i in range(3):
    turtle.seth(120 * i)
    turtle.fd(200)

turtle.seth(0)
turtle.fd(100)
for i in range(5,0,-2):
    turtle.seth(360 - 60 * i)
    turtle.fd(100)
'''
#六角形
'''
for i in range(3):
    turtle.seth(120 * i)
    turtle.fd(240)
turtle.seth(0)
turtle.fd(80)
turtle.seth(-60)
turtle.fd(80)
for i in range(5,0,-2):
    turtle.seth(360 - 60 * i)
    turtle.fd(240)
'''
# 多變形
angle = int(input("請輸入几角形:"))
angles = 0
for i in range(angle):
    for j in range(3):
        turtle.seth(angles)
        turtle.fd(100)
        angles += 120
    turtle.seth(angles)
    turtle.fd(100)
    angles += 360 - 360/angle

turtle.exitonclick()

