# -*- coding:utf-8 -*-
# @Time : 2022/5/23 23:42
# @Author: fbz
# @File : tankGame.py
import math
import random
import sys
import time
import pygame

version = "v2.02"

f"""
{version}
    新增功能：
        按F4开启外挂模式，子弹自动追踪敌方坦克
"""

COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_RED = pygame.Color(255, 0, 0)


class MainGame():
    # 游戏主窗口
    window = None
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500
    # 背景
    background = "images/background.gif"
    # 创建我方水晶
    Home = None
    # 创建我方坦克
    TANK_P1 = None
    # 存储所有的敌方坦克
    EnemyTank_List = []
    # 要创建的敌方坦克的数量
    EnemyTank_count = 2
    # 存储我方子弹的列表
    Bullet_List = []
    # 存储敌方子弹的列表
    Enemy_bullet_List = []
    # 爆炸效果列表
    Explode_List = []
    # 墙壁列表
    Wall_List = []
    # 外挂模式
    cheat = False

    # 开始游戏
    def startGame(self):
        # 初始化显示模块
        pygame.display.init()
        # 创建窗口加载窗口
        MainGame.window = pygame.display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])
        # 创建我方坦克
        self.creatMyTank()
        # 创建敌方坦克
        self.creatEnemyTank()
        # 创建水晶
        self.creatHome()
        # 创建墙壁
        self.creatWalls()
        # 设置游戏标题
        pygame.display.set_caption("坦克大战" + version)
        # 创建音乐对象
        music = Music("audios/start.wav")
        # 调用播放音乐方法
        music.play()
        # 让窗口持续刷新操作
        while True:
            # 给窗口填充颜色
            MainGame.window.fill(COLOR_BLACK)
            # 显示背景
            self.blitBackground()
            # 在循环中持续完成事件的获取
            self.getEvent()
            # 将绘制文字得到的小画布粘贴到窗口中
            MainGame.window.blit(self.getTextSurface("剩余敌方坦克%d辆" % len(MainGame.EnemyTank_List)), (5, 5))
            # 调用展示墙壁的方法
            self.blitWalls()
            # 展示水晶
            self.blitHome()
            if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                # 将我方坦克加入到窗口中
                MainGame.TANK_P1.displayTank()
            else:
                del MainGame.TANK_P1
                MainGame.TANK_P1 = None
            # 将敌方坦克加入到窗口中
            self.blitEnemyTank()
            # 根据坦克的开关状态调用坦克的移动方法
            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()
                # 调用坦克与墙壁的碰撞方法,判断是否碰撞
                MainGame.TANK_P1.hitWalls()
                # 调用我方坦克与敌方坦克的碰撞方法,判断是否碰撞
                MainGame.TANK_P1.hitEnemyTank()
            # 调用渲染我方子弹列表的一个方法
            self.blitBullet()
            # 调用渲染敌方子弹列表的一个方法
            self.blitEnemyBullet()
            # 调用展示爆炸效果的方法
            self.displayExplodes()
            time.sleep(0.02)
            if not MainGame.Home.live:
                # 将绘制文字得到的小画布粘贴到窗口中
                MainGame.window.blit(self.getTextSurface_gameover("Game Over!!"),
                                     (200, MainGame.SCREEN_HEIGHT / 2 - 60))
            if len(MainGame.EnemyTank_List) == 0:
                MainGame.window.blit(self.getTextSurface_gameover("victory!!"),
                                     (250, MainGame.SCREEN_HEIGHT / 2 - 60))
            # 窗口的刷新
            pygame.display.update()

    # 创建我方坦克
    def creatMyTank(self):
        MainGame.TANK_P1 = MyTank(275, 440)

    # 创建敌方坦克
    def creatEnemyTank(self):
        top = 100
        for i in range(MainGame.EnemyTank_count):
            speed = random.randint(3, 6)
            left = random.randint(1, int(MainGame.SCREEN_WIDTH / 100 - 1))
            eTank = EnemyTank(left * 100, top, speed)
            MainGame.EnemyTank_List.append(eTank)

    # 创建墙壁
    def creatWalls(self):
        # 创建障碍物
        for i in range(6):
            for j in range(2):
                for k in range(2):
                    wall = Wall(140 * i + 31 * j, MainGame.SCREEN_HEIGHT / 2 - 31 * k)
                    MainGame.Wall_List.append(wall)

        # 创建水晶保护墙
        for i in range(3):
            for j in range(4):
                if i != 0:
                    if j == 0 or j == 4 - 1:
                        wall = Wall(MainGame.Home.rect.left - 31 + 30 * j, MainGame.SCREEN_HEIGHT - 30 * i)
                        MainGame.Wall_List.append(wall)
                else:
                    wall = Wall(MainGame.Home.rect.left - 31 + 30 * j, MainGame.SCREEN_HEIGHT - 30 * 3)
                    MainGame.Wall_List.append(wall)

    # 创建我方水晶
    def creatHome(self):
        MainGame.Home = Home()

    # 将墙壁加入到窗口中
    def blitWalls(self):
        for wall in MainGame.Wall_List:
            if wall.live:
                wall.displayWall()
            else:
                MainGame.Wall_List.remove(wall)

    # 展示背景
    def blitBackground(self):
        Background(MainGame.background).displayBackground()

    # 将水晶标志加入到窗口中
    def blitHome(self):
        MainGame.Home.displayHome()

    # 将敌方坦克加入到窗口中
    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_List:
            if eTank.live:
                eTank.displayTank()  # 继承父类
                # 坦克移动
                eTank.randMove()
                # 调用坦克与墙壁的碰撞方法
                eTank.hitWalls()
                # 敌方坦克是否撞到我方坦克
                eTank.hitMyTank()
                # 调用敌方坦克的射击
                eBullet = eTank.shot()
                # 如果子弹为None，不加入到列表
                if eBullet:
                    # 将子弹存储敌方子弹列表
                    MainGame.Enemy_bullet_List.append(eBullet)
            else:
                MainGame.EnemyTank_List.remove(eTank)

    # 将我方子弹加入到窗口中
    def blitBullet(self):
        for bullet in MainGame.Bullet_List:
            # 如果子弹还活着绘制出来，否则直接从列表中移除该子弹
            if bullet.live:
                bullet.displayBullet()
                print(bullet.cheat)
                bullet.cheat = MainGame.cheat
                if bullet.cheat:
                    # 子弹追踪
                    if len(MainGame.EnemyTank_List) > 0:
                        bullet.bulletFollowMove(MainGame.EnemyTank_List[0].rect.left,
                                                MainGame.EnemyTank_List[0].rect.top)
                else:
                    # 让子弹移动
                    bullet.bulletMove()
                # 判断我方子弹与敌方坦克是否碰撞
                bullet.hitEnemyTank()
                # 判断子弹是否碰撞到墙壁
                bullet.hitWalls()
                # 判断子弹是否碰撞
                bullet.hitBullet()
                # 判断子弹是否打到水晶
                bullet.hitHome()
            else:
                MainGame.Bullet_List.remove(bullet)

    # 将敌方子弹加入到窗口中
    def blitEnemyBullet(self):
        for eBullet in MainGame.Enemy_bullet_List:
            # 如果子弹还活着绘制出来，否则直接从列表中移除该子弹
            if eBullet.live:
                eBullet.displayBullet()
                # 让子弹移动
                eBullet.bulletMove()
                # 判断子弹是否碰撞到墙壁
                eBullet.hitWalls()
                # 判断子弹是否打到水晶
                eBullet.hitHome()
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    eBullet.hitMyTank()
            else:
                MainGame.Enemy_bullet_List.remove(eBullet)

    # 展示爆炸效果列表
    def displayExplodes(self):
        for explode in MainGame.Explode_List:
            if explode.live:
                explode.displayExplode()
            else:
                MainGame.Explode_List.remove(explode)

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
                # 点击F1按键让我方坦克重生
                if event.key == pygame.K_F1 and not MainGame.TANK_P1:
                    # 调用创建我方坦克方法
                    self.creatMyTank()
                # 点击F2按键让我方水晶重生
                if event.key == pygame.K_F2 and not MainGame.Home.live:
                    MainGame.Home.live = True
                # 点击F3按键让敌方坦克重生
                if event.key == pygame.K_F3 and len(MainGame.EnemyTank_List) == 0:
                    self.creatEnemyTank()
                if event.key == pygame.K_F4:
                    MainGame.cheat = True
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
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
                            m = MainGame.TANK_P1.shot()
                            # 将子弹加入到子弹列表
                            MainGame.Bullet_List.append(m)
                            music = Music("audios/fire.wav")
                            music.play()
                        else:
                            print("子弹数量不足")
                        print("当前屏幕中的子弹数量为：%d" % len(MainGame.Bullet_List))
            # 判断方向键是否弹起
            if event.type == pygame.KEYUP:
                # 松开的如果是方向键，才更改移动开关状态
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                        # 修改坦克的移动状态
                        MainGame.TANK_P1.stop = True
        # 获取键盘的第二种方法，考虑后面用该方法控制2P
        key = pygame.key.get_pressed()
        if MainGame.TANK_P1 and MainGame.TANK_P1.live:
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

    # 游戏结束提示
    def getTextSurface_gameover(self, text):
        # 字体初始化
        pygame.font.init()
        # 查看系统支持的所有字体
        # fontList = pygame.font.get_fonts()
        # print(fontList)
        # 选择一个合适的字体
        font = pygame.font.SysFont("kaiti", 60, bold=True, italic=True)  # pygame.font.SysFont("字体名称", 字号, 默认不粗体, 默认不斜体)
        # 使用对应的字符完成相关内容的绘制
        textSurface = font.render(text, True, COLOR_RED)  # font.render(文字, 是否抗锯齿, 颜色, 背景默认没有)
        return textSurface

    # 结束游戏
    def endGame(self):
        print("谢谢使用")
        # 结束python解释器
        # exit()
        # 结束程序
        sys.exit()


