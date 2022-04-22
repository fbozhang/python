# -*- coding:utf-8 -*-
# @Time : 2022/4/21 21:56
# @Author: fbz
# @File : dushu.py
# https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"4315647161"}   -> 所有章节的内容(名称，cid)
# https://dushu.baidu.com/api/pc/getChapterContent?data={"book_id":"4315647161","cid":"4315647161|10221391","need_bookinfo":1}  -> 章节内部内容

import json
import time
import requests
import asyncio
import aiohttp
import aiofiles

'''
1.同步操作: 访问getCatalog 拿到所有章节的cid和名称
2.异步操作: 访问getChapterContent 下载所有文章的内容
'''


def Format(Str):
    String = f'''{Str}'''
    list_s = list(String)  # str -> list

    num = 0
    i = 0
    for j in list_s:
        if list_s[i] == "\n":
            list_s[i] = "\n\n"
            num = 0
        if num == 46:
            list_s.insert(i, '\n')
            num = 0
        num += 1
        i += 1
    # print(list_s)

    String = ''.join(list_s)  # list -> str
    # print(String)
    return String


async def aiodownload(title, cid, b_id):
    data = {
        "book_id": b_id,
        "cid": f"{b_id}|{cid}",
        "need_bookinfo": 1
    }
    data = json.dumps(data)
    url = f"https://dushu.baidu.com/api/pc/getChapterContent?data={data}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            dic = await resp.json()
            txt = dic['data']['novel']['content']
            # print(txt)
            txt = Format(txt)
            print(title, "over")
            async with aiofiles.open("novel/" + title + ".txt", mode="w", encoding="utf-8") as f:
                await f.write(txt)  # 把小说内容写出


async def getCatalog(url):
    resp = requests.get(url)
    # print(resp.json())
    dic = resp.json()
    tasks = []
    items = dic['data']['novel']['items']
    for item in items:
        title = item['title']
        cid = item['cid']
        # print(title, cid)
        # 准备异步任务
        tasks.append(asyncio.create_task(aiodownload(title, cid, b_id)))

    await asyncio.wait(tasks)


if __name__ == '__main__':
    t1 = time.time()
    b_id = "4306063500"
    url = 'https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":' + b_id + '}'
    # asyncio.run(getCatalog(url))
    loop = asyncio.get_event_loop()  # 可以防止报错
    loop.run_until_complete(getCatalog(url))
    t2 = time.time()
    print(t2 - t1)
