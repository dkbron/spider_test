import parsel
import requests
import re
import csv
import time
import random


class TencentSpider:
    """爬取腾讯招聘网的招聘信息"""

    def __init__(self):
        with open('./tencent_career_info.csv', 'w', newline='', encoding='utf-8') as f:
            spawriter = csv.writer(f)
            spawriter.writerow(['招聘岗位', '工作职责', '工作要求'])

    # 获取url的html页面
    def get_html(self, url):
        response = requests.get(url, headers=headers)
        print(response.status_code)
        response.encoding = 'utf-8'
        html = response.text
        return html

    def save_as_csv(self, career_info_list):
        with open('./tencent_career_info.csv', 'a', newline='', encoding='utf-8') as f:
            spawriter = csv.writer(f)
            spawriter.writerow(career_info_list)

    def get_career_info(self, PostId):
        """单个职位信息爬取"""
        get_info_url = f'https://careers.tencent.com/tencentcareer/api/post/ByPostId?postId={PostId}'
        career_info = self.get_html(get_info_url)
        RecruitPostName = re.findall('"RecruitPostName":"(.*?)"', career_info, re.S)
        Responsibility = re.findall('"Responsibility":"(.*?)"', career_info, re.S)
        Requirement = re.findall('"Requirement":"(.*?)"', career_info, re.S)
        self.save_as_csv([RecruitPostName[0],Responsibility[0],Requirement[0]])

    def do_main(self):
        """
        爬虫主函数
        """
        for i in range(1, 10):

            url = f'https://careers.tencent.com/tencentcareer/api/post/Query?pageIndex={i}&pageSize=10&language=zh-cn&area=cn'
            data_text = self.get_html(url)
            # print(data_text)
            re_rule = '"PostId":"(.*?)"'
            PostId_list = re.findall(re_rule, data_text, re.S)
            # print(PostId_list)
            for PostId in PostId_list:
                time.sleep(random.uniform(0, 0.5))
                self.get_career_info(PostId)


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    }

    t = TencentSpider()
    t.do_main()
