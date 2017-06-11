# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import os


class ScrapystudyPipeline(object):
    def process_item(self, item, spider):
        return item



        # def download_img(img_url, name):
        #     if not os.path.exists('doutu'):
        #         print('创建文件夹...')
        #         os.makedirs('doutu')
        #     r = requests.get(img_url)
        #     filename = 'doutu\\{}'.format(name) + '.gif'
        #     with open(filename, 'wb') as fo:
        #         fo.write(r.content)
