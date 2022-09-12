# -*- coding:utf-8 -*-
# @Time : 2022/9/9 22:19
# @Author: fbz
# @File : views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


# 验证用户是否登陆
# LoginRequiredMixin未登錄是返回重定向，前後端分離需要返回json
class LoginRequiredJsonMixin(LoginRequiredMixin):
    # 重寫方法
    def handle_no_permission(self):
        return JsonResponse({'code': 400, 'errmsg': '沒有登錄'})
