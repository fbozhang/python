from django.shortcuts import render

# Create your views here.

# 序列化一个对象
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

# 序列化多个对象
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

# 对外键的处理
'''
from app01.serializers import CountrySerializers
from app01.models import Country

# 获取查询结果集
country = Country.objects.all()

serializer = CountrySerializers(instance=country, many=True)

# 获取序列化器中，将对象转为字典数据
serializer.data
'''

# 反序列化保存数据
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

# 反序列化更新数据
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