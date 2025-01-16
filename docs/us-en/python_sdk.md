# Python SDK

### Getting Started

> The Cloudbypass Python SDK only supports Python 3.7 and above.

This SDK, based on `psf/requests`, supports calls to the Scrapingbypass API service. It automatically handles session
requests through the built-in session manager, eliminating the need to manually manage cookies and other information.

[![cloudbypass](https://img.shields.io/pypi/pyversions/cloudbypass)](https://pypi.org/project/cloudbypass/)
[![cloudbypass](https://img.shields.io/pypi/v/cloudbypass)](https://pypi.org/project/cloudbypass/)
[![cloudbypass](https://img.shields.io/pypi/dd/cloudbypass)](https://pypi.org/project/cloudbypass/#files)
[![cloudbypass](https://img.shields.io/pypi/wheel/cloudbypass)](https://pypi.org/project/cloudbypass/)

### Installation

```shell
python3 -m pip install cloudbypass -i https://pypi.org/simple
```

### Making Requests

`cloudbypass` is based on the `requests` library and supports all `requests` methods.

It allows you to set the Scrapingbypass API service key and proxy IP by adding the `apikey` and `proxy` initialization
parameters.

Custom users can specify the service address by setting the `api_host` parameter.

> These parameters can also be configured using the environment variables `CB_APIKEY`, `CB_PROXY`, and `CB_APIHOST`.

```python
from cloudbypass import SessionV2

if __name__ == '__main__':
    # Cookie mode: The server returns an encrypted cookie, which is sent by the client for authentication in the next request.
    with SessionV2(apikey="<APIKEY>", proxy="http://proxy:port") as session:
        resp = session.get("https://etherscan.io/accounts/label/lido")
        print("Status:", resp.status_code, resp.headers.get("x-cb-status"))
        print("Cookie:", resp.headers.get("set-cookie"))
        print("Body:", resp.text)

    # Part mode: The server manages the authentication cookie, and the client only needs to control the part parameter.
    with SessionV2(apikey="<APIKEY>", proxy="http://proxy:port", part="0") as session:
        resp = session.get("https://etherscan.io/accounts/label/lido")
        print("Status:", resp.status_code, resp.headers.get("x-cb-status"))
        print("Body:", resp.text)
```

#### async

The `AsyncSession` class inherits from `aiohttp.ClientSession` and supports all methods of `aiohttp`.

```python
import asyncio
from cloudbypass import AsyncSessionV2


async def main():
    # Cookie mode: The server returns an encrypted cookie, which is sent by the client for authentication in the next request.
    async with AsyncSessionV2(apikey="<APIKEY>", proxy="http://proxy:port") as session:
        resp = await session.get("https://etherscan.io/accounts/label/lido")
        print("Status:", resp.status)
        print("Cookie:", resp.headers.get("set-cookie"))
        text = await resp.text()
        print("Body:", text)

    # Part mode: The server manages the authentication cookie, and the client only needs to control the part parameter.
    async with AsyncSessionV2(apikey="<APIKEY>", proxy="http://proxy:port", part="0") as session:
        resp = await session.get("https://etherscan.io/accounts/label/lido")
        print("Status:", resp.status)
        text = await resp.text()
        print("Body:", text)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

### Using V2

Scrapingbypass API V2 is suitable for websites that require JS challenge verification. For example, to
access [https://etherscan.io/accounts/label/lido](https://etherscan.io/accounts/label/lido), a sample request would be:

```python
from cloudbypass import Session

if __name__ == '__main__':
    with Session(apikey="<APIKEY>", proxy="http://proxy:port") as session:
        resp = session.get("https://etherscan.io/accounts/label/lido", part="0")
        print(resp.status_code, resp.headers.get("x-cb-status"))
        print(resp.text)
```

#### async

```python
import asyncio
from cloudbypass import AsyncSession


async def main():
    async with AsyncSession(apikey="<APIKEY>", proxy="http://proxy:port") as session:
        resp = await session.get("https://etherscan.io/accounts/label/lido", part="0")
        print("Status:", resp.status)
        print("Content-type:", resp.headers['content-type'])
        html = await resp.text()
        print("Body:", html[:15], "...")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

### Check balance

Use the `get_balance` method to query the current account balance.

```python
from cloudbypass import get_balance

if __name__ == '__main__':
    print(get_balance("<APIKEY>"))

```

#### async

```python
import asyncio
from cloudbypass import async_get_balance


async def main():
    print(await async_get_balance("<APIKEY>"))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```

### Extracting Proxies

The `Proxy` class allows you to extract dynamic and time-sensitive proxies from Scrapingbypass.

+ `copy()` – Copies the current object so that the original object is not affected.
+ `set_dynamic()` – Sets the proxy as a dynamic proxy.
+ `set_expire(int)` – Sets the proxy as an expiring proxy, with the parameter being the expiration time of the IP in
  seconds.
+ `set_region(str)` – Sets the region for the proxy IP.
+ `clear_region()` – Clears the proxy's region.
+ `format(str)` – Formats the proxy IP, with the parameter being the format string, such
  as `{username}:{password}@gateway`.
+ `limit(int, str)` – Returns an iterator for a specified number of proxy IP strings and a proxy format string.
+ `loop(int, str)` – Returns a looped iterator for the specified number of proxy IP strings and a proxy format string.

```python
from cloudbypass import Proxy

if __name__ == '__main__':
    proxy = Proxy("username-res:password")

    # Extract dynamic proxy
    print("Extract dynamic proxy: ")
    print(str(proxy.set_dynamic()))  # Set the proxy as dynamic
    print(str(proxy.set_region('US')))  # Set the proxy region to 'US'

    # Extract expiring proxy and specify region
    print("Extract proxy with expire and region: ")
    print(str(proxy.copy().set_expire(60 * 30).set_region('US')))

    # Extract five proxies with 10-minute expiration
    print("Extract five 10-minute aging proxies: ")
    pool = proxy.copy().set_expire(60 * 10).set_region('US').limit(5)
    for _ in pool:
        print(_)

    # Loop to extract proxies with 10-minute expiration
    print("Loop two 10-minute aging proxies: ")
    loop = proxy.copy().set_expire(60 * 10).set_region('US').loop(2)
    for _ in range(10):
        print(loop.__next__()) 
```

### About Redirection Issues

When making requests with the SDK, redirection is automatically handled, and manual handling is not required. Redirect
responses will also consume credits.