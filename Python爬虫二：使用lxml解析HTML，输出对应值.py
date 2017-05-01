import requests
import lxml.html

url = 'http://news.ifeng.com/listpage/11502/0/1/rtlist.shtml'
html = requests.get(url).text
doc = lxml.html.fromstring(html)
titles = doc.xpath('//div[@class="newsList"]/ul/li/a/text()')
href = doc.xpath('//div[@class="newsList"]/ul/li/a/@href')
i = 0
for content in titles:
    results = {
        '标题': titles[i],
        '链接': href[i]
    }
    i += 1
    print(results)
