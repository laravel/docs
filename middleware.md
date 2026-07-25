---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Middleware

- [Вступ](#introduction)
- [Визначення middleware](#defining-middleware)
- [Реєстрація middleware](#registering-middleware)
    - [Глобальні middleware](#global-middleware)
    - [Призначення middleware маршрутам](#assigning-middleware-to-routes)
    - [Групи middleware](#middleware-groups)
    - [Псевдоніми middleware](#middleware-aliases)
    - [Впорядкування middleware](#sorting-middleware)
- [Параметри middleware](#middleware-parameters)
- [Завершувані middleware](#terminable-middleware)

<a name="introduction"></a>
## Вступ

`Middleware` дають зручний механізм для перевірки та фільтрації HTTP-запитів, що надходять до вашого застосунку. Наприклад, Laravel містить `middleware`, який перевіряє, чи автентифікований користувач вашого застосунку. Якщо ні - `middleware` перенаправить користувача на екран входу. Якщо ж користувач автентифікований, `middleware` дозволить запиту рухатися далі вглиб застосунку.

Додаткові `middleware` можна писати для найрізноманітніших завдань, окрім автентифікації. Наприклад, `middleware` логування може записувати всі вхідні запити до вашого застосунку. Laravel містить чимало `middleware`, зокрема для автентифікації та захисту від CSRF; утім, усі визначені вами `middleware` зазвичай розташовані в каталозі `app/Http/Middleware` вашого застосунку.

<a name="defining-middleware"></a>
## Визначення middleware

Щоб створити новий `middleware`, скористайтеся командою Artisan `make:middleware`:

```shell
php artisan make:middleware EnsureTokenIsValid
```

Ця команда помістить новий клас `EnsureTokenIsValid` до каталогу `app/Http/Middleware`. У цьому `middleware` ми дозволимо доступ до маршруту лише тоді, коли переданий вхідний параметр `token` збігається з визначеним значенням. Інакше ми перенаправимо користувачів назад на URI `/home`:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureTokenIsValid
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->input('token') !== 'my-secret-token') {
            return redirect('/home');
        }

        return $next($request);
    }
}
```

Як бачите, якщо переданий `token` не збігається з нашим секретним токеном, `middleware` поверне клієнту HTTP-перенаправлення; інакше запит буде передано далі вглиб застосунку. Щоб передати запит глибше (тобто дозволити `middleware` «пропустити» його), викличте колбек `$next` із `$request`.

Найкраще уявляти `middleware` як низку «шарів», крізь які HTTP-запити мають пройти, перш ніж потраплять до вашого застосунку. Кожен шар може перевірити запит і навіть цілком його відхилити.

> [!NOTE]
> Усі `middleware` розв'язуються через [сервіс-контейнер](/docs/{{version}}/container), тож ви можете вказати типи будь-яких потрібних залежностей у конструкторі `middleware`.

<a name="middleware-and-responses"></a>
#### Middleware та відповіді

Звісно, `middleware` може виконувати завдання до або після передавання запиту глибше в застосунок. Наприклад, наведений нижче `middleware` виконає певне завдання **перед** тим, як застосунок обробить запит:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class BeforeMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        // Perform action

        return $next($request);
    }
}
```

Натомість цей `middleware` виконає своє завдання **після** того, як застосунок обробить запит:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class AfterMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);

        // Perform action

        return $response;
    }
}
```

<a name="registering-middleware"></a>
## Реєстрація middleware

<a name="global-middleware"></a>
### Глобальні middleware

Якщо ви хочете, щоб `middleware` виконувався під час кожного HTTP-запиту до вашого застосунку, додайте його до глобального стека `middleware` у файлі `bootstrap/app.php`:

```php
use App\Http\Middleware\EnsureTokenIsValid;

->withMiddleware(function (Middleware $middleware): void {
     $middleware->append(EnsureTokenIsValid::class);
})
```

Об'єкт `$middleware`, переданий замиканню `withMiddleware`, є екземпляром `Illuminate\Foundation\Configuration\Middleware` і відповідає за керування `middleware`, призначеними маршрутам вашого застосунку. Метод `append` додає `middleware` у кінець списку глобальних. Якщо ви хочете додати `middleware` на початок списку, скористайтеся методом `prepend`.

<a name="manually-managing-laravels-default-global-middleware"></a>
#### Ручне керування типовими глобальними middleware Laravel

Якщо ви хочете керувати глобальним стеком `middleware` Laravel вручну, передайте типовий стек методу `use`. Далі ви можете коригувати його за потреби:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->use([
        \Illuminate\Foundation\Http\Middleware\InvokeDeferredCallbacks::class,
        // \Illuminate\Http\Middleware\TrustHosts::class,
        \Illuminate\Http\Middleware\TrustProxies::class,
        \Illuminate\Http\Middleware\HandleCors::class,
        \Illuminate\Foundation\Http\Middleware\PreventRequestsDuringMaintenance::class,
        \Illuminate\Http\Middleware\ValidatePostSize::class,
        \Illuminate\Foundation\Http\Middleware\TrimStrings::class,
        \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
    ]);
})
```

<a name="assigning-middleware-to-routes"></a>
### Призначення middleware маршрутам

Якщо ви хочете призначити `middleware` конкретним маршрутам, викличте метод `middleware` під час визначення маршруту:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    // ...
})->middleware(EnsureTokenIsValid::class);
```

Ви можете призначити маршруту кілька `middleware`, передавши методу `middleware` масив їхніх імен:

```php
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<a name="excluding-middleware"></a>
#### Виключення middleware

Призначаючи `middleware` групі маршрутів, ви подекуди можете захотіти не застосовувати його до окремого маршруту в межах цієї групи. Це робиться методом `withoutMiddleware`:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::middleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/', function () {
        // ...
    });

    Route::get('/profile', function () {
        // ...
    })->withoutMiddleware([EnsureTokenIsValid::class]);
});
```

Ви також можете виключити певний набір `middleware` для цілої [групи](/docs/{{version}}/routing#route-groups) визначень маршрутів:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        // ...
    });
});
```

