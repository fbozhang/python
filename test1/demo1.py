# -*- coding:utf-8 -*-
# @Time : 2022/3/16 21:24
# @Author: fbz
# @File : demo1.py

products = [["ipone",6888],["MacPro",14800],["小米6",2499],["Coffee",31],["Book",60],["Nike",699]]
print("-"*6 + "商品列表" + "-"*6)
print("編號\t商品\t\t單價")
for i in range(len(products)):
    print(i, end='\t')
    for j in range(len(products[i])):
        print(products[i][j],end='\t')
    print()
# 問用戶商品編號，把商品加入購物車，輸入q退出，打印購買列表

shoppingCart = []
flag = 1
while flag:
    buy = input("請輸入商品編號:")
    if(buy == 'q'):
        print("結束購物")
        flag = 0
    else:
        shoppingCart.append(products[int(buy)])

print("-"*6 + "購買列表" + "-"*6)
#下標遍歷
'''
for i in range(len(shoppingCart)):
    print(products.index(shoppingCart[i]), end='\t')
    for j in range(len(shoppingCart[i])):
        print(shoppingCart[i][j],end='\t')
    print()
'''
# 直接遍歷
for i in shoppingCart:
    print(products.index(i),end='\t')
    for j in i:
        print(j,end='\t')
    print()

print("-"*20)
for i in shoppingCart:
    print("{qwe}\t{asd}\t\t{da}".format(qwe = products.index(i),asd=i[0],da=i[1]))

# for i in shoppingCart:
#     print(i[1]*shoppingCart.count(i))
#     shoppingCart.remove(i)
#     del i

