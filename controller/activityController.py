import datetime
import json
from utils.jwt import Jwt
from models.activity import Activity
from utils.dumps import response
class Controller:
    def __init__(self):
        self.activity = Activity()
    def create(self, request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            data['creator'] = res['data']['username']
            result = self.activity.save(data)
            if result == None:
                return response({}, code=50000, message='该广告已存在！')
            return response({}, code=20000, message='创建成功！')
        else:
            return p
    def getList(self, request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            result = self.activity.findAll()
            return response(result, code=20000, message='获取成功！')
        else:
            return p
            return p

    def edit(self, request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            result = self.activity.update_one(data['id'], data)
            if result == None:
                return response({}, code=50000, message='该广告已存在！')
            return response({}, code=20000, message='修改成功！')
        else:
            return p
    def delete(self,request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            result = self.activity.delete(data)
            print(type(result))
            return response({}, code=20000, message='删除成功！')
        else:
            return p

