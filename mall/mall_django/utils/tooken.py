# -*- coding:utf-8 -*-
# @Time : 2022/9/13 15:16
# @Author: fbz
# @File : tooken.py
from authlib.jose import jwt, JoseError
from mall_django import settings


# 加密
def generate_token(data):
    """
    生成用于邮箱验证的JWT（json web token）
    傳入一個需要加密的字典

    例如: data = {'openid': openid}
    """
    # 签名算法
    header = {'alg': 'HS256'}
    # 用于签名的密钥
    key = settings.SECRET_KEY
    # 待签名的数据负载
    # 例子：data = {'openid': openid}
    # data.update(**kwargs)

    access_token = jwt.encode(header=header, payload=data, key=key)

    # 將bytes類型轉爲str
    return access_token.decode()


# 解密
def validate_token(token):
    """用于验证token, 返回原未加密字典數據"""
    key = settings.SECRET_KEY

    try:
        data = jwt.decode(token, key)
        # print(data)
    except JoseError:
        return None
    else:
        return data
