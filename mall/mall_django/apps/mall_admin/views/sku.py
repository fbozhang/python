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
            return SKU.objects.filter(name__contains=keyword).order_by('id')

        return SKU.objects.all().order_by('id')

    serializer_class = SKUModelSerializer
    pagination_class = PageNum


from apps.goods.models import GoodsCategory
from rest_framework.generics import ListAPIView
from apps.mall_admin.serializers.sku import GoodsCategoryModelSerializer


class GoodsCategoryAPIView(ListAPIView):
    """ 获取三级分类信息 """
    # subs=None 代表是三级标签，因为一级分类的 .subs.all() 是二级，同理二级的subs是三级，三级就没有subs
    queryset = GoodsCategory.objects.filter(subs=None)
    serializer_class = GoodsCategoryModelSerializer


from apps.goods.models import SPU
from apps.mall_admin.serializers.sku import SPUModelSerializer


class SPUListAPIView(ListAPIView):
    """ SPU数据 """
    queryset = SPU.objects.all()
    serializer_class = SPUModelSerializer
