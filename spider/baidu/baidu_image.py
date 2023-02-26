# -*- coding:utf-8 -*-
# @Time : 2023/2/26 15:30
# @Author: fbz
# @File : baidu_image.py
import random
import time

import requests


def downloadImg(word, i):
    global num
    url = 'https://image.baidu.com/search/acjson'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    params = {
        'tn': 'resultjson_com',
        'word': word,
        'pn': 30 * i,
        '1677397526392': '',
        'logid': '',
        'ipn': '',
        'fp': '',
        'ct': ''
    }

    res = requests.get(url, headers=headers, params=params).json()
    data = res.get('data')

    for i in range(30):
        thumbURL = data[i].get('thumbURL')
        image = requests.get(thumbURL, headers=headers).content
        with open("img/dog/dog.{num}.jpg".format(num=num), mode="wb") as f:
            f.write(image)  # 图片内容写入文件
            num += 1
        print('dog.{num}.jpg  下載完成'.format(num=num))


if __name__ == '__main__':
    num = 1
    word = '狗'
    for i in range(30):
        downloadImg(word=word, i=i)
        time.sleep(random.randint(2, 4))
