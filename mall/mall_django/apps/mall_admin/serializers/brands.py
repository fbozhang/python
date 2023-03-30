# -*- coding:utf-8 -*-
# @Time : 2023/3/30 17:17
# @Author: fbz
# @File : brands.py
import time

from rest_framework import serializers
from apps.goods.models import Brand
from utils.tooken import generate_token


class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo', 'first_letter']

    def validate(self, data):
        path = data.get('logo').name.split('.')
        generate_path = {
            'img_name': path[0],
            't': int(time.time())
        }
        data.get('logo').name = generate_token(generate_path) + f'.{path[1]}'

        return data
