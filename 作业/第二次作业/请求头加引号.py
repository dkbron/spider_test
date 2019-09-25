"""
使用正则表达式将headers转换成python字典格式的工具函数
"""

import re

headers_str = """
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Length: 24
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: JSESSIONID=9278C754FEE53E337F699658AE3097A8
Host: www.hbfu.edu.cn
Origin: https://www.hbfu.edu.cn
Referer: https://www.hbfu.edu.cn/newsList?type=1
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36
X-Requested-With: XMLHttpRequest
"""


pattern = '^(.*?): (.*)$' #
#           1     2
for line in headers_str.splitlines(): # 反向引用
    print(re.sub(pattern, '\'\\1\': \'\\2\',', line))
