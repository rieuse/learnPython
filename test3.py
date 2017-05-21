from selenium.common.exceptions import TimeoutException
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
wait = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)


def get_url():
    url = 'http://huaban.com/boards/favorite/beauty/'
    browser.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Board wfc')))
    html = browser.page_source
    doc = lxml.html.fromstring(html)
    for item in doc.xpath('//*[@id="waterfall"]/div/a/@href'):
        url = 'http://huaban.com' + item


def dowload(ur):
    url = 'http://huaban.com/boards/28040275/'
    browser.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#waterfall')))

    html = browser.page_source
    doc = lxml.html.fromstring(html)
    if not os.path.exists('image'):
        os.makedirs('image')

    link = doc.xpath('//*[@id="waterfall"]/div/a/img/@src')

    i = 0
    for item in link:
        i += 1
        url = 'http:' + item
        r = requests.get(url)
        filename = 'image\\' + str(i) + '.jpg'
        with open(filename, 'wb') as fo:
            fo.write(r.content)
