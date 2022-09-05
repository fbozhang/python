from django.shortcuts import render

# Create your views here.


from django.views import View
from apps.users.models import *
from django.http import JsonResponse


# 判断用户名是否重复
class UsernmaeCountView(View):

    def get(self, request, username):
        # 1. 接收用户名
        # 2. 根据用户名查询数据库
        count = User.objects.filter(username=username).count()
        # 3. 返回响应
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})
