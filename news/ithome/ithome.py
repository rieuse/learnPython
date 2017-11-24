import re

import pymongo
import requests
from lxml import etree
import sys
from pybloom import BloomFilter
import logzero
from logzero import logger
import time
from fake_useragent import UserAgent
from multiprocessing.dummy import Pool as thpool

ua = UserAgent()
sys.setrecursionlimit(1000000)
clients = pymongo.MongoClient('localhost')
db = clients["bbs"]
col1 = db["ithome-bbs"]
col2 = db["ithome-url"]
logzero.logfile('ithome.log', maxBytes=500 * 1024 ^ 3)
# filter = BloomFilter(capacity=15*(8*1024*1024), error_rate=0.001) # 1Mb可以去重58 - 80 万数据

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://it.ithome.com/',
    'User-Agent': ua.random,
}

proxies = {
    'http': "http://H25P63881QWD60HD:4312068F64019001@http-dyn.abuyun.com:9020",
    'https': "http://H25P63881QWD60HD:4312068F64019001@http-dyn.abuyun.com:9020"
}


def get_comment(news_id):
    comment_url = 'https://dyn.ithome.com/comment/{}'.format(news_id)
    comment_post_url = 'https://dyn.ithome.com/ithome/getajaxdata.aspx'
    hash = etree.HTML(requests.get(comment_url).text).xpath('//*[@id="hash"]/@value')[0]
    comment = []
    page = ''
    data = {
        'newsID': news_id,
        'hash': hash,
        'type': 'commentpage',
        'page': '',
        'order': 'false',
    }
    for i in range(1, 10):
        try:
            data['page'] = str(i)
            html = requests.post(comment_post_url, data=data).text
            com = etree.HTML(html).xpath('//li/div[2]/div[2]/p/text()')
            for j in com:
                comment.append(j)
        except:
            return comment, hash


def parse_html(url):
    print(url)
    news_id = re.search(r'(?<=/)(\d)+(?=.htm)', url)[0]
    r = requests.get(url, headers=headers)
    html = ''
    if r.status_code == 200:
        html = r.content.decode('utf-8')
    else:
        return
    title = etree.HTML(html).xpath('//*[@id="wrapper"]/div[1]/div[2]/h1/text()')
    if title:
        title = title[0]
    else:
        return
    content = etree.HTML(html).xpath('//*[@id="paragraph"]/p/text()')
    content = ''.join([i.strip() for i in content])
    try:
        comment, hash = get_comment(news_id)
        # if not hash:
        #     print(url)
        # if content:
        #     print(url)
        comment_num = len(comment)
        doc = {
            'url': url,
            'hash': hash,
            'title': title,
            'content': content,
            'comment': comment,
            'comment_num': comment_num,
        }
        col1.insert(doc)
    except Exception as e:
        print(url, e)
        return
    print(title)


def parse_url(url):
    logger.info(url)
    html = requests.get(url, headers=headers).content
    urls = etree.HTML(html).xpath('//ul[@class="ulcl"]/li/a/@href')
    thread_pool(urls)
    # for u in urls:
    # print(u)
    # parse_html(u)
    # return


def start():
    # https://www.ithome.com/list/2011-05-15.html
    start_date = 1
    for i in range(15, 18):
        for j in range(1, 13):
            urls = ['https://www.ithome.com/list/20{}-{}-{}.html'.format(str(i).zfill(2), str(j).zfill(2),
                                                                         str(num).zfill(2)) for num in
                    range(start_date, 32)]
            for url in urls:
                parse_url(url)
        return


def thread_pool(item):
    pool = thpool(8)
    pool.map(parse_html, item)
    pool.close()
    pool.join()


if __name__ == '__main__':
    start()
