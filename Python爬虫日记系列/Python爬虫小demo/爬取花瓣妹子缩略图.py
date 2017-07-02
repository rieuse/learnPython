from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import requests
import lxml.html
import os

SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
# browser = webdriver.Firefox()
wait = WebDriverWait(browser, 15)
browser.set_window_size(1400, 900)


def get_url():
    print('打开主页搜寻链接中...')
    try:
        browser.get('http://huaban.com/boards/favorite/beauty/')
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#waterfall')))
        html = browser.page_source
        doc = lxml.html.fromstring(html)
        name = doc.xpath('//*[@id="waterfall"]/div/a[1]/div[2]/h3/text()')
        u = doc.xpath('//*[@id="waterfall"]/div/a[1]/@href')
        for item, fileName in zip(u, name):
            url = 'http://huaban.com' + item
            print('主链接已找到：' + url)
            if '*' in fileName:
                fileName = fileName.replace('*', '')
            dowload(url, fileName)
    except Exception as e:
        print(e)


def dowload(url, fileName):
    try:
        browser.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#waterfall')))
        html = browser.page_source
        doc = lxml.html.fromstring(html)
        if not os.path.exists('image2\\' + fileName):
            os.makedirs('image2\\' + fileName)
        link = doc.xpath('//*[@id="waterfall"]/div/a/img/@src')
        i = 0
        for item in link:
            i += 1
            ur = 'http:' + item
            print('正在下载第' + str(i) + '张图片，地址：' + ur)
            r = requests.get(ur)
            filename = 'image2\\{}\\'.format(fileName) + str(i) + '.jpg'
            with open(filename, 'wb') as fo:
                fo.write(r.content)
    except Exception:
        print('本次出错了')


if __name__ == '__main__':
    get_url()
