# -*- coding:utf-8 -*-
# @Time : 2023/3/27 18:29
# @Author: fbz
# @File : urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh, token_verify

from apps.mall_admin.user import MyTokenObtainPairView
from apps.mall_admin.views import home, user, images, sku, permissions, order, spu, specs, options, brands

urlpatterns = [
    # path('authorizations/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 或者下面这样写，点进去看源码发现一样
    path('authorizations/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', token_refresh, name='token_refresh'),
    path('verify/', token_verify, name='token_verify'),

    # 日活统计
    path('statistical/day_active/', home.DailyActiveAPIView.as_view()),
    # 日下单用户统计
    path('statistical/day_orders/', home.DailyOrderCountAPIView.as_view()),
    # 用户总量统计
    path('statistical/total_count/', home.UserCountAPIView.as_view()),
    # 日增用户统计
    path('statistical/day_increment/', home.DailyIncreaseAPIView.as_view()),
    # 日商品访问量统计
    path('statistical/goods_day_views/', home.DailyVistCountAPIView.as_view()),
    # 月增用户统计
    path('statistical/month_increment/', home.MonthIncreaseAPIView.as_view()),

    # 查询用户
    path('users/', user.UserAPIView.as_view()),

    # 获取图片新增中的 sku展示
    path('skus/simple/', images.ImageSKUAPIView.as_view()),
    # 获取三级分类信息
    path('skus/categories/', sku.GoodsCategoryAPIView.as_view()),

    # sku中获取spu数据
    path('goods/simple/', sku.SPUListAPIView.as_view()),
    # sku中获取spu的规格和规格选项
    path('goods/<spu_id>/specs/', sku.SPUSpecAPIView.as_view()),
    # 获取品牌信息
    path('goods/brands/simple/', spu.SPUBrandListAPIView.as_view()),
    path('goods/specs/simple/', options.SPUSimpleListAPIView.as_view()),
    # 获取一级分类信息
    path('goods/channel/categories/', spu.SPUCategoriesListAPIView.as_view()),
    # 获取二级和三级分类
    path('goods/channel/categories/<pk>/', spu.SPUSonCategoriesListAPIView.as_view()),

    # 获取权限类型列表数据
    path('permission/content_types/', permissions.ConentTypeListAPIView.as_view()),
    # 组中获取权限列表数据
    path('permission/simple/', permissions.GroupPermissionListAPIView.as_view()),
    # 获取组数据
    path('permission/groups/simple/', permissions.SimpleGroupListAPIView.as_view()),

    # 更新订单状态
    path('orders/<order_id>/status/', order.OrderStatusUpdateAPIView.as_view()),
]

from rest_framework.routers import DefaultRouter

# 创建router实例
router = DefaultRouter()
# 设置路由
router.register('skus/images', images.ImageModelViewSet, basename='images')
# sku
router.register('skus', sku.SKUModelViewSet, basename='skus')
# 规格表管理(一定要写在spu上面，不然会得不到)
router.register('goods/specs', specs.SpecsModelViewSet, basename='specs')
# 品牌表管理
router.register('goods/brands', brands.BrandModelViewSet, basename='brands')
# spu
router.register('goods', spu.SPUModelViewSet, basename='goods')
# 规格选项表管理
router.register('specs/options', options.OptionsModelViewSet, basename='options')
# 订单管理
router.register('orders', order.OrderInfoModelViewSet, basename='orders')
# 权限
router.register('permission/perms', permissions.PermissionModelViewSet, basename='permission')
# 组
router.register('permission/groups', permissions.GroupModelViewSet, basename='groups')
# 普通管理员
router.register('permission/admins', permissions.AdminUserModelViewSet, basename='admins')
# 追加到urlpatterns
urlpatterns += router.urls
