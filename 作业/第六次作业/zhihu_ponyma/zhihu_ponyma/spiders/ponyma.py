# -*- coding: utf-8 -*-
import scrapy
import re
import pymysql


class PonymaSpider(scrapy.Spider):
    name = 'ponyma'
    allowed_domains = ['zhihu.com']

    def __init__(self):
        super().__init__()
        self.connection = pymysql.connect(host='127.0.0.1',
                                      port=3306,
                                      database='ponyma_fans',
                                      user='dkborn',
                                      password='ddk123',
                                      charset='utf8',
                                      )
        self.cursor = self.connection.cursor()

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
            self.save_in_mysql(info)

    def save_in_mysql(self, info):
        sql = "insert into info(zid,zname,zimageurl,zurl) values('%s','%s','%s','%s');"%(info[0],info[1],info[2],info[3])
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