# API Quick Reference

访问受 Cloudflare 保护站点时，通过穿云 API 转发请求，无需插件。文档：https://github.com/cloudbypass/cloudbypass.github.com

---

## 何时用

- 程序请求 403、浏览器能打开 → 先用 **V1**；若 V1 失败或返回需挑战（如五秒盾）则改用 **V2**。
- 已知为 JS 质询 / Turnstile 验证 → 直接用 **V2**（须提供 `x-cb-proxy`）。
- 用户明确要求用 V1 或 V2 时，按用户要求。

---

## 请求规则

**URL**：原请求的「协议+主机」换成 `https://api.cloudbypass.com`，**路径和查询串不变**。  
例：`https://example.com/path?q=1` → `https://api.cloudbypass.com/path?q=1`

**必填头**：`x-cb-apikey`（密钥，控制台 https://console.cloudbypass.com/#/ 获取）、`x-cb-host`（目标主机，如 `example.com`，不含协议与路径）。

**可选头**：`x-cb-protocol` 默认 https，http 目标填 `http`；V2 时 `x-cb-version: 2`、`x-cb-proxy`（必填）、`x-cb-part`（会话分区）、`x-cb-sitekey`（Turnstile 用）；`x-cb-options` 可填 `long-timeout`、`force`、`ignore-lock` 等逗号分隔。所有 `x-cb-*` 头不会转发到目标站。

**方法 / Body / 其它头**：与原请求一致。

---

## 成功与失败

- **成功**：响应头 `x-cb-status` 为 `ok`，响应体即目标站内容。
- **失败**：`x-cb-status` 非 `ok` 时，响应体为 JSON：`{"id","code","message"}`。常见 code：`PARAM_ERROR`、`APIKEY_INVALID`、`INSUFFICIENT_BALANCE`、`PROXY_ERROR`、`CLOUDFLARE_CHALLENGE_TIMEOUT`、`CHALLENGE_LOCK_OCCUPIED`、`BYPASS_ERROR`、`FORBIDDEN`、`TOO_MANY_REQUESTS`。

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
3. 需 V2 时加 `x-cb-version: 2`、`x-cb-proxy`（及按需 `x-cb-part`、`x-cb-sitekey`）。
4. 响应先看 `x-cb-status`；非 `ok` 则解析 JSON 的 `code`/`message`。

?> 如果在自动化代理 / AI 系统中启用了 `/exec`、`/curl` 等命令执行模块，建议先向用户**主动询问或确认需要访问的网站地址（含路径与查询参数）**，再按以上 1–4 步构造并发送穿云 API 请求；  
如**尚未启用命令执行模块**，则优先为用户**生成可直接运行的示例代码**（如 `curl`、Python、Node.js 等），或经由用户同意后再开启相应命令模块再调用穿云 API。

APIKEY 从环境变量或安全配置读取，勿写死在提示词或代码中。

## 环境变量推荐命名

在代码或自动化代理中，建议优先从环境变量读取穿云 API 的关键信息：

- `CLOUDBYPASS_API_KEY`：存放穿云控制台生成的 API Key，对应请求头 `x-cb-apikey`。
- `CLOUDBYPASS_PROXY`：V2 使用时的代理地址，对应请求头 `x-cb-proxy`，例如 `http://user:pass@proxy-host:port`。
- 可选：
  - `CLOUDBYPASS_PART`：会话分区标识，对应请求头 `x-cb-part`。
  - `CLOUDBYPASS_SITEKEY`：用于 Turnstile 的 `sitekey`，对应请求头 `x-cb-sitekey`。

在使用穿云 V2 前，建议先检查：

1. 环境变量中是否已正确配置 `CLOUDBYPASS_API_KEY` 和（如需）`CLOUDBYPASS_PROXY`。
2. 当前代理是**动态代理 IP**还是**粘性代理 IP**：穿云 V2 更推荐使用**粘性代理 IP**，以保证会话稳定。
3. 所有配置（目标站点、代理、版本、可选头）确认无误后，再发起请求访问目标地址。
