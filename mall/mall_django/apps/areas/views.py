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


class SubAreaView(View):

    def get(self, request, id):
        """ 省市區數據 """

        # 通過省或市id查詢市或區信息
        try:
            parent_model = Area.objects.get(id=id)
            sub_model_list = parent_model.subs.all()

            # 對象轉爲字典數據
            sub_list = []
            for sub_model in sub_model_list:
                sub_list.append({
                    'id': sub_model.id,
                    'name': sub_model.name
                })

            sub_data = {
                'id': parent_model.id,  # 父級的id
                'name': parent_model.name,  # 父級的name
                'subs': sub_list  # 父級的子集
            }

        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '市或區數據錯誤'})

        else:
            return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': sub_data})
