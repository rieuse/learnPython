from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
driver.get('http://bbs.myquark.cn/')
cookie = driver.get_cookies()
driver.quit()
print(cookie)
