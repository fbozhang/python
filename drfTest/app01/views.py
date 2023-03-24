from django.shortcuts import render

# Create your views here.
from app01.serializers import AutherSerializers
from app01.models import Author

author = Author.objects.get(id=1)

# AutherSerializers(instance=对象, data=字典)
serializers = AutherSerializers(instance=author)

# 获取序列化器将对象转换为字典的数据
serializers.data
