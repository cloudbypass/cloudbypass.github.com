# 请求参数

> HTTP 基础请求由请求行、请求头和请求体组成，其中请求行包括请求方法、请求 URL 和 HTTP 协议版本。
> <br/>由于穿云 API 采用 HTTP API 进行代理转发模式，您在请求穿云 API 时，需调整原始请求的 **请求 URL** 和 **请求头**。
> 调整后的请求将通过穿云 API 代理访问目标地址。

## 请求 URL 配置

穿云 API 使用 HTTPS 协议，并支持所有 HTTP 请求方法。您需要将目标地址的协议和主机名替换为穿云 API 地址进行访问。穿云 API 的请求地址为：

`https://api.cloudbypass.com`

?> 例如，若原始请求为 `https://example.io/user/login.html`，则应将其修改为 `https://api.cloudbypass.com/user/login.html`。

## 请求头配置

除了 URL 之外，您还需要以下请求头参数：

* [`x-cb-apikey`](/zh-cn/request_parameters?id=X-Cb-Apikey) *[APIKEY](/zh-cn/quickstart?id=获取apikey)* – 访问穿云 API 的唯一密钥。
* [`x-cb-host`](/zh-cn/request_parameters?id=x-cb-host、x-cb-protocol) – 目标服务器的主机名或 IP 地址（包括端口）。例如，访问 `https://www.example.com/to/path`，则此参数为 `www.example.com`，请求 URL 为 `https://api.cloudbypass.com/to/path`。
* [`x-cb-proxy`](/zh-cn/request_parameters?id=X-Cb-Proxy) – 设置代理服务器。穿云 V1 提供默认动态代理；穿云 V2 必须设置固定或具有时效性的 IP 代理。

?> 所有与穿云 API 相关的标头均以 `x-cb-*` 开头，穿云 API 在转发请求时不会携带这些请求头。

以下是用于自定义请求的请求头完整列表：

