# -*- coding:utf-8 -*-
# @Time : 2023/3/30 1:16
# @Author: fbz
# @File : order.py

from rest_framework.viewsets import ModelViewSet

from apps.mall_admin.serializers.order import OrderInfoModelSerializer
from apps.mall_admin.utils import PageNum
from apps.orders.models import OrderInfo


class OrderInfoModelViewSet(ModelViewSet):
    """ 订单管理 """

    def get_queryset(self):
        """ 搜索功能呢 """
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return OrderInfo.objects.filter(order_id__contains=keyword).order_by('order_id')

        return OrderInfo.objects.all().order_by('order_id')

    serializer_class = OrderInfoModelSerializer

    pagination_class = PageNum
