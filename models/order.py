import pymongo
import configs
import datetime
import random
from bson.objectid import ObjectId

class Order:

    def __init__(self):
        try:
            self.db = pymongo.MongoClient(configs.mongoUrl, configs.mongoPort)[configs.dbname]
            self.col = self.db['order']
            self.good = self.db['good']
        except:
            print(Exception)

    def save(self,data):
        data['createTime'] = datetime.datetime.utcnow()
        return self.col.insert_one(data)

    def findById(self,id):
        return self.col.find_one({'_id':ObjectId(id)})

    def find(self,data):
        skip = data['pageSize'] * (data['pageNum'] - 1)
        results = self.col.find({data['queryType']: {'$regex': data['query']}}).skip(skip).limit(
            data['pageSize'])
        count = self.col.find().count()
        totalPage = int(count / data['pageSize']) + 1
        items = []
        for result in results:
            result['id'] = str(result['_id'])
            good=self.good.find_one({"_id":ObjectId(result['goodId'])})
            if good != None:
                result['goodName']=good['name']
            else:
                result['goodName'] = "该商品已不存在"
            del result['_id']
            items.append(result)
        print(items)
        page = {'items': items, 'totalPage': totalPage}
        return page

    def update_one(self, id, newValues):
        del newValues['createTime']
        del newValues['id']
        del newValues['goodName']
        self.col.update_one({'_id': ObjectId(id)}, {'$set': newValues})
        return self.col.find_one({'_id': ObjectId(id)})
    def delete(self, id):
        result = self.col.delete_one({'_id': ObjectId(id)})
        return result