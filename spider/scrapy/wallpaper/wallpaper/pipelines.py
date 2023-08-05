# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from redis import Redis
import json


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
