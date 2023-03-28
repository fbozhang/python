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
