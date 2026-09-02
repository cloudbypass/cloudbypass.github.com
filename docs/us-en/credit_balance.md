# Check account balance

You can view usage in the [console](https://console.cloudbypass.com/#/api/), or query via HTTP API / SDK.

### Via HTTP API

Use **POST** `https://console.cloudbypass.com/api/v1/balance` with `Content-Type: application/json` and a JSON body: `apikey`, `email`, `type`.

**`type` and response (on HTTP 200):**

| `type` | Meaning | Response body |
|--------|---------|----------------|
| `points` | Account **credits** | See **Credit response fields** below |
| `res` | **Residential** proxy traffic | `{"total": <bytes>, "balance": <bytes>}` (values are **bytes**) |
| `dat` | **Datacenter** proxy traffic | same shape as `res` |

**Credit response fields (`type=points`):**

| Field | Type | Description |
|-------|------|-------------|
| `balance` | number | Remaining credit balance |
| `expires_at_min` | number \| null | Earliest expiration among valid credits (Unix timestamp in seconds); `null` if none |
| `expires_at_max` | number \| null | Latest expiration among valid credits (Unix timestamp in seconds); `null` if none |

```json
{
  "balance": 9999816,
  "expires_at_min": 1725408000,
  "expires_at_max": 1728000000
}
```

```shell
# Credits
curl -s -X POST "https://console.cloudbypass.com/api/v1/balance" \
  -H "Content-Type: application/json" \
  -d '{"apikey":"<APIKEY>","email":"<EMAIL>","type":"points"}'

# Residential traffic (use "dat" for datacenter)
curl -s -X POST "https://console.cloudbypass.com/api/v1/balance" \
  -H "Content-Type: application/json" \
  -d '{"apikey":"<APIKEY>","email":"<EMAIL>","type":"res"}'
```

**GET is deprecated**

The old **GET** call with query string `?apikey=<APIKEY>&email=<email>` is **deprecated**. Use **POST with a JSON body** (including `type`) instead. Migrate as soon as possible to avoid future breakage.

### Via SDK

* [Python](/us-en/python_sdk?id=check-balance)
* [Nodejs](/us-en/nodejs_sdk?id=check-balance)
* [Go](/us-en/golang_sdk?id=check-balance)
