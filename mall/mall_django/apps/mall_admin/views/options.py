# -*- coding:utf-8 -*-
# @Time : 2023/3/30 16:39
# @Author: fbz
# @File : options.py

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from apps.goods.models import SpecificationOption, SPUSpecification
from apps.mall_admin.serializers.options import OptionsModelSerializer, SPUSimpleModelSerializer
from apps.mall_admin.utils import PageNum


class OptionsModelViewSet(ModelViewSet):
    queryset = SpecificationOption.objects.all().order_by('id')
    serializer_class = OptionsModelSerializer
    pagination_class = PageNum


class SPUSimpleListAPIView(ListAPIView):
    queryset = SPUSpecification.objects.all()
    serializer_class = SPUSimpleModelSerializer
