# -*- coding:utf-8 -*-
# @Time : 2022/5/23 23:42
# @Author: fbz
# @File : tankGame.py

"""
v1.14
    1.子弹打中墙壁的时候，直接消除而不是粘在墙上
    2.解决我方坦克可以无限发射子弹的问题(最多3发子弹)
"""
import random
import time

import pygame

version = "v1.14"
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_RED = pygame.Color(255, 0, 0)


class MainGame():
    # 游戏主窗口
    window = None
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 400
    # 创建我方坦克
    TANK_P1 = None
    # 存储所有的敌方坦克
    EnemyTank_List = []
    # 要创建的敌方坦克的数量
    EnemyTank_count = 5
    # 存储我方子弹的列表
    Bullet_List = []

    def __init__(self):
        pass

    # 开始游戏方法
    def startGame(self):
        # 创建窗口加载窗口
        MainGame.window = pygame.display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])
        # 创建我方坦克
        MainGame.TANK_P1 = Tank(200, 300)
        # 创建敌方坦克
        self.creatEnemyTank()
        # 设置游戏标题
        pygame.display.set_caption("坦克大战" + version)
        # 让窗口持续刷新操作
        while True:
            # 给窗口填充颜色
            MainGame.window.fill(COLOR_BLACK)
            # 在循环中持续完成事件的获取
            self.getEvent()
            # 将绘制文字得到的小画布粘贴到窗口中
            MainGame.window.blit(self.getTextSurface("剩余敌方坦克%d辆" % len(MainGame.EnemyTank_List)), (5, 5))
            # 将我方坦克加入到窗口中
            MainGame.TANK_P1.displayTank()
            # 将敌方坦克加入到窗口中
            self.blitEnemyTank()
            # 根据坦克的开关状态调用坦克的移动方法
            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()
            self.blitBullet()
            time.sleep(0.01)
            # 窗口的刷新
            pygame.display.update()

    # 创建敌方坦克
    def creatEnemyTank(self):
        top = 100
        speed = random.randint(3, 6)
        for i in range(MainGame.EnemyTank_count):
            left = random.randint(1, int(MainGame.SCREEN_WIDTH / 100 - 1))
            eTank = EnemyTank(left * 100, top, speed)
            MainGame.EnemyTank_List.append(eTank)

    # 将坦克加入到窗口中
    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_List:
            eTank.displayTank()  # 继承父类
            # 坦克移动方法
            eTank.randMove()

    # 将子弹加入到窗口中
    def blitBullet(self):
        for bullet in MainGame.Bullet_List:
            # 如果子弹还活着绘制出来，否则直接从列表中移除该子弹
            if bullet.live:
                bullet.displayBullet()
                # 让子弹移动
                bullet.bulletMove()
            else:
                MainGame.Bullet_List.remove(bullet)

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
                    # 修改坦克方向
                    MainGame.TANK_P1.direction = "L"
                    MainGame.TANK_P1.stop = False
                    # 完成移动操作
                    # MainGame.TANK_P1.move()
                elif event.key == pygame.K_RIGHT:
                    print("坦克向右调头, 移动")
                    MainGame.TANK_P1.direction = "R"
                    MainGame.TANK_P1.stop = False
                elif event.key == pygame.K_UP:
                    print("坦克向上调头, 移动")
                    MainGame.TANK_P1.direction = "U"
                    MainGame.TANK_P1.stop = False
                elif event.key == pygame.K_DOWN:
                    print("坦克向下调头, 移动")
                    MainGame.TANK_P1.direction = "D"
                    MainGame.TANK_P1.stop = False
                elif event.key == pygame.K_SPACE:
                    print("发射子弹")
                    if len(MainGame.Bullet_List) < 3:
                        # 产生一颗子弹
                        m = Bullet(MainGame.TANK_P1)
                        # 将子弹加入到子弹列表
                        MainGame.Bullet_List.append(m)
                    else:
                        print("子弹数量不足")
                    print("当前屏幕中的子弹数量为：%d"%len(MainGame.Bullet_List))
            # 判断方向键是否弹起
            if event.type == pygame.KEYUP:
                # 松开的如果是方向键，才更改移动开关状态
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    # 修改坦克的移动状态
                    MainGame.TANK_P1.stop = True
        # 获取键盘的第二种方法，考虑后面用该方法控制2P
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            print("坦克向左调头, 移动")
            MainGame.TANK_P1.direction = "L"
            MainGame.TANK_P1.move()
        elif key[pygame.K_w]:
            print("坦克向上调头, 移动")
            MainGame.TANK_P1.direction = "U"
            MainGame.TANK_P1.move()
        elif key[pygame.K_s]:
            print("坦克向下调头, 移动")
            MainGame.TANK_P1.direction = "D"
            MainGame.TANK_P1.move()
        elif key[pygame.K_d]:
            print("坦克向右调头, 移动")
            MainGame.TANK_P1.direction = "R"
            MainGame.TANK_P1.move()
        # 这个方法暂未解决边移动边设计
        elif key[pygame.K_KP0]:
            print("射击")
            # 产生一颗子弹
            m = Bullet(MainGame.TANK_P1)
            # 将子弹加入到子弹列表
            MainGame.Bullet_List.append(m)

    # 左上角文字绘制
    def getTextSurface(self, text):
        # 字体初始化
        pygame.font.init()
        # 查看系统支持的所有字体
        # fontList = pygame.font.get_fonts()
        # print(fontList)
        # 选择一个合适的字体
        font = pygame.font.SysFont("kaiti", 18)  # pygame.font.SysFont("字体名称", 字号, 默认不粗体, 默认不斜体)
        # 使用对应的字符完成相关内容的绘制
        textSurface = font.render(text, True, COLOR_RED)  # font.render(文字, 是否抗锯齿, 颜色, 背景默认没有)
        return textSurface

    # 结束游戏方法
    def endGame(self):
        print("谢谢使用")
        # 结束python解释器
        exit()


