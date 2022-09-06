from django.db import models

# Create your models here.

# 1. 自己定义模型
# 密码要自己加密，还要实现登录的时候密码的验证
# class User(models.Model):
#     username = models.CharField(verbose_name='用户名', max_length=20, unique=True)
#     password = models.CharField(verbose_name='密码', max_length=20, )
#     mobile = models.CharField(erbose_name='手机号', max_length=11, unique=True)

# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# 2. django 自带一个用户模型
# 这个用户模型有密码的加密和验证
class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
