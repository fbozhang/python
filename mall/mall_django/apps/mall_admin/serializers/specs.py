# -*- coding:utf-8 -*-
# @Time : 2023/3/30 15:53
# @Author: fbz
# @File : specs.py
from rest_framework import serializers

from apps.goods.models import SPUSpecification


class SpecsModelSerializer(serializers.ModelSerializer):
    """ SPU规格 序列化器"""

    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()

    class Meta:
        model = SPUSpecification
        fields = ['id', 'name', 'spu', 'spu_id']
