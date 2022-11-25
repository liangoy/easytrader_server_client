from flask import Flask,request,jsonify
import flask
import easytrader
import time
import hashlib
from types import MethodType
from gevent import pywsgi

'''
config
'''
user=easytrader.use('htzq_client')#需要根据自身情况修改
user.connect('C:\htzq\海通证券金融终端独立下单2.0/xiadan.exe')#需要根据自身情况修改
password='your password'#填入你的通信密码，用于加密通信
port=5000#服务端口




app = Flask(__name__)

def md5(t):
    t=t.encode() if type(t)==str else t
    return hashlib.md5(t).hexdigest()

used_time_stamp=set()


def permission(fn):
    def func(*l,**k):
        global used_time_stamp
        
        time_stamp=float(request.headers.get('time-stamp','0'))
        stamp=request.headers.get('stamp','')
        now_time_stamp=time.time()
        
        cond1=abs(time_stamp-now_time_stamp)<2
        
        true_stamp=md5(password+str(time_stamp))
        cond2=true_stamp==stamp
        
        used_time_stamp={i for i in used_time_stamp if abs(now_time_stamp-i)<5}
        cond3=time_stamp not in used_time_stamp
        
        cond=cond1&cond2&cond3
        if cond:
            used_time_stamp.add(time_stamp)
            return fn(*l,**k)
        return {'error_msg':'U have no permission'},401
    func.__name__=fn.__name__
    return func

def handle_error(fn):
    def func(*l,**k):
        try:
            r=fn(*l,**k)
        except Exception as e:
            message = "{}: {}".format(e.__class__, e)
            r=jsonify({"error": message}), 400
        return r
    func.__name__=fn.__name__
    return func

@app.route("/<method>",methods=['get','post','put'])
@permission
@handle_error
def fn(method):
    data=request.get_json()
    args=data.get('args',list())
    kwargs=data.get('kwargs',dict())
    r=getattr(user,method)
    if isinstance(r,MethodType):
        r=r(*args,**kwargs)
    return jsonify(r)

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', port), app)
    server.serve_forever()
