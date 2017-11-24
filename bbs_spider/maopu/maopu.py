import json
import pymongo
import requests
import time
from lxml import etree
import sys
from pybloom import BloomFilter
import logzero
from logzero import logger
from fake_useragent import UserAgent
from multiprocessing.dummy import Pool as thpool

"""
http://pclistinterface.mop.com/mdi/data.html?pgnum=1&colid=110001&pgsize=40&serialnum=300000&startcol=10020&mirrorid=1507777321

colid=110001  这是type
pgsize=40 每页内容多少
startcol=10020  开始的页数   如果是第0 页  则为null
mirrorid=1507777321 


"""

ua = UserAgent()
sys.setrecursionlimit(1000000)
clients = pymongo.MongoClient('localhost')
startcol = ''
db = clients["bbs"]
col1 = db["maopu"]
col2 = db["maopu-last"]
logzero.logfile('maopu.log', maxBytes=50 * 1024 ^ 3)
filter = BloomFilter(capacity=15 * (8 * 1024 * 1024), error_rate=0.001)  # 1Mb可以去重58 - 80 万数据

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://dzh.mop.com/yuanchuang.html',
    'User-Agent': ua.random,
}


# http://pclistinterface.mop.com/mdi/data.html?pgnum=1&colid=110001&pgsize=40&serialnum=300000&startcol=10020&mirrorid=1507777321&platform=pc&uid=15077176192749157&qid=null&_=1507779251596

def get_txt(doc):
    articleid = doc['articleid']
    doc['content'] = parse(articleid)['content']
    doc['other'] = parse(articleid)
    col1.insert(doc)
    print(doc['title'][:4])


def repaly(repaly_id):
    url = 'http://comment.mop.com/mopcommentapi/dzh/replylist/api/v170828/replyat/offset/asc/{}/0/100'.format(repaly_id)
    try:
        html = requests.get(url, headers=headers).text
    except:
        html = requests.get(url, headers=headers).text
    js = json.loads(html)
    return js['data']


def get_url():
    for i in range(1000000000):
        if i == 0:
            startcol = 'null'
        # else:
        #     col1.find()
        #     startcol = 1
        timestamp = int(time.time() * 1000)
        u = 'http://pclistinterface.mop.com/mdi/data.html?pgnum={}&colid=110007&pgsize=40&serialnum=000000&startcol={}&mirrorid={}&_={}'
        url = u.format(i, startcol, '1507777321', timestamp)
        # startcol = 10019 + (i * 20)
        logger.info(url)
        html = requests.get(url, headers=headers).text
        js = json.loads(html)
        # print(js['data'][0]['title'])
        startcol = js['data'][-1]['startcol']
        # articleid = js['data'][20]['articleid']
        docs = []
        for doc in js['data']:
            # get_txt(doc)
            docs.append(doc)
        thread_pool(docs)
        # doc['content'] = parse(articleid)['content']
        # doc['other'] = parse(articleid)
        # col1.insert(doc)
        # print(doc['title'])


def parse(articleid):
    try:
        parse_url = 'http://staticize.mop.com/subject/getArticleById?id={}&type=dzh'.format(articleid)
        html = requests.get(parse_url, headers=headers).text
    except:
        parse_url = 'http://staticize.mop.com/subject/getArticleById?id={}&type=dzh'.format(articleid)
        html = requests.get(parse_url, headers=headers).text
    js = json.loads(html)
    repaly_id = str(js['article']['publishtime']) + str(js['article']['rdts'])
    # print(js['article']['publishtime'],js['article']['rdts'],repaly_id)
    js['article']['comment'] = repaly(repaly_id)
    return js['article']


def thread_pool(item):
    pool = thpool(8)
    pool.map(get_txt, item)
    pool.close()
    pool.join()


if __name__ == '__main__':
    get_url()
    # parse('50559398')

    # 正在抓取的是娱乐的最新帖子数据
