# -*- coding:utf-8 -*-
# @Time : 2022/9/16 0:12
# @Author: fbz
# @File : urls.py
from django.urls import path
from apps.goods.views import *

urlpatterns = [
    # 判断用户名是否重复
    path('index/', IndexView.as_view()),
]