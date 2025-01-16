# Golang SDK

> Inherits [go-resty/resty#supported-go-versions](https://github.com/go-resty/resty#supported-go-versions) v2 Supported
> Go versions

[![GoDoc](https://godoc.org/github.com/cloudbypass/golang-sdk?status.svg)](https://godoc.org/github.com/cloudbypass/golang-sdk ":no-zoom")
[![Go Report Card](https://goreportcard.com/badge/github.com/cloudbypass/golang-sdk)](https://goreportcard.com/report/github.com/cloudbypass/golang-sdk ":no-zoom")

The Cloud SDK encapsulated based on `go-resty/resty.v2`.

[![npm version](https://img.shields.io/npm/v/cloudbypass-sdk.svg?style=flat-square)](https://www.npmjs.org/package/cloudbypass-sdk ":no-zoom")
[![install size](https://img.shields.io/badge/dynamic/json?url=https://packagephobia.com/v2/api.json?p=cloudbypass-sdk&query=$.install.pretty&label=install%20size&style=flat-square)](https://packagephobia.now.sh/result?p=cloudbypass-sdk ":no-zoom")
[![npm bundle size](https://img.shields.io/bundlephobia/minzip/cloudbypass-sdk?style=flat-square)](https://bundlephobia.com/package/cloudbypass-sdk@latest ":no-zoom")

### Install

```bash
// Go Modules
require github.com/cloudbypass/golang-sdk latest
```

### Usage

```go
// Import package cloudbypass
import cloudbypass "github.com/cloudbypass/golang-sdk"
```

### Make a Request

Create a new `resty.Client` instance using `cloudbypass.New()`.

Added initialization parameters `apikey` and `proxy` to set the Scrapingbypass API service key and proxy IP
respectively.

Custom users can specify the service address by setting the `api_host` parameter.

> The above parameters can be configured using the environment variables `CB_APIKEY`, `CB_PROXY`, and `CB_APIHOST`.

```go
package main

import (
	"fmt"
	cloudbypass "github.com/cloudbypass/golang-sdk"
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

### Using V2

Scrapingbypass API V2 is suitable for websites that need to pass JS challenge verification. For example,
visit https://etherscan.io/accounts/label/lido and request an example:

```go
package main

import (
	"fmt"
	cloudbypass "github.com/cloudbypass/golang-sdk"
)

func main() {
	// Cookie mode: The server returns an encrypted cookie, which is sent by the client for authentication in the next request.
	client := cloudbypass.New(cloudbypass.BypassConfig{
		Apikey: "/* APIKEY */",
		Proxy:  "/* PROXY */",
		UseV2:  true,
	})

	resp, err := client.R().
		EnableTrace().
		Get("https://etherscan.io/accounts/label/lido")

	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println(resp.StatusCode(), resp.Header().Get("X-Cb-Status"))
	fmt.Println(resp.Header().Get("set-cookie"))
	fmt.Println(resp.String())
}

```

```go
package main

import (
	"fmt"
	cloudbypass "github.com/cloudbypass/golang-sdk"
)

func main() {
	// Part mode: The server manages the authentication cookie, and the client only needs to control the part parameter.
	client := cloudbypass.New(cloudbypass.BypassConfig{
		Apikey: "/* APIKEY */",
		Proxy:  "/* PROXY */",
		Part:   "0",
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

### Check balance

Use the `GetBalance` method to query the current account balance.

```go
package main

import (
	"fmt"
	cloudbypass "github.com/cloudbypass/golang-sdk"
)

func main() {
	balance, err := cloudbypass.GetBalance( /* APIKEY */)

	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("Balance:", balance)
}

```

### Extraction Proxy

Create a CloudPiercing proxy instance through the `NewProxy` method, which can extract the CloudPiercing dynamic proxy
IP and time-sensitive proxy IP.

+ `Copy()` Duplicate the proxy instance so that the original proxy instance is not affected.
+ `SetDynamic()` Set as dynamic proxy.
+ `SetExpire(expire int)` Set to time-limited proxy, the parameter is the IP expiration time, in seconds.
+ `SetRegion(region string)` Set the proxy IP region.
+ `String()` Returns the proxy IP string.
+ `StringFormat(format string)` Format proxy IP. The parameter is a formatted string, for
  example, `username:password@gateway`.
+ `SetFormat(format string)` Set the proxy IP format string.
+ `Iterate(count int)` Returns an iterator of proxy IP instances, with the parameter being the number of extractions.
+ `Loop(count int)` Returns a proxy IP instance loop iterator, with the parameter being the actual number.

```go
package main

import (
	"fmt"
	cloudbypass "github.com/cloudbypass/golang-sdk"
)

func main() {
	proxy, err := cloudbypass.NewProxy("username-res:password")

	if err != nil {
		fmt.Println(err)
		return
	}

	// Extracting dynamic proxies
	fmt.Println("Extract dynamic proxy: ")
	fmt.Println(proxy.SetDynamic().String())
	fmt.Println(proxy.SetRegion("US").String())

	// Extract time agent and specify region
	fmt.Println("Extract proxy with expire and region: ")
	fmt.Println(proxy.SetExpire(60 * 10).SetRegion("US").String())

	// Batch Extraction
	fmt.Println("Extract five 10-minute aging proxies: ")
	iterator := proxy.SetExpire(60 * 10).SetRegion("US").SetFormat("username:password:gateway").Iterate(10)
	for iterator.HasNext() {
		fmt.Println(iterator.Next())
	}

	// Cycle Extraction
	fmt.Println("Loop two 10-minute aging proxies: ")
	loop := proxy.SetExpire(60 * 10).SetRegion("US").Loop(2)
	for i := 0; i < 10; i++ {
		fmt.Println(loop.Next())
	}
}
```

### About redirection issues

When using the SDK to initiate a request, the redirection operation is automatically handled without manual processing.
The redirection response will also consume credits.