# Quick Start

> Using Scrapingbypass can help you easily bypass Cloudflare's verifications, including JS Challenges, Turnstile, and other product verifications. This document provides detailed usage instructions for Scrapingbypass's [HTTP API](/us-en/request_parameters), [Local Proxy Tools](/us-en/proxy_tools), and [SDK](/us-en/quickstart?id=code-example).

# Workflow

The request flow for the Scrapingbypass API:

![cloudbypass_api_fc.svg](img/cloudbypass_api_fc.svg)

?> Whether using [Local Proxy Tools](/us-en/proxy_tools) or [SDK](/us-en/quickstart?id=code-example), it is essentially forwarding requests, and the underlying operation still relies on HTTP API requests.

# Get API Key

Visit the [Scrapingbypass API Console](https://console.cloudbypass.com/#/api/) to register and get your API key.

# Code Examples

Check out the existing [code examples](https://github.com/cloudbypass/example) to quickly integrate them into your project.

![GitHub last commit](https://img.shields.io/github/last-commit/cloudbypass/example ":no-zoom")

* [Python SDK](/us-en/python_sdk) ![PyPI - Version](https://img.shields.io/pypi/v/cloudbypass ":no-zoom")
* [Nodejs SDK](/us-en/nodejs_sdk) ![NPM Version](https://img.shields.io/npm/v/cloudbypass-sdk ":no-zoom")
* [Go SDK](/us-en/golang_sdk) ![GitHub go.mod Go version](https://img.shields.io/github/go-mod/go-version/cloudbypass/golang-sdk ":no-zoom")

# Accessibility Test

Use the [Code Generator](https://console.cloudbypass.com/#/code-generator) to check if the target website can be bypassed. New users can [contact customer support](https://t.me/cloudbypasscom) for a trial.

# About Scrapingbypass API Versions

## Scrapingbypass V1

> Use when the website is accessible in a browser but returns a `403` when accessed via code.

Scrapingbypass V1 comes with a built-in dynamic proxy. You can also set up your own proxy server if needed. Each request is stateless.

## Scrapingbypass V2

> Use when encountering `JS Challenge` or `Turnstile` components.

![turnstile.png](img%2Fturnstile.gif ":no-zoom :size=350")

?> Scrapingbypass V2 requires a fixed or time-sensitive IP proxy to operate.

### How to Distinguish Between Two Verifications?

In Scrapingbypass V2, you can distinguish between `JS Challenge` and `Turnstile` verification mechanisms using the following rules:

1. **JS Challenge**
    - When the visitor **first loads the website page**, the server returns HTTP status code `403`.
    - The response headers contain the field `cf-mitigated: challenge`.

2. **Turnstile**
    - Triggered **when submitting a form** that involves a verification widget.
    - Does not meet the characteristics of `JS Challenge`, i.e., the response does not contain the `cf-mitigated: challenge` field.

### Bypass `JS Challenge`, Scrapingbypass V2 Auto Challenge

Scrapingbypass V2 supports two modes to automatically handle the JS Challenge mechanism on the target website: `Cookie` mode and `Part` mode. Below are the details for each mode:

**1. Cookie Mode**  
The client is responsible for managing the encrypted Cookie returned by the server.

- **Session Management**  
  The client needs session management functionality. For example, Python’s `requests` library integrates a session management module, which can maintain session state across multiple requests.

- **Challenge Success**  
  After a successful challenge, Scrapingbypass returns the encrypted Cookie to the client. The client can carry this Cookie in subsequent requests to maintain the session state.

- **Challenge Failure**  
  If the challenge fails, the server returns a JSON formatted response body that includes:
    - Request ID
    - [Error Codes](/us-en/response_data?id=error-codes)
    - Error message

**2. Part Mode**  
The server hosts the verification Cookie and supports session partitioning for finer control.

- **Partition Control**  
  The `x-cb-part` header parameter can be configured to manage server-side session partitioning, ensuring session isolation within the partition.

- **Challenge Success**  
  After a successful challenge, Scrapingbypass stores the validated Cookie in the server's session partition, which is valid for 10 minutes. During this period:
    - Subsequent client requests automatically carry the Cookie from the partition to maintain the session state.
    - Each successful request refreshes the session partition's validity, ensuring continuous access.

- **Challenge Failure**  
  If the challenge fails, the server returns a JSON formatted response body that includes:
    - Request ID
    - [Error Codes](/us-en/response_data?id=error-codes)
    - Error message

---

### Bypass `Turnstile` Component

Scrapingbypass V2 supports handling the `Turnstile` component verification. Below are the specific steps:

**Functionality Description**

- **Provide `sitekey`**  
  The user needs to fill in the `x-cb-sitekey` header parameter and provide the corresponding [`sitekey`](/us-en/request_parameters?id=how-to-get-sitekey).

- **Verification Result**  
  Typically, after a successful verification, `Turnstile` will return a token string starting with `0.`, or other names like `cf-turnstile-response` or `turnstileToken`, depending on the naming convention.

- **Token Usage**  
  Scrapingbypass V2 will not return the Token directly to the client. Instead, it will replace `[cf_token]` in the request with the valid Token and initiate the request.

**Usage Examples**

Here are code examples for different scenarios of using the Token:

1. **Example 1**  
   Place the Token in the `Authorization` header:  
   [View Code Example](https://github.com/cloudbypass/example/blob/main/code/com/berachain/faucet/artio/api_claim.py#L20)

2. **Example 2**  
   Place the Token in the `X-Turnstile-Response` header:  
   [View Code Example](https://github.com/cloudbypass/example/blob/main/code/com/joshsfrogs/login.py#L24)

3. **Example 3**  
   Place the Token in the `accessToken` field in the request body:  
   [View Code Example](https://github.com/cloudbypass/example/blob/main/code/com/cityline/api_otp.py#L22)

### Get Help

* [Visit the Forum](https://www.cloudbypass.com/blog/)
* [Contact Customer Support](https://t.me/cloudbypasscom)
