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
