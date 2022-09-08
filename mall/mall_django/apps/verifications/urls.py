# -*- coding:utf-8 -*-
# @Time : 2022/9/7 20:46
# @Author: fbz
# @File : urls.py

from django.urls import path
from apps.verifications.views import ImageCodeView, SmsCodeView

urlpatterns = [
    path('image_codes/<uuid>/', ImageCodeView.as_view()),
    path('sms_codes/<mobile:mobile>/', SmsCodeView.as_view()),
]