class Tank():
    def __init__(self, left, top):
        self.images = {
            "U": pygame.image.load("images/p1tankU.gif"),
            "D": pygame.image.load("images/p1tankD.gif"),
            "L": pygame.image.load("images/p1tankL.gif"),
            "R": pygame.image.load("images/p1tankR.gif"),
        }
        self.direction = "U"
        self.image = self.images[self.direction]
        # 坦克所在的区域
        self.rect = self.image.get_rect()
        # 指定坦克初始化位置 分别距x，y轴的位置
        self.rect.left = left
        self.rect.top = top
        # 新增速度属性
        self.speed = 5
        # 新增属性：坦克的移动开关
        self.stop = True

    # 坦克的移动方法
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

    # 射击
    def shot(self):
        return Bullet(self)

    # 展示坦克(将坦克这个surface绘制到窗口中 blit())
    def displayTank(self):
        # 1.重新设置坦克的图片
        self.image = self.images[self.direction]
        # 2.将坦克加入到窗口中
        MainGame.window.blit(self.image, self.rect)


class MyTank(Tank):
    def __int__(self):
        pass


class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        self.images = {
            "U": pygame.image.load("images/enemy1U.gif"),
            "D": pygame.image.load("images/enemy1D.gif"),
            "L": pygame.image.load("images/enemy1L.gif"),
            "R": pygame.image.load("images/enemy1R.gif"),
        }
        self.direction = self.randDirection()
        self.image = self.images[self.direction]
        # 坦克所在的区域
        self.rect = self.image.get_rect()
        # 指定坦克初始化位置 分别距x，y轴的位置
        self.rect.left = left
        self.rect.top = top
        # 新增速度属性
        self.speed = speed
        # 坦克的移动开关
        self.stop = True
        # 新增步数属性，用来控制敌方坦克随机移动
        self.step = 20

    def randDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            # self.direction = 'U'
            return 'U'
        elif num == 2:
            # self.direction = 'D'
            return 'D'
        elif num == 3:
            # self.direction = 'L'
            return 'L'
        elif num == 4:
            # self.direction = 'R'
            return 'R'

    # 随机移动
    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = 20
        else:
            self.move()
            self.step -= 1


class Bullet():
    def __init__(self, tank):
        # 图片
        self.image = pygame.image.load("images/enemymissile.gif")
        # 方向(坦克方向)
        self.direction = tank.direction
        # 位置
        self.rect = self.image.get_rect()
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.height / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.height / 2
        # 速度
        self.speed = 7
        # 用来记录子弹是否活着
        self.live = True

    # 子弹的移动方法
    def bulletMove(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                # 如果碰壁，修改状态值
                self.live = False
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                self.live = False

    # 展示子弹的方法
    def displayBullet(self):
        MainGame.window.blit(self.image, self.rect)


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
