---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Обробка помилок

- [Вступ](#introduction)
- [Конфігурація](#configuration)
- [Обробка винятків](#handling-exceptions)
    - [Звітування про винятки](#reporting-exceptions)
    - [Рівні логування винятків](#exception-log-levels)
    - [Ігнорування винятків за типом](#ignoring-exceptions-by-type)
    - [Рендеринг винятків](#rendering-exceptions)
    - [Винятки зі звітуванням і рендерингом](#renderable-exceptions)
- [Обмеження частоти звітування про винятки](#throttling-reported-exceptions)
- [HTTP-винятки](#http-exceptions)
    - [Власні сторінки HTTP-помилок](#custom-http-error-pages)

<a name="introduction"></a>
## Вступ

Коли ви розпочинаєте новий проєкт Laravel, обробку помилок і винятків уже налаштовано за вас; утім, будь-коли ви можете скористатися методом `withExceptions` у файлі `bootstrap/app.php` вашого застосунку, щоб керувати тим, як застосунок звітує про винятки та рендерить їх.

Об'єкт `$exceptions`, переданий замиканню `withExceptions`, є екземпляром `Illuminate\Foundation\Configuration\Exceptions` і відповідає за керування обробкою винятків у вашому застосунку. Ми глибше розглянемо цей об'єкт далі в документації.

<a name="configuration"></a>
## Конфігурація

Опція `debug` у вашому конфігураційному файлі `config/app.php` визначає, скільки інформації про помилку насправді показується користувачеві. За замовчуванням ця опція налаштована на значення змінної середовища `APP_DEBUG`, яка зберігається у вашому файлі `.env`.

Під час локальної розробки змінній середовища `APP_DEBUG` варто задати значення `true`.

> [!WARNING]
> У продакшен-середовищі значення `APP_DEBUG` завжди має бути `false`. Якщо в продакшені воно матиме значення `true`, ви ризикуєте розкрити конфіденційні значення конфігурації кінцевим користувачам вашого застосунку.

<a name="handling-exceptions"></a>
## Обробка винятків

<a name="reporting-exceptions"></a>
### Звітування про винятки

У Laravel звітування про винятки використовується, щоб логувати їх або надсилати до зовнішнього сервісу на кшталт [Laravel Nightwatch](https://nightwatch.laravel.com), [Sentry](https://github.com/getsentry/sentry-laravel) чи [Flare](https://flareapp.io). За замовчуванням винятки логуються відповідно до вашої конфігурації [логування](/docs/{{version}}/logging). Утім, ви вільні логувати їх як завгодно.

Якщо вам потрібно звітувати про різні типи винятків по-різному, скористайтеся методом винятків `report` у файлі `bootstrap/app.php`, щоб зареєструвати замикання, яке має виконуватися, коли потрібно відзвітувати про виняток певного типу. Laravel визначить тип винятку, про який звітує замикання, за вказаним у ньому типом:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

Коли ви реєструєте власний колбек звітування методом `report`, Laravel усе одно логуватиме виняток за типовою конфігурацією логування застосунку. Якщо ви хочете зупинити поширення винятку до типового стека логування, скористайтеся методом `stop` під час визначення колбека або поверніть із нього `false`:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    })->stop();

    $exceptions->report(function (InvalidOrderException $e) {
        return false;
    });
})
```

> [!NOTE]
> Щоб налаштувати звітування для конкретного винятку, ви також можете скористатися [винятками зі звітуванням](/docs/{{version}}/errors#renderable-exceptions).

<a name="global-log-context"></a>
#### Глобальний контекст логів

Якщо він доступний, Laravel автоматично додає ідентифікатор поточного користувача до повідомлення логу кожного винятку як контекстні дані. Ви можете визначити власні глобальні контекстні дані методом винятків `context` у файлі `bootstrap/app.php`. Цю інформацію буде додано до кожного повідомлення логу про виняток, що його записує ваш застосунок:

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->context(fn () => [
        'foo' => 'bar',
    ]);
})
```

<a name="exception-log-context"></a>
#### Контекст логу винятку

Хоча додавати контекст до кожного повідомлення логу корисно, іноді конкретний виняток має унікальний контекст, який ви хотіли б бачити у логах. Визначивши метод `context` в одному з винятків вашого застосунку, ви можете вказати будь-які дані, доречні для цього винятку, які слід додати до його запису в логу:

```php
<?php

namespace App\Exceptions;

use Exception;

class InvalidOrderException extends Exception
{
    // ...

    /**
     * Get the exception's context information.
     *
     * @return array<string, mixed>
     */
    public function context(): array
    {
        return ['order_id' => $this->orderId];
    }
}
```

<a name="the-report-helper"></a>
#### Хелпер `report`

Іноді вам може знадобитися відзвітувати про виняток, але продовжити обробку поточного запиту. Функція-хелпер `report` дозволяє швидко відзвітувати про виняток, не рендерячи користувачеві сторінку помилки:

```php
public function isValid(string $value): bool
{
    try {
        // Validate the value...
    } catch (Throwable $e) {
        report($e);

        return false;
    }
}
```

<a name="deduplicating-reported-exceptions"></a>
#### Усунення дублікатів у звітах про винятки

Якщо ви використовуєте функцію `report` у всьому застосунку, ви можете подекуди відзвітувати про той самий виняток кілька разів, створивши дублікати записів у логах.

Якщо ви хочете, щоб про кожен окремий екземпляр винятку звітувалося лише раз, викличте метод винятків `dontReportDuplicates` у файлі `bootstrap/app.php` вашого застосунку:

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReportDuplicates();
})
```

Тепер, коли хелпер `report` викликається з тим самим екземпляром винятку, буде відзвітовано лише перший виклик:

```php
$original = new RuntimeException('Whoops!');

report($original); // reported

try {
    throw $original;
} catch (Throwable $caught) {
    report($caught); // ignored
}

report($original); // ignored
report($caught); // ignored
```

<a name="exception-log-levels"></a>
### Рівні логування винятків

Коли повідомлення записуються до [логів](/docs/{{version}}/logging) вашого застосунку, вони записуються на визначеному [рівні логування](/docs/{{version}}/logging#log-levels), що вказує на серйозність чи важливість повідомлення.

Як зазначено вище, навіть коли ви реєструєте власний колбек звітування методом `report`, Laravel усе одно логуватиме виняток за типовою конфігурацією логування; однак оскільки рівень логування іноді впливає на канали, до яких потрапляє повідомлення, ви можете захотіти налаштувати рівень, на якому логуються певні винятки.

Для цього скористайтеся методом винятків `level` у файлі `bootstrap/app.php`. Він приймає тип винятку першим аргументом і рівень логування другим:

```php
use PDOException;
use Psr\Log\LogLevel;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->level(PDOException::class, LogLevel::CRITICAL);
})
```

<a name="ignoring-exceptions-by-type"></a>
### Ігнорування винятків за типом

Створюючи застосунок, ви матимете типи винятків, про які ніколи не захочете звітувати. Щоб ігнорувати їх, скористайтеся методом винятків `dontReport` у файлі `bootstrap/app.php`. Про будь-який клас, переданий цьому методу, ніколи не звітуватиметься; утім, він усе ще може мати власну логіку рендерингу:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReport([
        InvalidOrderException::class,
    ]);
})
```

Як альтернативу ви можете просто «позначити» клас винятку інтерфейсом `Illuminate\Contracts\Debug\ShouldntReport`. Коли виняток позначено цим інтерфейсом, обробник винятків Laravel ніколи про нього не звітуватиме:

```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Contracts\Debug\ShouldntReport;

class PodcastProcessingException extends Exception implements ShouldntReport
{
    //
}
```

Якщо вам потрібен ще більший контроль над тим, коли ігнорується певний тип винятку, передайте замикання методу `dontReportWhen`:

```php
use App\Exceptions\InvalidOrderException;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReportWhen(function (Throwable $e) {
        return $e instanceof PodcastProcessingException &&
               $e->reason() === 'Subscription expired';
    });
})
```

Внутрішньо Laravel уже ігнорує деякі типи помилок за вас - як-от винятки від HTTP-помилок 404, відповідей 403 через розбіжність джерела чи відповідей 419 через недійсні CSRF-токени. Якщо ви хочете вказати Laravel припинити ігнорувати певний тип винятку, скористайтеся методом винятків `stopIgnoring` у файлі `bootstrap/app.php`:

```php
use Symfony\Component\HttpKernel\Exception\HttpException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->stopIgnoring(HttpException::class);
})
```

<a name="rendering-exceptions"></a>
### Рендеринг винятків

За замовчуванням обробник винятків Laravel перетворює винятки на HTTP-відповідь за вас. Однак ви вільні зареєструвати власне замикання рендерингу для винятків певного типу. Це робиться методом винятків `render` у файлі `bootstrap/app.php` вашого застосунку.

Замикання, передане методу `render`, має повертати екземпляр `Illuminate\Http\Response`, який можна створити хелпером `response`. Laravel визначить тип винятку, який рендерить замикання, за вказаним у ньому типом:

```php
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', status: 500);
    });
})
```

Ви також можете скористатися методом `render`, щоб перевизначити поведінку рендерингу вбудованих винятків Laravel чи Symfony - як-от `NotFoundHttpException`. Якщо передане методу `render` замикання не повертає значення, буде використано типовий рендеринг винятків Laravel:

```php
use Illuminate\Http\Request;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (NotFoundHttpException $e, Request $request) {
        if ($request->is('api/*')) {
            return response()->json([
                'message' => 'Record not found.'
            ], 404);
        }
    });
})
```

<a name="rendering-exceptions-as-json"></a>
#### Рендеринг винятків у форматі JSON

Рендерячи виняток, Laravel автоматично визначає, чи слід віддати його як HTML- чи JSON-відповідь, спираючись на заголовок `Accept` запиту. Якщо ви хочете налаштувати, як саме Laravel це вирішує, скористайтеся методом `shouldRenderJsonWhen`:

```php
use Illuminate\Http\Request;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->shouldRenderJsonWhen(function (Request $request, Throwable $e) {
        if ($request->is('admin/*')) {
            return true;
        }

        return $request->expectsJson();
    });
})
```

<a name="customizing-the-exception-response"></a>
#### Налаштування відповіді для винятку

Зрідка вам може знадобитися налаштувати всю HTTP-відповідь, яку рендерить обробник винятків Laravel. Для цього зареєструйте замикання налаштування відповіді методом `respond`:

```php
use Symfony\Component\HttpFoundation\Response;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->respond(function (Response $response) {
        if ($response->getStatusCode() === 419) {
            return back()->with([
                'message' => 'The page expired, please try again.',
            ]);
        }

        return $response;
    });
})
```

<a name="renderable-exceptions"></a>
### Винятки зі звітуванням і рендерингом

Замість визначати власну поведінку звітування та рендерингу у файлі `bootstrap/app.php`, ви можете визначити методи `report` і `render` безпосередньо у винятках свого застосунку. Коли ці методи існують, фреймворк викликатиме їх автоматично:

```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class InvalidOrderException extends Exception
{
    /**
     * Report the exception.
     */
    public function report(): void
    {
        // ...
    }

    /**
     * Render the exception as an HTTP response.
     */
    public function render(Request $request): Response
    {
        return response(/* ... */);
    }
}
```

Якщо ваш виняток успадковує виняток, який уже підлягає рендерингу - як-от вбудований виняток Laravel чи Symfony, - ви можете повернути `false` з методу `render`, щоб відрендерити типову HTTP-відповідь цього винятку:

```php
/**
 * Render the exception as an HTTP response.
 */
public function render(Request $request): Response|bool
{
    if (/** Determine if the exception needs custom rendering */) {

        return response(/* ... */);
    }

    return false;
}
```

Якщо ваш виняток містить власну логіку звітування, потрібну лише за певних умов, вам може знадобитися вказати Laravel іноді звітувати про виняток за типовою конфігурацією обробки. Для цього поверніть `false` з методу `report` винятку:

```php
/**
 * Report the exception.
 */
public function report(): bool
{
    if (/** Determine if the exception needs custom reporting */) {

        // ...

        return true;
    }

    return false;
}
```

> [!NOTE]
> Ви можете вказати типи будь-яких потрібних залежностей методу `report`, і [сервіс-контейнер](/docs/{{version}}/container) Laravel автоматично впровадить їх у метод.

<a name="throttling-reported-exceptions"></a>
### Обмеження частоти звітування про винятки

Якщо ваш застосунок звітує про дуже велику кількість винятків, ви можете захотіти обмежити, скільки з них справді логується чи надсилається до зовнішнього сервісу відстеження помилок.

Щоб брати випадкову вибірку винятків, скористайтеся методом винятків `throttle` у файлі `bootstrap/app.php`. Метод `throttle` приймає замикання, яке має повертати екземпляр `Lottery`:

```php
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        return Lottery::odds(1, 1000);
    });
})
```

Вибірку можна робити й умовно, залежно від типу винятку. Якщо ви хочете брати вибірку лише для екземплярів конкретного класу, повертайте `Lottery` тільки для нього:

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof ApiMonitoringException) {
            return Lottery::odds(1, 1000);
        }
    });
})
```

Ви також можете обмежити частоту винятків, які логуються чи надсилаються до зовнішнього сервісу відстеження помилок, повернувши екземпляр `Limit` замість `Lottery`. Це корисно, якщо ви хочете захиститися від раптових сплесків винятків, що заповнюють ваші логи, - наприклад, коли сторонній сервіс, який використовує ваш застосунок, недоступний:

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof BroadcastException) {
            return Limit::perMinute(300);
        }
    });
})
```

