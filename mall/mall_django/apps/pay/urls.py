# -*- coding:utf-8 -*-
# @Time : 2022/9/25 17:27
# @Author: fbz
# @File : urls.py
from django.urls import path
from apps.pay.views import *

urlpatterns = [
    # 保存支付寶的交易信息
    # 這個路由放上面，不然被路由 payment/<order_id>/ 截獲，出現Method Not Allowed
    path('payment/status/', PaymentStatusView.as_view()),
    # 跳转到支付宝支付
    path('payment/<order_id>/', PayUrlView.as_view()),
]