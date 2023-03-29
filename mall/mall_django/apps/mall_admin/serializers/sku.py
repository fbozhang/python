# -*- coding:utf-8 -*-
# @Time : 2023/3/29 17:47
# @Author: fbz
# @File : sku.py
from apps.goods.models import SKU, GoodsCategory, SPU
from rest_framework import serializers


class SKUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = '__all__'


class GoodsCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ['id', 'name']


class SPUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = ['id', 'name']
