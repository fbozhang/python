# -*- coding:utf-8 -*-
# @Time : 2023/7/11 22:57
# @Author: fbz
# @File : chat.py
import queue

from django.shortcuts import render
from django.http import JsonResponse

# 这里用python的队列来模拟。也可以使用redis的发布和订阅来实现，则不需要建那么多队列，所有访客都可以访问同一个消息队列
USER_QUEUE = {}  # {'asd':queue.Queue(),'qwe':queue.Queue()} 为每一个访客建一个队列


def longPoll_chat(request):
    uid = request.GET.get('uid')
    USER_QUEUE[uid] = queue.Queue()
    return render(request, 'longPoll_chat.html', {'uid': uid})


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


from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync


def ws_chat(request):
    return render(request, 'ws_chat.html')

CONN_LIST = []
class wsChat(WebsocketConsumer):
    def websocket_connect(self, message):
        # 有客户端来向后端发送ws连接的请求时，自动触发。
        print('连接成功')
        # 服务端允许和客户端创建连接(握手)
        self.accept()  # 同时请求WebSocket HANDSHAKING和WebSocket CONNECT，分别是握手和连接
        CONN_LIST.append(self)

    def websocket_receive(self, message):
        # 浏览器基于ws向后端发送数据，自动触发接收消息
        text = message['text']  # {'type': 'websocket.receive', 'text': 'asd'}
        if text == 'close':
            # 服务端主动断开连接
            self.close()  # 同时也会执行客户端断开连接方法 WebSocket DISCONNECT(websocket_disconnect())
            return  # 不再执行下面的代码，如果断开连接还发送消息会报错
            # raise StopConsumer() #如果服务端断开连接时，执行raise StopConsumer()，那么不会执行websocket_disconnect()方法

        for conn in CONN_LIST:
            conn.send(f'接收到消息：{text}')
        #self.send(f'接收到消息：{text}')  # 服务端给客户端发送消息

    def websocket_disconnect(self, message):
        # 客户端与服务端端开连接时自动触发(客户端主动端开连接)
        print('断开连接')
        CONN_LIST.remove(self)
        raise StopConsumer()  # WebSocket DISCONNECT