Метод `withoutMiddleware` може прибирати лише `middleware` маршрутів і не діє на [глобальні `middleware`](#global-middleware).

<a name="middleware-groups"></a>
### Групи middleware

Іноді вам може знадобитися згрупувати кілька `middleware` під одним ключем, щоб їх було зручніше призначати маршрутам. Це робиться методом `appendToGroup` у файлі `bootstrap/app.php` вашого застосунку:

```php
use App\Http\Middleware\First;
use App\Http\Middleware\Second;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->appendToGroup('group-name', [
        First::class,
        Second::class,
    ]);

    $middleware->prependToGroup('group-name', [
        First::class,
        Second::class,
    ]);
})
```

Групи `middleware` можна призначати маршрутам і діям контролерів тим самим синтаксисом, що й окремі `middleware`:

```php
Route::get('/', function () {
    // ...
})->middleware('group-name');

Route::middleware(['group-name'])->group(function () {
    // ...
});
```

<a name="laravels-default-middleware-groups"></a>
#### Типові групи middleware Laravel

Laravel містить наперед визначені групи `middleware` `web` та `api` із поширеними `middleware`, які ви можете захотіти застосувати до своїх веб- та API-маршрутів. Пам'ятайте: Laravel автоматично застосовує ці групи до відповідних файлів `routes/web.php` і `routes/api.php`:

<div class="overflow-auto">

| Група `middleware` `web`                                  |
| --------------------------------------------------------- |
| `Illuminate\Cookie\Middleware\EncryptCookies`             |
| `Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse` |
| `Illuminate\Session\Middleware\StartSession`              |
| `Illuminate\View\Middleware\ShareErrorsFromSession`       |
| `Illuminate\Foundation\Http\Middleware\PreventRequestForgery` |
| `Illuminate\Routing\Middleware\SubstituteBindings`        |

</div>

<div class="overflow-auto">

| Група `middleware` `api`                           |
| -------------------------------------------------- |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

</div>

Якщо ви хочете додати `middleware` в кінець чи на початок цих груп, скористайтеся методами `web` та `api` у файлі `bootstrap/app.php`. Вони є зручною альтернативою методу `appendToGroup`:

```php
use App\Http\Middleware\EnsureTokenIsValid;
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [
        EnsureUserIsSubscribed::class,
    ]);

    $middleware->api(prepend: [
        EnsureTokenIsValid::class,
    ]);
})
```

Ви можете навіть замінити один із записів типової групи `middleware` Laravel власним:

```php
use App\Http\Middleware\StartCustomSession;
use Illuminate\Session\Middleware\StartSession;

$middleware->web(replace: [
    StartSession::class => StartCustomSession::class,
]);
```

Або ж цілком прибрати `middleware`:

```php
$middleware->web(remove: [
    StartSession::class,
]);
```

<a name="manually-managing-laravels-default-middleware-groups"></a>
#### Ручне керування типовими групами middleware Laravel

Якщо ви хочете вручну керувати всіма `middleware` у типових групах `web` та `api`, ви можете повністю перевизначити ці групи. Приклад нижче визначає групи `web` та `api` з їхніми типовими `middleware`, дозволяючи налаштувати їх за потреби:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->group('web', [
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Foundation\Http\Middleware\PreventRequestForgery::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        // \Illuminate\Session\Middleware\AuthenticateSession::class,
    ]);

    $middleware->group('api', [
        // \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        // 'throttle:api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ]);
})
```

> [!NOTE]
> За замовчуванням групи `middleware` `web` та `api` автоматично застосовуються до відповідних файлів `routes/web.php` і `routes/api.php` вашого застосунку через файл `bootstrap/app.php`.

<a name="middleware-aliases"></a>
### Псевдоніми middleware

Ви можете призначати `middleware` псевдоніми у файлі `bootstrap/app.php` вашого застосунку. Псевдоніми дозволяють визначити коротку назву для класу `middleware`, що особливо корисно для `middleware` з довгими іменами класів:

```php
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class
    ]);
})
```

Щойно псевдонім визначено у файлі `bootstrap/app.php`, ви можете використовувати його, призначаючи `middleware` маршрутам:

```php
Route::get('/profile', function () {
    // ...
})->middleware('subscribed');
```

Для зручності деякі вбудовані `middleware` Laravel мають псевдоніми за замовчуванням. Наприклад, `auth` - це псевдонім для `middleware` `Illuminate\Auth\Middleware\Authenticate`. Нижче наведено список типових псевдонімів:

<div class="overflow-auto">

| Псевдонім          | Middleware                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------- |
| `auth`             | `Illuminate\Auth\Middleware\Authenticate`                                                                     |
| `auth.basic`       | `Illuminate\Auth\Middleware\AuthenticateWithBasicAuth`                                                        |
| `auth.session`     | `Illuminate\Session\Middleware\AuthenticateSession`                                                           |
| `cache.headers`    | `Illuminate\Http\Middleware\SetCacheHeaders`                                                                  |
| `can`              | `Illuminate\Auth\Middleware\Authorize`                                                                        |
| `guest`            | `Illuminate\Auth\Middleware\RedirectIfAuthenticated`                                                          |
| `password.confirm` | `Illuminate\Auth\Middleware\RequirePassword`                                                                  |
| `precognitive`     | `Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests`                                            |
| `signed`           | `Illuminate\Routing\Middleware\ValidateSignature`                                                             |
| `subscribed`       | `\Spark\Http\Middleware\VerifyBillableIsSubscribed`                                                           |
| `throttle`         | `Illuminate\Routing\Middleware\ThrottleRequests` or `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` |
| `verified`         | `Illuminate\Auth\Middleware\EnsureEmailIsVerified`                                                            |

</div>

<a name="sorting-middleware"></a>
### Впорядкування middleware

Зрідка вам може знадобитися, щоб ваші `middleware` виконувалися в певному порядку, але ви не маєте контролю над їхнім порядком під час призначення маршруту. У таких випадках ви можете задати пріоритет `middleware` методом `priority` у файлі `bootstrap/app.php` вашого застосунку:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->priority([
        \Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests::class,
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Foundation\Http\Middleware\PreventRequestForgery::class,
        \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        \Illuminate\Routing\Middleware\ThrottleRequests::class,
        \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        \Illuminate\Contracts\Auth\Middleware\AuthenticatesRequests::class,
        \Illuminate\Auth\Middleware\Authorize::class,
    ]);
})
```

