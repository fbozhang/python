# -*- coding:utf-8 -*-
# @Time : 2022/8/28 23:07
# @Author: fbz
# @File : order.py
import random
from datetime import datetime

from django import forms
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01.models import *
from app01.utils.bootstrap import BootStrapModelForm


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        # exclude = ['oid']
        

def order_list(request):
    form = OrderModelForm()
    return render(request, 'order_list.html', {'form': form})


@csrf_exempt
def order_add(request):
    """ 新建订单(Ajax请求) """

    # 用户发送过来的数据进行校验(ModelForm)
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        form.instance.oid = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(100, 999))
        # 保存到数据库中
        form.save()
        data_dict = {'status': True}
        return JsonResponse(data_dict)

    data_dict = {'status': False, 'error': form.errors}
    return JsonResponse(data_dict)
