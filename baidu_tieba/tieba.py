# -*- coding： utf-8 -*-
# 按贴吧帖子 ID 顺序爬取纯文本数据， 每个帖子保存为一个 ID_帖子标题.txt 文件
# ./ID.txt 存放从哪个 ID 开始爬，不存在则ID默认为 5000000000

import re
import os
import threading
import time
import codecs
import multiprocessing
from multiprocessing.dummy import Pool as thpool
import urllib.request
import random
import logging
import pymongo
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

client = pymongo.MongoClient('localhost')
db = client['baidu']
col = db['tieba']

# 多进程锁
m_lock = multiprocessing.Lock()
ua = UserAgent()


def get_title(html):
    try:
        soup = BeautifulSoup(html, 'lxml')
        raw_title = soup.find('h1')
        if not raw_title:
            raw_title = soup.find('h3')
        if not raw_title:
            raw_title = re.findall('很抱歉，该贴已被删除。', html)
            if raw_title:
                raw_title = raw_title[0]
        if not raw_title:
            raw_title = re.findall('该吧被合并您所访问的贴子无法显示', html)
            if raw_title:
                raw_title = raw_title[0]
        if not raw_title:
            raw_title = re.findall('抱歉，您访问的贴子被隐藏，暂时无法访问。', html)
            if raw_title:
                raw_title = raw_title[0]
        if not raw_title:
            return ''
        title = remove_html_tag(str(raw_title))
        return title
    except Exception as e:
        logging.warning('Get title: {}'.format(e))
        return ''


def get_posts_num(html):
    try:
        soup = BeautifulSoup(html, 'lxml')
        raw_posts_num = soup.find('ul', {'class': 'l_posts_num'})
        match = re.findall('pn=[0-9]+', str(raw_posts_num))
        if match:
            last_num_url = match.pop()
            last_num = re.findall('[0-9]+', str(last_num_url))
            return int(last_num[0])
        else:
            return 1
    except Exception as e:
        logging.warning('Get posts num: '.format(e))
        return 1


# 暂时不需要
def get_floor(content):
    c_content = '<html><body>' + str(content) + '</html></body>'
    try:
        soup = BeautifulSoup(c_content, 'lxml')
        raw_floor = soup.findAll('span', {'class': 'tail-info'})
        f_floor = re.findall('[0-9]+楼', str(raw_floor))
        if f_floor:
            floor = remove_html_tag(str(f_floor[0]))
            return str(floor)
        else:
            return ''
    except Exception as e:
        logging.warning('Get floor: {}'.format(e))
        return ''


def get_whole_page_content(html):
    try:
        soup = BeautifulSoup(html, 'lxml')
        raw_posts_content = soup.findAll('div', {'class': ['d_post_content_main']})
        content = ''
        for post_content in raw_posts_content:
            each_content = get_content(post_content)
            if each_content:
                content = content + each_content + '\n\n'
        return content
    except Exception as e:
        logging.warning('Get whole page content: {}'.format(e))
        return ''


def get_content(text):
    c_text = '<html><body>' + str(text) + '</html></body>'
    try:
        soup = BeautifulSoup(c_text, 'lxml')
        raw_content = soup.find('div', {'class': 'd_post_content'})
        content = re.findall('\S.+', remove_html_tag(str(raw_content)))
        if content:
            return str(content[0])
        else:
            return ''
    except Exception as e:
        logging.warning('Get content: {}'.format(e))
        return ''


def save_content(path, content):
    try:
        with codecs.open(path, 'w', 'utf-8') as fw:
            fw.write(content)
    except Exception as e:
        logging.warning('Save content: {}'.format(e))


def remove_html_tag(html):
    html = html.strip()
    dr = re.compile(r'<[^>]+>', re.S)
    html = dr.sub('', html)
    return html


