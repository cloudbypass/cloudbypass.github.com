# Nodejs SDK

### Getting Started

> Cloudbypass Node.js SDK depends on [Axios](https://axios-http.com/).

All Axios options are supported, plus cross-origin requests and cookie handling.

[![npm version](https://img.shields.io/npm/v/cloudbypass-sdk.svg?style=flat-square)](https://www.npmjs.org/package/cloudbypass-sdk ":no-zoom")
[![install size](https://img.shields.io/badge/dynamic/json?url=https://packagephobia.com/v2/api.json?p=cloudbypass-sdk&query=$.install.pretty&label=install%20size&style=flat-square)](https://packagephobia.now.sh/result?p=cloudbypass-sdk ":no-zoom")
[![npm bundle size](https://img.shields.io/bundlephobia/minzip/cloudbypass-sdk?style=flat-square)](https://bundlephobia.com/package/cloudbypass-sdk@latest ":no-zoom")

### Installation

Using npm:

```shell
$ npm install cloudbypass-sdk
```

Using yarn:

```shell
$ yarn add cloudbypass-sdk
```

Using pnpm:

```shell
$ pnpm add cloudbypass-sdk
```

### Usage

```js
const cloudbypass = require('cloudbypass-sdk');
```

ES modules:

```js
import cloudbypass from 'cloudbypass-sdk';
```

### Making Requests

Treat `cloudbypass-sdk` like Axios. Extra config fields:

- `cb_apikey` — API key;
- `cb_version` — `'1'`, `'2'`, or `'2s'` (default `'1'`);
- `cb_use_v2` — deprecated; prefer `cb_version: '2'`;
- `cb_part` — V2 part mode;
- `cb_proxy` — HTTP or SOCKS5 proxy;
- `cb_apihost` — custom API host;

> Env vars: `CLOUDBYPASS_APIKEY` / `CLOUDBYPASS_PROXY` first, then `CB_APIKEY` / `CB_PROXY`. `CB_APIHOST` for API server.

```js
import cloudbypass from 'cloudbypass-sdk';

cloudbypass.get('https://opensea.io/category/memberships', {
    cb_apikey: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
})
    .then(function (response) {
        console.log(response.status, response.headers.get("x-cb-status"));
        console.log(response.data);
    })
    .catch(function (error) {
        console.log(error.response.data || error.response || error.message);
    });
```

### Using V2

For JS challenges, e.g. https://etherscan.io/accounts/label/lido :

```js
import cloudbypass, {isBypassError} from 'cloudbypass-sdk';

try {
    const resp = (await cloudbypass.get("https://etherscan.io/accounts/label/lido", {
        cb_apikey: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        cb_proxy: 'http://proxy:port',
        cb_version: '2'
    }));
    console.log(resp.headers['set-cookie']);
    console.log(resp.data);
} catch (e) {
    if (isBypassError(e)) {
        console.log(e.response.data || e.response || e.message);
    } else {
        console.log(e);
    }
}

try {
    const resp = (await cloudbypass.get("https://etherscan.io/accounts/label/lido", {
        cb_apikey: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        cb_proxy: 'http://proxy:port',
        cb_version: '2s'
    }));
    console.log(resp.data);
} catch (e) {
    if (isBypassError(e)) {
        console.log(e.response.data || e.response || e.message);
    } else {
        console.log(e);
    }
}

try {
    const resp = (await cloudbypass.get("https://etherscan.io/accounts/label/lido", {
        cb_apikey: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        cb_proxy: 'http://proxy:port',
        cb_part: '0'
    }));
    console.log(resp.status, resp.headers.get("x-cb-status"));
    console.log(resp.data);
} catch (e) {
    if (isBypassError(e)) {
        console.log(e.response.data || e.response || e.message);
    } else {
        console.log(e);
    }
}

try {
    const resp = (await cloudbypass.get("https://etherscan.io/accounts/label/lido", {
        cb_apikey: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        cb_proxy: 'http://proxy:port',
        cb_use_v2: true
    }));
    console.log(resp.data);
} catch (e) {
    if (isBypassError(e)) {
        console.log(e.response.data || e.response || e.message);
    } else {
        console.log(e);
    }
}
```

### Check balance

`getBalance` calls `POST https://console.cloudbypass.com/api/v1/balance` with JSON. Pass `{ type }` as third argument (`BALANCE_TYPE_POINTS`, `BALANCE_TYPE_RES`, `BALANCE_TYPE_DAT`). Traffic types return `{ total, balance }` in bytes; credits return `{ balance }`.

```js
import cloudbypass, {
    BALANCE_TYPE_DAT,
    BALANCE_TYPE_POINTS,
    BALANCE_TYPE_RES,
} from 'cloudbypass-sdk';

cloudbypass.getBalance('/* APIKEY */', '/* EMAIL */').then((data) => console.log(data));
cloudbypass.getBalance('/* APIKEY */', '/* EMAIL */', { type: BALANCE_TYPE_RES }).then((data) => {
    console.log(data.total, data.balance);
});
```

`convertBytes` formats byte values for display, e.g. `convertBytes(data.balance)`.

### Extracting proxies

`cloudbypass.createProxy(auth)` returns a `CloudbypassProxy` instance.

+ `copy()`, `setDynamic()`, `setExpire`, `setRegion`, `clearRegion`, `toString`, `format`, `limit`, `loop` — see README behavior.

```js
import cloudbypass from 'cloudbypass-sdk';

const proxy = cloudbypass.createProxy("username-res:password");

console.log("Extract dynamic proxy: ")
console.log(proxy.setDynamic().toString())
console.log(proxy.setRegion("US").toString())

console.log("Extract proxy with expire and region: ")
console.log(proxy.copy().setExpire(60 * 30).setRegion("US").toString())

console.log("Extract five 10-minute aging proxies: ")
const pool = proxy.copy().setExpire(60 * 10).limit(5);
for (let p of pool) {
    console.log(p)
}

console.log("Loop two 10-minute aging proxies: ")
const loop = proxy.copy().setExpire(60 * 10).loop(2);
for (let i = 0; i < 10; i++) {
    console.log(loop.next().value)
}
```

### About redirects

Redirects are handled automatically; redirect responses still consume credits.