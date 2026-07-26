---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---

# Redis

- [Вступ](#introduction)
- [Конфігурація](#configuration)
    - [Кластери](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Робота з Redis](#interacting-with-redis)
    - [Транзакції](#transactions)
    - [Конвеєр команд](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## Вступ

[Redis](https://redis.io) - це відкрите сховище пар «ключ - значення» з широкими можливостями. Його часто називають сервером структур даних, бо ключі можуть містити [рядки](https://redis.io/docs/latest/develop/data-types/strings/), [хеші](https://redis.io/docs/latest/develop/data-types/hashes/), [списки](https://redis.io/docs/latest/develop/data-types/lists/), [множини](https://redis.io/docs/latest/develop/data-types/sets/) та [відсортовані множини](https://redis.io/docs/latest/develop/data-types/sorted-sets/).

Перед тим як використовувати Redis із Laravel, радимо встановити PHP-розширення [PhpRedis](https://github.com/phpredis/phpredis) через PECL. Встановити його складніше, ніж PHP-пакети «з користувацького простору», але для застосунків, які активно працюють із Redis, він може дати кращу продуктивність. Якщо ви користуєтеся [Laravel Sail](/docs/{{version}}/sail), це розширення вже встановлене в Docker-контейнері вашого застосунку.

Якщо встановити розширення PhpRedis не вдається, ви можете встановити через Composer пакет `predis/predis`. Predis - це клієнт Redis, повністю написаний на PHP, і він не потребує додаткових розширень:

```shell
composer require predis/predis
```

<a name="configuration"></a>
## Конфігурація

Налаштування Redis для вашого застосунку лежать у файлі `config/database.php`. У ньому ви побачите масив `redis` зі серверами Redis, які використовує ваш застосунок:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
    ],

    'default' => [
        'url' => env('REDIS_URL'),
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'username' => env('REDIS_USERNAME'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', '6379'),
        'database' => env('REDIS_DB', '0'),
    ],

    'cache' => [
        'url' => env('REDIS_URL'),
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'username' => env('REDIS_USERNAME'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', '6379'),
        'database' => env('REDIS_CACHE_DB', '1'),
    ],

],
```

Кожен сервер Redis, описаний у вашому файлі конфігурації, має мати назву, хост і порт - хіба що ви задаєте єдиний URL, який представляє підключення до Redis:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
    ],

    'default' => [
        'url' => 'tcp://127.0.0.1:6379?database=0',
    ],

    'cache' => [
        'url' => 'tls://user:password@127.0.0.1:6380?database=1',
    ],

],
```

<a name="configuring-the-connection-scheme"></a>
#### Налаштування схеми підключення

За замовчуванням клієнти Redis підключаються до ваших серверів за схемою `tcp`; втім, ви можете скористатися шифруванням TLS / SSL, задавши опцію `scheme` у масиві конфігурації сервера Redis:

```php
'default' => [
    'scheme' => 'tls',
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
],
```

<a name="clusters"></a>
### Кластери

Якщо ваш застосунок працює з кластером серверів Redis, опишіть ці кластери під ключем `clusters` конфігурації Redis. За замовчуванням цього ключа немає, тож вам доведеться створити його у файлі `config/database.php` вашого застосунку:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
    ],

    'clusters' => [
        'default' => [
            [
                'url' => env('REDIS_URL'),
                'host' => env('REDIS_HOST', '127.0.0.1'),
                'username' => env('REDIS_USERNAME'),
                'password' => env('REDIS_PASSWORD'),
                'port' => env('REDIS_PORT', '6379'),
                'database' => env('REDIS_DB', '0'),
            ],
        ],
    ],

    // ...
],
```

За замовчуванням Laravel використовує нативну кластеризацію Redis, бо значення конфігурації `options.cluster` дорівнює `redis`. Кластеризація Redis - чудовий вибір за замовчуванням, бо вона коректно обробляє перемикання при відмові.

Laravel також підтримує шардинг на боці клієнта під час роботи з Predis. Проте шардинг на боці клієнта не обробляє відмов, тому підходить насамперед для тимчасових кешованих даних, які можна взяти з іншого основного сховища.

Якщо ви хочете використовувати шардинг на боці клієнта замість нативної кластеризації Redis, приберіть значення конфігурації `options.cluster` з файлу `config/database.php` вашого застосунку:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'clusters' => [
        // ...
    ],

    // ...
],
```

<a name="predis"></a>
### Predis

Якщо ви хочете, щоб ваш застосунок працював із Redis через пакет Predis, переконайтеся, що змінна оточення `REDIS_CLIENT` має значення `predis`:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

Крім стандартних опцій конфігурації, Predis підтримує додаткові [параметри підключення](https://github.com/nrk/predis/wiki/Connection-Parameters), які можна задати для кожного з ваших серверів Redis. Щоб скористатися ними, додайте їх до конфігурації сервера Redis у файлі `config/database.php` вашого застосунку:

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'read_write_timeout' => 60,
],
```

<a name="phpredis"></a>
### PhpRedis

За замовчуванням Laravel спілкується з Redis через розширення PhpRedis. Який саме клієнт використовувати, визначає значення опції конфігурації `redis.client`, що зазвичай відображає значення змінної оточення `REDIS_CLIENT`:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

Крім стандартних опцій конфігурації, PhpRedis підтримує такі додаткові параметри підключення: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout` і `context`. Будь-яку з цих опцій можна додати до конфігурації сервера Redis у файлі `config/database.php`:

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'read_timeout' => 60,
    'context' => [
        // 'auth' => ['username', 'secret'],
        // 'stream' => ['verify_peer' => false],
    ],
],
```

<a name="retry-and-backoff-configuration"></a>
#### Налаштування повторних спроб і затримок

Опціями `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base` і `backoff_cap` можна налаштувати, як клієнт PhpRedis має перепідключатися до сервера Redis. Підтримуються такі алгоритми затримки: `default`, `decorrelated_jitter`, `equal_jitter`, `exponential`, `uniform` і `constant`:

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'max_retries' => env('REDIS_MAX_RETRIES', 3),
    'backoff_algorithm' => env('REDIS_BACKOFF_ALGORITHM', 'decorrelated_jitter'),
    'backoff_base' => env('REDIS_BACKOFF_BASE', 100),
    'backoff_cap' => env('REDIS_BACKOFF_CAP', 1000),
],
```

Predis 3.4.0 і новіші підтримують вбудоване налаштування повторних спроб і затримок через клас `Retry`. Кількість спроб задається опцією `max_retries`, а стратегія затримки - опцією `retry`. Опція `retry` має бути масивом, ключами якого є один із таких класів стратегій: `NoBackoff`, `EqualBackoff` або `ExponentialBackoff`:

```php
use Predis\Retry\Strategy\ExponentialBackoff;

'default' => [
    'url' => env('REDIS_URL'),
    // ...
    'retry' => [
        ExponentialBackoff::class => [
            env('REDIS_BACKOFF_BASE', 100),
            env('REDIS_BACKOFF_CAP', 1000),
            true, // Enable jitter...
        ],
    ],
    'max_retries' => env('REDIS_MAX_RETRIES', 3),
],
```

Коли ви використовуєте Predis із кластером Redis, налаштування повторних спроб можна задати в опції `parameters` конфігурації кластера:

```php
use Predis\Retry\Strategy\NoBackoff;

'clusters' => [
    'default' => [
        // ...
    ],
],

'options' => [
    'cluster' => env('REDIS_CLUSTER', 'redis'),
    'parameters' => [
        'retry' => [
            NoBackoff::class => [],
        ],
        'max_retries' => env('REDIS_MAX_RETRIES', 3),
    ],
],
```

<a name="unix-socket-connections"></a>
#### Підключення через Unix-сокет

Підключення до Redis можна налаштувати й на Unix-сокети замість TCP. Це може підвищити продуктивність, бо прибирає накладні витрати TCP для підключень до екземплярів Redis на тому самому сервері, де й ваш застосунок. Щоб налаштувати Redis на Unix-сокет, задайте змінній оточення `REDIS_HOST` шлях до сокета Redis, а змінній `REDIS_PORT` - значення `0`:

```env
REDIS_HOST=/run/redis/redis.sock
REDIS_PORT=0
```

<a name="phpredis-serialization"></a>
#### Серіалізація та стиснення в PhpRedis

Розширення PhpRedis можна також налаштувати на різні серіалізатори та алгоритми стиснення. Ці алгоритми задаються в масиві `options` вашої конфігурації Redis:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
        'serializer' => Redis::SERIALIZER_MSGPACK,
        'compression' => Redis::COMPRESSION_LZ4,
    ],

    // ...
],
```

Наразі підтримуються такі серіалізатори: `Redis::SERIALIZER_NONE` (за замовчуванням), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY` і `Redis::SERIALIZER_MSGPACK`.

Підтримувані алгоритми стиснення: `Redis::COMPRESSION_NONE` (за замовчуванням), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD` і `Redis::COMPRESSION_LZ4`.

<a name="interacting-with-redis"></a>
## Робота з Redis

Працювати з Redis можна, викликаючи різні методи [фасаду](/docs/{{version}}/facades) `Redis`. Фасад `Redis` підтримує динамічні методи: ви можете викликати на ньому будь-яку [команду Redis](https://redis.io/commands), і її буде передано безпосередньо до Redis. У цьому прикладі ми викличемо команду Redis `GET`, звернувшись до методу `get` фасаду `Redis`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Redis;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => Redis::get('user:profile:'.$id)
        ]);
    }
}
```

Як згадано вище, на фасаді `Redis` можна викликати будь-яку команду Redis. Laravel використовує магічні методи, щоб передати команди на сервер Redis. Якщо команда Redis очікує аргументи, передайте їх до відповідного методу фасаду:

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

Або ж ви можете передавати команди на сервер методом `command` фасаду `Redis`: першим аргументом він приймає назву команди, а другим - масив значень:

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### Кілька підключень до Redis

Файл `config/database.php` вашого застосунку дозволяє описати кілька підключень чи серверів Redis. Отримати конкретне підключення можна методом `connection` фасаду `Redis`:

```php
$redis = Redis::connection('connection-name');
```

Щоб отримати екземпляр підключення до Redis за замовчуванням, викличте метод `connection` без додаткових аргументів:

```php
$redis = Redis::connection();
```

<a name="transactions"></a>
### Транзакції

Метод `transaction` фасаду `Redis` дає зручну обгортку над нативними командами Redis `MULTI` та `EXEC`. Метод `transaction` приймає єдиний аргумент - замикання. Воно отримає екземпляр підключення до Redis і може надсилати цьому екземпляру будь-які команди. Усі команди Redis, надіслані в межах замикання, буде виконано як одну атомарну транзакцію:

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Описуючи транзакцію Redis, ви не можете отримувати жодних значень із підключення до Redis. Пам'ятайте: ваша транзакція виконується як одна атомарна операція, а сама операція не виконується, поки все замикання не завершить надсилати команди.

#### Скрипти Lua

Метод `eval` - ще один спосіб виконати кілька команд Redis як одну атомарну операцію. Але `eval` має перевагу: під час цієї операції він може працювати зі значеннями ключів Redis і перевіряти їх. Скрипти Redis пишуть [мовою програмування Lua](https://www.lua.org).

Спершу метод `eval` може здатися дещо страшним, але розберімо простий приклад, щоб зламати кригу. Метод `eval` очікує кілька аргументів. Першим передайте скрипт Lua (рядком). Другим - кількість ключів (цілим числом), з якими працює скрипт. Третім - назви цих ключів. І нарешті, ви можете передати будь-які інші додаткові аргументи, потрібні вам у скрипті.

У цьому прикладі ми збільшимо один лічильник, перевіримо його нове значення й збільшимо другий лічильник, якщо значення першого більше за п'ять. Вкінці повернемо значення першого лічильника:

```php
$value = Redis::eval(<<<'LUA'
    local counter = redis.call("incr", KEYS[1])

    if counter > 5 then
        redis.call("incr", KEYS[2])
    end

    return counter
LUA, 2, 'first-counter', 'second-counter');
```

> [!WARNING]
> Детальніше про скриптинг у Redis читайте в [документації Redis](https://redis.io/commands/eval).

<a name="pipelining-commands"></a>
### Конвеєр команд

Іноді вам потрібно виконати десятки команд Redis. Замість того щоб для кожної команди йти по мережі до сервера Redis, скористайтеся методом `pipeline`. Він приймає один аргумент - замикання, яке отримає екземпляр Redis. Ви надсилаєте цьому екземпляру всі свої команди, і їх буде відправлено на сервер Redis одночасно, щоб зменшити кількість звернень по мережі. Команди все одно виконаються в тому порядку, у якому ви їх надіслали:

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::pipeline(function (Redis $pipe) {
    for ($i = 0; $i < 1000; $i++) {
        $pipe->set("key:$i", $i);
    }
});
```

<a name="pubsub"></a>
## Pub / Sub

Laravel дає зручний інтерфейс до команд Redis `publish` і `subscribe`. Ці команди дозволяють слухати повідомлення в заданому «каналі». Ви можете публікувати повідомлення в канал з іншого застосунку або навіть іншою мовою програмування, що дозволяє легко налагодити зв'язок між застосунками й процесами.

Спершу налаштуємо слухача каналу методом `subscribe`. Розмістимо цей виклик в [artisan-команді](/docs/{{version}}/artisan), бо метод `subscribe` запускає довготривалий процес:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Redis;

class RedisSubscribe extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'redis:subscribe';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Subscribe to a Redis channel';

    /**
     * Execute the console command.
     */
    public function handle(): void
    {
        Redis::subscribe(['test-channel'], function (string $message) {
            echo $message;
        });
    }
}
```

Тепер ми можемо публікувати повідомлення в канал методом `publish`:

```php
use Illuminate\Support\Facades\Redis;

Route::get('/publish', function () {
    // ...

    Redis::publish('test-channel', json_encode([
        'name' => 'Adam Wathan'
    ]));
});
```

<a name="wildcard-subscriptions"></a>
#### Підписки за шаблоном

Методом `psubscribe` ви можете підписатися на канал за шаблоном - це буває корисно, щоб ловити всі повідомлення в усіх каналах. Назву каналу буде передано другим аргументом до вашого замикання:

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```
