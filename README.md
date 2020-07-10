# flask-admin-service
 基于flask的运用于vue-element-admin后端，使用jwt作为token鉴权。
### 运行
``` bash
pip install
run app.py
```

### 目录

```javascript
├─app.py //项目入口文件
├─configs.py //全局变量的配置
├─requirements.txt //依赖
├─utils //工具类
|   ├─dumps.py //封装response
|   ├─jwt.py  //jwt解析和封装
|   └md5.py  // md5加密
├─models 
|   ├─activity.py
|   ├─admin.py
|   ├─category.py
|   ├─goods.py
|   ├─order.py
|   └user.py
├─controller 
|     ├─activityController.py
|     ├─adminController.py
|     ├─categoryController.py
|     ├─goodsController.py
|     ├─orderController.py
```

