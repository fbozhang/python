# -*- coding:utf-8 -*-
# @Time : 2023/3/28 22:29
# @Author: fbz
# @File : images.py
from rest_framework import serializers
from apps.goods.models import SKUImage


class SKUImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKUImage
        fields = '__all__'