# 背景
class Background():
    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0

    def displayBackground(self):
        MainGame.window.blit(self.image, self.rect)


class BaseItem(pygame.sprite.Sprite):
    def __int__(self):
        pygame.sprite.Sprite.__init__(self)


class Tank(BaseItem):
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
        # 速度属性
        self.speed = 5
        # 坦克的移动开关
        self.stop = True
        # live用来记录，坦克是否活着
        self.live = True
        # 用来记录坦克移动之前的坐标(用于坐标还原时使用)
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    # 坦克的移动
    def move(self):
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
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

    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop

    def hitWalls(self):
        for wall in MainGame.Wall_List:
            if pygame.sprite.collide_rect(wall, self):  # 监测两个精灵的矩形是否碰撞返回布尔值
                self.stay()

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
    def __init__(self, left, top):
        super(MyTank, self).__init__(left, top)

    # 主动碰撞到敌方坦克
    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_List:
            if pygame.sprite.collide_rect(eTank, self):
                self.stay()


class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        super(EnemyTank, self).__init__(left, top)
        # self.live = True
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

    def shot(self):
        num = random.randint(1, 100)
        if num <= 2:
            return Bullet(self)

    def hitMyTank(self):
        if MainGame.TANK_P1 and MainGame.TANK_P1.live:
            if pygame.sprite.collide_rect(self, MainGame.TANK_P1):
                # 让敌方坦克停下来
                self.stay()


