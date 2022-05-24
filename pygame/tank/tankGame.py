# -*- coding:utf-8 -*-
# @Time : 2022/5/23 23:42
# @Author: fbz
# @File : tankGame.py

"""
v1.04
    新增功能:
    实现左上角问题提示内容
        font
"""

import pygame

version = "v1.04"
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_RED = pygame.Color(255, 0, 0)


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
            # 将绘制文字得到的小画布粘贴到窗口中
            MainGame.window.blit(self.getTextSurface("剩余敌方坦克%d辆"%5), (5,5))
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
                    print("坦克向左调头, 移动")
                elif event.key == pygame.K_RIGHT:
                    print("坦克向右调头, 移动")
                elif event.key == pygame.K_UP:
                    print("坦克向上调头, 移动")
                elif event.key == pygame.K_DOWN:
                    print("坦克向下调头, 移动")
                elif event.key == pygame.K_SPACE:
                    print("发射子弹")
        # 获取键盘的第二种方法，后面再再决定用上面还是下面的方法
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            print("坦克向左调头, 移动")
        elif key[pygame.K_w]:
            print("坦克向上调头, 移动")
        elif key[pygame.K_s]:
            print("坦克向下调头, 移动")
        elif key[pygame.K_d]:
            print("坦克向右调头, 移动")

    # 左上角文字绘制
    def getTextSurface(self, text):
        # 字体初始化
        pygame.font.init()
        # 查看系统支持的所有字体
        # fontList = pygame.font.get_fonts()
        # print(fontList)
        # 选择一个合适的字体
        font = pygame.font.SysFont("kaiti", 18)     # pygame.font.SysFont("字体名称", 字号, 默认不粗体, 默认不斜体)
        # 使用对应的字符完成相关内容的绘制
        textSurface = font.render(text, True, COLOR_RED)    # font.render(文字, 是否抗锯齿, 颜色, 背景默认没有)
        return textSurface

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
