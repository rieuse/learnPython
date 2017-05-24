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
            if '*' in fileName:
                fileName = fileName.replace('*', '')
            dowload(url, fileName)
    except Exception as e:
        print(e)


def dowload(url, fileName):
    print('准备下载中...')
    try:
        browser.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#waterfall')))
        html = browser.page_source
        doc = lxml.html.fromstring(html)
        if not os.path.exists('image\\' + fileName):
            os.makedirs('image\\' + fileName)
        link = doc.xpath('//*[@id="waterfall"]/div/a/img/@src')
        i = 0
        for item in link:
            i += 1
            ur = 'http:' + item
            r = requests.get(ur)
            filename = 'image\\{}\\'.format(fileName) + str(i) + '.jpg'
            with open(filename, 'wb') as fo:
                fo.write(r.content)
    except Exception as e:
        print(e)
        return


if __name__ == '__main__':
    get_url()
