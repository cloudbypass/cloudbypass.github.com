# 请求参数配置

### 请求URL配置

穿云API使用HTTPS协议，支持所有HTTP请求方法。您需要将目标地址协议和主机名替换为穿云API地址进行访问，以下是穿云API的请求地址：

`https://api.cloudbypass.com`

?> 如果要请求`https://example.io/user/login.html`，则需要修改为`https://api.cloudbypass.com/user/login.html`

### 请求头配置

除了URL之外还需要以下请求头参数：

* `x-cb-apikey` *[APIKEY](/zh-cn/quickstart?id=获取apikey)。
* `x-cb-host` *
  目标服务器主机名或IP地址。如访问`https://www.example.com/to/path`，则此参数为`www.example.com`，请求地址为`https://api.cloudbypass.com/to/path`。
* `x-cb-proxy` *设置代理服务器。V1有默认动态代理IP，并支持此参数设置代理服务器地址; 穿云V2必须设置固定或具有时效性的IP代理。

?> 与穿云API关联所有标头都以`x-cb-*`开头，穿云API在转发请求时不会携带相关请求头。

以下是用于自定义请求的请求头完整列表：

| 参数                                                            |    类型     |                       默认值                        |  支持版本  |            必填             | 描述                                                                                                                              |
|---------------------------------------------------------------|:---------:|:------------------------------------------------:|:------:|:-------------------------:|---------------------------------------------------------------------------------------------------------------------------------|
| [x-cb-apikey](/zh-cn/parameters?id=APIKEY)                    | `string`  | [去控制台获取](https://console.cloudbypass.com/#/api/) | `所有版本` | ![yes.svg](img%2Fyes.svg ":no-zoom") | 访问穿云API时使用的密钥                                                                                                                   |
| [x-cb-host](/zh-cn/parameters?id=x-cb-host、x-cb-protocol)     | `string`  |                                                  | `所有版本` | ![yes.svg](img%2Fyes.svg ":no-zoom") | 请求的目标域名，如：opensea.io，不要填协议和路径                                                                                                   |
| [x-cb-protocol](/zh-cn/parameters?id=x-cb-host、x-cb-protocol) | `string`  |                     "https"                      | `所有版本` |                           | 请求协议，如：http、https                                                                                                               |
| [x-cb-fp](/zh-cn/parameters?id=X-Cb-Fp)                       | `string`  |                     "chrome"                     |  `v1`  |                           | 客户端指纹，默认是Chrome浏览器的指纹。除此之外还支持Firefox、Edge。                                                                                      |
| [x-cb-proxy](/zh-cn/parameters?id=X-Cb-Proxy)                 | `string`  |                                                  | `所有版本` |                           | 自定义代理地址，可以是IP或域名。<br />支持http、socks5协议，如：http://proxy.com:8080 或 http://username:password:proxy.com:8080。<br />协议头可选，不填默认为http。 |
| x-cb-version                                                  | `string`  |                                                  | `所有版本` |                           | 当您需要使用穿云v2时，该请求头值应为`2`。                                                                                                         |
| [x-cb-part](/zh-cn/parameters?id=X-Cb-Part)                   | `integer` |                        0                         |  `v2`  |                           | 该请求头仅在穿云v2时有效，用于区分不同的会话，用户最多可以拥有1000个会话分区（0~999）。                                                                               |
| [x-cb-origin](/zh-cn/parameters?id=关于浏览器跨域的问题)                | `string`  |                                                  | `所有版本` |                           | 替换请求头中的origin字段，一般用于浏览器跨域请求绕过CORS限制。                                                                                            |
| [x-cb-referer](/zh-cn/parameters?id=关于浏览器跨域的问题)               | `string`  |                                                  | `所有版本` |                           | 替换请求头中的referer字段，一般用于浏览器跨域请求绕过CORS限制。                                                                                           |
| x-cb-cookie                                                   | `string`  |                                                  | `所有版本` |                           | 替换请求头中的cookie字段，一般用于浏览器跨域请求绕过CORS限制。                                                                                            |
| [x-cb-sitekey](/zh-cn/parameters?id=如何获取sitekey)              | `string`  |                                                  |  `v2`  |                           | 填写后将触发Turnstile小部件验证。在请求数据中将cf_token值设置为[cf_token]，验证结果将自动替填充后请求。                                                               |
| [x-cb-options](/zh-cn/parameters?id=配置选项列表)                   | `string`  |                                                  | `所有版本` |                           | 配置选项列表，可以填写多个附加配置选项，逗号分隔。详细请查看[配置选项列表](/zh-cn/parameters?id=配置选项列表)。                                                            |

### 配置选项列表

`x-cb-options`请求头配置列表：

| 参数               |  支持版本  | 描述                                                                                                   |
|------------------|:------:|------------------------------------------------------------------------------------------------------|
| disable-redirect | `所有版本` | 禁用重定向，服务端遇到300~399响应码时将会返回，Set-Cookie将会返回完整内容。（默认自动处理重定向，SDK默认配置）。                                   |
| force            |  `v2`  | 正常情况下，在穿云V2会话期内无法更换代理，会返回`BYPASS_ERROR`错误。使用`force`配置可以强制替换代理。                                       |
| ignore-lock      |  `v2`  | 使用忽略锁策略，当两个或多个请求同时使用同一个会话时，直接忽略验证挑战锁，可以防止出现**CHALLENGE_LOCK_TIMEOUT**或**CHALLENGE_LOCK_OCCUPIED**错误。 |
| wait-lock        |  `v2`  | 使用等待锁策略，当两个或多个请求同时使用同一个会话时，可以防止出现CHALLENGE_LOCK_TIMEOUT错误。（比ignore-lock优先级更高）                        |

### APIKEY

`APIKEY`为每个账户唯一的穿云API请求授权访问密钥，是访问穿云API的必要参数之一。

?> 若`APIKEY`出现泄露问题，可通过访问[穿云API控制台](https://console.cloudbypass.com/#/api/)刷新。

访问`https://opensea.io/category/memberships`，请求示例：

```shell
# linux
curl --request GET \
--url "https://api.cloudbypass.com/category/memberships" \
--header "x-cb-apikey: <APIKEY>" \
--header "x-cb-host: opensea.io"

# windows
curl --request GET ^
--url "https://api.cloudbypass.com/category/memberships" ^
--header "x-cb-apikey: <APIKEY>" ^
--header "x-cb-host: opensea.io"
```

### X-Cb-Host、X-Cb-Protocol

`X-Cb-Host`和`X-Cb-Protocol`也是访问穿云API的必要参数之一。
`X-Cb-Protocol`默认为https，所以一般不用设置。

?> 将原始请求URL中的协议、主机域名(也可以是IP)、端口号替换为穿云API地址(`https://api.cloudbypass.com`)，`X-Cb-Host`
则填写被替换掉的主机域名。
如下HTTP示例：

```http request
# 原始请求
GET https://example.io/user/login.html

# 修改后的请求
GET https://api.cloudbypass.com/user/login.html
X-Cb-Apikey: <APIKEY>
X-Cb-Host: example.io
```

如果原始请求是http协议：

```http request
# 原始请求
GET http://example.io/user/login.html

# 修改后的请求
GET https://api.cloudbypass.com/user/login.html
X-Cb-Apikey: <APIKEY>
X-Cb-Host: example.io
X-Cb-Protocol: http
```

> 您可以了解一下：HTTP基础请求由请求行、请求头、请求体组成，其中请求行包含了请求方法、请求URL、HTTP协议版本。
> 由于穿云API使用HTTP代理转发的模式，在使用穿云API请求时，需要在原始请求上对**请求URL**、**请求头**进行一些调整。
> 经过调整后的请求将由穿云API代理访问目标地址。

### X-Cb-Proxy

客户端自定义代理，支持HTTP、Socks5协议

支持格式如下

* 用户名:密码@主机名:端口 (默认http协议)
* 用户名:密码:主机名:端口 (默认http协议)
* 协议://用户名:密码@主机名:端口
* 协议://用户名:密码:主机名:端口
* 协议:用户名:密码:主机名:端口

### X-Cb-Fp

设置API代理请求时使用的浏览器指纹。以下是支持列表

* 穿云V1
    * `chrome`
    * `firefox`
    * `edge`
* 穿云V2
    * `chrome`、`chrome-linux`、`chrome-mac`、`chrome127`、`chrome127-linux`、`chrome127-mac`
    * `edge`、`edge-linux`、`edge-mac`、`edge127`、`edge127-linux`、`edge127-mac`
    * `chrome-android`、`edge-android`、`chrome127-android`、`edge127-android`

### X-Cb-Part

穿云V2采用会话托管模式，所有cloudflare响应的cookie都将被存储到穿云服务器，用户可以通过设置`X-Cb-Part`请求头切换会话。
当验证通过后`cloudflare cookie`将保留10分钟，10分钟内再次请求成功则续期。

?> 在会话期内无法更换代理，如有业务需求可配置`x-cb-options: force`强制更换。(一般不推荐)

### 使用穿云V2进行请求

穿云API V2适用于需要通过JS质询验证的网站。例如访问`https://etherscan.io/accounts/label/lido`，请求示例：

```shell
# linux
curl --request GET \
--url "https://api.cloudbypass.com/accounts/label/lido" \
--header "x-cb-apikey: <APIKEY>" \
--header "x-cb-host: etherscan.io" \
--header "x-cb-version: 2" \
--header "x-cb-part: 0" \
--header "x-cb-proxy: http:proxy:1087"

# windows
curl --request GET ^
--url "https://api.cloudbypass.com/accounts/label/lido" ^
--header "x-cb-apikey: <APIKEY>" ^
--header "x-cb-host: etherscan.io" ^
--header "x-cb-version: 2" ^
--header "x-cb-part: 0" ^
--header "x-cb-proxy: http:proxy:1087"
```

### 关于V2并发请求的问题

遇到验证时会根据`host`、`part`进行上锁，验证完成后释放。所以默认情况下`host`、`part`锁定状态下是无法进行请求的。

?> 推荐多线程请求的情况下，每个线程使用单独的`part`发起请求，可以避免以下模式中出现的各种问题。这样合理使用`part`
可以避免出现更多验证以及减少积分、流量、时间的消耗。(多线程推荐)

* `default` 默认情况下遇到验证锁时会返回`CHALLENGE_LOCK_OCCUPIED`错误。这表示有一条同`host`、`part`的请求正在验证中。
* `ignore-lock` 忽略验证锁，通过请求头`x-cb-options: ignore-lock`设置。
    * 优点：可以避免所有锁错误
    * 缺点：消耗更多的积分、流量、时间
* `wait-lock` 等待验证锁，通过请求头`x-cb-options: wait-lock`设置。
    * 优点：可以避免`CHALLENGE_LOCK_OCCUPIED`错误，等待验证通过后将会直接使用新的Cookie完成请求
    * 缺点：如果等待时间过长，可能出现`CHALLENGE_LOCK_TIMEOUT`错误

### 关于浏览器跨域的问题

> 您可以了解一下：浏览器跨域是指由于浏览器的同源策略限制，不同源的文档或脚本不能相互交互的问题。
> 同源策略是一种安全机制，它要求协议、域名和端口都相同才能认为是同源。这是为了防止恶意网站读取或操作其他网站的数据。
> 跨域资源共享（CORS）是一种解决跨域问题的技术，它允许浏览器向不同源的服务器发送HTTP请求。

一般浏览器在请求接口时会自动补充`origin`、`referer`这些站点无法控制的请求头。
这些请求头到穿云API后也会被转发至目标服务器，导致请求失败。
所以通过配置`x-cb-origin`、`x-cb-referer`可以对部分跨域相关请求头进行覆盖。

### 如何获取sitekey

这里`sitekey`是指调用`turnstile`部件的主要参数，每个站点都有单独的`turnstile sitekey`。

?> 注意：`cloudflare js`质询不需要填写sitekey

1. 打开浏览器`开发者工具`（Ctrl+Shift+I或F12）
2. 点击`网络`选项卡，确保`记录网络日志`按钮的状态如图所示<br />
   ![devtools_network.png](img%2Fdevtools_network.png)
3. 访问具有`turnstile`部件的页面
4. 在筛选器上输入`https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/b/turnstile/`
5. 如图选中的内容就是`sitekey` <br />
   ![devtools_network1.png](img%2Fdevtools_network1.png)