import urllib.request
import lxml.html
url = 'http://news.ifeng.com/listpage/11502/0/1/rtlist.shtml'
r = urllib.request.urlopen(url)
html = r.read().decode('utf-8')
doc = lxml.html.fromstring(html)
info = doc.xpath('//div[@class="newsList"]/ul[1]/li/a/text()')
href = doc.xpath('//div[@class="newsList"]/ul[1]/li/a/@href')
i = 0
all = []
for content in info:
    title = info
    link = href
    results = {
        '标题':title[i],
        '链接':link[i]
    }
    i += 1
    print(results)