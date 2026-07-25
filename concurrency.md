---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Паралельність

- [Вступ](#introduction)
- [Запуск паралельних завдань](#running-concurrent-tasks)
    - [Іменовані результати](#named-results)
    - [Тайм-аути завдань](#task-timeouts)
- [Відкладені паралельні завдання](#deferring-concurrent-tasks)

<a name="introduction"></a>
## Вступ

Іноді вам може знадобитися виконати кілька повільних завдань, які не залежать одне від одного. У багатьох випадках паралельне виконання дає значний приріст швидкодії. Фасад `Concurrency` у Laravel надає простий і зручний API для паралельного виконання замикань.

<a name="how-it-works"></a>
#### Як це працює

Laravel досягає паралельності, серіалізуючи передані замикання й надсилаючи їх до прихованої команди Artisan CLI, яка десеріалізує замикання та виконує їх у власному процесі PHP. Після виконання замикання отриманий результат серіалізується назад до батьківського процесу.

Фасад `Concurrency` підтримує три драйвери: `process` (типовий), `fork` і `sync`.

Драйвер `fork` дає кращу швидкодію порівняно з типовим `process`, але його можна використовувати лише в контексті PHP CLI, адже PHP не підтримує форкування під час веб-запитів. Перш ніж використовувати драйвер `fork`, потрібно встановити пакет `spatie/fork`:

```shell
composer require spatie/fork
```

Драйвер `sync` насамперед корисний під час тестування, коли ви хочете вимкнути будь-яку паралельність і просто виконати передані замикання послідовно в батьківському процесі.

<a name="running-concurrent-tasks"></a>
## Запуск паралельних завдань

Щоб запустити паралельні завдання, викличте метод `run` фасаду `Concurrency`. Метод `run` приймає масив замикань, які слід виконати одночасно в дочірніх процесах PHP:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
]);
```

Щоб скористатися конкретним драйвером, застосуйте метод `driver`:

```php
$results = Concurrency::driver('fork')->run(...);
```

Або, щоб змінити типовий драйвер паралельності, опублікуйте конфігураційний файл `concurrency` командою Artisan `config:publish` і оновіть у ньому опцію `default`:

```shell
php artisan config:publish concurrency
```

<a name="named-results"></a>
### Іменовані результати

Якщо ви хочете звертатися до результатів паралельних завдань за іменем, а не за позицією, передайте асоціативний масив замикань. Кожен результат буде повернуто під тим самим ключем, що й відповідне замикання:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

$results = Concurrency::run([
    'users' => fn () => DB::table('users')->count(),
    'orders' => fn () => DB::table('orders')->count(),
]);

$userCount = $results['users'];
$orderCount = $results['orders'];
```

<a name="task-timeouts"></a>
### Тайм-аути завдань

Використовуючи драйвер `process` (типовий), ви можете вказати максимальну кількість секунд, протягом яких паралельному завданню дозволено виконуватися до примусового завершення, передавши тайм-аут методу `run`:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
], timeout: 30);
```

Ви також можете передати екземпляр `CarbonInterval`, якщо вам більше до вподоби виразніше визначення тайм-ауту:

```php
use Illuminate\Support\Facades\Concurrency;

use function Illuminate\Support\seconds;

Concurrency::run([...], timeout: seconds(30));
```

<a name="deferring-concurrent-tasks"></a>
## Відкладені паралельні завдання

Якщо ви хочете виконати масив замикань паралельно, але вас не цікавлять їхні результати, скористайтеся методом `defer`. Коли викликано метод `defer`, передані замикання не виконуються одразу. Натомість Laravel виконає їх паралельно після того, як HTTP-відповідь буде надіслано користувачеві:

```php
use App\Services\Metrics;
use Illuminate\Support\Facades\Concurrency;

Concurrency::defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);
```
