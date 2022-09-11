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
        print(openid)  # C35E6560AF6B22ED06A78F7706837FD9
        # 4.根據openid進行判斷
        # 5.如果沒有綁定過，則需要綁定
        # 6.如果綁定過，則直接登錄
