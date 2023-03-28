# -*- coding:utf-8 -*-
# @Time : 2023/3/28 18:13
# @Author: fbz
# @File : user.py

from rest_framework import serializers
from apps.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    """ 用户信息序列化器 """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile', 'password']
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
            }
        }

    def create(self, validated_data):
        """ 密码加密 """
        return User.objects.create_user(**validated_data)
