# -*- coding:utf-8 -*-
# @Time : 2022/9/6 1:30
# @Author: fbz
# @File : urls.py
from django.urls import path
from apps.users.views import UsernmaeCountView

urlpatterns = [
    # 判断用户名是否重复
    path('usernames/<username>/count/', UsernmaeCountView.as_view()),
]