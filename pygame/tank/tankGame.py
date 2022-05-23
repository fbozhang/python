# -*- coding:utf-8 -*-
# @Time : 2022/5/23 23:42
# @Author: fbz
# @File : tankGame.py

"""
v1.01
1.主逻辑类
    开始游戏
    结束游戏
2.坦克类（1.我方坦克   2.敌方坦克）
    移动
    射击
    展示坦克
3.子弹类
    移动
    展示子弹
4.爆炸效果类
    展示爆炸效果
5.墙壁类
    属性：是否可以通过
6.音效类
    播放音乐
"""

import pygame


class MainGame():
    def __init__(self):
        pass

    # 开始游戏方法
    def startGame(self):
        pass

    # 结束游戏方法
    def endGame(self):
        pass


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