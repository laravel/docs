# Broadcasting

- [Introduction](#introduction)
- [Quickstart](#quickstart)
- [Server Side Installation](#server-side-installation)
    - [Reverb](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
- [Client Side Installation](#client-side-installation)
    - [Reverb](#client-reverb)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
- [Concept Overview](#concept-overview)
    - [Using an Example Application](#using-example-application)
- [Defining Broadcast Events](#defining-broadcast-events)
    - [Broadcast Name](#broadcast-name)
    - [Broadcast Data](#broadcast-data)
    - [Broadcast Queue](#broadcast-queue)
    - [Broadcast Conditions](#broadcast-conditions)
    - [Broadcasting and Database Transactions](#broadcasting-and-database-transactions)
- [Authorizing Channels](#authorizing-channels)
    - [Defining Authorization Callbacks](#defining-authorization-callbacks)
    - [Defining Channel Classes](#defining-channel-classes)
- [Broadcasting Events](#broadcasting-events)
    - [Only to Others](#only-to-others)
    - [Customizing the Connection](#customizing-the-connection)
    - [Anonymous Events](#anonymous-events)
    - [Rescuing Broadcasts](#rescuing-broadcasts)
- [Receiving Broadcasts](#receiving-broadcasts)
    - [Listening for Events](#listening-for-events)
    - [Leaving a Channel](#leaving-a-channel)
    - [Namespaces](#namespaces)
    - [Using React or Vue](#using-react-or-vue)
- [Presence Channels](#presence-channels)
    - [Authorizing Presence Channels](#authorizing-presence-channels)
    - [Joining Presence Channels](#joining-presence-channels)
    - [Broadcasting to Presence Channels](#broadcasting-to-presence-channels)
- [Model Broadcasting](#model-broadcasting)
    - [Model Broadcasting Conventions](#model-broadcasting-conventions)
    - [Listening for Model Broadcasts](#listening-for-model-broadcasts)
- [Client Events](#client-events)
- [Notifications](#notifications)

<a name="introduction"></a>
## Introduction

In many modern web applications, WebSockets are used to implement realtime, live-updating user interfaces. When some data is updated on the server, a message is typically sent over a WebSocket connection to be handled by the client. WebSockets provide a more efficient alternative to continually polling your application's server for data changes that should be reflected in your UI.

For example, imagine your application is able to export a user's data to a CSV file and email it to them. However, creating this CSV file takes several minutes so you choose to create and mail the CSV within a [queued job](/docs/{{version}}/queues). When the CSV has been created and mailed to the user, we can use event broadcasting to dispatch an `App\Events\UserDataExported` event that is received by our application's JavaScript. Once the event is received, we can display a message to the user that their CSV has been emailed to them without them ever needing to refresh the page.

To assist you in building these types of features, Laravel makes it easy to "broadcast" your server-side Laravel [events](/docs/{{version}}/events) over a WebSocket connection. Broadcasting your Laravel events allows you to share the same event names and data between your server-side Laravel application and your client-side JavaScript application.

The core concepts behind broadcasting are simple: clients connect to named channels on the frontend, while your Laravel application broadcasts events to these channels on the backend. These events can contain any additional data you wish to make available to the frontend.

<a name="supported-drivers"></a>
#### Supported Drivers

By default, Laravel includes three server-side broadcasting drivers for you to choose from: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), and [Ably](https://ably.com).

> [!NOTE]
> Before diving into event broadcasting, make sure you have read Laravel's documentation on [events and listeners](/docs/{{version}}/events).

<a name="quickstart"></a>
## Quickstart

By default, broadcasting is not enabled in new Laravel applications. You may enable broadcasting using the `install:broadcasting` Artisan command:

```shell
php artisan install:broadcasting
```

The `install:broadcasting` command with prompt you for which event broadcasting service you would like to use. In addition, it will create the `config/broadcasting.php` configuration file and the `routes/channels.php` file where you may register your application's broadcast authorization routes and callbacks.

Laravel supports several broadcast drivers out of the box: [Laravel Reverb](/docs/{{version}}/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), and a `log` driver for local development and debugging. Additionally, a `null` driver is included which allows you to disable broadcasting during testing. A configuration example is included for each of these drivers in the `config/broadcasting.php` configuration file.

All of your application's event broadcasting configuration is stored in the `config/broadcasting.php` configuration file. Don't worry if this file does not exist in your application; it will be created when you run the `install:broadcasting` Artisan command.

<a name="quickstart-next-steps"></a>
#### Next Steps

Once you have enabled event broadcasting, you're ready to learn more about [defining broadcast events](#defining-broadcast-events) and [listening for events](#listening-for-events). If you're using Laravel's React or Vue [starter kits](/docs/{{version}}/starter-kits), you may listen for events using Echo's [useEcho hook](#using-react-or-vue).

> [!NOTE]
> Before broadcasting any events, you should first configure and run a [queue worker](/docs/{{version}}/queues). All event broadcasting is done via queued jobs so that the response time of your application is not seriously affected by events being broadcast.

<a name="server-side-installation"></a>
## Server Side Installation

To get started using Laravel's event broadcasting, we need to do some configuration within the Laravel application as well as install a few packages.

Event broadcasting is accomplished by a server-side broadcasting driver that broadcasts your Laravel events so that Laravel Echo (a JavaScript library) can receive them within the browser client. Don't worry - we'll walk through each part of the installation process step-by-step.

<a name="reverb"></a>
### Reverb

To quickly enable support for Laravel's broadcasting features while using Reverb as your event broadcaster, invoke the `install:broadcasting` Artisan command with the `--reverb` option. This Artisan command will install Reverb's required Composer and NPM packages and update your application's `.env` file with the appropriate variables:

```shell
php artisan install:broadcasting --reverb
```

<a name="reverb-manual-installation"></a>
#### Manual Installation

When running the `install:broadcasting` command, you will be prompted to install [Laravel Reverb](/docs/{{version}}/reverb). Of course, you may also install Reverb manually using the Composer package manager:

```shell
composer require laravel/reverb
```

Once the package is installed, you may run Reverb's installation command to publish the configuration, add Reverb's required environment variables, and enable event broadcasting in your application:

```shell
php artisan reverb:install
```

You can find detailed Reverb installation and usage instructions in the [Reverb documentation](/docs/{{version}}/reverb).

<a name="pusher-channels"></a>
### Pusher Channels

To quickly enable support for Laravel's broadcasting features while using Pusher as your event broadcaster, invoke the `install:broadcasting` Artisan command with the `--pusher` option. This Artisan command will prompt you for your Pusher credentials, install the Pusher PHP and JavaScript SDKs, and update your application's `.env` file with the appropriate variables:

```shell
php artisan install:broadcasting --pusher
```

<a name="pusher-manual-installation"></a>
#### Manual Installation

To install Pusher support manually, you should install the Pusher Channels PHP SDK using the Composer package manager:

```shell
composer require pusher/pusher-php-server
```

Next, you should configure your Pusher Channels credentials in the `config/broadcasting.php` configuration file. An example Pusher Channels configuration is already included in this file, allowing you to quickly specify your key, secret, and application ID. Typically, you should configure your Pusher Channels credentials in your application's `.env` file:

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

The `config/broadcasting.php` file's `pusher` configuration also allows you to specify additional `options` that are supported by Channels, such as the cluster.

Then, set the `BROADCAST_CONNECTION` environment variable to `pusher` in your application's `.env` file:

```ini
BROADCAST_CONNECTION=pusher
```

Finally, you are ready to install and configure [Laravel Echo](#client-side-installation), which will receive the broadcast events on the client-side.

<a name="ably"></a>
### Ably

> [!NOTE]
> The documentation below discusses how to use Ably in "Pusher compatibility" mode. However, the Ably team recommends and maintains a broadcaster and Echo client that is able to take advantage of the unique capabilities offered by Ably. For more information on using the Ably maintained drivers, please [consult Ably's Laravel broadcaster documentation](https://github.com/ably/laravel-broadcaster).

To quickly enable support for Laravel's broadcasting features while using [Ably](https://ably.com) as your event broadcaster, invoke the `install:broadcasting` Artisan command with the `--ably` option. This Artisan command will prompt you for your Ably credentials, install the Ably PHP and JavaScript SDKs, and update your application's `.env` file with the appropriate variables:

```shell
php artisan install:broadcasting --ably
```

**Before continuing, you should enable Pusher protocol support in your Ably application settings. You may enable this feature within the "Protocol Adapter Settings" portion of your Ably application's settings dashboard.**

<a name="ably-manual-installation"></a>
#### Manual Installation

To install Ably support manually, you should install the Ably PHP SDK using the Composer package manager:

```shell
composer require ably/ably-php
```

Next, you should configure your Ably credentials in the `config/broadcasting.php` configuration file. An example Ably configuration is already included in this file, allowing you to quickly specify your key. Typically, this value should be set via the `ABLY_KEY` [environment variable](/docs/{{version}}/configuration#environment-configuration):

```ini
ABLY_KEY=your-ably-key
```

Then, set the `BROADCAST_CONNECTION` environment variable to `ably` in your application's `.env` file:

```ini
BROADCAST_CONNECTION=ably
```

Finally, you are ready to install and configure [Laravel Echo](#client-side-installation), which will receive the broadcast events on the client-side.

<a name="client-side-installation"></a>
## Client Side Installation

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver.

When installing Laravel Reverb via the `install:broadcasting` Artisan command, Reverb and Echo's scaffolding and configuration will be injected into your application automatically. However, if you wish to manually configure Laravel Echo, you may do so by following the instructions below.

<a name="reverb-client-manual-installation"></a>
#### Manual Installation

To manually configure Laravel Echo for your application's frontend, first install the `pusher-js` package since Reverb utilizes the Pusher protocol for WebSocket subscriptions, channels, and messages:

```shell
npm install --save-dev laravel-echo pusher-js
```

Once Echo is installed, you are ready to create a fresh Echo instance in your application's JavaScript. A great place to do this is at the bottom of the `resources/js/bootstrap.js` file that is included with the Laravel framework:

```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'reverb',
    key: import.meta.env.VITE_REVERB_APP_KEY,
    wsHost: import.meta.env.VITE_REVERB_HOST,
    wsPort: import.meta.env.VITE_REVERB_PORT ?? 80,
    wssPort: import.meta.env.VITE_REVERB_PORT ?? 443,
    forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    enabledTransports: ['ws', 'wss'],
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "reverb",
    // key: import.meta.env.VITE_REVERB_APP_KEY,
    // wsHost: import.meta.env.VITE_REVERB_HOST,
    // wsPort: import.meta.env.VITE_REVERB_PORT,
    // wssPort: import.meta.env.VITE_REVERB_PORT,
    // forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    // enabledTransports: ['ws', 'wss'],
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "reverb",
    // key: import.meta.env.VITE_REVERB_APP_KEY,
    // wsHost: import.meta.env.VITE_REVERB_HOST,
    // wsPort: import.meta.env.VITE_REVERB_PORT,
    // wssPort: import.meta.env.VITE_REVERB_PORT,
    // forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    // enabledTransports: ['ws', 'wss'],
});
```

Next, you should compile your application's assets:

```shell
npm run build
```

> [!WARNING]
> The Laravel Echo `reverb` broadcaster requires laravel-echo v1.16.0+.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver.

When installing broadcasting support via the `install:broadcasting --pusher` Artisan command, Pusher and Echo's scaffolding and configuration will be injected into your application automatically. However, if you wish to manually configure Laravel Echo, you may do so by following the instructions below.

<a name="pusher-client-manual-installation"></a>
#### Manual Installation

To manually configure Laravel Echo for your application's frontend, first install the `laravel-echo` and `pusher-js` packages which utilize the Pusher protocol for WebSocket subscriptions, channels, and messages:

```shell
npm install --save-dev laravel-echo pusher-js
```

Once Echo is installed, you are ready to create a fresh Echo instance in your application's `resources/js/bootstrap.js` file:

```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    forceTLS: true
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "pusher",
    // key: import.meta.env.VITE_PUSHER_APP_KEY,
    // cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    // forceTLS: true,
    // wsHost: import.meta.env.VITE_PUSHER_HOST,
    // wsPort: import.meta.env.VITE_PUSHER_PORT,
    // wssPort: import.meta.env.VITE_PUSHER_PORT,
    // enabledTransports: ["ws", "wss"],
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "pusher",
    // key: import.meta.env.VITE_PUSHER_APP_KEY,
    // cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    // forceTLS: true,
    // wsHost: import.meta.env.VITE_PUSHER_HOST,
    // wsPort: import.meta.env.VITE_PUSHER_PORT,
    // wssPort: import.meta.env.VITE_PUSHER_PORT,
    // enabledTransports: ["ws", "wss"],
});
```

Next, you should define the appropriate values for the Pusher environment variables in your application's `.env` file. If these variables do not already exist in your `.env` file, you should add them:

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"

VITE_APP_NAME="${APP_NAME}"
VITE_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
VITE_PUSHER_HOST="${PUSHER_HOST}"
VITE_PUSHER_PORT="${PUSHER_PORT}"
VITE_PUSHER_SCHEME="${PUSHER_SCHEME}"
VITE_PUSHER_APP_CLUSTER="${PUSHER_APP_CLUSTER}"
```

Once you have adjusted the Echo configuration according to your application's needs, you may compile your application's assets:

```shell
npm run build
```

> [!NOTE]
> To learn more about compiling your application's JavaScript assets, please consult the documentation on [Vite](/docs/{{version}}/vite).

<a name="using-an-existing-client-instance"></a>
#### Using an Existing Client Instance

If you already have a pre-configured Pusher Channels client instance that you would like Echo to utilize, you may pass it to Echo via the `client` configuration option:

```js
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

const options = {
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY
}

window.Echo = new Echo({
    ...options,
    client: new Pusher(options.key, options)
});
```

<a name="client-ably"></a>
### Ably

> [!NOTE]
> The documentation below discusses how to use Ably in "Pusher compatibility" mode. However, the Ably team recommends and maintains a broadcaster and Echo client that is able to take advantage of the unique capabilities offered by Ably. For more information on using the Ably maintained drivers, please [consult Ably's Laravel broadcaster documentation](https://github.com/ably/laravel-broadcaster).

[Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver.

When installing broadcasting support via the `install:broadcasting --ably` Artisan command, Ably and Echo's scaffolding and configuration will be injected into your application automatically. However, if you wish to manually configure Laravel Echo, you may do so by following the instructions below.

<a name="ably-client-manual-installation"></a>
#### Manual Installation

To manually configure Laravel Echo for your application's frontend, first install the `laravel-echo` and `pusher-js` packages which utilize the Pusher protocol for WebSocket subscriptions, channels, and messages:

```shell
npm install --save-dev laravel-echo pusher-js
```

**Before continuing, you should enable Pusher protocol support in your Ably application settings. You may enable this feature within the "Protocol Adapter Settings" portion of your Ably application's settings dashboard.**

Once Echo is installed, you are ready to create a fresh Echo instance in your application's `resources/js/bootstrap.js` file:

```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    wsHost: 'realtime-pusher.ably.io',
    wsPort: 443,
    disableStats: true,
    encrypted: true,
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```

You may have noticed our Ably Echo configuration references a `VITE_ABLY_PUBLIC_KEY` environment variable. This variable's value should be your Ably public key. Your public key is the portion of your Ably key that occurs before the `:` character.

Once you have adjusted the Echo configuration according to your needs, you may compile your application's assets:

```shell
npm run dev
```

> [!NOTE]
> To learn more about compiling your application's JavaScript assets, please consult the documentation on [Vite](/docs/{{version}}/vite).

<a name="concept-overview"></a>
## Concept Overview

Laravel's event broadcasting allows you to broadcast your server-side Laravel events to your client-side JavaScript application using a driver-based approach to WebSockets. Currently, Laravel ships with [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), and [Ably](https://ably.com) drivers. The events may be easily consumed on the client-side using the [Laravel Echo](#client-side-installation) JavaScript package.

Events are broadcast over "channels", which may be specified as public or private. Any visitor to your application may subscribe to a public channel without any authentication or authorization; however, in order to subscribe to a private channel, a user must be authenticated and authorized to listen on that channel.

<a name="using-example-application"></a>
### Using an Example Application

Before diving into each component of event broadcasting, let's take a high level overview using an e-commerce store as an example.

In our application, let's assume we have a page that allows users to view the shipping status for their orders. Let's also assume that an `OrderShipmentStatusUpdated` event is fired when a shipping status update is processed by the application:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### The `ShouldBroadcast` Interface

When a user is viewing one of their orders, we don't want them to have to refresh the page to view status updates. Instead, we want to broadcast the updates to the application as they are created. So, we need to mark the `OrderShipmentStatusUpdated` event with the `ShouldBroadcast` interface. This will instruct Laravel to broadcast the event when it is fired:

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class OrderShipmentStatusUpdated implements ShouldBroadcast
{
    /**
     * The order instance.
     *
     * @var \App\Models\Order
     */
    public $order;
}
```

The `ShouldBroadcast` interface requires our event to define a `broadcastOn` method. This method is responsible for returning the channels that the event should broadcast on. An empty stub of this method is already defined on generated event classes, so we only need to fill in its details. We only want the creator of the order to be able to view status updates, so we will broadcast the event on a private channel that is tied to the order:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channel the event should broadcast on.
 */
public function broadcastOn(): Channel
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

If you wish the event to broadcast on multiple channels, you may return an `array` instead:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channels the event should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(): array
{
    return [
        new PrivateChannel('orders.'.$this->order->id),
        // ...
    ];
}
```

<a name="example-application-authorizing-channels"></a>
#### Authorizing Channels

Remember, users must be authorized to listen on private channels. We may define our channel authorization rules in our application's `routes/channels.php` file. In this example, we need to verify that any user attempting to listen on the private `orders.1` channel is actually the creator of the order:

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

The `channel` method accepts two arguments: the name of the channel and a callback which returns `true` or `false` indicating whether the user is authorized to listen on the channel.

All authorization callbacks receive the currently authenticated user as their first argument and any additional wildcard parameters as their subsequent arguments. In this example, we are using the `{orderId}` placeholder to indicate that the "ID" portion of the channel name is a wildcard.

<a name="listening-for-event-broadcasts"></a>
#### Listening for Event Broadcasts

Next, all that remains is to listen for the event in our JavaScript application. We can do this using [Laravel Echo](#client-side-installation). Laravel Echo's built-in React and Vue hooks make it simple to get started, and, by default, all of the event's public properties will be included on the broadcast event:

```js tab=React
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

<a name="defining-broadcast-events"></a>
## Defining Broadcast Events

To inform Laravel that a given event should be broadcast, you must implement the `Illuminate\Contracts\Broadcasting\ShouldBroadcast` interface on the event class. This interface is already imported into all event classes generated by the framework so you may easily add it to any of your events.

The `ShouldBroadcast` interface requires you to implement a single method: `broadcastOn`. The `broadcastOn` method should return a channel or array of channels that the event should broadcast on. The channels should be instances of `Channel`, `PrivateChannel`, or `PresenceChannel`. Instances of `Channel` represent public channels that any user may subscribe to, while `PrivateChannels` and `PresenceChannels` represent private channels that require [channel authorization](#authorizing-channels):

```php
<?php

namespace App\Events;

use App\Models\User;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class ServerCreated implements ShouldBroadcast
{
    use SerializesModels;

    /**
     * Create a new event instance.
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * Get the channels the event should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel>
     */
    public function broadcastOn(): array
    {
        return [
            new PrivateChannel('user.'.$this->user->id),
        ];
    }
}
```

After implementing the `ShouldBroadcast` interface, you only need to [fire the event](/docs/{{version}}/events) as you normally would. Once the event has been fired, a [queued job](/docs/{{version}}/queues) will automatically broadcast the event using your specified broadcast driver.

<a name="broadcast-name"></a>
### Broadcast Name

By default, Laravel will broadcast the event using the event's class name. However, you may customize the broadcast name by defining a `broadcastAs` method on the event:

```php
/**
 * The event's broadcast name.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

If you customize the broadcast name using the `broadcastAs` method, you should make sure to register your listener with a leading `.` character. This will instruct Echo to not prepend the application's namespace to the event:

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
### Broadcast Data

When an event is broadcast, all of its `public` properties are automatically serialized and broadcast as the event's payload, allowing you to access any of its public data from your JavaScript application. So, for example, if your event has a single public `$user` property that contains an Eloquent model, the event's broadcast payload would be:

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

However, if you wish to have more fine-grained control over your broadcast payload, you may add a `broadcastWith` method to your event. This method should return the array of data that you wish to broadcast as the event payload:

```php
/**
 * Get the data to broadcast.
 *
 * @return array<string, mixed>
 */
public function broadcastWith(): array
{
    return ['id' => $this->user->id];
}
```

<a name="broadcast-queue"></a>
### Broadcast Queue

By default, each broadcast event is placed on the default queue for the default queue connection specified in your `queue.php` configuration file. You may customize the queue connection and name used by the broadcaster by defining `connection` and `queue` properties on your event class:

```php
/**
 * The name of the queue connection to use when broadcasting the event.
 *
 * @var string
 */
public $connection = 'redis';

/**
 * The name of the queue on which to place the broadcasting job.
 *
 * @var string
 */
public $queue = 'default';
```

Alternatively, you may customize the queue name by defining a `broadcastQueue` method on your event:

```php
/**
 * The name of the queue on which to place the broadcasting job.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

If you would like to broadcast your event using the `sync` queue instead of the default queue driver, you can implement the `ShouldBroadcastNow` interface instead of `ShouldBroadcast`:

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

class OrderShipmentStatusUpdated implements ShouldBroadcastNow
{
    // ...
}
```

<a name="broadcast-conditions"></a>
### Broadcast Conditions

Sometimes you want to broadcast your event only if a given condition is true. You may define these conditions by adding a `broadcastWhen` method to your event class:

```php
/**
 * Determine if this event should broadcast.
 */
public function broadcastWhen(): bool
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>
#### Broadcasting and Database Transactions

When broadcast events are dispatched within database transactions, they may be processed by the queue before the database transaction has committed. When this happens, any updates you have made to models or database records during the database transaction may not yet be reflected in the database. In addition, any models or database records created within the transaction may not exist in the database. If your event depends on these models, unexpected errors can occur when the job that broadcasts the event is processed.

If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular broadcast event should be dispatched after all open database transactions have been committed by implementing the `ShouldDispatchAfterCommit` interface on the event class:

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Contracts\Events\ShouldDispatchAfterCommit;
use Illuminate\Queue\SerializesModels;

class ServerCreated implements ShouldBroadcast, ShouldDispatchAfterCommit
{
    use SerializesModels;
}
```

> [!NOTE]
> To learn more about working around these issues, please review the documentation regarding [queued jobs and database transactions](/docs/{{version}}/queues#jobs-and-database-transactions).

<a name="authorizing-channels"></a>
## Authorizing Channels

Private channels require you to authorize that the currently authenticated user can actually listen on the channel. This is accomplished by making an HTTP request to your Laravel application with the channel name and allowing your application to determine if the user can listen on that channel. When using [Laravel Echo](#client-side-installation), the HTTP request to authorize subscriptions to private channels will be made automatically.

When broadcasting is enabled, Laravel automatically registers the `/broadcasting/auth` route to handle authorization requests. The `/broadcasting/auth` route is automatically placed within the `web` middleware group.

<a name="defining-authorization-callbacks"></a>
### Defining Authorization Callbacks

Next, we need to define the logic that will actually determine if the currently authenticated user can listen to a given channel. This is done in the `routes/channels.php` file that was created by the `install:broadcasting` Artisan command. In this file, you may use the `Broadcast::channel` method to register channel authorization callbacks:

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

The `channel` method accepts two arguments: the name of the channel and a callback which returns `true` or `false` indicating whether the user is authorized to listen on the channel.

All authorization callbacks receive the currently authenticated user as their first argument and any additional wildcard parameters as their subsequent arguments. In this example, we are using the `{orderId}` placeholder to indicate that the "ID" portion of the channel name is a wildcard.

You may view a list of your application's broadcast authorization callbacks using the `channel:list` Artisan command:

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### Authorization Callback Model Binding

Just like HTTP routes, channel routes may also take advantage of implicit and explicit [route model binding](/docs/{{version}}/routing#route-model-binding). For example, instead of receiving a string or numeric order ID, you may request an actual `Order` model instance:

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> Unlike HTTP route model binding, channel model binding does not support automatic [implicit model binding scoping](/docs/{{version}}/routing#implicit-model-binding-scoping). However, this is rarely a problem because most channels can be scoped based on a single model's unique, primary key.

<a name="authorization-callback-authentication"></a>
#### Authorization Callback Authentication

Private and presence broadcast channels authenticate the current user via your application's default authentication guard. If the user is not authenticated, channel authorization is automatically denied and the authorization callback is never executed. However, you may assign multiple, custom guards that should authenticate the incoming request if necessary:

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### Defining Channel Classes

If your application is consuming many different channels, your `routes/channels.php` file could become bulky. So, instead of using closures to authorize channels, you may use channel classes. To generate a channel class, use the `make:channel` Artisan command. This command will place a new channel class in the `App/Broadcasting` directory.

```shell
php artisan make:channel OrderChannel
```

Next, register your channel in your `routes/channels.php` file:

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

Finally, you may place the authorization logic for your channel in the channel class' `join` method. This `join` method will house the same logic you would have typically placed in your channel authorization closure. You may also take advantage of channel model binding:

```php
<?php

namespace App\Broadcasting;

use App\Models\Order;
use App\Models\User;

class OrderChannel
{
    /**
     * Create a new channel instance.
     */
    public function __construct() {}

    /**
     * Authenticate the user's access to the channel.
     */
    public function join(User $user, Order $order): array|bool
    {
        return $user->id === $order->user_id;
    }
}
```

> [!NOTE]
> Like many other classes in Laravel, channel classes will automatically be resolved by the [service container](/docs/{{version}}/container). So, you may type-hint any dependencies required by your channel in its constructor.

<a name="broadcasting-events"></a>
## Broadcasting Events

Once you have defined an event and marked it with the `ShouldBroadcast` interface, you only need to fire the event using the event's dispatch method. The event dispatcher will notice that the event is marked with the `ShouldBroadcast` interface and will queue the event for broadcasting:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### Only to Others

When building an application that utilizes event broadcasting, you may occasionally need to broadcast an event to all subscribers to a given channel except for the current user. You may accomplish this using the `broadcast` helper and the `toOthers` method:

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

To better understand when you may want to use the `toOthers` method, let's imagine a task list application where a user may create a new task by entering a task name. To create a task, your application might make a request to a `/task` URL which broadcasts the task's creation and returns a JSON representation of the new task. When your JavaScript application receives the response from the end-point, it might directly insert the new task into its task list like so:

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

However, remember that we also broadcast the task's creation. If your JavaScript application is also listening for this event in order to add tasks to the task list, you will have duplicate tasks in your list: one from the end-point and one from the broadcast. You may solve this by using the `toOthers` method to instruct the broadcaster to not broadcast the event to the current user.

> [!WARNING]
> Your event must use the `Illuminate\Broadcasting\InteractsWithSockets` trait in order to call the `toOthers` method.

<a name="only-to-others-configuration"></a>
#### Configuration

When you initialize a Laravel Echo instance, a socket ID is assigned to the connection. If you are using a global [Axios](https://github.com/axios/axios) instance to make HTTP requests from your JavaScript application, the socket ID will automatically be attached to every outgoing request as an `X-Socket-ID` header. Then, when you call the `toOthers` method, Laravel will extract the socket ID from the header and instruct the broadcaster to not broadcast to any connections with that socket ID.

If you are not using a global Axios instance, you will need to manually configure your JavaScript application to send the `X-Socket-ID` header with all outgoing requests. You may retrieve the socket ID using the `Echo.socketId` method:

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### Customizing the Connection

If your application interacts with multiple broadcast connections and you want to broadcast an event using a broadcaster other than your default, you may specify which connection to push an event to using the `via` method:

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

Alternatively, you may specify the event's broadcast connection by calling the `broadcastVia` method within the event's constructor. However, before doing so, you should ensure that the event class uses the `InteractsWithBroadcasting` trait:

```php
<?php

namespace App\Events;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithBroadcasting;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class OrderShipmentStatusUpdated implements ShouldBroadcast
{
    use InteractsWithBroadcasting;

    /**
     * Create a new event instance.
     */
    public function __construct()
    {
        $this->broadcastVia('pusher');
    }
}
```

<a name="anonymous-events"></a>
### Anonymous Events

Sometimes, you may want to broadcast a simple event to your application's frontend without creating a dedicated event class. To accommodate this, the `Broadcast` facade allows you to broadcast "anonymous events":

```php
Broadcast::on('orders.'.$order->id)->send();
```

The example above will broadcast the following event:

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

Using the `as` and `with` methods, you may customize the event's name and data:

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

The example above will broadcast an event like the following:

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

If you would like to broadcast the anonymous event on a private or presence channel, you may utilize the `private` and `presence` methods:

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

Broadcasting an anonymous event using the `send` method dispatches the event to your application's [queue](/docs/{{version}}/queues) for processing. However, if you would like to broadcast the event immediately, you may use the `sendNow` method:

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

To broadcast the event to all channel subscribers except the currently authenticated user, you can invoke the `toOthers` method:

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="rescuing-broadcasts"></a>
### Rescuing Broadcasts

When your application's queue server is unavailable or Laravel encounters an error while broadcasting an event, an exception is thrown that typically causes the end user to see an application error. Since event broadcasting is often supplementary to your application's core functionality, you can prevent these exceptions from disrupting the user experience by implementing the `ShouldRescue` interface on your events.

Events that implement the `ShouldRescue` interface automatically utilize Laravel's [rescue helper function](/docs/{{version}}/helpers#method-rescue) during broadcast attempts. This helper catches any exceptions, reports them to your application's exception handler for logging, and allows the application to continue executing normally without interrupting the user's workflow:

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Contracts\Broadcasting\ShouldRescue;

class ServerCreated implements ShouldBroadcast, ShouldRescue
{
    // ...
}
```

<a name="receiving-broadcasts"></a>
## Receiving Broadcasts

<a name="listening-for-events"></a>
### Listening for Events

Once you have [installed and instantiated Laravel Echo](#client-side-installation), you are ready to start listening for events that are broadcast from your Laravel application. First, use the `channel` method to retrieve an instance of a channel, then call the `listen` method to listen for a specified event:

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

If you would like to listen for events on a private channel, use the `private` method instead. You may continue to chain calls to the `listen` method to listen for multiple events on a single channel:

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### Stop Listening for Events

If you would like to stop listening to a given event without [leaving the channel](#leaving-a-channel), you may use the `stopListening` method:

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```

<a name="leaving-a-channel"></a>
### Leaving a Channel

To leave a channel, you may call the `leaveChannel` method on your Echo instance:

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

If you would like to leave a channel and also its associated private and presence channels, you may call the `leave` method:

```js
Echo.leave(`orders.${this.order.id}`);
```
<a name="namespaces"></a>
### Namespaces

You may have noticed in the examples above that we did not specify the full `App\Events` namespace for the event classes. This is because Echo will automatically assume the events are located in the `App\Events` namespace. However, you may configure the root namespace when you instantiate Echo by passing a `namespace` configuration option:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

Alternatively, you may prefix event classes with a `.` when subscribing to them using Echo. This will allow you to always specify the fully-qualified class name:

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="using-react-or-vue"></a>
### Using React or Vue

Laravel Echo includes React and Vue hooks that make it painless to listen for events. To get started, invoke the `useEcho` hook, which is used to listen for private events. The `useEcho` hook will automatically leave channels when the consuming component is unmounted:

```js tab=React
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

You may listen to multiple events by providing an array of events to `useEcho`:

```js
useEcho(
    `orders.${orderId}`,
    ["OrderShipmentStatusUpdated", "OrderShipped"],
    (e) => {
        console.log(e.order);
    },
);
```

You may also specify the shape of the broadcast event payload data, providing greater type safety and editing convenience:

```ts
type OrderData = {
    order: {
        id: number;
        user: {
            id: number;
            name: string;
        };
        created_at: string;
    };
};

useEcho<OrderData>(`orders.${orderId}`, "OrderShipmentStatusUpdated", (e) => {
    console.log(e.order.id);
    console.log(e.order.user.id);
});
```

The `useEcho` hook will automatically leave channels when the consuming component is unmounted; however, you may utilize the returned functions to manually stop / start listening to channels programmatically when necessary:

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// Stop listening without leaving channel...
stopListening();

// Start listening again...
listen();

// Leave channel...
leaveChannel();

// Leave a channel and also its associated private and presence channels...
leave();
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// Stop listening without leaving channel...
stopListening();

// Start listening again...
listen();

// Leave channel...
leaveChannel();

// Leave a channel and also its associated private and presence channels...
leave();
</script>
```

<a name="react-vue-connecting-to-public-channels"></a>
#### Connecting to Public Channels

To connect to a public channel, you may use the `useEchoPublic` hook:

```js tab=React
import { useEchoPublic } from "@laravel/echo-react";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoPublic } from "@laravel/echo-vue";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="react-vue-connecting-to-presence-channels"></a>
#### Connecting to Presence Channels

To connect to a presence channel, you may use the `useEchoPresence` hook:

```js tab=React
import { useEchoPresence } from "@laravel/echo-react";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoPresence } from "@laravel/echo-vue";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="presence-channels"></a>
## Presence Channels

Presence channels build on the security of private channels while exposing the additional feature of awareness of who is subscribed to the channel. This makes it easy to build powerful, collaborative application features such as notifying users when another user is viewing the same page or listing the inhabitants of a chat room.

<a name="authorizing-presence-channels"></a>
### Authorizing Presence Channels

All presence channels are also private channels; therefore, users must be [authorized to access them](#authorizing-channels). However, when defining authorization callbacks for presence channels, you will not return `true` if the user is authorized to join the channel. Instead, you should return an array of data about the user.

The data returned by the authorization callback will be made available to the presence channel event listeners in your JavaScript application. If the user is not authorized to join the presence channel, you should return `false` or `null`:

```php
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### Joining Presence Channels

To join a presence channel, you may use Echo's `join` method. The `join` method will return a `PresenceChannel` implementation which, along with exposing the `listen` method, allows you to subscribe to the `here`, `joining`, and `leaving` events.

```js
Echo.join(`chat.${roomId}`)
    .here((users) => {
        // ...
    })
    .joining((user) => {
        console.log(user.name);
    })
    .leaving((user) => {
        console.log(user.name);
    })
    .error((error) => {
        console.error(error);
    });
```

The `here` callback will be executed immediately once the channel is joined successfully, and will receive an array containing the user information for all of the other users currently subscribed to the channel. The `joining` method will be executed when a new user joins a channel, while the `leaving` method will be executed when a user leaves the channel. The `error` method will be executed when the authentication endpoint returns an HTTP status code other than 200 or if there is a problem parsing the returned JSON.

<a name="broadcasting-to-presence-channels"></a>
### Broadcasting to Presence Channels

Presence channels may receive events just like public or private channels. Using the example of a chatroom, we may want to broadcast `NewMessage` events to the room's presence channel. To do so, we'll return an instance of `PresenceChannel` from the event's `broadcastOn` method:

```php
/**
 * Get the channels the event should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(): array
{
    return [
        new PresenceChannel('chat.'.$this->message->room_id),
    ];
}
```

As with other events, you may use the `broadcast` helper and the `toOthers` method to exclude the current user from receiving the broadcast:

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

As typical of other types of events, you may listen for events sent to presence channels using Echo's `listen` method:

```js
Echo.join(`chat.${roomId}`)
    .here(/* ... */)
    .joining(/* ... */)
    .leaving(/* ... */)
    .listen('NewMessage', (e) => {
        // ...
    });
```

<a name="model-broadcasting"></a>
## Model Broadcasting

> [!WARNING]
> Before reading the following documentation about model broadcasting, we recommend you become familiar with the general concepts of Laravel's model broadcasting services as well as how to manually create and listen to broadcast events.

It is common to broadcast events when your application's [Eloquent models](/docs/{{version}}/eloquent) are created, updated, or deleted. Of course, this can easily be accomplished by manually [defining custom events for Eloquent model state changes](/docs/{{version}}/eloquent#events) and marking those events with the `ShouldBroadcast` interface.

However, if you are not using these events for any other purposes in your application, it can be cumbersome to create event classes for the sole purpose of broadcasting them. To remedy this, Laravel allows you to indicate that an Eloquent model should automatically broadcast its state changes.

To get started, your Eloquent model should use the `Illuminate\Database\Eloquent\BroadcastsEvents` trait. In addition, the model should define a `broadcastOn` method, which will return an array of channels that the model's events should broadcast on:

```php
<?php

namespace App\Models;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Database\Eloquent\BroadcastsEvents;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Post extends Model
{
    use BroadcastsEvents, HasFactory;

    /**
     * Get the user that the post belongs to.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Get the channels that model events should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>
     */
    public function broadcastOn(string $event): array
    {
        return [$this, $this->user];
    }
}
```

Once your model includes this trait and defines its broadcast channels, it will begin automatically broadcasting events when a model instance is created, updated, deleted, trashed, or restored.

In addition, you may have noticed that the `broadcastOn` method receives a string `$event` argument. This argument contains the type of event that has occurred on the model and will have a value of `created`, `updated`, `deleted`, `trashed`, or `restored`. By inspecting the value of this variable, you may determine which channels (if any) the model should broadcast to for a particular event:

```php
/**
 * Get the channels that model events should broadcast on.
 *
 * @return array<string, array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>>
 */
public function broadcastOn(string $event): array
{
    return match ($event) {
        'deleted' => [],
        default => [$this, $this->user],
    };
}
```

<a name="customizing-model-broadcasting-event-creation"></a>
#### Customizing Model Broadcasting Event Creation

Occasionally, you may wish to customize how Laravel creates the underlying model broadcasting event. You may accomplish this by defining a `newBroadcastableEvent` method on your Eloquent model. This method should return an `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` instance:

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * Create a new broadcastable model event for the model.
 */
protected function newBroadcastableEvent(string $event): BroadcastableModelEventOccurred
{
    return (new BroadcastableModelEventOccurred(
        $this, $event
    ))->dontBroadcastToCurrentUser();
}
```

<a name="model-broadcasting-conventions"></a>
### Model Broadcasting Conventions

<a name="model-broadcasting-channel-conventions"></a>
#### Channel Conventions

As you may have noticed, the `broadcastOn` method in the model example above did not return `Channel` instances. Instead, Eloquent models were returned directly. If an Eloquent model instance is returned by your model's `broadcastOn` method (or is contained in an array returned by the method), Laravel will automatically instantiate a private channel instance for the model using the model's class name and primary key identifier as the channel name.

So, an `App\Models\User` model with an `id` of `1` would be converted into an `Illuminate\Broadcasting\PrivateChannel` instance with a name of `App.Models.User.1`. Of course, in addition to returning Eloquent model instances from your model's `broadcastOn` method, you may return complete `Channel` instances in order to have full control over the model's channel names:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channels that model events should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(string $event): array
{
    return [
        new PrivateChannel('user.'.$this->id)
    ];
}
```

If you plan to explicitly return a channel instance from your model's `broadcastOn` method, you may pass an Eloquent model instance to the channel's constructor. When doing so, Laravel will use the model channel conventions discussed above to convert the Eloquent model into a channel name string:

```php
return [new Channel($this->user)];
```

If you need to determine the channel name of a model, you may call the `broadcastChannel` method on any model instance. For example, this method returns the string `App.Models.User.1` for an `App\Models\User` model with an `id` of `1`:

```php
$user->broadcastChannel();
```

<a name="model-broadcasting-event-conventions"></a>
#### Event Conventions

Since model broadcast events are not associated with an "actual" event within your application's `App\Events` directory, they are assigned a name and a payload based on conventions. Laravel's convention is to broadcast the event using the class name of the model (not including the namespace) and the name of the model event that triggered the broadcast.

So, for example, an update to the `App\Models\Post` model would broadcast an event to your client-side application as `PostUpdated` with the following payload:

```json
{
    "model": {
        "id": 1,
        "title": "My first post"
        ...
    },
    ...
    "socket": "someSocketId"
}
```

The deletion of the `App\Models\User` model would broadcast an event named `UserDeleted`.

If you would like, you may define a custom broadcast name and payload by adding a `broadcastAs` and `broadcastWith` method to your model. These methods receive the name of the model event / operation that is occurring, allowing you to customize the event's name and payload for each model operation. If `null` is returned from the `broadcastAs` method, Laravel will use the model broadcasting event name conventions discussed above when broadcasting the event:

```php
/**
 * The model event's broadcast name.
 */
public function broadcastAs(string $event): string|null
{
    return match ($event) {
        'created' => 'post.created',
        default => null,
    };
}

/**
 * Get the data to broadcast for the model.
 *
 * @return array<string, mixed>
 */
public function broadcastWith(string $event): array
{
    return match ($event) {
        'created' => ['title' => $this->title],
        default => ['model' => $this],
    };
}
```

<a name="listening-for-model-broadcasts"></a>
### Listening for Model Broadcasts

Once you have added the `BroadcastsEvents` trait to your model and defined your model's `broadcastOn` method, you are ready to start listening for broadcasted model events within your client-side application. Before getting started, you may wish to consult the complete documentation on [listening for events](#listening-for-events).

First, use the `private` method to retrieve an instance of a channel, then call the `listen` method to listen for a specified event. Typically, the channel name given to the `private` method should correspond to Laravel's [model broadcasting conventions](#model-broadcasting-conventions).

Once you have obtained a channel instance, you may use the `listen` method to listen for a particular event. Since model broadcast events are not associated with an "actual" event within your application's `App\Events` directory, the [event name](#model-broadcasting-event-conventions) must be prefixed with a `.` to indicate it does not belong to a particular namespace. Each model broadcast event has a `model` property which contains all of the broadcastable properties of the model:

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.UserUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="model-broadcasts-with-react-or-vue"></a>
#### Using React or Vue

If you are using React or Vue, you may use Laravel Echo's included `useEchoModel` hook to easily listen for model broadcasts:

```js tab=React
import { useEchoModel } from "@laravel/echo-react";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
</script>
```

You may also specify the shape of the model event payload data, providing greater type safety and editing convenience:

```ts
type User = {
    id: number;
    name: string;
    email: string;
};

useEchoModel<User, "App.Models.User">("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model.id);
    console.log(e.model.name);
});
```

<a name="client-events"></a>
## Client Events

> [!NOTE]
> When using [Pusher Channels](https://pusher.com/channels), you must enable the "Client Events" option in the "App Settings" section of your [application dashboard](https://dashboard.pusher.com/) in order to send client events.

Sometimes you may wish to broadcast an event to other connected clients without hitting your Laravel application at all. This can be particularly useful for things like "typing" notifications, where you want to alert users of your application that another user is typing a message on a given screen.

To broadcast client events, you may use Echo's `whisper` method:

```js tab=JavaScript
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
</script>
```

To listen for client events, you may use the `listenForWhisper` method:

```js tab=JavaScript
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
</script>
```

<a name="notifications"></a>
## Notifications

By pairing event broadcasting with [notifications](/docs/{{version}}/notifications), your JavaScript application may receive new notifications as they occur without needing to refresh the page. Before getting started, be sure to read over the documentation on using [the broadcast notification channel](/docs/{{version}}/notifications#broadcast-notifications).

Once you have configured a notification to use the broadcast channel, you may listen for the broadcast events using Echo's `notification` method. Remember, the channel name should match the class name of the entity receiving the notifications:

```js tab=JavaScript
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

```js tab=React
import { useEchoModel } from "@laravel/echo-react";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
</script>
```

In this example, all notifications sent to `App\Models\User` instances via the `broadcast` channel would be received by the callback. A channel authorization callback for the `App.Models.User.{id}` channel is included in your application's `routes/channels.php` file.
