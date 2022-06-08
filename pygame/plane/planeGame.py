# -*- coding:utf-8 -*-
# @Time : 2022/6/8 22:14
# @Author: fbz
# @File : planeGame.py
"""
v1.03
    新增功能：
        显示飞机
        飞机可以移动
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
    # 创建我方飞机
    MYPLANE = None

    # 开始游戏方法
    def startGame(self):
        # 创建窗口加载窗口
        MainGame.window = pygame.display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])
        # 创建我方坦克
        self.creatMyPlane()
        # 设置游戏标题
        pygame.display.set_caption("飞机大战" + version)
        # 让窗口持续刷新操作
        while True:
            # 给窗口填充颜色
            MainGame.window.fill(COLOR_BLACK)
            # 显示背景
            self.blitBackground()

            if MainGame.MYPLANE and MainGame.MYPLANE.live:
                # 将我方坦克加入到窗口中
                MainGame.MYPLANE.displayPlane()
            else:
                del MainGame.MYPLANE
                MainGame.MYPLANE = None
            # 在循环中持续完成事件的获取
            self.getEvent()
            # 我方飞机移动
            self.planeMove(MainGame.MYPLANE)
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
                    MainGame.MYPLANE.direction = "L"
                    MainGame.MYPLANE.stop = False
                elif event.key == pygame.K_RIGHT:
                    print("向右移动")
                    MainGame.MYPLANE.direction = "R"
                    MainGame.MYPLANE.stop = False
                elif event.key == pygame.K_UP:
                    print("向上移动")
                    MainGame.MYPLANE.direction = "U"
                    MainGame.MYPLANE.stop = False
                elif event.key == pygame.K_DOWN:
                    print("向下移动")
                    MainGame.MYPLANE.direction = "D"
                    MainGame.MYPLANE.stop = False
                elif event.key == pygame.K_SPACE:
                    print("发射子弹")
            # 判断方向键是否弹起
            if event.type == pygame.KEYUP:
                # 松开的如果是方向键，才更改移动开关状态
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if MainGame.MYPLANE and MainGame.MYPLANE.live:
                        # 修改飞机的移动状态
                        MainGame.MYPLANE.stop = True

    # 展示背景
    def blitBackground(self):
        Background(MainGame.background).displayBackground()

    # 创建我方坦克
    def creatMyPlane(self):
        MainGame.MYPLANE = MyPlane(200, 600)

    def planeMove(self, plane):
        if plane and not plane.stop:
            plane.move()
            # 调用飞机与墙壁的碰撞方法,判断是否碰撞
            # plane.hitWalls()
            # 调用我方坦克与敌方坦克的碰撞方法,判断是否碰撞
            # plane.hitEnemyTank()

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
    def __init__(self, left, top):
        self.image = pygame.image.load("resources/images/plane.png")
        self.direction = "U"
        # 坦克所在的区域
        self.rect = self.image.get_rect()
        # 指定坦克初始化位置 分别距x，y轴的位置
        self.rect.left = left
        self.rect.top = top
        # 速度属性
        self.speed = 5
        # 移动开关
        self.stop = True
        # live用来记录是否活着
        self.live = True
        # 用来记录移动之前的坐标(用于坐标还原时使用)
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    def move(self):
        if self.direction == "L":
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == "R":
            if self.rect.left + self.rect.width < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == "U":
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == "D":
            if self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed

    def shot(self):
        pass

    def displayPlane(self):
        MainGame.window.blit(self.image, self.rect)


class MyPlane(Plane):
    def __init__(self, left, top):
        super(MyPlane, self).__init__(left, top)


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
