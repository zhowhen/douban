# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanmovieSpider(scrapy.Spider):
    name = "doubanmovie"
    allowed_domains = ["douban.com"]
    url = 'https://movie.douban.com/top250?start='
    offset = 0
    start_urls = [url+str(offset), ]

    def parse(self, response):
        # print(response.url)
        part_list = response.xpath('//div[@class="info"]')
        for each in part_list:
            item = DoubanItem()
            item['title'] = each.xpath('.//span[@class="title"][1]/text()').extract_first()
            item['bd'] = ''.join(each.xpath('./div/p[1]/text()').extract()).replace('\xa0', '').\
                replace('\xf4', '').replace(' ', '').strip()
            item['star'] = each.xpath('.//span[@class="rating_num"]/text()').extract_first()
            item['quote'] = each.xpath('.//p[@class="quote"]/span/text()').extract_first()
            yield item
        if self.offset < 225:
            self.offset += 25
            yield scrapy.Request(url=self.url+str(self.offset), callback=self.parse)