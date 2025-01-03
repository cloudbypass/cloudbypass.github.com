# Request parameter

> Understand: HTTP basic request consists of request line, request header, and request body, where the request line
> contains the request method, request URL, and HTTP protocol version.
> <br/>Since the Scrapingbypass API uses the HTTP API for proxy forwarding, when using the Scrapingbypass API request,
> you need to make some adjustments to the **request URL** and **request header** on the original request.
> The adjusted request will be proxied by the Scrapingbypass API to access the target address.

### URL Configuration

The Scrapingbypass API uses the HTTPS protocol and supports all HTTP request methods. You need to replace the target
address protocol and host name with the Scrapingbypass API address to access it. The following is the request address of
the Scrapingbypass API:

`https://api.scrapingbypass.com`

?> If you want to request `https://example.io/user/login.html`, you need to change it
to `https://api.scrapingbypass.com/user/login.html`

### Header configuration

n addition to the URL, the following request header parameters are required:

* [`x-cb-apikey`](/us-en/request_parameters?id=X-Cb-Apikey) *[APIKEY](/us-en/quickstart?id=get-apikey) A unique key to
  access the Scrapingbypass API.
* [`x-cb-host`](/us-en/request_parameters?id=x-cb-host、x-cb-protocol) *
  The target server host name or IP address, including the port. If you access `https://www.example.com/to/path`, this
  parameter is `www.example.com` and the request address is `https://api.scrapingbypass.com/to/path`.
* [`x-cb-proxy`](/us-en/request_parameters?id=X-Cb-Proxy) *Set up a proxy server. Scrapingbypass V1 has a default
  dynamic proxy; Scrapingbypass V2 must set up a fixed or time-sensitive IP proxy.

?> All headers associated with the Scrapingbypass API start with `x-cb-*`. The Scrapingbypass API does not carry these
request headers when forwarding requests.

The following is a complete list of request headers used for custom requests:

