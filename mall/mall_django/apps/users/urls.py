# -*- coding:utf-8 -*-
# @Time : 2022/9/6 1:30
# @Author: fbz
# @File : urls.py
from django.urls import path
from apps.users.views import *

urlpatterns = [
    # 判断用户名是否重复
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    # 判断手机号是否存在
    path('mobiles/<mobile:mobile>/count/', MobileCountView.as_view()),
    # 注冊
    path('register/', RsgisterView.as_view()),
    # 登錄
    path('login/', LoginView.as_view()),
]
