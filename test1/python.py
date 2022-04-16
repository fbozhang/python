# -*- coding:utf-8 -*-
# @Time : 2022/3/18 17:22
# @Author: fbz
# @File : python.py

import turtle

turtle.setup(1000,500,200,200)
# turtle.speed(10)      #設置畫筆速度
turtle.penup()
turtle.fd(-250)
turtle.pendown()
turtle.pensize(25)
turtle.pencolor("purple")
turtle.seth(-40)
color = ["black","gold","violet","green","red"]
for i in color:
    turtle.circle(40,80)
    turtle.circle(-40,80)
    turtle.pencolor(i)

turtle.circle(40,80/2)
turtle.fd(40)
turtle.circle(16,180)
turtle.fd(40*2/3)

turtle.exitonclick()        #暫停窗口點擊退出