| PARAMETER                                                                           |   TYPE    |                           DEFAULT                           | SUPPORTED VERSION |               Required               | DESCRIPTION                                                                                                                                                                                                                                                    |
|-------------------------------------------------------------------------------------|:---------:|:-----------------------------------------------------------:|:-----------------:|:------------------------------------:|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [x-cb-apikey](/us-en/request_parameters?id=APIKEY)                                  | `string`  |   [Get APIKEY](https://console.scrapingbypass.com/#/api/)   |       `All`       | ![yes.svg](img%2Fyes.svg ":no-zoom") | The key to use when accessing the Scrapingbypass API.                                                                                                                                                                                                          |
| [x-cb-host](/us-en/request_parameters?id=x-cb-host、x-cb-protocol)                   | `string`  |                                                             |       `All`       | ![yes.svg](img%2Fyes.svg ":no-zoom") | The target domain name of the request, such as opensea.io. Do not fill in the protocol and path.                                                                                                                                                               |
| [x-cb-protocol](/us-en/request_parameters?id=x-cb-host、x-cb-protocol)               | `string`  |                           "https"                           |       `All`       |                                      | Request protocol, such as http, https.                                                                                                                                                                                                                         |
| [x-cb-fp](/us-en/request_parameters?id=X-Cb-Fp)                                     | `string`  | [Version distinction](/us-en/request_parameters?id=x-cb-fp) |       `v1`        |                                      | Client fingerprint.                                                                                                                                                                                                                                            |
| [x-cb-proxy](/us-en/request_parameters?id=X-Cb-Proxy)                               | `string`  |                                                             |       `All`       |                                      | Custom proxy address, which can be IP or domain name.<br />Supports http and socks5 protocols, such as: http://proxy.com:8080 or http://username:password:proxy.com:8080. <br /> The protocol header is optional. If it is not filled in, the default is http. |
| x-cb-version                                                                        | `string`  |                                                             |       `All`       |                                      | When you need to use Scrapingbypass v2, the request header value should be `2`.                                                                                                                                                                                |
| [x-cb-part](/us-en/request_parameters?id=X-Cb-Part)                                 | `integer` |                              0                              |       `v2`        |                                      | This request header is valid only in Scrapingbypass v2 and is used to distinguish different sessions. A user can have up to 1000 session partitions (0 to 999).                                                                                                |
| [x-cb-origin](/us-en/request_parameters?id=about-the-browser-cross-domain-problem)  | `string`  |                                                             |       `All`       |                                      | Replace the origin field in the request header, generally used for browser cross-domain requests to bypass CORS restrictions.                                                                                                                                  |
| [x-cb-referer](/us-en/request_parameters?id=about-the-browser-cross-domain-problem) | `string`  |                                                             |       `All`       |                                      | Replace the referer field in the request header, generally used for browser cross-domain requests to bypass CORS restrictions.                                                                                                                                 |
| x-cb-cookie                                                                         | `string`  |                                                             |       `All`       |                                      | Replace the cookie field in the request header, generally used for browser cross-domain requests to bypass CORS restrictions.                                                                                                                                  |
| [x-cb-sitekey](/us-en/request_parameters?id=how-to-get-sitekey)                     | `string`  |                                                             |       `v2`        |                                      | After filling in, the `Turnstile` widget verification will be triggered. Set the cf_token value to [cf_token] in the request data, and the verification result will automatically replace the request after filling in.                                        |
| [x-cb-options](/us-en/request_parameters?id=options-list)                           | `string`  |                                                             |       `All`       |                                      | Configuration option list, you can fill in multiple additional configuration options, separated by commas. For details, please see [Options list](/us-en/request_parameters?id=options-list).                                                                  |

### Options list

`x-cb-options` request header configuration option list:

| PARAMETER                                                                | TYPE  | DESCRIPTION                                                                                                                                                                                                                                         |
|--------------------------------------------------------------------------|:-----:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| disable-redirect                                                         | `All` | Disable redirection. When the server encounters a response code of 300~399, it will return, and Set-Cookie will return the complete content. (Redirection is automatically processed by default, SDK default configuration).                        |
| long-timeout                                                             | `v2`  | Delay timeout. The default timeout is 15 seconds. If the target server responds slowly, you can set this parameter to delay it to 60 seconds.                                                                                                       |
| force                                                                    | `v2`  | Normally, you cannot change the proxy during a Scrapingbypass V2 session, and will return a [`BYPASS_ERROR`](/us-en/response_data?id=error-code) error. Use the `force` configuration to force a proxy change.                                      |
| [ignore-lock](/us-en/request_parameters?id=about-v2-concurrent-requests) | `v2`  | Use the ignore challenge lock configuration to directly ignore the verification challenge lock when two or more requests use the same session at the same time, which can prevent **CHALLENGE_LOCK_TIMEOUT** or **CHALLENGE_LOCK_OCCUPIED** errors. |
| [wait-lock](/us-en/request_parameters?id=about-v2-concurrent-requests)   | `v2`  | Use the wait-challenge lock configuration to prevent [CHALLENGE_LOCK_TIMEOUT](/us-en/response_data?id=error-code) errors when two or more requests use the same session at the same time. (Higher priority than ignore-lock)                        |

### APIKEY

`APIKEY` is a unique Scrapingbypass API request authorization access key for each account and is one of the necessary
parameters for accessing the Scrapingbypass API.

?> If the `APIKEY` is leaked, you can visit the [Scrapingbypass API Console](https://console.scrapingbypass.com/#/api/)
to
reset it.

Visit https://opensea.io/category/memberships and request an example:


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

`X-Cb-Host` and `X-Cb-Protocol` are also required parameters to access the Scrapingbypass API.
`X-Cb-Protocol` defaults to https, so it generally does not need to be set.

?> Replace the protocol, host domain name (or IP), and port number in the original request URL with the Scrapingbypass
API address (`https://api.scrapingbypass.com`), and fill in the replaced host domain name in `X-Cb-Host`.
The following is an HTTP example:

```http request
# Original request
GET https://example.io/user/login.html

# Modified request
GET https://api.scrapingbypass.com/user/login.html
X-Cb-Apikey: <APIKEY>
X-Cb-Host: example.io
```

##### If the original request is HTTP protocol：

```http request
# Original request
GET http://example.io/user/login.html

# Modified request
GET https://api.scrapingbypass.com/user/login.html
X-Cb-Apikey: <APIKEY>
X-Cb-Host: example.io
X-Cb-Protocol: http
```

### X-Cb-Proxy

Client-defined proxy, supports HTTP and Socks5 protocols

Supported formats are as follows

* Username: Password@Hostname:Port (Default http protocol)
* Username: Password:Hostname:Port (Default http protocol)
* Protocol://Username: Password@Hostname:Port
* Protocol://Username: Password:Hostname:Port
* Protocol:Username: Password:Hostname:Port

### X-Cb-Fp

Set the browser fingerprint used when making requests. The following is a list of supported browsers.

* Scrapingbypass V1 (default `chrome`)
    * `chrome`
    * `firefox`
    * `edge`
* Scrapingbypass V2 (default `edge128-linux`)
    * `chrome`、`chrome-linux`、`chrome-mac`、`chrome127`、`chrome127-linux`、`chrome127-mac`、`chrome128`、`chrome128-linux`、`chrome128-mac`
    * `edge`、`edge-linux`、`edge-mac`、`edge127`、`edge127-linux`、`edge127-mac`、`edge128`、`edge128-linux`、`edge128-mac`
    * `chrome-android`、`edge-android`、`chrome127-android`、`edge127-android`、`chrome128-android`、`edge128-android`

### X-Cb-Part

Scrapingbypass V2 uses session hosting mode. All cookies responded by cloudflare will be stored on the Scrapingbypass
server. Users can switch sessions by setting the `X-Cb-Part` request header.
Once the verification is successful, the cloudflare cookie will be retained for 10 minutes and renewed if another
request is successful within 10 minutes.

?> The proxy cannot be changed during the session. If there is a business requirement, you can
configure `x-cb-options: force` to force the change. (Not recommended)

### Request using Scrapingbypass V2

Scrapingbypass API V2 is suitable for websites that need to pass the `JS challenge` verification. For example,
visit `https://etherscan.io/accounts/label/lido` and request an example:

<!-- tabs:start -->

#### **cURL**

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

#### **Python**

```Python
import requests

url = "https://api.scrapingbypass.com/accounts/label/lido"

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

	resp, err := client.R().Get("https://api.scrapingbypass.com/accounts/label/lido")

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

const url = "https://api.scrapingbypass.com/accounts/label/lido";
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
        String url = "https://api.scrapingbypass.com/accounts/label/lido";
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

### About V2 concurrent requests

When encountering verification, it will be locked according to `"{host}_{part}"` and released after the verification is
completed. Therefore, by default, no request can be made when `"{host}_{part}"` is locked.

?> It is recommended that in case of multi-threaded requests, each thread use a separate `part` to initiate a request,
which can avoid various problems in the following modes. In this way, the reasonable use of `part` can avoid more
verification and reduce the consumption of points, traffic, and time. (Multi-threaded recommendation)

* `default` By default, when encountering a verification lock,
  a [`CHALLENGE_LOCK_OCCUPIED`](/us-en/response_data?id=error-code) error will be returned, which means that a request
  with
  the same `"{host}_{part}"` is being verified.
* `ignore-lock` ignores the verification lock, which is set via the request header `x-cb-options: ignore-lock`.
    * Advantages: All locking errors can be avoided.
    * Disadvantages: consumes more points, traffic, and time.
* `wait-lock` waits for the verification lock, which is set by the request header `x-cb-options: wait-lock`.
    * Advantages: It can avoid the [`CHALLENGE_LOCK_OCCUPIED`](/us-en/response_data?id=error-code) error, and the new
      cookie will be used directly to complete the request after the verification is passed.
    * Disadvantage: If you wait too long, a [`CHALLENGE_LOCK_TIMEOUT`](/us-en/response_data?id=error-code) error may
      occur.

### About the browser cross-domain problem

> Understand: Browser cross-domain refers to the problem that documents or scripts from different sources cannot
> interact with each other due to the browser's same-origin policy restrictions.
> The same-origin policy is a security mechanism that requires the protocol, domain name, and port to be the same to be
> considered the same origin. This is to prevent malicious websites from reading or manipulating data from other
> websites.
> Cross-origin resource sharing (CORS) is a technology that solves cross-origin issues by allowing browsers to send HTTP
> requests to servers at different origins.

Generally, when requesting an interface, browsers will automatically add request headers such as `origin` and `referer`
that cannot be controlled by the site.These request headers will also be forwarded to the target server after reaching
the Scrapingbypass API, causing the request to fail. Therefore, by configuring `x-cb-origin` and `x-cb-referer`, some
cross-domain related request headers can be overwritten.

### How to get sitekey

Here `sitekey` refers to the main parameter of calling the `turnstile` component. Each site has a
separate `turnstile sitekey`.

?> Note: `JS challenge` does not require sitekey

1. Open the browser Developer Tools (Ctrl+Shift+I or F12)
2. Click the Network tab and make sure the Network Log button is as shown<br />
   ![devtools_network.png](img%2Fdevtools_network.png)
3. Visit a page with a `turnstile` widget
4. Enter `https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/b/turnstile/` on the filter
5. As shown in the figure, the selected content is `sitekey` <br />
   ![devtools_network1.png](img%2Fdevtools_network1.png)
