from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs')  # 构建无头浏览器，用来解析 Js 加载内容

driver.get('https://www.shanbay.com/read/news/')

time.sleep(5)  # 显式延时5秒，等待页面完全加载

try:
    load_more_btn = driver.find_element_by_class_name('loadNewsBtn')  #"加载更多"按钮
    load_more_btn.click()   #点击这个按钮
except:
    print('error')
soup = BeautifulSoup(driver.page_source,'html.parser')
# print(driver.page_source)
tags = soup.find_all('a',attrs={'class':'linkContainer'})
time.sleep(5)
for i in tags:
    print(i.attrs['href'])

