"""
通过Python程序登陆美食杰网站页面。
"""
__Author__ = 'DKBorn'

import requests


def domain(url):
    response = requests.post(url, data=data, headers=headers)
    response.encoding = response.apparent_encoding
    with open('./meishi_index.html', mode='wb') as f:
        try:
            f.write(response.content)
            print('保存完毕')
        except:
            print('保存失败')


if __name__ == '__main__':
    start_url = 'https://i.meishi.cc/login.php'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '97',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'i.meishi.cc',
        'Origin': 'https://i.meishi.cc',
        'Referer': 'https://i.meishi.cc/login.php?redirect=http%3A%2F%2Fi.meishi.cc%2Faccount%2Fbasic.php',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    }

    data = {
        'redirect': 'http://i.meishi.cc/account/basic.php',
        'username': '3427241590@qq.com',
        'password': 'dkborn123',
    }

    domain(start_url)

