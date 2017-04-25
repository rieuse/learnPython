import urllib.request
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup
url = 'http://www.8she.com/31988.html'
res = urllib.request.urlopen(url)
# html1 = BeautifulSoup(res)
# print(html1)
# try:
#     print(html1)
# except HTTPError as e:
#     print(e)
# else:
#     print('error')
html = res.read().decode('utf-8')
soup = BeautifulSoup(html,'html.parser')
print(soup)