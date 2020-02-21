import json
from utils.jwt import Jwt
from models.category import Category
from utils.dumps import response


class Controller:
    def __init__(self):
        self.category = Category()

    def create(self, request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            data['creator'] = res['data']['username']
            result = self.category.save(data)
            if result == None:
                return response({}, code=50000, message='该分类已存在！')
            return response({}, code=20000, message='创建成功！')
        else:
            return p

    def getList(self, request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            result = self.category.find(data)
            return response(result, code=20000, message='获取成功！')
        else:
            return p
    def delete(self,request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            result = self.category.delete(data)
            print(type(result))
            return response({}, code=20000, message='删除成功！')
        else:
            return p
    def edit(self,request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            result = self.category.update_one(data['id'],data)
            if result == None:
                return response({}, code=50000, message='该分类已存在！')
            return response({}, code=20000, message='修改成功！')
        else:
            return p
    def delete(self,request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            result = self.category.delete(data)
            print(type(result))
            return response({}, code=20000, message='删除成功！')
        else:
            return p
    def getCascader(self,request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            results=self.category.findAll()
            series = []
            for result in results:
                series.append(result['series'])
            formatList = list({}.fromkeys(series).keys())
            data = []
            for i in formatList:
                children = []
                for result in results:
                    if result['series'] == i:
                        children.append({"label": result['label'], "value": result['value']})
                data.append({"value": i, "label": i, "children": children})
            return response(data, code=20000, message='获取成功！')
        else:
            return p

