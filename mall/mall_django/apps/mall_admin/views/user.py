# -*- coding:utf-8 -*-
# @Time : 2023/3/28 18:08
# @Author: fbz
# @File : user.py
from rest_framework.generics import ListAPIView
from apps.users.models import User
from apps.mall_admin.serializers.user import UserModelSerializer


class UserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
