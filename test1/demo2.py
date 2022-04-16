# -*- coding:utf-8 -*-
# @Time : 2022/3/17 14:07
# @Author: fbz
# @File : demo2.py

# 鍵盤輸入值
n=int(input("輸入幾行:"))
line=[[]]*n
for i in range(n):
    line[i]=input("輸入第%d個列表的元素以空格分割："%(i+1)).split(' ')

print(line)

for i in line:
    for j in i:
        print(j,end='\t')
    print()

m = int(input("輸入幾行:"))
grid = [[]for i in range(m)]
for i in range(m):
    line = input("輸入第%d個列表的元素以空格分割："%(i+1)).split(' ')
    for j in range(len(line)):
        grid[i].append(line[j])
print(grid)

