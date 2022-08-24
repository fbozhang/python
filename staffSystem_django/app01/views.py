from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from django import forms

from app01.utils.encrypt import md5
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from django.utils.safestring import mark_safe

from app01.models import *


# Create your views here.
def depart_list(request):
    """ 部门列表 """
    queryset = Department.objects.all()

    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,  # 分页数据
        'page_string': page_object.html(),  # 页码
    }

    return render(request, "depart_list.html", context)


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

    page_object = Pagination(request, quertset, page_size=2)

    context = {
        'queryset': page_object.page_queryset,  # 分页数据
        'page_string': page_object.html(),  # 页码
    }

    return render(request, "user_list.html", context)


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
# from django import forms
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


def user_edit(request, nid):
    """ 编辑用户 """

    # 根据id去数据库获取要编辑的那一行数据(对象)
    row_object = UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})

    else:
        form = UserModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            # 默认保存的是用户输入的所有数值，如果想要用户输入以外增加一点值
            # form.instance.字段名 = 默认值(form.instance.name = '阿斯顿')
            form.save()
            return redirect('/user/list/')
        return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    UserInfo.objects.filter(id=nid).delete()

    return redirect('/user/list/')


def pretty_list(request):
    """ 靓号列表 """

    '''
    Prettynum.objects.filter(id=5)  # 等于5
    Prettynum.objects.filter(id__gt=5)  # 大于5
    Prettynum.objects.filter(id__gte=5)  # 大于等于5
    Prettynum.objects.filter(id__lt=5)  # 小于5
    Prettynum.objects.filter(id__lte=5)  # 小于等于5

    data_dict = {'id__lte': 5}
    Prettynum.objects.filter(**data_dict)

    Prettynum.objects.filter(mobile='123')  # 等于123
    Prettynum.objects.filter(mobile__startswith='123')  # 筛选出以123开头
    Prettynum.objects.filter(mobile__endswith='123')  # 筛选出以123结尾
    Prettynum.objects.filter(mobile__contains='123')  # 筛选出包含123

    data_dict = {'mobile__contains': 123}
    Prettynum.objects.filter(**data_dict)
    '''

    # 搜索
    data_dict = {}
    value = request.GET.get('query', '')
    if value:
        data_dict['mobile__contains'] = value

    # 根据搜索条件去数据库获取
    queryset = Prettynum.objects.filter(**data_dict).order_by('-level')
    # 根据用户想要访问的页码计算出起止位置，默认是1
    # page = int(request.GET.get('page', 1))
    # page_size = 10
    # start = (page - 1) * page_size
    # end = page * page_size
    # queryset = Prettynum.objects.filter(**data_dict).order_by('-level')[start:end]
    page_object = Pagination(request, queryset)

    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    # 数据总条数
    # total_count = Prettynum.objects.filter(**data_dict).order_by('-level').count()
    #
    # # 总页码
    # total_page_count, div = divmod(total_count, page_size)  # divmod(67,10) -> (6,7) -> (商，余数)
    # if div:
    #     total_page_count += 1

    # # 显示当前页的前5页后5页
    # plus = 5
    # if total_page_count <= 2 * plus + 1:
    #     # 数据库数据较少，没有达到11页
    #     start_page = 1
    #     end_page = total_page_count
    # else:
    #     # 数据库中数据大于11页
    #     if page <= plus:
    #         # 当前页<5(极小值)
    #         start_page = 1
    #         end_page = 2 * plus + 1
    #     else:
    #         # 当前页 > 5
    #         if (page + plus) > total_page_count:
    #             start_page = total_page_count - 2 * plus
    #             end_page = total_page_count
    #         else:
    #             start_page = page - plus
    #             end_page = page + plus
    #
    # # 页码
    # '''
    # <li><a href="?page=1">1</a></li>
    # <li><a href="?page=2">2</a></li>
    # <li><a href="?page=3">3</a></li>
    # '''
    #
    # page_list = []
    #
    # # 首页
    # page_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    #
    # # 上一页
    # if page > 1:
    #     prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    # else:
    #     prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    # page_list.append(prev)
    #
    # # 页面
    # for i in range(start_page, end_page + 1):
    #     if i == page:
    #         element = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
    #     else:
    #         element = '<li><a href="?page={}">{}</a></li>'.format(i, i)
    #     page_list.append(element)
    #
    # # 下一页
    # if page < total_page_count:
    #     prev = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    # else:
    #     prev = '<li><a href="?page={}">下一页</a></li>'.format(total_page_count)
    # page_list.append(prev)
    #
    # # 尾页
    # page_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page_count))
    #
    # search_string = """
    # <li>
    #     <form style="float: left;margin-left: -1px" method="get">
    #         <input type="text"
    #                style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;"
    #                name="page" class="form-control" placeholder="页码">
    #         <span class="input-group-btn">
    #             <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
    #         </span>
    #     </form>
    # </li>
    # """
    # page_list.append(search_string)
    #
    # page_string = mark_safe(''.join(page_list))  # 标记为安全的才可以在前端显示为标签

    # select * from prettynum by level desc
    # queryset = Prettynum.objects.all().order_by('-level')
    context = {
        'queryset': page_queryset,  # 分页数据
        'value': value,
        'page_string': page_string  # 页码
    }
    return render(request, 'pretty_list.html', context)


