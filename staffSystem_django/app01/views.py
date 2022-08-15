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


def user_add(request):
    """ 添加用户(原始方法) """

    if request.method == 'GET':
        context = {
            'gender_choices': UserInfo.gender_choices,
            'depart_list': Department.objects.all(),
        }
        return render(request, "user_add.html", context)

    # 获取用户提交的数据
    name = request.POST.get('name')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # 添加到数据库中
    UserInfo.objects.create(name=name, password=pwd, age=age,
                            account=account, create_time=ctime,
                            gender=gender, depart_id=depart_id)

    # 返回到用户列表
    return redirect("/user/list")


# ModelForm示例
from django import forms


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3, label="用户名")
    # password = forms.CharField(mlabel="密码", validators=) # validators=正则表达式

    class Meta:
        model = UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有插件，添加class="form-control"
        for name, field in self.fields.items():
            # if name == "age":
            #     continue
            # print(name, field)
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_model_form_add(request):
    """ 添加用户(ModelForm版本) """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {'form': form})

    # 用户POST提交数据,数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如歌数据合法，保存到数据库
        # print(form.cleaned_data)    # {'name': '史蒂夫', 'password': '432'}
        # UserInfo.objects.create(..)
        form.save()
        return redirect('/user/list/')
    else:
        # 校验失败
        # print(form.errors)
        return render(request, 'user_model_form_add.html', {'form': form})
