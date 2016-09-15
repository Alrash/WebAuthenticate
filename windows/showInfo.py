#!/usr/bin/env python3
# coding=utf-8

# author: "alrash"
# email: "kasukuikawai@gmail.com"
# version: for windows alpha version


try:
    import urllib
    #from urllib.request import urlopen
    import urllib.request
    import json
except:
    print("缺少下列库中的某些，请先安装: urllib json")
    print("退出脚本...")
    exit(-1)

url = "http://a.nuist.edu.cn/index.php/index/init"

def get_status_with_json(url, data = None, isPost = False):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request, data if data is None else data.encode(encoding = 'utf-8'))
    return json.loads(response.read().decode())

def show_time(seconds):
    seconds = seconds if seconds > 0 else 0
    return '{:02d}'.format(seconds // 3600) + ":" + '{:02d}'.format(seconds // 60 % 60) + ":" + '{:02d}'.format(seconds % 60)

def show_status_login(status):
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

def show_status_logout(status):
    print("*****************************************************")
    try:
        print(status['info'])
    except KeyError:
        print("认证页面已更换api，可以联系作者更新程序了-_-|||")
    print("*****************************************************")
    return

def show_status():
    status = get_status_with_json(url)
    if status['status'] != 0:
        show_status_login(status)
    else:
        show_status_logout(status)
    return

if __name__ == '__main__':
    show_status()
