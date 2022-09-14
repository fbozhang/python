from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse
from django.core.cache import cache
from apps.areas.models import *


class AreaView(View):

    def get(self, request):

        # 先查詢緩存數據
        province_list = cache.get('province')

        # 如果沒有緩存則查詢數據庫並緩存
        if province_list is None:
            # 查詢省份信息
            provinces = Area.objects.filter(parent=None)

            # 將queryset對象轉爲字典數據
            province_list = []
            for province in provinces:
                province_list.append({
                    'id': province.id,
                    'name': province.name
                })

            # 保存緩存數據
            # cache.set(key,vlaue,expire) -> 鍵 值 過期時間
            cache.set('province', province_list, 24 * 3600)  # 一天

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'province_list': province_list})


class SubAreaView(View):

    def get(self, request, id):
        """ 省市區數據 """

        # 先獲取緩存數據
        sub_list = cache.get(f'city_{id}')

        # 如果緩存不存在
        if sub_list is None:
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

                # 設置緩存數據
                cache.set(f'city_{id}', sub_list, 24 * 3600)

            except Exception as e:
                print(e)
                return JsonResponse({'code': 400, 'errmsg': '市或區數據錯誤'})

            else:
                return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': sub_data})

        # 如果緩存存在
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': {'subs': sub_list}})
