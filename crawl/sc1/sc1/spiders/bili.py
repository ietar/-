# -*- coding: utf-8 -*-
import scrapy
from sc1.items import Sc1Item


class BiliSpider(scrapy.Spider):
    name = 'bili'
    allowed_domains = ['www.bilibili.com']
    start_urls = ['https://www.bilibili.com/ranking']

    def parse(self, response):
        items = response.css('li.rank-item')
        for i in items:
            item = Sc1Item()
            item['num'] = i.css('div.num').css('::text').extract()[0]
            item['title'] = i.css('div.content').css('div.info').css('a.title').css('::text').extract()[0].strip()
            item['author'] = i.css('div.content').css('div.info').css('div.detail').css('a').css('::text').extract()[0]
            yield item
