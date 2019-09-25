# -*- coding: utf-8 -*-
import scrapy
import re
import csv


class PonymaSpider(scrapy.Spider):
    name = 'ponyma_csv'
    allowed_domains = ['zhihu.com']

    def __init__(self):
        super().__init__()
        with open('./pony_fans_info.csv', 'w', newline='', encoding='utf-8') as f:
            spawriter = csv.writer(f)
            spawriter.writerow(['id', '姓名', '头像地址', '知乎地址'])

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }
        for n in range(0, 200, 20):
            url = f'https://www.zhihu.com/api/v4/members/ponyma/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={n}&limit=20'
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        info_list = re.findall('"id":"(.*?)",.*?"name":"(.*?)".*?"avatar_url":"(.*?)".*?"url":"(.*?)"',response.text)
        for info in info_list:
            self.save_as_csv(info)

    def save_as_csv(self, info):
        with open('./pony_fans_info.csv', 'a', newline='', encoding='utf-8') as f:
            spawriter = csv.writer(f)
            spawriter.writerow(info)




