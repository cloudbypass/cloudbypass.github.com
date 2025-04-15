# Scrapingbypass API proxy tool

?> It is recommended to use in Java projects, collectors and other services.
> Calling the Scrapingbypass API service through the Scrapingbypass API Proxy Client is suitable for complex session requests, such as login, session redirection requests, etc. Users only need to add proxy parameters to the original request, and the Scrapingbypass API Proxy Client will automatically forward the proxy request to the Scrapingbypass API service.

### Get tools

Visit the [API Proxy Client release page](https://github.com/cloudbypass/example/releases) to download the executable program and root certificate for the corresponding platform

### Startup parameters

| PARAMETER | DESCRIPTION                                        |
|----|-------------------------------------------|
| -k | (Optional) Scrapingbypass API service key, configure the default request header `x-cb-apikey`      |
| -l | (Optional) Service listening address (default "0.0.0.0:1087")      |
| -s | (Optional) Service address (default "api.scrapingbypass.com") |
| -x | (Optional) Configure the Scrapingbypass API request proxy. This value will be passed into the `x-cb-proxy` request header.    |

### Startup Command

> Use the following command to enable the preset apikey. You do not need to set the `x-cb-apikey` request header in subsequent calls.

```shell
# Use the default apikey
> cfb-mitm -k 0000000000000000 -x http:example.io:1288 -l 127.0.0.1:1087

# OUTPUT
# api.scrapingbypass.com -> 127.0.0.1:1087
# Please use proxy 127.0.0.1:1087
```

?> If -k or -x is not set, it can be dynamically configured via the request headers `x-cb-apikey` and `x-cb-proxy`.

The interface after startup👇

![proxy_tools.png](img%2Fproxy_tools.png)

### Calling with cURL

```shell
# linux
curl --request GET \
--url "https://opensea.io/category/memberships" \
--proxy "http://127.0.0.1:1087" \
-k

# windows
curl --request GET ^
--url "https://opensea.io/category/memberships" ^
--proxy "http://127.0.0.1:1087" ^
-k
```

?> Scrapingbypass API Proxy Client can solve the problem of managing information such as cookies in user programs. The http proxy runs locally, so there is no need to worry about security issues.

# About the software

This software is provided by [Scrapingbypass API](https://scrapingbypass.com/). It is strictly prohibited to use this software to engage in illegal activities such as fraud, theft of other people's accounts, funds, service attacks, etc.
