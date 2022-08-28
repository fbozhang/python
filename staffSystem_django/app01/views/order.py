# -*- coding:utf-8 -*-
# @Time : 2022/8/28 23:07
# @Author: fbz
# @File : order.py
from django.shortcuts import render

from app01.models import *
from app01.utils.bootstrap import BootStrapModelForm


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = Order
        fields = '__all__'


def order_list(request):
    form = OrderModelForm()
    return render(request, 'order_list.html', {'form': form})
