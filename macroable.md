# Macros & Mixins

- [Introduction](#introduction)
- [Collection Macros](#collection-macros)
    - [Macro Arguments](#macro-arguments)
- [Response Macros](#response-macros)
- [HTTP client Macros](#http-client-macros)
- [Packages, that support macros](#packages)
- [Mixins](#mixins)

<a name="introduction"></a>
## Introduction

Several classes in Laravel are "macroable", which allows you to add additional methods to them at run time via the `Illuminate\Support\Traits\Macroable` trait:

- [`Illuminate\Support\Facades\Facade`](/docs/{{version}}/facades)
- [`Illuminate\Support\Collection`](/docs/{{version}}/collections)
- `Illuminate\Database\Schema\Blueprint`

The `macro` method accepts a closure that will be executed when your macro is called. The macro closure may access the classes other methods via `$this`, just as if it were a real method of the class. The `macro` function accepts a name as its first argument and a closure as its second argument.

Typically, you should declare macros in the `boot` method of a [service provider](/docs/{{version}}/providers).

<a name="collection-macros"></a>
## Collection Macros

For example, the following code adds a `toUpper` method to the `Collection` class:

```php
namespace App\Providers;

use Illuminate\Support\Collection; // [tl! focus]
use Illuminate\Support\Str; // [tl! focus]
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Collection::macro('toUpper', function () { // [tl! focus:start]
            return $this->map(function (string $value) {
                return Str::upper($value);
            });
        }); // [tl! focus:end]
    }
}

// …

$collection = collect(['first', 'second']);  // [tl! focus]
$upper = $collection->toUpper(); // ['FIRST', 'SECOND'] [tl! focus]
```

<a name="macro-arguments"></a>
### Macro Arguments

If necessary, you may define macros that accept additional arguments:

```php
namespace App\Providers;

use Illuminate\Support\Collection; // [tl! focus]
use Illuminate\Support\Facades\Lang; // [tl! focus]
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Collection::macro('toLocale', function (string $locale) { // [tl! focus:start]
            return $this->map(function (string $value) use ($locale) {
                return Lang::get($value, [], $locale);
            });
        }); // [tl! focus:end]
     }
}

// …

$collection = collect(['first', 'second']); // [tl! focus]
$translated = $collection->toLocale('es'); // [tl! focus]
```

<a name="response-macros"></a>
## Response Macros

If you would like to define a custom response that you can re-use in a variety of your routes and controllers, you may use the `macro` method on the `Response` facade:

```php
namespace App\Providers;

use Illuminate\Support\Facades\Response; // [tl! focus]
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Response::macro('caps', function (string $value) { // [tl! focus:start]
            return Response::make(strtoupper($value));
        }); // [tl! focus:end]
     }
}
```

The macro's closure will be executed when calling the macro name from a `ResponseFactory` implementation or the `response` helper:

```php
return response()->caps('foo');
```

<a name="http-client-macros"></a>
## HTTP client Macros

The Laravel HTTP client allows you to define "macros", which can serve as a fluent, expressive mechanism to configure common request paths and headers when interacting with services throughout your application:

```php
namespace App\Providers;

use Illuminate\Support\Facades\Http; // [tl! focus]
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Http::macro('github', function () { // [tl! focus:start]
            return Http::withHeaders([
                'X-Example' => 'example',
            ])->baseUrl('https://github.com');
        }); // [tl! focus:end]
    }
}
```

Once your macro has been configured, you may invoke it from anywhere in your application to create a pending request with the specified configuration:

```php
$response = Http::github()->get('/');
```

<a name="packages"></a>
## Packages, that support macros

* [Carbon](https://carbon.nesbot.com/docs/#api-macro)

<a name="mixins"></a>
## Mixins
Mixins have similar functionality to macros, yet they are registered a little different. When you want to add more than just one or two macros, mixins might be the better choice. Mixins are classes whose methods are added to the class they are mixed into.

```php tab=Definition
namespace App\Mixins;

class CasingMixin
{
    public function toUpper()
    {
        return function () {
            return $this->map(function (string $value) {
                return Str::upper($value);
            });
        };
    }

    public function toLower()
    {
        return function () {
            return $this->map(function (string $value) {
                return Str::lower($value);
            });
        };
    }
}
```

```php tab=Registration
namespace App\Providers;

use App\Mixin\CasingMixin; // [tl! focus]
use Illuminate\Support\Collection; // [tl! focus]
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Collection::mixin(new CasingMixin()); // [tl! focus]
    }
}
```

```php tab=Use
$collection = collect([ 'lOrEm', 'iPsUm' ]);
$collection->toUpper(); // [ 'LOREM', 'IPSUM' ]
$collection->toLower(); // [ 'lorem', 'ipsum' ]
```
