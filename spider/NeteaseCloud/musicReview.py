# -*- coding:utf-8 -*-
# @Time : 2022/4/18 0:31
# @Author: fbz
# @File : musicReview.py

# 1. 找到未加密的参数
# 2. 想办法把参数进行加密(必须参考网易的逻辑)， params => encText encSecKey => encSecKey(window.asrsea(参数,xxx,xxx,xxx))
# 3. 请求网易，拿到评论信息

import json
import requests
# crypto在python上面的名字是pycrypto, 安装pycrypto报错，就安装pycryptodome, 它是pycrypto的延伸版本, 用法和pycrypto是一模一样的
from Crypto.Cipher import AES
from base64 import b64encode

# https://music.163.com/#/song?id=167827
url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="

e = "010001"
f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7 "
g = "0CoJUm6Qyw8W8jud"
i = "u9fsFAj7Rcoeg2Iq"


def get_encSecKey():
    return "185c72b55d2a2368927dbd20684596c9bf616dd9adf1ca56ff8c36d585c020844160358a3ba0a870306a2cd0383c1cf344e430ee97715c7555596fc562462d24d93815203157afdae2e35ec6abf1fb8009a42e5890ff8378416d75f5c9b25f94d74583f07fa28580e95f668c6c2cbf4e9a8394afd09a3b4feea56930358eeafb"


def get_params(data):  # 默认收到的是字符串
    first = enc_params(data, g)
    second = enc_params(first, i)
    return second  # 返回params


# eg: 123456789'char(5)'*5 , 123456789abcdef'char(16)'*16, 即离16缺x个就补x个char(x) 刚好16也要补16个char(16)
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


def enc_params(data, key):  # 加密过程
    iv = "0102030405060708"
    data = to_16(data)
    aes = AES.new(key=key.encode("utf-8"), IV=iv.encode("utf-8"), mode=AES.MODE_CBC)  # 创建加密器
    bs = aes.encrypt(data.encode("utf-8"))  # 加密, 加密的内容的长度必须是16的倍数
    # eg: 123456789'char(5)'*5 , 123456789abcdef'char(16)'*16, 即离16缺x个就补x个char(x) 刚好16也要补16个char(16)
    return str(b64encode(bs), "utf-8")  # 转换成字符串返回


# 处理加密过程
'''
    function a(a = 16) {    # 随机的16位字符串
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)  # 循环16次
            e = Math.random() * b.length,   # 随机数
            e = Math.floor(e),  # 取整
            c += b.charAt(e);   # 取字符串中的xxx位置
        return c
    }
    function b(a, b) {  # a是要加密的内容
        var c = CryptoJS.enc.Utf8.parse(b)  # 由下推得b是密钥
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)  # e是数据
          , f = CryptoJS.AES.encrypt(e, c, {    # AES加密, c是密钥
            iv: d,  # AES加密的偏移量
            mode: CryptoJS.mode.CBC # 模式: cbc
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {    d: 数据(data), e: 010001, f: (f), g: (g)
        var h = {}  # 空对象
          , i = a(16);  # 随机的16位字符串， 由c需求将i设置成定值
        h.encText = b(d, g),    # 推得g密钥
        h.encText = b(h.encText, i),    # 得到params, 推得i也是密钥
        h.encSecKey = c(i, e, f),   # 得到encSecKey, e和f是定值, 如果把i固定则c一定固定
        return h
    }
'''

def svaeJson():
    music_url = input("请输入歌曲连接:")
    id = "R_SO_4_" + music_url.split('=')[1]
    pageNum = int(input("请输入第几页评论:"))
    pageNum = str((pageNum-1) * 20)
    # POST
    data = {
        "csrf_token": "",
        "cursor": "-1",
        "offset": pageNum,  # offset =（页数-1）*20
        "orderType": "1",
        "pageNo": "1",
        "pageSize": "20",
        "rid": id,  # 歌曲id
        "threadId": id
    }

    resp = requests.post(url, data={
        "params": get_params(json.dumps(data)),
        "encSecKey": get_encSecKey()
    })
    dic = resp.json()
    with open("temp.json", mode="w", encoding="utf-8") as file:
        json.dump(dic, file)  # 把列表numbers内容写入到"list.json"文件中

with open("temp.json") as file:
    dic = json.load(file)  # 读取文件
# print(dic)

comments = dic['data']['comments']
hotComments = dic['data']['hotComments']


def comment(comments):
    comment_list = []
    beReplied_dic = {"beReplied": ""}
    for comment in comments:
        comment_dic = get_comment(comment)
        if comment['beReplied'] is not None:
            beReplied_dic["beReplied"] = get_beReplied(comment['beReplied'])
            comment_dic.update(beReplied_dic)
        comment_list.append(comment_dic)

    return comment_list


def get_comment(comment):
    nickname = comment['user']['nickname']
    content = comment['content']
    comment_dic = {nickname: content}

    return comment_dic


def get_beReplied(beReplieds):
    beReplied_list = []
    for beReplied in beReplieds:
        beReplied_list.append(get_comment(beReplied))

    return beReplied_list


def printList(comments_list):
    for comments in comments_list:
        for key, values in comments.items():
            if key == "beReplied":
                for beReplied in values:
                    for i, j in beReplied.items():
                        print(f"{i}: {j}")
            else:
                print(f"{key}: {values}")
        print()


if __name__ == '__main__':
    # svaeJson()
    comments_list = comment(comments)
    hotComments_list = comment(hotComments)
    printList(comments_list)
    print("over!!")
