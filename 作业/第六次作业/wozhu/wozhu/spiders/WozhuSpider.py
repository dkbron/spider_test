# -*- coding: utf-8 -*-
import scrapy
import json
import requests


class WozhuspiderSpider(scrapy.Spider):
    name = 'WozhuSpider'
    allowed_domains = ['7799520.com']
    start_urls = [f'http://www.7799520.com/api/user/pc/list/search?marry={marry}&page={n}' for marry in [1, 3, 4] for n in range(1,2)]

    def parse(self, response):
        json_data = json.loads(response.text)
        info = json_data.get('data')
        for info in info['list']:
            # print(info['username']+info['avatar'])
            img_content = requests.get(info['avatar']).content
            username = info['username']
            self.save_as_png(img_content, username)

    @staticmethod
    def save_as_png(img_content, username):
        with open(f'./{username}.png', 'wb') as f:
            f.write(img_content)