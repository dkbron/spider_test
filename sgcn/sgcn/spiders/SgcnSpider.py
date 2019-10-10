# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from sgcn.items import SgcnItem
import re

class SgcnspiderSpider(scrapy.Spider):
    name = 'SgcnSpider'

    def start_requests(self):
        url = ''
        category = getattr(self, 'category', False)
        if category == '美食街':
            url = 'https://bbs.sgcn.com/forum-212-1.html'
        if category == '求职招聘':
            url = 'https://bbs.sgcn.com/forum-1255-1.html'

        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        url_list = response.xpath('//tbody[@id="separatorline"]/./following-sibling::tbody//th/a[2]/@href').getall()
        next_page = LinkExtractor(allow='', restrict_xpaths='//a[@class="nxt"]').extract_links(response)
        if next_page[0].url:
            yield scrapy.Request(next_page[0].url, callback=self.parse)

        for url in url_list:
            yield scrapy.Request(url, callback=self.detail_parse)

    def detail_parse(self, response):
        item = SgcnItem()
        item["name"] = response.xpath('//*[@id="thread_subject"]/text()').get()
        picture = re.findall("<img src='./code.php(.*?)' />", response.text)

        # if not picture:
        #     print(item["name"])
        if picture:
            picture_url = 'https://bbs.sgcn.com/code.php'+picture[0]
            item["image_Path"] = picture_url
            item["type"] = getattr(self, 'category', False)
            print(f'爬取{item["name"]}的电话图片,地址{item["image_Path"]}')
            yield item
        else:
            print(f'{item["name"]}的电话图片不存在')




