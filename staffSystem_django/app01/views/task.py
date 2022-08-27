# -*- coding:utf-8 -*-
# @Time : 2022/8/28 0:03
# @Author: fbz
# @File : task.py
import json

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def task_list(request):
    """ 任务列表 """

    return render(request, 'task_list.html')


@csrf_exempt  # 免除csrftoken认证
def task_ajax(request):
    print(request.POST)

    data_dict = {'name': request.POST.get('name'), 'age': request.POST.get('age')}
    return HttpResponse(json.dumps(data_dict))
    # return JsonResponse(json_str)
