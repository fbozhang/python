# -*- coding:utf-8 -*-
# @Time : 2023/3/30 17:17
# @Author: fbz
# @File : brands.py
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.goods.models import Brand
from apps.mall_admin.serializers.brands import BrandModelSerializer
from apps.mall_admin.utils import PageNum


class BrandModelViewSet(ModelViewSet):
    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandModelSerializer
    pagination_class = PageNum

    def list(self, request, *args, **kwargs):
        counts = self.get_queryset().count()
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'counts': counts, 'lists': serializer.data})
