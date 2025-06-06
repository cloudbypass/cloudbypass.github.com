# Request Parameters

> The basic HTTP request consists of the request line, headers, and body, where the request line includes the request
> method, request URL, and HTTP version.
> <br/>Since Scrapingbypass API uses an HTTP API for proxy forwarding, when making requests to the Scrapingbypass API,
> you need to adjust the **request URL** and **request headers** of the original request.
> The adjusted request will be proxied through the Scrapingbypass API to access the target address.

## Request URL Configuration

Scrapingbypass API uses the HTTPS protocol and supports all HTTP request methods. You need to replace the protocol and
hostname of the target address with the Scrapingbypass API address. The request address for Scrapingbypass API is:

`https://console.scrapingbypass.com`

?> For example, if the original request is `https://example.io/user/login.html`, it should be modified
to `https://console.scrapingbypass.com/user/login.html`.

## Request Header Configuration

In addition to the URL, you will also need the following request header parameters:

* [`x-cb-apikey`](/us-en/request_parameters?id=x-cb-apikey) *[APIKEY](/us-en/quickstart?id=获取apikey)* – The unique key
  to access Scrapingbypass API.
* [`x-cb-host`](/us-en/request_parameters?id=x-cb-host-x-cb-protocol) – The hostname or IP address (including port) of
  the target server. For example, to access `https://www.example.com/to/path`, this parameter would
  be `www.example.com`, and the request URL would be `https://console.scrapingbypass.com/to/path`.
* [`x-cb-proxy`](/us-en/request_parameters?id=x-cb-proxy) – Set the proxy server. Scrapingbypass V1 provides a default
  dynamic proxy, while Scrapingbypass V2 requires setting a fixed or time-sensitive IP proxy.

?> All headers related to Scrapingbypass API start with `x-cb-*`, and Scrapingbypass API does not carry these headers
when forwarding requests.

Here is the complete list of request headers for custom requests:

