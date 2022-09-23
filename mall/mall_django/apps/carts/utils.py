# -*- coding:utf-8 -*-
# @Time : 2022/9/23 17:15
# @Author: fbz
# @File : utils.py

import pickle
import base64

from django_redis import get_redis_connection


def merge_cookie_to_redis(request, response):
    # 读取cookie数据
    cookie_carts = request.COOKIES.get('carts')

    if cookie_carts is not None:
        carts = pickle.loads(base64.b64decode(cookie_carts))
        # 初始化一个字典 用于保存 sku_id:count
        # {sku_id: count, ...}
        cookie_dict = {}
        # 初始化一个列表 用于保存选中的商品id
        selected_ids = []
        # 初始化一个列表 用于保存未选中的商品id
        unselected_ids = []

        # 遍历cookie数据
        # {1: {count: 6, selected: True}}
        for sku_id, count_selected_dict in carts.items():
            cookie_dict[sku_id] = count_selected_dict['count']
            if count_selected_dict['selected']:
                selected_ids.append(sku_id)
            else:
                unselected_ids.append(sku_id)

        user = request.user
        # 将字典数据，列表数据分别添加到redis中
        redis_cli = get_redis_connection('carts')
        pipeline = redis_cli.pipeline()
        # {sku_id:count}
        pipeline.hmset(f'carts_{user.id}', cookie_dict)
        # seleted_id [1,2,3]
        if len(selected_ids) > 0:
            # *selected_ids 對列表數據進行解包
            pipeline.sadd(f'selected_{user.id}', *selected_ids)
        if len(unselected_ids) > 0:
            # *selected_ids 對列表數據進行解包
            pipeline.srem(f'selected_{user.id}', *unselected_ids)

        pipeline.execute()

        # 删除cookie数据
        response.delete_cookie('carts')

    return response