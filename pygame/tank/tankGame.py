# -*- coding:utf-8 -*-
# @Time : 2022/5/23 23:42
# @Author: fbz
# @File : tankGame.py

"""
v1.03
    新增功能:
    事件处理:
        点击关闭按钮，推出程序的事件
        方向控制，子弹发射
"""

import pygame

version = "v1.02"
COLOR_BLACK = pygame.Color(0, 0, 0)


class MainGame():
    # 游戏主窗口
    window = None
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 400

    def __init__(self):
        pass

    # 开始游戏方法
    def startGame(self):
        # 创建窗口加载窗口
        MainGame.window = pygame.display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])
        # 设置游戏标题
        pygame.display.set_caption("坦克大战" + version)
        # 让窗口持续刷新操作
        while True:
            # 给窗口填充颜色
            MainGame.window.fill(COLOR_BLACK)
            # 在循环中持续完成事件的获取
            self.getEvent()
            # 窗口的刷新
            pygame.display.update()

    # 获取程序运行期间所有事件(鼠标事件，键盘事件)
    def getEvent(self):
        key = pygame.key.get_pressed()
        # 1.获取所有事件
        eventList = pygame.event.get()
        # 2.对事件进行判断处理(1. 点击关闭按钮  2.按下键盘上的某个键)
        for event in eventList:
            # 判断event.type  是否QUIT，如果是退出的话，直接调用程序结束方法
            if event.type == pygame.QUIT:
                self.endGame()
            # 判断事件类型是否为按键按下，如果是:继续判断按键是哪一个按键来进行对应的处理
            if event.type == pygame.K_DOWN:
                # 具体是哪一个按键的处理
                if event.key == pygame.K_LEFT:
                    print("坦克向左调头, 移动")
                elif event.key == pygame.K_RIGHT:
                    print("坦克向右调头, 移动")
                elif event.key == pygame.K_UP:
                    print("坦克向上调头, 移动")
                elif event.key == pygame.K_DOWN:
                    print("坦克向下调头, 移动")
                elif event.key == pygame.K_SPACE:
                    print("发射子弹")

    # 结束游戏方法
    def endGame(self):
        print("谢谢使用")
        # 结束python解释器
        exit()


class Tank():
    def __init__(self):
        pass

    # 坦克的移动方法
    def move(self):
        pass

    # 射击
    def shot(self):
        pass

    # 展示
    def displayTank(self):
        pass


class MyTank(Tank):
    def __int__(self):
        pass


class EnemyTank(Tank):
    def __init__(self):
        pass


class Bullet():
    def __init__(self):
        pass

    # 子弹的移动方法
    def move(self):
        pass

    # 展示子弹的方法
    def displayBullet(self):
        pass


class Explode():
    def __init__(self):
        pass

    # 展示爆炸效果
    def displayExplode(self):
        pass


class Wall():
    def __init__(self):
        pass

    # 展示墙壁
    def displayWall(self):
        pass


class Music():
    def __init__(self):
        pass

    # 开始播放音乐
    def play(self):
        pass


MainGame().startGame()
