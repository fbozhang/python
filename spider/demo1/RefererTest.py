# -*- coding:utf-8 -*-
# @Time : 2022/4/17 21:26
# @Author: fbz
# @File : RefererTest.py

import requests
from lxml import etree

url = "https://pearvideo.com/video_1758850"
conId = url.split("_")[1]  # split("xxx")[1],以xxx分割:[0]是xxx前面的，[1]是xxx后面的
# print(conId)

videoStatusUrl = f"https://pearvideo.com/videoStatus.jsp?contId={conId}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
    , "Referer": url    # 防盗链:溯源,当前本次请求的上一级是谁
}
resp = requests.get(videoStatusUrl, headers=headers)
# print(resp.json())
dic = resp.json()

systemTime = dic["systemTime"]
srcUrl = dic["videoInfo"]["videos"]["srcUrl"]
srcUrl = srcUrl.replace(systemTime,f"cont-{conId}")     # 把srcUrl中systemTime的部分替换成cont-{conId}
# import re
# srcUrl = re.sub(systemTime, f"cont-{conId}", srcUrl)
print(srcUrl)

# with open("test.mp4",mode="wb") as f:
#     f.write(requests.get(srcUrl).content)
