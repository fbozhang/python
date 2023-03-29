# -*- coding:utf-8 -*-
# @Time : 2023/3/30 03:14
# @Author: fbz
# @File : spu.py
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SPU
from apps.mall_admin.serializers.spu import SPUModelSerializer
from apps.mall_admin.utils import PageNum


class SPUModelViewSet(ModelViewSet):
    def get_queryset(self):
        """ 搜索功能 """
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return SPU.objects.filter(name__contains=keyword).order_by('id')

        return SPU.objects.all().order_by('id')

    serializer_class = SPUModelSerializer
    pagination_class = PageNum

