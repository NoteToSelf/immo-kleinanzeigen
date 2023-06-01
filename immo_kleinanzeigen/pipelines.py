# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

from itemadapter import ItemAdapter
import pymongo

from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.collection.insert_one(adapter.asdict())
        logging.info(f"Real estate entered (id: '{adapter['_id']}')")
        return item


class DuplicatesPipeline:
    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.ids_seen = set()

        for item in self.collection.find():
            self.ids_seen.add(item['_id'])

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['_id'] in self.ids_seen:
            raise DropItem(f"Duplicate item '{adapter['_id']}' found")
        else:
            self.ids_seen.add(adapter['_id'])
            return item