За замовчуванням обмеження використовують клас винятку як ключ. Ви можете налаштувати це, вказавши власний ключ методом `by` на `Limit`:

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof BroadcastException) {
            return Limit::perMinute(300)->by($e->getMessage());
        }
    });
})
```

Звісно, ви можете повертати поєднання екземплярів `Lottery` та `Limit` для різних винятків:

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        return match (true) {
            $e instanceof BroadcastException => Limit::perMinute(300),
            $e instanceof ApiMonitoringException => Lottery::odds(1, 1000),
            default => Limit::none(),
        };
    });
})
```

<a name="http-exceptions"></a>
## HTTP-винятки

Деякі винятки описують коди HTTP-помилок від сервера. Наприклад, це може бути помилка «сторінку не знайдено» (404), «неавторизовано» (401) чи навіть згенерована розробником помилка 500. Щоб згенерувати таку відповідь із будь-якого місця застосунку, скористайтеся хелпером `abort`:

```php
abort(404);
```

<a name="custom-http-error-pages"></a>
### Власні сторінки HTTP-помилок

Laravel спрощує показ власних сторінок помилок для різних HTTP-статусів. Наприклад, щоб налаштувати сторінку помилки для статусу 404, створіть шаблон представлення `resources/views/errors/404.blade.php`. Це представлення рендеритиметься для всіх помилок 404, згенерованих вашим застосунком. Представлення в цьому каталозі мають називатися відповідно до HTTP-статусу, якому вони відповідають. Екземпляр `Symfony\Component\HttpKernel\Exception\HttpException`, створений функцією `abort`, буде передано представленню як змінну `$exception`:

```blade
<h2>{{ $exception->getMessage() }}</h2>
```

Ви можете опублікувати типові шаблони сторінок помилок Laravel командою Artisan `vendor:publish`. Опублікувавши шаблони, ви можете налаштувати їх на свій смак:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### Резервні сторінки HTTP-помилок

Ви також можете визначити «резервну» сторінку помилки для певної серії HTTP-статусів. Вона рендеритиметься, якщо для конкретного статусу немає відповідної сторінки. Для цього визначте шаблони `4xx.blade.php` і `5xx.blade.php` у каталозі `resources/views/errors` вашого застосунку.

Резервні сторінки не впливатимуть на відповіді з помилками `404`, `500` і `503`, оскільки Laravel має внутрішні спеціальні сторінки для цих статусів. Щоб налаштувати сторінки для них, визначте власну сторінку помилки для кожного окремо.
