import json
import re

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from apps.users.models import *


# Create your views here.


# 判断用户名是否重复
class UsernameCountView(View):

    def get(self, request, username):
        # 1. 接收用户名,对用户名进行一下判断
        # if not re.match('[a-zA-Z0-9_-]{5,20}', username):
        #     return JsonResponse({'code': 200, 'errmsg': '用户名不满足需求'})
        # 2. 根据用户名查询数据库
        count = User.objects.filter(username=username).count()
        # 3. 返回响应
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


# 检查手机号
class MobileCountView(View):

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()

        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


# 注册
class RsgisterView(View):

    def post(self, request):
        # 1. 接收请求（POST------JSON）
        # body_dict = request.POST
        body_str = request.body.decode()
        body_dict = json.loads(body_str)

        # 2. 获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        sms_code = body_dict.get('sms_code')
        allow = body_dict.get('allow')

        # 3. 验证数据
        #     3.1 用户名，密码，确认密码，手机号，是否同意协议 都要有
        # all()里面的元素只要是 None，False就返回False否则返回True
        if not all([username, password, password2, mobile, sms_code, allow]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        #     3.2 用户名满足规则，用户名不能重复
        if not re.match('[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 200, 'errmsg': '用户名不满足规则'})
        count = User.objects.filter(username=username).count()
        if count > 0:
            return JsonResponse({'code': 200, 'errmsg': '用户名已存在'})
        #     3.3 密码满足规则
        if len(password) < 8 or len(password) > 20:
            return JsonResponse({'code': 200, 'errmsg': '密码位数不满足规则'})
        #     3.4 确认密码和密码要一致
        if password != password2:
            return JsonResponse({'code': 200, 'errmsg': '确认密码和密码不一致'})
        #     3.5 手机号满足规则，手机号也不能重复
        if not re.match('1[345789]\d{9}', mobile):
            return JsonResponse({'code': 200, 'errmsg': '手机号不满足规则'})
        count = User.objects.filter(mobile=mobile).count()
        if count > 0:
            return JsonResponse({'code': 200, 'errmsg': '手机号已存在'})
        #     3.6 驗證碼短信驗證碼
        from django_redis import get_redis_connection
        # 連接redis
        redis_cli = get_redis_connection('code')
        # 獲取redis數據
        redis_sms_code = redis_cli.get(mobile)
        # 判斷短信驗證碼是否過期
        if redis_sms_code is None:
            return JsonResponse({'code': 400, 'errmsg': '短信驗證碼過期'})
        # 對比用戶輸入的驗證碼是否正確
        if redis_sms_code.decode() != sms_code:  # redis_sms_code是byte類型，要decode為str類型
            return JsonResponse({'code': 400, 'errmsg': '短信驗證碼有誤'})
        #     3.7 需要同意协议
        if not allow:
            return JsonResponse({'code': 200, 'errmsg': '需要同意协议'})

        # 4. 数据入库
        '''user = User(username=username, password=password, mobile=mobile)
        user.save()

        User.objects.create(username=username,password=password,mobile=mobile)
        # 以上2中方式，都是可以数据入库的
        # 但是 有一个问题 密码没有加密'''

        # 密码加密
        user = User.objects.create_user(username=username, password=password, mobile=mobile)

        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})

        # 设置session信息
        # request.session['user_id'] = user.id

        # Django 提供的状态保存方法
        from django.contrib.auth import login
        # request, user
        # 状态保持 -- 登录用户的状态保持
        # user 已经登录的用户信息
        login(request, user)

        # 5. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


"""
如果需求是注册成功后即表示用户认证通过，那么此时可以在注册成功后实现状态保持 (注册成功即已经登录)  
如果需求是注册成功后不表示用户认证通过，那么此时不用在注册成功后实现状态保持 (注册成功，单独登录)

实现状态保持主要有两种方式：
    在客户端存储信息使用Cookie
    在服务器端存储信息使用Session
"""


class LoginView(View):

    def post(self, request):
        # 1. 接收数据
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')

        # 2. 验证数据
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '參數不全'})

        # 判斷是根據手機號登錄還是用戶名登錄
        # authenticate根據修改User.USERNAME_FIELD字段來查詢
        if re.match('1[3-9]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'  # 源代碼默認是用戶名

        # 3. 验证用户名和密码是否正确
        # 通過模型根據用戶名查詢
        # User.objects.get(username=username)
        # print(User.objects.get(username=username).check_password(password))

        # 方法2
        from django.contrib.auth import authenticate
        # authenticate傳遞用戶名和密碼
        # 如果用戶名和密碼正確，返回User信息，不正確返回None
        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '賬號或密碼錯誤'})

        # 4. session
        from django.contrib.auth import login
        login(request, user)

        # 5. 判断是否记住密碼
        if remembered:
            # 記住密碼  -- 2周
            request.session.set_expiry(None)
        else:
            # 不記住密碼，瀏覽器關閉session過期
            request.session.set_expiry(0)

        # 6. 返回响应
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        # 爲了首頁顯示用戶信息展示
        response.set_cookie('username', user.username)

        return response


from django.contrib.auth import logout


class LogoutView(View):

    def delete(self, request):
        # 刪除session信息
        logout(request)

        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        # 刪除cookie信息
        response.delete_cookie('username')

        return response


from django.contrib.auth.mixins import LoginRequiredMixin
from utils.views import LoginRequiredJsonMixin


# 用戶中心必須是登錄用戶
class CenterView(LoginRequiredJsonMixin, View):

    def get(self, request):
        # request.user 就是已經登錄的用戶信息
        # request.user 就是來源於中間件
        # 系統會進行判斷 如果確實是登錄用戶，則可以獲取到登錄用戶對應的模型實例數據
        # 如果不是登錄用戶，則request.user = AnoymousUesr() 匿名用戶
        info_data = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
        }

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': info_data})


# 添加郵箱
class EmailView(LoginRequiredJsonMixin, View):

    def put(self, request):
        # 接收請求
        data = json.loads(request.body.decode())
        # 獲取數據
        email = data.get('email')

        # 驗證數據
        if not email:
            return JsonResponse({'code': 400, 'errmsg': '缺少email參數'})
        if not re.match(r'[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}', email):
            return JsonResponse({'code': 400, 'errmsg': '參數email有誤'})

        # 保存郵箱地址
        user = request.user
        user.email = email
        user.save()

        # 發送一封激活郵件
        from django.core.mail import send_mail
        subject = '龜靈商城激活郵件'  # 主題
        message = ""  # 郵件内容
        from_email = '龜靈聖母<fbozhang@163.com>'  # 發件人
        recipient_list = ['fbozhang@163.com']  # 收件人列表

        # 加密數據
        from utils.tooken import generate_token
        id_token = generate_token(data={'id_token': request.user.id})

        # 郵件内容如果是html，使用html_message, 將message制空即可因爲不管裏面是什麽都不會發出去
        html_message = "點擊按鈕進行激活 <a href='http://www.guiling.cn:8080?token={id_token}'>激活</a>".format(
            id_token=id_token)  # html郵件内容

        # 發送郵件
        send_mail(subject=subject,
                  message=message,
                  from_email=from_email,
                  recipient_list=recipient_list,
                  html_message=html_message)

        # 返回相應
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
