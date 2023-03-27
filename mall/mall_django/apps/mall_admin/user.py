# -*- coding:utf-8 -*-
# @Time : 2023/3/28 1:29
# @Author: fbz
# @File : user.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # data = super().validate(attrs)
        # refresh = self.get_token(self.user)
        # data['refresh'] = str(refresh)
        # data['access'] = str(refresh.access_token)
        # Add extra responses here
        # data['username'] = str(self.user.username)

        super().validate(attrs)  # 这里不接收原来的字典，重新构建一个
        refresh = self.get_token(self.user)
        data = {
            'token': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'id': self.user.id,
            'username': self.user.username,
        }

        return data

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
