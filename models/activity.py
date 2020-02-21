import datetime
import pymongo
from bson import ObjectId
import configs

class Activity:

    def __init__(self):
        try:
            self.db = pymongo.MongoClient(configs.mongoUrl, configs.mongoPort)[configs.dbname]
            self.col = self.db['active']
        except:
            print(Exception)

    def save(self, data):
        if 'id' in data:
            del data['id']
        data['createTime'] = datetime.datetime.utcnow()
        return self.col.insert_one(data)

    def update_one(self, id, newValues):
        del newValues['id']
        self.col.update_one({'_id': ObjectId(id)}, {'$set': newValues})
        return self.col.find_one({'_id': ObjectId(id)})

    def findAll(self):
        results = self.col.find()
        items = []
        for result in results:
            result['id'] = str(result['_id'])
            del result['_id']
            items.append(result)
        return items
    def delete(self, id):
        result = self.col.delete_one({'_id': ObjectId(id)})
        return result
