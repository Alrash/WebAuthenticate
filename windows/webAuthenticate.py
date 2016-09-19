#!/usr/bin/env python3
# coding=utf-8

# author: "alrash"
# email: "kasukuikawai@gmail.com"
# version: for windows Beta version

#总体返回值约束
##登录成功1
##登录失败1000
##已登录10
##未登录0
##退出成功100
##退出失败-1

import urllib
import urllib.request
import base64
import json

sp_list = ['CMCC', 'ChinaNet', 'Unicom']
url = 'http://a.nuist.edu.cn/index.php'
urlInit = url + '/index/init'               #查看连接状态和连接时长
urlLogin = url + '/index/login'             #登录使用
urlLogout = url + '/index/logout'           #登出使用

#读取配置文件
def get_json_info(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except OSError:
            return None

def set_json_info(filename, username, password, sp, encrypt):
    with open(filename, "w") as f:
        json.dump({"username":username, "provider": sp, "encrypt": encrypt, "password": password}, f)

def encode_password(password, encrypt = False):
    return password if encrypt else base64.b64encode(password.encode(encoding='utf-8')).decode()

def decode_password(password, encrypt = False):
    return base64.b64decode(password).decode() if encrypt else password

def get_status_with_json(url, data = None, isPost = False):
    request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request, data if data is None else data.encode(encoding = 'utf-8'), timeout = 5)
    except:
        return {"status":0, "info": "wifi未连接 或 网络不通畅"}
    return json.loads(response.read().decode())

def show_time(seconds):
    seconds = seconds if seconds > 0 else 0
    return '{:02d}'.format(seconds // 3600) + ":" + '{:02d}'.format(seconds // 60 % 60) + ":" + '{:02d}'.format(seconds % 60)

#登录
#成功status置1
#失败，返回None
def connect(username, sp, password, enablemacauth = 0):
    #获取当前状态，若已登录，直接返回
    status = show_status()
    if status['status'] != 0:
        return status

    data = {'username': username, 'domain': sp, 'password' : password, 'enablemacauth': enablemacauth}
    status = get_status_with_json(urlLogin, urllib.parse.urlencode(data))
    if status['status'] == 0:
        status['status'] = 1000
    return status

#获得当前状态
#未登录status['status'] = 0
#已登录status['status'] = 10
def show_status():
    status = get_status_with_json(urlInit)
    if status['status'] != 0:
        status['status'] = 10
    return status

#退出登录
#成功退出,status置100
#失败，status置-1
def logout():
    status = show_status()
    if status['status'] == 0:
        return status
    status = get_status_with_json(urlLogout)
    if status['status'] != 0:
        #退出成功
        status['status'] = 100
    else:
        status['status'] = -1
    return status
