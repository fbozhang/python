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


from rest_framework.generics import ListAPIView
from apps.goods.models import Brand
from apps.mall_admin.serializers.spu import SPUBrandModelSerializer


class SPUBrandListAPIView(ListAPIView):
    """ 获取品牌信息 """

    queryset = Brand.objects.all()

    serializer_class = SPUBrandModelSerializer


from apps.goods.models import GoodsCategory
from apps.mall_admin.serializers.spu import SPUCategoriesModelSerializer


class SPUCategoriesListAPIView(ListAPIView):
    """ 获取一级分类信息 """

    queryset = GoodsCategory.objects.all()

    serializer_class = SPUCategoriesModelSerializer


class SPUSonCategoriesListAPIView(ListAPIView):
    """ 获取二级和三级分类 """

    queryset = GoodsCategory.objects.all()

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_field)

        return self.queryset.filter(parent_id=pk)

    serializer_class = SPUCategoriesModelSerializer
