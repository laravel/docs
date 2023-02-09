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
- [Eager Loading](#eager-loading)
- [Updating Values](#updating-values)
    - [Bulk Updates](#bulk-updates)
    - [Purging Features](#purging-features)
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

After publishing Pennant's assets, its configuration file will be located at `config/pennant.php`. This configuration file allows you to select the default driver and more.

<a name="creating-features"></a>
## Creating Features

When creating a feature you will need to provide a name and a Closure. The Closure should return the initial value for the feature. Typically, features are defined in a service provider using the `Feature` facade. The Closure will be passed the "scope" for the feature check, which would commonly be the currently authenticated user.

In this example, we will define a feature for incrementally rolling out a new API to our application's users.

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
- Otherwise the feature should be randomly assigned to users with a 1 in 100 chance of being active.

The first time the `new-api` feature is checked for a given user, the result of the Closure will be stored by the underlying driver. The next time the feature is checked against the same user, the value will be retrieved from storage and the Closure will not be invoked.

If a feature definition only returns a lottery, you may omit the Closure completely.

    Feature::define('site-redesign', Lottery::odds(1, 1000));

<a name="class-based-features"></a>
### Class Based Features

Class based features are also supported. Unlike Closure based definitions, there is no need to register a class based feature in a service provider.

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

There are some additional methods that may come in handy when checking if a feature is active or not:

    // Check if all the features are active...
    Feature::allAreActive(['new-api', 'site-redesign']);

    // Check if any of the features are active...
    Feature::someAreActive(['new-api', 'site-redesign']);

    // Check if a feature is inactive...
    Feature::inactive('new-api');

    // Check if all the features are inactive...
    Feature::allAreInactive(['new-api', 'site-redesign']);

    // Check if any of the features are inactive...
    Feature::someAreInactive(['new-api', 'site-redesign']);

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

To make checking features in Blade a seamless experience, Pennant also offers a `@feature` directive.

```blade
@feature('site-redesign')
    <!-- 'site-redesign' is active -->
@else
    <!-- 'site-redesign' is inactive -->
@endfeature
```

<a name="in-memory-cache"></a>
### In-Memory Cache

When checking a feature, Pennant will create an in-memory cache of the result. If you are using the database driver, this means that re-checking the same feature flag throughout a single request will not trigger additional database queries. It also ensures you have a consistent result for the duration of the request.

If you need to manually flush the in-memory cache, you may use the `flushCache` method on the `Feature` facade.

    Feature::flushCache();

<a name="scope"></a>
## Scope

As previously mentioned, features are checked against the currently authenticated user by default. This may not always suit your needs. For one off feature checks, it is possible to specify the scope you would like to check the feature against.

Imagine you have built a new billing experience that you are rolling out to entire teams at once, rather than individual users. You want the oldest teams have a slower rollout than the newer teams. Your feature Closure might look something like the following:

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

You will notice that the Closure we have defined is not expecting a `User`, but is instead expecting a `Team` model. To check if this feature is active for a user's team, you should pass the team to the `for` method.

    use Laravel\Pennant\Feature;

    if (Feature::for($user->team)->active('billing-v2')) {
        return redirect()->to('/billing/v2');
    }

    // ...

<a name="default-scope"></a>
### Default Scope

It is also possible to customize the default scope used when checking features. Suppose all your features are checked against the currently authenticated user's team; rather than having to call `Feature::for($user->team)` on every feature check, you may instead specify the default scope to use in a service provider.

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

If no scope is provided via the `for` method, a feature check will now use the currently authenticated user's team.

    Feature::active('billing-v2');

    // is now equivalent to...

    Feature::for($user->team)->active('billing-v2');

<a name="identifying-scope"></a>
### Identifying Scope

Implementing the `FeatureScopeable` contract on your scope objects allows you to customize what is passed to the underlying Pennant drivers.

Imagine you are using two different feature drivers in a single application, perhaps the built-in database driver and a 3rd party "Flag Rocket" driver. The "Flag Rocket" driver requires a `FlagRocketUser` to identify a user. The database driver, however, can handle an Eloquent model. Implementing the `toFeatureIdentifier` method allows you to customize the scope passed to each driver.

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
            'flag-rocket' => FlagRocketUser::fromId($this->flag_rocket_id),
        };
    }
}
```

<a name="rich-feature-values"></a>
## Rich Feature Values

Until now, we have shown features as being in a binary state, that is they are either active or inactive, but Pennant allows you to store rich values as well.

Imagine you are testing 3 new colors for the "Buy now" button of your application. Instead of returning `true` or `false` from the feature definition, you may instead return a string.

    use Illuminate\Support\Arr;
    use Laravel\Pennant\Feature;

    Feature::define('purchase-button', function (User $user) {
        return Arr::random([
            'blue-sapphire',
            'seafoam-green',
            'tart-orange',
        ]);
    });

You may retrieve the value of the `'purchase-button'` feature using the `value` method.

    $color = Feature::value('purchase-button');

The Blade directive also makes it easy to conditionally render content based on the current value of the feature.

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire' is active -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green' is active -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-oranage' is active -->
@endfeature
```

> **Note** When using rich values, it is important to know that a feature is considered "active" when it has any value other than `false`.

<a name="eager-loading"></a>
## Eager Loading

Although Pennant keeps an in-memory cache of all resolved features for a single request, it is still possible to run into performance issues. To alleviate this, Pennant offers the ability to eager load feature values.

Imagine that we are checking if a feature is active within a loop:

    foreach ($users as $user) {
        if (Feature::for($user)->active('notifications-beta')) {
            $user->notify(new RegistrationSuccess);
        }
    }

Assuming we are using the database driver, we are going to be hitting the database for every user in the loop - potentially hundreds of queries. With eager loading we can remove this potential performance bottleneck.

    Feature::for($users)->load('notifications-beta');

    foreach ($users as $user) {
        if (Feature::for($user)->active('notifications-beta')) {
            $user->notify(new RegistrationSuccess);
        }
    }

Once in place we no longer trigger any database queries inside the loop.

To load values only when it has not already been loaded, use the `loadMissing` method:

    Feature::for($users)->loadMissing([
        'new-api',
        'purchase-button',
        'notifications-beta',
    ]);

<a name="updating-values"></a>
## Updating Values

When a feature's value is resolved for the first time, the underlying driver will store the result. This is handy to ensure a consistent experience for your users across requests, but you may also want to manually update the feature's stored value.

To achieve this you can use the `activate` and `deactivate` methods to toggle a feature on or off.

    // Activate the feature for the default scope...
    Feature::activate('new-api');

    // Deactivate the feature for the given scope...
    Feature::for($user->team)->deactivate('billing-v2');

It is also possible to manually set rich value for a feature by passing through a second argument to the `activate` method.

    Feature::activate('purchase-button', 'seafoam-green');

If you wish to forget the stored value for a feature, so that the next time it is checked the value is resolved from the feature definition, you may use the `forget` method.

    Feature::forget('purchase-button');

<a name="bulk-updates"></a>
### Bulk Updates

To make bulk updates you may use the `activateForEveryone` and `deactivateForEveryone` methods. 

Say you are now confident in the `'new-api'` feature's stability and have landed on the best `'purchase-button'` color to be using, you can update the stored value for all users accordingly.

    Feature::activateForEveryone('new-api');

    Feature::activateForEveryone('purchase-button', 'seafoam-green');


Alternatively, if you are having issues with a feature rollout you may need to deactivate the feature for all users instead.

    Feature::deactivateForEveryone('new-api');

> **Note** This will only update the existing stored values. You may also need to update the feature definition in your code.

<a name="purging-features"></a>
### Purging Features

It can be useful to purge an entire feature from storage, whether you have removed the feature from your system or you have made adjustments to the features definition that you would like to rollout fresh to all users.

You may completely remove all stored values for a feature using the `purge` method.

    Feature::purge('new-api');

If you would like to purge _all_ features from storage, you may do so by calling `purge` without any arguments.

    Feature::purge();

As it can be useful to do this as part of your deployment pipeline, we have also included a handy Artisan.

```sh
php artisan pennant:purge new-api
```

<a name="events"></a>
## Events

Pennant dispatches a few events that may be useful for tracking feature flags throughout your application.

### `Illuminate\Pennant\Events\RetrievingKnownFeature` 

This event is dispatched the first time a known feature is retrieved during a request for a specific scope. This event can be useful to create and track metrics against the feature flags that are in-use throughout your application.

### `Illuminate\Pennant\Events\RetrievingUnknownFeature` 

This event is dispatched the first time an unknown feature is retrieved during a request for the specific scope. This event can be useful if you have intended to remove a feature flag, but left some stray references to it throughout your application.

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
