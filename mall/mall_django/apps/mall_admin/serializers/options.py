# -*- coding:utf-8 -*-
# @Time : 2023/3/30 16:39
# @Author: fbz
# @File : options.py
from rest_framework import serializers
from apps.goods.models import SpecificationOption, SPUSpecification


class OptionsModelSerializer(serializers.ModelSerializer):
    spec = serializers.StringRelatedField()
    spec_id = serializers.IntegerField()

    class Meta:
        model = SpecificationOption
        fields = ['id', 'value', 'spec', 'spec_id']


class SPUSimpleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPUSpecification
        fields = ['id', 'name']
