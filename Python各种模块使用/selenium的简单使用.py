from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs')  # 构建无头浏览器，用来解析 Js 加载内容
# driver = webdriver.Firefox()
driver.get('https://www.shanbay.com/read/news/')

time.sleep(5)  # 显式延时5秒，等待页面完全加载
soup = BeautifulSoup(driver.page_source, 'lxml')
# print(driver.page_source)
tags = soup.find_all('a', attrs={'class': 'linkContainer'})
# for i in tags:
#     print(i['href'])
# driver.find_element_by_id('kw').send_keys(keyword)
# driver.find_element_by_id('su').click()
# for i in range(1,81):
#     driver.find_element_by_class_name('icon-refresh').send_keys(Keys.DOWN)
'''这将给你屏幕截图在那一刻图像将被保存在你的脚本的工作'''
try:
    driver.get('http://whatsmyuseragent.com/')

except Exception as e:
    driver.save_screenshot('screenshot.png')
