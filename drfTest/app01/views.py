from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

# Serializer序列化一个对象
'''
from app01.serializers import AutherSerializers
from app01.models import Author

# 获取一个对象
author = Author.objects.get(id=1)

# AutherSerializers(instance=对象, data=字典)
serializers = AutherSerializers(instance=author)

# 获取序列化器将对象转换为字典的数据
serializers.data
'''

# Serializer序列化多个对象
'''
from app01.serializers import AutherSerializers
from app01.models import Author

# 获取一个对象
authors = Author.objects.all()

# AutherSerializers(instance=对象, data=字典)
"""
AttributeError: Got AttributeError when attempting to get a value for field `id` on serializer `AutherSerializers`.
The serializer field might be named incorrectly and not match any attribute or key on the `QuerySet` instance.
Original exception text was: 'QuerySet' object has no attribute 'id'.
"""
# 如果要序列化是多条数据的查询集QuerySet，需要添加many=True
serializers = AutherSerializers(instance=authors, many=True)

# 获取序列化器将对象转换为字典的数据
serializers.data
'''

# Serializer对外键的处理
'''
from app01.serializers import CountrySerializers
from app01.models import Country

# 获取查询结果集
country = Country.objects.all()

serializer = CountrySerializers(instance=country, many=True)

# 获取序列化器中，将对象转为字典数据
serializer.data
'''

# Serializer反序列化保存数据
'''
from app01.serializers import AutherSerializers

data = {
    'author': 'asdasd',
    'direction': 'aseq',
    'useNum': '1',
    'company_name': 'asd',
    'documentTitle': 'asd',
}

# instance 用于序列化(对象转换为字典)
# data     用于反序列化(字典转换为对象)
serializer = AutherSerializers(data=data)

# 验证数据
serializer.is_valid(raise_exception=True)

# 保存数据库, 必须进行验证才能保存
serializer.save()
'''

# Serializer反序列化更新数据
'''
from app01.serializers import AutherSerializers
from app01.models import Author

data = {
    'author': 'qwe',
    'direction': 'qwe',
    'useNum': '1',
    'company_name': 'asd',
    'documentTitle': 'asd',
}

author = Author.objects.get(id=1)

# instance 用于序列化(对象转换为字典)
# data     用于反序列化(字典转换为对象)
serializer = AutherSerializers(instance=author, data=data)

# 验证数据
serializer.is_valid(raise_exception=True)

# 保存数据库, 必须进行验证才能保存
serializer.save()
# 获取新字典数据
serializer.data
'''

# ModelSerializer反序列化保存数据单个字典
'''
from app01.serializers import CountryModelSerializers

data = {
    'country': 'China',
    'area': '1',
}

serializers = CountryModelSerializers(data=data)
serializers.is_valid(raise_exception=True)
serializers.save()
'''

# ModelSerializer反序列化保存数据多个字典
'''
from app01.serializers import CountryModelSerializers

data = [
    {
        'id': 4,
        'country': 'China',
        'area': '1',
    },
    {
        'country': 'HK',
        'area': '2',
    },
]

serializers = CountryModelSerializers(data=data,many=True)
serializers.is_valid(raise_exception=True)
serializers.save()
'''

# ModelSerializer序列化器啊嵌套序列化器保存嵌套字典数据
'''
from app01.serializers import AreaModelSerializers

data = {
    'area': 'Zone IV',
    'country': [
        {
            'id': 4,
            'country': 'China',
        },
        {
            'id': 5,
            'country': 'HK',
        },
    ]
}

serializers = AreaModelSerializers(data=data)
serializers.is_valid(raise_exception=True)
serializers.save()
'''

from rest_framework.views import APIView
from app01.serializers import CountryModelSerializers
from app01.models import Country

from django.http import HttpRequest  # django
from django.http import HttpResponse  # django
from rest_framework.request import Request  # drf
from rest_framework.response import Response  # drf
from rest_framework import status

'''
GenericAPIView 比 APIView 扩展了一些属性和方法

属性
    queryset            设置查询结果集
    serializer_class    设置序列化器
    lookup_field        设置查询指定数据的关键字参数
方法
    get_queryset()      获取查询结果集
    get_serializer()    获取序列化实例
    get_object()        获取到指定的数据
'''


# 一级视图 -- APIView
class CountryListAPIView(APIView):

    def get(self, request: Request):
        # django -- request.GET
        # drf -- request.query_params
        query_params = request.query_params

        # 查询所有数据
        country = Country.objects.all()
        # 将查询结果集给序列化器
        serializers = CountryModelSerializers(instance=country, many=True)

        # 返回响应
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        # django -- request.POST, request.body
        # drf -- request.data
        # 接收参数
        data = request.data
        # 验证参数
        serializer = CountryModelSerializers(data=data)
        serializer.is_valid()
        # 保存数据
        serializer.save()

        # 返回响应
        return Response(data=serializer.data, status=status.HTTP_200_OK)


from rest_framework.generics import GenericAPIView


# 二级视图 -- GenericAPIView
class CountryListGenericAPIView(GenericAPIView):
    # 查询结果集
    queryset = Country.objects.all()
    # 序列化器
    serializer_class = CountryModelSerializers

    def get(self, request: Request):
        # django -- request.GET
        # drf -- request.query_params
        query_params = request.query_params

        # 查询所有数据
        # country = Country.objects.all()
        # country = self.queryset
        country = self.get_queryset()  # 获取查询结果集
        # 将查询结果集给序列化器
        # serializers = CountryModelSerializers(instance=country, many=True)
        # serializers = self.serializer_class(instance=country, many=True)
        serializers = self.get_serializer(instance=country, many=True)  # 获取序列化实例

        # 返回响应
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        # django -- request.POST, request.body
        # drf -- request.data
        # 接收参数
        data = request.data
        # 验证参数
        serializer = self.get_serializer(data=data)  # 获取序列化实例
        serializer.is_valid()
        # 保存数据
        serializer.save()

        # 返回响应
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CountryDetailGenericAPIView(GenericAPIView):
    # 查询所有数据，因为查询结果集有惰性 后续代码可以采用 self.queryset.filter(id=pk) 属性
    # 所以直接设置 手游查询结果就可以
    # 查询结果集
    queryset = Country.objects.all()
    # 序列化器
    serializer_class = CountryModelSerializers
    # 如果想要传参不是 pk，而是其他 则需要设置 lookup_field
    lookup_field = 'id'  # 设置查询指定数据的关键字参数

    def get(self, request: Request, id):
        # 查询指定数据
        # country = self.queryset.filter(id=pk)
        # country = self.get_queryset().filter(id=pk)
        country = self.get_object()  # 获取到指定的数据

        # 将对象数据转换为字典数据
        serializers = self.get_serializer(instance=country)  # 获取序列化实例

        # 返回响应
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk):
        pass

    def delete(self, request: Request, pk):
        pass


from rest_framework.mixins import ListModelMixin, CreateModelMixin


# 二级视图 -- GenericAPIView + mixin
# GenericAPIView 一般和 mixin 配合使用
class CountryGenericMixinAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    # 查询结果集
    queryset = Country.objects.all()
    # 序列化器
    serializer_class = CountryModelSerializers

    def get(self, request: Request):
        # ListModelMixin 中的方法
        return self.list(request)

    def post(self, request: Request):
        # CreateModelMixin 中的方法
        return self.create(request)


from rest_framework.generics import ListCreateAPIView


# 三级视图
class CountryListCreateAPIView(ListCreateAPIView):
    # 查询结果集
    queryset = Country.objects.all()
    # 序列化器
    serializer_class = CountryModelSerializers