class Spider(object):
    def __init__(self):
        self.list_url_queue = multiprocessing.Manager().list()
        self.seed_url = 'https://tieba.baidu.com/'
        self.post_id_file = './ID.txt'
        self.output_dir = './output/'
        self.post_id = int()

        # 多进程数量
        self.process_num = 100
        # 150 2min 750 `
        # 200 2min 880
        # 180  820
        # 一次放多少条帖子链接队列
        self.queue_put_num = 1000

    def get_html(self, url):
        req = urllib.request.Request(url, headers={'User-Agent': ua.random})
        time.sleep(random.randint(3, 20))
        attempts = 0
        attempts_times = 15
        while attempts < attempts_times:
            try:
                website = urllib.request.urlopen(req, timeout=(25 + random.randint(3, 10)))
                html = website.read().decode('utf-8')
                return html
            except Exception as e:
                attempts = attempts + 1
                if attempts == attempts_times:
                    logging.warning('Get html: {0}: {1}'.format(e, url))
                    return ''

    def load_post_id(self):
        with open(self.post_id_file, 'r') as fr:
            self.post_id = int(fr.read())

    def save_post_id(self, numb):
        with open(self.post_id_file, 'w') as fw:
            fw.write(str(numb))

    def init_post_id(self):
        with m_lock:
            if not os.path.exists(self.output_dir):
                os.mkdir(self.output_dir)
            if not os.path.exists(self.post_id_file):
                with open(self.post_id_file, 'w') as fw:
                    fw.write('5000000000')

            self.load_post_id()
            logging.info('导入 {} 到队列'.format(str(self.post_id)))
            for post_count in range(self.post_id, self.post_id + self.queue_put_num):
                self.list_url_queue.append(post_count)
            self.save_post_id(int(self.post_id + self.queue_put_num))

    def crawl_post_list(self):
        while True:
            try:
                if not self.list_url_queue:
                    self.init_post_id()

                post_id = self.list_url_queue.pop(0)
                post_id_prefix = re.findall('^[0-9]{6}', str(post_id))
                output_file_path = self.output_dir + str(post_id_prefix[0]) + '/'
                if not os.path.exists(output_file_path):
                    os.makedirs(output_file_path, exist_ok=True)
                post_url = self.seed_url + 'p/' + str(post_id)

            except Exception as e:
                logging.critical('取ID问题: {}'.format(e))
                continue

            try:
                post_html = self.get_html(post_url)
                if not post_html:
                    continue
                post_title = get_title(post_html)
                if post_title == '很抱歉，该贴已被删除。':
                    # logging.error('{}: ---贴子被删---'.format(post_url))
                    continue
                if post_title == '该吧被合并您所访问的贴子无法显示':
                    logging.error('{}: 贴吧被合并无法显示'.format(post_url))
                    continue
                if post_title == '抱歉，您访问的贴子被隐藏，暂时无法访问。':
                    # logging.error('{}: *****帖子被隐藏*****'.format(post_url))
                    continue
                if not post_title:
                    logging.error('{}: 找不到title'.format(post_url))
                    continue
                first_page_content = get_whole_page_content(post_html)
                if not first_page_content:
                    # logging.error('{}: ### 帖子无内容 ###'.format(post_url))
                    continue

                all_content = first_page_content.split('\n\n')
                page_num = get_posts_num(post_html)

                for i in range(page_num):
                    if i != 0:
                        page_url = post_url + '?pn=' + str(i + 1)
                        other_page = self.get_html(page_url)
                        other_content = get_whole_page_content(other_page)
                        all_content = all_content + other_content.split('\n\n')
                if not all_content[-1]:
                    all_content.pop()
                dr = re.compile(r'/|[\\]|[ ]|[|]|[:]|[*]|[<]|[>]|[?]|[\']|["]')
                post_title = dr.sub('_', post_title)
                doc = {
                    'id': post_id,
                    'title': post_title,
                    'content': all_content

                }
                col.insert(doc)
                print(doc)
                # output_file = output_file_path + str(post_id) + '_' + post_title + '.txt'
                # save_content(output_file, all_content)
                logging.info('{0} ---{2}--- {1}'.format(post_id, post_title, str(page_num)))

            except Exception as e:
                logging.critical('尚未预料到的错误: {0} | {1}'.format(e, post_url))
                continue

    def start(self):
        self.init_post_id()

        task = []
        for _ in range(1, self.process_num):
            t = (threading.Thread(target=self.crawl_post_list))
            t.start()
            task.append(t)
        for t in task:
            t.join()

            # processes = []
            # for i in range(1, self.process_num):
            #     t = multiprocessing.Process(target=self.crawl_post_list, args=())
            #     t.start()
            #     processes.append(t)
            # for t in processes:
            #     t.join()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s|PID:%(process)d|%(levelname)s: %(message)s',
                        level=logging.INFO, filename='./log.txt')
    spider = Spider()
    spider.start()
