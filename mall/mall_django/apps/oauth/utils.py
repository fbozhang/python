# -*- coding:utf-8 -*-
# @Time : 2022/9/13 15:16
# @Author: fbz
# @File : utils.py
from authlib.jose import jwt, JoseError
from mall_django import settings


# 加密
def generate_token(openid, **kwargs):
    """生成用于邮箱验证的JWT（json web token）"""
    # 签名算法
    header = {'alg': 'HS256'}
    # 用于签名的密钥
    key = settings.SECRET_KEY
    # 待签名的数据负载
    data = {'openid': openid}
    data.update(**kwargs)

    access_token = jwt.encode(header=header, payload=data, key=key)

    # 將bytes類型轉爲str
    return access_token.decode()


# 解密
def validate_token(token):
    """用于验证用户注册和用户修改密码或邮箱的token, 并完成相应的确认操作"""
    key = settings.SECRET_KEY

    try:
        data = jwt.decode(token, key)
        # print(data)
    except JoseError:
        return None
    else:
        return data.get('openid')
