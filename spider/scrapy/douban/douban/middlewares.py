# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import base64

from scrapy import signals
import random
from douban.settings import USER_AGENT_LIST, PROXY_LIST


class RandomUserAgentMiddleware(object):

    def process_request(self, request, spider):
        print(request.headers['User-Agent'])
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = user_agent


class RandomProxyMiddleware(object):

    def process_request(self, request, spider):
        proxy = random.choice(PROXY_LIST)
        print(proxy)

        if 'user_password' in proxy:
            # 对账号密码进行编码
            b64_ip = base64.b64encode(proxy['user_password'].encode('utf-8'))
            # 设置认证(百度http认证流程，就是添加请求头)(注意 Basic 后面有一个空格)
            request.headers['Proxy-Authorization'] = 'Basic ' + b64_ip.decode()
            # 设置代理
            request.meta['proxy'] = 'http://' + proxy['ip_port']
        else:
            request.meta['proxy'] = 'http://' + proxy['ip_port']

    def process_response(self, request, response, spider):
        # 如果返回的状态码是 200，说明请求成功
        if response.status == 200:
            return response
        # 如果不是 200，说明请求失败
        else:
            proxy = request.meta['proxy']
            PROXY_LIST.remove(proxy)
            request.meta['proxy'] = random.choice(PROXY_LIST)
            print('更换代理')
            return request

    def process_exception(self, request, exception, spider):
        print('代理请求失败')
        if isinstance(exception, (TimeoutError, ConnectionRefusedError)):
            # if 'proxy' in request.meta:
            proxy = request.meta['proxy']
            PROXY_LIST.remove(proxy)
            request.meta['proxy'] = random.choice(PROXY_LIST)
            print('更换代理')
            return request
        else:
            # 其他异常情况，根据实际情况处理
            pass
