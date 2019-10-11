# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import os
from aip import AipOcr
import pymysql

class SgcnPipeline(object):
    def __init__(self):
        self.connection = pymysql.connect(host='127.0.0.1',
                                  port=3306,
                                  database='sgcn',
                                  user='dkborn',
                                  password='ddk123',
                                  charset='utf8',
                                  )
        self.cursor = self.connection.cursor()

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
        try:
            i = open(picfile, 'rb')
            img = i.read()
            message = client.basicGeneral(img)  # 通用文字识别，每天 50 000 次免费
            if message:
                info = message.get('words_result')[0]["words"]
                print('识别图片：' + filename + '该图片电话为：' + info)
                self.save_in_mysql(name, info)
            i.close()
        except:
            print('无此图片')

    def save_in_mysql(self, name, info):
        sql = "insert into info(sinfo, sphone) values('%s','%s');" % (name, info)
        # print(sql)
        try:
            self.cursor.execute(sql)
            print('插入成功')
        except pymysql.err.IntegrityError:
            self.connection.rollback()
        except Exception as e:
            print(e)

    def __del__(self):
        self.connection.commit()