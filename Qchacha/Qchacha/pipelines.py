# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import Qchacha.settings as conf


class QchachaPipeline(object):


    def __init__(self):
        self.client = pymongo.MongoClient(conf.mongo_host, conf.mongo_port)
        self.db = self.client[conf.mongo_db]
        self.collection = self.db['QchachaAll']

    def process_item(self, item, spider):

        res = dict(item)
        self.collection.insert(res)
        return item


    def __del__(self):
        self.client.close()