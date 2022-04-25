# -*- coding:utf-8 -*-
# @Time : 2022/4/23 1:29
# @Author: fbz
# @File : app_movie.py

import json
import os
import time
import requests
import asyncio
import aiohttp
import aiofiles
from lxml import etree
from Crypto.Cipher import AES

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}


def get_m3u8(url):
    player_data = "/html/body/div[1]/div/div[3]/div[1]/div/script[1]/text()"
    resp = requests.get(url, headers=headers)
    tree = etree.HTML(resp.text)
    player_data_dic = tree.xpath(player_data)[0]
    player_data_dic = str(player_data_dic).split("=")[1]  # 转为字符串, 并进行切割得到=后的{}
    player_data_dic = json.loads(player_data_dic)  # 转为字典
    # print(player_data_dic,type(player_data_dic))
    m3u8_url = player_data_dic['url']
    # print(m3u8_url)
    return m3u8_url


def download_m3u8(m3u8, name):
    resp = requests.get(m3u8)
    with open(name, mode="wb") as f:
        f.write(resp.content)


async def download_ts(url, name, session):
    async with session.get(url) as resp:
        async with aiofiles.open(f"video/{name}", mode="wb") as f:
            await f.write(await resp.content.read())  # 把下载的内容写入到文件中
    print(f"{name} Over")


async def aio_download(domain):  # https://cdn6.sxmzwl.com:65
    tasks = []
    n = 1
    async with aiohttp.ClientSession() as session:  # 提前准备好session
        async with aiofiles.open("second_m3u8.txt", mode="r", encoding="utf-8") as f:
            async for line in f:
                line = line.strip()
                if line.startswith("#"):
                    continue
                # line => xxx.ts
                ts_url = line
                # name = line.split("hls/")[1]
                task = asyncio.create_task(download_ts(ts_url, f"{n}.ts", session))  # 创建任务
                tasks.append(task)
                n += 1

            await asyncio.wait(tasks)  # 等待任务结束


def get_key(url):
    resp = requests.get(url)
    print(resp.text)
    return resp.text


async def dec_ts(name, key):
    aes = AES.new(key=key.encode("utf-8"), IV=b"0000000000000000", mode=AES.MODE_CBC)  # IV看key的长度
    async with aiofiles.open(f"video/{name}", mode="rb") as f1, \
            aiofiles.open(f"video/temp_{name}", mode="wb") as f2:
        bs = await f1.read()  # 从源文件读取内容
        await f2.write(aes.decrypt(bs))  # 把解密好的内容写入文件
    print(f"{name}处理完毕")


async def aio_dec(key):
    # 解密
    tasks = []
    n = 1
    async with aiofiles.open("second_m3u8.txt", mode="r", encoding="utf-8") as f:
        async for line in f:
            line = line.strip()
            if line.startswith("#"):
                continue
            # 开始创建异步任务
            # name = line.split("hls/")[1]
            task = asyncio.create_task(dec_ts(f"{n}.ts", key))
            tasks.append(task)
            n += 1
        await asyncio.wait(tasks)


def merge_ts():
    # mac: cat 1.ts 2.ts 3.ts > xxx.mp4
    # windows: copy /b 1.ts+2.ts+3.ts xxx.mp4
    lst = []
    with open("second_m3u8.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()  # 去空白空格或者换行符
            if line.startswith("#"):
                continue
            name = line.split("hls/")[1]
            lst.append(f"video/temp_{name}")

    '''
    # mac:
    s = " ".join(lst)   # 1.ts 2.ts 3.ts
    os.system(f"cat {s} > movie.mp4")
    print("OVER!!")
    '''
    # windows:
    s = "+".join(lst)  # 1.ts+2.ts+3.ts
    # print(s, type(s))
    os.system(f"copy /b {s} movie.ts")
    # a = "copy /b video\temp_*.ts movie.mp4"
    # os.system(a)
    print("OVER!!")


def main(url):
    first_m3u8_url = get_m3u8(url)
    # 得到域名
    m3u8_domain = "https://" + first_m3u8_url.split("/")[2]
    # print(m3u8_domain)
    # 下载第一层m3u8
    download_m3u8(first_m3u8_url, "first_m3u8.txt")
    print("first_m3u8 Over")
    # 下载第二层m3u8
    with open("first_m3u8.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()  # 去空白空格或者换行符
            if line.startswith("#"):
                continue
            # 拼接得到第二层m3u8的地址
            second_m3u8_domain = m3u8_domain + line
            # print(second_m3u8_domain)
            download_m3u8(second_m3u8_domain, "second_m3u8.txt")
            print("second_m3u8 Over")

    # 异步协程
    # asyncio.run(aio_download(m3u8_domain))
    loop = asyncio.get_event_loop()  # 可以防止报错
    loop.run_until_complete(aio_download(m3u8_domain))

    # 拿到密钥
    key_url = "https://iqiyi.shanshanku.com/20211015/oXpCawKB/1200kb/hls/key.key"
    key = get_key(key_url)
    # 解密
    asyncio.run(aio_dec(key))

    # 合并ts文件为mp4文件
    merge_ts()


if __name__ == '__main__':
    t1 = time.time()
    url = "https://app.movie/index.php/vod/play/id/207443/sid/1/nid/1.html"
    main(url)
    t2 = time.time()
    print(t2 - t1, "秒")
