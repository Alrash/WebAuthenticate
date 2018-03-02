#!/usr/bin/env python
# coding=utf-8

# Author: Alrash
# Email:  kasukuikawai@gmail.com

import pywifi
from pywifi import const

import sys
import json

try:
    import argparse
except ImportError:
    sys.stderr.write("The required Argparse modules could not be loaded.\n")
    sys.exit(1)

#check python version
if sys.version_info.major == 2:
    sys.stderr.write("Please run this script above the Python 2 executable.\n ")
    sys.exit(1)

#Handle command-line arguments with Argparse module
parse = argparse.ArgumentParser(description = '命令行控制认证网络')
parse.add_argument('-I', '--login', action = 'store_true', dest = 'login', help='接入Internet')
parse.add_argument('-s', '--section', action = 'store', dest = 'section', help='设置使用组组名')
parse.add_argument('-t', '--time', action = 'store', dest = 'time', type = int, help='设置倒计时时间，单位s')
parse.add_argument('-S', '--status', action = 'store_true', dest = 'status', help='显示当前信息')
parse.add_argument('-O', '--logout', action = 'store_true', dest = 'logout', help='断开Internet')
parse.add_argument('-v', '--version', action = 'version', version='%(prog)s 1.0')

# ------------------------- main -----------------------------------

# some config parameters
config_file = './webAuthenticate.json'
service_provider = ['NUIST', 'CMCC', 'ChinaNet', 'Unicom'];

# url
url = 'http://a.nuist.edu.cn/index.php'
urlInit = url + '/index/init'
urlLogin = url + '/index/login'
urlLogout = url + '/index/logout'

username = ''
passwd = ''
provider = ''
enablemacauth = 0
wifi = False

# load config from file
# return item or None
def load_config(filename, alias):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except OSError as e:
        if e.errno == errno.ENOENT:
            sys.stderr.write('cannot find the file {0}.\n'.format(jsonFile));
            sys.exit(-1)
        else:
            sys.stderr.write('permission denied {0}.\n'.format(jsonFile));
            sys.exit(-1)

    for item in data:
        if item['alias'] == alias:
            return item

    return None

# return base64 code
def encode_password(password, encrypt = False):
    return password if encrypt == True else base64.b64encode(password.encode(encoding = 'utf-8')).decode()


