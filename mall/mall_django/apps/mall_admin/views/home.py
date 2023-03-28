# -*- coding:utf-8 -*-
# @Time : 2023/3/28 15:58
# @Author: fbz
# @File : home.py

from apps.users.models import User
from datetime import date, timedelta
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


class DailyIncreaseAPIView(APIView):
    """ 日增用户统计 """

    def get(self, request):
        # 获取当前日期
        today = date.today()
        # 账号创建时间是今天，并且是普通用户
        count = User.objects.filter(date_joined__gte=today, is_staff=0).count()
        return Response({"count": count})


class MonthIncreaseAPIView(APIView):
    """ 月增用户统计 """

    def get(self, request):
        # 获取当前日期
        today = date.today()
        # 获取一个月前日期
        start_date = today - timedelta(days=30)
        # 创建空列表保存每天的用户量
        date_list = []

        for i in range(31):
            # 循环遍历获取当天日期
            index_date = start_date + timedelta(days=i)
            # 指定下一天日期
            cur_date = start_date + timedelta(days=i + 1)

            # 查询条件是大于当前日期index_date，小于明天日期的用户cur_date，得到当天用户量，并且是普通用户
            count = User.objects.filter(date_joined__gte=index_date, date_joined__lt=cur_date, is_staff=0).count()

            date_list.append({
                'count': count,
                'date': index_date
            })

        return Response(date_list)
