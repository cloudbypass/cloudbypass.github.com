# 快速开始

>
使用穿云可以帮助您轻松绕过Cloudflare的验证，目前支持绕过JS质询、Turnstile等产品验证。本文档提供了穿云[HTTP API](/zh-cn/request_parameters)、[本地代理工具](/zh-cn/proxy_tools)
以及[SDK](/zh-cn/quickstart?id=代码示例)的详细使用方法。

### 工作流程

穿云API的请求流程

![cloudbypass_api_fc.svg](img/cloudbypass_api_fc.svg)

?> 无论使用[本地代理工具](/zh-cn/proxy_tools)或是[SDK](/zh-cn/quickstart?id=代码示例)都只是对请求进行转发，实际上还是HTTP
API请求。

### 获取APIKEY

访问[穿云API控制台](https://console.cloudbypass.com/#/api/)注册账户获取APIKEY。

### 代码示例

查看已有的[代码示例](https://github.com/cloudbypass/example)快速集成到项目。

![GitHub last commit](https://img.shields.io/github/last-commit/cloudbypass/example ":no-zoom")

* [Python SDK](/zh-cn/python_sdk) ![PyPI - Version](https://img.shields.io/pypi/v/cloudbypass ":no-zoom")
* [Nodejs SDK](/zh-cn/nodejs_sdk) ![NPM Version](https://img.shields.io/npm/v/cloudbypass-sdk ":no-zoom")
* [Go SDK](/zh-cn/golang_sdk) ![GitHub go.mod Go version](https://img.shields.io/github/go-mod/go-version/cloudbypass/golang-sdk ":no-zoom")

### 可访问性测试

通过使用[代码生成器](https://console.cloudbypass.com/#/code-generator)
检查目标网站是否可以突破，新注册用户可以[联系客服](https://t.me/cloudbypasscom)获取试用。

### 关于穿云API版本

#### 穿云V1

> 在浏览器可以访问，通过程序代码访问就返回403的情况时使用。

穿云v1默认自带动态代理，也可以根据需求自行设置代理服务器，且每次请求都是无状态的。

#### 穿云V2

> 当遇到以下`js质询`或者`turnstile`部件时使用

![turnstile.png](img%2Fturnstile.gif ":no-zoom :size=350")

?> 穿云V2必须提供固定或具有时效性的IP代理才能运作。

* **突破`js质询`，穿云V2会自动进行挑战**
    * 挑战成功后穿云服务将存储`cloudflare cookie`持续10分钟，后续请求会自动使用该会话进行访问，再次请求成功后会话将自动续期。
    * 可以通过配置`x-cb-part`参数设置会话分区，实现会话隔离效果。
    * 挑战失败后会响应json格式响应体，包含请求ID、[错误代码](/zh-cn/response_data?id=错误代码)、错误信息。
* **突破`turnstile`部件**
    * 用户需要提供[`sitekey`](/zh-cn/request_parameters?id=如何获取sitekey)，填写到请求头`x-cb-sitekey`。
    * 一般在验证通过后`turnstile`会返回一个`0.`开头的token字符串，也可能是`cf-turnstile-response`、`turnstileToken`
      等，只是命名不同。
    * 穿云V2不会将其token返回到客户端，在需要token的位置补充`[cf-token]`字符串，穿云会自动填充后发起请求。
        * [查看示例1](https://github.com/cloudbypass/example/blob/main/code/com/berachain/faucet/artio/api_claim.py#L20)
          将`token`放到了请求头`Authorization`。
        * [查看示例2](https://github.com/cloudbypass/example/blob/main/code/com/joshsfrogs/login.py#L24)
          将`token`放到了请求头`X-Turnstile-Response`。
        * [查看示例3](https://github.com/cloudbypass/example/blob/main/code/com/cityline/api_otp.py#L22)
          将`token`放到了请求体`accessToken`。

### 获取帮助

* [访问论坛](https://www.cloudbypass.com/blog/)
* [联系客服](https://t.me/cloudbypasscom)
