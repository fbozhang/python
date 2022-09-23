"""mall_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.http import HttpResponse

# def log(request):
#     # 1. 导入
#     import logging
#     # 2. 创建日志器
#     logger = logging.getLogger('django')
#     # 3. 调动日志器的方法来保存日志
#     logger.info('用户登录了')
#     logger.warning('redis缓存不足')
#     logger.error('该记录不存在')
#
#     return HttpResponse('log')

# 注册转换器
from utils.converters import UsernameConverter, MobileConverter
from django.urls import register_converter

register_converter(UsernameConverter, 'username')
register_converter(MobileConverter, 'mobile')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('log/', log),
    # 导入users子应用的路由
    path('', include('apps.users.urls')),
    # 导入verifications子应用的路由
    path('', include('apps.verifications.urls')),
    # 导入oauth子应用的路由
    path('', include('apps.oauth.urls')),
    # 导入 areas 子应用的路由
    path('', include('apps.areas.urls')),
    # 导入 goods 子应用的路由
    path('', include('apps.goods.urls')),
    # 导入 contents 子应用的路由
    path('', include('apps.contents.urls')),
    # 导入 carts 子应用的路由
    path('', include('apps.carts.urls')),
    # 导入 orders 子应用的路由
    path('', include('apps.orders.urls')),
]
