# -*- coding:utf-8 -*-
# @Time : 2022/8/24 23:27
# @Author: fbz
# @File : encrypt.py
from django.conf import settings

import hashlib


def md5(dara_str):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(dara_str.encode('utf-8'))

    return obj.hexdigest()
