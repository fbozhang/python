# -*- coding:utf-8 -*-
# @Time : 2022/8/25 20:42
# @Author: fbz
# @File : user.py
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from django import forms

from app01.utils.encrypt import md5
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from django.utils.safestring import mark_safe

from app01.models import *


def user_list(request):
    """ 用户管理 """

    # 获取所有用户列表
    quertset = UserInfo.objects.all()

    """
    for obj in quertset:
        print(obj.name, obj.create_time, type(obj.create_time))
        print(obj.create_time.strftime("%Y-%m-%d"), type(obj.create_time.strftime("%Y-%m-%d")))
        print(obj.gender, obj.get_gender_display()) # get_字段名_display()得到choices的值

        # title = Department.objects.filter(id=obj.depart_id).first().title
        # print(title)
        # obj.depart_id   # 获取数据库中存储的那个字段值
        # obj.depart  # 根据id自动去关联的表中获取那一行数据的depart对象
        print(obj.depart.title)
        """

    page_object = Pagination(request, quertset, page_size=2)

    context = {
        'queryset': page_object.page_queryset,  # 分页数据
        'page_string': page_object.html(),  # 页码
    }

    return render(request, "user_list.html", context)


def user_add(request):
    """ 添加用户(原始方法) """

    if request.method == 'GET':
        context = {
            'gender_choices': UserInfo.gender_choices,
            'depart_list': Department.objects.all(),
        }
        return render(request, "user_add.html", context)

    # 获取用户提交的数据
    name = request.POST.get('name')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # 添加到数据库中
    UserInfo.objects.create(name=name, password=pwd, age=age,
                            account=account, create_time=ctime,
                            gender=gender, depart_id=depart_id)

    # 返回到用户列表
    return redirect("/user/list")


# ModelForm示例
# from django import forms
class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3, label="用户名")

    # password = forms.CharField(mlabel="密码", validators=) # validators=正则表达式

    class Meta:
        model = UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有插件，添加class="form-control"
        for name, field in self.fields.items():
            # if name == "age":
            #     continue
            # print(name, field)
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_model_form_add(request):
    """ 添加用户(ModelForm版本) """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {'form': form})

    # 用户POST提交数据,数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如歌数据合法，保存到数据库
        # print(form.cleaned_data)    # {'name': '史蒂夫', 'password': '432'}
        # UserInfo.objects.create(..)
        form.save()
        return redirect('/user/list/')
    else:
        # 校验失败
        # print(form.errors)
        return render(request, 'user_model_form_add.html', {'form': form})


def user_edit(request, nid):
    """ 编辑用户 """

    # 根据id去数据库获取要编辑的那一行数据(对象)
    row_object = UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})

    else:
        form = UserModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            # 默认保存的是用户输入的所有数值，如果想要用户输入以外增加一点值
            # form.instance.字段名 = 默认值(form.instance.name = '阿斯顿')
            form.save()
            return redirect('/user/list/')
        return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    UserInfo.objects.filter(id=nid).delete()

    return redirect('/user/list/')
