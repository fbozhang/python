"""drfTest URL Configuration

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
from django.urls import path
from app01.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apicountry/', CountryListAPIView.as_view()),
    # GenericAPIView
    path('genericcountry/', CountryListGenericAPIView.as_view()),
    # path('genericcountry/<pk>/', CountryDetailGenericAPIView.as_view()),
    path('genericcountry/<id>/', CountryDetailGenericAPIView.as_view()),
    # GenericAPIView + Mixin
    path('mixincountry/', CountryGenericMixinAPIView.as_view()),
    path('mixincountry/<pk>/', CountryDetailGenericMixinAPIView.as_view()),
    # 三级视图
    path('threecountry/', CountryListCreateAPIView.as_view()),

    # 视图集
    path('viewsetcountry/', CountryViewSet.as_view({'get': 'list'})),
    path('viewsetcountry/<pk>/', CountryViewSet.as_view({'get': 'retrieve'})),
]

# 视图集的路由借助于 drf 的 router 实现
from rest_framework.routers import DefaultRouter

# 创建router实例
router = DefaultRouter()
# 设置列表视图和详情视图的公共部分(不包括/部分)
# prefix            列表视图和详情视图的公共部分(不包括/部分)
# viewset           视图集
# basename=None     给列表视图和详情视图的路由设置别名
router.register(prefix='asd', viewset=CountryModelViewSet, basename='qwe')
# 将router生成的路由追加到 urlpatterns
urlpatterns += router.urls
