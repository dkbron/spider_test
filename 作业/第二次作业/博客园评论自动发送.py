"""等待博客园申请通过"""
import requests

if __name__ == '__main__':
    header = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '56',
        'content-type': 'application/json; charset=UTF-8',
        'cookie': "回复后抓包获取cookie",
        'origin': 'https://www.cnblogs.com',
        'referer': 'https://www.cnblogs.com/',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    cookie = {
        'Cookie': "回复后抓包获取cookie"
    }

    data = {
        'postId': 11484792,
        'body': "自动评论1",
        'parentCommentId': 0,
    }
    response = requests.post('https://www.cnblogs.com/dkborn/ajax/PostComment/Add.aspx',
                             headers=header, cookies=cookie, json=data)
    print(response.text)