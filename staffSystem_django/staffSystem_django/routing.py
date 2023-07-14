# -*- coding:utf-8 -*-
# @Time : 2023/7/15 0:53
# @Author: fbz
# @File : routing.py
from django.urls import re_path
from app01.views import chat

websocket_urlpatterns = [
    re_path(r'ws/(?P<group>\w+/$)',chat.wsChat.as_asgi()),
]