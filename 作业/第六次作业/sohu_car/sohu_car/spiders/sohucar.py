# -*- coding: utf-8 -*-
import scrapy
import re
import csv


class SohucarSpider(scrapy.Spider):
    name = 'sohucar'
    allowed_domains = ['sohu.com']
    start_urls = ['http://db.auto.sohu.com/cxdata/xml/basic/brandList.xml']

    def __init__(self):
        super().__init__()
        with open('./sohu_carsales_info.csv', 'w', newline='', encoding='utf-8') as f:
            spawriter = csv.writer(f)
            spawriter.writerow(['品牌', '车型', '日期', '销售量'])

    def parse(self, response):
        # print(response.text)
        id_list = re.findall('id="(\d*)"', response.text)
        for id in id_list:
            url = f'http://db.auto.sohu.com/cxdata/xml/basic/brand{id}ModelListWithCorp.xml'
            yield scrapy.Request(url, callback=self.parseCarId)

    def parseCarId(self, response):
        car_name = response.xpath('//brand/@name').extract()[0]
        car_type_id_list = response.xpath('//model/@id').extract()
        for car_type_id in car_type_id_list:
            url = f'http://db.auto.sohu.com/cxdata/xml/sales/model/model{car_type_id}sales.xml'
            yield scrapy.Request(url, meta={'car_name': car_name}, callback=self.parseTypeId)

    def parseTypeId(self, response):
        car_name = response.meta['car_name']
        car_type = response.xpath('//model/@name').extract()[0]
        car_sales_xpath_list = response.xpath('//sales')
        for car_sales_xpath in car_sales_xpath_list:
            date = car_sales_xpath.xpath('./@date').extract()[0]
            salesNum = car_sales_xpath.xpath('./@salesNum').extract()[0]
            self.save_as_csv([car_name, car_type, date, salesNum])

    # 保存文件为csv格式
    def save_as_csv(self, carsales_info_list):
        try:
            with open('./sohu_carsales_info.csv', 'a', newline='', encoding='utf-8') as f:
                spawriter = csv.writer(f)
                spawriter.writerow(carsales_info_list)
            print(f'保存品牌{carsales_info_list[0]}车型{carsales_info_list[1]}于{carsales_info_list[2]}的信息成功')
        except Exception as e:
            print(f'保存品牌{carsales_info_list[0]}车型{carsales_info_list[1]}于{carsales_info_list[2]}的信息失败')
            print(e)
