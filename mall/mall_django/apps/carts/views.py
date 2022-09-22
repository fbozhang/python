import base64
import json
import pickle

from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse
from django_redis import get_redis_connection

from apps.goods.models import *


class CartVist(View):

    def post(self, request):
        # 接收數據
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        count = data.get('count')

        # 驗證數據
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '查無此商品'})

        # 類型簽字轉換
        try:
            count = int(count)
        except Exception:
            count = 1

        # 判斷用戶的登錄狀態
        '''
        request.user 如果是登錄用戶就是關聯User的模型數據
        is_authenticated = True 認證用戶
        如果不是登錄用戶就是匿名用戶
        匿名用戶的 is_authenticated = False
        '''
        user = request.user

        # 登錄用戶保存redis
        if user.is_authenticated:
            # 連接redis
            redis_cli = get_redis_connection('carts')
            # 操作hash
            # redis_cli.hset(key,field,value)
            redis_cli.hset(f'carts_{user.id}', sku_id, count)
            # 操作set
            # 默認選中
            redis_cli.sadd(f'selected_{user.id}', sku_id)

            # 返回相應
            return JsonResponse({'code': 0, 'errmsg': 'ok'})

        # 未登錄用戶保存cookie
        else:
            '''
                cookie:
                    {
                        sku_id:{'count': count,'selected': True},
                        sku_id:{'count': count,'selected': True},
                        sku_id:{'count': count,'selected': True},
                    }
            '''
            # 先讀取cookie數據
            cookie_carts = request.COOKIES.get('carts')
            if cookie_carts:
                # 對數據解密
                carts = pickle.loads(base64.b64decode(cookie_carts))
            else:
                # 初始化cookie字典
                carts = {}

            # 判斷新增的商品有沒有在購物車裏
            if sku_id in carts:
                # 購物車中 已經有該商品id
                origin_count = carts[sku_id]['count']
                count += origin_count

            carts[sku_id] = {
                'count': count,
                'selected': True
            }

            # 將數據轉換為bytes
            carts_bytes = pickle.dumps(carts)
            # bytes類型數據base64編碼
            base64endoce = base64.b64encode(carts_bytes)

            # 設置cookie
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            # key, value = "", max_age = None,
            # base64endoce.decode() 的作用是 將bytes類型轉換為str
            # 因爲value的數據是 str
            response.set_cookie('carts', base64endoce.decode(), max_age=3600 * 24 * 14)

            # 返回相應
            return response