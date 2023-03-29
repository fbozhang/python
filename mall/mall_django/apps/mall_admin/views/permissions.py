# -*- coding:utf-8 -*-
# @Time : 2023/3/29 21:11
# @Author: fbz
# @File : permissions.py

from apps.mall_admin.utils import PageNum
from apps.mall_admin.serializers.permissions import PermissionModelSerializer
from rest_framework.viewsets import ModelViewSet

# 权限
from django.contrib.auth.models import Permission


class PermissionModelViewSet(ModelViewSet):
    """ 权限 """
    queryset = Permission.objects.all()

    serializer_class = PermissionModelSerializer

    pagination_class = PageNum


from rest_framework.generics import ListAPIView
from django.contrib.auth.models import ContentType
from apps.mall_admin.serializers.permissions import ContentTypeModelSerializer


class ConentTypeListAPIView(ListAPIView):
    """ 获取权限类型(哪个模型) """

    queryset = ContentType.objects.all().order_by('id')

    serializer_class = ContentTypeModelSerializer


# 组
from django.contrib.auth.models import Group
from apps.mall_admin.serializers.permissions import GroupModelSerializer


class GroupModelViewSet(ModelViewSet):
    """ 组管理 """
    queryset = Group.objects.all().order_by('id')

    serializer_class = GroupModelSerializer

    pagination_class = PageNum


class GroupPermissionListAPIView(ListAPIView):
    """ 组管理-权限列表展示 """
    queryset = Permission.objects.all()

    serializer_class = PermissionModelSerializer


# 用户
from apps.users.models import User
from apps.mall_admin.serializers.permissions import AdminUserModelSerializer


class AdminUserModelViewSet(ModelViewSet):
    """ 管理员管理 """
    queryset = User.objects.filter(is_staff=True)

    serializer_class = AdminUserModelSerializer

    pagination_class = PageNum
