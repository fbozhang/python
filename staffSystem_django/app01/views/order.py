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
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = Order
        # fields = '__all__'
        exclude = ['admin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(100, 999))
        # 循环找到所有插件，添加class="form-control"
        for name, field in self.fields.items():
            if name == "oid":
                field.widget.attrs = {
                    "value": value,
                    "class": "form-control",
                    "placeholder": field.label,
                    # 'disabled': "disabled", # 不可编辑，不可复制，不可选择，不能接收焦点,后台也不会接收到传值
                    "readonly": "readonly",  # 只读可复制，可选择,可以接收焦点，可以选中或拷贝其文本。后台会接收到传值
                }


def order_list(request):
    queryset = Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)

    form = OrderModelForm()
    context = {
        'form': form,
        'queryset': page_object.page_queryset,  # 分页数据
        'page_string': page_object.html(),  # 页码
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """ 新建订单(Ajax请求) """

    # 用户发送过来的数据进行校验(ModelForm)
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 订单号默认值（也可以使用上面构造方法的方式设置）
        # form.instance.oid = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(100, 999))
        # 设置管理员ID为当前用户ID
        form.instance.admin_id = request.session['info']['id']

        # 保存到数据库中
        form.save()
        data_dict = {'status': True}
        return JsonResponse(data_dict)

    data_dict = {'status': False, 'error': form.errors}
    return JsonResponse(data_dict)


def order_delete(request):
    """ 删除订单 """

    uid = request.GET.get("uid")
    exists = Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "删除失败，数据不存在"})

    Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    """ 根据ID获取订单详细"""

    uid = request.GET.get("uid")
    # queryset = [{"oid":123, "title":"asd"},{dict},{}]
    row_dict = Order.objects.filter(id=uid).values("oid", "title", "price", "status").first()  # .values()得到字典
    # print(row_dict)
    if not row_dict:
        return JsonResponse({"status": False, "error": "数据不存在"})

    # 从数据库取字典
    result = {
        "status": True,
        "data": row_dict,
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """ 编辑订单 """
    uid = request.GET.get("uid")
    row_object = Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "数据不存在,请刷新重试"})

    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})