class Bullet(BaseItem):
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
        # 记录是否开挂
        self.cheat = False

    # 子弹的移动
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

    # 子弹跟踪移动
    def bulletFollowMove(self, x, y):
        velocity = 10000
        time = 1 / 1000
        space = velocity * time
        clock = pygame.time.Clock()  # 创建时钟对象
        clock.tick(120)  # 每秒最多循环60次，即设置帧率为60

        distance = math.sqrt(pow(x - self.rect.left, 2) + pow(y - self.rect.top, 2))
        sina = (y - self.rect.top) / distance
        cosa = (x - self.rect.left) / distance
        self.rect.left = self.rect.left + space * cosa
        self.rect.top = self.rect.top + space * sina
        print(self.rect.left,self.rect.top, x, y)

    # 展示子弹
    def displayBullet(self):
        MainGame.window.blit(self.image, self.rect)

    # 我方子弹碰撞敌方坦克
    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_List:
            if pygame.sprite.collide_rect(eTank, self):  # 监测两个精灵的矩形是否碰撞返回布尔值
                # 产生一个爆炸效果
                explode = Explode(eTank)
                # 将爆炸效果加入到爆炸效果列表
                MainGame.Explode_List.append(explode)
                # 如果打中坦克修改状态值
                self.live = False
                eTank.live = False

    # 敌方子弹碰撞我方坦克
    def hitMyTank(self):
        if pygame.sprite.collide_rect(self, MainGame.TANK_P1):
            # 产生爆炸效果，并加入到爆炸效果列表中
            explode = Explode(MainGame.TANK_P1)
            MainGame.Explode_List.append(explode)
            # 修改子弹状态
            self.live = False
            # 修改我方坦克状态
            MainGame.TANK_P1.live = False

    # 新增子弹与墙壁的碰撞
    def hitWalls(self):
        for wall in MainGame.Wall_List:
            if pygame.sprite.collide_rect(self, wall):
                # 修改子弹状态
                self.live = False
                wall.hp -= 1
                if wall.hp <= 0:
                    wall.live = False

    # 双方子弹碰撞
    def hitBullet(self):
        for bullet in MainGame.Enemy_bullet_List:
            if pygame.sprite.collide_rect(bullet, self):  # 监测两个精灵的矩形是否碰撞返回布尔值
                # 如果打中子弹修改状态值
                self.live = False
                bullet.live = False

    # 子弹碰撞水晶
    def hitHome(self):
        if pygame.sprite.collide_rect(self, MainGame.Home):
            # 修改子弹状态
            self.live = False
            # 修改我方水晶状态
            MainGame.Home.live = False


