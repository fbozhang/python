# -*- coding:utf-8 -*-
# @Time : 2022/4/20 23:11
# @Author: fbz
# @File : ThreadTest.py

from threading import Thread  # 线程类

# 多线程
# 方法1
# def asd():
#     for i in range(1000):
#         print("asd", i)
#
#
# if __name__ == '__main__':
#     t = Thread(target=asd)  # 创建线程并给线程安排任务
#     t.start()  # 多线程状态为可以开始工作状态, 具体执行时间由CPU决定
#     for i in range(1000):
#         print("qwe", i)

# 方法2
# class MyThread(Thread):
#     def run(self):  # 固定的 -> 当线程被执行之后, 被执行的就是run()
#         for i in range(1000):
#             print("子线程", i)
#
#
# if __name__ == '__main__':
#     t = MyThread()  # 创建一个对象
#     # t.run() # 方法的调用 -> 单线程
#     t.start()
#
#     for i in range(1000):
#         print("主线程", i)


def asd(name):
    for i in range(1000):
        print(name, i)


if __name__ == '__main__':
    t1 = Thread(target=asd, args=("ads", ))  # 传递参数必须是元组
    t1.start()

    t2 = Thread(target=asd, args=("qwe",))  # 传递参数必须是元组
    t2.start()




'''
# 多进程
from multiprocessing import Process  # 进程类


def asd():
    for i in range(1000):
        print("子进程", i)


if __name__ == '__main__':
    p = Process(target=asd)  # 创建线程并给线程安排任务
    p.start()  # 多线程状态为可以开始工作状态, 具体执行时间由CPU决定
    for i in range(1000):
        print("主进程", i)'''
