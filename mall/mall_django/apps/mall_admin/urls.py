# -*- coding:utf-8 -*-
# @Time : 2023/3/27 18:29
# @Author: fbz
# @File : urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh, token_verify
from apps.mall_admin.views import home

urlpatterns = [
    # path('authorizations/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 或者下面这样写，点进去看源码发现一样
    path('authorizations/', token_obtain_pair, name='token_obtain_pair'),
    path('refresh/', token_refresh, name='token_refresh'),
    path('verify/', token_verify, name='token_verify'),

    # 日活统计
    path('statistical/day_active/', home.DailyActiveAPIView.as_view()),
    # 日下单用户统计
    path('statistical/day_orders/', home.DailyOrderCountAPIView.as_view()),
    # 用户总量统计
    path('statistical/total_count/', home.UserCountAPIView.as_view()),
    # 日增用户统计
    path('statistical/day_increment/', home.DailyIncreaseAPIView.as_view()),
]
