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
            # 14天免登录
            # set_expiry(value), value是一个整数，将在value秒后过期
            #                           None 默认两周，可以在setting中设置
            #                            0   将在浏览器关闭时过期
            request.session.set_expiry(None)
        else:
            # 不記住密碼，瀏覽器關閉session過期
            request.session.set_expiry(0)

        # 6. 返回响应
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        # 爲了首頁顯示用戶信息展示
        response.set_cookie('username', user.username)

        # 登錄后合并購物車
        from apps.carts.utils import merge_cookie_to_redis
        response = merge_cookie_to_redis(request, response)

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
        # html_message = "點擊按鈕進行激活 <a href='http://www.guiling.cn:8080'>激活</a>"  # html郵件内容
        verify_url = f'http://www.guiling.cn:8080/success_verify_email.html?token={id_token}'

        html_message = f'''
        <p>尊敬的用户您好！</p>
        <p>感谢您使用龜靈商城。</p>
        <p>您的邮箱为：{email} 。请点击此链接激活您的邮箱：</p>
        <p><a href="{verify_url}">{verify_url}<a></p>
        '''

        # 發送郵件
        # send_mail(subject=subject,
        #           message=message,
        #           from_email=from_email,
        #           recipient_list=recipient_list,
        #           html_message=html_message)

        # 使用celery異步發送郵件
        from celery_tasks.email.tasks import celery_send_email
        # 必須要要 .delay 才有celery異步，不然是同步
        celery_send_email.delay(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message
        )

        # 返回相應
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class EmailVerfyView(View):

    def put(self, request):
        # 接收請求
        params = request.GET
        # 獲取參數
        token = params.get('token')
        # 驗證參數
        if token is None:
            return JsonResponse({'code': 400, 'errmsg': '參數缺失'})

        # 獲取user_id
        from utils.tooken import validate_token
        # 解密token
        user_id = validate_token(token=token).get('id_token')
        if user_id is None:
            return JsonResponse({'code': 400, 'errmsg': '參數錯誤'})

        # 根據用戶id查詢數據
        user = User.objects.get(id=user_id)
        # 修改數據
        user.email_active = True
        user.save()

        # 返回相應
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class AddressCreateView(LoginRequiredJsonMixin, View):
    """ 新增地址 """

    def post(self, request):
        # 接收請求
        data = json.loads(request.body.decode())

        # 獲取參數,
        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')

        user = request.user

        # 驗證參數
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({'code': 400, 'errmsg': '參數不全'})
        if not re.match(r'1[345789]\d{9}', mobile):
            return JsonResponse({'code': 400, 'errmsg': '參數mobile有誤'})
        if email:
            if not re.match(r'[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}', email):
                return JsonResponse({'code': 400, 'errmsg': '參數email有誤'})

        # 數據入庫
        address = Address.objects.create(
            user=user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            tel=tel,
            email=email
        )

        adress_dict = {
            'id': address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'address': adress_dict})


class AddressView(LoginRequiredJsonMixin, View):

    def get(self, request):
        # 查詢數據
        user = request.user
        # addresses = user.addresses
        addresses = Address.objects.filter(user=user, is_deleted=False)

        # 将对象数据转换为字典数据
        address_list = []
        for address in addresses:
            address_list.append({
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            })

        # 3.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'addresses': address_list})


from apps.goods.models import *
from django_redis import get_redis_connection


class UserHistoryView(LoginRequiredJsonMixin, View):

    def post(self, request):
        """ 添加用户浏览历史记录 """

        user = request.user
        # 接收請求
        data = json.loads(request.body.decode())
        # 獲取請求參數
        sku_id = data.get('sku_id')
        # 驗證參數
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '沒有此商品'})

        # 連接redis
        redis_cli = get_redis_connection('history')
        # 去重(先刪除這個商品id的數據，再添加就可以了)
        redis_cli.lrem(f'history_{user.id}', 0, sku_id)  # 刪除
        # 保存到redis list
        redis_cli.lpush(f'history_{user.id}', sku_id)  # 添加
        # 只保存5條記錄
        # ltrim(list,0,4) -> 只保留列表中 0 ~ 4 號位的5個數據
        redis_cli.ltrim(f'history_{user.id}', 0, 4)

        # 返回相應
        return JsonResponse({'code': 0, 'errmsg': 'ok'})

    def get(self, request):
        """ 展示用户浏览历史记录 """

        # 連接redis
        redis_cli = get_redis_connection('history')
        # 獲取redis數據([1,2,3])
        ids = redis_cli.lrange(f'history_{request.user.id}', 0, 4)
        # ([1,2,3])
        # 根據商品id進行數據查詢
        history_list = []
        for sku_id in ids:
            try:
                sku = SKU.objects.get(id=sku_id)
            except SKU.DoesNotExist:
                return JsonResponse({'code': 400, 'errmsg': '沒有此商品'})

            # 將對象轉爲字典
            history_list.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image.name,
                'price': sku.price
            })

        # 返回相應
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'skus': history_list})
