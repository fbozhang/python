# -*- coding:utf-8 -*-
# @Time : 2022/9/19 23:53
# @Author: fbz
# @File : detail.py

import sys

# ../ 就是當前目錄的上一級目錄，也就是base_dir
sys.path.insert(0, '../')

import os

# 告訴 os 我們的django配置文件在哪裏
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mall_django.settings')

import django

# django.setup 相當於當前的文件有了django的環境，就可以單獨運行這個文件
django.setup()

from apps.goods.models import SKU
from utils.goods import *


def generic_detail_html(sku):
    # try:
    #     sku = SKU.objects.get(id=sku_id)
    # except SKU.DoesNotExist:
    #     pass
    # 分類數據
    categories = get_categories()
    # 麵包屑
    breadcrumb = get_breadcrumb(sku.category)
    # hot_skus
    hot_skus = SKU.objects.all().order_by('sales')[0:3]

    # 規格信息
    goods_spece = get_goods_specs(sku)

    context = {
        'categories': categories,
        'breadcrumb': breadcrumb,
        'sku': sku,
        'hot_skus': hot_skus,
        'specs': goods_spece,
    }

    # 加載模板
    from django.template import loader
    detail_template = loader.get_template('detail.html')

    # 模板渲染
    detail_html_data = detail_template.render(context)

    # 寫入到指定文件
    from mall_django import settings
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), f'front_end_pc/goods/{sku.id}.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(detail_html_data)

    print(sku.id)


if __name__ == '__main__':
    skus = SKU.objects.all()
    for sku in skus:
        generic_detail_html(sku)
