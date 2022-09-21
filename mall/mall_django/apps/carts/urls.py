# -*- coding:utf-8 -*-
# @Time : 2022/9/22 2:40
# @Author: fbz
# @File : urls.py

from django.urls import path
from apps.carts.views import *

urlpatterns = [
    path('carts/', CartVist.as_view()),
]
