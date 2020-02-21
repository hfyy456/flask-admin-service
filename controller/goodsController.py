import json
from utils.jwt import Jwt
from models.goods import Goods
from utils.dumps import response
class Controller:
    def __init__(self):
        self.goods = Goods()

    def create(self, request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            data['creator'] = res['data']['username']
            result = self.goods.save(data)
            return response({}, code=20000, message='创建成功！')
        else:
            return p

    def getList(self,request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            if data['searchType'] == 'search':
                data['queryType'] = 'name'
                results=self.goods.find(data)
            else:
                data['queryType']='categoryId'
                results=self.goods.find(data)
            return response(results, code=20000, message='获取成功！')
        else:
            return p

    def edit(self,request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            result = self.goods.update_one(data['id'], data)
            if result == None:
                return response({}, code=50000, message='该商品名已存在！')
            return response({}, code=20000, message='修改成功！')
        else:
            return p

    def delete(self, request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            result = self.goods.delete(data)
            return response({}, code=20000, message='删除成功！')
        else:
            return p
