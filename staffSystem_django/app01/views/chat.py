# -*- coding:utf-8 -*-
# @Time : 2023/7/11 22:57
# @Author: fbz
# @File : chat.py
import queue

from django.shortcuts import render
from django.http import JsonResponse

# 这里用python的队列来模拟。也可以使用redis的发布和订阅来实现，则不需要建那么多队列，所有访客都可以访问同一个消息队列
USER_QUEUE = {}  # {'asd':queue.Queue(),'qwe':queue.Queue()} 为每一个访客建一个队列


def chat_list(request):
    uid = request.GET.get('uid')
    USER_QUEUE[uid] = queue.Queue()
    return render(request, 'chat.html', {'uid': uid})


def send_msg(request):
    text = request.GET.get('text')
    for uid, q in USER_QUEUE.items():
        q.put(text)
    return JsonResponse({"msg": 'ok'})


def get_msg(request):
    uid = request.GET.get('uid')
    q = USER_QUEUE[uid]  # 获取自己的队列

    result = {'status': True, 'data': None}
    try:
        data = q.get(timeout=10)
        result['data'] = data
    except queue.Empty as e:
        result['status'] = False

    return JsonResponse(result)
