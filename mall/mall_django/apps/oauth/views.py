import json
import re

from django.shortcuts import render

# Create your views here.
# pip install QQLoginTool 安裝QQLoginTool

from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from mall_django import settings
from django.http import JsonResponse


class QQLoginURLView(View):

    def get(self, request):
        # 1.生成QQLoginTool 實例對象
        qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,  # appid
                     client_secret=settings.QQ_CLIENT_SECRET,  # appsecret
                     redirect_uri=settings.QQ_REDIRECT_URI,  # 用戶同意登錄之後跳轉的頁面
                     state='asd')  # 不知道是什麽東西，先隨便寫
        # 2.調用對象的方法生成跳轉鏈接
        qq_login_url = qq.get_qq_url()
        # 3.返回相應
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'login_url': qq_login_url})


from apps.oauth.models import OAuthQQUser
from apps.users.models import User
from django.contrib.auth import login


class OauthQQView(View):

    def get(self, request):
        # 1.獲取code
        code = request.GET.get('code')
        if code is None:
            return JsonResponse({'code': 400, 'errmsg': '參數不全'})

        # 2.通過code換取token
        qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,  # appid
                     client_secret=settings.QQ_CLIENT_SECRET,  # appsecret
                     redirect_uri=settings.QQ_REDIRECT_URI,  # 用戶同意登錄之後跳轉的頁面
                     state='asd')  # 不知道是什麽東西，先隨便寫
        token = qq.get_access_token(code)

        # 3.根據token換取openid
        openid = qq.get_open_id(token)
        # print(openid)  # C35E6560AF6B22ED06A78F7706837FD9

        # 4.根據openid進行判斷
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 不存在
            # 5.如果沒有綁定過，則需要綁定
            from apps.oauth.utils import generate_token
            # 加密openid
            access_token = generate_token(openid=openid)

            response = JsonResponse({'code': 400, 'access_token': access_token})
            return response
        else:
            # 存在
            # 6.如果綁定過，則直接登錄
            # 設置session
            login(request, qquser.user)
            # 設置cookie
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('username', qquser.user.username)

            return response

    def post(self, request):
        # 1.接收請求
        data = json.loads(request.body.decode())

        # 2.獲取請求參數 openid
        mobile = data.get('mobile')
        password = data.get('password')
        sms_code = data.get('sms_code')
        access_token = data.get('access_token')

        # 解密 access_token
        from apps.oauth.utils import validate_token
        openid = validate_token(access_token)
        if openid is None:
            return JsonResponse({'code': 400, 'errmsg': '參數缺失'})

        # 校驗參數
        if not all([password, mobile, sms_code, openid]):
            return JsonResponse({'code': 400, 'errmsg': '參數不全'})
        # 手機號
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '請輸入正確的手機號哦'})
        # 密碼
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': '請輸入8-20位密碼'})
        # 短信驗證碼
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')  # 創建redis連接對象
        redis_sms_code = redis_cli.get(mobile)  # 得到redis中的短信驗證碼
        if redis_sms_code is None:
            return JsonResponse({'code': 400, 'errmsg': '驗證碼失效'})
        if sms_code != redis_sms_code.decode():
            return JsonResponse({'code': 400, 'errmsg': '輸入的驗證碼有誤'})

        # 3.根據手機號進行用戶信息的查詢
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 手機號不存在
            # 4.查詢到用戶手機號沒有注冊，就創建一個user信息然後綁定
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)
        else:
            # 手機號存在
            # 5.查詢到用戶手機號已經注冊。判斷密碼是否正確，正確就可以直接保存（綁定）user和openid信息
            if not user.check_password(password):
                return JsonResponse({'code': 400, 'errmsg': '賬號或密碼錯誤'})

        OAuthQQUser.objects.create(user=user, openid=openid)

        # 6.狀態保持
        login(request, user)

        # 7.返回相應
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', user.username)

        return response
