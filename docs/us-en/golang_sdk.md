# Golang SDK

### Getting Started

> Supports Go versions listed under [go-resty/resty#supported-go-versions](https://github.com/go-resty/resty#supported-go-versions).

[![GoDoc](https://godoc.org/github.com/cloudbypass/golang-sdk?status.svg)](https://godoc.org/github.com/cloudbypass/golang-sdk ":no-zoom")
[![Go Report Card](https://goreportcard.com/badge/github.com/cloudbypass/golang-sdk)](https://goreportcard.com/report/github.com/cloudbypass/golang-sdk ":no-zoom")

Built on `go-resty/resty/v2`.

### Installation

```bash
// Go Modules
require github.com/cloudbypass/golang-sdk latest
```

### Usage

```go
import cloudbypass "github.com/cloudbypass/golang-sdk"
```

### Making Requests

Create a client with `cloudbypass.New()`. Use `BypassConfig` fields `Apikey`, `Proxy`, `ApiHost`, etc.

> Configure via `CB_APIKEY`, `CB_PROXY`, and `CB_APIHOST` when needed.

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

For JS challenges, e.g. https://etherscan.io/accounts/label/lido :

```go
package main

import (
	"fmt"
	cloudbypass "github.com/cloudbypass/golang-sdk"
)

func main() {
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

`GetBalance` calls `POST https://console.cloudbypass.com/api/v1/balance` with JSON. Third argument is `type`: `BalanceTypePoints` (default when empty), `BalanceTypeRes`, `BalanceTypeDat`. Returns `*BalanceResult`; traffic responses include `Total` and `Balance` in bytes.

`ConvertBytes` formats bytes for display, e.g. with `Balance`.

```go
package main

import (
	"fmt"
	cloudbypass "github.com/cloudbypass/golang-sdk"
)

func main() {
	points, err := cloudbypass.GetBalance("/* APIKEY */", "/* EMAIL */", cloudbypass.BalanceTypePoints)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println("points balance:", points.Balance)

	res, err := cloudbypass.GetBalance("/* APIKEY */", "/* EMAIL */", cloudbypass.BalanceTypeRes)
	if err != nil {
		fmt.Println(err)
		return
	}
	s, _ := cloudbypass.ConvertBytes(res.Balance, "G")
	fmt.Println("res total / balance bytes:", res.Total, res.Balance, s)
}

```

### Extracting proxies

Use `NewProxy` to create a proxy extractor instance.

+ `Copy`, `SetDynamic`, `SetExpire`, `SetRegion`, `String`, `StringFormat`, `SetFormat`, `Iterate`, `Loop` — same behavior as README.

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

	fmt.Println("Extract dynamic proxy: ")
	fmt.Println(proxy.SetDynamic().String())
	fmt.Println(proxy.SetRegion("US").String())

	fmt.Println("Extract proxy with expire and region: ")
	fmt.Println(proxy.SetExpire(60 * 10).SetRegion("US").String())

	fmt.Println("Extract five 10-minute aging proxies: ")
	iterator := proxy.SetExpire(60 * 10).SetRegion("US").SetFormat("username:password:gateway").Iterate(10)
	for iterator.HasNext() {
		fmt.Println(iterator.Next())
	}

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