import json
import os

import requests
import re

import xlwt

url = 'https://s.taobao.com/search'


def main(url):
    # 爬取网页保存本地,如果本地存在这个文件则不爬取
    if os.path.exists("./goods.html"):  # 判断html文件是存在不需要爬取，直接解析
        data_list = getData()
        saveDataXls(data_list=data_list,savepath='goods.xls')
    else:
        saveHTML(url)
        getData()


# 得到html并保存到本地
def saveHTML(url):
    headers = {
        'referer': 'https://s.taobao.com/',
        'cookie': 'thw=cn; t=8ef5948506d609509b897ac412767013; _m_h5_tk=9205a93d94f5b54d1a54922316af5aec_1662141389697; _m_h5_tk_enc=123f20d72912e0d20050d22d851d8ded; xlly_s=1; sgcookie=E100VDChATh+YF/a5XZOqc/BDeRr4gZUQX3rSgAEw4oXUXy2Udy8tx1wWWjzhOBc/o5mIX4q+764oyt17cpgqibtwwGhuHYUNQEZnCSu3MmKt9E=; enc=zXYf7Jlko8azrQNhGjxvP5EAtmWVddVyyqtVqVP3Q+GwDN0FgLr5ApX0nh+rp1QDzOoRksm7x6Nza71uDm7DuwP6k/fK8WsdWvhHxCH+oNE=; mt=ci=0_0; tracknick=; cna=vRwmGkmxuHkCATr4wRnOiqN+; JSESSIONID=9B7785091EB056DD2E6716832A8F77DC; isg=BNXVAmsvGgeRwDyI_Zg3NlHW5NGP0onkq9AEMld6g8ybrvWgKiCutOZnfLIYrqGc; l=eBPGHwblg9rbzAbTBOfZnurza779QIRAguPzaNbMiOCP9vCp53qfW6k0GPY9CnGVh6py635Wn1oBBeYBqHKKnxv92j-la1Hmn; tfstk=cC5VB7Db2SF22SWFUQONasojdodAZLbcSb8BnkQAdETZappciim9rnTvzFgrjKf..',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }

    param = {
        'spm': ' a21bo.jianhua.201856-fline.5.5af911d9YaRmCw',
        'q': ' 短裤',
        'refpid': ' 430145_1006',
        'source': ' tbsy',
        'style': ' grid',
        'tab': ' all',
        'pvid': ' d0f2ec2810bcec0d5a16d5283ce59f69',
    }

    resp = requests.get(url=url, params=param, headers=headers)
    # print(resp.request.url)
    # print(resp.text)
    f = open("goods.html", mode="w", encoding="utf-8")
    f.write(resp.text)
    f.close()


# 解析网页得到商品数据
def getData():
    data_list = []
    # 以 utf-8 的编码格式打开指定文件
    f = open("goods.html", encoding="utf-8")
    # 输出读取到的数据
    # print(f.read())

    g_page_config = re.compile(r'g_page_config = (?P<data>[\s\S]*?)g_srp_loadCss', flags=re.S)
    '''# 方法1
    # result = g_page_config.finditer(f.read())
    # for i in result:
    #     data = i.group('data')
    #     print(data)'''

    # 方法2
    all_data = g_page_config.findall(f.read())[0]
    # print(all_data)
    all_data = all_data.split(';\n')[0]
    # print(all_data)
    all_data = json.loads(all_data)  # 将json字符串转为字典

    auctions_list = all_data['mods']['itemlist']['data']['auctions']

    # 逐一解析數據
    for auctions in auctions_list:
        # print(auctions)  # 测试： 查看auctions全部信息
        data = {
            'title': auctions['raw_title'],  # 商品标题
            'pic_url': 'https://' + auctions['pic_url'],  # 预览图地址
            'price': auctions['view_price'],  # 商品价格
            'salesNum': auctions['view_sales'],  # 付款人数
            'region': auctions['item_loc'],  # 产地
            'detail_url': auctions['detail_url'],  # 商品详情链接
            'shop_name': auctions['nick'],  # 店铺名称
            'shopLink': auctions['shopLink'],  # 店铺地址
        }
        data_list.append(data)
    f.close()

    return data_list


# 保存數據到excel
def saveDataXls(data_list, savepath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet("淘宝商品列表", cell_overwrite_ok=True)  # 创建工作表
    col = ["商品标题", "预览图链接", "商品价格", "付款人数", "产地", "商品详情链接", "店铺名称", "店铺地址"]
    for i in range(8):
        sheet.write(0, i, col[i])  # 列名

    # 遍历列表
    row_index = 1
    for data in data_list:
        column_index = 0
        for value in data.values():
            sheet.write(row_index, column_index, value)  # 数据
            column_index += 1
            print('column_index_in=', column_index)
        row_index += 1
        print('row_index=', row_index)
        print('column_index_out=', column_index)

    book.save(savepath)  # 保存数据表


if __name__ == '__main__':
    main(url=url)
