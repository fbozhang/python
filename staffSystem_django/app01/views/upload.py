# -*- coding:utf-8 -*-
# @Time : 2022/9/2 0:17
# @Author: fbz
# @File : upload.py
from django.shortcuts import render, HttpResponse


def upload_list(request):
    if request.method == 'GET':
        return render(request, "upload_list.html")

    # print(request.POST)  # 请求体中的数据
    # print(request.FILES)  # 请求发过来的文件{}
    file_object = request.FILES.get('avatar')
    # print(file_object.name)  # 文件名: 123.png

    f = open(file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()

    return HttpResponse("asd")
