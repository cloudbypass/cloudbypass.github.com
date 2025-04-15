# 穿云API转代理工具客户端

?> 推荐在Java项目、采集器等服务中使用。
> 通过穿云API代理服务客户端调用穿云API服务，适用于复杂的会话请求，例如登录、会话重定向请求等。用户只需要将原有的请求加上代理参数即可，穿云API代理服务客户端会自动将代理请求转发到穿云API服务。

### 获取工具

访问[穿云API代理服务客户端发布页面](https://github.com/cloudbypass/example/releases)下载对应平台的可执行程序和根证书

### 启动参数

| 参数 | 说明                                        |
|----|-------------------------------------------|
| -k | (可选) 穿云API服务密钥，配置默认请求标头`x-cb-apikey`      |
| -l | (可选) 服务监听地址 (default "0.0.0.0:1087")      |
| -s | (可选) 服务地址 (default "api.cloudbypass.com") |
| -x | (可选) 配置穿云API请求代理，该值将被传入`x-cb-proxy`请求头    |

### 启动命令

> 使用以下命令启动可预设apikey，在之后调用请求中无需再设置`x-cb-apikey`请求头

```shell
# 使用预设apikey
> cfb-mitm -k 0000000000000000 -x http:example.io:1288 -l 127.0.0.1:1087

# OUTPUT
# api.cloudbypass.com -> 127.0.0.1:1087
# Please use proxy 127.0.0.1:1087
```

?> 如果没有设置-k或-x时，可以通过请求头`x-cb-apikey`和`x-cb-proxy`动态配置。

启动后的界面👇

![proxy_tools.png](img%2Fproxy_tools.png)

### 通过cURL调用

```shell
# linux
curl --request GET \
--url "https://opensea.io/category/memberships" \
--proxy "http://127.0.0.1:1087" \
-k

# windows
curl --request GET ^
--url "https://opensea.io/category/memberships" ^
--proxy "http://127.0.0.1:1087" ^
-k
```

?> 穿云API代理服务客户端可以解决用户程序中Cookie等信息的管理问题。http代理在本地运行，无需担心安全问题。

# 关于软件

该软件由[穿云API](https://cloudbypass.com/)提供，严禁使用此软件从事欺诈、盗用他人账户、资金、服务攻击等违法犯罪活动。