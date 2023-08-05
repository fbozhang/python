import scrapy
from scrapy.http.response import Response
from wallpaper.items import WallpaperItem
from redis import Redis


class PicSpider(scrapy.Spider):
    name = "pic"
    allowed_domains = ["pic.netbian.com"]
    start_urls = ["https://pic.netbian.com"]

    def __init__(self, name=None, **kwargs):
        super(PicSpider, self).__init__(name, **kwargs)
        self.redis = Redis(host='127.0.0.1', port=6379, db=5)

    def parse(self, response: Response, **kwargs):
        li_list = response.xpath('//ul[@class="clearfix"]/li')[:-1]
        for li in li_list:
            href = li.xpath('./a/@href').extract_first()
            detail_url = response.urljoin(href)
            # 数据去重
            # 1. url，优点: 简单，缺点: 如果url会更新可能造成重复
            # 判断redis里有没有这个url，只有redis里面没有url才访问详情页，防止重复抓取
            # 2. 判断数据是否重复，优点: 保证数据的一致性，缺点: 数据量大的时候，效率低，对redis不利因为redis本质在内存(在pipelines中写)
            result = self.redis.sismember('wallpaper:detail:url', detail_url)
            if result:
                print(f'该详情页已经被抓取过了{detail_url}')  # 不管他就完事了
            else:
                yield scrapy.Request(detail_url, callback=self.parse_detail)

        # next_url = response.xpath('//div[@class="page"]/a[last()]/@href').extract_first()
        next_url = response.xpath('//div[@class="page"]/a[contains(text(),"下一页")]/@href').extract_first()
        next_url = response.urljoin(next_url)
        yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail(self, response: Response, **kwargs):
        w = WallpaperItem()
        src = response.xpath('//a[@id="img"]/img/@src').extract_first()
        img = response.urljoin(src)
        w['img'] = img
        self.redis.sadd('wallpaper:detail:url', response.url)  # 抓取完了就存redis，免得重复抓取
        yield w
