# -*- coding:utf-8 -*-
# @Time : 2022/9/10 23:13
# @Author: fbz
# @File : models.py
from django.db import models


class BaseModel(models.Model):
    """ 為模型類補充字段 """

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='更新時間')

    class Meta:
        abstract = True # 説明是抽象模型類，用於繼承使用，數據庫遷移時不會創建BaseModel的表
