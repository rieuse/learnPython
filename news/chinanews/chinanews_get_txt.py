import requests
from lxml import etree
import importlib

# url1 = 'http://www.chinanews.com/m/kong/2017/05-05/8216106.shtml'  # 手机端接口
url2 = 'http://www.chinanews.com/gj/2015/06-11/7337348.shtml'
# html1 = requests.get(url).content.decode('utf-8')
# doc1 = etree.HTML(html1).xpath('//*[@id="backtop"]/div[6]/p/text()')
# print(''.join(doc1))


html2 = requests.get(url2).content.decode('gbk')
# print(html2)
doc2 = etree.HTML(html2).xpath('//*[@id="cont_1_1_2"]/div/p/text()')
print(''.join(doc2))