| Parameter                                                                           |   Type    |                          Default Value                          | Supported Versions |               Required               | Description                                                                                                                                                                       |
|-------------------------------------------------------------------------------------|:---------:|:---------------------------------------------------------------:|:------------------:|:------------------------------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [x-cb-apikey](/us-en/request_parameters?id=apikey)                                  | `string`  |  [Get from Console](https://console.scrapingbypass.com/#/api/)  |   `All Versions`   | ![yes.svg](img%2Fyes.svg ":no-zoom") | The key used when accessing Scrapingbypass API.                                                                                                                                   |
| [x-cb-host](/us-en/request_parameters?id=x-cb-host-x-cb-protocol)                   | `string`  |                                                                 |   `All Versions`   | ![yes.svg](img%2Fyes.svg ":no-zoom") | The target domain of the request, e.g., `opensea.io`. Do not include the protocol and path.                                                                                       |
| [x-cb-protocol](/us-en/request_parameters?id=x-cb-host-x-cb-protocol)               | `string`  |                             "https"                             |   `All Versions`   |                                      | The request protocol, e.g., `http`, `https`.                                                                                                                                      |
| [x-cb-fp](/us-en/request_parameters?id=x-cb-fp)                                     | `string`  | [Version Differentiation](/us-en/request_parameters?id=x-cb-fp) |        `v1`        |                                      | Client fingerprint.                                                                                                                                                               |
| [x-cb-proxy](/us-en/request_parameters?id=x-cb-proxy)                               | `string`  |                                                                 |   `All Versions`   |                                      | Custom proxy address, can be an IP or domain. Supports `http` and `socks5` protocols.                                                                                             |
| x-cb-version                                                                        | `string`  |                                                                 |   `All Versions`   |                                      | When using Scrapingbypass V2, this header should have the value `2`.                                                                                                              |
| [x-cb-part](/us-en/request_parameters?id=x-cb-part)                                 | `integer` |                                                                 |        `v2`        |                                      | This header is valid only in Scrapingbypass V2, used to differentiate sessions, with a maximum of 1000 session partitions.                                                        |
| [x-cb-origin](/us-en/request_parameters?id=about-the-browser-cross-domain-problem)  | `string`  |                                                                 |   `All Versions`   |                                      | Replaces the `origin` field in the request header, commonly used to bypass CORS restrictions.                                                                                     |
| [x-cb-referer](/us-en/request_parameters?id=about-the-browser-cross-domain-problem) | `string`  |                                                                 |   `All Versions`   |                                      | Replaces the `referer` field in the request header, commonly used to bypass CORS restrictions.                                                                                    |
| x-cb-cookie                                                                         | `string`  |                                                                 |   `All Versions`   |                                      | Replaces the `cookie` field in the request header, commonly used to bypass CORS restrictions.                                                                                     |
| [x-cb-sitekey](/us-en/request_parameters?id=how-to-get-sitekey)                     | `string`  |                                                                 |        `v2`        |                                      | Triggers the `Turnstile` widget verification, and the verification result will automatically populate subsequent requests.                                                        |
| [x-cb-options](/us-en/request_parameters?id=configuration-options-list)             | `string`  |                                                                 |   `All Versions`   |                                      | List of configuration options, supports multiple options separated by commas. For detailed configurations, see [Configuration Options List](/us-en/request_parameters?id=配置选项列表). |

### Configuration Options List

List of configuration options for the `x-cb-options` request header:

| Parameter                                                                           | Supported Versions | Description                                                                                                                                                               |
|-------------------------------------------------------------------------------------|:------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| disable-redirect                                                                    |   `All Versions`   | Disable redirects; when encountering a 300-399 response code, it will return the full content, including `Set-Cookie`. (By default, redirects are handled automatically.) |
| long-timeout                                                                        |        `v2`        | Extend the timeout. The default timeout is 15 seconds, and this can be extended to 60 seconds when the target server responds slowly.                                     |
| force                                                                               |        `v2`        | Force the proxy change to avoid returning a `BYPASS_ERROR` when the proxy cannot be changed during a Scrapingbypass V2 session.                                           |
| [ignore-lock](/us-en/request_parameters?id=about-v2-part-mode-concurrency-issues)   |        `v2`        | Ignore challenge lock. When multiple requests use the same session, it will directly ignore the verification challenge lock to avoid errors.                              |
| ~~[wait-lock](/us-en/request_parameters?id=about-v2-part-mode-concurrency-issues)~~ |        `v2`        | ~~Wait for the challenge lock. When multiple requests use the same session, it prevents the `CHALLENGE_LOCK_TIMEOUT` error.~~                                             |
| no-challenge                                                                        |        `v2`        | When encountering verification, reject the challenge and directly return an error message.                                                                                     |

### APIKEY

`APIKEY` is a unique authorization key for each account to access the Scrapingbypass API and is one of the necessary
parameters for API requests.

?> If your `APIKEY` is compromised, you can reset it by visiting
the [Scrapingbypass API Console](https://console.scrapingbypass.com/#/api/).

Example request to `https://opensea.io/category/memberships`:

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

### X-Cb-Host, X-Cb-Protocol

`X-Cb-Host` and `X-Cb-Protocol` are also required parameters for accessing the Scrapingbypass API.
The default value for `X-Cb-Protocol` is `https`, so you generally don't need to set it.

?> Replace the protocol, domain name (or IP), and port number in the original request URL with the Scrapingbypass API
address (`https://api.cloudbypass.com`). The `X-Cb-Host` header should contain the domain name that was replaced.
Here is an HTTP example:

```http request
# Original Request
GET https://example.io/user/login.html

# Modified Request
GET https://api.cloudbypass.com/user/login.html
X-Cb-Apikey: <APIKEY>
X-Cb-Host: example.io
```

##### If the original request uses the HTTP protocol:

```http request
# Original Request
GET http://example.io/user/login.html

# Modified Request
GET https://api.cloudbypass.com/user/login.html
X-Cb-Apikey: <APIKEY>
X-Cb-Host: example.io
X-Cb-Protocol: http
```

### X-Cb-Proxy

Custom proxy for the client, supporting HTTP and Socks5 protocols.

Supported formats are as follows:

* `username:password@hostname:port` (default is HTTP protocol)
* `username:password:hostname:port` (default is HTTP protocol)
* `protocol://username:password@hostname:port`
* `protocol://username:password@hostname:port`
* `protocol:username:password:hostname:port`

### X-Cb-Fp

Set the browser fingerprint used in the request. The following are the supported list:

* Scrapingbypass V1 (default `chrome`）
    * `chrome`
    * `firefox`
    * `edge`
* Scrapingbypass V2 (default `edge-linux`）
    * `chrome`、`chrome-linux`、`chrome-mac`、`chrome127`、`chrome127-linux`、`chrome127-mac`
    * `edge`、`edge-linux`、`edge-mac`、`edge127`、`edge127-linux`、`edge127-mac`
    * `chrome-android`、`edge-android`、`chrome127-android`、`edge127-android`

### X-Cb-Part

Scrapingbypass V2 uses session-based management, where all Cloudflare response cookies are stored on the Scrapingbypass
servers. Users can switch sessions by setting the `X-Cb-Part` request header.
After the validation succeeds, the `cloudflare cookie` will remain valid for 10 minutes. If another request is made
within 10 minutes, the session will be extended.

?> During the session, the proxy cannot be changed. If needed, you can configure `x-cb-options: force` to force a proxy
change. (Generally not recommended.)

## Using Scrapingbypass V2 for Requests

Scrapingbypass V2 is suitable for websites that require `JS Challenges` or `Turnstile` widgets.

### `Part` Mode Request Example

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

### `Cookie` Mode Request Example

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

## About V2 Part Mode Concurrency Issues

In Part mode, Scrapingbypass locks the session based on `"{host}_{part}"`, and the lock is released after validation is
complete. Therefore, when `"{host}_{part}"` is locked, requests cannot be made.

?> In multi-threaded requests, it is recommended that each thread use a unique `part` to make requests. This can
effectively avoid issues in the following modes and make better use of `part`, thus reducing validation times, credits,
traffic, and time consumption. (Multi-threading is recommended.)

### Locking Mode Description

* **`default`**  
  By default, when a validation lock is encountered, the system returns
  a [`CHALLENGE_LOCK_OCCUPIED`](/us-en/response_data?id=error-code) error, indicating that a request with the
  same `"{host}_{part}"` is being validated.

* **`ignore-lock`**  
  Ignore the validation lock, which can be set by the request header `x-cb-options: ignore-lock`.
    * **Advantages**: Avoids all locking errors.
    * **Disadvantages**: Consumes more credits, traffic, and time.

* ~~`wait-lock`~~  
  ~~Wait for the validation lock, which can be set by the request header `x-cb-options: wait-lock`.~~
    * ~~**Advantages**: Avoids the [`CHALLENGE_LOCK_OCCUPIED`](/us-en/response_data?id=error-code) error. After
      validation, it will directly use the new cookie to complete the request.~~
    * ~~**Disadvantages**: If the wait time is too long,
      the [`CHALLENGE_LOCK_TIMEOUT`](/us-en/response_data?id=error-code) error may occur.~~

## About Browser Cross-Origin Issues

> **Browser Cross-Origin** refers to the issue where documents or scripts from different origins cannot interact due to
> the browser's same-origin policy.  
> The same-origin policy is a security mechanism that requires the protocol, domain, and port to be the same to be
> considered the same origin. This is done to prevent malicious websites from reading or manipulating data from other
> websites.  
> **Cross-Origin Resource Sharing (CORS)** is a technology to solve the cross-origin issue, allowing browsers to send
> HTTP requests to servers from different origins.

When the browser initiates an API request, it automatically adds request headers like `origin`, `referer`, etc., which
the site cannot control.  
When these headers are forwarded through the Scrapingbypass API, they will also be passed to the target server, which
may lead to request failure.

To solve this problem, you can configure `x-cb-origin` and `x-cb-referer` to override some of the cross-origin-related
request headers.

## How to Obtain Sitekey

Here, `sitekey` refers to the primary parameter for invoking the `turnstile` widget, and each site has a
unique `turnstile sitekey`.

?> Note: `JS Challenges` do not require a sitekey.

1. Open the browser's `Developer Tools` (Ctrl+Shift+I or F12)
2. Click the `Network` tab, ensuring that the `Record network log` button is in the state shown in the image below<br />
   ![devtools_network.png](img%2Fdevtools_network.png)
3. Visit a page with the `turnstile` widget
4. In the filter, type `https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/b/turnstile/`
5. The highlighted content in the image is the `sitekey` <br />
   ![devtools_network1.png](img%2Fdevtools_network1.png)
