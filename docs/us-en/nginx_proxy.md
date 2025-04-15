# Scraping bypass API through Nginx proxy

The website proxied by this method does not have `Cloudflare WAF`, it is recommended to deploy it locally for personal use

### Configuration

`example.io` sets your domain name. You can also configure the test in the local `hosts` file.
`proxy.io` is the website you want to proxy.

```nginx
server {
    listen       80;
    server_name  example.io;

     location / {
        proxy_pass https://api.scrapingbypass.com;
        proxy_set_header x-cb-host proxy.io;
        proxy_set_header x-cb-apikey <APIKEY>;
        proxy_ssl_server_name on;
        proxy_ssl_name api.scrapingbypass.com;
    }
}
```