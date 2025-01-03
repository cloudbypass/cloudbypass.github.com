# 请求参数

> 您可以了解一下：HTTP基础请求由请求行、请求头、请求体组成，其中请求行包含了请求方法、请求URL、HTTP协议版本。
> <br/>由于穿云API使用HTTP API进行代理转发的模式，在使用穿云API请求时，需要在原始请求上对**请求URL**、**请求头**进行一些调整。
> 经过调整后的请求将由穿云API代理访问目标地址。

### 请求URL配置

穿云API使用HTTPS协议，支持所有HTTP请求方法。您需要将目标地址协议和主机名替换为穿云API地址进行访问，以下是穿云API的请求地址：

`https://api.cloudbypass.com`

?> 如果要请求`https://example.io/user/login.html`，则需要修改为`https://api.cloudbypass.com/user/login.html`

### 请求头配置

除了URL之外还需要以下请求头参数：

* [`x-cb-apikey`](/zh-cn/request_parameters?id=X-Cb-Apikey) *[APIKEY](/zh-cn/quickstart?id=获取apikey) 访问穿云API的唯一密钥。
* [`x-cb-host`](/zh-cn/request_parameters?id=x-cb-host、x-cb-protocol) *
  目标服务器主机名或IP地址，包括端口。如访问`https://www.example.com/to/path`，则此参数为`www.example.com`，请求地址为`https://api.cloudbypass.com/to/path`。
* [`x-cb-proxy`](/zh-cn/request_parameters?id=X-Cb-Proxy) *设置代理服务器。穿云V1有默认动态代理; 穿云V2必须设置固定或具有时效性的IP代理。

?> 与穿云API关联所有标头都以`x-cb-*`开头，穿云API在转发请求时不会携带这些请求头。

以下是用于自定义请求的请求头完整列表：

