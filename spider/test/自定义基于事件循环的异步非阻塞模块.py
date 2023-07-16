# -*- coding:utf-8 -*-
# @Time : 2023/7/16 16:59
# @Author: fbz
# @File : 事件循环.py
import socket
import select  # IO多路复用
"""
- 什么是异步?
    其实就是回调，当一个任务完成后自动执行某个函数。
- 什么是非阻塞?
    其实就是不等待，socket中如果设置setblocing(False)那么就不阻塞
- IO多路复用的作用?
    监听socket的状态:
        - 是否连接成功
        - 是否获取结果
    IO多路复用的实现:
        - select: 只能监听1024个socket；内部会循环所有的socket去检测(windows仅支持这个)
        - poll: 无个数限制，内部会循环所有的socket去检测
        - epoll: 无个数限制，回调(不用循环，性能更好,linux一般用这个)
"""

class Test(object):

    def __init__(self):
        self.socket_list = []
        self.conn_list = []
        self.conn_func_dict = {}

    def add_request(self, url_func):
        conn = socket.socket()
        conn.setblocking(False)  # 非阻塞
        try:
            conn.connect((url_func[0], 80))
        except BlockingIOError as e:
            pass
        self.conn_func_dict[conn] = url_func[1]

        self.socket_list.append(conn)
        self.conn_list.append(conn)

    def run(self):
        """ 检测self.socket_list中的socket对象是否连接成功 """
        while True:
            # IO多路复用
            # r:具体哪个socket获取到结果, w:具体哪个socketli j连接成功
            r, w, e = select.select(
                self.socket_list,  # 用于检测其中socket是否获取到响应内容
                self.conn_list,  # 用于检测其中socket是否已经连接成功
                [],  # 用来检测是否发生错误
                0.05)  # hold住0.05s
            for sock in w:  # [socket1, socket2]
                sock.send(b'GET / http1.1\r\nhost:xxx.com\r\n\r\n')
                self.conn_list.remove(sock)

            for sock in r:
                data = sock.recv(8096)
                # print(data)
                func = self.conn_func_dict[sock]
                func(data)
                sock.close()
                self.socket_list.remove(sock)

            if not self.socket_list:
                break


def callback1(data):
    print(data)


def callback2(data):
    print(data)


asd = Test()
urls = [
    ('www.baidu.com', callback1),
    ('www.cnblogs.com', callback1),
    ('www.pythonav.com', callback2),
    ('www.bing.com', callback2),
    ('www.stackoverflow.com', callback2),
]
for url in urls:
    asd.add_request(url)

asd.run()
