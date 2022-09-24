import json

from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse
from django_redis import get_redis_connection

from apps.goods.models import *
from apps.users.models import *
from utils.views import LoginRequiredJsonMixin


class OrderSettlementView(LoginRequiredJsonMixin, View):
    """ 提交訂單頁面 """

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


from apps.orders.models import *
from django.db import transaction


class OrderCommitView(LoginRequiredJsonMixin, View):
    """ 提交訂單 """

    def post(self, request):
        # 接收请求  user, address_id, pay_method
        user = request.user
        data = json.loads(request.body.decode())
        address_id = data.get('address_id')
        pay_method = data.get('pay_method')

        # 验证数据
        if not all([address_id, pay_method]):
            return JsonResponse({'code': 400, 'errmsg': '參數不全'})

        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '參數不正確'})

        # if pay_method not in [1,2]: # 可讀性差
        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'], OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return JsonResponse({'code': 400, 'errmsg': '參數不正確'})

        # order_id  主键（自己生成）年月日時分秒 + 用戶id(9位數字)
        # from datetime import datetime
        # datetime.strftime()
        from django.utils import timezone
        # timezone.localtime() -> 2022-10-10 10:10:10
        # timezone.localtime().strftime('%Y%m%d%H%M%S') -> 20221010101010
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + '%09d' % user.id

        # 支付状态由支付方式决定
        # 代码是对的。可读性差
        # if pay_method == 1: # 货到付款
        #     pay_status=2
        # else:
        #     pay_status=1
        if pay_method == OrderInfo.PAY_METHODS_ENUM['CASH']:
            status = OrderInfo.ORDER_STATUS_ENUM['UNSEND']
        else:
            status = OrderInfo.ORDER_STATUS_ENUM['UNPAID']

        # 总数量，总金额， = 0
        total_count = 0
        from decimal import Decimal
        total_amount = Decimal('0')
        # 运费
        freight = Decimal('8.00')

        # 開始事務
        with transaction.atomic():

            # 事務開始點(回滾點)，回滾到這
            point = transaction.savepoint()

            # 先保存订单基本信息
            orderinfo = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                address=address,
                total_count=total_count,
                total_amount=total_amount,
                freight=freight,
                pay_method=pay_method,
                status=status
            )

            # 再保存订单商品信息
            # 连接redis
            redis_cli = get_redis_connection('carts')
            # 获取hash
            sku_id_counts = redis_cli.hgetall(f'carts_{user.id}')
            # 获取set
            selected_ids = redis_cli.smembers(f'selected_{user.id}')

            # 遍历选中商品的id，
            # 重写组织一个数据，这个数据是选中的商品信息
            carts = {}
            # {sku_id:count,sku_id:count}
            for sku_id in selected_ids:
                carts[int(sku_id)] = int(sku_id_counts[sku_id])

            # 遍历 {sku_id:count,sku_id:count}
            for sku_id, count in carts.items():
                # 根据选中商品的id进行查询
                try:
                    sku = SKU.objects.get(id=sku_id)
                except SKU.DoesNotExist:
                    return JsonResponse({'code': 400, 'errmsg': '商品不存在'})

                # 判断库存是否充足，
                # 如果不充足，下单失败
                if sku.stock < count:
                    # 回滾點
                    transaction.savepoint_rollback(point)

                    return JsonResponse({'code': 400, 'errmsg': '庫存不足'})

                # 如果充足，则库存减少，销量增加
                # sku.stock -= count
                # sku.sales += count
                # sku.save()  # 保存

                # 先記錄表一個數據, 哪個都行 (樂觀鎖)
                old_stock = sku.stock
                # 更新的時候比對這個記錄對不對
                new_stock = sku.stock - count
                new_sales = sku.sales + count

                result = SKU.objects.filter(id=sku_id, stock=old_stock).update(stock=new_stock, sales=new_sales)
                # result = 1 表示 有1條記錄修改成功
                # result = 0 表示 沒有更新
                if result == 0:
                    transaction.savepoint_rollback(point)
                    return JsonResponse({'code': 400, 'errmsg': '下單失敗~~~'})

                # 累加总数量和总金额
                orderinfo.total_count += count
                orderinfo.total_amount += (count * sku.price)

                #  保存订单商品信息
                OrderGoods.objects.create(
                    order=orderinfo,
                    sku=sku,
                    count=count,
                    price=sku.price,
                )
            # 更新订单的总金额和总数量
            orderinfo.save()

            # 提交點，提交事務
            transaction.savepoint_commit(point)
        # 将redis中选中的商品信息移除出去(暫緩)

        # 返回相應
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'order_id': order_id})


"""
解决并发的超卖问题：
① 队列
② 锁
    悲观锁： 当查询某条记录时，即让数据库为该记录加锁，锁住记录后别人无法操作

            悲观锁类似于我们在多线程资源竞争时添加的互斥锁，容易出现死锁现象

    举例：

    甲   1,3,5,7

    乙   2,4,7,5


    乐观锁:    乐观锁并不是真的锁。
            在更新的时候判断此时的库存是否是之前查询出的库存，
            如果相同，表示没人修改，可以更新库存，否则表示别人抢过资源，不再执行库存更新。



    举例：
                桌子上有10个肉包子。  9    8 

                现在有5个人。 这5个人，每跑1km。只有第一名才有资格吃一个肉包子。 

                5

                4

                3 

    步骤：
            1. 先记录某一个数据  
            2. 我更新的时候，再比对一下这个记录对不对  


MySQL数据库事务隔离级别主要有四种：

    Serializable：串行化，一个事务一个事务的执行。  用的并不多

    Repeatable read：可重复读，无论其他事务是否修改并提交了数据，在这个事务中看到的数据值始终不受其他事务影响。

v    Read committed：读取已提交，其他事务提交了对数据的修改后，本事务就能读取到修改后的数据值。

    Read uncommitted：读取未提交，其他事务只要修改了数据，即使未提交，本事务也能看到修改后的数据值。


    举例：     5,7 库存 都是  8

    甲   5,   7        5

    乙  7,    5         5


MySQL数据库默认使用可重复读（ Repeatable read）

"""