class Explode():
    def __init__(self, tank):
        self.rect = tank.rect
        self.step = 0
        self.images = [
            pygame.image.load("images/blast0.gif"),
            pygame.image.load("images/blast1.gif"),
            pygame.image.load("images/blast2.gif"),
            pygame.image.load("images/blast3.gif"),
            pygame.image.load("images/blast4.gif")
        ]
        self.image = self.images[self.step]
        self.live = True

    # 展示爆炸效果
    def displayExplode(self):
        if self.step < len(self.images):
            self.image = self.images[self.step]
            MainGame.window.blit(self.image, self.rect)
            time.sleep(0.03)
            self.step += 1
        else:
            self.live = False
            self.step = 0


class Wall():
    def __init__(self, left, top):
        self.image = pygame.image.load("images/cement_wall.gif")
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        # 用来判断墙壁是否应该在窗口中展示
        self.live = True
        # 用来记录墙壁的生命值
        self.hp = 3

    # 展示墙壁
    def displayWall(self):
        MainGame.window.blit(self.image, self.rect)


class Home():
    def __init__(self):
        self.image_symbol = pygame.image.load("images/symbol.gif")
        self.image_symbol_destoryed = pygame.image.load("images/symbol_destoryed.gif")
        self.rect = self.image_symbol.get_rect()
        self.rect.left = MainGame.SCREEN_WIDTH / 2 - self.rect.width / 2
        self.rect.top = MainGame.SCREEN_HEIGHT - self.rect.height
        # 用来判断水晶还在吗
        self.live = True

    def displayHome(self):
        if self.live:
            MainGame.window.blit(self.image_symbol, self.rect)
        else:
            MainGame.window.blit(self.image_symbol_destoryed, self.rect)


class Music():
    def __init__(self, fileName):
        self.fileName = fileName
        # 先初始化混响器
        pygame.mixer.init()
        # 加载音乐文件进行播放
        pygame.mixer.music.load(self.fileName)

    # 开始播放音乐
    def play(self):
        # loops是一个可选的整数参数，默认情况下为0，表示重复音乐的次数(lopps=5,即播放一次重复5次一共6次)。如果此参数设置为-1，则音乐无限重复
        pygame.mixer.music.play(loops=0)


if __name__ == '__main__':
    MainGame().startGame()
