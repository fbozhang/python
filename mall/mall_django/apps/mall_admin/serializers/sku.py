# -*- coding:utf-8 -*-
# @Time : 2023/3/29 17:47
# @Author: fbz
# @File : sku.py
from apps.goods.models import SKU, GoodsCategory, SPU, SKUSpecification
from apps.goods.models import SPUSpecification, SpecificationOption
from rest_framework import serializers


class SKUSpecificationModelSerializer(serializers.ModelSerializer):
    """ sku规格和规格选项序列化器"""
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    class Meta:
        model = SKUSpecification
        fields = ['spec_id', 'option_id']


class SKUModelSerializer(serializers.ModelSerializer):
    """ sku序列化器 """
    spu_id = serializers.IntegerField()
    category_id = serializers.IntegerField()

    spu = serializers.StringRelatedField(required=False)
    category = serializers.StringRelatedField(required=False)

    specs = SKUSpecificationModelSerializer(many=True)

    class Meta:
        model = SKU
        fields = '__all__'

    def create(self, validated_data):
        # 吧规格和规格选项单独获取出来
        specs = validated_data.pop('specs')
        # 先保存sku数据
        sku = SKU.objects.create(**validated_data)
        # 对规格和规格选项进行遍历保存
        for spec in specs:
            # spec = {'spec_id': '2', 'option_id': 7}
            SKUSpecification.objects.create(sku=sku, **spec)

        return sku


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
