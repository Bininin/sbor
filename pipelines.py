from itemadapter import ItemAdapter
from pymongo import MongoClient

class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.instagram

    def process_item(self, item, spider):
        collection = self.mongobase[item.get('username')]
        collection.insert_one(item)
        return item