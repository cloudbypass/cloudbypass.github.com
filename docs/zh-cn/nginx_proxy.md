# 通过Nginx代理穿云API

这种方式代理出来的网站没有`Cloudflare WAF`，建议在本地部署个人使用就行了

### 配置文件

`example.io`设置你的域名，你也可以在本机`hosts`文件中配置测试。
`proxy.io`是你要代理的网站。

```nginx
server {
    listen       80;
    server_name  example.io;

     location / {
        proxy_pass https://api.cloudbypass.com;
        proxy_set_header x-cb-host proxy.io;
        proxy_set_header x-cb-apikey <APIKEY>;
        proxy_ssl_server_name on;
        proxy_ssl_name api.cloudbypass.com;
    }
}
```