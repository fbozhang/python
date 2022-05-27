# -*- coding:utf-8 -*-
# @Time : 2022/5/27 15:01
# @Author: fbz
# @File : 三国人物出现次数.py

import json
import time
import requests
import asyncio
import aiohttp
import aiofiles
import os
import jieba
import webbrowser
from pyecharts import options as opts
from pyecharts.charts import Bar


def Format(Str):
    String = f'''{Str}'''
    list_s = list(String)

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

    String = ''.join(list_s)
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
                await f.write(txt)


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
        tasks.append(asyncio.create_task(aiodownload(title, cid, b_id)))

    await asyncio.wait(tasks)


def statistics():
    excludes = {
        "将军", "却说", "二人", "不可", "不能", "如此", "众将", "兄弟", "当先", "南皮", "当先", "商议", "百姓"
        , "冀州", "袁尚", "袁氏", "易州", "甄氏", "不如", "刘氏", "闻言", "世子", "荆州", "如何", "军士", "次日"
        , "左右", "军马", "徐州", "天下", "江东", "夫人", "今日", "不知", "先生", "不敢", "一人", "大叫", "人马"
        , "引军", "何故", "只见", "上马", "且说", "上马", "大喜", "引兵", "此人", "东吴", "下马", "赶来"
    }
    path = "novel"
    lsdir = os.listdir(path)
    files = [i for i in lsdir if os.path.isfile(os.path.join(path, i))]
    txt = ""
    for f in files:
        filename = os.path.join(path, f)
        txt += open(filename, mode="r", encoding="utf-8").read()

    words = jieba.lcut(txt)
    counts = {}
    for word in words:
        if len(word) == 1:
            continue
        elif word == "诸葛亮" or word == "孔明曰":
            rword = "孔明"
        elif word == "关公" or word == "云长":
            rword = "关羽"
        elif word == "玄德" or word == "玄德曰" or word == "主公":
            rword = "刘备"
        elif word == "孟德" or word == "丞相":
            rword = "曹操"
        else:
            rword = word
        counts[rword] = counts.get(rword, 0) + 1
    for word in excludes:
        del (counts[word])
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)

    # 导出数据
    fo = open("人物出场次数.txt", "w", encoding='utf-8')
    for i in range(20):
        word, count = items[i]
        print("{0:<10}{1:>5}".format(word, count))
        word = str(word)
        count = str(count)
        fo.write(word)
        fo.write(':')  # 使用冒号分开
        fo.write(count)
        fo.write('\n')
    fo.close()
    dataVisualization()


def dataVisualization():
    fr = open('人物出场次数.txt', 'r', encoding='utf-8')
    dic = {}
    keys = []
    for line in fr:
        v = line.strip().split(':')
        dic[v[0]] = v[1]
        keys.append(v[0])
    fr.close()
    # print(dic)
    list1 = list(dic.keys())
    list2 = list(dic.values())
    c = (
        Bar()
            .add_xaxis(list1)
            .add_yaxis("人物出场次数", list2)
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        )
            .render("人物出场次数.html")
    )
    # os.remove("人物出场次数.txt")
    webbrowser.open('人物出场次数.html')


if __name__ == '__main__':
    t1 = time.time()
    if os.path.exists("./novel"):
        pass
    else:
        os.mkdir("novel")  # 新建一个目录
        b_id = "4305593258"
        url = 'https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":' + b_id + '}'
        # asyncio.run(getCatalog(url))
        loop = asyncio.get_event_loop()  # 可以防止报错
        loop.run_until_complete(getCatalog(url))
    statistics()
    t2 = time.time()
    print(t2 - t1)
