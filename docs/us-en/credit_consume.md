# About the consumption of Scrapingbypass API credits

> Using Piercing Cloud v1 and v2 will consume `1 credit` after each [Request Success](/us-en/response_data?id=response-body)
<br/>
> When using Cloud Piercing v2, an additional `2 credits` will be consumed if a verification challenge is successful

This includes the following validations::

* `Cloudflare JS challenge`
* `Cloudflare Turnstile`
* `Incapsula`

If the verification challenge is successful, `2 credits` will be deducted immediately. If an error occurs during the response, the points will not be returned, but the request points will not be deducted.

?> **hint**<br/>Please use your credits within the validity period, as they will be automatically cleared after expiration.<br/>Credits will be deducted in the order of expiration.