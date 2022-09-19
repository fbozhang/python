# -*- coding:utf-8 -*-
# @Time : 2022/9/19 1:30
# @Author: fbz
# @File : scheduler.py
from apps.contents.models import ContentCategory
from utils.goods import get_categories


def generic_guiling_index_html():
    # 商品分類數據
    categories = get_categories()

    # 廣告數據
    contents = {}
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

    context = {
        'categories': categories,
        'contents': contents,
    }

    # 加載渲染的模板
    from django.template import loader
    index_template = loader.get_template('index.html')

    # 把數據給模板
    index_html_data = index_template.render(context)

    # 把渲染好的HTML，寫入到文件
    from mall_django import settings
    import os
    # os.path.dirname 拿到 BASE_DIR 的上一級目錄
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'front_end_pc/index.html')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(index_html_data)





