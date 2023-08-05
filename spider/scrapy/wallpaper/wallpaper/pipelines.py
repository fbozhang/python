# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from redis import Redis
import json

from scrapy.pipelines.images import ImagesPipeline
import scrapy


class WallpaperPipeline:
    def process_item(self, item, spider):
        print('收到数据', item)
        res = self.redis.sadd('wallpaper:detail:item', json.dumps(dict(item)))  # 抓取完了就存redis，免得重复抓取
        if res:
            print('存入数据库')
        else:
            print('数据已存在在数据库中')
        return item

    def open_spider(self, spider):
        self.redis = Redis(host='127.0.0.1', port=6379, db=5)

    def close_spider(self, spider):
        self.redis.close()


class ImgPipeline(ImagesPipeline):  # 利用图片管道帮我们完成数据下载操作
    # 想要使用ImagesPipeline 必须要单独设置一个配置，用来保存文件的文件夹
    def get_media_requests(self, item, info):  # 负责下载的
        img_url = item['img']
        yield scrapy.Request(img_url)  # 直接返回一个请求即可

    def file_path(self, request, response=None, info=None, *, item=None):  # 准备文件路径
        file_name = request.url.split('/')[-1]  # request.url可以获取到刚刚请求的url
        return f'{file_name}'

    def item_completed(self, results, item, info):  # 返回文件的详细信息
        return item
