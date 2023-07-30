import scrapy
from scrapy.http.response import Response


class SmallGameSpider(scrapy.Spider):
    name = "small_game"  # 爬虫名字
    allowed_domains = ["4399.com"]  # 允许的域名
    start_urls = ["https://www.4399.com/"]  # 起始页面的URL

    def parse(self, response: Response, **kwargs):  # 该方法默认是用来处理解析的
        # 拿到页面源代码
        # print(response.text)
        # 提取数据
        # response.xpath() # 用xpath进行数据解析
        # response.css() # 用css选择器进行数据解析

        # 获取到页面中所有的游戏名字
        # name = response.xpath('//*[@id="skinbody"]/div[10]/div[1]/div[1]/ul/li/a/text()').extract() #提取内容
        # print(name)

        # 分块提取数据
        li_list = response.xpath('//*[@id="skinbody"]/div[10]/div[1]/div[1]/ul/li')
        for li in li_list:
            # name = li.xpath('./a/text()').extract()[0] # 如果列表为空取0会报错
            # extract() 返回列表, extract_first() 返回第一项数据
            name = li.xpath('./a/text()').extract_first()  # extract_first提取一项内容，如果没有返回 None
            img = li.xpath('./a/img/@lz_src').extract_first()

            data_dict = {
                'name': name,
                'img': img,
            }
            # 需要用yield将数据传递给管道, 不是装在列表一次性return使用yield省内存
            yield data_dict  # 如果返回的是数据，直接可以认为是给了管道pipeline(给了引擎，引擎给管道)
