# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import os
from aip import AipOcr
from redis import StrictRedis

class SgcnPipeline(object):
    def __init__(self, redisHost, redisPort, redisDB):
        self.redis = StrictRedis(
            host=redisHost,
            port=redisPort,
            db=redisDB
        )

    @classmethod
    def from_settings(cls, settings):
        redisHost = settings.get('REDISHOST')
        redisPort = settings.get('REDISPORT')
        reidsDB = settings.get('REDISDB1')

        return cls(
            redisHost,
            redisPort,
            reidsDB
        )

    def process_item(self, item, spider):
        picfile = f'E:/{item["type"]}/{item["name"]}.PNG'
        if os.path.exists(f'E:/{item["type"]}') == False:
            os.mkdir(f'E:/{item["type"]}')
        with open(picfile, 'wb') as f:
            f.write(requests.get(item["image_Path"]).content)

        self.baiduOCR(picfile, item["name"])

    def baiduOCR(self, picfile, name):
        APP_ID = '17423159'
        API_KEY = 'wV3204ZDDdQaXxGmk71Gm9Bs'
        SECRECT_KEY = 'udL1WwrA5ySdpBczbPupjzoFD8mb6vA1'
        client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)

        filename = os.path.basename(picfile)
        i = open(picfile, 'rb')
        img = i.read()
        message = client.basicGeneral(img)  # 通用文字识别，每天 50 000 次免费
        info = message.get('words_result')[0]["words"]
        print('识别图片：'+filename+'该图片电话为：'+ info)
        self.redis.sadd(name, info)
        i.close()
