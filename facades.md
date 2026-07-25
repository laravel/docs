---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Фасади

- [Вступ](#introduction)
- [Коли використовувати фасади](#when-to-use-facades)
    - [Фасади проти впровадження залежностей](#facades-vs-dependency-injection)
    - [Фасади проти функцій-хелперів](#facades-vs-helper-functions)
- [Як працюють фасади](#how-facades-work)
- [Фасади в реальному часі](#real-time-facades)
- [Довідник класів фасадів](#facade-class-reference)

<a name="introduction"></a>
## Вступ

У всій документації Laravel ви бачитимете приклади коду, що взаємодіє з можливостями Laravel через «фасади». Фасади дають «статичний» інтерфейс до класів, доступних у [сервіс-контейнері](/docs/{{version}}/container) застосунку. Laravel постачається з багатьма фасадами, які дають доступ майже до всіх можливостей фреймворку.

Фасади Laravel слугують «статичними проксі» до класів у сервіс-контейнері, даючи стислий виразний синтаксис і зберігаючи водночас кращу тестованість і гнучкість, ніж традиційні статичні методи. Цілком нормально, якщо ви не до кінця розумієте, як працюють фасади, - просто рухайтеся далі й вивчайте Laravel.

Усі фасади Laravel визначені у просторі імен `Illuminate\Support\Facades`. Тож звернутися до фасаду можна легко:

```php
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

У всій документації Laravel багато прикладів використовують фасади, щоб продемонструвати різні можливості фреймворку.

<a name="helper-functions"></a>
#### Функції-хелпери

На додачу до фасадів Laravel пропонує різноманітні глобальні «функції-хелпери», які ще більше спрощують роботу з поширеними можливостями Laravel. Серед хелперів, з якими ви можете стикатися, - `view`, `response`, `url`, `config` тощо. Кожна функція-хелпер Laravel задокументована разом із відповідною можливістю, а повний список доступний в окремій [документації з хелперів](/docs/{{version}}/helpers).

Наприклад, замість фасаду `Illuminate\Support\Facades\Response` для генерації JSON-відповіді можна просто скористатися функцією `response`. Оскільки функції-хелпери доступні глобально, для їх використання не потрібно імпортувати жодних класів:

```php
use Illuminate\Support\Facades\Response;

Route::get('/users', function () {
    return Response::json([
        // ...
    ]);
});

Route::get('/users', function () {
    return response()->json([
        // ...
    ]);
});
```

<a name="when-to-use-facades"></a>
## Коли використовувати фасади

Фасади мають багато переваг. Вони дають стислий, легкий для запам'ятовування синтаксис, що дозволяє користуватися можливостями Laravel, не пам'ятаючи довгих імен класів, які треба впроваджувати чи налаштовувати вручну. До того ж завдяки своєму особливому використанню динамічних методів PHP їх легко тестувати.

Однак із фасадами слід бути обачними. Головна їхня небезпека - «розповзання» відповідальності класу. Оскільки фасадами дуже просто користуватися і вони не потребують впровадження, легко дозволити своїм класам розростатися й використовувати багато фасадів в одному класі. При впровадженні залежностей цього ризику менше завдяки візуальному сигналу: великий конструктор одразу показує, що клас стає завеликим. Тож, використовуючи фасади, особливо уважно стежте за розміром класу, щоб його зона відповідальності лишалася вузькою. Якщо клас стає завеликим, подумайте про поділ його на кілька менших.

<a name="facades-vs-dependency-injection"></a>
### Фасади проти впровадження залежностей

Одна з головних переваг впровадження залежностей (dependency injection) - можливість підміняти реалізації впровадженого класу. Це корисно під час тестування, адже ви можете впровадити мок чи стаб і перевірити, що на ньому були викликані певні методи.

Зазвичай замокати чи застабити справді статичний метод класу неможливо. Однак оскільки фасади використовують динамічні методи, щоб проксіювати виклики до об'єктів, розв'язаних із сервіс-контейнера, ми фактично можемо тестувати фасади так само, як тестували б впроваджений екземпляр класу. Наприклад, маючи такий маршрут:

```php
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

За допомогою методів тестування фасадів Laravel ми можемо написати такий тест, щоб переконатися, що метод `Cache::get` було викликано з очікуваним аргументом:

```php tab=Pest
use Illuminate\Support\Facades\Cache;

test('basic example', function () {
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
});
```

```php tab=PHPUnit
use Illuminate\Support\Facades\Cache;

/**
 * A basic functional test example.
 */
public function test_basic_example(): void
{
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}
```

<a name="facades-vs-helper-functions"></a>
### Фасади проти функцій-хелперів

Крім фасадів, Laravel містить різноманітні функції-хелпери, які виконують типові завдання: генерують представлення, запускають події, диспетчеризують завдання чи надсилають HTTP-відповіді. Багато з них виконують те саме, що й відповідний фасад. Наприклад, цей виклик фасаду й виклик хелпера рівнозначні:

```php
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

Між фасадами та функціями-хелперами немає абсолютно жодної практичної різниці. Використовуючи хелпери, ви можете тестувати їх точно так само, як відповідний фасад. Наприклад, маючи такий маршрут:

```php
Route::get('/cache', function () {
    return cache('key');
});
```

Хелпер `cache` викличе метод `get` на класі, що лежить в основі фасаду `Cache`. Тож навіть використовуючи функцію-хелпер, ми можемо написати такий тест, щоб переконатися, що метод було викликано з очікуваним аргументом:

```php
use Illuminate\Support\Facades\Cache;

/**
 * A basic functional test example.
 */
public function test_basic_example(): void
{
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}
```

<a name="how-facades-work"></a>
## Як працюють фасади

У застосунку Laravel фасад - це клас, що дає доступ до об'єкта з контейнера. Механізм, який це забезпечує, міститься в класі `Facade`. Фасади Laravel, як і будь-які створені вами власні фасади, успадковують базовий клас `Illuminate\Support\Facades\Facade`.

Базовий клас `Facade` використовує магічний метод `__callStatic()`, щоб перенаправляти виклики з вашого фасаду до об'єкта, розв'язаного з контейнера. У прикладі нижче виконується звернення до системи кешу Laravel. Побіжно глянувши на цей код, можна припустити, що на класі `Cache` викликається статичний метод `get`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function showProfile(string $id): View
    {
        $user = Cache::get('user:'.$id);

        return view('profile', ['user' => $user]);
    }
}
```

Зверніть увагу, що ближче до початку файлу ми «імпортуємо» фасад `Cache`. Цей фасад слугує проксі для доступу до реалізації інтерфейсу `Illuminate\Contracts\Cache\Factory`. Усі виклики, зроблені через фасад, буде передано до відповідного екземпляра сервісу кешу Laravel.

Якщо ми зазирнемо до класу `Illuminate\Support\Facades\Cache`, то побачимо, що статичного методу `get` там немає:

```php
class Cache extends Facade
{
    /**
     * Get the registered name of the component.
     */
    protected static function getFacadeAccessor(): string
    {
        return 'cache';
    }
}
```

Натомість фасад `Cache` успадковує базовий клас `Facade` і визначає метод `getFacadeAccessor()`. Завдання цього методу - повернути ім'я прив'язки сервіс-контейнера. Коли користувач звертається до будь-якого статичного методу фасаду `Cache`, Laravel розв'язує прив'язку `cache` із [сервіс-контейнера](/docs/{{version}}/container) і виконує на цьому об'єкті запитаний метод (у цьому випадку - `get`).

<a name="real-time-facades"></a>
## Фасади в реальному часі

За допомогою фасадів у реальному часі ви можете поводитися з будь-яким класом свого застосунку так, ніби це фасад. Щоб проілюструвати, як це працює, спершу розгляньмо код, що їх не використовує. Припустімо, наша модель `Podcast` має метод `publish`. Однак, щоб опублікувати подкаст, нам потрібно впровадити екземпляр `Publisher`:

```php
<?php

namespace App\Models;

use App\Contracts\Publisher;
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * Publish the podcast.
     */
    public function publish(Publisher $publisher): void
    {
        $this->update(['publishing' => now()]);

        $publisher->publish($this);
    }
}
```

Впровадження реалізації publisher у метод дозволяє легко тестувати його ізольовано, адже ми можемо замокати впроваджений publisher. Однак це вимагає щоразу передавати екземпляр publisher під час виклику методу `publish`. Із фасадами в реальному часі ми зберігаємо ту саму тестованість, не будучи зобов'язаними явно передавати екземпляр `Publisher`. Щоб створити фасад у реальному часі, додайте до простору імен імпортованого класу префікс `Facades`:

```php
<?php

namespace App\Models;

use App\Contracts\Publisher; // [tl! remove]
use Facades\App\Contracts\Publisher; // [tl! add]
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * Publish the podcast.
     */
    public function publish(Publisher $publisher): void // [tl! remove]
    public function publish(): void // [tl! add]
    {
        $this->update(['publishing' => now()]);

        $publisher->publish($this); // [tl! remove]
        Publisher::publish($this); // [tl! add]
    }
}
```

Коли використовується фасад у реальному часі, реалізацію publisher буде розв'язано із сервіс-контейнера за тією частиною імені інтерфейсу чи класу, що йде після префікса `Facades`. Під час тестування ми можемо скористатися вбудованими хелперами тестування фасадів Laravel, щоб замокати цей виклик методу:

```php tab=Pest
<?php

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;

pest()->use(RefreshDatabase::class);

test('podcast can be published', function () {
    $podcast = Podcast::factory()->create();

    Publisher::shouldReceive('publish')->once()->with($podcast);

    $podcast->publish();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PodcastTest extends TestCase
{
    use RefreshDatabase;

    /**
     * A test example.
     */
    public function test_podcast_can_be_published(): void
    {
        $podcast = Podcast::factory()->create();

        Publisher::shouldReceive('publish')->once()->with($podcast);

        $podcast->publish();
    }
}
```

<a name="facade-class-reference"></a>
## Довідник класів фасадів

Нижче наведено кожен фасад і клас, що лежить у його основі. Це зручний інструмент, щоб швидко зазирнути в документацію API для конкретного фасаду. Де це доречно, також вказано ключ [прив'язки сервіс-контейнера](/docs/{{version}}/container).

<div class="overflow-auto">

| Фасад | Клас | Прив'язка сервіс-контейнера |
| --- | --- | --- |
| App | [Illuminate\Foundation\Application](https://api.laravel.com/docs/{{version}}/Illuminate/Foundation/Application.html) | `app` |
| Artisan | [Illuminate\Contracts\Console\Kernel](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| Auth (Instance) | [Illuminate\Contracts\Auth\Guard](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| Auth | [Illuminate\Auth\AuthManager](https://api.laravel.com/docs/{{version}}/Illuminate/Auth/AuthManager.html) | `auth` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://api.laravel.com/docs/{{version}}/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| Broadcast (Instance) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| Broadcast | [Illuminate\Contracts\Broadcasting\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| Bus | [Illuminate\Contracts\Bus\Dispatcher](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| Cache (Instance) | [Illuminate\Cache\Repository](https://api.laravel.com/docs/{{version}}/Illuminate/Cache/Repository.html) | `cache.store` |
| Cache | [Illuminate\Cache\CacheManager](https://api.laravel.com/docs/{{version}}/Illuminate/Cache/CacheManager.html) | `cache` |
| Config | [Illuminate\Config\Repository](https://api.laravel.com/docs/{{version}}/Illuminate/Config/Repository.html) | `config` |
| Context | [Illuminate\Log\Context\Repository](https://api.laravel.com/docs/{{version}}/Illuminate/Log/Context/Repository.html) | &nbsp; |
| Cookie | [Illuminate\Cookie\CookieJar](https://api.laravel.com/docs/{{version}}/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt | [Illuminate\Encryption\Encrypter](https://api.laravel.com/docs/{{version}}/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| Date | [Illuminate\Support\DateFactory](https://api.laravel.com/docs/{{version}}/Illuminate/Support/DateFactory.html) | `date` |
| DB (Instance) | [Illuminate\Database\Connection](https://api.laravel.com/docs/{{version}}/Illuminate/Database/Connection.html) | `db.connection` |
| DB | [Illuminate\Database\DatabaseManager](https://api.laravel.com/docs/{{version}}/Illuminate/Database/DatabaseManager.html) | `db` |
| Event | [Illuminate\Events\Dispatcher](https://api.laravel.com/docs/{{version}}/Illuminate/Events/Dispatcher.html) | `events` |
| Exceptions (Instance) | [Illuminate\Contracts\Debug\ExceptionHandler](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; |
| Exceptions | [Illuminate\Foundation\Exceptions\Handler](https://api.laravel.com/docs/{{version}}/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; |
| File | [Illuminate\Filesystem\Filesystem](https://api.laravel.com/docs/{{version}}/Illuminate/Filesystem/Filesystem.html) | `files` |
| Gate | [Illuminate\Contracts\Auth\Access\Gate](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| Hash | [Illuminate\Contracts\Hashing\Hasher](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| Http | [Illuminate\Http\Client\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Http/Client/Factory.html) | &nbsp; |
| Lang | [Illuminate\Translation\Translator](https://api.laravel.com/docs/{{version}}/Illuminate/Translation/Translator.html) | `translator` |
| Log | [Illuminate\Log\LogManager](https://api.laravel.com/docs/{{version}}/Illuminate/Log/LogManager.html) | `log` |
| Mail | [Illuminate\Mail\Mailer](https://api.laravel.com/docs/{{version}}/Illuminate/Mail/Mailer.html) | `mailer` |
| Notification | [Illuminate\Notifications\ChannelManager](https://api.laravel.com/docs/{{version}}/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| Password (Instance) | [Illuminate\Auth\Passwords\PasswordBroker](https://api.laravel.com/docs/{{version}}/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| Password | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://api.laravel.com/docs/{{version}}/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| Pipeline (Instance) | [Illuminate\Pipeline\Pipeline](https://api.laravel.com/docs/{{version}}/Illuminate/Pipeline/Pipeline.html) | &nbsp; |
| Process | [Illuminate\Process\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Process/Factory.html) | &nbsp; |
| Queue (Base Class) | [Illuminate\Queue\Queue](https://api.laravel.com/docs/{{version}}/Illuminate/Queue/Queue.html) | &nbsp; |
| Queue (Instance) | [Illuminate\Contracts\Queue\Queue](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| Queue | [Illuminate\Queue\QueueManager](https://api.laravel.com/docs/{{version}}/Illuminate/Queue/QueueManager.html) | `queue` |
| RateLimiter | [Illuminate\Cache\RateLimiter](https://api.laravel.com/docs/{{version}}/Illuminate/Cache/RateLimiter.html) | &nbsp; |
| Redirect | [Illuminate\Routing\Redirector](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis (Instance) | [Illuminate\Redis\Connections\Connection](https://api.laravel.com/docs/{{version}}/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| Redis | [Illuminate\Redis\RedisManager](https://api.laravel.com/docs/{{version}}/Illuminate/Redis/RedisManager.html) | `redis` |
| Request | [Illuminate\Http\Request](https://api.laravel.com/docs/{{version}}/Illuminate/Http/Request.html) | `request` |
| Response (Instance) | [Illuminate\Http\Response](https://api.laravel.com/docs/{{version}}/Illuminate/Http/Response.html) | &nbsp; |
| Response | [Illuminate\Contracts\Routing\ResponseFactory](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| Route | [Illuminate\Routing\Router](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Router.html) | `router` |
| Schedule | [Illuminate\Console\Scheduling\Schedule](https://api.laravel.com/docs/{{version}}/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; |
| Schema | [Illuminate\Database\Schema\Builder](https://api.laravel.com/docs/{{version}}/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| Session (Instance) | [Illuminate\Session\Store](https://api.laravel.com/docs/{{version}}/Illuminate/Session/Store.html) | `session.store` |
| Session | [Illuminate\Session\SessionManager](https://api.laravel.com/docs/{{version}}/Illuminate/Session/SessionManager.html) | `session` |
| Storage (Instance) | [Illuminate\Contracts\Filesystem\Filesystem](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| Storage | [Illuminate\Filesystem\FilesystemManager](https://api.laravel.com/docs/{{version}}/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| URL | [Illuminate\Routing\UrlGenerator](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/UrlGenerator.html) | `url` |
| Validator (Instance) | [Illuminate\Validation\Validator](https://api.laravel.com/docs/{{version}}/Illuminate/Validation/Validator.html) | &nbsp; |
| Validator | [Illuminate\Validation\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Validation/Factory.html) | `validator` |
| View (Instance) | [Illuminate\View\View](https://api.laravel.com/docs/{{version}}/Illuminate/View/View.html) | &nbsp; |
| View | [Illuminate\View\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/View/Factory.html) | `view` |
| Vite | [Illuminate\Foundation\Vite](https://api.laravel.com/docs/{{version}}/Illuminate/Foundation/Vite.html) | &nbsp; |

</div>
