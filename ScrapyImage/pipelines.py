# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class ScrapyimagePipeline(object):
    def process_item(self, item, spider):
        
        print('*************')
        print(item)

        image = requests.get(item['download'])

        with open(item['filepath'], 'wb') as f:
            f.write(image.content)

        print('*************')

        return item

class MyImagesPipeline(ImagesPipeline):
    @classmethod
    def get_media_requests(self, item , info):
        print('*************')
        print(item)
        yield scrapy.Request(item['download'])

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        #item['file_paths'] = file_paths
        return item
