from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import csv, time

driver = webdriver.Firefox()
first_url = 'http://www.yidianzixun.com/channel/c6'
driver.get(first_url)
time.sleep(1)
driver.find_element_by_class_name('icon-refresh').click()
for i in range(1, 90):
    driver.find_element_by_class_name('icon-refresh').send_keys(Keys.DOWN)
time.sleep(3)
soup = BeautifulSoup(driver.page_source, 'lxml')
articles = []
for article in soup.find_all(class_='item doc style-small-image style-content-middle'):
    title = article.find(class_='doc-title').get_text()
    source = article.find(class_='source').get_text()
    comment = article.find(class_='comment-count').get_text()
    link = 'http://www.yidianzixun.com' + article.get('href')
    articles.append([title, source, comment, link])
driver.quit()
with open(r'document\yidian.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['文章标题', '作者', '评论数', '文章地址'])
    for row in articles:
        writer.writerow(row)
