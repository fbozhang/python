import scrapy
from scrapy.http.response import Response

from douban.items import DoubanItem


class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response: Response, **kwargs):
        div_list = response.xpath('//div[@class="item"]')
        item = DoubanItem()
        for div in div_list:
            item['img'] = div.xpath('./div[@class="pic"]/a/img/@src').extract_first()
            item['name'] = div.xpath('./div[@class="info"]/div[@class="hd"]/a/span/text()').extract_first()
            item['score'] = div.xpath(
                './div[@class="info"]/div[@class="bd"]//span[@class="rating_num"]/text()').extract_first()
            yield item

        url = response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').extract_first()
        if url is not None:
            yield scrapy.Request(response.urljoin(url), callback=self.parse)
