from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse
from django_redis import get_redis_connection

from apps.goods.models import *
from apps.users.models import *
from utils.views import LoginRequiredJsonMixin


class OrderSettlementView(LoginRequiredJsonMixin, View):

    def get(self, request):
        # 获取用户信息
        user = request.user

        # 地址信息
        # 查询用户的地址信息[Address, Address, ...]
        addresses = Address.objects.filter(is_deleted=False)

        # 将对象数据转换为字典数据
        addresses_list = []
        for address in addresses:
            addresses_list.append({
                'id': address.id,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'receiver': address.receiver,
                'mobile': address.mobile,
            })

        # 购物车中选中商品的信息
        # 连接redis
        redis_cli = get_redis_connection('carts')
        pipeline = redis_cli.pipeline()
        # hash  {sku_id: count, sku_id: count}
        pipeline.hgetall(f'carts_{user.id}')
        # set   [1, 2]
        pipeline.smembers(f'selected_{user.id}')
        result = pipeline.execute()
        # result = [hash結果, set結果]
        sku_id_counts = result[0]  # {sku_id: count, sku_id: count}
        selected_ids = result[1]  # [1, 2]

        # 重新组织一个 选中的信息
        # selected_carts = {sku_id: count}
        selected_carts = {}
        for sku_id in selected_ids:
            selected_carts[int(sku_id)] = int(sku_id_counts[sku_id])

        # 根据商品的id 查询商品的具体信息[SKU, SKU, SKu...]
        sku_list = []
        for sku_id, count in selected_carts.items():
            try:
                sku = SKU.objects.get(id=sku_id)
            except SKU.DoesNotExist:
                return JsonResponse({'code': 400, 'errmsg': '商品不存在'})
            else:
                # 需要将对象数据转换为字典数据
                sku_list.append({
                    'id': sku.id,
                    'name': sku.name,
                    'default_image_url': sku.default_image.url,
                    'price': sku.price,
                    'count': count,
                })

        # 運費
        from decimal import Decimal
        freight = Decimal('8')

        context = {
            'skus': sku_list,
            'freight': freight,  # 運費
            'addresses': addresses_list
        }

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'context': context})
