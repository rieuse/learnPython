import requests

url = 'https://www.ithome.com/list/2011-05-15.html'
html = requests.get(url).text
print(html)
