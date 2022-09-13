# -*- coding:utf-8 -*-
# @Time : 2022/9/13 17:16
# @Author: fbz
# @File : tasks.py

# 生产者（任务，函数）
# 1. 這個函數必須要讓celery的實例的task裝飾器 裝飾
# 2. 需要celery自動檢測指定包的任務
from django.core.mail import send_mail
from celery_tasks.main import app


@app.task
def celery_send_email(subject, message, from_email, recipient_list, html_message):
    send_mail(subject=subject,
              message=message,
              from_email=from_email,
              recipient_list=recipient_list,
              html_message=html_message)
