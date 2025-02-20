# Golang SDK

> 继承 [go-resty/resty#supported-go-versions](https://github.com/go-resty/resty#supported-go-versions) v2支持的Go版本


[![GoDoc](https://godoc.org/github.com/cloudbypass/golang-sdk?status.svg)](https://godoc.org/github.com/cloudbypass/golang-sdk ":no-zoom")
[![Go Report Card](https://goreportcard.com/badge/github.com/cloudbypass/golang-sdk)](https://goreportcard.com/report/github.com/cloudbypass/golang-sdk ":no-zoom")

在`go-resty/resty.v2`基础上封装的穿云SDK。

[![npm version](https://img.shields.io/npm/v/cloudbypass-sdk.svg?style=flat-square)](https://www.npmjs.org/package/cloudbypass-sdk ":no-zoom")
[![install size](https://img.shields.io/badge/dynamic/json?url=https://packagephobia.com/v2/api.json?p=cloudbypass-sdk&query=$.install.pretty&label=install%20size&style=flat-square)](https://packagephobia.now.sh/result?p=cloudbypass-sdk ":no-zoom")
[![npm bundle size](https://img.shields.io/bundlephobia/minzip/cloudbypass-sdk?style=flat-square)](https://bundlephobia.com/package/cloudbypass-sdk@latest ":no-zoom")

### 安装

```bash
// Go Modules
require github.com/cloudbypass/golang-sdk latest
```

### 用法

```go
// Import package cloudbypass
import cloudbypass "github.com/cloudbypass/golang-sdk"
```

### 发起请求

使用 `cloudbypass.New()` 创建一个新的 `resty.Client` 实例。

增加初始化参数`apikey`和`proxy`，分别用于设置穿云API服务密钥和代理IP。

定制用户可以通过设置`api_host`参数来指定服务地址。

> 以上参数可使用环境变量`CB_APIKEY`、`CB_PROXY`和`CB_APIHOST`进行配置。

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

### 使用V2

穿云API V2适用于需要通过JS质询验证的网站。例如访问https://etherscan.io/accounts/label/lido ，请求示例：

```go
package main

import (
	"fmt"
	cloudbypass "github.com/cloudbypass/golang-sdk"
)

func main() {
	// Cookie模式：服务端返回加密Cookie，下次请求时由客户端发送验证Cookie
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
	// Part模式：由服务端管理验证Cookie，客户端只需要控制part参数
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

### 查询余额

使用`GetBalance`方法可以查询当前账户余额。

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

### 提取代理

通过`NewProxy`方法创建穿云代理实例，该实例可提取穿云动态代理IP和时效代理IP。

+ `Copy()` 复制代理实例，使原有代理实例不受影响。
+ `SetDynamic()` 设置为动态代理。
+ `SetExpire(expire int)` 设置为时效代理，参数为IP过期时间，单位为秒。
+ `SetRegion(region string)` 设置代理IP地区。
+ `String()` 返回代理IP字符串。
+ `StringFormat(format string)` 格式化代理IP，参数为格式化字符串，例如`username:password@gateway`。
+ `SetFormat(format string)` 设置代理IP格式化字符串。
+ `Iterate(count int)` 返回一个代理IP实例迭代器，参数为提取数量。
+ `Loop(count int)` 返回一个代理IP实例循环迭代器，参数为实际数量。

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

	// 提取动态代理
	fmt.Println("Extract dynamic proxy: ")
	fmt.Println(proxy.SetDynamic().String())
	fmt.Println(proxy.SetRegion("US").String())

	// 提取时效代理并指定地区
	fmt.Println("Extract proxy with expire and region: ")
	fmt.Println(proxy.SetExpire(60 * 10).SetRegion("US").String())

	// 批量提取
	fmt.Println("Extract five 10-minute aging proxies: ")
	iterator := proxy.SetExpire(60 * 10).SetRegion("US").SetFormat("username:password:gateway").Iterate(10)
	for iterator.HasNext() {
		fmt.Println(iterator.Next())
	}

	// 循环提取
	fmt.Println("Loop two 10-minute aging proxies: ")
	loop := proxy.SetExpire(60 * 10).SetRegion("US").Loop(2)
	for i := 0; i < 10; i++ {
		fmt.Println(loop.Next())
	}
}
```

### 关于重定向问题

使用SDK发起请求时，重定向操作会自动处理，无需手动处理。且重定向响应也会消耗积分。