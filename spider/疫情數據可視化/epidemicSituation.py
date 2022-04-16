# -*- coding:utf-8 -*-
# @Time : 2022/4/11 20:03
# @Author: fbz
# @File : epidemicSituation.py
import csv
import re

import requests
import json
import re

with open('data.csv', mode='a', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['area', 'curConfirm', 'confirmedRelative', 'confirmed', 'crued', 'died'])

url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
}

response = requests.get(url=url, headers=headers)
data_html = response.text
response.close()

json_str = re.findall('"component":\[(.*)\}]', data_html)[0] + '}'
# print(json_str)   # 得到一個json,打印去json.cn轉譯
json_dict = json.loads(json_str)  # 把json字符串轉爲字典
caseList = json_dict['caseList']

for case in caseList:
    area = case['area']  # 省份
    curConfirm = case['curConfirm']  # 確診人數
    confirmedRelative = case['confirmedRelative']  # 新增人數
    confirmed = case['confirmed']  # 纍計確診
    crued = case['crued']  # 治愈人数
    died = case['died']  # 死亡人数
    print(area, curConfirm, confirmedRelative, confirmed, crued, died)
    with open('data.csv', mode='a', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([area, curConfirm, confirmedRelative, confirmed, crued, died])