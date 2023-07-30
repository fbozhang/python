# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# 管道默认是不生效的，需要取settings里面开启管道!!!
class Game4399Pipeline:
    def process_item(self, item, spider):  # 处理数据的专用方法，item:数据，spider是爬虫
        print(item)
        return item  # 给下一个管道(必须要return东西，不然下一个管道收不到数据)


class NewPipeline:
    def process_item(self, item, spider):  # 处理数据的专用方法，item:数据，spider是爬虫
        item['test'] = '先走了'  # 先走了这个，process_item就会得到这个数据
        return item  # 给下一个管道(必须要return东西，不然下一个管道收不到数据)
