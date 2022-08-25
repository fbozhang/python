# -*- coding:utf-8 -*-
# @Time : 2022/8/25 20:40
# @Author: fbz
# @File : account.py
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from django import forms

from app01.utils.encrypt import md5
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import *
from django.utils.safestring import mark_safe

from app01.models import *


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True  # 必填(默认为True，这里不写也行)
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def login(request):
    """ 登录 """

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，获取到的用户名和密码
        # print(form.cleaned_data)  # {'username': 'asd', 'password': '8dcc02a3be062a857c2252db1f36866a'}

        # 去数据库校验用户名和密码是否正确,获取用户对象、None
        # Admin.objects.filter(username=form.cleaned_data['username'],password=form.cleaned_data['password']).first()
        admin_object = Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error('password', '用户名或密码错误')  # 加一个错误信息
            # form.add_error('username', '用户名或密码错误')  # 加一个错误信息
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串；写到用户浏览器的cookie中；再写入到session中
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}
        return redirect('/admin/list/')

    return render(request, 'login.html', {'form': form})
