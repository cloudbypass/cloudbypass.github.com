# 采集器配置

### 火车头采集器

1. 下载启动[穿云API代理服务客户端](/zh-cn/proxy_tools)
2. 在火车头中新建任务，在其他设置的代理设置里配置`http://127.0.0.1:1087`代理

![huochetou_bjrw.png](img%2Fhuochetou_bjrw.png)

3. 如果启动`穿云API代理服务客户端`时没有配置APIKEY或者需要添加代理请求（已配置可忽略此步骤），可以在`其他设置`界面添加Http请求头

![huochetou_bjrw1.png](img%2Fhuochetou_bjrw1.png)

`apikey`对应`x-cb-apikey`请求头，代理则对应`x-cb-proxy`请求头。

?> **图中的`x-cb-host`请忽略掉**。