# -*- coding:utf-8 -*-
# @Time : 2022/9/16 0:12
# @Author: fbz
# @File : urls.py
from django.urls import path
from apps.goods.views import *

urlpatterns = [
    # 首頁
    path('index/', IndexView.as_view()),
    # 詳情頁
    path('detail/<sku_id>/', DetailView.as_view()),
    # 商品数据
    path('list/<category_id>/skus/', ListView.as_view()),
    # 获取热销商品数据
    path('hot/<category_id>/', HotView.as_view()),
    # 搜索商品
    path('search/', SKUSearchView()),  # 直接實例化就行，他沒有as_vieew()
]
