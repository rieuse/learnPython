import multiprocessing
import requests
from lxml import etree
import time

# pc_gn_urls

# def  poor(url):
#     try:
#         print(url)
#         html2 = requests.get(url).content.decode('gbk')
#         doc2 = etree.HTML(html2).xpath('//*[@id="cont_1_1_2"]/div/p/text()')
#         # print(doc2)
#         with open('content\\pc_gn_content.txt', 'a',encoding='utf-8') as fi:
#             fi.write(''.join(doc2) + '\n')
#     except Exception as e:
#         print(e)
#         pass
# if __name__ == '__main__':
#     urls = []
#     name = input('input txt name:   ')
#     with open('{}.txt'.format(name),'r') as f:
#         for url in f.readlines():
#             urls.append(url[:-1])
#     pool = multiprocessing.Pool(4)  # 使用4个进程
#     pool.map(poor, urls)  # map函数就是把后面urls列表中的url分别传递给method_2()函数
#     pool.close()
#     pool.join()



name = input('input txt name:   ')
with open('{}.txt'.format(name), 'r') as f:
    for url in f.readlines():
        print(url[:-1])
        try:
            html2 = requests.get(url[:-1]).content.decode('gbk')
            doc2 = etree.HTML(html2).xpath('//*[@id="cont_1_1_2"]/div/p/text()')
            # print(doc2[0])
            with open('content\\{}_content.txt'.format(name[:5]), 'a', encoding='utf-8') as fi:
                fi.write(''.join(doc2) + '\n')
        except Exception as e:
            print(e)
            continue
