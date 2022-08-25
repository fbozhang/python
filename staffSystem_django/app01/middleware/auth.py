# -*- coding:utf-8 -*-
# @Time : 2022/8/25 23:35
# @Author: fbz
# @File : auth.py
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class authMiddleware(MiddlewareMixin):
    """ 中间件 """

    def process_request(self, request):
        # 如果方法中没有返回值（返回None），继续先后走
        # 如果方法中有返回值 render redirect,不往后执行 返回浏览器

        # 排除那些不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的URL /login/
        if request.path_info == '/login/':
            return

        # 检查用户是否已登录，未登录则跳转回登录页面
        # 用户发来请求，获取cookie随机字符串，拿着随机字符串看看session中有没有
        info_dict = request.session.get('info')

        # 读取当前访问的用户的session信息，如果能读到说明登录过，就可以往后走
        if info_dict:
            return

        # 没有登录过，重新回到登录页面
        if not info_dict:
            # None -> 没有登录
            return redirect('/login/')

    def process_response(self, request, response):
        return response
