# -*- coding:utf-8 -*-
# @Time : 2022/9/6 2:13
# @Author: fbz
# @File : converters.py

from django.urls import converters

class UsernameConverter:
    regex = '[a-zA-Z0-9_-]{5,20}'

    def to_python(self, value):
        return value
