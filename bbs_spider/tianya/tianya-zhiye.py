import threading
import time
import multiprocessing
import pymongo
import redis
import threadpool
import requests
from lxml import etree
import sys
from pybloom import BloomFilter
import logzero
from logzero import logger

from fake_useragent import UserAgent
from multiprocessing.dummy import Pool as thpool

ua = UserAgent()
sys.setrecursionlimit(1000000)
clients = pymongo.MongoClient('localhost')
db = clients["bbs"]
col1 = db["tianya-bbs"]
col2 = db["tianya-url"]
filter = BloomFilter(capacity=15 * (8 * 1024 * 1024), error_rate=0.001)  # 1Mb可以去重58 - 80 万数据
logzero.logfile('zhiye.log', maxBytes=50 * 1024 ^ 3)


def add_bloom_from_mongo():
    print('add user_id to bloomfilter form mongodb')
    for i in col2.find():
        filter.add(i['url'])
    print('over')


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': ua.random,
    # 'cookie': '_dacevid3=748ac4b3.2240.97e1.ca5d.3023e34efe24; _HUPUSSOID=5c904bc3-02a3-4c73-a630-1298ca6a354f; _CLT=b0c2a05996d8b48b354e1fa4ddfc1fef; u=32023008|5LiN6IKv5byA5Y+j|1068|568bcea6bff5398192f8e5c114a67672|bff5398192f8e5c1|aHVwdV9kMzQ2ZDdmNzc3M2RlZDIz; us=4a7ac4a0344d0f42cd093dbb393654f10e187dce817b6bc5b5f349c6de812ddc452edda81a76fd190ac22c90b1c10887af210b8718fe8b6ec2fc28ce3522bf02; _fmdata=4543AD30FB53502925A1CC1A227A8192C6419010310B679335F7B9CBF7FFC05EFDB446EED3ECF143E115FADEE69D04723488662B07B36DEC; ua=166995178; lastvisit=6699%091502956882%09%2Fthread.php%3Fboardname%3Dtopic%26page%3D2; __dacevst=390ffac6.37cb7c32|1502958681045; _cnzz_CV30020080=buzi_cookie%7C748ac4b3.2240.97e1.ca5d.3023e34efe24%7C-1; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1502681042,1502681117,1502760900,1502956607; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1502956882'
}

# proxies = {
#     'http': "http://H25P63881QWD60HD:4312068F64019001@http-dyn.abuyun.com:9020",
#     'https': "http://H25P63881QWD60HD:4312068F64019001@http-dyn.abuyun.com:9020"
# }

proxies = {
    'http': "61.132.93.14:6500",
    'https': "61.132.93.14:6500"
}


def to_redis(data):
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    print("{} into redis".format(data))
    r.sadd("tianya_zhiye_url", '{}'.format(data))


def pop_redis():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
    po = r.spop("tianya_zhiye_url")
    return po


def get_url_list():
    url = 'http://bbs.tianya.cn/'
    try:
        html = requests.get(url, headers=headers, timeout=7).content
        ls = etree.HTML(html).xpath('//*[@id="bbs_left_nav"]/div[7]/ul/li/a/@href')
        ls = ['http://bbs.tianya.cn' + i for i in ls]
        # print(ls)
        for i in ls:
            to_redis(i)
    except:
        get_url_list()


def get_list(url):
    print('this list url is :   ', url)
    if url == 'http://bbs.tianya.cnjavascript:history.go(-1)':
        print('over...')
        new_url = pop_redis()
        if start_url != new_url:
            get_list(new_url)
        return
    if url not in filter:
        logger.info('URL:  ' + url)
        try:
            html = requests.get(url, headers=headers, timeout=7).content
        except requests.exceptions.ConnectionError:
            html = ''
            get_list(url)
        # print(html.decode('utf-8'))
        lss = etree.HTML(html).xpath(''
                                     '//*[@id="main"]/div[6]/table/tbody/tr/td[1]/a/@href')
        if not lss:
            lss = etree.HTML(html).xpath('//*[@id="main"]/div[7]/table/tbody/tr/td[1]/a/@href')
        detail_list = []
        for i in lss:
            link = 'http://bbs.tianya.cn' + i
            detail_list.append(link)
        # thread_main(detail_list)
        thread_pool(detail_list)
        # thread(detail_list)
        # multipro_main(detail_list)
        dic2 = {'url': url}
        col2.insert(dic2)
        filter.add(url)
        next_page(url)
    else:
        logger.warning('exists: {}'.format(url))
        next_page(url)


def next_page(url):
    html = requests.get(url, headers=headers).content
    next_page = etree.HTML(html).xpath('//*[@id="main"]/div[7]/div/a[last()]/@href')
    if not next_page:
        next_page = etree.HTML(html).xpath('//*[@id="main"]/div[8]/div/a[last()]/@href')
    if next_page:
        next_link = 'http://bbs.tianya.cn' + next_page[0]
        if not 'http://bbs.tianya.cn' in next_link:
            next_link = 'http://bbs.tianya.cn' + next_page
        try:
            get_list(next_link)
        except requests.exceptions.Timeout:
            print('error')
            print(next_link)
            # print(next_link)
            get_list(next_link)


def get_detail(url):
    try:
        html = requests.get(url, headers=headers, timeout=4).content
        title = ''.join(etree.HTML(html).xpath('//*[@id="post_head"]/h1/span[1]/span/text()'))
        if not title:
            title = ''.join(etree.HTML(html).xpath('//*[@id="container"]/div[2]/div[2]/h1/span/text()'))
        anwsers = etree.HTML(html).xpath('//div[@class="atl-main"]/div[@class="atl-item"]/div[2]/div[2]/div[1]/text()')
        if not anwsers:
            anwsers = etree.HTML(html).xpath('//div[@class="content"]/text()')
        # print(title)
        anwsers_new = [i.replace(" ", "").replace("\t", "").strip() for i in anwsers]
        dic = {
            'title': title,
            'anwsers': anwsers_new
        }
        col1.insert(dic)
        print(dic['title'])
    except Exception as e:
        print(e)
        # get_detail(url)


def thread_pool(item):
    pool = thpool(20)
    pool.map(get_detail, item)
    pool.close()
    pool.join()


def thread_main(item):
    pool = threadpool.ThreadPool(4)
    tasks = threadpool.makeRequests(get_detail, item)
    [pool.putRequest(req) for req in tasks]
    pool.wait()


def multipro_main(item):
    pool = multiprocessing.Pool(4)
    pool.map(get_detail, item)
    pool.close()
    pool.join()


def thread(item):
    task = []
    for i in item:
        task.append(threading.Thread(target=get_detail, args=(i,)))
    for t in task:
        t.start()
    for t in task:
        t.join()


if __name__ == '__main__':
    # get_url_list()
    start_url = 'http://bbs.tianya.cnjavascript:history.go(-1)'
    with open('zhiye.log', 'r') as f:
        ls = f.readlines()
        start_url = ls[-1][42:-1]
    # start_url = 'http://bbs.tianya.cn/list.jsp?item=763&nextid=1418452648000'
    add_bloom_from_mongo()
    get_list(start_url)
