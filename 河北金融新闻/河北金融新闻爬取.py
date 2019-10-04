"""
 爬取河北金融学院新闻模块数据
"""
__Author__ = 'DKBorn'

import requests
import pprint
import re
import csv


class HbfuSpider:
    """
    爬取河北金融学院新闻
    """
    def __init__(self):
        with open('./河北金融学院新闻.csv', 'w', newline='', encoding='utf-8') as f:
            spawriter = csv.writer(f)
            spawriter.writerow(['标题', '部分内容'])

    # 保存文件为csv格式
    def save_as_csv(self, news_info):
        with open('./河北金融学院新闻.csv', 'a', newline='', encoding='utf-8') as f:
            spawriter = csv.writer(f)
            spawriter.writerow(news_info)

    def get_html_post(self, url, data):
        """
        使用post请求html，并返回json数据
        :param url: 主页面url
        :param data: post请求时传入的数据
        :return: json_data，返回json数据
        """
        response = requests.post(url, verify=False, headers=headers, data=data)
        json_data = response.json()
        return json_data

    def get_html(self, url):
        response = requests.get(url, verify=False, headers=headers)
        response.encoding = 'utf-8'
        html = response.text
        return html

    def re_content(self, content):
        """
        对json_data中的content内容进行正则提取
        """
        # 定义正则规则
        re_rule = '<p style="text-indent:2em;">(.*?)</p>'

        news_info = re.findall(re_rule, content, re.S)
        return news_info[0].strip()

    def domain(self, url):
        """
        主函数
        :param url: 传入的url为河北金融学院新闻模块地址
        """

        for start_num in range(0, 1000, 20):
            data = {
                'start': start_num,
                'limit': 20,
                'type': 1,
            }
            json_data = self.get_html_post(url, data)
            for json_data_num in range(0, len(json_data['rows'])):
                news_num = json_data['rows'][json_data_num]['id']
                data_id = {
                    'id': news_num,
                }
                json_data_news = self.get_html_post('https://www.hbfu.edu.cn/news/findById', data_id)
                news_content = self.re_content(json_data_news['content'])
                news_title = json_data_news['title']
                news_info = [news_title, news_content]
                self.save_as_csv(news_info)
                print(news_info)


if __name__ == '__main__':
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '24',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=9278C754FEE53E337F699658AE3097A8',
        'Host': 'www.hbfu.edu.cn',
        'Origin': 'https://www.hbfu.edu.cn',
        'Referer': 'https://www.hbfu.edu.cn/newsList?type=1',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    url = 'https://www.hbfu.edu.cn/news/queryListForPage'
    # url1 = 'https://www.hbfu.edu.cn/news/findById'
    hb_spider = HbfuSpider()
    hb_spider.domain(url)
