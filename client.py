import json
import hashlib
import requests
import time

def md5(t):
    t=t.encode() if type(t)==str else t
    return hashlib.md5(t).hexdigest()

class User():
    def __init__(self,password='your password',ip='127.0.0.1',port=5000):
        self.password=password
        self.ip=ip
        self.port=port
    def __getattr__(self,method):
        return self.make_fn(method)
    def make_fn(self,fn_name):
        def fn(*args,**kwargs):
            time_stamp=str(time.time())
            stamp=md5(self.password+str(time_stamp))
            headers={
                'time-stamp':time_stamp,
                'stamp':stamp,
                'Content-Type':'application/json'
            }
            data={
                'args':args,
                'kwargs':kwargs
            }
            r=requests.post(f'http://{self.ip}:{self.port}/{fn_name}',data=json.dumps(data),headers=headers)
            return r.json()
        return fn
