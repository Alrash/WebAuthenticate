# 脚本版认证

## 用途
> 1. 用于南京信息工程大学校园网web认证：
> 2. 可用于windows与linux平台
> 3. 可通过部分设置，达到开机启动的效果

## 依赖
> 1. python3
> 2. [pywifi模块 2017-11-05版本](https://github.com/awkman/pywifi) *有线可不用* 

## 部分bug
> 1. <strike>windows无法强制切换wifi</strike>
> 2. <strike>每次自动连接时，都会先断开wifi</strike>

## 如何使用
> 1. 使用-h参数查看参数使用
> 2. 常用参数
>  * -I 表示连接
>  * -c filename 表示使用filename配置文件，**不加此参数，默认为当前目录下的webAuthenticate.json**
>  * -s alias 表示使用配置文件中的哪一组配置
>  * -O 表示退出登陆
>  * -a 使用表示自动连接校园网络 **无线可选，有线无需选择**
>  * -w wait_time 表示自动连接网络之后等待的时间，防止wifi扫描不完整，默认0
>  * -W 0|1 表示使用什么方式自动连接网络，0表示WPA，1表示NetworkManager*默认*；**-a 参数未使用时，此参数无用**

## 配置文件
配置文件使用json格式编写 
```json
[
    {
        "alias":"-s 参数指定的名称",
        "username": "登陆时的用户名",
        "provider": "供应商，具体请看自带的配置文件",
        "encrypt": "true or false",
        "password": "密码；与encrypt对应，true时，请填写base64编码之后的文本；false时，直接使用明文"
    }
]
```

## 已连接i_NUIST，登陆样例
```python
python webAuthenticate -I -s alrash -c "D:\code\WebAuthenticate\webAuthenticate.json"
```

## 自动连接i_NUIST，登陆样例
### 使用WPA连接i_NUIST
```python
python webAuthenticate -I -s alrash -c "D:\code\WebAuthenticate\webAuthenticate.json" -a -W 0 -w 1
```

### 使用NetworkManager连接i_NUIST（注意，未完成）
```python
python webAuthenticate -I -s alrash -c "D:\code\WebAuthenticate\webAuthenticate.json" -a -w 1
```

## windows登陆设置
**右击“此电脑”/“我的计算机”等，选择“管理”**  
![01](./pic/01.png)
![02](./pic/02.png)
![03](./pic/03.png)
![04](./pic/04.png)
![05](./pic/05.png)
![06](./pic/06.png)
![07](./pic/07.png)
![08](./pic/08.png)

## 许可证
MIT

## 作者邮箱
**kasukuikawai@gmail.com**<br>
1607768311@qq.com
