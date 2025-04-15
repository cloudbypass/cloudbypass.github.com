# 响应数据

> 不同的穿云API版本，响应标头和响应正文以及错误消息可能会有所不同。

穿云API响应数据与目标服务器响应数据同步。如遇到请求失败，则响应状态码根据错误类型进行设置。

### 响应头

穿云API将对以下响应头进行处理：

* `content-length` `content-encoding` 响应体正文可能会压缩，因此这些字段会有变化。
* `date` `connection` `transfer-encoding` `datekeep-alive` `server` `vary` 被移除。
* `access-control-allow-origin` `access-control-allow-credentials` `access-control-allow-headers` `access-control-allow-method`
  被设置为*。
* `set-cookie` V2则会过滤掉cloudflare相关的Cookie。

以下是穿云服务的响应头字段：

| 参数          |  支持版本  |   类型   | 描述                                                      |
|-------------|:------:|:------:|---------------------------------------------------------|
| x-cb-status | `所有版本` | string | 响应状态，返回`ok`代表请求处理成功，为空时代表请求处理失败。<br />返回`ok`时将会扣除相应的积分。 |

### 响应体

如果响应头`x-cb-status`为`ok`，则响应体将直接返回所有正文数据。

穿云服务响应的正文数据会根据请求头中的`Accept-Encoding`字段进行压缩。目前支持`gzip`、`deflate`、`br`等压缩方式。

出现错误时，穿云服务响应的正文数据会根据错误类型进行解析，响应体则是JSON格式的[错误信息](/zh-cn/response_data?id=错误信息)。

?> 穿云SDK会自动处理响应错误并抛出异常，使用`HTTP API`则需要自行判断响应状态。

### 错误信息

错误信息是一条JSON格式的数据，包含以下字段：

* `id` 请求唯一标识，可用于管理员排查问题。
* `code` [错误代码](/zh-cn/response_data?id=错误代码)，用于标识错误类型。
* `message` 错误信息，描述错误详细原因。

```json
{
  "id": "xxxxxx-xxxxxxx-xxxxxxx-xxxxxxxxx",
  "code": "PARAM_ERROR",
  "message": "xxxxxxxxxxxxxxxxxxxxx"
}
```

### 错误代码

