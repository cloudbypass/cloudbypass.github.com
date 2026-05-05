# 查询账户余额

您可以通过[登录控制台](https://console.cloudbypass.com/#/api/)查看账户与用量，也可通过 HTTP API 或各语言 SDK 查询。

### 通过 HTTP API

当前约定为 **POST** `https://console.cloudbypass.com/api/v1/balance`，请求头 `Content-Type: application/json`，请求体为 JSON 字段 `apikey`、`email`、`type`。

**`type` 与返回（HTTP 200 时）：**

| `type` | 含义 | 响应体 |
|--------|------|--------|
| `points` | 账户**积分** | `{"balance": <number>}` |
| `res` | **住宅代理**用户流量 | `{"total": <bytes>, "balance": <bytes>}`，流量字段为**字节** |
| `dat` | **机房代理**用户流量 | 同上 |

```shell
# 查询积分
curl -s -X POST "https://console.cloudbypass.com/api/v1/balance" \
  -H "Content-Type: application/json" \
  -d '{"apikey":"<APIKEY>","email":"<EMAIL>","type":"points"}'

# 查询住宅流量（机房将 type 改为 dat）
curl -s -X POST "https://console.cloudbypass.com/api/v1/balance" \
  -H "Content-Type: application/json" \
  -d '{"apikey":"<APIKEY>","email":"<EMAIL>","type":"res"}'
```

**GET 接口已废弃**

原先使用 **GET** 并在 URL 中附带 `?apikey=<APIKEY>&email=<email>` 的用法**已废弃**，不再推荐使用；请改用 **POST + JSON body**（含 `type`）。若仍在使用 GET，请尽快迁移，以免影响后续调用。

### 通过 SDK

* [Python](/zh-cn/python_sdk?id=查询余额)
* [Nodejs](/zh-cn/nodejs_sdk?id=查询余额)
* [Go](/zh-cn/golang_sdk?id=查询余额)

更完整的字段说明与流量字节格式化（SDK 辅助函数）见主仓库 **`docs/console-balance-api.md`**。
