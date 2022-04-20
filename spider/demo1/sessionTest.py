# -*- coding:utf-8 -*-
# @Time : 2022/4/17 17:33
# @Author: fbz
# @File : sessionTest.py

# 用session进行请求拿登录的cookie去请求到书架url
import requests

# 会话
session = requests.session()
data = {
    "loginName": "123456789",
    "password": "123654789"
}
# 登录
url = "https://passport.17k.com/ck/user/login"
session.post(url, data=data)
# print(resp.text)
# print(resp.cookies)     # 看cookie

# 拿书架上的书
resp = session.get('https://passport.17k.com/ck/author/shelf')
print(resp.json())
