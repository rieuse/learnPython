from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup
import lxml.html
import pymongo
import re

MONGO_URL = 'localhost'
MONGO_DB = 'amazon'
MONGO_TABLE = 'amazon-python'
SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
KEYWORD = 'python'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
# browser = webdriver.Firefox()
wait = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)


def search():
    print('正在搜索')
    try:
        browser.get('https://www.amazon.cn/')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#twotabsearchtextbox'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#nav-search > form > div.nav-right > div > input')))
        input.send_keys(KEYWORD)
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#pagn > span.pagnDisabled')))
        get_products()
        print('一共' + total.text + '页')
        return total.text
    except TimeoutException:
        return search()


def next_page(number):
    print('正在翻页', number)
    try:
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#pagnNextString'), '下一页'))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#pagnNextString')))
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '.pagnCur'), str(number)))
        get_products()
    except TimeoutException:
        next_page(number)


def get_products():
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#s-results-list-atf')))
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        doc = lxml.html.fromstring(html)
        date = doc.xpath('//*[@class="s-result-item  celwidget "]/div/div[2]/div[1]/span[2]/text()')
        content = soup.find_all(attrs={"id": re.compile(r'result_\d+')})
        for item, time in zip(content, date):
            product = {
                'title': item.find(class_='s-access-title').get_text(),
                'image': item.find(class_='s-access-image cfMarker').get('src'),
                'price': item.find(class_='a-size-base a-color-price s-price a-text-bold').get_text(),
                'date': time
            }
            save_to_mongo(product)
            print(product)
    except Exception as e:
        print(e)


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到mongodb成功', result)
    except Exception:
        print('存储到mongodb失败', result)


def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2, total + 1):
            next_page(i)
    except Exception as e:
        print('出错啦', e)
    finally:
        browser.close()


if __name__ == '__main__':
    main()
