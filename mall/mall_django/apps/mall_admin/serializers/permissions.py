# -*- coding:utf-8 -*-
# @Time : 2023/3/29 21:11
# @Author: fbz
# @File : permissions.py
from rest_framework import serializers
from django.contrib.auth.models import Permission


class PermissionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
