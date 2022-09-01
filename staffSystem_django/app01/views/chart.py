# -*- coding:utf-8 -*-
# @Time : 2022/9/1 18:50
# @Author: fbz
# @File : chart.py
from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    """ 数据统计页面 """
    return render(request, "chart_list.html")


def chart_line(request):
    """ 构造折线图数据 """

    data_list = [820, 932, 901, 934, 1290, 1330, 1320]

    result = {
        "status": True,
        "data": data_list
    }
    return JsonResponse(result)


def chart_bar(request):
    """ 构造柱状图数据 """

    # 在数据库获取数据
    legend = ['阿斯顿', '周星驰']
    series_list = [
        {
            'name': '阿斯顿',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20]
        },
        {
            'name': '周星驰',
            'type': 'bar',
            'data': [5, 20, 80, 10, 10, 100]
        }
    ]
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月']

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    """ 构造饼图数据 """

    data_list = [
        {'value': 1048, 'name': 'IT部'},
        {'value': 735, 'name': '运维部'},
        {'value': 580, 'name': '测试部'},
        {'value': 484, 'name': '销售部'},
        {'value': 300, 'name': '新闻部'}
    ]

    result = {
        "status": True,
        "data": data_list
    }

    return JsonResponse(result)
