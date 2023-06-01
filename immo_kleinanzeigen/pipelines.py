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
        self.collection.create_index([('id', pymongo.ASCENDING), ('hash', pymongo.ASCENDING)], unique=True)

    def process_item(self, item, spider):
        # found_existing = self.collection.count_documents({'id': item.get_id(), 'hash': item.get_hash()})
        # if found_existing > 0:
        #     raise DropItem(f"Duplicate item '{item.get_id()}' found with hash '{item.get_hash()}'")
        # else:
            self.collection.insert_one(ItemAdapter(item).asdict())
            logging.info(f"Real estate entered (id: '{item.get_id()}', hash: '{item.get_hash()}')")
            return item


class HashDuplicatesPipeline:
    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.hash_seen = set()

        for item in self.collection.find():
            self.hash_seen.add(item['hash'])

    def process_item(self, item, spider):
        item.set_hash(hash(item))
        if item.get_hash() in self.hash_seen:
            raise DropItem(f"Duplicate item '{item.get_id()}' found with hash '{item.get_hash()}'")
        else:
            self.hash_seen.add(item.get_hash())
            return item
