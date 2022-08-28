# -*- coding:utf-8 -*-
# @Time : 2022/8/28 0:03
# @Author: fbz
# @File : task.py
import json

from django import forms
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01.models import *
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            # 'detail': forms.Textarea,
            'detail': forms.TextInput
        }


def task_list(request):
    """ 任务列表 """

    # 去数据库获取所有的任务
    queryset = Task.objects.all().order_by('id')
    form = TaskModelForm()

    page_object = Pagination(request, queryset)

    context = {
        'form': form,
        'queryset': page_object.page_queryset,  # 分页数据
        'page_string': page_object.html(),  # 页码
    }
    return render(request, 'task_list.html', context)


@csrf_exempt  # 免除csrftoken认证
def task_ajax(request):
    print(request.POST)

    data_dict = {'status': True, 'data': [12, 23]}
    return HttpResponse(json.dumps(data_dict))
    # return JsonResponse(json_str)


@csrf_exempt
def task_add(request):
    print(request.POST)

    # 用户发送过来的数据进行校验(ModelForm)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {'status': True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
