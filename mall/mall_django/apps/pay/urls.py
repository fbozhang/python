# -*- coding:utf-8 -*-
# @Time : 2022/9/25 17:27
# @Author: fbz
# @File : urls.py
from django.urls import path
from apps.pay.views import *

urlpatterns = [
    # 跳转到支付宝支付
    path('payment/<order_id>/', PayUrlView.as_view()),
]