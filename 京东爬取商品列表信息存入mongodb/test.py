import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pymongo

# MONGO_URL = 'localhost'
# MONGO_DB = 'jingdong'
# MONGO_TABLE = 'product'
SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
KEYWORD = '连衣裙'
# client = pymongo.MongoClient(MONGO_URL)
# db = client[MONGO_DB]

browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)


def search():
    print('正在搜索')
    try:
        browser.get('https://www.jd.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#key'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#search > div > div.form > button')))
        input.send_keys(KEYWORD)
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > em:nth-child(1) > b')))
        # get_products()
        return total.text
    except TimeoutException:
        return search()


def next_page(page_number):
    print('正在翻页', page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > input'))
        )
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > a')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'), str(page_number)))
        # get_products()
    except TimeoutException:
        next_page(page_number)


# def get_products():
#     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList > ul > li > div')))
#     html = browser.page_source
#     doc = BeautifulSoup(html, 'lxml')
#     items = doc('#J_goodsList > ul > li > div').items()
#     for item in items:
#         product = {
#             'image': item.find('.p-img > a > img').attr('src'),
#             'price': item.find('.p-price').text()[1:],
#             'deal': item.find('.p-commit').text(),
#             'title': item.find('.p-name-type-2').text(),
#             'shop': item.find('.p-shop .J_im_icon .a').attr('title')
#         }
#         print(product)
def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList > ul > li > div')))
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    # items = soup.find_all(class_='gl-warp clearfix')
    items = []
    for item in soup.find_all(class_='gl-warp clearfix'):
        image = item.find(class_='err-product').get('src')
        price = item.select('#J_goodsList > ul > li > div > div.p-price > strong')
        deal = item.find(class_='p-commit').get_text()[3:]
        # title = item.select('#J_goodsList ul li div')[0]
        # shop = item.find(class_='p-shop').get('title')
        # items.append([image, price, deal, title , shop])
        print(price)
        # print(items)


search()
get_products()
browser.close()
# def main():
#     try:
#         total = search()
#         total = int(re.compile('(\d+)').search(total).group(1))
#         for i in range(2, total + 1):
#             next_page(i)
#     except Exception:
#         print('出错啦')
#     # finally:
#     #     browser.close()
#
# if __name__ == '__main__':
#     main()
