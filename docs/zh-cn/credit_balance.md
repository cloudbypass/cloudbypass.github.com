# 查询账户余额

您可以通过[登录控制台](https://console.cloudbypass.com/#/api/)查看账户与用量，也可通过 HTTP API 或各语言 SDK 查询。

### 通过 HTTP API

当前约定为 **POST** `https://console.cloudbypass.com/api/v1/balance`，请求头 `Content-Type: application/json`，请求体为 JSON 字段 `apikey`、`email`、`type`。

**`type` 与返回（HTTP 200 时）：**

| `type` | 含义 | 响应体 |
|--------|------|--------|
| `points` | 账户**积分** | 见下方「积分响应字段」 |
| `res` | **住宅代理**用户流量 | `{"total": <bytes>, "balance": <bytes>}`，流量字段为**字节** |
| `dat` | **机房代理**用户流量 | 同上 |

**积分响应字段（`type=points`）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `balance` | number | 当前可用积分余额 |
| `expires_at_min` | number \| null | 有效积分中**最早**到期时间（Unix 时间戳，秒）；无到期时间时为 `null` |
| `expires_at_max` | number \| null | 有效积分中**最晚**到期时间（Unix 时间戳，秒）；无到期时间时为 `null` |

```json
{
  "balance": 9999816,
  "expires_at_min": 1725408000,
  "expires_at_max": 1728000000
}
```

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

**GET 接口已废弃**：原先使用 **GET** 并在 URL 中附带 `?apikey=<APIKEY>&email=<email>` 的用法**已废弃**，不再推荐使用；请改用 **POST + JSON body**（含 `type`）。若仍在使用 GET，请尽快迁移，以免影响后续调用。

### 通过 SDK

* [Python](/zh-cn/python_sdk?id=查询余额)
* [Nodejs](/zh-cn/nodejs_sdk?id=查询余额)
* [Go](/zh-cn/golang_sdk?id=查询余额)
