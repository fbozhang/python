# -*- coding:utf-8 -*-
# @Time : 2023/3/29 21:11
# @Author: fbz
# @File : permissions.py
from rest_framework import serializers
from django.contrib.auth.models import Permission
from django.contrib.auth.models import ContentType
from django.contrib.auth.models import Group


class PermissionModelSerializer(serializers.ModelSerializer):
    """ 权限序列化器 """

    class Meta:
        model = Permission
        fields = '__all__'


class ContentTypeModelSerializer(serializers.ModelSerializer):
    """ 权限类型序列化器 """

    class Meta:
        model = ContentType
        fields = ['id', 'name']


class GroupModelSerializer(serializers.ModelSerializer):
    """ 组管理序列化器 """

    class Meta:
        model = Group
        fields = '__all__'


from apps.users.models import User


class AdminUserModelSerializer(serializers.ModelSerializer):
    """ 普通管理员序列化器 """

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email']
