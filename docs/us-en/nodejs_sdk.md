# Nodejs SDK

> Cloudbypass Nodejs SDK depends on [Axios](https://axios-http.com/).

Keep all request configurations of axios and support **⚠cross-domain requests** and Cookie management.

The CloudCross SDK, which is encapsulated on the basis of `psf/requests`, supports the call of Scrapingbypass API service. Through the built-in session manager, session requests can be automatically processed without manually managing information such as cookies.

[![npm version](https://img.shields.io/npm/v/cloudbypass-sdk.svg?style=flat-square)](https://www.npmjs.org/package/cloudbypass-sdk ":no-zoom")
[![install size](https://img.shields.io/badge/dynamic/json?url=https://packagephobia.com/v2/api.json?p=cloudbypass-sdk&query=$.install.pretty&label=install%20size&style=flat-square)](https://packagephobia.now.sh/result?p=cloudbypass-sdk ":no-zoom")
[![npm bundle size](https://img.shields.io/bundlephobia/minzip/cloudbypass-sdk?style=flat-square)](https://bundlephobia.com/package/cloudbypass-sdk@latest ":no-zoom")

### Install

#### Package Manager Installation

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

Once the package is installed, you can import the library using the require method:

```js
// Using Node.js `require()`
const cloudbypass = require('cloudbypass-sdk');
```

Or, if you're using ES modules:

```js
// Using ES6 imports
import cloudbypass from 'cloudbypass-sdk';
```

### Make a Request

After importing `cloudbypass-sdk`, you can use it similarly to `axios`.

The `config` parameter supports all `axios` request configurations, along with the following additional configurations:

- `cb_apikey`: API key;
- `cb_use_v2`: Use V2 mode, default is `false`;
- `cb_part`: Use V2 and enable part mode;
- `cb_proxy`: Proxy address, supports both http and socks5 proxies;
- `cb_apihost`: Custom users can use their own API server;

> The above parameters can be configured using environment variables `CB_APIKEY`, `CB_PROXY`, and `CB_APIHOST`.

```js
import cloudbypass from 'cloudbypass-sdk';
// Using Node.js `require()`
// const cloudbypass = require('cloudbypass-sdk'); 

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

Scrapingbypass API V2 is suitable for websites that need to pass JS challenge verification. For example, visit https://etherscan.io/accounts/label/lido and request an example:

```js
import cloudbypass from 'cloudbypass';
// Using Node.js `require()`
// const cloudbypass = require('cloudbypass');

// Cookie mode: The server returns an encrypted cookie, which is sent by the client for authentication in the next request.
try {
    const resp = (await cloudbypass.get("https://etherscan.io/accounts/label/lido", {
        cb_apikey: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        cb_proxy: 'http://proxy:port',
        cb_use_v2: true
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

// Part mode: The server manages the authentication cookie, and the client only needs to control the part parameter.
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
```

### Check balance

Use the `getBalance` method to query the current account balance.

```js
import cloudbypass from 'cloudbypass-sdk';
// Using Node.js `require()`
// const cloudbypass = require('cloudbypass-sdk');

cloudbypass.getBalance(/* APIKEY */).then(balance => {
    console.log(balance);
}).catch(err => {
    console.log(err);
})
```

### Extraction Proxy

The `cloudbypass.createProxy(auth: string)` method can be used to create a `CloudbypassProxy` instance, which can extract the cloud-piercing dynamic proxy IP and time-sensitive proxy IP.

+ `copy()` Duplicate the proxy instance so that the original proxy instance is not affected.
+ `setDynamic()` Set as dynamic proxy.
+ `setExpire(expire: number)` Set to time-limited proxy, the parameter is the IP expiration time, in seconds.
+ `setRegion(region: string)` Set the proxy IP region.
+ `clearRegion()` Clear the area of the agent.
+ `toString()` Returns the proxy IP string.
+ `format(format_str?: string)` Format proxy IP. The parameter is a formatted string, for example: `username:password@gateway`.
+ `limit(count: number, format_str?: string)` Returns a proxy IP string iterator, with the parameters being the extraction quantity and the proxy format string.
+ `loop(count: number, format_str?: string)` Returns a proxy IP string loop iterator, the parameters are the actual number and the proxy format string.

```js
import cloudbypass from 'cloudbypass-sdk';

const proxy = cloudbypass.createProxy("username-res:password");

// Extracting dynamic proxies
console.log("Extract dynamic proxy: ")
console.log(proxy.setDynamic().toString())
console.log(proxy.setRegion("US").toString())

// Extract time agent and specify region
console.log("Extract proxy with expire and region: ")
console.log(proxy.copy().setExpire(60 * 30).setRegion("US").toString())

// Batch Extraction
console.log("Extract five 10-minute aging proxies: ")
const pool = proxy.copy().setExpire(60 * 10).limit(5);
for (let p of pool) {
    console.log(p)
}

// Cycle Extraction
console.log("Loop two 10-minute aging proxies: ")
const loop = proxy.copy().setExpire(60 * 10).loop(2);
for (let i = 0; i < 10; i++) {
    console.log(loop.next().value)
}
```

### About Redirection Issues

When making requests with the SDK, redirection is automatically handled, and manual handling is not required. Redirect
responses will also consume credits.