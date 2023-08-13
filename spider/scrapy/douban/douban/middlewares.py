# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from douban.settings import USER_AGENT_LIST


class RandomUserAgentMiddleware(object):

    def process_request(self, request, spider):
        print(request.headers['User-Agent'])
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = user_agent
