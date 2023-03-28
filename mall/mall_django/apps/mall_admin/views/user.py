# -*- coding:utf-8 -*-
# @Time : 2023/3/28 18:08
# @Author: fbz
# @File : user.py
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict

from apps.users.models import User
from apps.mall_admin.serializers.user import UserModelSerializer


class PageNum(PageNumberPagination):
    """ 分页 """
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


class UserAPIView(ListCreateAPIView):
    """ 用户管理视图 """
    # queryset = User.objects.all() # 重写属性只能设置一个查询结果集
    serializer_class = UserModelSerializer
    pagination_class = PageNum

    def get_queryset(self):
        # 重写 get_queryset 方法，根据不同业务逻辑获取不同查询结果集
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return User.objects.filter(username__contains=keyword)

        return User.objects.all()
