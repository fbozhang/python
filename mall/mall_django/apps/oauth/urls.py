# -*- coding:utf-8 -*-
# @Time : 2022/9/11 0:52
# @Author: fbz
# @File : urls.py
from django.urls import path
from apps.oauth.views import *

urlpatterns = [
    # 判断用户名是否重复
    path('qq/authorization/', QQLoginURLView.as_view()),
    # QQ登錄
    path('oauth_callback/', OauthQQView.as_view()),
]