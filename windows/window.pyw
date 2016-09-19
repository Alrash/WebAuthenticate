import tkinter
import webAuthenticate
import time
import _thread
import sys
import subprocess

##每次启动，强制连接i-NUIST无线
##但是没有windows进行测试，貌似有些小问题，故注释
##想要使用，去除下一行的'#'号即可
#subprocess.call("netsh wlan connect i-NUIST")

jsonFile = "webAuthenticate.json"

username = ""
password = ""
server_provider = None
timer = 0
encrypt = False
login = False
Is_show = False

def mainloop():
    global timer, server_provider, username, password, encrypt,login

    #一个坑爹的问题：网络不通，界面跳不出来-_-|||
    webStatus = webAuthenticate.show_status()
    if webStatus['status'] == 1 or webStatus['status'] == 10:
        timer = webStatus['logout_timer']
        server_provider = webStatus['logout_domain']
        login = True
    
    #基本上是未登录状态
    #json文件，默认只有一个配置内容
    #此时，密码未经base64编码
    info = webAuthenticate.get_json_info(jsonFile)
    if info:
        username = info['username']
        server_provider = info['provider']
        password = info['password']
        encrypt = info['encrypt']
    else:
        server_provider = "CMCC"

    window = tkinter.Tk()
    window.title("网页认证客户端")
    window.resizable(0, 0)                  #不可缩放

    sp = tkinter.StringVar()
    sp.set(server_provider)
    user = tkinter.StringVar()
    user.set(username)
    passwd = tkinter.StringVar()
    passwd.set(webAuthenticate.decode_password(password, encrypt))

    #分上下两个区域
    top = tkinter.Frame(window)
    top.pack(pady = 10)
    buttom = tkinter.Frame(window)
    buttom.pack(pady = 2)

    #top区域增加控件
    status = tkinter.Frame(top)
    status.pack(pady = 5)
    info = tkinter.Frame(top)
    info.pack(padx = 15)
    buttomBlank = tkinter.Frame(top)
    buttomBlank.pack()

    status_info = tkinter.Label(status, text=webStatus['info'], font = "-size 16")
    status_info.pack()
    tkinter.Label(info, text="用户: ", font = "-size 12").pack(side = tkinter.LEFT)
    text_info = webStatus['logout_username'] if webStatus['status'] == 1 or webStatus['status'] == 10 else "0000000000"
    user_top = tkinter.Label(info, text = text_info, font = "-size 12")
    user_top.pack(side = tkinter.LEFT)
    text_info = webAuthenticate.show_time(timer)
    clock = tkinter.Label(info, text = text_info, font = "-size 12")
    clock.pack(side = tkinter.RIGHT)
    tkinter.Label(info, text= "    " + "登录时间: ", font = "-size 12").pack(side = tkinter.RIGHT)
        
    
    try:
        _thread.start_new_thread(flush_timer, (clock, status_info))
    except:
        sys.stderr.write("不能创建线程")
        sys.exit(-1)

    #buttom区域增加控件
    username_Area = tkinter.Frame(buttom)
    username_Area.pack(pady = 3)
    password_Area = tkinter.Frame(buttom)
    password_Area.pack(pady = 3)
    provider = tkinter.Frame(buttom)
    provider.pack(pady = 3)
    button = tkinter.Frame(buttom)
    button.pack(pady = 8)

    tkinter.Label(username_Area, text = "用户: ", font = "-size 10").pack(side = tkinter.LEFT)
    in_user = tkinter.Entry(username_Area, text = user)
    in_user.pack(side = tkinter.LEFT)
    tkinter.Label(password_Area, text = "密码: ", font = "-size 10").pack(side = tkinter.LEFT)
    in_passwd = tkinter.Entry(password_Area, show = "*", text = passwd)
    in_passwd.pack(side = tkinter.LEFT)
    tkinter.Radiobutton(provider, text = "中国移动", anchor=tkinter.W, value = "CMCC", variable = sp).pack(side = tkinter.LEFT)
    tkinter.Radiobutton(provider, text = "中国电信", anchor=tkinter.W, value = "ChinaNet", variable = sp).pack(side = tkinter.LEFT)
    tkinter.Radiobutton(provider, text = "中国联通", anchor=tkinter.W, value = "Unicom", variable = sp).pack(side = tkinter.LEFT)
    tkinter.Button(button, text = "网络登录", command = lambda:connect(in_user.get(), in_passwd.get(), sp.get(), status_info, user_top, clock)).pack(side = tkinter.LEFT, padx = 30)
    tkinter.Button(button, text = "断开连接", command = lambda:logout(status_info)).pack(side = tkinter.LEFT, padx = 30)

    try:
        _thread.start_new_thread(ajust_timer, (clock, status_info))
    except:
        pass

    window.mainloop()

def connect(username, password, provider, info_status, user, clock):
    global timer, login, Is_show
    if login:
        return

    status = webAuthenticate.connect(username, provider, webAuthenticate.encode_password(password))
    if status:
        info_status['text'] = status['info']
        if status['status'] == 1 or status['status'] == 10:
            timer = status['logout_timer']
            user['text'] = status['logout_username']
        
        info = webAuthenticate.get_json_info(jsonFile)
        if not info or info['username'] != username or info['password'] != password:
            webAuthenticate.set_json_info(jsonFile, username, webAuthenticate.encode_password(password), provider, True)
        
        #启动计时线程
        if status['status'] == 1:
            login = True
            Is_show = False
            try:
                _thread.start_new_thread(flush_timer, (clock, info_status,))
                _thread.start_new_thread(update_status_info, (info_status, "已登录",))
            except:
                return
    else:
        info_status['text'] = status['info'];

def logout(info_status):
    global login, Is_show

    status = webAuthenticate.logout()
    if status['status'] == -1:
        info_status['text'] = "退出失败"
    elif status['status'] == 0:
        return
    else:
        info_status['text'] = status['info']
        login = False
        Is_show = True
    return

def flush_timer(clock, info_status):
    global timer

    while login:
        time.sleep(1)
        timer += 1
        clock['text'] = webAuthenticate.show_time(timer)
    
    if Is_show:
        update_status_info(info_status, "未登录")
        timer = 0

    _thread.exit()

def ajust_timer(clock, info_status):
    global login, timer
    while True:
        time.sleep(600)
        status = webAuthenticate.show_status()

        #等待2秒，使flush_timer线程安全退出
        login = False
        if status['status'] == 10:
            time.sleep(2)
            timer = status['logout_timer'] + 2
            login = True
            try:
                _thread.start_new_thread(flush_timer, (clock, info_status,))
            except:
                pass
        else:
            info_status["text"] = "未登录"

    _thread.exit()

def update_status_info(info, text):
    time.sleep(5)
    info['text'] = text
    _thread.exit()

if __name__ == '__main__':
    mainloop()
