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


linkss = []


def start():
    # print('打开主页搜寻链接中...')
    # try:
    doc = parser('http://huaban.com/boards/favorite/beauty/', '#waterfall')
    href = doc.xpath('//*[@id="waterfall"]/div/a[1]/@href')
    for item in href:
        main_url = 'http://huaban.com' + item
        #       print(main_url)
        download(main_url)
        # except Exception as e:
        #     print(e)


link = ['http://huaban.com/boards/27908318/']


def download(link):
    print('-------准备下载中-------')
    for item in link:
        doc = parser(item, '#waterfall')
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
            linkss.append(url)
        print(linkss)


if __name__ == '__main__':
    start_time = time.time()
    start()
    # download(link)
    # one.start()
    # two.start()
    end_time = time.time()
    print(start_time - end_time)
