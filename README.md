> 官方文档: https://developer.work.weixin.qq.com/document
> 
> 项目参考: https://github.com/sbzhu/weworkapi_python/tree/master
> 
> 项目结构请自行调整, 代码都是网上 copy 的, 能通过企业微信的回调认证, 其他后续的功能扩展请自行添加
>
> 因为参考仓库没有注明开源协议, 非个人开发者请谨慎使用!!!

## 项目准备

> 1. 本项目建设您已经创建好企业微信账号并且完成相关的个人或者企业认证
> 2. 建议使用 `Python 3.0 +` 版本, 本项目使用 `3.10`, 如果遇到报错请尝试升级 `Python` 版本
> 3. 企业微信发送消息需要微信加入企业才可发送

### 项目所需参数以及相关介绍

> 项目所需参数如下
>
> 1. AgentId = 企业微信应用ID
> 2. Secret = 企业微信应用Secret
> 3. CorpID = 企业微信ID
> 4. Token = 企业微信应用Token
> 5. EncodingAESKey = 企业微信应用EncodingAESKey

#### AgentId

> 我的企业 -> 企业ID

![image-20231023144053040](https://qiniu.waite.wang/202310231440734.png)

#### Secret 以及CorpID

+ 应用管理 -> 创建应用
+ 按各自使用场景创建完毕应用, 进入应用管理页面

![image-20231023144252189](https://qiniu.waite.wang/202310231442994.png)

#### Token 以及 EncodingAESKey

+ 应用管理页面 -> 接收消息 -> Api 接收
+ 填写 URL(如果在本地需要使用内网穿透相关服务, 本文不再详细描述)
+ 保存 Token 以及 EncodingAESKey

## 项目启动

1. 把以上所需参数填入 `example.config.ini` 中
2. `pip install -r requirements.txt`
3. 运行 `main.py`
4. 可以实现简单的企业微信的回调认证以及消息的接收和返回, 其他具体的功能需要开发者自行开发以及植入
5. `ierror.py提供了错误`, 如果遇到问题请自行查看



> 创建 `API接收消息` 时报错 `50001` 时可能是网络延迟, 请等待 15 - 30 秒左右重新尝试


## 接收消息和事件

> 详细查看 https://developer.work.weixin.qq.com/document/path/90238
> 
> 获取临时素材接口 https://developer.work.weixin.qq.com/document/path/90254
> 
> 在 `receive.py` 有简单的参考,本项目不再详细描述, 具体参考官方文档自行开发
> 
> 在 `main.py` 中引用了 `receive` 中的方法, 图片/ 视频接收好像会发送两次链接请求, 具体原因不明, 请自行查看(因为我想做的东西没有这个需求, 而且有替代方案, so 不管啦)
 

## 消息主动推送

> 仅提供 `text` 类型推送, 其他类型请参考 https://developer.work.weixin.qq.com/document/path/90235

1. 需在 应用管理 -> 配置企业可信 IP 为服务器 IP
2. 运行 api.examples.MessageTest.py 更改其中 to_user 为企业中成员姓名
3. 运行后即可在微信中收到推送消息

> 以下为发送应用消息类型: https://developer.work.weixin.qq.com/document/path/90250#%E5%9B%BE%E7%89%87%E6%B6%88%E6%81%AF
### 临时素材上传

+ 在某些推送只支持 `media_id` 推送文件, 图片 或者 语音
+ 详细查看 https://developer.work.weixin.qq.com/document/path/91054
+ 所有文件size必须大于5个字节
  - 图片（image）：10MB，支持JPG,PNG格式
  - 语音（voice） ：2MB，播放长度不超过60s，**仅支持**AMR格式
  - 视频（video） ：10MB，支持MP4格式
  - 普通文件（file）：20MB
+ 如果需要上传更大的素材文件, 可以尝试异步上传临时素材接口 https://developer.work.weixin.qq.com/document/path/96219
  - 图片（image）：暂不支持
  + 语音（voice） ：暂不支持
  + 视频（video） ：**200MB**，仅支持MP4格式
  + 普通文件（file）：**200MB**

```python
# 以下为调用临时素材上传接口, 如需使用建议封装, 文档: https://developer.work.weixin.qq.com/document/path/90253
path = "exam.png"
img_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token{}&type=image".format(api.getAccessToken())
files = {'image': open(path, 'rb')}
r = requests.post(img_url, files=files)
re = json.loads(r.text)
# print(re)
media_id = re['media_id']
```

### 推送注意事项

+ 图片, 视频, 语音, 图文消息推送需要先行调用临时素材上传接口, 并获取接口返回值中的 `media_id` 数据
+ 以上推送文件只支持`media_id` 传参
  + 小程序推送需要申请权限, 否则会有 `48002`报错, 具体[点击查看](https://developer.work.weixin.qq.com/devtool/query?e=48002)
+ 具体案例在 `api/examples` 中, 不确保正确/ 规范与否, 具体以[官方文档](https://developer.work.weixin.qq.com/document/path/90235)为主


### Token 相关


>注意:
> token是需要缓存的，不能每次调用都去获取token，否则会中频率限制

在本库的设计里，token是以类里的一个变量缓存的
比如api/src/CorpApi.py 里的access_token变量
在类的生命周期里，这个accessToken都是存在的， 当且仅当发现token过期，CorpAPI类会自动刷新token
刷新机制在 api/src/AbstractApi.py
所以，使用时，只需要全局实例化一个CorpAPI类，不要析构它，就可一直用它调函数，不用关心 token

```python
api = CorpAPI(corpid, corpsecret)
api.dosomething()
api.dosomething()
api.dosomething()
....
```
当然，如果要更严格的做的话，建议自行修改，全局缓存token，比如存redis、存文件等，失效周期设置为2小时。

## 截图

![image-20231023150035965](https://qiniu.waite.wang/202310231500336.png)

![image-20231023150113305](https://qiniu.waite.wang/202310231501014.png)

