# -*- coding:utf-8 -*-
# @Time : 2023/3/24 23:55
# @Author: fbz
# @File : serializers.py
from rest_framework import serializers


class AutherSerializers(serializers.Serializer):
    # 变量名与模型字段名一样
    # 类型与模型类型一样
    # read_only 只用于序列化使用，反序列化的时候 忽略该字段
    id = serializers.IntegerField(read_only=True)
    # 通过字段选项验证数据。例如：max_length=10, min_length=2
    author = serializers.CharField(max_length=10, min_length=2)
    # required 表明该字段在反序列化时必须输入，默认True
    email = serializers.CharField(required=False)
    # write_only 只用于反序列化使用，序列化的时候 忽略该字段
    direction = serializers.CharField(write_only=True)
    useNum = serializers.IntegerField(max_value=5)
    company_name = serializers.CharField()

    def validate_company_name(self, attrs):
        # 写额外的检测代码
        if len(attrs) < 3:
            raise serializers.ValidationError('单位名称不能小于3')

        return attrs


class AreaSerializers(serializers.Serializer):
    area = serializers.CharField()


class CountrySerializers(serializers.Serializer):
    country = serializers.CharField()

    # 对外键的学习
    # area = serializers.IntegerField()
    # TypeError: int() argument must be a string, a bytes-like object or a number, not 'Area'

    # 方法1
    # 如果定义的序列化起外键字段类型为 IntegerField
    # 那么定义的序列化器字段名 必须和数据库中的外键字段名一致
    # area_id = serializers.IntegerField()

    # 方法2
    # 如果想要外键数据的key就是模型字段名字，那么PrimaryKeyRelatedField 就可以获取到关联的模型id
    # queryset 再验证数据的时候告诉系统在哪匹配外键数据
    # AssertionError: Relational field must provide a `queryset` argument, override `get_queryset`, or set read_only=`True`.
    # from app01.models import Area
    # area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    # 或者 read_only=True,意思是不验证了
    # area = serializers.PrimaryKeyRelatedField(read_only=True)

    # 方法3
    # 如果想要获取外键字段关联的 字符串信息，可以使用 StringRelatedField
    # 实际上获取的是模型中 def __str__(self): 的返回值
    # area = serializers.StringRelatedField()

    # 方法4
    area = AreaSerializers()

    # 方法5 在下面的 AreaCountrySerializers


class AreaCountrySerializers(serializers.Serializer):
    area = serializers.CharField()
    country_set = CountrySerializers(many=True)
