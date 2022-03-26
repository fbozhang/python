# -*- coding:utf-8 -*-
# @Time : 2022/3/26 15:37
# @Author: fbz
# @File : testXwt.py

import xlwt

# workbook = xlwt.Workbook(encoding="utf-8")  # 创建workbook对象
# worksheet = workbook.add_sheet("sheet1")  # 创建工作表
# worksheet.write(0, 0, "hello  ")  # 写入数据，第一个参数“行”，第二个参数”列“，第三个参数内容
# workbook.save("test.xls")  # 保存数据表

workbook = xlwt.Workbook(encoding="utf-8")  # 创建workbook对象
worksheet = workbook.add_sheet("sheet1")  # 创建工作表
for i in range(1,10):
    for j in range(1,i+1):
        ride = i*j
        worksheet.write(i-1,j-1,"%d * %d = %d"%(j,i,ride))
workbook.save("test.xls")  # 保存数据表
