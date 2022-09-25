from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse

from mall_django import settings
from alipay import AliPay, AliPayConfig
from apps.orders.models import OrderInfo
from utils.views import LoginRequiredJsonMixin

"""
https://github.com/fzlee/alipay/blob/master/README.zh-hans.md
"""


class PayUrlView(LoginRequiredJsonMixin, View):

    def get(self, request, order_id):
        user = request.user
        # 获取订单id
        # 验证订单id (根据订单id查询订单信息)
        try:
            # 查詢待支付的訂單
            order = OrderInfo.objects.get(order_id=order_id,
                                          status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'],
                                          user=user)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '沒有此訂單'})

        # 查看文檔: https://github.com/fzlee/alipay/blob/master/README.zh-hans.md
        # 读取应用私钥和支付宝公钥
        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()

        # 创建支付宝实例
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调 url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=settings.ALIPAY_DEBUG,  # 默认 False
            verbose=False,  # 输出调试数据
            config=AliPayConfig(timeout=15)  # 可选，请求超时时间
        )

        # 调用支付宝的支付方法
        # 如果你是 Python3 的用户，使用默认的字符串即可
        subject = "龜靈商城测试订单"

        # 电脑网站支付，需要跳转到：https://openapi.alipay.com/gateway.do? + order_string
        # https://openapi.alipay.com/gateway.do? 這個是綫上的
        # https://openapi.alipaydev.com/gateway.do 這個是沙箱的
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),  # DecimalField 類型一定要强制轉換
            subject=subject,
            return_url=settings.ALIPAY_RETURN_URL,
            notify_url="https://example.com/notify"  # 可选，不填则使用默认 notify url
        )
        # 拼接连接
        pay_url = settings.ALIPAY_URL + '?' + order_string

        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'alipay_url': pay_url})
