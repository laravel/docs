# Laravel Pennant

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
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

<a name="events"></a>
## Events

### `Illuminate\Pennant\Events\RetrievingKnownFeature` 

This event is dispatched the first time a known feature is resolved during a request for the given scope. This may be useful to create and track metrics against the feature flags that are in-use throughout your application.

### `Illuminate\Pennant\Events\RetrievingUnknownFeature` 

This event is dispatched thefirst time an unknown feature is resolved during a request for the given scope. This may be useful if you have intended to remove a feature flag, but left some stray references to it throughout your application.

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

This event is dispatched whenever a feature is being dynamically defined for the first time during a request.


- Defining features
    - string based
    - class based
    - dynamic class based

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
