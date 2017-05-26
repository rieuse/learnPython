__author__ = '布咯咯_rieuse'

import os, re, time
import lxml.html
import requests, threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
# browser = webdriver.Firefox()
wait = WebDriverWait(browser, 5)
browser.set_window_size(1400, 900)


def parser(url, param):
    # 解析模块
    browser.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, param)))
    html = browser.page_source
    doc = lxml.html.fromstring(html)
    return doc


link1 = []
link2 = []


class Thread1(threading.Thread):
    def __init__(self, link):
        threading.Thread.__init__(self)
        self.link = link

    def run(self):
        print('线程1开始')
        print(self.link)
        download(link1)
        print('线程1结束')


class Thread2(threading.Thread):
    def __init__(self, link):
        threading.Thread.__init__(self)
        self.link = link

    def run(self):
        print('线程2开始')
        print(self.link)
        download(link2)
        print('线程2结束')


one = Thread1(link1)
two = Thread2(link2)


def start():
    print('打开主页搜寻链接中...')
    try:
        doc = parser('http://huaban.com/boards/favorite/beauty/', '#waterfall')
        href = doc.xpath('//*[@id="waterfall"]/div/a[1]/@href')
        for item in href:
            main_url = 'http://huaban.com' + item
            num = int(re.findall('\d{8}', main_url)[0])
            if (num % 2) == 0:
                link2.append(main_url)
            else:
                link1.append(main_url)
    except Exception:
        print('出错了！：all_url')


def download(link):
    print('-------准备下载中-------')
    for item in link:
        doc = parser(item, '#waterfall')
        doc2 = parser(item, '#board_card')
        name = doc2.xpath('//*[@id="board_card"]/div[1]/div[1]/h1/text()')
        fileName = name[0]
        if '*' in fileName:
            fileName = fileName.replace('*', '')
        if not os.path.exists('image2\\' + fileName):
            print('创建文件夹...')
            os.makedirs('image2\\' + fileName)
        links = doc.xpath('//*[@id="waterfall"]/div/a/@href')
        # print(links)
        i = 0
        for item in links:
            i += 1
            minor_url = 'http://huaban.com' + item
            doc = parser(minor_url, '#pin_view_page')
            img_url = doc.xpath('//*[@id="baidu_image_holder"]/a/img/@src')
            img_url2 = doc.xpath('//*[@id="baidu_image_holder"]/img/@src')
            img_url += img_url2
            url = 'http:' + str(img_url[0])
            print('正在下载第' + str(i) + '张图片，地址：' + url)
            r = requests.get(url)
            filename = 'image2\\{}\\'.format(fileName) + str(i) + '.jpg'
            with open(filename, 'wb') as fo:
                # pass
                fo.write(r.content)


if __name__ == '__main__':
    # start_time = time.time()
    start()
    one.start()
    two.start()
    # end_time = time.time()
    # print(start_time - end_time)
