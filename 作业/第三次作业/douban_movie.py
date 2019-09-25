"""
采集豆瓣网站电影数据
Author : 陈永康
"""


import requests
import csv
import concurrent.futures
import re
import time
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
                # movie_info_list[0][4].strip().replace('<br />', '').replace('\n', '').replace(" ", '')
                movie_detail = movie_info_list[0][4].strip().replace('<br />', '').replace('\n', '').replace(" ", '')
                spawriter.writerow([movie_info_list[0][0], movie_info_list[0][2], movie_info_list[0][3], movie_info_list[0][1], movie_detail])
            print(f'保存电影{movie_info_list[0][0]}信息成功')
        except Exception as e:
            print(f'保存电影{movie_info_list[0][0]}信息失败')
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
    def re_html_index(html):
        re_rule = '<div class="hd">.*?<a href="(.*?)" class="">.*?</a>'
        movie_url_list = re.findall(re_rule, html, re.S)
        return movie_url_list

    def re_html_movie(self, movie_url):
        html = self.get_html(movie_url)
        re_rule = '<h1>.*?<span property="v:itemreviewed">(.*?)</span>.*?</h1>.*?' \
                  '<img src="(.*?)".*?' \
                  '<strong class="ll rating_num" property="v:average">(.*?)</strong>.*?' \
                  '<span property="v:votes">(.*?)</span>.*?' \
                  '<span property="v:summary".*?>(.*?)</span>'
        movie_info = re.findall(re_rule, html, re.S)
        return movie_info

    def main_spder(self, url):
        html = self.get_html(url)
        movie_url_list = self.re_html_index(html)
        for movie_url in movie_url_list:
            movie_info_list = self.re_html_movie(movie_url)
            self.save_as_csv(movie_info_list)
            time.sleep(random.uniform(0, 3))

    def domain(self):
        # 多线程
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # 这里调用了tag_main，即每个分类的爬虫
            executor.map(self.main_spder, [f'https://movie.douban.com/top250?start={num}&filter=' for num in range(0, 250, 25)])


if __name__ == '__main__':
    # 创建爬虫实例对象
    d = DoubanSpider()
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    }

    # 调用爬虫启动函数
    d.domain()
