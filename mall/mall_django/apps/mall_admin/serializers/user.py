# -*- coding:utf-8 -*-
# @Time : 2023/3/28 18:13
# @Author: fbz
# @File : user.py

from rest_framework import serializers
from apps.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile']
