# -*- coding:utf-8 -*-
# @Time : 2022/9/14 19:35
# @Author: fbz
# @File : urls.py
from django.urls import path
from apps.areas.views import *

urlpatterns = [
    # 省數據
    path('areas/', AreaView.as_view()),
    # 市區數據
    path('areas/<id>/', SubAreaView.as_view()),
]