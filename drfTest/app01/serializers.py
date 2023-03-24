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


class AreaSerializers(serializers.Serializer):
    area = serializers.CharField()


from app01.models import Area


class CountrySerializers(serializers.Serializer):
    country = serializers.CharField()

    # 对外键的学习
    # area = serializers.IntegerField()
    # TypeError: int() argument must be a string, a bytes-like object or a number, not 'Area'

    # 方法1
    # area_id = serializers.IntegerField()

    # 方法2
    # AssertionError: Relational field must provide a `queryset` argument, override `get_queryset`, or set read_only=`True`.
    area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    # 或者 read_only=True,意思是不验证了
    # area = serializers.PrimaryKeyRelatedField(read_only=True)
