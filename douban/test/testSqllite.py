# -*- coding:utf-8 -*-
# @Time : 2022/3/26 17:49
# @Author: fbz
# @File : testSqllite.py

import sqlite3

# 创建数据库

'''conn = sqlite3.connect("test.db")  # 打开或创建数据库文件
print("成功打开数据库")'''


# 创建数据表

# conn = sqlite3.connect("test.db")  # 打开或创建数据库文件
# print("成功打开数据库")
# c = conn.cursor()  # 获取游标
#
# sql = '''
#     create table company
#         (id int primary key not null,
#         name text not null,
#         age int not null,
#         address char (50),
#         salary real);
#
# '''
#
# c.execute(sql)  # 执行sql语句
# conn.commit()  # 提交数据库操作
# conn.close()  # 关闭数据库连接
#
# print("成功建表")

# 插入数据

# conn = sqlite3.connect("test.db")  # 打开或创建数据库文件
# print("成功打开数据库")
# c = conn.cursor()  # 获取游标
#
# sql = '''
#     insert into company (id,name,age,address,salary)
#         values (2,"老王",18,"深圳",123);
#
# '''
#
# c.execute(sql)  # 执行sql语句
# conn.commit()  # 提交数据库操作
# conn.close()  # 关闭数据库连接
#
# print("插入数据完毕")

# 查询数据

conn = sqlite3.connect("test.db")  # 打开或创建数据库文件
print("成功打开数据库")
c = conn.cursor()  # 获取游标

sql = "select * from company"

cursor = c.execute(sql)  # 执行sql语句

for i in cursor:
    for j in i:
        print(j,end=' ')
    print()
conn.close()  # 关闭数据库连接

print("查询完毕")