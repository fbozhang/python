from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse
from apps.areas.models import *


class AreaView(View):

    def get(self, request):
        # 查詢省份信息
        provinces = Area.objects.filter(parent=None)

        # 將queryset對象轉爲字典數據
        province_list = []
        for province in provinces:
            province_list.append({
                'id': province.id,
                'name': province.name
            })

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'province_list': province_list})
