# -*- coding:utf-8 -*-
# @Time : 2022/9/9 22:19
# @Author: fbz
# @File : views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class LoginRequiredJsonMixin(LoginRequiredMixin):
    # 重寫方法
    def handle_no_permission(self):
        return JsonResponse({'code': 400, 'errmsg': '沒有登錄'})