# -*- coding:utf-8 -*-
# @Time : 2023/3/30 1:17
# @Author: fbz
# @File : order.py

from rest_framework import serializers
from apps.orders.models import OrderInfo, OrderGoods
from apps.goods.models import SKU


class SKUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = '__all__'


class OrderGoodsModelSerializer(serializers.ModelSerializer):
    """ 订单商品序列化器 """
    sku = SKUModelSerializer()

    class Meta:
        model = OrderGoods
        fields = ['sku', 'count', 'price']


class OrderInfoModelSerializer(serializers.ModelSerializer):
    """ 订单信息序列化器 """
    skus = OrderGoodsModelSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderStatusModelSerializer(serializers.ModelSerializer):
    """ 订单状态序列化器 """

    class Meta:
        model = OrderInfo
        fields = ['status']
