# -*- coding:utf-8 -*-
# @Time : 2022/3/24 15:51
# @Author: fbz
# @File : spyder.py

from bs4 import BeautifulSoup  # 網頁解析，獲取數據
import re  # 正則表達式，進行文字匹配
import urllib.request, urllib.error  # 制定URL，獲取網頁數據
import xlwt  # 進行excel操作
import sqlite3  # 進行SQLite數據庫操作
import os


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 爬取網頁
    datalist = getData(baseurl)

    savepath = "豆瓣250.xls"
    dbpath = "douban.db"
    # 保存數據
    # saveDataXls(datalist, savepath)
    saveDataDB(datalist, dbpath)

    while True:  # 询问是否删除临时文件
        rmdir = input("删除temp中html请输入(Y/N): ")
        if rmdir == 'Y' or rmdir == 'y':
            for i in range(1):
                os.remove("./temp/第%d页.html" % (i + 1))
            print("已删除")
            break
        elif rmdir == 'N' or rmdir == 'n':
            break
        else:
            print("请重新输入")


# 影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则（字符串的模式）
# 影片图片链接的规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S 让换行符包含再字符中
# 影片片名链接的规则
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分链接的规则
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 找到评价人数
findJudge = re.compile(r'<span>(.*)人评价</span>')
# 找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取網頁
def getData(baseurl):
    datalist = []
    if os.path.exists("./temp"):
        pass
    else:
        os.mkdir("temp")  # 新建一个目录

    for i in range(10):
        # url = baseurl + str(i * 25)
        # html = askURL(url)  # 保存获取到的网页源码

        if os.path.exists("./temp/第%d页.html" % (i + 1)):  # 判断html文件是否存在不存在则生成对应html
            continue
        else:
            savaHTML(baseurl, i)

        file = open("./temp/第%d页.html" % (i + 1), "rb")
        html = file.read().decode("utf-8")
        # 逐一解析數據
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_="item"):
            # print(item)  # 测试： 查看电影item全部信息
            data = []  # 保存一部电影的所有信息
            item = str(item)

            # 影片详情的链接
            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定的字符串
            data.append(link)  # 添加链接
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)  # 添加图片
            titles = re.findall(findTitle, item)  # 片名可能只有一个中文名，没有外国名
            if (len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)  # 添加中文名
                etitle = titles[1].replace("/", "")  # 去掉无关的符号
                data.append(etitle)  # 添加外国名
            else:
                data.append(titles[0])
                data.append('')  # 外国名留空

            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加评分
            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)  # 添加评价人数

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)  # 添加概述
            else:
                data.append(" ")

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 去掉<br/>
            bd = re.sub('/', " ", bd)  # 替换/
            data.append(bd.strip())  # 去掉前后的空格

            datalist.append(data)  # 把处理好的一部电影信息放入datalist

        file.close()

    return datalist


def savaHTML(baseurl, i):  # 保存为html文件
    url = baseurl + str(i * 25)
    html = askURL(url)  # 保存获取到的网页源码
    # print(html)
    filename = "./temp/第%d页.html" % (i + 1)
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(html)


# 得到指定一個URL的網頁内容
def askURL(url):
    head = {  # 模擬瀏覽器頭部信息，向豆瓣服務器發送消息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }  # 用戶代理，表示告訴豆瓣服務器，我們是什麽類型的機器、瀏覽器（本質上是告訴瀏覽器，我們可以接收什麽水平的文件内容）
    request = urllib.request.Request(url=url, headers=head)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as err:
        if hasattr(err, "code"):
            print(err.code)
        if hasattr(err, "reason"):
            print(err.reason)

    return html


# 保存數據到excel
def saveDataXls(datalist, savepath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet("豆瓣250", cell_overwrite_ok=True)  # 创建工作表
    col = ["电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价人数", "概况", "相关信息"]
    for i in range(8):
        sheet.write(0, i, col[i])  # 列名
    # 索引遍历
    # for i in range(250):
    #     data = datalist[i]
    #     for j in range(8):
    #         sheet.write(i + 1, j, data[j])  # 数据
    # 直接遍历
    for i in datalist:
        for j in i:
            sheet.write(datalist.index(i) + 1, i.index(j), j)  # 数据

    book.save(savepath)  # 保存数据表


# 保存数据到数据库
def saveDataDB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)  # 打开或创建数据库文件
    print("成功打开数据库")
    cursor = conn.cursor()  # 获取游标

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
                insert into movie(
                    info_link,pic_link,cname,ename,score,rated,instroduction,info)
                    values (%s)
        ''' % ",".join(data)
        # print(sql)    #测试得到的sql
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交数据库操作
    cursor.close()
    conn.close()  # 关闭数据库连接
    print("插入数据完毕")


# 创建数据库表
def init_db(dbpath):
    conn = sqlite3.connect(dbpath)  # 打开或创建数据库文件
    print("成功创建数据库")
    cursor = conn.cursor()  # 获取游标

    sql = '''
            create table if not exists movie
                (
                id integer primary key autoincrement,
                info_link text,
                pic_link text,
                cname varchar,
                ename varchar,
                score numeric,
                rated numeric,
                instroduction text,
                info text
                );

        '''

    cursor.execute(sql)  # 执行sql语句
    conn.commit()  # 提交数据库操作
    conn.close()  # 关闭数据库连接

    print("成功建表")


if __name__ == "__main__":
    # 調用函數
    main()
    print("爬取完毕")
