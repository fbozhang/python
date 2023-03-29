# -*- coding:utf-8 -*-
# @Time : 2023/3/28 22:29
# @Author: fbz
# @File : images.py
import time

from rest_framework import serializers
from apps.goods.models import SKU, SKUImage
from utils.tooken import generate_token


class SKUImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKUImage
        fields = '__all__'

    def validate(self, data):
        path = data.get('image').name.split('.')
        generate_path = {
            'img_name': path[0],
            't': int(time.time())
        }
        data.get('image').name = generate_token(generate_path) + f'.{path[1]}'

        return data


class ImageSKUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ['id', 'name']
