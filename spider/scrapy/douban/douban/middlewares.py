# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import time

from scrapy import signals
import random
from selenium import webdriver
from scrapy.http import HtmlResponse
from douban.settings import USER_AGENT_LIST, PROXY_LIST

"""
中间件有三种返回
1. 返回response -> 给爬虫
2. 返回request ->  给调度器
3. 返回None -> 给下载器，默认是None
"""


class seleniumMIddleware(object):
    """ selenium中间件(解决ajax动态渲染网页) """

    def process_request(self, request, spider):
        if spider.name == 'movie':
            print('使用selenium')
            url = request.url
            if '250' in url:  # 看哪个url需要用selenium等页面渲染完再拿响应
                driver = webdriver.Chrome()

                driver.get(url)
                time.sleep(3)  # 等页面渲染完，可以判断出现了哪些元素就是渲染完
                data = driver.page_source  # 获取渲染完的页面

                driver.close()

                return HtmlResponse(url=url, body=data, encoding='utf-8', request=request)  # 返回给爬虫去解析
            else:
                return None  # 返回给下载器，不写else也可以，默认返回None


class RandomUserAgentMiddleware(object):
    """ 随机UA中间件 """

    def process_request(self, request, spider):
        print(request.headers['User-Agent'])
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = user_agent


class RandomProxyMiddleware(object):
    """ 随机代理中间件 """

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
