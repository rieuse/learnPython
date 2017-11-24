from lxml import etree

import requests

url = 'https://dyn.ithome.com/ithome/getajaxdata.aspx'
data = {
    'newsID': '326707',
    'hash': 'A379730C87B522EA',
    'type': 'commentpage',
    'page': '3',
    'order': 'false',
}
html = requests.post(url, data=data).text
print(html)


# urls = 'https://dyn.ithome.com/comment/326707'
# html =requests.post(urls).text
# print(html)
