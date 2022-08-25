# -*- coding:utf-8 -*-
# @Time : 2022/8/25 20:42
# @Author: fbz
# @File : pretty.py
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from django import forms

from app01.utils.encrypt import md5
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from django.utils.safestring import mark_safe

from app01.models import *


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
