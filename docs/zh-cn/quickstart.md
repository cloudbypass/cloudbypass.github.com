# 快速开始

>
使用穿云可以帮助您轻松绕过Cloudflare的验证，目前支持绕过JS质询、Turnstile等产品验证。本文档提供了穿云[HTTP API](/zh-cn/request_parameters)、[本地代理工具](/zh-cn/proxy_tools)
以及[SDK](/zh-cn/quickstart?id=代码示例)的详细使用方法。

# 工作流程

穿云API的请求流程

![cloudbypass_api_fc.svg](img/cloudbypass_api_fc.svg)

?> 无论使用[本地代理工具](/zh-cn/proxy_tools)或是[SDK](/zh-cn/quickstart?id=代码示例)都只是对请求进行转发，实际上还是HTTP
API请求。

# 获取APIKEY

访问[穿云API控制台](https://console.cloudbypass.com/#/api/)注册账户获取APIKEY。

# 代码示例

查看已有的[代码示例](https://github.com/cloudbypass/example)快速集成到项目。

![GitHub last commit](https://img.shields.io/github/last-commit/cloudbypass/example ":no-zoom")

* [Python SDK](/zh-cn/python_sdk) ![PyPI - Version](https://img.shields.io/pypi/v/cloudbypass ":no-zoom")
* [Nodejs SDK](/zh-cn/nodejs_sdk) ![NPM Version](https://img.shields.io/npm/v/cloudbypass-sdk ":no-zoom")
* [Go SDK](/zh-cn/golang_sdk) ![GitHub go.mod Go version](https://img.shields.io/github/go-mod/go-version/cloudbypass/golang-sdk ":no-zoom")

# 可访问性测试

通过使用[代码生成器](https://console.cloudbypass.com/#/code-generator)
检查目标网站是否可以突破，新注册用户可以[联系客服](https://t.me/cloudbypasscom)获取试用。

# 关于穿云API版本

## 穿云V1

> 在浏览器可以访问，通过程序代码访问就返回403的情况时使用。

穿云v1默认自带动态代理，也可以根据需求自行设置代理服务器，且每次请求都是无状态的。

## 穿云V2

> 当遇到以下`JS质询`或者`Turnstile`部件时使用

![turnstile.png](img%2Fturnstile.gif ":no-zoom :size=350")

?> 穿云V2必须提供固定或具有时效性的IP代理才能运作。

### 如何区分两种验证？

在穿云V2中，可以通过以下规则判断目标网站使用的是 `JS质询` 还是 `Turnstile` 验证机制：

1. **JS质询**
    - 当访问者**第一次加载网站页面**时，返回 HTTP 状态码 `403`。
    - 响应头中包含 `cf-mitigated: challenge` 字段。

2. **Turnstile**
    - 当**提交表单时**触发验证小部件。
    - 不符合以上 `JS质询` 的特征，即响应中不包含 `cf-mitigated: challenge` 字段。

### 突破 `JS质询`，穿云V2自动挑战

穿云V2支持两种模式来自动应对目标网站的 JS 质询机制，分别是 `Cookie` 模式和 `Part` 模式。以下是两种模式的具体说明：

**1. Cookie 模式**
客户端负责管理服务端返回的加密 Cookie。

- **会话管理**  
  客户端需具备会话管理功能。例如，Python 的 `requests` 库集成了会话管理模块，可用于在多个请求之间保持会话状态。

- **挑战成功**  
  穿云服务在挑战成功后，将加密后的 Cookie 返回给客户端。客户端在后续请求中携带这些 Cookie，即可持续保持会话状态。

- **挑战失败**  
  如果挑战失败，服务端会返回一个 JSON 格式的响应体，其中包括：
    - 请求 ID
    - [错误代码](/zh-cn/response_data?id=错误代码)
    - 错误信息

**2. Part 模式**
服务端托管验证 Cookie，支持通过会话分区实现更精细的控制。

- **分区控制**  
  配置请求头参数 `x-cb-part`，可实现服务端会话的分区管理，确保分区内的会话相互独立。

- **挑战成功**  
  穿云服务在挑战成功后，会将验证通过的 Cookie 存储在服务端的会话分区内，有效期为 10 分钟。在此期间：
    - 客户端发起的后续请求会自动携带分区内的 Cookie，保持会话状态。
    - 每次成功请求会刷新会话分区的有效期，确保持续访问。

- **挑战失败**  
  如果挑战失败，服务端会返回一个 JSON 格式的响应体，其中包括：
    - 请求 ID
    - [错误代码](/zh-cn/response_data?id=错误代码)
    - 错误信息

---

### 突破 `turnstile` 部件

穿云V2支持应对 `turnstile` 部件的验证机制。以下为具体操作说明：

**功能说明**

- **提供 `sitekey`**  
  用户需在请求头中填写参数 `x-cb-sitekey`，并提供对应的 [`sitekey`](/zh-cn/request_parameters?id=如何获取sitekey)。

- **验证结果**  
  通常情况下，`turnstile` 验证通过后会返回一个以 `0.` 开头的 Token 字符串，或者其他命名如 `cf-turnstile-response`
  或 `turnstileToken`，只是命名方式不同。

- **Token 使用方式**  
  穿云V2不会将 Token 直接返回到客户端，而是在需要使用 Token 的位置填充 `[cf_token]` 字符串，穿云会自动替换为有效的 Token
  并发起请求。

**使用示例**

以下为 Token 不同使用场景的示例代码：

1. **示例 1**  
   将 Token 放入请求头的 `Authorization` 字段：  
   [查看代码示例](https://github.com/cloudbypass/example/blob/main/code/com/berachain/faucet/artio/api_claim.py#L20)

2. **示例 2**  
   将 Token 放入请求头的 `X-Turnstile-Response` 字段：  
   [查看代码示例](https://github.com/cloudbypass/example/blob/main/code/com/joshsfrogs/login.py#L24)

3. **示例 3**  
   将 Token 放入请求体的 `accessToken` 字段：  
   [查看代码示例](https://github.com/cloudbypass/example/blob/main/code/com/cityline/api_otp.py#L22)

### 获取帮助

* [访问论坛](https://www.cloudbypass.com/blog/)
* [联系客服](https://t.me/cloudbypasscom)
