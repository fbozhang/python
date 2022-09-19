# -*- coding:utf-8 -*-
# @Time : 2022/9/19 18:25
# @Author: fbz
# @File : urls.py

from django.urls import path
from apps.goods.views import *

urlpatterns = [

]
# 使用 apscheduler，不需要在setting注冊app也不需要遷移數據庫，直接使用即可
# from apscheduler.scheduler import Scheduler
#
# sched = Scheduler()
#
# @sched.interval_schedule(seconds=2,misfire_grace_time=3600)
# def excute_task():
#     fun()  #执行任务函数
#
# sched.start()  #启动定时任务脚本


"""
使用 django_apscheduler:

1. pip install django_apscheduler
2. 在setting注冊app
3. 生成遷移文件 python manage.py migrate
    没有其他表结构不必运行  python manage.py makemigrations
    
    執行migrate生成 django_apscheduler_djangojob django_apscheduler_djangojobexecution兩張表
    django_apscheduler_djangojob 表保存注册的任务以及下次执行的时间
    django_apscheduler_djangojobexecution 保存每次任务执行的时间和结果和任务状态
    这里注意 missed 则是表示撞车的场景, 为避免这种场景需要在 周期的长度以及是否进行强制结束进行选择
"""
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


# 时间间隔1分鐘執行一次函數
@register_job(scheduler, "interval", minutes=1, id='index_html', replace_existing=True)  # replace_existing=解决第二次启动失败的问题
def index_html():
    from apps.contents.scheduler import generic_guiling_index_html
    generic_guiling_index_html()


scheduler.start()
