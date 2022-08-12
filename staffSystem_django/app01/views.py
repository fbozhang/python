from django.shortcuts import render, redirect
from app01.models import *


# Create your views here.
def depart_list(request):
    """ 部门列表 """
    queryset = Department.objects.all()

    return render(request, "depart_list.html", {"queryset": queryset})


def depart_add(request):
    """ 添加部门 """
    if request.method == "GET":
        return render(request, "depart_add.html")

    # 获取用户post提交过来的数据
    title = request.POST.get("title")

    # 保存到数据库
    Department.objects.create(title=title)

    # 重定向回部门列表
    return redirect("/depart/list/")


def depart_delete(request):
    """ 删除部门 """
    # 获取ID
    nid = request.GET.get('nid')
    # 删除
    Department.objects.filter(id=nid).delete()

    # 重定向回部门列表
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """ 修改部门 """
    if request.method == 'GET':
        # 根据nid获取数据[obj,]
        row_object = Department.objects.filter(id=nid).first()

        return render(request, "depart_edit.html", {'row_object': row_object})

    # 获取用户提交的标题
    title = request.POST.get('title')
    # 根据id找到数据库中数据更新
    Department.objects.filter(id=nid).update(title=title)

    # 重定向回部门列表
    return redirect("/depart/list/")


def user_list(request):
    """ 用户管理 """

    # 获取所有用户列表
    quertset = UserInfo.objects.all()

    """
    for obj in quertset:
        print(obj.name, obj.create_time, type(obj.create_time))
        print(obj.create_time.strftime("%Y-%m-%d"), type(obj.create_time.strftime("%Y-%m-%d")))
        print(obj.gender, obj.get_gender_display()) # get_字段名_display()得到choices的值

        # title = Department.objects.filter(id=obj.depart_id).first().title
        # print(title)
        # obj.depart_id   # 获取数据库中存储的那个字段值
        # obj.depart  # 根据id自动去关联的表中获取那一行数据的depart对象
        print(obj.depart.title)
        """

    return render(request, "user_list.html", {'quertset': quertset})