| 参数                                                                    | 类型     | 默认值                         | 支持版本  | 必填 | 描述                                                                 |
|-----------------------------------------------------------------------|:--------:|:------------------------------:|:--------:|:----:|---------------------------------------------------------------------|
| [x-cb-apikey](/zh-cn/request_parameters?id=APIKEY)                    | `string` | [去控制台获取](https://console.cloudbypass.com/#/api/) | `所有版本` | ![yes.svg](img%2Fyes.svg ":no-zoom") | 访问穿云 API 时使用的密钥。                                               |
| [x-cb-host](/zh-cn/request_parameters?id=x-cb-host、x-cb-protocol)     | `string` |                                | `所有版本` | ![yes.svg](img%2Fyes.svg ":no-zoom") | 请求的目标域名，例如：`opensea.io`，不要填协议和路径。                   |
| [x-cb-protocol](/zh-cn/request_parameters?id=x-cb-host、x-cb-protocol) | `string` | "https"                        | `所有版本` |      | 请求协议，例如：`http`、`https`。                                        |
| [x-cb-fp](/zh-cn/request_parameters?id=X-Cb-Fp)                       | `string` | [版本区分](/zh-cn/request_parameters?id=x-cb-fp) | `v1`     |      | 客户端指纹。                                                           |
| [x-cb-proxy](/zh-cn/request_parameters?id=X-Cb-Proxy)                 | `string` |                                | `所有版本` |      | 自定义代理地址，可以是 IP 或域名。支持 `http`、`socks5` 协议。          |
| x-cb-version                                                          | `string` |                                | `所有版本` |      | 使用穿云 V2 时，该请求头值应为 `2`。                                    |
| [x-cb-part](/zh-cn/request_parameters?id=X-Cb-Part)                   | `integer`|                                | `v2`     |      | 该请求头仅在穿云 V2 时有效，用于区分不同的会话，最多可有 1000 个会话分区。|
| [x-cb-origin](/zh-cn/request_parameters?id=关于浏览器跨域的问题)        | `string` |                                | `所有版本` |      | 替换请求头中的 `origin` 字段，常用于跨域请求绕过 CORS 限制。           |
| [x-cb-referer](/zh-cn/request_parameters?id=关于浏览器跨域的问题)       | `string` |                                | `所有版本` |      | 替换请求头中的 `referer` 字段，常用于跨域请求绕过 CORS 限制。          |
| x-cb-cookie                                                           | `string` |                                | `所有版本` |      | 替换请求头中的 `cookie` 字段，常用于跨域请求绕过 CORS 限制。           |
| [x-cb-sitekey](/zh-cn/request_parameters?id=如何获取sitekey)            | `string` |                                | `v2`     |      | 填写后触发 `Turnstile` 小部件验证，验证结果将自动填充后续请求。          |
| [x-cb-options](/zh-cn/request_parameters?id=配置选项列表)               | `string` |                                | `所有版本` |      | 配置选项列表，支持多个选项，逗号分隔。详细配置请查看 [配置选项列表](/zh-cn/request_parameters?id=配置选项列表)。 |

### 配置选项列表

`x-cb-options` 请求头的配置选项列表：

| 参数                                                           | 支持版本  | 描述                                                                                 |
|--------------------------------------------------------------|:--------:|------------------------------------------------------------------------------------|
| disable-redirect                                             | `所有版本` | 禁用重定向，遇到 300-399 响应码时会返回完整内容，包括 `Set-Cookie`。（默认自动处理重定向） |
| long-timeout                                                 | `v2`     | 延长超时，默认超时为 15 秒，目标服务器响应慢时可通过此参数延长至 60 秒。               |
| force                                                        | `v2`     | 强制更换代理，避免在穿云 V2 会话期内无法更换代理时返回 `BYPASS_ERROR` 错误。           |
| [ignore-lock](/zh-cn/request_parameters?id=关于V2 Part并发问题)  | `v2`     | 忽略挑战锁，多个请求同时使用同一个会话时，直接忽略验证挑战锁，避免错误。                |
| ~~[wait-lock](/zh-cn/request_parameters?id=关于V2 Part并发问题)~~ | `v2`     | ~~等待挑战锁，多个请求同时使用同一个会话时，防止 `CHALLENGE_LOCK_TIMEOUT` 错误。~~       |
| no-challenge                                                | `v2`     | 遇到验证时拒绝挑战，直接返回错误信息。                                     |


### APIKEY

`APIKEY`为每个账户唯一的穿云API请求授权访问密钥，是访问穿云API的必要参数之一。

?> 若`APIKEY`出现泄露问题，可以访问[穿云API控制台](https://console.cloudbypass.com/#/api/)重置。

访问`https://opensea.io/category/memberships`，请求示例：

<!-- tabs:start -->

#### **cURL**

```shell
# linux
curl --request GET \
--url "https://api.scrapingbypass.com/category/memberships" \
--header "x-cb-apikey: <APIKEY>" \
--header "x-cb-host: opensea.io"

# windows
curl --request GET ^
--url "https://api.scrapingbypass.com/category/memberships" ^
--header "x-cb-apikey: <APIKEY>" ^
--header "x-cb-host: opensea.io"
```

#### **Python**

```Python
import requests

url = "https://api.scrapingbypass.com/category/memberships"

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

	resp, err := client.R().Get("https://api.scrapingbypass.com/category/memberships")

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

const url = "https://api.scrapingbypass.com/category/memberships";
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
        String url = "https://api.scrapingbypass.com/category/memberships";
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
    * 支持 `127~139` 所有版本

### X-Cb-Part

穿云V2采用会话托管模式，所有cloudflare响应的cookie都将被存储到穿云服务器，用户可以通过设置`X-Cb-Part`请求头切换会话。
当验证通过后`cloudflare cookie`将保留10分钟，10分钟内再次请求成功则续期。

?> 在会话期内无法更换代理，如有业务需求可配置`x-cb-options: force`强制更换。(一般不推荐)

## 使用穿云V2进行请求

穿云V2适用于需要通过`JS质询`或者`Turnstile`部件的网站。

### `Part`模式请求示例

<!-- tabs:start -->

##### **cURL**

```shell
# linux
curl --request GET \
--url "https://api.scrapingbypass.com/accounts/label/lido" \
--header "x-cb-apikey: <APIKEY>" \
--header "x-cb-host: etherscan.io" \
--header "x-cb-version: 2" \
--header "x-cb-part: 0" \
--header "x-cb-proxy: <PROXY>"

# windows
curl --request GET ^
--url "https://api.scrapingbypass.com/accounts/label/lido" ^
--header "x-cb-apikey: <APIKEY>" ^
--header "x-cb-host: etherscan.io" ^
--header "x-cb-version: 2" ^
--header "x-cb-part: 0" ^
--header "x-cb-proxy: <PROXY>"
```

##### **Python**

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
from cloudbypass import SessionV2

if __name__ == '__main__':
    with SessionV2(apikey="<APIKEY>", proxy="http://proxy:port", part="0") as session:
        resp = session.get("https://etherscan.io/accounts/label/lido")
        print("Status:", resp.status_code, resp.headers.get("x-cb-status"))
        print("Body:", resp.text)
```

##### **Go**

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

##### **Nodejs**

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

try {
    const resp = (await cloudbypass.get("https://etherscan.io/accounts/label/lido", {
        cb_apikey: '/* APIKEY */',
        cb_proxy: '/* PROXY */',
        cb_part: '0'
    }));
    console.log(resp.headers['set-cookie']);
    console.log(resp.data);
} catch (e) {
    if (isBypassError(e)) {
        console.log(e.response.data || e.response || e.message);
    } else {
        console.log(e);
    }
}
```

##### **Java**

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

### `Cookie`模式请求示例

<!-- tabs:start -->

##### **cURL**

```shell
# linux
curl --request GET \
--url "https://api.scrapingbypass.com/accounts/label/lido" \
--header "x-cb-apikey: <APIKEY>" \
--header "x-cb-host: etherscan.io" \
--header "x-cb-version: 2" \
--header "x-cb-proxy: <PROXY>"

# windows
curl --request GET ^
--url "https://api.scrapingbypass.com/accounts/label/lido" ^
--header "x-cb-apikey: <APIKEY>" ^
--header "x-cb-host: etherscan.io" ^
--header "x-cb-version: 2" ^
--header "x-cb-proxy: <PROXY>"
```

##### **Python**

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
from cloudbypass import SessionV2

if __name__ == '__main__':
    with SessionV2(apikey="<APIKEY>", proxy="http://proxy:port") as session:
        resp = session.get("https://etherscan.io/accounts/label/lido")
        print("Status:", resp.status_code, resp.headers.get("x-cb-status"))
        print("Cookie:", resp.headers.get("set-cookie"))
        print("Body:", resp.text)
```

##### **Go**

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
		Proxy:  "/* PROXY */",
		UseV2:   true,
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

##### **Nodejs**

```javascript
const axios = require('axios');

const url = "https://api.cloudbypass.com/accounts/label/lido";
const headers = {
    'x-cb-apikey': '/* APIKEY */',
    'x-cb-host': 'etherscan.io',
    'x-cb-version': '2',
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

try {
    const resp = (await cloudbypass.get("https://etherscan.io/accounts/label/lido", {
        cb_apikey: '/* APIKEY */',
        cb_proxy: '/* PROXY */',
        cb_use_v2: true
    }));
    console.log(resp.headers['set-cookie']);
    console.log(resp.data);
} catch (e) {
    if (isBypassError(e)) {
        console.log(e.response.data || e.response || e.message);
    } else {
        console.log(e);
    }
}
```

##### **Java**

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
                .header("x-cb-proxy", "/* PROXY */")
                .GET(HttpRequest.BodyPublishers.noBody())
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());
    }
}
```

<!-- tabs:end -->

## 关于 V2 Part 模式并发问题

在 Part 模式下，穿云会根据 `"{host}_{part}"` 锁定会话，验证完成后释放锁。因此，当 `"{host}_{part}"` 被锁定时，无法进行请求。

?> 在多线程请求的情况下，推荐每个线程使用独立的 `part` 发起请求。这可以有效避免以下模式中出现的问题，并合理利用 `part`，从而减少验证次数、积分、流量和时间消耗。（推荐使用多线程）

### 锁定模式说明

* **`default`**  
  默认情况下，当遇到验证锁时，系统会返回 [`CHALLENGE_LOCK_OCCUPIED`](/zh-cn/response_data?id=错误代码) 错误，表示有一个同 `"{host}_{part}"` 的请求正在进行验证。

* **`ignore-lock`**  
  忽略验证锁，可以通过请求头 `x-cb-options: ignore-lock` 设置。
    * **优点**：避免所有锁定错误。
    * **缺点**：会消耗更多积分、流量和时间。

* ~~`wait-lock`~~  
  ~~等待验证锁，可以通过请求头 `x-cb-options: wait-lock` 设置。~~
    * ~~**优点**：可以避免 [`CHALLENGE_LOCK_OCCUPIED`](/zh-cn/response_data?id=错误代码) 错误，等待验证通过后会直接使用新的 Cookie 完成请求。~~
    * ~~**缺点**：如果等待时间过长，可能会出现 [`CHALLENGE_LOCK_TIMEOUT`](/zh-cn/response_data?id=错误代码) 错误。~~


## 关于浏览器跨域的问题

> **浏览器跨域** 是指由于浏览器的同源策略限制，不同源的文档或脚本不能相互交互的问题。  
> 同源策略是一种安全机制，它要求协议、域名和端口都必须相同，才能认为是同源。这样做的目的是防止恶意网站读取或操作其他网站的数据。  
> **跨域资源共享（CORS）** 是一种解决跨域问题的技术，它允许浏览器向不同源的服务器发送 HTTP 请求。

在浏览器发起接口请求时，浏览器会自动添加 `origin`、`referer` 等请求头，这些请求头是站点无法控制的。  
当这些请求头经过穿云 API 转发时，它们也会被传递到目标服务器，这可能导致请求失败。

为了解决这一问题，您可以通过配置 `x-cb-origin` 和 `x-cb-referer` 来覆盖部分与跨域相关的请求头。


## 如何获取sitekey

这里`sitekey`是指调用`turnstile`部件的主要参数，每个站点都有单独的`turnstile sitekey`。

?> 注意：`js质询`不需要填写sitekey

1. 打开浏览器`开发者工具`（Ctrl+Shift+I或F12）
2. 点击`网络`选项卡，确保`记录网络日志`按钮的状态如图所示<br />
   ![devtools_network.png](img%2Fdevtools_network.png)
3. 访问具有`turnstile`部件的页面
4. 在筛选器上输入`https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/b/turnstile/`
5. 如图选中的内容就是`sitekey` <br />
   ![devtools_network1.png](img%2Fdevtools_network1.png)
