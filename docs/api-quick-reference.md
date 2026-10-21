# API Quick Reference

访问受 Cloudflare 保护站点时，通过穿云 API 转发请求，无需插件。文档：https://github.com/cloudbypass/cloudbypass.github.com

---

## 何时用

- 程序请求 403、浏览器能打开 → 先用 **V1**；若 V1 失败或返回需挑战（如五秒盾）则改用 **V2**。
- 已知为 JS 质询 / Turnstile / DataDome 验证 → 直接用 **V2**（须提供 `x-cb-proxy`；DataDome 特征为 `403` + `x-datadome-cid` + `x-dd-b`）。
- 需要 **stream 流式响应**（如大文件下载）→ 使用 **V2s**（`x-cb-version: 2s`，与 V2 一致）。
- 用户明确要求用 V1、V2 或 V2s 时，按用户要求。

---

## 请求规则

**URL**：原请求的「协议+主机」换成 `https://api.cloudbypass.com`，**路径和查询串不变**。  
例：`https://example.com/path?q=1` → `https://api.cloudbypass.com/path?q=1`

**必填头**：`x-cb-apikey`（密钥，控制台 https://console.cloudbypass.com/#/ 获取）、`x-cb-host`（目标主机，如 `example.com`，不含协议与路径）。

**可选头**：`x-cb-protocol` 默认 https，http 目标填 `http`；V2 时 `x-cb-version: 2`、`x-cb-proxy`（必填）、`x-cb-part`（会话分区）、`x-cb-sitekey`（Turnstile 用）；**穿云 V2s** 使用 `x-cb-version: 2s`，与 V2 一致但支持 **stream 流式响应**（适合大文件/下载）；`x-cb-fp` 客户端指纹，默认 `edge155-win`（未写版本号的 `chrome`/`edge` 用主版本 `152`）；`x-cb-ua` 自定义 User-Agent（**优先于** `x-cb-fp`；Go V1 / Go V2 / V2s 生效，当前 Python V2 不读取）；`x-cb-timeout` 为请求超时秒数（整数，v1/v2s 范围 5–3600、默认 30，v2 范围 5–360、默认 15），优先级高于 `x-cb-options` 中的 ~~`long-timeout`~~（可能后续废弃）；`x-cb-options` 可填 ~~`long-timeout`~~、`force`、`ignore-lock` 等逗号分隔。所有 `x-cb-*` 头不会转发到目标站。请求头 `User-Agent` 会被过滤，请用 `x-cb-ua` 指定。

**方法 / Body / 其它头**：与原请求一致。

---

## 参数边界与默认值

- 默认指纹为 `edge155-win`；省略版本号的 `chrome` / `edge` 仍使用 `152`。服务端可分别通过 `ELECTRON_API_FP`、`ELECTRON_API_FP_CHROMIUM_VERSION` 覆盖，部署值可能不同。
- V2 / V2s 的 `x-cb-part` 默认接受 `0–998`（999 个分区），实际要求 `0 ≤ part < V2_PART_MAX`，以服务端配置为准。
- Turnstile 须同时设置 `x-cb-sitekey`，并在 URL、请求头或请求体中包含 `[cf_token]` 或 `%5Bcf_token%5D`；仅填写 sitekey 不会触发 Token 求解。可选 `x-cb-action`、`x-cb-cdata` 分别传递 action、cData。
- Go V1 / V2s 忽略非整数或超出 5–3600 的 `x-cb-timeout`；Python V2 对非整数或超出 5–360 的值返回 HTTP 400 / `PARAMS_ERROR`。`long-timeout` 在 Go V1 / V2s 和 Python V2 均将超时设为 60 秒，有效的 `x-cb-timeout` 优先。
- `x-cb-cookie` 与原 Cookie 合并，同名项以 `x-cb-cookie` 为准，其余保留。

## 成功与失败

- **成功**：响应头 `x-cb-status` 为 `ok`，响应体即目标站内容。
- **失败**：`x-cb-status` 非 `ok` 时，响应体为 JSON：`{"id","code","message"}`。常见 code：`PARAMS_ERROR`、`USER_AGENT_INVALID`、`APIKEY_INVALID`、`INSUFFICIENT_BALANCE`、`PROXY_ERROR`、`CLOUDFLARE_CHALLENGE_TIMEOUT`、`CHALLENGE_LOCK_OCCUPIED`、`BYPASS_ERROR`、`FORBIDDEN`、`TOO_MANY_REQUESTS`。

---

## 示例

**V1：**
```bash
curl -X GET "https://api.cloudbypass.com/category/memberships" \
  -H "x-cb-apikey: YOUR_APIKEY" -H "x-cb-host: opensea.io"
```

**V2（需代理）：**
```bash
curl -X GET "https://api.cloudbypass.com/accounts/label/lido" \
  -H "x-cb-apikey: YOUR_APIKEY" -H "x-cb-host: etherscan.io" \
  -H "x-cb-version: 2" -H "x-cb-part: 0" -H "x-cb-proxy: http://proxy:port"
```

---

## 操作步骤

1. URL 改为 `https://api.cloudbypass.com` + 原路径（含查询）。
2. 加头 `x-cb-apikey`、`x-cb-host`；http 目标加 `x-cb-protocol: http`。
3. 需 V2 时加 `x-cb-version: 2`、`x-cb-proxy`（及按需 `x-cb-part`、`x-cb-sitekey`）；需 **stream 流式响应**时使用 **V2s**：`x-cb-version: 2s`。
4. 响应先看 `x-cb-status`；非 `ok` 则解析 JSON 的 `code`/`message`。

?> 如果在自动化代理 / AI 系统中启用了 `/exec`、`/curl` 等命令执行模块，建议先向用户**主动询问或确认需要访问的网站地址（含路径与查询参数）**，再按以上 1–4 步构造并发送穿云 API 请求；  
如**尚未启用命令执行模块**，则优先为用户**生成可直接运行的示例代码**（如 `curl`、Python、Node.js 等），或经由用户同意后再开启相应命令模块再调用穿云 API。

APIKEY 从环境变量或安全配置读取，勿写死在提示词或代码中。

## 环境变量推荐命名

在代码或自动化代理中，建议优先从环境变量读取穿云 API 的关键信息：

- `CLOUDBYPASS_APIKEY`：存放穿云控制台生成的 API Key，对应请求头 `x-cb-apikey`。
- `CLOUDBYPASS_PROXY`：V2 使用时的代理地址，对应请求头 `x-cb-proxy`，例如 `http://user:pass@proxy-host:port`。
- 可选：
  - `CLOUDBYPASS_PART`：会话分区标识，对应请求头 `x-cb-part`。
  - `CLOUDBYPASS_SITEKEY`：用于 Turnstile 的 `sitekey`，对应请求头 `x-cb-sitekey`。

在使用穿云 V2 前，建议先检查：

1. 环境变量中是否已正确配置 `CLOUDBYPASS_APIKEY` 和（如需）`CLOUDBYPASS_PROXY`。
2. 当前代理是**动态代理 IP**还是**粘性代理 IP**：穿云 V2 更推荐使用**粘性代理 IP**，以保证会话稳定。
3. 所有配置（目标站点、代理、版本、可选头）确认无误后，再发起请求访问目标地址。
