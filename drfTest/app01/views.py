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