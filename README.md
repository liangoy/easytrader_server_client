### 作用

1、用于交易命令执行端在云服务器上的场景，加入了严格的权限控制，保证所有操作均来自本人的命令
2、确保云端的操作方式与本地部署的操作方式一致，减少学习成本

## 用法

1. 在云端安装券商交易客户端
2. 在云端执行python server.py，启动服务
3. 在本地使用client.py文件中的User类进行交易，client.py中的User类的实例用法与server.py中的user使用方式基本一致。

## 范例

在云端部署完成后，在本地通过以下代码即可进行交易：

'''python
from client import User

user=User(
    password='your password',#用于权限验证，不可告诉他人
    ip='127.0.0.1',#云端服务器的地址
    port=5000
)
print(user.balance())
print(user.today_trades())
print(user.buy('510300',100,100))
'''