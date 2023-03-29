# -*- coding:utf-8 -*-
# @Time : 2023/3/29 21:11
# @Author: fbz
# @File : permissions.py

# 组
from django.contrib.auth.models import Group
# 权限
from django.contrib.auth.models import Permission
# 用户
from apps.users.models import User
from apps.mall_admin.utils import PageNum

from apps.mall_admin.serializers.permissions import PermissionModelSerializer
from rest_framework.viewsets import ModelViewSet


class PermissionModelViewSet(ModelViewSet):
    queryset = Permission.objects.all()

    serializer_class = PermissionModelSerializer

    pagination_class = PageNum
