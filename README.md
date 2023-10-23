> 官方文档: https://developer.work.weixin.qq.com/document
> 
> 项目参考: https://github.com/sbzhu/weworkapi_python/tree/master
> 
> 项目结构请自行调整, 代码都是网上 copy 的, 能通过企业微信的回调认证, 其他后续的功能扩展请自行添加


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
+ 填写 URL(如果在本地需要使用外网穿透相关服务, 本文不再详细描述)
+ 保存 Token 以及 EncodingAESKey

## 项目启动

1. 把以上所需参数填入 `example.config.ini` 中
2. `pip install -r requirements.txt`
3. 运行 `main.py`
4. 可以实现简单的企业微信的回调认证以及消息的接收和返回, 其他具体的功能需要开发者自行开发以及植入
5. `ierror.py提供了错误`, 如果遇到问题请自行查看



> 创建 `API接收消息` 时报错 `50001` 时可能是网络延迟, 请等待 15 - 30 秒左右重新尝试



## 截图

![image-20231023150035965](https://qiniu.waite.wang/202310231500336.png)

![image-20231023150113305](https://qiniu.waite.wang/202310231501014.png)

    