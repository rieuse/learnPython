from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    # 'Cache-Control':'no-cache',
    # 'Connection': 'keep-alive',
    'Host': 'channel.chinanews.com',
    # 'Pragma':'no-cache',
    'Upgrade-Insecure-Requests': '1',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.16232', # enge
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
# chrome
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36', # 360chrome
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER', # liebao
    'Cookie': '__jsluid=b65f0102317c5e8d7a8e877455d73309; __jsl_clearance=1500210265.392|0|SkjU77r4IrAqDlfm1RLjAgoV%2Bek%3D'
}

for i in range(13, 387):
    data = {
        'pager': str(i),
        'pagenum': '400',
    }
    url = 'http://channel.chinanews.com/cns/s/channel:life.shtml?pager={}&pagenum={}'.format(data['pager'],
                                                                                             data['pagenum'])
    print('解析网页：' + url)
    browser = webdriver.Chrome()
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    time.sleep(6)
    html = browser.page_source
    try:
        # print(html[101:-18].strip())
        ls = json.loads(html[101:-18].strip())
        with open('pc_life_urls.txt', 'a') as f:
            for item in ls:
                print(item['url'])
                if not 'shipin' in item['url']:
                    f.writelines(item['url'] + '\n')
            print('插入一页完毕')
            browser.close()
    except Exception as e:
        print(e)
        browser.close()
        continue
