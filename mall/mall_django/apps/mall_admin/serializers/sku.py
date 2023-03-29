# -*- coding:utf-8 -*-
# @Time : 2023/3/29 17:47
# @Author: fbz
# @File : sku.py
from apps.goods.models import SKU, GoodsCategory, SPU
from apps.goods.models import SPUSpecification, SpecificationOption
from rest_framework import serializers


class SKUModelSerializer(serializers.ModelSerializer):
    spu_id = serializers.IntegerField()
    category_id = serializers.IntegerField()

    spu = serializers.StringRelatedField(required=False)
    category = serializers.StringRelatedField(required=False)

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


class OptionModelSerializer(serializers.ModelSerializer):
    """ SPU规格选项 序列化器"""

    class Meta:
        model = SpecificationOption
        fields = ['id', 'value']


class SpecsModelSerializer(serializers.ModelSerializer):
    """ SPU规格 序列化器"""
    options = OptionModelSerializer(many=True)

    class Meta:
        model = SPUSpecification
        fields = ['id', 'name', 'options']
