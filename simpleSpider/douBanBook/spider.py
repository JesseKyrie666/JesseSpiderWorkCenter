# coding=utf-8
import random
import requests
from lxml import etree
import time
import json

class BookSpider:
    def __init__(self, start_page=0, end_page=1):
        self.home_page_url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4'
        self.start_page = int(start_page)
        self.end_page = int(end_page)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        self.save_dict = {
            'start_page': self.start_page,
            'end_page': self.end_page,
        }

    def start_requests(self):
        for page in range(self.start_page - 1, self.end_page):
            params = {
                'start': str(page * 20),
                'type': 'T',
            }
            response = requests.get(url=self.home_page_url, params=params, headers=self.headers)
            print("status code:",response.status_code)
            html = response.text
            self.save_dict[page] = {
                'page': page,
                'status_code': response.status_code,
                'data': [],
            }
            self.parse(html, page)


    def parse(self,html,page):
        eobj = etree.HTML(html)
        book_li = eobj.xpath('//ul[@class="subject-list"]/li')
        for li in book_li:
            title = li.xpath('./div[@class="info"]/h2/a/text()')[0]
            info_link = li.xpath('./div[@class="info"]/h2/a/@href')[0]
            author_info = li.xpath('./div[@class="info"]/div[1]/text()')[0]
            novel = {
                'title': title.strip(),
                'info_link': info_link.strip(),
                'author': author_info.strip(),
            }
            print(novel)
            self.save_dict[page]['data'].append(novel)
            self.info_page_requests(novel['info_link'],page)
            time.sleep(random.uniform(1, 3))


    def info_page_requests(self,info_link,page):
        response = requests.get(url=info_link, headers=self.headers)
        html = response.text
        self.info_parse(html,page)

    def info_parse(self,html,page):
        eobj = etree.HTML(html)
        content_div = eobj.xpath('//*[@id="content"]')[0]
        content = etree.tostring(content_div, encoding='utf-8').decode('utf-8')
        self.save_dict[page]['data'][-1]['content_div'] = content

    def save(self):
        with open('douBanBook.json', 'w', encoding='utf-8') as f:
            json.dump(self.save_dict, f, ensure_ascii=False)


if __name__ == '__main__':
    start_page = 1
    end_page = 2
    spider = BookSpider(start_page, end_page)
    spider.start_requests()
    spider.save()
