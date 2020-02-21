import datetime
import json
from utils.jwt import Jwt
from models.admin import Admin
from utils.dumps import response




class Controller:
    def __init__(self):
        self.admin = Admin()

    def login(self, request):
        data = json.loads(request.get_data())
        result = self.admin.findByUsernameAndPassword(data)
        if result == None:
            return response(result, code=50000, message='账号或密码错误！')
        else:
            loginTime=datetime.datetime.utcnow()
            self.admin.update_one(result['username'],{'loginTime':loginTime})
            auth={'username':result['username'],'role':result['role']}
            data={}
            data['token']=Jwt.jwtEncode(auth).decode('utf-8')
            return response(data, code=20000, message='登陆成功！')

    def getInfo(self,request):
        p=Jwt.authHeader(request)
        res=json.loads(p)
        if res['code']==20000:
            result=self.admin.findByUsername(res['data']['username'])
            return response(result, code=20000, message='获取成功！')
        else:
            return p

    def logout(self):
        return response({}, code=20000, message='登出成功！')

    def getList(self,request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            result = self.admin.find(data)
            return response(result, code=20000, message='获取成功！')
        else:
            return p

    def delete(self,request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            result = self.admin.delete(data)
            print(type(result))
            return response({}, code=20000, message='删除成功！')
        else:
            return p
    def edit(self,request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            if 'username' in data:
                result = self.admin.update_one(data['username'],data)
            else:
                data['username']==res['username']
                result = self.admin.update_one(data['username'],data)
            print(type(result))
            return response({}, code=20000, message='修改成功！')
        else:
            return p

    def create(self,request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            data = json.loads(request.get_data())
            result=self.admin.save(data)
            if result==None:
                return response({}, code=50000, message='该用户名已存在！')
            return response({}, code=20000, message='创建成功！')
        else:
            return p

    def changePwd(self,request):
        p = Jwt.authHeader(request)
        res = json.loads(p)
        if res['code'] == 20000:
            admin = dict()
            data = json.loads(request.get_data())
            admin['username']=res['data']['username']
            admin['oldPass']=data['oldpass']
            admin['password']=data['password']
            result=self.admin.update_pwd(admin)
            if result !=None:
                return response({}, code=20000, message='修改成功！')
            else:
                return response({}, code=50000, message='修改失败,请检查原密码！')
        else:
            return p