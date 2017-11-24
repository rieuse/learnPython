import requests
from lxml import etree
import time

file = input('请输入文件名：  ')
with open(file, 'r') as f:
    for url in f.readlines():
        if 'com/m' in url[:-1]:
            print(url[:-1])
            try:
                html1 = requests.get(url[:-1]).content.decode('utf-8')
                doc1 = etree.HTML(html1).xpath('//*[@id="backtop"]/div[6]/p/text()')
                with open('content\\content_{}'.format(file), 'a') as fi:
                    fi.write(''.join(doc1))
                    time.sleep(0.01)
            except:
                print('error')
                pass
                # else:
                #     print(url[:-1])
                #     html2 = requests.get(url[:-1]).content.decode('gbk')
                #     doc2 = etree.HTML(html2).xpath('//*[@id="cont_1_1_2"]/div/p/text()')
                #     # print(doc2)
                #     with open('gj_source_content.txt', 'a') as fi:
                #         fi.write(''.join(doc2))
