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

Use initialization parameters `apikey` and `proxy` for the API key and proxy IP.

Custom deployments can set `api_host` for the API base URL.

> You can also configure these via environment variables `CB_APIKEY`, `CB_PROXY`, and `CB_APIHOST`.

```python
from cloudbypass import Session

if __name__ == '__main__':
    with Session(apikey="<APIKEY>", proxy="http://proxy:port") as session:
        resp = session.get("https://opensea.io/category/memberships")
        print(resp.status_code, resp.headers.get("x-cb-status"))
        print(resp.text)
```

#### async

```python
import asyncio
from cloudbypass import AsyncSession


async def main():
    async with AsyncSession(apikey="<APIKEY>", proxy="http://proxy:port") as session:
        resp = await session.get("https://opensea.io/category/memberships")
        print("Status:", resp.status)
        text = await resp.text()
        print("Body:", text)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

### Using V2

Cloudbypass API V2 is for sites that require JS challenges. Example: https://etherscan.io/accounts/label/lido

```python
from cloudbypass import SessionV2

if __name__ == '__main__':
    # Cookie mode: server returns encrypted cookie; client sends it on the next request
    with SessionV2(apikey="<APIKEY>", proxy="http://proxy:port") as session:
        resp = session.get("https://etherscan.io/accounts/label/lido")
        print("Status:", resp.status_code, resp.headers.get("x-cb-status"))
        print("Cookie:", resp.headers.get("set-cookie"))
        print("Body:", resp.text)

    # Part mode: server manages cookie; client only sets part
    with SessionV2(apikey="<APIKEY>", proxy="http://proxy:port", part="0") as session:
        resp = session.get("https://etherscan.io/accounts/label/lido")
        print("Status:", resp.status_code, resp.headers.get("x-cb-status"))
        print("Body:", resp.text)

```

#### async

```python
import asyncio
from cloudbypass import AsyncSessionV2


async def main():
    async with AsyncSessionV2(apikey="<APIKEY>", proxy="http://proxy:port") as session:
        resp = await session.get("https://etherscan.io/accounts/label/lido")
        print("Status:", resp.status)
        print("Cookie:", resp.headers.get("set-cookie"))
        text = await resp.text()
        print("Body:", text)

    async with AsyncSessionV2(apikey="<APIKEY>", proxy="http://proxy:port", part="0") as session:
        resp = await session.get("https://etherscan.io/accounts/label/lido")
        print("Status:", resp.status)
        text = await resp.text()
        print("Body:", text)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

### Check balance

`get_balance` calls `POST https://console.cloudbypass.com/api/v1/balance` with a JSON body (query parameters were
replaced by JSON fields).

Use keyword argument `type` (or constants `BALANCE_TYPE_POINTS`, `BALANCE_TYPE_RES`, `BALANCE_TYPE_DAT`).

| Constant / `type`               | Meaning                   | Response JSON                |
|---------------------------------|---------------------------|------------------------------|
| `BALANCE_TYPE_POINTS` (default) | Credits                   | `{"balance": 0}`             |
| `BALANCE_TYPE_RES`              | Residential proxy traffic | `{"total": 0, "balance": 0}` |
| `BALANCE_TYPE_DAT`              | Datacenter proxy traffic  | `{"total": 0, "balance": 0}` |

```python
from cloudbypass import (
    BALANCE_TYPE_DAT,
    BALANCE_TYPE_POINTS,
    BALANCE_TYPE_RES,
    get_balance,
)

if __name__ == '__main__':
    print(get_balance("<APIKEY>", "<EMAIL>"))
    print(get_balance("<APIKEY>", "<EMAIL>", type=BALANCE_TYPE_POINTS))
    print(get_balance("<APIKEY>", "<EMAIL>", type=BALANCE_TYPE_RES))
    print(get_balance("<APIKEY>", "<EMAIL>", type=BALANCE_TYPE_DAT))

```

#### async

```python
import asyncio
from cloudbypass import BALANCE_TYPE_RES, async_get_balance


async def main():
    print(await async_get_balance("<APIKEY>", "<EMAIL>"))
    print(await async_get_balance("<APIKEY>", "<EMAIL>", type=BALANCE_TYPE_RES))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```

`convert_bytes` formats byte counts as human-readable strings, e.g. `convert_bytes(data["balance"])`.

### Extracting Proxies

The `Proxy` class extracts dynamic and time-limited proxies.

+ `copy()` — clone without affecting the original.
+ `set_dynamic()` — dynamic proxy.
+ `set_expire(int)` — expiring proxy; seconds until expiry.
+ `set_region(str)` — region.
+ `clear_region()` — clear region.
+ `format(str)` — format string such as `{username}:{password}@gateway`.
+ `limit(int, str)` — iterator over N proxies with format.
+ `loop(int, str)` — cyclic iterator.

```python
from cloudbypass import Proxy

if __name__ == '__main__':
    proxy = Proxy("username-res:password")

    print("Extract dynamic proxy: ")
    print(str(proxy.set_dynamic()))
    print(str(proxy.set_region('US')))

    print("Extract proxy with expire and region: ")
    print(str(proxy.copy().set_expire(60 * 30).set_region('US')))

    print("Extract five 10-minute aging proxies: ")
    pool = proxy.copy().set_expire(60 * 10).set_region('US').limit(5)
    for _ in pool:
        print(_)

    print("Loop two 10-minute aging proxies: ")
    loop = proxy.copy().set_expire(60 * 10).set_region('US').loop(2)
    for _ in range(10):
        print(loop.__next__())
```

### About Redirection Issues

When making requests with the SDK, redirection is automatically handled, and manual handling is not required. Redirect
responses will also consume credits.
