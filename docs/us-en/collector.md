# Collector Configuration

### Locoy Collector

1. Download Start [Scrapingbypass API Proxy Client](/us-en/proxy_tools)
2. Create a new task in Locoy and configure the proxy `http://127.0.0.1:1087` in the proxy settings of other settings

![huochetou_bjrw.png](img%2Fhuochetou_bjrw.png)

3. If you do not configure APIKEY when starting `Scrapingbypass API Proxy Client` or need to add a proxy request (if configured, you can ignore this step), you can add the Http request header in the `Other Settings` interface

![huochetou_bjrw1.png](img%2Fhuochetou_bjrw1.png)

`apikey` corresponds to the `x-cb-apikey` request header, and the proxy corresponds to the `x-cb-proxy` request header.

?> **Please ignore the `x-cb-host` in the picture.**.