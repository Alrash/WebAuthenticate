#脚本版认证

##用途
用于南京信息工程大学校园网web认证：
> 1. 入网 
> 2. 查看本次登录时间
> 3. 退出登录

##更新情况
2016-09-15 添加windows版<br>
2016-09-17 添加linux版

##预计更新
<strike>添加linux版</strike><br>
<strike>添加倒计时功能(linux)</strike><br>
添加windows版界面

##如何使用
系统中需装有python3任意版本（下列下载链接，均来源于python.org）<br>
[python3.5.1 32位](https://www.python.org/ftp/python/3.5.1/python-3.5.1.exe) <br>
[python3.5.1 64位](https://www.python.org/ftp/python/3.5.1/python-3.5.1-amd64.exe)<br>

修改net.ini文件
```
net.ini文件中由如下形式组成（等于号右边表达可以填写的东西）
[example]
username = xxxxxxxxxxx
sp = 0/1/2
encrypt = 0/1
passwd = xxxxxx

username 用户名
sp 运营商(0代表中国移动 1代表中国电信 2代表中国联通)
encrypt passwd键是否使用的是密文, 0否，1是
passwd 对应密码，若encrypt为0，填写正常密码，若为1,填写base64散列后的密文
```

```
windows:
    双击xx.py即可，会显示提示信息
```

```
linux:
    仅提供命令行
    相对于windows使用ini配置文件格式，这里使用json格式作为配置文件，每项意义均和windows版相同
    webAuthenticate.json文件按照webAuthenticate内所写(path变量)，应放置于/etc/webAuthenticate文件夹下，webAuthenticate程序随意放置
    webAuthenticate程序内检测连接wifi的部分，使用NetworkManager内置nmcli模块
    具体使用详见参数说明(webAuthenticate -h/--help)
```
##许可证
MIT

##作者邮箱
kasukuikawai@gmail.com<br>
1607768311@qq.com
