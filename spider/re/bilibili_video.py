# -*- coding:utf-8 -*-
# @Time : 2022/8/31 23:15
# @Author: fbz
# @File : bilibili_video.py
import ast
import time
from pprint import pprint

import requests
import re
import json

url = 'https://www.bilibili.com/video/BV13d4y1o7J3?spm_id_from=333.851.b_7265636f6d6d656e64.4&vd_source=837ec8470c28cc7797d92b5dd001820a'

headers = {
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
    ,"referer": "https://www.bilibili.com/"
}
resp = requests.get(url, headers)
# print(resp.text)
obj1 = re.compile(r'window.__playinfo__=(?P<script>.*?)</script>')
time.sleep(2)
result1 = obj1.finditer(resp.text)
for i in result1:
    script = i.group("script")
    # print(script)
    dic1 = json.loads(script)
    # pprint(dic1)
    # print(dic1, type(dic1))
    url = dic1['data']['dash']
    # print(url)
    video_url = url['video'][0]['backupUrl'][0]
    audio_url = url['audio'][0]['backupUrl'][0]
    header = {
        ":authority": "xy36x248x55x2xy.mcdn.bilivideo.cn:4483"
        ,":method": "GET"
        ,':path': '/upgcxcode/85/96/803069685/803069685_nb3-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1661974396&gen=playurlv2&os=mcdn&oi=3524612085&trid=0000427b2732ef3a47e8969544e8b50e921eu&mid=94807515&platform=pc&upsig=126af79702e2e12c6c673f008444bc17&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&mcdnid=11000057&bvc=vod&nettype=0&orderid=0,3&agrr=1&bw=16218&logo=A0000400'
        ,':scheme': 'https'
        ,'accept-encoding': 'identity'
        ,'origin':' https://www.bilibili.com'
    }
    headers.update(header)
    # headers["referer"] = "https://www.bilibili.com/video/BV13d4y1o7J3?spm_id_from=333.851.b_7265636f6d6d656e64.4&vd_source=837ec8470c28cc7797d92b5dd001820a"
    video_resp = requests.get(video_url, headers)
    print(video_resp.text)
    # with open("video.mp4", mode="wb") as f:
    #     f.write(video_resp.content)  # 图片内容写入文件
    # break

# str1 = '{"code":0,"message":"0","ttl":1,"data":{"from":"local","result":"suee","message":"","quality":32}}'
# dic1 = ast.literal_eval(str1)
# dic1 = eval(str1)
# dic1 = json.loads(str1)
# print(type(str1),type(dic1),dic1)

