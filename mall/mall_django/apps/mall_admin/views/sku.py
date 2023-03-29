# -*- coding:utf-8 -*-
# @Time : 2023/3/29 17:47
# @Author: fbz
# @File : sku.py
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKU
from apps.mall_admin.serializers.sku import SKUModelSerializer
from apps.mall_admin.utils import PageNum


class SKUModelViewSet(ModelViewSet):
    # queryset = SKU.objects.all()
    def get_queryset(self):
        """ 搜索功能呢 """
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return SKU.objects.filter(name__contains=keyword)

        return SKU.objects.all()

    serializer_class = SKUModelSerializer
    pagination_class = PageNum
