# -*- coding:utf-8 -*-
# @Time : 2022/4/21 18:12
# @Author: fbz
# @File : aiohttpTest.py

import asyncio
import aiohttp

urls = [
    "http://kr.shanghai-jiuxin.com/file/mm/20211129/cv5xpueozr5.jpg",
    "http://kr.shanghai-jiuxin.com/file/mm/20211129/wjgc4eu1rqr.jpg",
    "http://kr.shanghai-jiuxin.com/file/mm/20211129/1dl52zzfawi.jpg"
]


async def aiodownload(url):
    # s = aiohttp.ClientSession()     <==> requests
    # s.get() -> requests.get()
    name = url.rsplit("/", 1)[1]  # 从右边切，切一次，得到[1]位置的内容
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            # resp.content.read() => resp.content
            with open(name, mode="wb") as f:
                f.write(await resp.content.read())  # 读取内容是异步的, 需要await挂起
    print(name, "over")


async def main():
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(aiodownload(url)))
    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())
