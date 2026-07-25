---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Сервіс-провайдери

- [Вступ](#introduction)
- [Написання сервіс-провайдерів](#writing-service-providers)
    - [Метод register](#the-register-method)
    - [Метод boot](#the-boot-method)
- [Реєстрація провайдерів](#registering-providers)
- [Відкладені провайдери](#deferred-providers)

<a name="introduction"></a>
## Вступ

Сервіс-провайдери - центральне місце завантаження всього застосунку Laravel. І ваш власний застосунок, і всі базові сервіси Laravel завантажуються саме через сервіс-провайдери.

Але що ми маємо на увазі під «завантаженням»? Загалом - **реєстрацію** речей: прив'язок сервіс-контейнера, слухачів подій, `middleware` і навіть маршрутів. Сервіс-провайдери є центральним місцем налаштування вашого застосунку.

Внутрішньо Laravel використовує десятки сервіс-провайдерів, щоб завантажити свої базові сервіси - поштовий модуль, черги, кеш тощо. Багато з цих провайдерів «відкладені», тобто вони завантажуються не на кожному запиті, а лише тоді, коли сервіси, які вони надають, справді потрібні.

Усі визначені вами сервіс-провайдери реєструються у файлі `bootstrap/providers.php`. Далі в документації ви дізнаєтеся, як писати власні сервіс-провайдери та реєструвати їх у своєму застосунку Laravel.

> [!NOTE]
> Якщо ви хочете дізнатися більше про те, як Laravel обробляє запити й працює всередині, перегляньте нашу документацію про [життєвий цикл запиту](/docs/{{version}}/lifecycle).

<a name="writing-service-providers"></a>
## Написання сервіс-провайдерів

Усі сервіс-провайдери успадковують клас `Illuminate\Support\ServiceProvider`. Більшість сервіс-провайдерів містять методи `register` і `boot`. У методі `register` слід **лише прив'язувати речі до [сервіс-контейнера](/docs/{{version}}/container)**. Ніколи не намагайтеся реєструвати в методі `register` слухачів подій, маршрути чи будь-яку іншу функціональність.

Artisan CLI може згенерувати новий провайдер командою `make:provider`. Laravel автоматично зареєструє ваш новий провайдер у файлі `bootstrap/providers.php` вашого застосунку:

```shell
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
### Метод register

Як згадувалося раніше, у методі `register` слід лише прив'язувати речі до [сервіс-контейнера](/docs/{{version}}/container). Ніколи не намагайтеся реєструвати там слухачів подій, маршрути чи будь-яку іншу функціональність. Інакше ви можете випадково скористатися сервісом, який надає ще не завантажений сервіс-провайдер.

Погляньмо на простий сервіс-провайдер. У будь-якому з його методів вам завжди доступна властивість `$app`, що дає доступ до сервіс-контейнера:

```php
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->singleton(Connection::class, function (Application $app) {
            return new Connection(config('riak'));
        });
    }
}
```

Цей сервіс-провайдер визначає лише метод `register` і використовує його, щоб визначити реалізацію `App\Services\Riak\Connection` у сервіс-контейнері. Якщо ви ще не знайомі із сервіс-контейнером Laravel, перегляньте [його документацію](/docs/{{version}}/container).

<a name="the-bindings-and-singletons-properties"></a>
#### Властивості `bindings` і `singletons`

Якщо ваш сервіс-провайдер реєструє багато простих прив'язок, ви можете скористатися властивостями `bindings` і `singletons` замість того, щоб реєструвати кожну прив'язку контейнера вручну. Коли фреймворк завантажує сервіс-провайдер, він автоматично перевіряє ці властивості й реєструє їхні прив'язки:

```php
<?php

namespace App\Providers;

use App\Contracts\DowntimeNotifier;
use App\Contracts\ServerProvider;
use App\Services\DigitalOceanServerProvider;
use App\Services\PingdomDowntimeNotifier;
use App\Services\ServerToolsProvider;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * All of the container bindings that should be registered.
     *
     * @var array
     */
    public $bindings = [
        ServerProvider::class => DigitalOceanServerProvider::class,
    ];

    /**
     * All of the container singletons that should be registered.
     *
     * @var array
     */
    public $singletons = [
        DowntimeNotifier::class => PingdomDowntimeNotifier::class,
        ServerProvider::class => ServerToolsProvider::class,
    ];
}
```

<a name="the-boot-method"></a>
### Метод boot

А що, якщо нам потрібно зареєструвати в сервіс-провайдері [компоновник представлень](/docs/{{version}}/views#view-composers)? Це слід робити в методі `boot`. **Цей метод викликається після реєстрації всіх інших сервіс-провайдерів**, тобто вам доступні всі інші сервіси, зареєстровані фреймворком:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

class ComposerServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        View::composer('view', function () {
            // ...
        });
    }
}
```

<a name="boot-method-dependency-injection"></a>
#### Впровадження залежностей у методі boot

Ви можете вказати типи залежностей для методу `boot` вашого сервіс-провайдера. [Сервіс-контейнер](/docs/{{version}}/container) автоматично впровадить усі потрібні вам залежності:

```php
use Illuminate\Contracts\Routing\ResponseFactory;

/**
 * Bootstrap any application services.
 */
public function boot(ResponseFactory $response): void
{
    $response->macro('serialized', function (mixed $value) {
        // ...
    });
}
```

<a name="registering-providers"></a>
## Реєстрація провайдерів

Усі сервіс-провайдери реєструються в конфігураційному файлі `bootstrap/providers.php`. Цей файл повертає масив, що містить імена класів сервіс-провайдерів вашого застосунку:

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
];
```

Коли ви викликаєте команду Artisan `make:provider`, Laravel автоматично додає згенерований провайдер до файлу `bootstrap/providers.php`. Однак якщо ви створили клас провайдера вручну, вам слід самостійно додати його до масиву:

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
    App\Providers\ComposerServiceProvider::class, // [tl! add]
];
```

<a name="deferred-providers"></a>
## Відкладені провайдери

Якщо ваш провайдер **лише** реєструє прив'язки в [сервіс-контейнері](/docs/{{version}}/container), ви можете відкласти його реєстрацію до моменту, коли одна із зареєстрованих прив'язок справді знадобиться. Відкладене завантаження такого провайдера покращить швидкодію вашого застосунку, адже його не доведеться завантажувати з файлової системи на кожному запиті.

Laravel компілює та зберігає список усіх сервісів, які надають відкладені сервіс-провайдери, разом з іменами їхніх класів. Далі Laravel завантажує сервіс-провайдер лише тоді, коли ви намагаєтеся розв'язати один із цих сервісів.

Щоб відкласти завантаження провайдера, реалізуйте інтерфейс `\Illuminate\Contracts\Support\DeferrableProvider` і визначте метод `provides`. Метод `provides` має повертати прив'язки сервіс-контейнера, зареєстровані провайдером:

```php
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\Support\DeferrableProvider;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider implements DeferrableProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->singleton(Connection::class, function (Application $app) {
            return new Connection($app['config']['riak']);
        });
    }

    /**
     * Get the services provided by the provider.
     *
     * @return array<int, string>
     */
    public function provides(): array
    {
        return [Connection::class];
    }
}
```
