# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 10:47:13 2020

@author: Administrator
"""


def meun():
    menu_info = '''
 １添加学生信息                           
 ２显示所有学生的信息                     
 ３删除学生信息                           
 ４修改学生信息                           
  0退出：其他任意按键＜回车＞                 

'''
    print(menu_info)


# 以下二个函数用于sorted排序，　key的表达式函数
def get_age(*l):
    for x in l:
        return x.get("age")


def get_score(*l):
    for x in l:
        return x.get("score")


# １）添加学生信息
def add_student_info():
    L = []
    while True:
        n = input("请输入姓名：")
        if not n:  # 名字为空　跳出循环
            break
        try:
            a = input("请输入性别：")
            s = int(input("请输入手机号："))
        except:
            print("输入无效，不是整形数值．．．．重新录入信息")
            continue
        info = {"name": n, "age": a, "score": s}
        L.append(info)
    print("学生信息录入完毕！！！")
    return L


# ２）显示所有学生的信息
def show_student_info(student_info):
    if not student_info:
        print("无数据信息．．．．．")
        return
    print("名字".center(8), "性别".center(4), "手机号".center(4))
    for info in student_info:
        print(info.get("name").center(10), str(info.get("age")).center(4), str(info.get("score")).center(4))


# ３）删除学生信息
def del_student_info(student_info, del_name=''):
    if not del_name:
        del_name = input("请输入删除的学生姓名：")
    for info in student_info:
        if del_name == info.get("name"):
            return info
    raise IndexError("学生信息不匹配,没有找到%s" % del_name)


# ４）修改学生信息
def mod_student_info(student_info):
    mod_name = input("请输入修改的学生姓名：")
    for info in student_info:
        if mod_name == info.get("name"):
            a = int(input("请输入性别："))
            s = int(input("请输入手机号："))
            info = {"name": mod_name, "age": a, "score": s}
            return info
    raise IndexError("学生信息不匹配,没有找到%s" % mod_name)


def main():
    student_info = []
    while True:
        # print(student_info)
        meun()
        number = input("请输入选项：")
        if number == '1':
            student_info = add_student_info()
        elif number == '2':
            show_student_info(student_info)
        elif number == '3':
            try:
                student_info.remove(del_student_info(student_info))
            except Exception as e:
                # 学生姓名不匹配
                print(e)
        elif number == '4':
            try:
                student = mod_student_info(student_info)
            except Exception as e:
                # 学生姓名不匹配
                print(e)
            else:
                # 首先按照根据输入信息的名字，从列表中删除该生信息，然后重新添加该学生最新信息
                student_info.remove(del_student_info(student_info, del_name=student.get("name")))
                student_info.append(student)

        else:
            break
        input("回车显示菜单")


main()
