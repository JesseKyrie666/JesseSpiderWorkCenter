# coding=utf-8

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

response = requests.get('https://m.dytt8.net/html/gndy/dyzz/20221124/63182.html', headers=headers)

# 支持的编码格式
response.encoding = 'gb2312'
print(response.text)

with open('dytt.html', 'w', encoding='gb2312') as f:
    f.write(response.text)