"""
采集豆瓣网站书籍数据，采集的数据包含如下：
上市时间
书的价格
书籍评分
内容简介
书籍分类

本爬虫使用了多线程，因为害怕ip被封所以只开了几个，用的ip是自己购买的vpn的IP，爬了1个小时左右，没有被封，数据一万三千左右条
Author : 陈永康
"""


import requests
import parsel
import csv
import concurrent.futures
import re
import time
import random


class DoubanSpider:
    """豆瓣图书信息爬取"""

    def __init__(self):
        with open('./douban_book_info.csv', 'a', newline='', encoding='ANSI') as f:
            spawriter = csv.writer(f)
            spawriter.writerow(['书名', '上市时间', '书的价格', '书籍评分', '内容简介', '书籍分类'])

    # 保存文件为csv格式
    def save_as_csv(self, book_info_dic):
        with open('./douban_book_info.csv', 'a', newline='', encoding='ANSI') as f:
            spawriter = csv.writer(f)
            spawriter.writerow([book_info_dic['书名'], book_info_dic['上市时间'],
                                book_info_dic['书的价格'], book_info_dic['书籍评分'], book_info_dic['内容简介'],
                                book_info_dic['书籍分类']])

    # 获取url的html页面
    @staticmethod
    def get_html(url):
        response = requests.get(url, headers=headers)
        print(response.status_code)
        response.encoding = 'utf-8'
        html = response.text
        return html

    # 主页面解析
    @staticmethod
    def parsel_html_index(html):
        sel = parsel.Selector(html)
        book_tag_list_ = []
        book_tag_list = sel.xpath('//table[@class="tagCol"]//td')
        for book_tag in book_tag_list:
            book_tag_name = book_tag.xpath('./a/text()').get()
            book_tag_url = 'https://book.douban.com' + book_tag.xpath('./a/@href').get()
            book_tag_list_.append({'标签名': book_tag_name, '路径': book_tag_url})
        return book_tag_list_

    # 解析每本书的信息
    def parsel_book(self, book_url):
        # print(book_url[0] + "++" + book_url[1])
        time.sleep(random.uniform(0, 3))
        book_html = self.get_html(book_url[0])
        sel = parsel.Selector(book_html)
        book_info1 = re.findall('<span class="pl">出版年:</span>(.*?)<br/>.*?<span class="pl">定价:</span> (.*?)<br/>.*?'
                                '<strong class="ll rating_num " property="v:average"> (.*?) </strong>',
                                book_html, re.S)
        book_detail_ = sel.xpath('//div[@class="intro"]/p/text()').getall()
        book_detail = "".join(book_detail_)
        book_name = sel.xpath('//*[@id="wrapper"]/h1/span/text()').get()
        book_ttm = book_info1[0][0]
        book_price = book_info1[0][1]
        book_grade = book_info1[0][2]
        book_info_dic = {
            '书名': book_name,
            '上市时间': book_ttm,
            '书的价格': book_price,
            '书籍评分': book_grade,
            '内容简介': book_detail,
            '书籍分类': book_url[1],
        }
        # 调用存取函数，将数据保存到csv中
        self.save_as_csv(book_info_dic)

    # 分析出各页每本图书的url，并结合分类tag
    def parsel_html_tag(self, url, tag):
        html = self.get_html(url)
        sel = parsel.Selector(html)
        book_url_list = sel.xpath('//div[@class="info"]/h2/a/@href').getall()
        c = lambda x, y: (x, y)
        book_url_list_ = []
        for book_url in book_url_list:
            book_url_list_.append(c(book_url, tag))

        # 多线程爬取图书的基本信息
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.parsel_book, [book_url for book_url in book_url_list_])

    # 各类图书翻页页面主函数爬取
    def tag_main(self, book_tag):
        for num in range(0, 250, 25):
            start_url = book_tag['路径'] + f'?start={num}'
            page = num / 25 + 1
            print("开始爬取{}的第{}页".format(book_tag['标签名'], page))
            # 随机休眠0到3秒
            time.sleep(random.uniform(0, 3))
            # 进入对每页图书进行爬取的爬虫
            self.parsel_html_tag(start_url, book_tag['标签名'])

    def domain(self, url):
        # 获取html，调用了parsel_html_index函数对分类的名字和url进行爬取，最后返回
        html = self.get_html(url)
        book_tag_list = self.parsel_html_index(html)

        # 单线程
        # for book_tag in book_tag_list:
        #     self.tag_main(book_tag['路径'], book_tag['标签名'])

        # 多线程， 只使用了3个线程，同时对3种分类进行爬取
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # 这里调用了tag_main，即每个分类的爬虫
            executor.map(self.tag_main, [book_tag for book_tag in book_tag_list])


if __name__ == '__main__':
    # 创建爬虫实例对象
    d = DoubanSpider()
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    }
    # 豆瓣图书分类主页
    start_url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
    # 调用爬虫启动函数
    d.domain(start_url)
