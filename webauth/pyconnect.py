#! /usr/bin/python
# -*- coding: utf-8 -*-

# @Author: Alrash
# @Email: kasukuikawai@gmail.com
# @required: pywifi

import pywifi
import pywifi.const

import sys
import os
import time

from .const import *
from .ssid import *

# import logging
# pywifi.set_loglevel(logging.INFO)

# linux平台请使用root权限
if sys.platform == 'linux':
    if os.geteuid() != 0:
        sys.stderr.write("permission!\n")
        sys.exit(-1)

# 检查ssid是否是i-NUIST
# 返回-1（无线未连接，但是网卡配置正确） 0（没有） 1（一切正确）
def check_wifi_ssid(ssid):
    wifi = pywifi.PyWiFi()

    # 检查是否有无线网卡
    assert len(wifi.interfaces()) != 0

    iface = wifi.interfaces()[0]

    connected = check_connected_ssid(ssid)
    assert connected != None

    if connected == False:
        return DISCONNECTED
    else:
        if iface.status() in [pywifi.const.IFACE_CONNECTED, pywifi.const.IFACE_CONNECTING]:
            return CONNECTED
        else:
            return HASCONFIG

# 扫描，发现时候存在ssid
# return False, True
def scan_results(ssid):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(1)
    bessis = iface.scan_results()

    for net in bessis:
        if net.ssid == ssid:
            return True

    return False

# 创建配置
def _create_network_profile(ssid):
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = pywifi.const.AUTH_ALG_OPEN
    profile.akm.append(pywifi.const.AKM_TYPE_NONE)

    return profile

# 获取配置
def _get_network_profile(ssid):
    network_profile = pywifi.PyWiFi().interfaces()[0].network_profiles()

    profile = None
    for net in network_profile:
        if ssid == net.ssid:
            profile = net
            break

    return profile

# 检查wifi是否active
def active_connect(ssid, check_wifi_ssid):
    if check_wifi_ssid == CONNECTED:
        return True

    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    # 获取配置
    profile = _get_network_profile(ssid)
    if profile is None:
        profile = _create_network_profile(ssid)
        profile = iface.add_network_profile(profile)

    # 连接
    iface.connect(profile)
    time.sleep(1)
    return iface.status() in [pywifi.const.IFACE_CONNECTED, pywifi.const.IFACE_CONNECTING]
