import scrapy
from scrapy.http.response import Response
from wallpaper.items import WallpaperItem
from redis import Redis
from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider


class PicSpider(RedisSpider):  # 换成RedisSpider
    name = "pic"
    allowed_domains = ["pic.netbian.com"]
    # start_urls = ["https://pic.netbian.com"] # 换成redis_key
    redis_key = 'pic_start_url'

    def parse(self, response: Response, **kwargs):
        li_list = response.xpath('//ul[@class="clearfix"]/li')[:-1]
        for li in li_list:
            href = li.xpath('./a/@href').extract_first()
            detail_url = response.urljoin(href)
            # RedisSpider自动去重，不用光是否重复，所有判断工作交给scrapy_redis完成
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
        yield w
