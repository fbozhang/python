# -*- coding:utf-8 -*-
# @Time : 2023/3/28 15:58
# @Author: fbz
# @File : home.py

from apps.users.models import User
from datetime import date
from rest_framework.response import Response
from rest_framework.views import APIView


class DailyActiveAPIView(APIView):
    """ 日活用户统计 """

    def get(self, request):
        today = date.today()
        # 获得今日登录人数
        # last_login__gte 大于等于
        count = User.objects.filter(last_login__gte=today).count()

        return Response({'count': count})


class DailyOrderCountAPIView(APIView):
    """ 日下单用户统计 """

    def get(self, request):
        # 获取当前日期
        today = date.today()
        # 获取当日下单用户数量  orders__create_time 订单创建时间
        count = User.objects.filter(orderinfo__create_time__gte=today).count()
        return Response({"count": count})


class UserCountAPIView(APIView):
    """ 用户总量统计 """

    def get(self, request):
        count = User.objects.filter(is_staff=0).count()
        return Response({"count": count})
