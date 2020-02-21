import pymongo
import configs
import time
import random
from utils import md5
from bson.objectid import ObjectId

class User:
    def __init__(self):
        try:
            self.db = pymongo.MongoClient(configs.mongoUrl, configs.mongoPort)[configs.dbname]
            self.col = self.db['user']
        except:
            print(Exception)
    def save(self, data):
        result = self.findByUsername(data['username'])
        if result == None:
            data['password'] = md5.str2md5(data['password'] + data['username'])
            data['createTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
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

    def findById(self,id):
        return self.col.find_one({'_id':ObjectId(id)})

if __name__ == '__main__':
    for i in range(1,20):
        data = {'username': ''.join(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
             'd', 'c', 'b', 'a'], 8)), 'password': 'admin', 'avatarUrl': '', 'nickName': 'user',
            'intro': '', 'gender': 'male', 'mobilePhone': '123124125', 'loginTime': '', 'status': '0',
            'role': '1', 'createTime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'openID': ''}
        user = User()
        user.save(data)