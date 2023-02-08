# Laravel Pennant

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
- [Defining Features](#defining-features)
    - [Class Based Feature](#class-based-features)
- [Checking Features](#checking-features)
    - [In-Memory Cache](#in-memory-cache)
- [Events](#events)

<a name="introduction"></a>
## Introduction

[Laravel Pennant](https://github.com/laravel/pennant) is a simple and lightweight feature flag package, without any cruft. Feature flags enable you to incrementally roll out new application features with confidence, A/B test new interface designs, compliment a trunk-based development strategy, and much more.

<a name="installation"></a>
## Installation

First, install Pennant into your project using the Composer package manager:

```shell
composer require laravel/pennant
```

Next, you should publish the Pennant configuration and migration files using the `vendor:publish` Artisan command:

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

Finally, you should run the database migrations. This will create a `features` table that Pennant uses to power the database driver:

```shell
php artisan migrate
```

<a name="configuration"></a>
## Configuration

After publishing Pennant's assets, its configuration file will be located at `config/pennant.php`. This configuration file allows you to select the default driver and configure the individual drivers.

<a name="defining-features"></a>
## Defining Features

A feature definition is simply a Closure that returns the initial value for the specific feature. Typically, features are defined in a service provider using the `Feature` facade. The Closure will be passed the "scope" for the feature flag check, which would commonly be the current user.

In this example, we will define a feature for rolling out a new API implementation incrementally to our application's users.

```php
<?php

namespace App\Providers;

use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;
use Illuminate\Support\Lottery;
use Laravel\Pennat\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::define('new-api', function (User $user) {
            if ($user->isInternalTeamMember()) {
                return true;
            }

            if ($user->isHighTrafficCustomer()) {
                return false;
            }

            return Lottery::odds(1 / 100);
        });
    }
}
```

As you can see, we have the following rules for our feature definition:

- All internal team members should be using the new API.
- Any high traffic customers should not be using the new API.
- Otherwise the feature should be randomly assigned to users with a 1 in 100 chance of being activated.

The first time the `new-api` feature is checked for a given user, the result of the definition Closure will be persisted by the underlying driver. This means that the next time the feature is check against the same user, the value will be retrieved from storage rather than decided by the feature's definition.

If your feature definition only returns a lottery, you may omit the Closure completely.

    Feature::define('site-redesign', Lottery::odds(1, 1000));

<a name="class-based-features"></a>
### Class Based Features

You may also create class based features. Unlike Closure based definitions, there is no need to register class based features in a service provider.

When create a feature class you will need to implement the `resolve` method:

```php
<?php

namespace App\Features;

use Illuminate\Support\Lottery;

class NewApi
{
    public function resolve(User $user)
    {
        if ($user->isInternalTeamMember()) {
            return true;
        }

        if ($user->isHighTrafficCustomer()) {
            return false;
        }

        return Lottery::odds(1 / 100);
    }
}
```

> **Note** Feature classes are resolved via the container, so you may inject dependencies into the class's constructor when needed.

<a name="checking-features"></a>
## Checking Features

To check if a feature is active, you should use the `isActive` method on the `Feature` facade. By default, features are checked against the currently authenticated user.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        if (Feature::isActive('new-api')) {
            return $this->resolveNewApiResponse($request);
        }

        return $this->resolveLegacyApiResponse($request);
    }

    // ...
}
```

For class based features, you should use class name when checking the features state:

```php
<?php

namespace App\Http\Controllers;

use App\Features\NewApi;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        if (Feature::isActive(NewApi::class)) {
            return $this->resolveNewApiResponse($request);
        }

        return $this->resolveLegacyApiResponse($request);
    }

    // ...
}
```

<a name="in-memory-cache"></a>
### In-Memory Cache

When checking the state of a feature, Pennant will create a in-memory cache of the result. If you are using the database driver, this means that re-checking the same feature flag throughout a single request will not trigger subsequent database queries. It also ensures you have a consistent result for the duration of the request.

If you need to manually flush the in-memory cache, you may use the `flushCache` method on the `Feature` facade.

    Feature::flushCache();

<a name="events"></a>
## Events

Pennant dispatches a few events that may be useful for tracking the feature flags throughout your application.

### `Illuminate\Pennant\Events\RetrievingKnownFeature` 

This event is dispatched the first time a known feature is resolved during a request for a specific scope. This may be useful to create and track metrics against the feature flags that are in-use throughout your application.

### `Illuminate\Pennant\Events\RetrievingUnknownFeature` 

This event is dispatched the first time an unknown feature is resolved during a request for the specific scope. This may be useful if you have intended to remove a feature flag, but left some stray references to it throughout your application.

You may like to listen for this event and report or throw an exception when it occurs.

```php
<?php

namespace App\Providers;

use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;
use Illuminate\Pennant\Events\RetrievingUnknownFeature;
use Illuminate\Support\Facades\Event;

class EventServiceProvider extends ServiceProvider
{
    /**
     * Register any other events for your application.
     */
    public function boot(): void
    {
        Event::listen(function (RetrievingUnknownFeature $event) {
            report("Resolving unknown feature [{$event->feature}]."));
        });
    }
}
```

### `Illuminate\Pennant\Events\DynamicallyDefiningFeature`

This event is dispatched whenever an unregistered class based feature is being dynamically defined for the first time during a request.



- events
    - known
    - unknown
    - dynamic

- helpers
    - global
    - blade

- bulk updates
    - purge

- customising an objects scope
- default scope

- eager loading + loadMissing

- attaching feature to objects (this should be improved)
 $user->feature('foo')->active();

- using the array driver for lottery based features.
- using the array driver for package features

- array driver for testing
- custom drivers
