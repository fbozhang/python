import re

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from apps.users.models import *


# Create your views here.


# 判断用户名是否重复
class UsernmaeCountView(View):

    def get(self, request, username):
        # 1. 接收用户名,对用户名进行一下判断
        # if not re.match('[a-zA-Z0-9_-]{5,20}', username):
        #     return JsonResponse({'code': 200, 'errmsg': '用户名不满足需求'})
        # 2. 根据用户名查询数据库
        count = User.objects.filter(username=username).count()
        # 3. 返回响应
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})
