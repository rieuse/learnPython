import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
# r = requests.get('http://www.toutiao.com/a6394874942794793217/#p={}'.format(str(i)for i in range(1,6)))
# print(r.status_code)

def toutiao(url):
    r = urllib.request.urlopen(url)
    html = r.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    result1 = soup.xpath('/html/body/div/div[4]/div[1]/div[1]/div/div[1]/div/ul/li[2]/div/img')
    # result = soup.find_all('img', limit=6)
    print(result1)
    # links = []
    # for content in result:
    #     links.append(content.get('src'))
    # if not os.path.exists('toutiao'):
    #     os.makedirs('toutiao')
    # i = 0
    # for link in links:
    #     i += 1
    #     filename = 'toutiao\\' + 'toutiao' + str(i) + '.jpg'
    #     with open(filename, 'w') as file:
    #         urllib.request.urlretrieve(link, filename)

url = 'http://www.toutiao.com/a6402018208622510337/#p=1'

if __name__ == '__main__':
    toutiao(url)

