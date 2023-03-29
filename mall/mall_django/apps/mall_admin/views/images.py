# -*- coding:utf-8 -*-
# @Time : 2023/3/28 22:25
# @Author: fbz
# @File : images.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from apps.goods.models import SKUImage, SKU
from apps.mall_admin.serializers.images import SKUImageModelSerializer, ImageSKUModelSerializer
from apps.mall_admin.utils import PageNum


class ImageModelViewSet(ModelViewSet):
    queryset = SKUImage.objects.all().order_by('id')
    serializer_class = SKUImageModelSerializer
    pagination_class = PageNum


class ImageSKUAPIView(ListAPIView):
    queryset = SKU.objects.all()
    serializer_class = ImageSKUModelSerializer