| 代码                           | 支持版本   | 描述                                                                                                                                                                                                                                                                                                             |
|------------------------------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PARAM_ERROR                  | `所有版本` | 参数错误，可能是请求参数不正确或者缺少必填参数。<br />具体错误需要查看错误信息。                                                                                                                                                                                                                                                                    |
| APIKEY_INVALID               | `所有版本` | 可能是您的[apikey](/zh-cn/parameters?id=APIKEY)不存在或者已被禁用。                                                                                                                                                                                                                                                           |
| INSUFFICIENT_BALANCE         | `所有版本` | 账户余额不足。                                                                                                                                                                                                                                                                                                        |
| HOSTNAME_IS_FORBIDDEN        | `所有版本` | 请求的接口地址被禁止访问。                                                                                                                                                                                                                                                                                                  |
| HOSTNAME_IS_NULL             | `所有版本` | 请求头参数[x-cb-host](/zh-cn/parameters?id=x-cb-host、x-cb-protocol)不能为空。                                                                                                                                                                                                                                            |
| PROXY_ERROR                  | `所有版本` | 代理服务器无法连接或者返回了错误的响应。                                                                                                                                                                                                                                                                                           |
| PROXY_FORMAT_ERROR           | `所有版本` | 代理格式错误，仅支持HTTP/HTTPS代理协议。[参考代理格式](/zh-cn/parameters?id=X-Cb-Proxy)                                                                                                                                                                                                                                             |
| PROXY_IS_FORBIDDEN           | `所有版本` | 代理被禁止，请求的代理地址被禁止访问。                                                                                                                                                                                                                                                                                            |
| CONNECTION_ERROR             | `所有版本` | 连接错误，可能是代理服务器无法连接或者代理服务器返回了错误的响应。                                                                                                                                                                                                                                                                              |
| DNS_ERROR                    | `所有版本` | DNS解析失败或者DNS解析超时。                                                                                                                                                                                                                                                                                              |
| TLS_ERROR                    | `所有版本` | TLS客户端连接错误，请检查请求的地址或代理服务器地址是否正确。                                                                                                                                                                                                                                                                               |
| UNSUPPORTED_CAPTCHA          | `所有版本` | 请求网站地址的验证类型可能不被支持。                                                                                                                                                                                                                                                                                             |
| CERT_ERROR                   | `所有版本` | 证书错误，可能是证书解析失败或者证书解析超时。                                                                                                                                                                                                                                                                                        |
| REQUEST_ERROR                | `所有版本` | 请求错误，可能是请求超时或者请求被拒绝。                                                                                                                                                                                                                                                                                           |
| EOF_ERROR                    | `所有版本` | EOF错误，请检查请求的地址或代理服务器地址是否正确。                                                                                                                                                                                                                                                                                    |
| CLOUDFLARE_PREMIUM           | `v1`   | 受Cloudflare五秒盾保护，尝试[穿云V2](/zh-cn/request_parameters?id=使用穿云v2进行请求)请求。                                                                                                                                                                                                                                          |
| CLOUDFLARE_CHALLENGE_TIMEOUT | `v2`   | 挑战Cloudflare验证超时。                                                                                                                                                                                                                                                                                              |
| CHALLENGE_LOCK_TIMEOUT       | `v2`   | 在使用V2等待锁策略下可能遇到的超时错误。                                                                                                                                                                                                                                                                                          |
| CHALLENGE_LOCK_OCCUPIED      | `v2`   | 在使用V2默认策略下可能遇到的锁被占用的问题。                                                                                                                                                                                                                                                                                        |
| BYPASS_ERROR                 | `v2`   | 挑战预设错误，需要检查请求参数是否合理。                                                                                                                                                                                                                                                                                           |
| FORBIDDEN                    | `所有版本` | 受到目标网站限制访问，详细内容参考响应消息。                                                                                                                                                                                                                                                                                         |
| ACCESS_DENIED                | `所有版本` | 您的请求被Cloudflare拦截，<br/>请参考：<a rel="nofollow noreferrer" href="https://developers.cloudflare.com/support/troubleshooting/cloudflare-errors/troubleshooting-cloudflare-1xxx-errors/#errors-1009-access-denied-country-or-region-banned" target="_blank">Cloudflare文档</a><br />建议更换被允许访问的IP。                      |
| TOO_MANY_REQUESTS            | `所有版本` | 请求因“Too many requests”被Cloudflare拦截，<br/>请参考：<a rel="nofollow noreferrer" href="https://developers.cloudflare.com/support/troubleshooting/http-status-codes/4xx-client-error/#429-too-many-requests-rfc6585httpstoolsietforghtmlrfc6585" target="_blank">Cloudflare文档</a><br />建议更换您的IP或者账号。                   |
| BAD_GATEWAY                  | `所有版本` | 网关错误，可能是由于Cloudflare无法连接到源服务器造成的，<br/>请参考：<a rel="nofollow noreferrer" href="https://developers.cloudflare.com/support/troubleshooting/cloudflare-errors/troubleshooting-cloudflare-5xx-errors/#error-502-bad-gateway-or-error-504-gateway-timeout" target="_blank">Cloudflare文档</a><br />建议稍后重试或更换其它地区IP进行访问。 |
| SERVICE_UNAVAILABLE          | `所有版本` | 服务暂时不可用，可能源服务器过载，<br/>请参考：<a rel="nofollow noreferrer" href="https://developers.cloudflare.com/support/troubleshooting/cloudflare-errors/troubleshooting-cloudflare-5xx-errors/#error-503-service-temporarily-unavailable" target="_blank">Cloudflare文档</a><br />建议稍后重试或更换其它地区IP进行访问。                          |
| SOURCE_SERVER_ERROR          | `所有版本` | 该错误是由于源服务器错误导致的，<br/>请参考：<a rel="nofollow noreferrer" href="https://developers.cloudflare.com/support/troubleshooting/cloudflare-errors/troubleshooting-cloudflare-5xx-errors" target="_blank">Cloudflare文档</a><br />                                                                                          |
| BAD_GATEWAY                  | `所有版本` | 网关错误，可能是由于Cloudflare无法连接到源服务器造成的，<br/>请参考：<a rel="nofollow noreferrer" href="https://developers.cloudflare.com/support/troubleshooting/cloudflare-errors/troubleshooting-cloudflare-5xx-errors/#error-502-bad-gateway-or-error-504-gateway-timeout" target="_blank">Cloudflare文档</a><br />建议更换被允许访问的IP。        |
| INTERNAL_ERROR               | `所有版本` | 内部错误，我们在收到错误消息后会尽快修复。                                                                                                                                                                                                                                                                                          |

### 问题反馈

* [访问论坛](https://www.cloudbypass.com/blog/)
* [联系客服](https://t.me/cloudbypasscom)