# -*- coding:utf-8 -*-
# @Time : 2023/3/28 18:08
# @Author: fbz
# @File : user.py
from rest_framework.generics import ListCreateAPIView

from apps.mall_admin.utils import PageNum
from apps.users.models import User
from apps.mall_admin.serializers.user import UserModelSerializer


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
