# -*- coding:utf-8 -*-
# @Time : 2022/6/8 22:14
# @Author: fbz
# @File : planeGame.py
"""
v1.01
    搭建基本框架
"""

import pygame

version = "v1.01"
COLOR_BLACK = pygame.Color(0, 0, 0)


class MainGame():
    # 游戏主窗口
    window = None
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 700

    def __init__(self):
        pass

    # 开始游戏方法
    def startGame(self):
        # 创建窗口加载窗口
        MainGame.window = pygame.display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])
        # 设置游戏标题
        pygame.display.set_caption("飞机大战" + version)
        # 让窗口持续刷新操作
        while True:
            # 给窗口填充颜色
            MainGame.window.fill(COLOR_BLACK)
            # 窗口的刷新
            pygame.display.update()

    # 结束游戏方法
    def endGame(self):
        pass


class Plane():
    def __init__(self):
        pass

    def move(self):
        pass

    def shot(self):
        pass

    def displayTank(self):
        pass


class MyPlane(Plane):
    def __int__(self):
        pass


class EnemyPlane(Plane):
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


class Music():
    def __init__(self):
        pass

    # 开始播放音乐
    def play(self):
        pass


MainGame().startGame()
