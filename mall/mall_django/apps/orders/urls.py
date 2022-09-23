# -*- coding:utf-8 -*-
# @Time : 2022/9/23 21:42
# @Author: fbz
# @File : urls.py
from django.urls import path
from apps.orders.views import *

urlpatterns = [
    # 提交訂單頁面
    path('orders/settlement/', OrderSettlementView.as_view()),
    # 提交訂單
    path('orders/commit/', OrderCommitView.as_view()),
]
