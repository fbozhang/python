# -*- coding:utf-8 -*-
# @Time : 2022/9/23 21:42
# @Author: fbz
# @File : urls.py
from django.urls import path
from apps.orders.views import *

urlpatterns = [
    # 首頁，渲染模板
    path('orders/settlement/', OrderSettlementView.as_view()),
]
