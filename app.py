from flask import Flask,request
from flask_cors import CORS
import configs
import pymongo
from controller.adminController import Controller as admin
from controller.goodsController import Controller as goods
from controller.categoryController import Controller as category
from controller.orderController import Controller as order
from controller.activityController import Controller as activity


from utils.dumps import response
from utils.uploadPic import uploadImg

app = Flask(__name__)
CORS(app, supports_credentials=True)
client = pymongo.MongoClient(configs.mongoUrl, configs.mongoPort)
db=client[configs.dbname]
admin=admin()
category=category()
goods=goods()
order=order()
activity=activity()
@app.route('/')
def hello_world():
    return 'Hello World!'

#ADMIN
@app.route('/api/admin/login',methods=["POST"])
def adminLogin():
    return admin.login(request)

@app.route('/api/admin/info',methods=["GET"])
def adminInfo():
    return admin.getInfo(request)

@app.route('/api/admin/logout',methods=["POST"])
def adminLogout():
    return admin.logout()

@app.route('/api/admin/list',methods=["POST"])
def adminList():
    return admin.getList(request)

@app.route('/api/admin/delete',methods=["POST"])
def adminDelete():
    return admin.delete(request)

@app.route('/api/admin/edit',methods=["POST"])
def adminEdit():
    return admin.edit(request)

@app.route('/api/admin/create',methods=["POST"])
def adminCreate():
    return admin.create(request)

@app.route('/api/admin/pwd',methods=["POST"])
def adminChangePwd():
    return admin.changePwd(request)

#图片上传
@app.route('/api/upload/picture',methods=["GET"])
def uploadPic():
    data=uploadImg()
    return response(data, code=20000, message='获取成功！')

#分类
@app.route('/api/category/create',methods=["POST"])
def categoryCreate():
    return category.create(request)

@app.route('/api/category/list',methods=["POST"])
def categoryList():
    return category.getList(request)
@app.route('/api/category/delete',methods=["POST"])
def categoryDelete():
    return category.delete(request)

@app.route('/api/category/edit',methods=["POST"])
def categoryEdit():
    return category.edit(request)

@app.route('/api/category/cascader',methods=["GET"])
def categoryCascader():
    return category.getCascader(request)
#商品
@app.route('/api/goods/create',methods=["post"])
def goodsCreate():
    return goods.create(request)
@app.route('/api/goods/list',methods=["post"])
def goodsList():
    return goods.getList(request)
@app.route('/api/goods/edit',methods=["post"])
def goodsEdit():
    return goods.edit(request)
@app.route('/api/goods/delete',methods=["POST"])
def goodsDelete():
    return goods.delete(request)
#订单
@app.route('/api/order/list',methods=["post"])
def orderList():
    return order.getList(request)
@app.route('/api/order/edit',methods=["post"])
def orderEdit():
    return order.edit(request)
@app.route('/api/order/delete',methods=["post"])
def orderDelete():
    return order.delete(request)
#活动
@app.route('/api/activity/list',methods=["get"])
def activityList():
    return activity.getList(request)
@app.route('/api/activity/create',methods=["post"])
def activityCreate():
    return activity.create(request)
@app.route('/api/activity/edit',methods=["post"])
def activityEdit():
    return activity.edit(request)
@app.route('/api/activity/delete',methods=["post"])
def activityDelete():
    return activity.delete(request)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port='5000',
        debug = True
    )

