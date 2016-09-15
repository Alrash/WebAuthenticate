#!/usr/bin/env python3
# coding=utf-8

# author: "alrash"
# email: "kasukuikawai@gmail.com"
# version: for windows alpha version

try:
    import urllib
    import configparser
    import urllib.request
    import base64
    import json
except:
    print("缺少下列库中的某些，请先安装: urllib configparser base64 json")
    print("退出脚本...")
    exit(-1)

sp_list = ['CMCC', 'ChinaNet', 'Unicom']
url = 'http://a.nuist.edu.cn/index.php'
urlInit = url + '/index/init'               #查看连接状态和连接时长
urlLogin = url + '/index/login'             #登录使用
urlLogout = url + '/index/logout'           #登出使用

username = ""
password = ""
sp = ""                                     #运营商（移动、联通...）
enablemacauth = 0                           #参数未知意义

def get_ini(fileName, pos):
    #读取配置文件，并获取第pos + 1项的配置内容
    config = configparser.ConfigParser()
    config.read(fileName)
    section = config.sections()[pos]

    #为全局变量赋值
    global sp, username, password
    sp = sp_list[config.getint(section, "sp")]
    username = config.get(section, "username")
    password = encode_password(config.get(section, "passwd"), config.getint(section, "encrypt"))

    return

def encode_password(password, encrypt = 0):
    return password if encrypt != 0 else base64.b64encode(password.encode(encoding='utf-8')).decode()

def get_status_with_json(url, data = None, isPost = False):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request, data if data is None else data.encode(encoding = 'utf-8'))
    return json.loads(response.read().decode())

def show_time(seconds):
    seconds = seconds if seconds > 0 else 0
    return '{:02d}'.format(seconds // 3600) + ":" + '{:02d}'.format(seconds // 60 % 60) + ":" + '{:02d}'.format(seconds % 60)

def show_status(status):
    print("*****************************************************")
    try:
        print(status['info'])
        print("当前运营商: " + status['logout_domain'])
        print("当前ip地址: " + status['logout_ip'])
        print("本次在线时长: " + show_time(status['logout_timer']))
    except KeyError:
        print("认证页面已更换api，可以联系作者更新程序了-_-|||")
    print("*****************************************************")
    return

def connect():
    #获取当前状态，若已登录，显示状态后退出
    status = get_status_with_json(urlInit)
    if status['status'] != 0:
        show_status(status)
        return

    #获取配置信息
    get_ini('net.ini', 0)
    data = {'username': username, 'domain': sp, 'password' : password, 'enablemacauth': enablemacauth}
    status = get_status_with_json(urlLogin, urllib.parse.urlencode(data))
    if status['status'] != 0:
        status = get_status_with_json(urlInit)
        show_status(status)
    else:
        print("*****************************************************")
        print("请检查用户、密码，以及运营商是否正确")
        print("\t注意，运营商的大小写是否规范")
        print("\t若完全正确，表示认证页面已更换api，该脚本失效")
        print("当前用户名: " + username)
        print("当前密码: " + base64.b64decode(password).decode())
        print("当前运营商: " + sp)
        print("*****************************************************")

    return

if __name__ == '__main__':
    connect()
