# -*- coding:utf-8 -*-
# @Time : 2023/3/28 18:08
# @Author: fbz
# @File : user.py
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict

from apps.users.models import User
from apps.mall_admin.serializers.user import UserModelSerializer


class PageNum(PageNumberPagination):
    # 开启分页，设置默认每页多少条记录
    page_size = 5
    # 设置每页多少条记录的key
    page_size_query_param = 'pagesize'
    # 最大一页多少条记录
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),  # 用户总量
            ('lists', data),  # 用户信息结果列表
            ('page', self.page.number),  # 页码
            ('pages', self.page.paginator.num_pages),  # 总页数
            ('pagesize', self.page.paginator.per_page)  # 页容量
        ]))


class UserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    pagination_class = PageNum
