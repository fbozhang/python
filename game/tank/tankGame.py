# -*- coding:utf-8 -*-
# @Time : 2022/5/23 20:40
# @Author: fbz
# @File : tankGame.py

"""
v1.02
    新增功能:
        创建游戏窗口
        用到游戏引擎中的功能模块
        官方开发文档
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
            # 窗口的刷新
            pygame.display.update()

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