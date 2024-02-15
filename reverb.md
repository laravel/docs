# Laravel Reverb

- [Introduction](#introduction)
- [Installation](#installation)
- [Running the Server](#running-server)
    - [Debugging](#debugging)
    - [Restarting](#restarting)
- [Configuration](#configuration)
    - [Credentials](#credentials)
    - [Allowed Origins](#allowed-origins)
    - [Additional Applications](#additional-applications)
    - [SSL](#ssl)
    - [Laravel Echo](#echo)
- [Running in Production](#production)
    - [Open Files](#open-files)
    - [Web Server](#web-server)
    - [Ports](#ports)
    - [Process Management](#process-management)
    - [Scaling](#scaling)

<a name="introduction"></a>
## Introduction

[Laravel Reverb](https://github.com/laravel/reverb) brings super-fast and scalable real-time communication directly to your Laravel application and provides seamless integration with Laravel’s existing suite of broadcasting tools.

<a name="installation"></a>
## Installation

> **Warning**  
> Laravel Reveb requires PHP 8.2+.

You may use the Composer package manager to install Reverb into your Laravel project. Since Reverb is currently in beta, you will need to explicitly install the beta version:

```sh
composer require laravel/reverb:@beta
```

Once the package is installed, you may run Reverb's installation command to publish the configuration, add the required environment variables and enable broadcasting in your application:

```sh
php artisan reverb:install
```

<a name="running-server"></a>
## Running the Server

The Reverb server can be started using the `reverb:start` Artisan command:

```sh
php artisan reverb:start
```

By default, the Reverb server will be started on port 8080 of host 0.0.0.0. This makes it accessible from all network interfaces.

Should you need to use a custom host or port, you may do so by utilizing the `host` and `port` options when starting the server:

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

<a name="restarting"></a>
### Restarting

Due to the long-running nature of the Reverb, updated code will not be reflected without restarting the server. Using the `reverb:restart` Artisan command ensures all connections are gracefully terminated before stopping the server. If you are running Reverb with a process manager such as Supervisor, the server will automatically restart after all connections have been terminated:

```sh
php artisan reverb:restart
```

<a name="configuration"></a>
## Configuration

The `reverb:install` command will automatically set up Reverb with a sensible set of default configuration options. Should you wish to make any advanced configuration changes, you may do so by updating Reverb's environment variables or `config/reverb.php` configuration file.

<a name="credentials"></a>
### Credentials

In order for a client to connect to a Reverb WebSocket server, a set of credentials must be exchanged. These credentials are configured on the server and are used to verify the request from the client. You may define these credentials with the following enviroment variables:

```
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
### Allowed Origins

You may also define the origins from which client requests may originate by updating the value of `allowed_origins` in Reverb's apps section of the `config/reverb.php` configuration file. Any requests from an origin not listed will be rejected. You may allow all origins with `*`.

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

Although typically Reverb will provide a WebSocket server for the application in which it is installed, it is possible to serve more than one application at a time. For example, you may wish to maintain a single server which provides WebSocket connectivity for multiple applications. This can be achieved by defining multiple `apps` in the `config/reverb.php` configuration file:

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

<a name="ssl"><a>
### SSL

In most cases, secure WebSocket connections are likely to be handled by the web server before the request is proxied your Reverb server. However, it can be useful, such as in local development, for the Reverb server to handle secure connections directly. You may achieve this by setting the `tls` options in the `config/reverb.php` configuration file. Here you may use any of the options available in the [PHP SSL context options](https://www.php.net/manual/en/context.ssl.php):

```php
...
'options' => [
    'tls' => [
        'local_cert' => '/path/to/cert.pem'
    ],
],
...
```

<a name="echo"></a>
### Laravel Echo

Laravel Echo is a library which makes it incredibly simple to interact with Pusher channels from your front-end code and it can be paired with Reverb with some minor tweaks to your configuration. To begin, you should ensure you have followed [Echo's installation instructions](broadcasting#client-pusher-channels) before setting the `VITE_REVERB_` prefixed environment variables:

```env
# Using Vite
VITE_REVERB_APP_KEY="${PUSHER_APP_KEY}"
VITE_REVERB_HOST="${PUSHER_HOST}"
VITE_REVERB_PORT="${PUSHER_PORT}"
VITE_REVERB_SCHEME="${PUSHER_SCHEME}"
```

You may now instantiate Echo with using the `reverb` broadcaster:

```javascript
window.Echo = new Echo({
    broadcaster: 'reverb',
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    wsHost: import.meta.env.VITE_PUSHER_HOST,
    wsPort: import.meta.env.VITE_PUSHER_PORT,
    wssPort: import.meta.env.VITE_PUSHER_PORT,
    forceTLS: (import.meta.env.VITE_PUSHER_SCHEME ?? 'https') === 'https',
    enabledTransports: ['ws', 'wss'],
})
```

After rebuilding your assets, your application's frontend should now be connected to your Reverb server.

<a name="production"></a>
## Running in Production

Due to the long-running nature of WebSockets, you may need to make some optimizations to your hosting environment to ensure your Reverb server can effectively handle the optimal number of connections for the resources available.

If you are hosting your application on a server provisioned by [Laravel Forge](https://forge.laravel.com), you may automatically configure your server for Reverb directly from the "Application" panel of your site.

<a name="open-files"></a>
### Open Files
Each WebSocket connection is held in memory until either the client or server disconnects. In Unix and Unix-like environments, each connection is represented by a file. There are often limits on the number of allowed open files at both the operating system and application level.

<a name="operating-system"></a>
#### Operating System

On a Unix based operating system, you make check the allowed number of open files using the `ulimit` command:

```sh
ulimit -n
```

The command will display the open file limits allowed for different users. You may update these values by editing the `/etc/security/limits.conf` file. For example, updating the maximum number of open files to 10,000 for the `forge` user would look like this:

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
#### Event Loop

Under the hood, Reverb uses a ReactPHP event loop to manage WebSocket connections on the server. By default, this event loop is powered by `stream_select` which doesn't require any additional extensions. However, `stream_select` is, depending on the platform, typically limited to 1,024 open files. As such, if you plan to handle more than one thousand concurrent connections, you will need to use an alternate event loop not bound to the same restrictions.

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

In most cases, Reverb runs on a non web-facing port on your server so in order to route traffic to it, you should configure a reverse proxy. Assuming Reverb is running on host `0.0.0.0` port `8080` and using an Nginx web server, this can be achieved by updating the config for the site:

```nginx
server {
    ...

    location / {
        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Scheme $scheme;
        proxy_set_header SERVER_PORT $server_port;
        proxy_set_header REMOTE_ADDR $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";

        proxy_pass http://0.0.0.0:8080;
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
  worker_connections 10000;
  multi_accept on;
}
```

The above configuration will allow up to 10,000 Nginx workers per process to be spawned and also set the open file limit for Nginx to 10,000.

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

You may wish to use a process manager such as Supervisor to ensure the Reverb server is continually running. You should update the `minfds` setting of your server's `supervisor.conf` file to ensure Supervisor is able to open the files required to handle the connections to your Reverb server. 

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
### Scaling

Should you need to handle more connections than a single server will allow, you may scale your Reverb server horizontally . Utilizing the publish / subscribe capabilities of Redis, Reverb is able to manage connections across multiple servers.

To enable horizontal scaling, you should set the `REVERB_SCALING_ENABLED` variable to true in your environment:

```env
REVERB_SCALING_ENABLED=true
```

In most cases, it makes sense to have a dedicated central Redis server to which all of the Reverb servers will communicate. Reverb will use the default Redis connection [configured in your application](/redis#configuration).

Each connection will persist with the server it originally connects with so traffic should be evenly distributed between Reverb servers using a load balancer. Any message which should be broadcast to other connections will be received by a single server - it doesn't matter which. That server will then publish an event to Redis which the other servers will consume and forward to the connections they manage.