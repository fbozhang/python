# -*- coding:utf-8 -*-
# @Time : 2022/8/25 20:43
# @Author: fbz
# @File : admin.py
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from django import forms

from app01.utils.encrypt import md5
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from django.utils.safestring import mark_safe

from app01.models import *


def admin_list(request):
    """ 管理员列表 """

    # 构造搜索
    data_dict = {}
    value = request.GET.get('query', '')
    if value:
        data_dict['username__contains'] = value

    # 根据搜索条件去数据库获取
    queryset = Admin.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'value': value,
    }

    return render(request, 'admin_list.html', context)


# from app01.utils.bootstrap import BootStrapModelForm
class AdminModeForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = Admin
        fields = ["username", 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),  # render_value=True密码输入错误不会清空输入框
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)

    def clean_confirm_password(self):
        # print(self.cleaned_data)  # {'username': '阿瑟东', 'password': '13', 'confirm_password': '321'}
        password = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != password:
            raise ValidationError("密码不一致")

        # 返回此字段保存到数据库（数据库有此字段） -> 放在了cleaned_data里面
        return confirm


def admin_add(request):
    """ 添加管理员 """

    title = '新建管理员'

    if request.method == 'GET':
        form = AdminModeForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminModeForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)    # {'username': '阿瑟东', 'password': '13', 'confirm_password': '321'}
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {'form': form, 'title': title})


class AdminEditModeForm(BootStrapModelForm):
    class Meta:
        model = Admin
        fields = ['username']


def admin_edit(request, nid):
    """ 编辑管理员 """

    title = '编辑管理员'

    row_object = Admin.objects.filter(id=nid).first()
    if not row_object:
        msg = '数据不存在'
        return render(request, 'error.html', {'msg': msg})

    if request.method == "GET":
        form = AdminEditModeForm(instance=row_object)
        return render(request, "change.html", {"form": form})
    else:
        form = AdminEditModeForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')
        return render(request, 'change.html', {'form': form, 'title': title})


def admin_delete(request, nid):
    """ 删除管理员 """

    Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


class AdminResetModeForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = Admin
        fields = ['password', 'confirm_password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        md5_pwd = md5(password)

        # 去数据库校验当前密码和新输入的密码是否一致
        exists = Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与以前的一致")

        return md5(password)

    def clean_confirm_password(self):
        # print(self.cleaned_data)  # {'username': '阿瑟东', 'password': '13', 'confirm_password': '321'}
        password = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != password:
            raise ValidationError("密码不一致")

        # 返回此字段保存到数据库（数据库有此字段） -> 放在了cleaned_data里面
        return confirm


def admin_reset(request, nid):
    """ 重置密码 """

    row_object = Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')

    title = '重置密码 - {}'.format(row_object.username)
    if request.method == "GET":
        form = AdminResetModeForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminResetModeForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': form, 'title': title})
