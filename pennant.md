# Laravel Pennant

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
- [Creating Features](#creating-features)
    - [Class Based Features](#class-based-features)
- [Checking Features](#checking-features)
    - [Conditional Execution](#conditional-execution)
    - [Blade Directive](#blade-directive)
    - [In-Memory Cache](#in-memory-cache)
- [Scope](#scope)
    - [Default Scope](#default-scope)
    - [Identifying Scope](#identifying-scope)
- [Rich Feature Values](#rich-feature-values)
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

<a name="creating-features"></a>
## Creating Features

A feature is a Closure that returns the initial value for the specific feature. Typically, features are defined in a service provider using the `Feature` facade. The Closure will be passed the "scope" for the feature check, which would commonly be the currently authenticated user.

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

As you can see, we have the following rules for our feature:

- All internal team members should be using the new API.
- Any high traffic customers should not be using the new API.
- Otherwise the feature should be randomly assigned to users with a 1 in 100 chance of being activated.

The first time the `new-api` feature is checked for a given user, the result of the Closure will be persisted by the underlying driver. The next time the feature is checked against the same user, the value will be retrieved from storage and the Closure will not be invoked.

If a feature definition only returns a lottery, you may omit the Closure completely.

    Feature::define('site-redesign', Lottery::odds(1, 1000));

<a name="class-based-features"></a>
### Class Based Features

Class based features are also supported. Unlike Closure based definitions, there is no need to register class based features in a service provider.

When creating a feature class you will need to implement the `resolve` method:

```php
<?php

namespace App\Features;

use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * Resolve the feature's initial value.
     */
    public function resolve(User $user): mixed
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

To check if a feature is active, you should use the `active` method on the `Feature` facade. By default, features are checked against the currently authenticated user.

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
        if (Feature::active('new-api')) {
            return $this->resolveNewApiResponse($request);
        }

        return $this->resolveLegacyApiResponse($request);
    }

    // ...
}
```

For class based features, you should use the class name when checking the feature:

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
        if (Feature::active(NewApi::class)) {
            return $this->resolveNewApiResponse($request);
        }

        return $this->resolveLegacyApiResponse($request);
    }

    // ...
}
```

There are some additional methods that may be handy when checking if a feature is active or not:

    // Check if all the features are active...
    Feature::allAreActive(['billing-v2', 'payments-v2']);

    // Check if any of the features are active...
    Feature::someAreActive(['billing-v2', 'payments-v2']);

    // Check if a feature is inactive...
    Feature::inactive('billing-v2');

    // Check if all the features are active...
    Feature::allAreInactive(['billing-v2', 'payments-v2']);

    // Check if any of the features are active...
    Feature::someAreInactive(['billing-v2', 'payments-v2']);

<a name="conditional-execution"></a>
### Conditional Execution

Pennant offers the ability to conditionally execute a specific code block in a fluent manner. This is achieved via the `when` and `unless` methods.

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
            return Feature::when(NewApi::class,
                fn () => $this->resolveNewApiResponse($request),
                fn () => $this->resolveLegacyApiResponse($request),
            );
        }
     
        // ...
    }

<a name="blade-directive"></a>
### Blade Directive

To make checking features in Blade files a seamless experience, Pennant also offers a `@feature` directive.

```blade
@feature('billing-2.0')
    <!-- ... -->
@else
    <!-- ... -->
@endfeature
```

<a name="in-memory-cache"></a>
### In-Memory Cache

When checking a feature, Pennant will create a in-memory cache of the result. If you are using the database driver, this means that re-checking the same feature flag throughout a single request will not trigger subsequent database queries. It also ensures you have a consistent result for the duration of the request.

If you need to manually flush the in-memory cache, you may use the `flushCache` method on the `Feature` facade.

    Feature::flushCache();

<a name="scope"></a>
## Scope

As previous mentioned, by default features are checked against the currently authenticated user. This may not always suit your needs.

Imagine you have built a new billing experience that you are rolling out to entire teams at once, rather than individual users. You want our oldest teams have a slower rollout than our newer teams.

    use App\Models\Team;
    use Carbon\Carbon;
    use Illuminate\Support\Lottery;

    Feature::define('billing-v2', function (Team $team) {
        if ($team->created_at->isAfter(new Carbon('1st Jan, 2023'))) {
            return true;
        }

        if ($team->created_at->isAfter(new Carbon('1st Jan, 2019'))) {
            return Lottery::odds(1 / 100);
        }

        return Lottery::odds(1 / 1000);
    });

You will notice that the Closure receives an instance of the team model. To check if this feature is active for a user's team, you should pass the team to the `for` method on the `Feature` facade:

    use Laravel\Pennant\Feature;

    if (Feature::for($user->team)->active('billing-v2')) {
        return redirect()->to('/billing/v2');
    }

    // ...

<a name="default-scope"></a>
### Default Scope

It is possible to customize the default scope used when checking features. Suppose all your features are checked against the currently authenticated user's team, rather than having the call `Feature::for($user->team)` on every feature check, you may instead specify the default scope in a service provider.

```php
<?php

namespace App\Providers;

use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;
use Laravel\Pennat\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::resolveScopeUsing(function ($driver) {
            return request()->user()->team;
        });

        // ...
    }
}
```

If no scope is provided via the `for` method, all feature checks will now be done against the currently authenticated user's team.

    Feature::active('billing-v2');

    // Now equivalent to...

    Feature::for($user->team)->active('billing-v2');

<a name="identifying-scope"></a>
### Identifying Scope

When resolving the value of a feature, you may need to customize the value that is passed to a Pennant driver as the scope for the feature check. To do this, your scope should implement the `FeatureScopeable` contract.

Imagine you are using two different feature drivers in our application: the built-in database driver and a 3rd party "Flag Rocket" driver. The "Flag Rocket" driver requires a `FlagRocketUser` to identify a user. Implementing the `toFeatureIdentifier` method allows you to customize the scope passed to the Flag Rocket driver.

```php
<?php

namespace App\Models;

use FlagRocket\FlagRocketUser;
use Illuminate\Database\Eloquent\Model;
use Laravel\Pennant\Contracts\FeatureScopeable;

class User extends Model implements FeatureScopeable
{
    /**
     * Cast the object to a feature scope identifier for the given driver.
     */
    public function toFeatureIdentifier(string $driver): mixed
    {
        return match($driver) {
            'database' => $this,
            'flag-rocket' => new FlagRocketUser($this->flag_rocket_id),
        };
    }
}
```

The Flag Rocket driver will now receive an instance of the `FlagRocketUser` to handle it as needed.

<a name="rich-feature-values"></a>
## Rich Feature Values

Until now, we have shown features as being in a binary state, that is they are either active or inactive, but Pennant allows you to store rich values as well.

Imagine you are testing 3 new colors for the "Buy now" button of your application. Instead of returning `true` or `false` from the feature definition, you may instead return a string.

    use Illuminate\Support\Arr;
    use Laravel\Pennant\Feature;

    Feature::define('checkout-button', function (User $user) {
        return Arr::random([
            'blue-sapphire',
            'seafoam-green',
            'tart-orange',
        ]);
    });

You may retrieve the value of the `'checkout-button'` feature using the `value` method on the `Feature` facade.

    $color = Feature::value('checkout-button');

The Blade directive also makes it easy to conditionally render content based on the current value of the feature.

```blade
@feature('checkout-button', 'blue-sapphire')
    <!-- ... -->
@elsefeature('checkout-button', 'seafoam-green')
    <!-- ... -->
@elsefeature('checkout-button', 'tart-orange')
    <!-- ... -->
@endfeature
```

> **Note** When using rich values, it is important to know that a feature is considered "active" when it has any value other than `false`.

<a name="events"></a>
## Events

Pennant dispatches a few events that may be useful for tracking the feature flags throughout your application.

### `Illuminate\Pennant\Events\RetrievingKnownFeature` 

This event is dispatched the first time a known feature is resolved during a request for a specific scope. This event can be useful to create and track metrics against the feature flags that are in-use throughout your application.

### `Illuminate\Pennant\Events\RetrievingUnknownFeature` 

This event is dispatched the first time an unknown feature is resolved during a request for the specific scope. This event can be useful if you have intended to remove a feature flag, but left some stray references to it throughout your application.

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

This event is dispatched whenever a class based feature is being dynamically checked for the first time during a request.


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