<a name="middleware-parameters"></a>
## Параметри middleware

`Middleware` можуть також отримувати додаткові параметри. Наприклад, якщо вашому застосунку потрібно перевірити, чи має автентифікований користувач певну «роль», перш ніж виконати дію, ви можете створити `middleware` `EnsureUserHasRole`, який отримує ім'я ролі як додатковий аргумент.

Додаткові параметри передаються `middleware` після аргументу `$next`:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserHasRole
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next, string $role): Response
    {
        if (! $request->user()->hasRole($role)) {
            // Redirect...
        }

        return $next($request);
    }
}
```

Параметри `middleware` можна вказати під час визначення маршруту, відокремивши ім'я `middleware` від параметрів двокрапкою `:`:

```php
use App\Http\Middleware\EnsureUserHasRole;

Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor');
```

Кілька параметрів розділяються комами:

```php
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor,publisher');
```

<a name="terminable-middleware"></a>
## Завершувані middleware

Іноді `middleware` може знадобитися виконати певну роботу після того, як HTTP-відповідь надіслано браузеру. Якщо ви визначите у своєму `middleware` метод `terminate`, а ваш веб-сервер використовує [FastCGI](https://www.php.net/manual/en/install.fpm.php), метод `terminate` буде автоматично викликано після надсилання відповіді браузеру:

```php
<?php

namespace Illuminate\Session\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class TerminatingMiddleware
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return $next($request);
    }

    /**
     * Handle tasks after the response has been sent to the browser.
     */
    public function terminate(Request $request, Response $response): void
    {
        // ...
    }
}
```

Метод `terminate` має отримувати і запит, і відповідь. Визначивши завершуваний `middleware`, додайте його до списку маршрутних чи глобальних `middleware` у файлі `bootstrap/app.php` вашого застосунку.

Викликаючи метод `terminate` вашого `middleware`, Laravel розв'яже з [сервіс-контейнера](/docs/{{version}}/container) новий екземпляр `middleware`. Якщо ви хочете використовувати той самий екземпляр під час викликів методів `handle` і `terminate`, зареєструйте `middleware` в контейнері методом `singleton`. Зазвичай це варто робити в методі `register` вашого `AppServiceProvider`:

```php
use App\Http\Middleware\TerminatingMiddleware;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(TerminatingMiddleware::class);
}
```
