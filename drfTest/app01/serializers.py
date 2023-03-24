# -*- coding:utf-8 -*-
# @Time : 2023/3/24 23:55
# @Author: fbz
# @File : serializers.py
from rest_framework import serializers


class AutherSerializers(serializers.Serializer):
    # 变量名与模型字段名一样
    # 类型与模型类型一样
    id = serializers.IntegerField()
    author = serializers.CharField()
    email = serializers.CharField()
    direction = serializers.CharField()
    useNum = serializers.IntegerField()
    company_name = serializers.CharField()
