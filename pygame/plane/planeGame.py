# -*- coding:utf-8 -*-
# @Time : 2022/6/8 22:14
# @Author: fbz
# @File : planeGame.py
"""
v1.02
    添加背景
    事件处理:
        点击关闭按钮，推出程序的事件
"""

import sys

import pygame

version = "v1.01"
COLOR_BLACK = pygame.Color(0, 0, 0)


class MainGame():
    # 游戏主窗口
    window = None
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 800
    # 背景
    background = "resources/images/background.png"

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
            # 显示背景
            self.blitBackground()
            # 在循环中持续完成事件的获取
            self.getEvent()
            # 窗口的刷新
            pygame.display.update()

    # 获取程序运行期间所有事件(鼠标事件，键盘事件)
    def getEvent(self):
        # 1.获取所有事件
        eventList = pygame.event.get()
        # 2.对事件进行判断处理(1. 点击关闭按钮  2.按下键盘上的某个键)
        for event in eventList:
            # 判断event.type  是否QUIT，如果是退出的话，直接调用程序结束方法
            if event.type == pygame.QUIT:
                self.endGame()
            # 判断事件类型是否为按键按下，如果是:继续判断按键是哪一个按键来进行对应的处理
            if event.type == pygame.KEYDOWN:
                # 具体是哪一个按键的处理
                if event.key == pygame.K_LEFT:
                    print("向左移动")
                elif event.key == pygame.K_RIGHT:
                    print("向右移动")
                elif event.key == pygame.K_UP:
                    print("向上移动")
                elif event.key == pygame.K_DOWN:
                    print("向下移动")
                elif event.key == pygame.K_SPACE:
                    print("发射子弹")

    # 展示背景
    def blitBackground(self):
        Background(MainGame.background).displayBackground()

    # 结束游戏方法
    def endGame(self):
        print("谢谢使用")
        # 结束程序
        sys.exit()


# 背景
class Background:
    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0

    def displayBackground(self):
        MainGame.window.blit(self.image, self.rect)


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


if __name__ == '__main__':
    MainGame().startGame()
