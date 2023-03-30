# -*- coding:utf-8 -*-
# @Time : 2023/3/30 15:53
# @Author: fbz
# @File : specs.py


from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SPUSpecification
from apps.mall_admin.serializers.specs import SpecsModelSerializer
from apps.mall_admin.utils import PageNum


class SpecsModelViewSet(ModelViewSet):
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecsModelSerializer
    pagination_class = PageNum
