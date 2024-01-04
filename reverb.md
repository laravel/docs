# Laravel Reverb

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
- [Running the Server](#running-server)
    - [Debugging](#debugging)
- [Pusher Protocol](#pusher-protocol)
    - [Credentials](#credentials)
    - [Allowed Origins](#allowed-origins)
    - [Additional Applications](#additional-applications)
    - [Laravel Echo](#echo)
- [Running in Production](#production)
    - [Open Files](#open-files)
    - [Web Server](#web-server)
    - [Ports](#ports)
    - [Process Management](#process-management)
    - [Scaling](#scaling)

<a name="introduction"></a>
## Introduction

[Laravel Reverb](https://github.com/laravel/reverb) brings super-fast and scalable real-time communication directly to your Laravel application. Reverb is a low-level WebSocket server built on top of [ReactPHP](https://reactphp.org/) and offers baked in support for the Pusher protocol providing seamless integration with Laravel’s existing suite of broadcasting tools.

<a name="installation"></a>
## Installation

> **Warning**  
> Laravel Reveb requires PHP 8.2+.

Since Reverb is currently in beta, you may need to adjust your application's composer.json file to allow beta package releases to be installed:

```json
"minimum-stability": "beta",
"prefer-stable": true
```

Then, you may use the Composer package manager to install Reverb into your Laravel project:

```sh
composer install laravel/reverb
```

<a name="configuration"></a>
### Configuration

Many of Reverbs's configuration options can be controlled using environment variables. To see the available options, or configure advanced options, you may publish the `config/reverb.php` configuration file:

```sh
php artisan vendor:publish --tag=reverb-config
```

<a name="running-server"></a>
## Running the Server

The Reverb server can be started via the `reverb:start` Artisan command:

```sh
php artisan reverb:start
```

By default, Reverb will start the server on localhost port 8080.

Should you need to use a custom host or port, you may do so by utilizing the `host` and `port` options when running the command:

```sh
php artisan reverb:start --host=127.0.0.1 --port=9000
```

Alternatively, you may set the `REVERB_HOST` and `REVERB_PORT` environment variables.

<a name="debugging"></a>
### Debugging

In order optimize for scale, Reverb will not write any debug information to the logs. If you wish to see the stream of data passing through your Reverb server, you may opt-in using the `--debug` option:

```sh
php artisan reverb:start --debug
```

<a name="pusher-protocol"></a>
## Pusher Protocol

Reverb provides near-parity with the [Pusher Channels Protocol](https://pusher.com/docs/channels/library_auth_reference/pusher-websockets-protocol/). Using Reverb in place of Pusher requires just some minor changes to your configuration.

To begin, you should ensure you have followed the instructions [outlined in the broadcasting documentation](broadcasting#pusher-channels) for integrating with Pusher Channels.

<a name="credentials"></a>
### Credentials

In order for a client to connect to a Reverb WebSocket server, a set of credentials must be exchanged. These credentials are configured on the server and are used to verify the request from the client. To achieve this, the following environment variables should be set using string values of your choosing. Additionally, the Pusher host, port and scheme should be updated to reflect those on which Reverb is running:

```
PUSHER_APP_ID=my-app-id
PUSHER_APP_KEY=my-app-key
PUSHER_APP_SECRET=my-app-secret
PUSHER_HOST=localhost
PUSHER_PORT=8080
PUSHER_SCHEME=http
```

> **Warning**  
> The `PUSHER_APP_CLUSTER` environment variable is not required with Reverb and should be removed from your environment file to avoid connection issues.

<a name="allowed-origins"></a>
### Allowed Origins

You may also define the origins from which client requests may originate by updating the value of `allowed_origins` in Reverb's app configuration. Any requests from an origin not listed will be rejected. You may allow all origins with `*`.

```php
'apps' => [
    [
        'id' => 'my-app-one',
        'allowed_origins' => ['laravel.com'],
        ...
    ]
]
```

<a name="additional-applications"></a>
### Additional Applications

Although typically Reverb will provide a WebSocket server for the application in which it is installed, it is possible to serve more than one application at a time. For example, you may wish to maintain a single server which provides WebSockets for multiple applications. This can be achieved by defining multiple `apps` in the Reverb configuration file:

```php
'apps' => [
    [
        'id' => 'my-app-one',
        ...
    ],
    [
        'id' => 'my-app-two',
        ...
    ],
],
```

<a name="echo"></a>
### Laravel Echo

Laravel Echo is a library which makes it incredibly simple to interact with Pusher channels from your front-end code and it can be paired with Reverb with some minor tweaks to your configuration. To begin, you should ensure you have followed [Echo's installation instructions](broadcasting#client-pusher-channels) for Pusher Channels before updating your `VITE_` or `MIX_` prefixed Pusher environment variables:

```env
# Using Vite
VITE_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
VITE_PUSHER_HOST="${PUSHER_HOST}"
VITE_PUSHER_PORT="${PUSHER_PORT}"
VITE_PUSHER_SCHEME="${PUSHER_SCHEME}"
VITE_PUSHER_APP_CLUSTER=

# Using Mix
MIX_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
MIX_PUSHER_HOST="${PUSHER_HOST}"
MIX_PUSHER_PORT="${PUSHER_PORT}"
MIX_PUSHER_SCHEME="${PUSHER_SCHEME}"
MIX_PUSHER_APP_CLUSTER=
```

> **Note**  
> Although not used, the `VITE_PUSHER_APP_CLUSTER` environment variable is required by the Pusher JavaScript SDK. As such, it should be present in your environment file, but left empty.

Now you may update the intialization of Echo accordingly. In a default Laravel installation, this takes place in the `resources/js/bootstrap.js` file:

```javascript
window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    wsHost: import.meta.env.VITE_PUSHER_HOST,
    wsPort: import.meta.env.VITE_PUSHER_PORT,
    wssPort: import.meta.env.VITE_PUSHER_PORT,
    forceTLS: (import.meta.env.VITE_PUSHER_SCHEME ?? 'https') === 'https',
    enabledTransports: ['ws', 'wss'],
})
```

After rebuilding your assets, your frontend should now be connected to your Reverb server.

<a name="production"></a>
## Running in Production

Due to the long-running nature of WebSockets, you may need to make some optimizations to your hosting environment to ensure your Reverb server can effectively handle the optimal number of connections for the available resources. If you are hosting your application on a server provisioned by [Laravel Forge](https://forge.laravel.com), you may automatically optimize your server for Reverb directly from the "Application" panel of your site.

<a name="open-files"></a>
### Open Files
Each WebSocket connection is held in memory until either the client or server disconnects. In Unix and Unix-like environments, each connection is represented by a file. There are often limits on the number of allowed open files at both the operating system and application level which is typically 1,024 open files.

<a name="operating-system"></a>
#### Operating System

On a Unix based operating system, you make check the allowed number of open files using the `ulimit` command:

```sh
ulimit -n
```

The command will display both the soft limit where errors start to be logged and hard limit where requests to open files are refused. You may update these values by editing the `/etc/security/limits.conf` file. For example, updating the maximum number of open files to 10,000 for the `forge` user would look like this:

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
#### Event Loop

Under the hood, Reverb uses a ReactPHP event loop to manage WebSocket connections on the server. By default, this event loop is powered by `stream_select` which doesn't require any additional extensions. However, `stream_select` is, depending on the platform, typically limited to 1,024 open files. As such, if you plan to handle more than one thousand concurrent connections, you will need to use an alternative event loop not bound to the same restrictions.

Reverb will automatically switch to an `ext-event`, `ext-ev`, or `ext-uv` powered loop when available. All of the extensions are available for install via PECL:

```sh
pecl install event
# or
pecl install ev
# or
pecl install uv
```

<a name="web-server"></a>
### Web Server

In most cases, Reverb runs on a non web-facing port on your server so in order to route traffic to it, you should configure a reverse proxy. Assuming Reverb is running on host `127.0.0.1` port `8080` and using an Nginx web server, this can be achieved by updating the config for the site:

```nginx
server {
    ...

    location / {
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:8080;
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }

    ...
```

Typically, web servers are configured to limit the number of allowed connections in order to prevent overloading the server. To increase the number of allowed connections on an Nginx web server to 10,000, the `worker_rlimit_nofile` and `worker_connections` values of the `nginx.conf` file should be updated:

```nginx
user forge;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;
worker_rlimit_nofile 10000;

events {
  worker_connections 20000;
  multi_accept on;
}
```

The above configuration will allow up to 10,000 Nginx workers to be spawned and also set the open file limit for Nginx to 10,000.

<a name="ports"></a>
### Ports

Unix-based operating systems typically limit the number of ports which can be opened on the server. You may see the current allowed range by running:

 ```sh
 cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

The output above shows the server can handle a maximum of 28,231 (60,999 - 32,768) connections as each connection requires a free port. Although we would recommend [horizontal scaling](#scaling) to increase the number of allowed connections, should you wish to increase the number of open ports, you may do so by updating the allowed range in your server's `/etc/sysctl.conf` file.

<a name="process-management"></a>
### Process Management

You may wish to use a process manager such as Supervisor to ensure the Reverb server is continually running. You should update the `minfds` setting of your Supervisor configuration to ensure the Supervisor user is able to open the files required to handle the connections to your Reverb server. 

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
### Scaling

You may scale your Reverb server horizontally should you need to handle more connections than a single server will allow. Utilizing the publish / subscribe capabilities of Redis, Reverb is able to manage connections across multiple servers.

To enable horizontal scaling, you should set the `REVERB_SCALING_ENABLED` variable to true in your environment:

```env
REVERB_SCALING_ENABLED=true
```

In most cases, it makes sense to have a dedicated central Redis server to which all of the Reverb servers will communicate. Reverb will use the default Redis connection [configured in your application](/redis#configuration).

Each connection will persist with the server it originally connects with so traffic should be evenly distributed between Reverb servers using a load balancer. Any message which should be broadcast to other connections will be received by a single server - it doesn't matter which. That server will then publish an event to Redis which the other servers will consume and broadcast to the connections they manage.