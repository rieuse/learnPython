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
col1 = db["mydrivers-bbs"]
col2 = db["mydrivers-url"]
logzero.logfile('mydrivers.log', maxBytes=500 * 1024 ^ 3)
# filter = BloomFilter(capacity=15*(8*1024*1024), error_rate=0.001) # 1Mb可以去重58 - 80 万数据

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://news.mydrivers.com/',
    'User-Agent': ua.random,
}

proxies = {
    'http': "http://H25P63881QWD60HD:4312068F64019001@http-dyn.abuyun.com:9020",
    'https': "http://H25P63881QWD60HD:4312068F64019001@http-dyn.abuyun.com:9020"
}


# def add_bloom_from_mongo():
#     print('add user_id to bloomfilter form mongodb')
#     for i in col2.find():
#         filter.add(i['url'])
#     print('over')


# url = 'http://blog.mydrivers.com/getnewnewslistjson.aspx?pageid=100&cids=&timestamp={0}&callback=NewsList&_={0}'.format(timestamp)
# timestamp = int(time.time())
# headers['Referer'] = 'http://news.mydrivers.com/'


def parse_html(url):
    try:
        html = requests.get(url, headers=headers).content
        title = etree.HTML(html).xpath('//*[@id="thread_subject"]/text()')[0]
        content = etree.HTML(html).xpath('//div[@class="news_info"]/p/text()')
        content = ''.join(content)
        article_id = url[-10:-4]
        comment_url = 'http://comment8.mydrivers.com/ReviewAjax.aspx?Tid={}&Cid=1&Page=1'.format(article_id)
        comment = requests.get(comment_url).text
        doc = {
            'title': title,
            'content': content,
            'comment': comment
        }
        logger.info(url)
        col1.insert(doc)
        print(title)
    except:
        logger.warn(url)
        return


def parse_url(url):
    date = url[-14:-4]
    html = requests.get(url, headers=headers).text
    detail_urls = etree.HTML(html).xpath('//*[@id="newsleft"]/div/div[1]/a/@href')
    # print(detail_urls)
    thread_pool(detail_urls)
    page_num = etree.HTML(html).xpath('//*[@class="postpage"]/a[last()-2]/text()')
    if page_num:
        page_num = page_num[0]
    else:
        logger.warn('error!  please check it  url:  {}'.format(url))
        return
    if int(page_num) >= 2:
        for i in range(int(page_num) + 1):
            if i >= 2:
                page_url = 'http://news.mydrivers.com/getnewsupdatelistdata.aspx?data={}&pageid={}'.format(date, i)
                html2 = requests.get(page_url, headers=headers).text
                detail_urls2 = etree.HTML(html).xpath('//div/div[2]/div[2]/p/a/@href')
                # print(detail_urls2)
                thread_pool(detail_urls2)


def start():
    # 'http://news.mydrivers.com/update/2001-05-21.htm'
    for i in range(16, 18):
        for j in range(5, 13):
            urls = ['http://news.mydrivers.com/update/20{}-{}-{}.htm'.format(str(i).zfill(2), str(j).zfill(2),
                                                                             str(num).zfill(2)) for num in
                    range(21, 32)]
            for url in urls:
                parse_url(url)
                return


def thread_pool(item):
    pool = thpool(6)
    pool.map(parse_html, item)
    pool.close()
    pool.join()


if __name__ == '__main__':
    # url = 'http://news.mydrivers.com/1/305/305443.htm'
    # parse_html(url)
    start()
