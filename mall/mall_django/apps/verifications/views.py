from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse


class ImageCodeView(View):

    def get(self, request, uuid):
        # 1. 接收路由中的uuid
        # 2. 生成图片验证码和图片二进制
        from libs.captcha.captcha import captcha
        # text 是图片验证码的内容
        # image 是图片二进制
        text, image = captcha.generate_captcha()
        print(text)

        # 3. 通过redis把图片验证码保存起来
        # 进行redis的连接
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')
        # redis指令操作
        # name time value
        redis_cli.setex(uuid, 100, text)

        # 4. 返回图片二进制
        # 因为图片是二进制所以不能返回json
        # content_type=响应体数据类型
        # content_type 的语法形式是：大类/小类
        # 图片： image/jpeg, image/gif, image/png
        return HttpResponse(image, content_type='image/jpeg')
