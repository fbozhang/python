# -*- coding:utf-8 -*-
# @Time : 2023/3/30 03:14
# @Author: fbz
# @File : spu.py
from apps.goods.models import SPU, Brand, GoodsCategory
from rest_framework import serializers
from django.db import transaction


class SPUModelSerializer(serializers.ModelSerializer):
    """ spu序列化器 """

    category1_id = serializers.IntegerField()
    category2_id = serializers.IntegerField()
    category3_id = serializers.IntegerField()
    brand_id = serializers.IntegerField()

    class Meta:
        model = SPU
        fields = '__all__'

        extra_kwargs = {
            'brand': {
                'read_only': True
            },
            'category1': {
                'read_only': True
            },
            'category2': {
                'read_only': True
            },
            'category3': {
                'read_only': True
            },
        }


class SPUBrandModelSerializer(serializers.ModelSerializer):
    """ 品牌信息列化器 """

    class Meta:
        model = Brand
        fields = ['id', 'name']


class SPUCategoriesModelSerializer(serializers.ModelSerializer):
    """ 获取分类信息 """

    class Meta:
        model = GoodsCategory
        fields = ['id', 'name']
