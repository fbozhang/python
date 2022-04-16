from flask import Flask, render_template
import pandas
import sqlite3

app = Flask(__name__)

@app.route('/')
def showEcharts_Pie():
    data = pandas.read_csv("test.csv")
    # print(data)  # 查看得到的数据是否正常
    data = data.rename(columns={"影片中文名": "name", "评价人数": "value"})
    # print(data)     # 把得到的数据标题重命名为name和value
    data = data.to_dict(orient="records")  # 把数据转为字典的形式
    # print(data)
    # print(data[0])

    return render_template("douban.html", data=data)


@app.route('/index')
def showEcharts_Column():
    qwe = pandas.read_csv("test.csv")
    # print(data)  # 查看得到的数据是否正常
    qwe = qwe.rename(columns={"影片中文名": "name", "评价人数": "value"})
    # print(data)     # 把得到的数据标题重命名为name和value
    qwe = qwe.to_dict(orient="records")  # 把数据转为字典的形式

    score = []  # 评分
    num = []  # 每个评分所统计的电影数量

    conn = sqlite3.connect("douban.db")  # 打开或创建数据库文件
    print("成功打开数据库")
    cursor = conn.cursor()  # 获取游标

    sql = "select score,count(score) from movie group by score"

    data = cursor.execute(sql)  # 执行sql语句

    for i in data:
        score.append(i[0])
        num.append(i[1])
        # print(i)
    conn.close()  # 关闭数据库连接
    return render_template("score.html", score=score, num=num,data=qwe)


if __name__ == '__main__':
    app.run()
