"""
采集豆瓣网站电影数据
Author : 陈永康
"""

import requests
import csv
import concurrent.futures
import re
import time
import parsel
import random


class DoubanSpider:
    """豆瓣图书信息爬取"""

    def __init__(self):
        with open('./douban_movie_info.csv', 'w', newline='', encoding='utf-8') as f:
            spawriter = csv.writer(f)
            spawriter.writerow(['电影名称', '电影评分', '评分人数', '电影图片', '剧情简介'])

    # 保存文件为csv格式
    def save_as_csv(self, movie_info_list):
        try:
            with open('./douban_movie_info.csv', 'a', newline='', encoding='utf-8') as f:
                spawriter = csv.writer(f)
                spawriter.writerow(movie_info_list)
        except Exception as e:
            print(e)

    # 获取url的html页面
    def get_html(self, url):
        response = requests.get(url, headers=headers)
        print(response.status_code)
        response.encoding = 'utf-8'
        html = response.text
        return html

    # 分页页面解析
    @staticmethod
    def parsel_html_index(html):
        sel = parsel.Selector(html)
        movie_url_list = sel.xpath('//div[@class="hd"]/a/@href').getall()
        return movie_url_list

    def parsel_html_movie(self, movie_url):
        html = self.get_html(movie_url)
        sel = parsel.Selector(html)
        movie_name = sel.xpath('//h1/span[1]/text()').get()
        movie_picture = sel.xpath('//*[@id="mainpic"]/a/img/@src').get()
        command_grade = sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').get()
        command_num = sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()').get()
        movie_detail = sel.xpath('//span[@class="all hidden"]/text()').get()
        if movie_detail == None:
            movie_detail = sel.xpath('//*[@id="link-report"]/span[1]/text()').get()

        return [movie_name, movie_picture, command_grade, command_num, movie_detail.strip()]

    def main_spder(self, url):
        html = self.get_html(url)
        movie_url_list = self.parsel_html_index(html)
        for movie_url in movie_url_list:
            movie_info_list = self.parsel_html_movie(movie_url)
            print(movie_info_list)
            self.save_as_csv(movie_info_list)
            time.sleep(random.uniform(0, 3))

    def domain(self):
        # 多线程
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # 这里调用了tag_main，即每个分类的爬虫
            executor.map(self.main_spder,
                         [f'https://movie.douban.com/top250?start={num}&filter=' for num in range(0, 250, 25)])
        # for num in range(0, 250, 25):
        #     url = f'https://movie.douban.com/top250?start={num}&filter='
        #     self.main_spder(url)


if __name__ == '__main__':
    # 创建爬虫实例对象
    d = DoubanSpider()
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    }

    # 调用爬虫启动函数
    d.domain()
