# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
import os
import requests


class DoutuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    img_url = scrapy.Field()
    name = scrapy.Field()

# class ImageloadItem(scrapy.Item):
#     img_url = scrapy.Field()
#     name = scrapy.Field()



# if not os.path.exists('doutu'):
#     print('创建文件夹...')
#     os.makedirs('doutu')
# with open('json.json','w') as f:
#     f.write(img_url['img_url'])
# r = requests.get('http:' + str(img_url))
# filename = 'doutu\\{}'.format(name) + '.gif'
# with open(filename, 'wb') as fo:
#     fo.write(r.content)
