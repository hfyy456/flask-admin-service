import json
from utils.jwt import Jwt
from models.order import Order
from utils.dumps import response
class Controller:
    def __init__(self):
        self.order = Order()

    def getList(self, request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            result = self.order.find(data)
            return response(result, code=20000, message='获取成功！')
        else:
            return p
    def edit(self,request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            result = self.order.update_one(data['id'], data)
            return response({}, code=20000, message='修改成功！')
        else:
            return p

    def delete(self, request):
            p = Jwt.authHeader(request)
            res = json.loads(p)
            if res['code'] == 20000:
                data = json.loads(request.get_data())
                id = data['id']
                result = self.order.delete(id)
                print(type(result))
                return response({}, code=20000, message='删除成功！')
            else:
                return p