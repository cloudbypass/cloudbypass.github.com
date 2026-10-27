# Versions and Challenges

Complete the [Quick Start](/us-en/quickstart), then choose a version, proxy, and session mode for your target.

## Scrapingbypass V1

> Use when the website is accessible in a browser but returns a `403` when accessed via code.

Scrapingbypass V1 comes with a built-in dynamic proxy. You can also set up your own proxy server if needed. Each request is stateless.

## Scrapingbypass V2

> Use when encountering `JS Challenge`, `Turnstile` components, or `DataDome` challenges.

![turnstile.png](img%2Fturnstile.gif ":no-zoom :size=350")

?> Scrapingbypass V2 requires a fixed or time-sensitive IP proxy to operate.

## Scrapingbypass V2s

Scrapingbypass V2s is the same as V2 but supports **stream response**, suitable for large file downloads or when you need to process data as it streams. Usage: set request header `x-cb-version: 2s`; all other parameters are the same as V2 (e.g. `x-cb-proxy`, `x-cb-part`).

## How to Distinguish Common Verifications?

In Scrapingbypass V2, you can identify the verification mechanism using the following rules:

1. **JS Challenge**
    - When the visitor **first loads the website page**, the server returns HTTP status code `403`.
    - The response headers contain the field `cf-mitigated: challenge`.

2. **Turnstile**
    - Triggered **when submitting a form** that involves a verification widget.
    - Does not meet the characteristics of `JS Challenge`, i.e., the response does not contain the `cf-mitigated: challenge` field.

3. **DataDome**
    - Returns HTTP status code `403`.
    - Response headers include both `x-datadome-cid` and `x-dd-b` (often also `x-datadome: protected`).

## Bypass `JS Challenge`, Scrapingbypass V2 Auto Challenge

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
    - [Error Codes](/us-en/response_data?id=error-code)
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
    - [Error Codes](/us-en/response_data?id=error-code)
    - Error message

---

## Bypass `Turnstile` Component

Scrapingbypass V2 supports handling the `Turnstile` component verification. Below are the specific steps:

**Functionality Description**

- **Provide `sitekey`**  
  The user needs to fill in the `x-cb-sitekey` header parameter and provide the corresponding [`sitekey`](/us-en/request_parameters?id=how-to-obtain-sitekey). Also place `[cf_token]` or `%5Bcf_token%5D` at the token position in the URL, headers, or body; sitekey alone does not trigger token solving. Use `x-cb-action` and `x-cb-cdata` for the site's optional action and cData parameters.

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

---

## Bypass `DataDome` Challenge

Scrapingbypass V2 automatically detects and solves DataDome challenges. No extra request headers are required.

**Detection**

- Target returns `403`
- Response headers include both `x-datadome-cid` and `x-dd-b`

**Usage**

- Same as other V2 challenges: a **sticky / duration proxy** (`x-cb-proxy`) is required.
- Works with both [Cookie mode and Part mode](/us-en/challenges?id=bypass-js-challenge-scrapingbypass-v2-auto-challenge).
- In Cookie mode, a successful challenge returns an encrypted Cookie that includes `datadome`; in Part mode the session is hosted on the server.
- If a site uses both Cloudflare and DataDome, Scrapingbypass handles them in sequence. Each successful challenge stage consumes credits—see [Credit consumption](/us-en/credit_consume).

?> DataDome challenges may take longer. Set `x-cb-timeout` appropriately (V2 max 360 seconds).

## Get Help

* [Visit the Forum](https://www.scrapingbypass.com/blog/)
* [Contact Customer Support](https://t.me/cloudbypasscom)
