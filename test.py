from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs')
driver.get('http://www.toutiao.com/ch/news_tech/')
time.sleep(3)
soup = BeautifulSoup(driver.page_source, 'lxml')
articles = []
for article in soup.find_all(class_='item', ga_event="article_item_click"):
    tags = article.get_text()
    print(article)
    # print(tags)
