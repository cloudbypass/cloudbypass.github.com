# Quick start

> Scrapingbypass can help you easily bypass Cloudflare's verification. Currently, it supports bypassing JS challenge,
> Turnstile and other product verifications. This document provides detailed usage of
> Scrapingbypass [HTTP API](/us-en/request_parameters), [local proxy tool](/us-en/proxy_tools)
> and [SDK](/us-en/quickstart?id=code-sample).

### Workflow

Scrapingbypass API request flow

![cloudbypass_api_fc.svg](img/cloudbypass_api_fc.svg)

?> Whether you use the [local proxy tool](/us-en/proxy_tools) or [SDK](/us-en/quickstart?id=code-sample), you are only
forwarding the request, which is actually an HTTP API request.

### Get APIKEY

Visit the [Scrapingbypass API console](https://console.scrapingbypass.com/#/api/) to register an account and obtain the APIKEY.

### Code Sample

Check out the existing [code examples](https://github.com/cloudbypass/example) to quickly integrate into your project.

![GitHub last commit](https://img.shields.io/github/last-commit/cloudbypass/example ":no-zoom")

* [Python SDK](/us-en/python_sdk) ![PyPI - Version](https://img.shields.io/pypi/v/cloudbypass ":no-zoom")
* [Nodejs SDK](/us-en/nodejs_sdk) ![NPM Version](https://img.shields.io/npm/v/cloudbypass-sdk ":no-zoom")
* [Go SDK](/us-en/golang_sdk) ![GitHub go.mod Go version](https://img.shields.io/github/go-mod/go-version/cloudbypass/golang-sdk ":no-zoom")

### Accessibility Testing

By using the [Code Generator](https://console.scrapingbypass.com/#/code-generator) to check whether the target website can be breached, newly registered users can [Customer Support](https://t.me/cloudbypasscom) to get a trial.

### About version

#### Scrapingbypass V1

> This is used when the browser can access it, but 403 is returned when accessed through program code.

Scrapingbypass v1 comes with a dynamic proxy by default, and you can also set up your own proxy server as needed, and each request is stateless.

#### Scrapingbypass V2

> Used when encountering the following `JS challenge` or `turnstile` components

![turnstile.png](img%2Fturnstile.gif ":no-zoom :size=350")

?> Scrapingbypass V2 must provide a fixed or time-sensitive IP proxy to work.

* **Beat the `JS challenge`,Scrapingbypass V2 will automatically challenge**
    * After the challenge is successful, the Scrapingbypass service will store the `cloudflare cookie` for 10 minutes. Subsequent requests will automatically use the session for access. After another successful request, the session will be automatically renewed.
    * You can set the session partition by configuring the `x-cb-part` parameter to achieve session isolation.
    * If the challenge fails, a JSON-formatted response body will be sent, including the request ID, [error code](/us-en/response_data?id=error-code), and error information.
* **Breaking out the `turnstile` widget**
    * Users need to provide [`sitekey`](/us-en/request_parameters?id=how-to-get-sitekey) and fill it in the request header `x-cb-sitekey`.
    * Generally, after verification, `turnstile` will return a token string starting with `0.`. It may also be `cf-turnstile-response`, `turnstileToken`, etc., but with different names.
    * Scrapingbypass V2 will not return its token to the client. Add the `[cf-token]` string where the token is required. Scrapingbypass will automatically fill it in and initiate the request.
        * [Example 1](https://github.com/cloudbypass/example/blob/main/code/com/berachain/faucet/artio/api_claim.py#L20)
          Put the token in the request header Authorization.
        * [Example 2](https://github.com/cloudbypass/example/blob/main/code/com/joshsfrogs/login.py#L24)
          Put the token in the request header X-Turnstile-Response.
        * [Example 3](https://github.com/cloudbypass/example/blob/main/code/com/cityline/api_otp.py#L22)
          Put `token` in the request body `accessToken`.

### Get Help

* [Visit the forum](https://www.scrapingbypass.com/blog/)
* [Customer Support](https://t.me/cloudbypasscom)
