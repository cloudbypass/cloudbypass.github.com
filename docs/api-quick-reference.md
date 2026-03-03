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

APIKEY 从环境变量或安全配置读取，勿写死在提示词或代码中。
