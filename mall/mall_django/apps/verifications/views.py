from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse, JsonResponse


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


"""
https://www.yuntongxun.com/
短信业务免费开发测试
1.注册
我们提供免费开发测试，【免费开发测试前，请先 注册 成为平台用户】。咨询在线客服

2.绑定测试号
免费开发测试需要在"控制台—管理—号码管理—测试号码"绑定 测试号码 。

3.开发测试
开发测试过程请参考 短信业务接口https://doc.yuntongxun.com/p/5a533de33b8496dd00dce07c 
及 Demo示例https://doc.yuntongxun.com/p/5a533e0c3b8496dd00dce08c / sdk参考（新版）示例。Java环境安装请参考"新版sdk"。

4.免费开发测试注意事项
    4.1.免费开发测试需要使用到"控制台首页"，开发者主账户相关信息，如主账号、应用ID等。
    
    4.2.免费开发测试使用的模板ID为1，具体内容：【云通讯】您的验证码是{1}，请于{2}分钟内正确输入。其中{1}和{2}为短信模板参数。
    
    4.3.测试成功后，即可申请短信模板并 正式使用 。
"""


# /sms_codes/mobile/?image_code=this.image_code&image_code_id=this.image_code_id
class SmsCodeView(View):

    def get(self, request, mobile):
        # 1. 獲取請求參數
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 2. 驗證參數
        if not all([image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '參數不全'})
        # 3. 驗證圖片驗證碼
        # 連接redis
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')
        # 獲取redis數據
        redis_image_code = redis_cli.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code': 400, 'errmsg': '圖片驗證碼已過期'})
        # 對比 lower()轉爲小寫
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': 400, 'errmsg': '圖片驗證碼錯誤'})
        # 4. 生成短信驗證碼
        from random import randint
        sms_code = '%04d' % randint(0, 9999)
        # 5. 保存短信驗證碼
        redis_cli.setex(mobile, 300, sms_code)
        # 6. 發送短信驗證碼
        from libs.yuntongxun.sms import CCP
        CCP().send_template_sms(mobile, [sms_code, 5], 1)  # 給mobile手機號發驗證碼為sms_code時效5分鐘
        # 7. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