| 参数                                                                    |    类型     |                       默认值                        |  支持版本  |                  必填                  | 描述                                                                                                                              |
|-----------------------------------------------------------------------|:---------:|:------------------------------------------------:|:------:|:------------------------------------:|---------------------------------------------------------------------------------------------------------------------------------|
| [x-cb-apikey](/zh-cn/request_parameters?id=APIKEY)                    | `string`  | [去控制台获取](https://console.cloudbypass.com/#/api/) | `所有版本` | ![yes.svg](img%2Fyes.svg ":no-zoom") | 访问穿云API时使用的密钥。                                                                                                                  |
| [x-cb-host](/zh-cn/request_parameters?id=x-cb-host、x-cb-protocol)     | `string`  |                                                  | `所有版本` | ![yes.svg](img%2Fyes.svg ":no-zoom") | 请求的目标域名，如：opensea.io，不要填协议和路径。                                                                                                  |
| [x-cb-protocol](/zh-cn/request_parameters?id=x-cb-host、x-cb-protocol) | `string`  |                     "https"                      | `所有版本` |                                      | 请求协议，如：http、https。                                                                                                              |
| [x-cb-fp](/zh-cn/request_parameters?id=X-Cb-Fp)                       | `string`  |   [版本区分](/zh-cn/request_parameters?id=x-cb-fp)    |  `v1`  |                                      | 客户端指纹。                                                                                                                          |
| [x-cb-proxy](/zh-cn/request_parameters?id=X-Cb-Proxy)                 | `string`  |                                                  | `所有版本` |                                      | 自定义代理地址，可以是IP或域名。<br />支持http、socks5协议，如：http://proxy.com:8080 或 http://username:password:proxy.com:8080。<br />协议头可选，不填默认为http。 |
| x-cb-version                                                          | `string`  |                                                  | `所有版本` |                                      | 当您需要使用穿云v2时，该请求头值应为`2`。                                                                                                         |
| [x-cb-part](/zh-cn/request_parameters?id=X-Cb-Part)                   | `integer` |                        0                         |  `v2`  |                                      | 该请求头仅在穿云v2时有效，用于区分不同的会话，用户最多可以拥有1000个会话分区（0~999）。                                                                               |
| [x-cb-origin](/zh-cn/request_parameters?id=关于浏览器跨域的问题)                | `string`  |                                                  | `所有版本` |                                      | 替换请求头中的origin字段，一般用于浏览器跨域请求绕过CORS限制。                                                                                            |
| [x-cb-referer](/zh-cn/request_parameters?id=关于浏览器跨域的问题)               | `string`  |                                                  | `所有版本` |                                      | 替换请求头中的referer字段，一般用于浏览器跨域请求绕过CORS限制。                                                                                           |
| x-cb-cookie                                                           | `string`  |                                                  | `所有版本` |                                      | 替换请求头中的cookie字段，一般用于浏览器跨域请求绕过CORS限制。                                                                                            |
| [x-cb-sitekey](/zh-cn/request_parameters?id=如何获取sitekey)              | `string`  |                                                  |  `v2`  |                                      | 填写后将触发`Turnstile`小部件验证。在请求数据中将cf_token值设置为[cf_token]，验证结果将自动替填充后请求。                                                             |
| [x-cb-options](/zh-cn/request_parameters?id=配置选项列表)                   | `string`  |                                                  | `所有版本` |                                      | 配置选项列表，可以填写多个附加配置选项，逗号分隔。详细请查看[配置选项列表](/zh-cn/request_parameters?id=配置选项列表)。                                                    |

### 配置选项列表

`x-cb-options`请求头配置选项列表：

| 参数                                                      |  支持版本  | 描述                                                                                                              |
|---------------------------------------------------------|:------:|-----------------------------------------------------------------------------------------------------------------|
| disable-redirect                                        | `所有版本` | 禁用重定向，服务端遇到300~399响应码时将会返回，Set-Cookie将会返回完整内容。（默认自动处理重定向，SDK默认配置）。                                              |
| long-timeout                                            | `v2` | 超时延长，默认超时为15秒，如果目标服务器响应慢可以通过设置此参数延迟至60秒。                                                                        |
| force                                                   |  `v2`  | 正常情况下，在穿云V2会话期内无法更换代理，会返回[`BYPASS_ERROR`](/zh-cn/response_data?id=错误代码)错误。使用`force`配置可以强制替换代理。                  |
| [ignore-lock](/zh-cn/request_parameters?id=关于v2并发请求的问题) |  `v2`  | 使用忽略挑战锁配置，当两个或多个请求同时使用同一个会话时，直接忽略验证挑战锁，可以防止出现**CHALLENGE_LOCK_TIMEOUT**或**CHALLENGE_LOCK_OCCUPIED**错误。          |
| [wait-lock](/zh-cn/request_parameters?id=关于v2并发请求的问题)   |  `v2`  | 使用等待挑战锁配置，当两个或多个请求同时使用同一个会话时，可以防止出现[CHALLENGE_LOCK_TIMEOUT](/zh-cn/response_data?id=错误代码)错误。（比ignore-lock优先级更高） |

### APIKEY

`APIKEY`为每个账户唯一的穿云API请求授权访问密钥，是访问穿云API的必要参数之一。

?> 若`APIKEY`出现泄露问题，可以访问[穿云API控制台](https://console.cloudbypass.com/#/api/)重置。

访问`https://opensea.io/category/memberships`，请求示例：



<!-- tabs:start -->

#### **cURL**

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

#### **Python**

```Python
import requests

url = "https://api.cloudbypass.com/category/memberships"

headers = {
    'x-cb-apikey': '<APIKEY>',
    'x-cb-host': 'opensea.io',
}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

* **Python SDK**

```Python
# pip install cloudbypass --upgrade
from cloudbypass import Session

if __name__ == '__main__':
    with Session(apikey="<APIKEY>") as session:
        resp = session.get("https://opensea.io/category/memberships")
        print(resp.status_code, resp.headers.get("x-cb-status"))
        print(resp.text)
```

#### **Go**

```go
// # Go Modules
// require github.com/go-resty/resty/v2 v2.7.0
package main

import (
	"fmt"
	"github.com/go-resty/resty/v2"
)

func main() {
	client := resty.New()

	client.Header.Add("X-Cb-Apikey", "/* APIKEY */")
	client.Header.Add("X-Cb-Host", "opensea.io")

	resp, err := client.R().Get("https://api.cloudbypass.com/category/memberships")

	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println(resp.StatusCode(), resp.Header().Get("X-Cb-Status"))
	fmt.Println(resp.String())
}
```

* **Go SDK**

```go
// https://github.com/cloudbypass/golang-sdk
package main

import (
	"fmt"
	"github.com/cloudbypass/golang-sdk/cloudbypass"
)

func main() {
	client := cloudbypass.New(cloudbypass.BypassConfig{
		Apikey: "/* APIKEY */",
	})

	resp, err := client.R().
		EnableTrace().
		Get("https://opensea.io/category/memberships")

	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println(resp.StatusCode(), resp.Header().Get("X-Cb-Status"))
	fmt.Println(resp.String())
}
```

#### **Nodejs**

```javascript
const axios = require('axios');

const url = "https://api.cloudbypass.com/category/memberships";
const headers = {
    'x-cb-apikey': '/* APIKEY */',
    'x-cb-host': 'opensea.io',
};

axios.get(url, {}, {headers: headers})
    .then(response => console.log(response.data))
    .catch(error => console.error(error));
```

* **Nodejs SDK**

```javascript
// https://github.com/cloudbypass/nodejs-sdk
import cloudbypass from 'cloudbypass-sdk';

cloudbypass.get('https://opensea.io/category/memberships', {
    cb_apikey: '/* APIKEY */'
})
    .then(function (response) {
        console.log(response.status, response.headers.get("x-cb-status"));
        console.log(response.data);
    })
    .catch(function (error) {
        console.log(error.response.data || error.response || error.message);
    });
```

#### **Java**

```Java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;


public class Main {
    public static void main(String[] args) throws Exception {
        String url = "https://api.cloudbypass.com/category/memberships";
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("x-cb-apikey", "/* APIKEY */")
                .header("x-cb-host", "opensea.io")
                .GET(HttpRequest.BodyPublishers.noBody())
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());
    }
}
```

<!-- tabs:end -->

### X-Cb-Host、X-Cb-Protocol

`X-Cb-Host`和`X-Cb-Protocol`也是访问穿云API的必要参数。
`X-Cb-Protocol`默认为https，所以一般不用设置。

?> 将原始请求URL中的协议、主机域名（或IP）、端口号替换为穿云API地址(`https://api.cloudbypass.com`)，`X-Cb-Host`
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

##### 如果原始请求是http协议：

```http request
# 原始请求
GET http://example.io/user/login.html

# 修改后的请求
GET https://api.cloudbypass.com/user/login.html
X-Cb-Apikey: <APIKEY>
X-Cb-Host: example.io
X-Cb-Protocol: http
```

### X-Cb-Proxy

客户端自定义代理，支持HTTP、Socks5协议

支持格式如下

* 用户名:密码@主机名:端口 (默认http协议)
* 用户名:密码:主机名:端口 (默认http协议)
* 协议://用户名:密码@主机名:端口
* 协议://用户名:密码:主机名:端口
* 协议:用户名:密码:主机名:端口

### X-Cb-Fp

设置请求时使用的浏览器指纹。以下是支持列表

* 穿云V1（默认`chrome`）
    * `chrome`
    * `firefox`
    * `edge`
* 穿云V2（默认`edge-linux`）
    * `chrome`、`chrome-linux`、`chrome-mac`、`chrome127`、`chrome127-linux`、`chrome127-mac`
    * `edge`、`edge-linux`、`edge-mac`、`edge127`、`edge127-linux`、`edge127-mac`
    * `chrome-android`、`edge-android`、`chrome127-android`、`edge127-android`

### X-Cb-Part

穿云V2采用会话托管模式，所有cloudflare响应的cookie都将被存储到穿云服务器，用户可以通过设置`X-Cb-Part`请求头切换会话。
当验证通过后`cloudflare cookie`将保留10分钟，10分钟内再次请求成功则续期。

?> 在会话期内无法更换代理，如有业务需求可配置`x-cb-options: force`强制更换。(一般不推荐)

### 使用穿云V2进行请求

穿云API V2适用于需要通过`JS质询`验证的网站。例如访问`https://etherscan.io/accounts/label/lido`，请求示例：

<!-- tabs:start -->

#### **cURL**

```shell
# linux
curl --request GET \
--url "https://api.cloudbypass.com/accounts/label/lido" \
--header "x-cb-apikey: <APIKEY>" \
--header "x-cb-host: etherscan.io" \
--header "x-cb-version: 2" \
--header "x-cb-part: 0" \
--header "x-cb-proxy: <PROXY>"

# windows
curl --request GET ^
--url "https://api.cloudbypass.com/accounts/label/lido" ^
--header "x-cb-apikey: <APIKEY>" ^
--header "x-cb-host: etherscan.io" ^
--header "x-cb-version: 2" ^
--header "x-cb-part: 0" ^
--header "x-cb-proxy: <PROXY>"
```

#### **Python**

```Python
import requests

url = "https://api.cloudbypass.com/accounts/label/lido"

headers = {
    'x-cb-apikey': '<APIKEY>',
    "x-cb-host": r"etherscan.io",
    "x-cb-version": r"2",
    "x-cb-part": r"0",
    "x-cb-proxy": r"<PROXY>",
}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

* **Python SDK**

```Python
# pip install cloudbypass --upgrade
from cloudbypass import Session

if __name__ == '__main__':
    with Session(apikey="<APIKEY>", proxy="<PROXY>") as session:
        resp = session.get("https://etherscan.io/accounts/label/lido", part="0")
        print(resp.status_code, resp.headers.get("x-cb-status"))
        print(resp.text)
```

#### **Go**

```go
// # Go Modules
// require github.com/go-resty/resty/v2 v2.7.0
package main

import (
	"fmt"
	"github.com/go-resty/resty/v2"
)

func main() {
	client := resty.New()

	client.Header.Add("X-Cb-Apikey", "/* APIKEY */")
	client.Header.Add("X-Cb-Host", "etherscan.io")
	client.Header.Add("X-Cb-Proxy", "/* PROXY */")
	client.Header.Add("X-Cb-Version", "2")
	client.Header.Add("X-Cb-Part", "0")

	resp, err := client.R().Get("https://api.cloudbypass.com/accounts/label/lido")

	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println(resp.StatusCode(), resp.Header().Get("X-Cb-Status"))
	fmt.Println(resp.String())
}
```

* **Go SDK**

```go
// https://github.com/cloudbypass/golang-sdk
package main

import (
	"fmt"
	"github.com/cloudbypass/golang-sdk/cloudbypass"
)

func main() {
	client := cloudbypass.New(cloudbypass.BypassConfig{
		Apikey: "/* APIKEY */",
		Part:   "0",
		Proxy:  "/* PROXY */",
	})

	resp, err := client.R().
		EnableTrace().
		Get("https://etherscan.io/accounts/label/lido")

	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println(resp.StatusCode(), resp.Header().Get("X-Cb-Status"))
	fmt.Println(resp.String())
}
```

#### **Nodejs**

```javascript
const axios = require('axios');

const url = "https://api.cloudbypass.com/accounts/label/lido";
const headers = {
    'x-cb-apikey': '/* APIKEY */',
    'x-cb-host': 'etherscan.io',
    'x-cb-version': '2',
    'x-cb-part': '0',
    'x-cb-proxy': '/* PROXY */',
};

axios.get(url, {}, {headers: headers})
    .then(response => console.log(response.data))
    .catch(error => console.error(error));
```

* **Nodejs SDK**

```javascript
// https://github.com/cloudbypass/nodejs-sdk
import cloudbypass from 'cloudbypass-sdk';

cloudbypass.get('https://etherscan.io/accounts/label/lido', {
    cb_apikey: '/* APIKEY */',
    cb_part: '0',
    cb_proxy: '/* PROXY */'
})
    .then(function (response) {
        console.log(response.status, response.headers.get("x-cb-status"));
        console.log(response.data);
    })
    .catch(function (error) {
        console.log(error.response.data || error.response || error.message);
    });
```

#### **Java**

```Java
// Use java to request https://opensea.io/category/memberships
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;


public class Main {
    public static void main(String[] args) throws Exception {
        String url = "https://api.cloudbypass.com/accounts/label/lido";
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("x-cb-apikey", "/* APIKEY */")
                .header("x-cb-host", "etherscan.io")
                .header("x-cb-version", "2")
                .header("x-cb-part", "0")
                .header("x-cb-proxy", "/* PROXY */")
                .GET(HttpRequest.BodyPublishers.noBody())
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());
    }
}
```

<!-- tabs:end -->

### 关于V2并发请求的问题

遇到验证时会根据`"{host}_{part}"`进行上锁，验证完成后释放，所以默认`"{host}_{part}"`锁定状态下是无法进行请求的。

?> 推荐多线程请求的情况下，每个线程使用单独的`part`发起请求，可以避免以下模式中出现的各种问题。这样合理使用`part`
可以避免出现更多验证以及减少积分、流量、时间的消耗。(多线程推荐)

* `default` 默认情况下遇到验证锁时会返回[`CHALLENGE_LOCK_OCCUPIED`](/zh-cn/response_data?id=错误代码)
  错误，这表示有一条同`"{host}_{part}"`的请求正在验证中。
* `ignore-lock` 忽略验证锁，通过请求头`x-cb-options: ignore-lock`设置。
    * 优点：可以避免所有锁错误
    * 缺点：消耗更多的积分、流量、时间
* `wait-lock` 等待验证锁，通过请求头`x-cb-options: wait-lock`设置。
    * 优点：可以避免[`CHALLENGE_LOCK_OCCUPIED`](/zh-cn/response_data?id=错误代码)错误，等待验证通过后将会直接使用新的Cookie完成请求
    * 缺点：如果等待时间过长，可能出现[`CHALLENGE_LOCK_TIMEOUT`](/zh-cn/response_data?id=错误代码)错误

### 关于浏览器跨域的问题

> 您可以了解一下：浏览器跨域是指由于浏览器的同源策略限制，不同源的文档或脚本不能相互交互的问题。
> 同源策略是一种安全机制，它要求协议、域名和端口都相同才能认为是同源。这是为了防止恶意网站读取或操作其他网站的数据。
> 跨域资源共享（CORS）是一种解决跨域问题的技术，它允许浏览器向不同源的服务器发送HTTP请求。

一般浏览器在请求接口时会自动补充`origin`、`referer`这些站点无法控制的请求头，
这些请求头到穿云API后也会被转发至目标服务器，导致请求失败，
所以通过配置`x-cb-origin`、`x-cb-referer`可以对部分跨域相关请求头进行覆盖。

### 如何获取sitekey

这里`sitekey`是指调用`turnstile`部件的主要参数，每个站点都有单独的`turnstile sitekey`。

?> 注意：`js质询`不需要填写sitekey

1. 打开浏览器`开发者工具`（Ctrl+Shift+I或F12）
2. 点击`网络`选项卡，确保`记录网络日志`按钮的状态如图所示<br />
   ![devtools_network.png](img%2Fdevtools_network.png)
3. 访问具有`turnstile`部件的页面
4. 在筛选器上输入`https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/b/turnstile/`
5. 如图选中的内容就是`sitekey` <br />
   ![devtools_network1.png](img%2Fdevtools_network1.png)
