# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 11:05:35 2020

@author: Administrator
"""


stuInfo=[]
def main():
    while True:
        printMenu()  #打印菜单
        key=int(input('请输入功能对应的数字：'))
        if key==1:
            addInfo() #添加学生信息
        elif key==2:
            delInfo() #删除学生信息
        elif key==3:
            xiugai() #修改学生信息
        elif key==4:
            showInfo() #查看学生所有信息
        elif key==5:   #退出系统
            quit=input('真的要退出吗？（Y or N）：')
            if quit=='Y':
                break   #结束循环
            else:
                print('输入有误，请重新输入')
                
#打印功能提示         
def printMenu():
    print('='*30)
    print('学生信息管理系统')
    print('1.添加学生信息')
    print('2.删除学生信息')
    print('3.修改学生信息')
    print('4.显示所有学生信息')
    print('5.退出系统')
    print('='*30)
    
#添加学生信息  
def addInfo():
    newname=input('输入学生的名字:')
    newsex=input('输入学生的性别:')
    newphone=input('输入学生手机号:')
    newInfo={}
    newInfo['name']=newname
    newInfo['sex']=newsex
    newInfo['phone']=newphone
    stuInfo.append(newInfo)
    
#删除学生信息
def delInfo():
    delNum=int(input('请输入要删除的序号：'))-1
    del stuInfo[delNum]
    
#修改学生信息
def xiugai():
    stuId=int(input('请输入要修改的学生序号：'))-1
    newname=input('输入修改后学生的名字:')
    newsex=input('输入修改后学生的性别:')
    newphone=input('输入修改后学生的号码:')
    stuInfo[stuId]['name']=newname
    stuInfo[stuId]['sex']=newsex
    stuInfo[stuId]['phone']=newphone
 
#显示所有学生信息
def showInfo():
    print('='*30)
    print('学生信息如下：')
    print('='*30)
    i=1
    for tempInfo in stuInfo:
        print('%d  %s  %s  %s'%(i,tempInfo['name'],tempInfo['sex'],tempInfo['phone']))
        i+=1
    
main()