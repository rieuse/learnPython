import requests
from parsel import Selector

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Accept': 'application/json',
    'X-Request': 'JSON',
    'X-Requested-With': 'XMLHttpRequest'
}
url = 'http://huaban.com/pins/1042999055/'
request = requests.get(url, headers=headers)
doc = Selector(request.text)
link = doc.xpath('//*[@id="baidu_image_holder"]/a/img')
print(link)
