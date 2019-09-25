"""
我主良缘 交友网站数据采集  http://www.7799520.com/jiaoyou.html
"""
__Author__ = 'DKBorn'
import requests
import csv


class WoZhuSpider:
    """我主良缘 交友网站数据采集"""

    def __init__(self):
        with open('./我主良缘用户信息.csv', 'w', newline='', encoding='UTF-8') as f:
            spawriter = csv.writer(f)
            spawriter.writerow(['userid', 'province', 'city', 'height', 'education', 'username', 'monolog', 'birthdayyear', 'avatar', 'gender', 'salary', 'marry', 'monologflag'])

    # 保存文件为csv格式
    def save_as_csv(self, wz_info_json):
        print(wz_info_json)
        # wz_info['userid'], wz_info['province'], wz_info['city'], wz_info['height'], wz_info['education'], wz_info['username'], wz_info['monolog'], wz_info['birthdayyear'], wz_info['avatar'], wz_info['gender'], wz_info['salary'], wz_info['marry'], wz_info['monologflag']
        with open('./我主良缘用户信息.csv', 'a', newline='', encoding='UTF-8') as f:
            spawriter = csv.writer(f)
            for wz_info in wz_info_json:
                spawriter.writerow([wz_info['userid'], wz_info['province'], wz_info['city'], wz_info['height'],
                                    wz_info['education'], wz_info['username'], wz_info['monolog'], wz_info['birthdayyear'],
                                    wz_info['avatar'], wz_info['gender'], wz_info['salary'], wz_info['marry'], wz_info['monologflag']])


    # 获取url的html页面
    @staticmethod
    def get_html(url):
        response = requests.get(url, headers=headers)
        print(response.status_code)
        response.encoding = 'utf-8'
        html = response.json()
        return html

    def domain(self):
        for page in range(1,9):
            html = self.get_html(f'http://www.7799520.com/api/user/pc/list/search?marry=1&page={page}')
            self.save_as_csv(html['data']['list'])


if __name__ == '__main__':
    # 创建爬虫实例对象
    d = WoZhuSpider()
    # 设置请求头
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_ee0de768b7db1b355930288073352dbe=1567876037; 59167___602875_KS_59167___602875=0bfd6b082f824ebb92ba03a345d4791a; 59167___602875_KS_ri_ses=19094237434%7CE2F86EAA4C4A67C6007F9A283233E9C9-null; Hm_lpvt_ee0de768b7db1b355930288073352dbe=1567876185; 59167___602875_curPageNum=3; 59167___602875_curRanId=1567876204511_1567876038501; 59167___602875_curPage_1567876038501=2_false_1567876204513',
        'Host': 'www.7799520.com',
        'Referer': 'http://www.7799520.com/jiaoyou.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    # 调用爬虫启动函数
    d.domain()