# from django.core.validators import RegexValidator
# from django.core.exceptions import ValidationError
class PrettyModelForm(forms.ModelForm):
    # 验证: 方式1 (字段+正则)
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1\d{10}', '手机号为1开头的11位数字')]
    # )

    class Meta:
        model = Prettynum
        # fields = '__all__'  # 所有字段
        # exclude = ['level'] # 排除字段
        fields = ['mobile', 'price', 'level', 'status']  # 自定义字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有插件，添加class="form-control"
        for name, field in self.fields.items():
            # if name == "age":
            #     continue
            # print(name, field)
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 验证: 方式2 (钩子方法:clean_字段名)
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']  # 获取用户传入的数据

        exists = Prettynum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号已存在')

        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError('格式错误')

        # 验证通过：用户输入的值返回
        return txt_mobile


def pretty_add(request):
    """ 靓号添加 """

    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})

    # 用户POST提交数据,数据校验
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {'form': form})


class PrettyEditModelForm(forms.ModelForm):
    # mobile = forms.CharField(label="手机号", disabled=True)  # 不可编辑
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1\d{10}', '手机号为1开头的11位数字')]
    )

    class Meta:
        model = Prettynum
        fields = ['mobile', 'price', 'level', 'status']  # 自定义字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有插件，添加class="form-control"
        for name, field in self.fields.items():
            # if name == "age":
            #     continue
            # print(name, field)
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']  # 获取用户传入的数据

        # 排除id等于自己的手机号已存在
        exists = Prettynum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号已存在')

        # 验证通过返回用户输入
        return txt_mobile


def pretty_edit(request, nid):
    """ 靓号编辑 """
    row_object = Prettynum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {"form": form})

    else:
        form = PrettyEditModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('/pretty/list/')
        return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):
    """ 靓号删除 """
    Prettynum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')


def admin_list(request):
    """ 管理员列表 """

    # 构造搜索
    data_dict = {}
    value = request.GET.get('query', '')
    if value:
        data_dict['username__contains'] = value

    # 根据搜索条件去数据库获取
    queryset = Admin.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'value': value,
    }

    return render(request, 'admin_list.html', context)


# from app01.utils.bootstrap import BootStrapModelForm
class AdminModeForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = Admin
        fields = ["username", 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),  # render_value=True密码输入错误不会清空输入框
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)

    def clean_confirm_password(self):
        # print(self.cleaned_data)  # {'username': '阿瑟东', 'password': '13', 'confirm_password': '321'}
        password = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != password:
            raise ValidationError("密码不一致")

        # 返回此字段保存到数据库（数据库有此字段） -> 放在了cleaned_data里面
        return confirm


def admin_add(request):
    """ 添加管理员 """

    title = '新建管理员'

    if request.method == 'GET':
        form = AdminModeForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminModeForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)    # {'username': '阿瑟东', 'password': '13', 'confirm_password': '321'}
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {'form': form, 'title': title})


class AdminEditModeForm(BootStrapModelForm):
    class Meta:
        model = Admin
        fields = ['username']


def admin_edit(request, nid):
    """ 编辑管理员 """

    title = '编辑管理员'

    row_object = Admin.objects.filter(id=nid).first()
    if not row_object:
        msg = '数据不存在'
        return render(request, 'error.html', {'msg': msg})

    if request.method == "GET":
        form = AdminEditModeForm(instance=row_object)
        return render(request, "change.html", {"form": form})
    else:
        form = AdminEditModeForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')
        return render(request, 'change.html', {'form': form, 'title': title})
