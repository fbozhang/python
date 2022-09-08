# -*- coding:utf-8 -*-
# @Time : 2022/9/9 1:57
# @Author: fbz
# @File : tasks.py

# 生产者（任务，函数）
# 1. 這個函數必須要讓celery的實例的task裝飾器 裝飾
# 2. 需要celery自動檢測指定包的任務
from libs.yuntongxun.sms import CCP
from celery_tasks.main import app

@app.task
def celery_send_sms_code(mobile, code):
    CCP().send_template_sms(mobile, [code, 5], 1)  # 給mobile手機號發驗證碼為code時效5分鐘
