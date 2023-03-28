# -*- coding:utf-8 -*-
# @Time : 2023/3/28 22:25
# @Author: fbz
# @File : images.py
from rest_framework.viewsets import ModelViewSet

from apps.goods.models import SKUImage
from apps.mall_admin.serializers.images import SKUImageModelSerializer
from apps.mall_admin.utils import PageNum


class ImageModelViewSet(ModelViewSet):
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageModelSerializer
    pagination_class = PageNum
