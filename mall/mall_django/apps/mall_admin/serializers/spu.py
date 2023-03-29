# -*- coding:utf-8 -*-
# @Time : 2023/3/30 03:14
# @Author: fbz
# @File : spu.py
from apps.goods.models import SPU
from rest_framework import serializers
from django.db import transaction


class SPUModelSerializer(serializers.ModelSerializer):
    """ spu序列化器 """

    class Meta:
        model = SPU
        fields = '__all__'
