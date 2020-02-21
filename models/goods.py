import pymongo
import configs
import datetime
import random
from bson.objectid import ObjectId

class Goods:
    def __init__(self):
        try:
            self.db = pymongo.MongoClient(configs.mongoUrl, configs.mongoPort)[configs.dbname]
            self.col = self.db['good']
            self.cate=self.db['category']
        except:
            print(Exception)

    def save(self, data):
        data['createTime'] = datetime.datetime.utcnow()
        data['price'] = float(data['price'])
        return self.col.insert_one(data)

    def findByName(self, name):
        result = self.col.find_one({'name': name})
        return result

    def find(self,data):
        skip = data['pageSize'] * (data['pageNum'] - 1)
        results = self.col.find({data['queryType']: {'$regex': data['query'],'$options':"$i"}}).skip(skip).limit(
            data['pageSize'])
        count = self.col.find().count()
        totalPage = int(count / data['pageSize']) + 1
        items = []
        for result in results:
            result['id']=str(result['_id'])
            del result['_id']
            category=self.cate.find_one({'_id':ObjectId(result['categoryId'])})
            result['categoryName']=category['series']+'/'+category['name']
            items.append(result)
        print(items)
        page = {'items': items, 'totalPage': totalPage}
        return page
    def update_one(self, id, newValues):
        result = self.findByName(newValues['name'])
        if result==None:
            self.col.update_one({'_id': ObjectId(id)}, {'$set': newValues})
            return self.col.find_one({'_id': ObjectId(id)})
        else:
            fid = str(result['_id'])
            if fid == id:
                self.col.update_one({'_id': ObjectId(id)}, {'$set': newValues})
                return self.col.find_one({'_id': ObjectId(id)})
            else:
                return None
    def delete(self, data):
        result = self.col.delete_one(data)
        return result
if __name__ == '__main__':
    for i in range(1,20):
        data = {'name': ''.join(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
             'd', 'c', 'b', 'a'], 8)), 'image': 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=1740009991,843281789&fm=26&gp=0.jpg','images':'','categoryId': '',
            'adminId': '', 'intro': '', 'price': '12.00', 'status': '0',
            'key': 'WCS.2008', 'createTime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'count': '1',
            'address':'','VIN':'LSVG026R9F2086645'}
        good = Good()
        good.save(data)