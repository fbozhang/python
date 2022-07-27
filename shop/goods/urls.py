# -*- coding:utf-8 -*-
# @Time : 2022/7/26 15:09
# @Author: fbz
# @File : urls.py

from django.urls import re_path
from goods import views

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view()),
    re_path(r'^category/(\d+)$', views.IndexView.as_view()),
    re_path(r'^category/(\d+)/page/(\d+)$', views.IndexView.as_view()),
]
