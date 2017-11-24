import pymongo
import requests
import threadpool
from lxml import etree
import time
import random
import hashlib
from bs4 import BeautifulSoup
import json
import codecs
from multiprocessing.dummy import Pool as thpool

clients = pymongo.MongoClient('localhost')
db = clients["sougou"]
col = db['info9']

UA_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Proxy-Authorization': '',
    'User-Agent': random.choice(UA_LIST),
}

ips = []

proxies = {
    'http': "http://HNNQGH266EK51B9D:CED133A418A4C0CC@http-dyn.abuyun.com:9020",
    'https': "http://HNNQGH266EK51B9D:CED133A418A4C0CC@http-dyn.abuyun.com:9020"
}


# proxies = {
#     'http': 'http://ip.16yun.cn:917/myip/proxylist/3669ff19-a90e-40a1-9082-cddbe64af5e7/?u=admin',
#     'https': 'http://ip.16yun.cn:917/myip/proxylist/3669ff19-a90e-40a1-9082-cddbe64af5e7/?u=admin'
# }

# ips = []

# def get_ip():
#     r = requests.get('http://ip.16yun.cn:917/myip/proxylist/3669ff19-a90e-40a1-9082-cddbe64af5e7/?u=admin')
#     host_port = r.text
#     if host_port in ips:
#         get_ip()
#     else:
#         ips.append(host_port)
#         return host_port

def get_link():
    urls = ['http://zhinan.sogou.com/guide/cate?cateId=49&type=0&pg={}'.format(num) for num in range(0, 10)]
    for url in urls:
        print(url)
        html = requests.get(url, headers=headers).content.decode('utf-8')
        lins = etree.HTML(html).xpath('//div[@class="recommend-summary"]/h3/a/@href')
        urls = []
        for lin in lins:
            link = 'http://zhinan.sogou.com' + lin
            print(link)
            urls.append(link)
            # get_txt(link)
        thread_pool(urls)


def get_txt(link):
    html = requests.get(link, headers=headers).content.decode('utf-8')
    title = ''.join(etree.HTML(html).xpath('//div[@class="main"]/article/h1/text()'))
    img = ''.join(etree.HTML(html).xpath('/html/body/div[2]/div[1]/article/div[3]/img/@src'))
    # head = ''.join(etree.HTML(html).xpath('//div[@class="main"]/article/div[3]/p/text()'))
    # soup = BeautifulSoup(html, 'lxml')
    # con= soup.select('#guide_1_detail > li')
    # for i in range(0, con.__len__()):
    #     con[i] = str(con[i])
    # con = '\n'.join(con)
    # if not title:
    #     print('None')
    # dic = {
    #     'head': head,
    #     'img': img,
    #     'title': title,
    #     'content': con
    # }
    # js = json.dumps(dic,ensure_ascii=False)
    # with codecs.open('户外运动3.json','a','utf-8') as f:
    #     f.write(js + '\n')
    print(img)
    # time.sleep(3)


def thread_pool(item):
    pool = thpool(3)
    pool.map(get_txt, item)
    pool.close()
    pool.join()


if __name__ == '__main__':
    get_link()
