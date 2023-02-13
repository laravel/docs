# Laravel Pennant

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
- [Defining Features](#defining-features)
    - [Class Based Features](#class-based-features)
- [Checking Features](#checking-features)
    - [Conditional Execution](#conditional-execution)
    - [Blade Directive](#blade-directive)
    - [Middleware](#middleware)
    - [In-Memory Cache](#in-memory-cache)
- [Scope](#scope)
    - [Specifying The Scope](#specifying-the-scope)
    - [Default Scope](#default-scope)
    - [Nullable Scope](#nullable-scope)
    - [Identifying Scope](#identifying-scope)
- [Rich Feature Values](#rich-feature-values)
- [Eager Loading](#eager-loading)
- [Updating Values](#updating-values)
    - [Bulk Updates](#bulk-updates)
    - [Purging Features](#purging-features)
- [Events](#events)

<a name="introduction"></a>
## Introduction

[Laravel Pennant](https://github.com/laravel/pennant) is a simple and lightweight feature flag package - without the cruft. Feature flags enable you to incrementally roll out new application features with confidence, A/B test new interface designs, compliment a trunk-based development strategy, and much more.

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

Finally, you should run your application's database migrations. This will create a `features` table that Pennant uses to power its `database` driver:

```shell
php artisan migrate
```

<a name="configuration"></a>
## Configuration

After publishing Pennant's assets, its configuration file will be located at `config/pennant.php`. This configuration file allows you to specify the default storage mechanism that will be used by Pennant to store resolved feature flag values.

Pennant includes support for storing resolved feature flag values in an in-memory array via the `array` driver. Or, Pennant can store resolved feature flag values persistently in a relational database via the `database` driver, which is the default storage mechanism used by Pennant.

<a name="defining-features"></a>
## Defining Features

To define a feature, you may use the `define` method offered by the `Feature` facade. You will need to provide a name for the feature, as well as a closure that will be invoked to resolve the feature's initial value.

Typically, features are defined in a service provider using the `Feature` facade. The closure will receive the "scope" for the feature check. Most commonly, the scope is the currently authenticated user. In this example, we will define a feature for incrementally rolling out a new API to our application's users:

```php
<?php

namespace App\Providers;

use App\Models\User;
use Illuminate\Support\Lottery;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::define('new-api', fn (User $user) => match (true) {
            $user->isInternalTeamMember() => true,
            $user->isHighTrafficCustomer() => false,
            default => Lottery::odds(1 / 100),
        });
    }
}
```

As you can see, we have the following rules for our feature:

- All internal team members should be using the new API.
- Any high traffic customers should not be using the new API.
- Otherwise, the feature should be randomly assigned to users with a 1 in 100 chance of being active.

The first time the `new-api` feature is checked for a given user, the result of the closure will be stored by the storage driver. The next time the feature is checked against the same user, the value will be retrieved from storage and the closure will not be invoked.

For convenience, if a feature definition only returns a lottery, you may omit the closure completely:

    Feature::define('site-redesign', Lottery::odds(1, 1000));

<a name="class-based-features"></a>
### Class Based Features

Pennant also allows you to define class based features. Unlike closure based feature definitions, there is no need to register a class based feature in a service provider. To create a class based feature, you may invoke the `pennant:feature` Artisan command. By default the feature class will be placed in your application's `app/Features` directory:

```shell
php artisan pennant:feature NewApi
```

When writing a feature class, you only need to define a `resolve` method, which will be invoked to resolve the feature's initial value for a given scope. Again, the scope will typically be the currently authenticated user:

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
        return match (true) {
            $user->isInternalTeamMember() => true,
            $user->isHighTrafficCustomer() => false,
            default => Lottery::odds(1 / 100),
        };
    }
}
```

> **Note** Feature classes are resolved via the [container](/docs/{{version}}/container), so you may inject dependencies into the feature class's constructor when needed.

<a name="checking-features"></a>
## Checking Features

To determine if a feature is active, you may use the `active` method on the `Feature` facade. By default, features are checked against the currently authenticated user:

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
        return Feature::active('new-api')
                ? $this->resolveNewApiResponse($request)
                : $this->resolveLegacyApiResponse($request);
    }

    // ...
}
```

Although features are checked against the currently authenticated user by default, you may easily check the feature against another user or [scope](#scope). To accomplish this, use the `for` method offered by the `Feature` facade:

```php
return Feature::for($user)->active('new-api')
        ? $this->resolveNewApiResponse($request)
        : $this->resolveLegacyApiResponse($request);
```

> **Note** 
> When using Pennant outside of an HTTP context, such as in an Artisan command or a queued job, you should typically [explicitly specify the feature's scope](#specifying-the-scope). Alternatively, you may define a [default scope](#default-scope) that accounts for both authenticated HTTP contexts and unauthenticated contexts.

<a name="checking-class-based-features"></a>
#### Checking Class Based Features

For class based features, you should provide the class name when checking the feature:

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
        return Feature::active(NewApi::class)
                ? $this->resolveNewApiResponse($request)
                : $this->resolveLegacyApiResponse($request);
    }

    // ...
}
```

Pennant also offers some additional convenience methods that may prove useful when determining if a feature is active or not:

```php
// Determine if all of the given features are active...
Feature::allAreActive(['new-api', 'site-redesign']);

// Determine if any of the given features are active...
Feature::someAreActive(['new-api', 'site-redesign']);

// Determine if a feature is inactive...
Feature::inactive('new-api');

// Determine if all of the given features are inactive...
Feature::allAreInactive(['new-api', 'site-redesign']);

// Determine if any of the given features are inactive...
Feature::someAreInactive(['new-api', 'site-redesign']);
```

<a name="conditional-execution"></a>
### Conditional Execution

The `when` method may be used to fluently execute a given closure if a feature is active. Additionally, a second closure may be provided and will be executed if the feature is inactive:

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

The `unless` method serves as the inverse of the `when` method, executing the first closure if the feature is inactive:

    return Feature::unless(NewApi::class,
        fn () => $this->resolveLegacyApiResponse($request),
        fn () => $this->resolveNewApiResponse($request),
    );

<a name="blade-directive"></a>
### Blade Directive

To make checking features in Blade a seamless experience, Pennant offers a `@feature` directive:

```blade
@feature('site-redesign')
    <!-- 'site-redesign' is active -->
@else
    <!-- 'site-redesign' is inactive -->
@endfeature
```

<a name="middleware"></a>
### Middleware

Pennant also includes a [middleware](/docs/{{version}}/middleware) that may be used to verify the currently authenticated user has access to a feature before a route is even invoked. To get started, you should add a middleware alias for the `EnsureFeaturesAreActive` middleware to your application's `app/Http/Kernel.php` file:

```php
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

protected $middlewareAliases = [
    // ...
    'features' => EnsureFeaturesAreActive::class,
];
```

Next, you may assign the middleware to a route and specify the features that are required to access the route. If any of the specified features are inactive for the currently authenticated user, a `400 Bad Request` HTTP response will be returned by the route. Multiple features may be specified using a comma-delimited list:

```php
Route::get('/api/servers', function () {
    // ...
})->middleware(['features:new-api,servers-api']);
```

<a name="customizing-the-response"></a>
#### Customizing The Response

If you would like to customize the response that is returned by the middleware when one of the listed features is inactive, you may use the `whenInactive` method provided by the `EnsureFeaturesAreActive` middleware. Typically, this method should be invoked within the `boot` method of one of your application's service providers:

```php
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    EnsureFeaturesAreActive::whenInactive(
        function (Request $request, array $features) {
            return new Response(status: 403);
        }
    );

    // ...
}
```

<a name="in-memory-cache"></a>
### In-Memory Cache

When checking a feature, Pennant will create an in-memory cache of the result. If you are using the `database` driver, this means that re-checking the same feature flag within a single request will not trigger additional database queries. This also ensures that the feature has a consistent result for the duration of the request.

If you need to manually flush the in-memory cache, you may use the `flushCache` method offered by the `Feature` facade:

    Feature::flushCache();

<a name="scope"></a>
## Scope

<a name="specifying-the-scope"></a>
### Specifying The Scope

As discussed, features are typically checked against the currently authenticated user. However, this may not always suit your needs. Therefore, it is possible to specify the scope you would like to check a given feature against via the `Feature` facade's `for` method:

```php
return Feature::for($user)->active('new-api')
        ? $this->resolveNewApiResponse($request)
        : $this->resolveLegacyApiResponse($request);
```

Of course, feature scopes are not limited to "users". Imagine you have built a new billing experience that you are rolling out to entire teams rather than individual users. Perhaps you would like the oldest teams to have a slower rollout than the newer teams. Your feature resolution closure might look something like the following:

```php
use App\Models\Team;
use Carbon\Carbon;
use Illuminate\Support\Lottery;
use Laravel\Pennant\Feature;

Feature::define('billing-v2', function (Team $team) {
    if ($team->created_at->isAfter(new Carbon('1st Jan, 2023'))) {
        return true;
    }

    if ($team->created_at->isAfter(new Carbon('1st Jan, 2019'))) {
        return Lottery::odds(1 / 100);
    }

    return Lottery::odds(1 / 1000);
});
```

You will notice that the closure we have defined is not expecting a `User`, but is instead expecting a `Team` model. To determine if this feature is active for a user's team, you should pass the team to the `for` method offered by the `Feature` facade:

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect()->to('/billing/v2');
}

// ...
```

The `for` method also accepts an array of scopes, which will check that the feature is active for all of the provided scopes:

```php
Feature::define('improved-notifications', function (string $email) {
    return str_ends_with($email, '@example.com');
});

Feature::for([
    'anthony@example.com',
    'taylor@laravel.com',
])->active('improved-notifications');

// false
```

<a name="default-scope"></a>
### Default Scope

Sometimes, you may need to customize the default scope Pennant uses to check features. For example, maybe all of your features are checked against the currently authenticated user's team instead of the user. Instead of having to call `Feature::for($user->team)` every time you check a feature, you may instead specify the team as the default scope. Typically, this should be done in one of your application's service providers:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::resolveScopeUsing(fn ($driver) => Auth::user()?->team);

        // ...
    }
}
```

If no scope is explicitly provided via the `for` method, the feature check will now use the currently authenticated user's team as the default scope:

```php
Feature::active('billing-v2');

// Is now equivalent to...

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
### Nullable Scope

If the scope you are passing to a feature is potentially `null`, you should account for that in your feature's definition. A `null` scope may occur if you check a feature within an Artisan command, queued job, or unauthenticated route. Since there is usually not an authenticated user in these contexts, the default scope will be `null`.

If you do not always [explictly specify your feature scope](#specifying-the-scope) then you should ensure the scope's type is "nullable" and handle the `null` scope value within your feature definition logic:

```php
use App\Models\User;
use Illuminate\Support\Lottery;
use Laravel\Pennant\Feature;

Feature::define('new-api', fn (User $user) => match (true) {// [tl! remove]
Feature::define('new-api', fn (User|null $user) => match (true) {// [tl! add]
    $user === null => true,// [tl! add]
    $user->isInternalTeamMember() => true,
    $user->isHighTrafficCustomer() => false,
    default => Lottery::odds(1 / 100),
});
```

<a name="identifying-scope"></a>
### Identifying Scope

Pennant's built-in `array` and `database` storage drivers know how to properly store scope identifiers for all PHP data types as well as Eloquent models. However, if your application utilizes a third-party Pennant driver, that driver may not know how to properly store an identifier for an Eloquent model or other custom types in your application.

In light of this, Pennant allows you to format scope values for storage by implementing the `FeatureScopeable` contract on the objects in your application that are used as Pennant scopes.

For example, imagine you are using two different feature drivers in a single application: the built-in `database` driver and a third-party "Flag Rocket" driver. The "Flag Rocket" driver does not know how to properly store an Eloquent model. Instead, it requires a `FlagRocketUser` instance. By implementing the `toFeatureIdentifier` defined by the `FeatureScopeable` contract, we can customize the storable scope value provided to each driver used by our application:

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

Until now, we have primarily shown features as being in a binary state, meaning they are either "active" or "inactive", but Pennant also allows you to store rich values as well.

For example, imagine you are testing three new colors for the "Buy now" button of your application. Instead of returning `true` or `false` from the feature definition, you may instead return a string:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

You may retrieve the value of the `purchase-button` feature using the `value` method:

```php
$color = Feature::value('purchase-button');
```

Pennant's included Blade directive also makes it easy to conditionally render content based on the current value of the feature:

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire' is active -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green' is active -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-orange' is active -->
@endfeature
```

> **Note** When using rich values, it is important to know that a feature is considered "active" when it has any value other than `false`.

<a name="eager-loading"></a>
## Eager Loading

Although Pennant keeps an in-memory cache of all resolved features for a single request, it is still possible to encounter performance issues. To alleviate this, Pennant offers the ability to eager load feature values.

To illustrate this, imagine that we are checking if a feature is active within a loop:

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

Assuming we are using the database driver, this code will execute a database query for every user in the loop - executing potentially hundreds of queries. However, using Pennant's `load` method, we can remove this potential performance bottleneck by eager loading the feature values for a collection of users or scopes:

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

To load feature values only when they have not already been loaded, you may use the `loadMissing` method:

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

<a name="updating-values"></a>
## Updating Values

When a feature's value is resolved for the first time, the underlying driver will store the result in storage. This is often necessary to ensure a consistent experience for your users across requests. However, at times, you may want to manually update the feature's stored value.

To accomplish this, you may use the `activate` and `deactivate` methods to toggle a feature "on" or "off":

```php
use Laravel\Pennant\Feature;

// Activate the feature for the default scope...
Feature::activate('new-api');

// Deactivate the feature for the given scope...
Feature::for($user->team)->deactivate('billing-v2');
```

It is also possible to manually set a rich value for a feature by providing a second argument to the `activate` method:

```php
Feature::activate('purchase-button', 'seafoam-green');
```

To instruct Pennant to forget the stored value for a feature, you may use the `forget` method. When the feature is checked again, Pennant will resolve the feature's value from its feature definition:

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
### Bulk Updates

To update stored feature values in bulk, you may use the `activateForEveryone` and `deactivateForEveryone` methods.

For example, imagine you are now confident in the `new-api` feature's stability and have landed on the best `'purchase-button'` color for your checkout flow - you can update the stored value for all users accordingly:

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

Alternatively, you may deactivate the feature for all users:

```php
Feature::deactivateForEveryone('new-api');
```

> **Note** This will only update the resolved feature values that have been stored by Pennant's storage driver. You will also need to update the feature definition in your application.

<a name="purging-features"></a>
### Purging Features

Sometimes, it can be useful to purge an entire feature from storage. This is typically necessary if you have removed the feature from your application or you have made adjustments to the feature's definition that you would like to rollout to all users.

You may remove all stored values for a feature using the `purge` method:

```php
// Purging a single feature...
Feature::purge('new-api');

// Purging multiple features...
Feature::purge(['new-api', 'purchase-button']);
```

If you would like to purge _all_ features from storage, you may invoke the `purge` method without any arguments:

```php
Feature::purge();
```

As it can be useful to purge features as part of your application's deployment pipeline, Pennant includes a `pennant:purge` Artisan command:

```sh
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

<a name="events"></a>
## Events

Pennant dispatches a variety of events that can be useful when tracking feature flags throughout your application.

### `Laravel\Pennant\Events\RetrievingKnownFeature`

This event is dispatched the first time a known feature is retrieved during a request for a specific scope. This event can be useful to create and track metrics against the feature flags that are being used throughout your application.

### `Laravel\Pennant\Events\RetrievingUnknownFeature`

This event is dispatched the first time an unknown feature is retrieved during a request for a specific scope. This event can be useful if you have intended to remove a feature flag, but may have accidentally left some stray references to it throughout your application.

For example, you may find it useful to listen for this event and `report` or throw an exception when it occurs:

```php
<?php

namespace App\Providers;

use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Event;
use Laravel\Pennant\Events\RetrievingUnknownFeature;

class EventServiceProvider extends ServiceProvider
{
    /**
     * Register any other events for your application.
     */
    public function boot(): void
    {
        Event::listen(function (RetrievingUnknownFeature $event) {
            report("Resolving unknown feature [{$event->feature}].");
        });
    }
}
```

### `Laravel\Pennant\Events\DynamicallyDefiningFeature`

This event is dispatched when a class based feature is being dynamically checked for the first time during a request.
