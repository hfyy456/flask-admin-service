import datetime
import pymongo
import configs
import utils.md5 as md5
import random


class Admin:

    def __init__(self):
        try:
            self.db = pymongo.MongoClient(configs.mongoUrl, configs.mongoPort)[configs.dbname]
            self.col = self.db['admin']
        except:
            print(Exception)

    def save(self, data):
        result = self.findByUsername(data['username'])
        if result == None:
            data['password'] = md5.str2md5(data['password'] + data['username'])
            data['createTime'] = datetime.datetime.utcnow()
            self.col.insert_one(data)
            result = data
            del result['password']
            del result['_id']
        else:
            result = None
        return result

    def findByUsername(self, username):
        result = self.col.find_one({'username': username}, {"_id": 0, "password": 0})
        return result

    def findByUsernameAndPassword(self, data):
        data['password'] = md5.str2md5(data['password'] + data['username'])
        result = self.col.find_one(data)
        if result != None:
            del result['password']
            del result['_id']
        return result

    def find(self, data):
        skip = data['pageSize'] * (data['pageNum'] - 1)
        results = self.col.find({}, {"_id": 0, "password": 0}).skip(skip).limit(data['pageSize'])
        count = self.col.find().count()
        totalPage = int(count / data['pageSize']) + 1
        items = []
        for result in results:
            items.append(result)
        print(items)
        page = {'items': items, 'totalPage': totalPage}
        return page

    def update_one(self, username, newValues):
        if 'password' in newValues:
            newValues['password'] = md5.str2md5(newValues['password'] + username)
        self.col.update_one({'username': username}, {'$set': newValues})
        return self.col.find_one({'username': username})

    def delete(self, data):
        result = self.col.delete_one(data)
        return result

    def update_pwd(self,data):
        result=self.col.find_one({'username': data['username']}, {"_id": 0})
        if result['password'] == md5.str2md5(data['oldPass'] + data['username']):
            del data['oldPass']
            result=self.update_one(data['username'],data)
            return result
        else:
            return None

if __name__ == '__main__':
    for i in range(1,20):
        data = {'username': ''.join(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
                'd', 'c', 'b', 'a'], 8)), 'password': 'admin', 'avatarUrl': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif', 'nickName': 'admin',
                'intro': '', 'gender': 'male', 'mobilePhone': '123124125', 'loginTime': datetime.datetime.utcnow(), 'status': '0',
                'role': '1', 'createTime': datetime.datetime.utcnow()}

        admin = Admin()
    # message = admin.save(data)
        result = admin.save(data)
        print(result)
