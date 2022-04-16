# -*- coding:utf-8 -*-
# @Time : 2022/4/16 15:37
# @Author: fbz
# @File : testXpath.py

# xpath 是在XML文档中搜索内容的一门语言
# html是xml的一个子集

from lxml import etree

"""
xml = '''
<book>
    <id>1</id>
    <name>阿斯顿</name>
    <a>自行车</a>
    <b>
        <a>大厦4</a>
        <a>大厦5</a>
        <a>大厦6</a>
    </b>
    <div>
        <a>大厦1</a>
        <a>大厦2</a>
        <a>大厦3</a>
    </div>
</book>
'''

tree = etree.XML(xml)
# result = tree.xpath("/book")    # /表示层级关系，第一个是根节点
# result = tree.xpath("/book/name/text()") # text()拿到文本
# result = tree.xpath("/book//a/text()")  # //后代,例如：book后有a的后代
result = tree.xpath("/book/*/a/text()") # * 任意的节点,通配符。例如：任意节点的后代a

print(result)"""


tree = etree.parse("temp.html")
# result = tree.xpath("/html/body/ul/li/a/text()")
# result = tree.xpath("/html/body/ul/li[1]/a/text()")     # xpath的顺序是从1开始数的,[]表示索引
# result = tree.xpath("/html/body/ol/li/a[@href='zxc']/text()")   # [@xxx=xxx] 属性的筛选
# result = tree.xpath("/html/body/ol/li/a/@href")     # 拿到属性
# print(result)

ol_li_list = tree.xpath("/html/body/ol/li")
for li in ol_li_list:
#     从每一个li中提取到文字信息
    result = li.xpath("./a/text()")  # 在li中继续寻找，相对查找
    print(result)
    result2 = li.xpath("./a/@href") # 拿到属性值：@属性
    print(result2)

