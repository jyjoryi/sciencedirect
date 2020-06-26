# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class SciencedirectPipeline(object):

    def __init__(self):
        #Create connection variable
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )

        #Create database
        db = self.conn['science_direct']

        #Create table/collection
        self.collection = db['science_direct_abstract']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
