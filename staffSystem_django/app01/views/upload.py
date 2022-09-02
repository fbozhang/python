# -*- coding:utf-8 -*-
# @Time : 2022/9/2 0:17
# @Author: fbz
# @File : upload.py
import os

from django.shortcuts import render, HttpResponse
from django import forms

from app01.models import *
from app01.utils.bootstrap import BootStrapForm


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


class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']

    name = forms.CharField(label='姓名')
    age = forms.IntegerField(label='年龄')
    img = forms.FileField(label='头像')


def upload_form(request):
    title = 'Form上传'
    if request.method == 'GET':
        form = UpForm()
        return render(request, "upload_form.html", {'form': form, 'title': title})

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # print(form.cleaned_data)  # {'name': '阿斯顿', 'age': 34, 'img': <InMemoryUploadedFile: cat.jpg (image/jpeg)>}
        # 读取图片内容，写入到文件夹中并获取文件的路径
        image_object = form.cleaned_data.get('img')
        # file_path = "app01/static/img/{}".format(image_object.name)

        # 防止win和mac目录结构不同
        # http://127.0.0.1:8000/static/img/1.jpg 后台访问路径
        db_file_path = os.path.join('static', 'img', image_object.name)
        file_path = os.path.join('app01', db_file_path)  # 实际文件路径 app01\static\img\1.jpg
        # print(file_path)
        f = open(file_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()

        # 将图片文件路径写入到数据库
        Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=db_file_path,
        )
        return HttpResponse('asd')
    return render(request, "upload_form.html", {'form': form, 'title': title})
