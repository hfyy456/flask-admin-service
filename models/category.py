import pymongo
import configs
import datetime
from bson.objectid import ObjectId

class Category:
    def __init__(self):
        try:
            self.db = pymongo.MongoClient(configs.mongoUrl, configs.mongoPort)[configs.dbname]
            self.col = self.db['category']
        except:
            print(Exception)

    def save(self, data):
        result = self.findByName(data['name'])
        if result == None:
            data['count'] = 0
            if data['cover'].find('http') == -1:
                data['cover'] = configs.root + data['cover']
            data['createTime'] = datetime.datetime.utcnow()
            return self.col.insert_one(data)
        else:
            return None

    def findByName(self, name):
        result = self.col.find_one({'name': name})
        return result

    def findAll(self):
        results=self.col.find()
        items= []
        for result in results:
            item = dict()
            item['value']=str(result['_id'])
            item['label']=result['name']
            item['series']=result['series']
            items.append(item)
        return items

    def find(self, data):
        skip = data['pageSize'] * (data['pageNum'] - 1)
        results = self.col.find({data['queryType']: {'$regex': data['query']}}).skip(skip).limit(
            data['pageSize'])
        count = self.col.find().count()
        totalPage = int(count / data['pageSize']) + 1
        items = []
        for result in results:
            result['id']=str(result['_id'])
            del result['_id']
            items.append(result)
        print(items)
        page = {'items': items, 'totalPage': totalPage}
        return page

    def update_one(self, id, newValues):
        result = self.findByName(newValues['name'])
        if result==None:
            if newValues['cover'].find('http') ==-1 :
                newValues['cover']=configs.root+newValues['cover']
            self.col.update_one({'_id': ObjectId(id)}, {'$set': newValues})
            return self.col.find_one({'_id': ObjectId(id)})
        else:
            fid = str(result['_id'])
            if fid == id:
                if newValues['cover'].find('http') == -1:
                    newValues['cover'] = configs.root + newValues['cover']
                self.col.update_one({'_id': ObjectId(id)}, {'$set': newValues})
                return self.col.find_one({'_id': ObjectId(id)})
            else:
                return None
    def delete(self, data):
        result = self.col.delete_one(data)
        return result
if __name__ == '__main__':
    category=Category()
    results=category.findAll()
    series=[]
    for result in results:
        series.append(result['series'])
    formatList = list({}.fromkeys(series).keys())
    data=[]
    for i in formatList:
        children=[]
        for result in results:
            if result['series']==i:
                children.append({"label":result['label'],"value":result['value']})
        data.append({"value": i,"lable": i, "children":children})
    print(data)
