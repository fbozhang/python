# -*- coding:utf-8 -*-
# @Time : 2022/4/21 17:17
# @Author: fbz
# @File : asyncioTest.py

import asyncio
import time

# async def asd():    # 异步协程函数
#     print("asd")
#
# if __name__ == '__main__':
#     f = asd()   # 此时的函数是异步协程函数, 执行函数得到的是一个协程对象
#     print(f)
#     asyncio.run(f)  # 协程程序运行需要asyncio模块的支持

'''
async def asd1():  # 异步协程函数
    print("asd")
    # time.sleep(3)   # time.sleep相当于同步操作，当程序出现了同步操作的时候， 异步就中断了
    await asyncio.sleep(3)      # 异步操作的代码
    print("asd")


async def asd2():  # 异步协程函数
    print("qwe")
    # time.sleep(2)
    await asyncio.sleep(2)
    print("qwe")


async def asd3():  # 异步协程函数
    print("zxc")
    # time.sleep(4)
    await asyncio.sleep(4)
    print("zxc")


if __name__ == '__main__':
    a1 = asd1()
    a2 = asd2()
    a3 = asd3()
    tasks = [
        a1, a2, a3
    ]
    t1 = time.time()
    # 一次性启动多个任务(协程)
    asyncio.run(asyncio.wait(tasks))
    t2 = time.time()
    print(t2-t1)'''


async def asd1():  # 异步协程函数
    print("asd")
    # time.sleep(3)   # time.sleep相当于同步操作，当程序出现了同步操作的时候， 异步就中断了
    await asyncio.sleep(3)  # 异步操作的代码
    print("asd")


async def asd2():  # 异步协程函数
    print("qwe")
    # time.sleep(2)
    await asyncio.sleep(2)
    print("qwe")


async def asd3():  # 异步协程函数
    print("zxc")
    # time.sleep(4)
    await asyncio.sleep(4)
    print("zxc")


async def main():
    tasks = [
        asyncio.create_task(asd1()),    # 把协程对象变成task对象
        asyncio.create_task(asd2()),
        asyncio.create_task(asd3())
    ]
    await asyncio.wait(tasks)


if __name__ == '__main__':
    t1 = time.time()
    # 一次性启动多个任务(协程)
    asyncio.run(main())
    t2 = time.time()
    print(t2 - t1)
