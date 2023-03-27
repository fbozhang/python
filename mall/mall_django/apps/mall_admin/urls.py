# -*- coding:utf-8 -*-
# @Time : 2023/3/27 18:29
# @Author: fbz
# @File : urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh, token_verify

urlpatterns = [
    # path('authorizations/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 或者下面这样写，点进去看源码发现一样
    path('authorizations/', token_obtain_pair, name='token_obtain_pair'),
    path('refresh/', token_refresh, name='token_refresh'),
    path('verify/', token_verify, name='token_verify'),
]
