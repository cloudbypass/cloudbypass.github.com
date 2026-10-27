# Vibe Coding

Use an AI coding assistant to integrate the Scrapingbypass HTTP API into your project. Give the assistant the target URL, request method, expected response, and the relevant documentation below.

## Documentation for Your Assistant

- [Quick Start](/us-en/quickstart)
- [Request Parameters](/us-en/request_parameters)
- [Response Data and Error Codes](/us-en/response_data?id=error-code)
- [Python SDK](/us-en/python_sdk), [Nodejs SDK](/us-en/nodejs_sdk), and [Go SDK](/us-en/golang_sdk)

## Configure Credentials

Read credentials from environment variables rather than embedding them in prompts or source code:

| Environment variable | Request header | Usage |
| --- | --- | --- |
| `CLOUDBYPASS_APIKEY` | `x-cb-apikey` | Required for every request. Get your key from the [console](https://console.scrapingbypass.com/#/api/). |
| `CLOUDBYPASS_PROXY` | `x-cb-proxy` | Required for V2 and V2s. Use a sticky or fixed-IP proxy to maintain the session. |
| `CLOUDBYPASS_PART` | `x-cb-part` | Optional session partition for Part mode. |
| `CLOUDBYPASS_SITEKEY` | `x-cb-sitekey` | Used when handling a Turnstile widget. |

## Copyable Prompt

Replace the placeholders with your project requirements:

```text
Integrate the Scrapingbypass API into this project.

Target URL: <full URL, including path and query string>
Request method and body: <method and body, if any>
Language or framework: <project language or framework>
Expected output: <how to process the response>

Read the API documentation:
https://docs.scrapingbypass.com/#/us-en/request_parameters
https://docs.scrapingbypass.com/#/us-en/response_data

Implementation requirements:
1. Read the API key from CLOUDBYPASS_APIKEY. Do not log credentials.
2. Replace the target URL's scheme and host with https://api.scrapingbypass.com,
   preserving its path and query string. Set x-cb-host to the original host
   (including its port, if present), without the scheme or path.
3. Preserve the original method, body, and applicable request headers.
   Set x-cb-protocol: http only when the original target uses HTTP.
4. Start with V1 when the target works in a browser but returns 403 in code.
   Use V2 for JS Challenge, Turnstile, or DataDome challenges; set
   x-cb-version: 2 and read x-cb-proxy from CLOUDBYPASS_PROXY.
   Use x-cb-version: 2s when streaming is required, with the same proxy setup.
5. For V2/V2s, use Cookie mode or a consistent x-cb-part for the session.
   For Turnstile, follow the documented x-cb-sitekey and [cf_token] workflow.
6. Check the x-cb-status response header. If it is ok, process the target
   response; otherwise parse the JSON id, code, and message for diagnostics.
7. Validate required configuration before making a request. Provide runnable
   code and setup instructions, and avoid unbounded retries.
```

## Use in OpenClaw

You can also provide the existing [API Quick Reference](/api-quick-reference) to your agent:

```text
Use the Scrapingbypass API:
https://docs.scrapingbypass.com/api-quick-reference.md
```

The shared quick reference is currently written in Chinese. For English instructions, use the prompt and documentation links above.

Before sending requests, check the API key, target URL, selected API version, and proxy configuration. For V2/V2s, confirm that the proxy keeps the same IP for the session.

## Verify the Integration

- Confirm that the original path, query string, method, and body are preserved.
- Check `x-cb-status` as well as the target HTTP status; do not assume that every HTTP response means the API request succeeded.
- Handle API errors using the documented [error codes](/us-en/response_data?id=error-code).
- Configure `x-cb-timeout` within the documented limits: 5–3600 seconds for V1/V2s, or 5–360 seconds for V2.
- For streaming, process the V2s response incrementally instead of buffering the entire response.
- Review [credit consumption](/us-en/credit_consume) before running repeated requests.
