# -*- coding:utf-8 -*-
# @Time : 2023/7/15 0:53
# @Author: fbz
# @File : routing.py
from django.urls import path
from app01.views import chat

websocket_urlpatterns = [
    path(r'ws/<group>/',chat.wsChat.as_asgi()),
]