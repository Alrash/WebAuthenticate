# -*- coding: utf-8 -*-

import subprocess
import sys

if sys.platform == 'win32':
    _cmd = ['netsh', 'wlan', 'show', 'interfaces']
    _decode_coding = 'gb2312'
else:
    _cmd = ['wpa_cli', 'status']
    _decode_coding = 'utf-8'

# return None, False or True
def check_connected_ssid(ssid):     
    flag = False

    # _cmd = ['netsh', 'wlan', 'show', 'list']
    p = subprocess.Popen(_cmd, stdout = subprocess.PIPE)
    p.wait()
    
    if p.returncode != 0:
        print(p.stdout.decode(_decode_coding))
        return None
    else:
        for info in p.stdout.readlines():
            if info.decode(_decode_coding).find(ssid) != -1:
                flag = True
                break

    return flag                

if __name__ == '__main__':
    print(check_connected_ssid('i-NUIST'))