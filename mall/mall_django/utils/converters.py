# -*- coding:utf-8 -*-
# @Time : 2022/9/6 2:13
# @Author: fbz
# @File : converters.py

from django.urls import converters


# 验证用户名规则
class UsernameConverter:
    regex = '[a-zA-Z0-9_-]{5,20}'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return str(value)


# 验证手机号规则
class MobileConverter:
    regex = '1[345789]\d{9}'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return str(value)
