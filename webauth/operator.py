#! /usr/bin/python
# -*- coding=utf-8 -*-

# @Author: Alrash
# @Email: kasukuikawai@gmail.com

import sys
import json
import re

import base64

import urllib
import urllib.request
import socket

# 返回url所指状态
def _get_status_with_json(url, data = None, ssid = None):
    request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request, data if data is None else data.encode(encoding = 'utf-8'), timeout = 3)
    except urllib.error.URLError:
        sys.stderr.write("maybe, your connect wifi is not {}!\n".format(ssid))
        sys.exit(-1)
    except socket.timeout:
        sys.stderr.write("response time out!\n")
        sys.exit(-1)

    return json.loads(response.read().decode())

# 格式化输出时间
def _time_format(seconds):
    seconds = seconds if seconds > 0 else 0
    return '{:02d}'.format(seconds // 3600) + ":" + '{:02d}'.format(seconds // 60 % 60) + ":" + '{:02d}'.format(seconds % 60)

# 输出返回的状态信息
def _show_status_info(status):
    print("*****************************************************")
    for key in sorted(status.keys()):
        if key != 'status' and key != 'data':
            print('%-16s| %s'%(key, _time_format(status[key]) if re.compile(r'.*timer').match(key) else status[key]))
    print("*****************************************************")

# 返回当前状态信息
def show_info(config):
    status = _get_status_with_json(config['urlInit'], ssid = config['ssid'])
    _show_status_info(status)

# 登陆操作
def login(config):
    status = _get_status_with_json(config['urlInit'], ssid = config['ssid'])
    if status['status'] != 0:
        _show_status_info(status)
        return

    # 传输的json数据
    data = {'username': config['username'], 'domain': config['provider'], 'password': config['passwd'], 'enablemacauth': config['enablemacauth']}
    status = _get_status_with_json(config['urlLogin'], data = urllib.parse.urlencode(data), ssid = config['ssid'])
    if status['status'] != 0:
        print('login success')
    else:
        print("*****************************************************")
        print("login fail, please check your username, password and service provider")
        print("\tNote that uppercase and lowercase letters")
        print("\tanother case: web page change its api")
        print("username: " + config['username'])
        print("password: " + base64.b64decode(config['passwd']).decode())
        print("provider: " + config['provider'])
        print("*****************************************************")

# 登出操作
def logout(config):
    status = _get_status_with_json(config['urlInit'], ssid = config['ssid'])
    if status['status'] != 0:
        status = _get_status_with_json(config['urlLogout'], ssid = config['ssid'])

        if status['status'] != 0:
            print('logout success')
        else:
            print('unknown error, perhaps this script becomes useless!')
    else:
        print('not connected i-NUIST wifi or have logouted')