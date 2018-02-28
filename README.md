# 脚本版认证

## 用途
用于南京信息工程大学校园网web认证：
> 1. 入网 
> 2. 查看本次登录时间
> 3. 退出登录
> 4. 倒计时   #1(未实现查看当前时间)
> 5. 记录用户 #2(仅能记录)

*#1代表仅有linux含有的功能，#2代表仅有windows含有的功能*

## 更新情况
2016-09-15 添加windows版<br>
2016-09-17 添加linux版<br>
2016-09-19 更新windows UI版

## 预计更新
<strike>添加linux版</strike><br>
<strike>添加倒计时功能(linux)</strike><br>
<strike>添加windows版界面</strike><br>
暂无

## 如何使用
系统中需装有python3任意版本（下列下载链接，均来源于python.org）<br>
[python3.5.1 32位](https://www.python.org/ftp/python/3.5.1/python-3.5.1.exe) <br>
[python3.5.1 64位](https://www.python.org/ftp/python/3.5.1/python-3.5.1-amd64.exe)<br>

```
windows:
    双击window.pyw即可，弹出UI
```

```
linux:
    仅提供命令行
    相对于windows使用ini配置文件格式，这里使用json格式作为配置文件，每项意义均和windows版相同
    webAuthenticate.json文件按照webAuthenticate内所写(path变量)，应放置于/etc/webAuthenticate文件夹下，webAuthenticate程序随意放置
    webAuthenticate程序内检测连接wifi的部分，使用NetworkManager内置nmcli模块
    具体使用详见参数说明(webAuthenticate -h/--help)
```
## 许可证
MIT

## 作者邮箱
**kasukuikawai@gmail.com**<br>
1607768311@qq.com
