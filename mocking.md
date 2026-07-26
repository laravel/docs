---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Мокування

- [Вступ](#introduction)
- [Мокування об'єктів](#mocking-objects)
- [Мокування фасадів](#mocking-facades)
    - [Шпигуни фасадів](#facade-spies)
- [Робота з часом](#interacting-with-time)

<a name="introduction"></a>
## Вступ

Тестуючи застосунки Laravel, ви можете захотіти «замокати» певні частини вашого застосунку, щоб вони не виконувалися насправді під час конкретного тесту. Наприклад, тестуючи контролер, який відправляє подію, ви можете замокати слухачів події, щоб вони не виконувалися під час тесту. Це дозволяє перевірити лише HTTP-відповідь контролера, не переймаючись виконанням слухачів, адже їх можна протестувати окремим тест-кейсом.

Laravel надає корисні методи для мокування подій, завдань та інших фасадів одразу з коробки. Ці хелпери здебільшого є зручним шаром над Mockery, тож вам не доведеться вручну писати складні виклики його методів.

<a name="mocking-objects"></a>
## Мокування об'єктів

Мокуючи об'єкт, який буде впроваджено у ваш застосунок через [сервіс-контейнер](/docs/{{version}}/container) Laravel, вам треба прив'язати замокований екземпляр до контейнера як прив'язку `instance`. Це вкаже контейнеру використовувати ваш замокований екземпляр об'єкта замість того, щоб конструювати об'єкт самому:

```php tab=Pest
use App\Service;
use Mockery;
use Mockery\MockInterface;

test('something can be mocked', function () {
    $this->instance(
        Service::class,
        Mockery::mock(Service::class, function (MockInterface $mock) {
            $mock->expects('process');
        })
    );
});
```

```php tab=PHPUnit
use App\Service;
use Mockery;
use Mockery\MockInterface;

public function test_something_can_be_mocked(): void
{
    $this->instance(
        Service::class,
        Mockery::mock(Service::class, function (MockInterface $mock) {
            $mock->expects('process');
        })
    );
}
```

Щоб зробити це зручніше, скористайтеся методом `mock`, який надає базовий клас тест-кейса Laravel. Наприклад, наступний приклад рівносильний наведеному вище:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});
```

Коли вам треба замокати лише кілька методів об'єкта, скористайтеся методом `partialMock`. Методи, які не замоковані, при виклику виконуватимуться як зазвичай:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});
```

Так само, якщо ви хочете [шпигувати](http://docs.mockery.io/en/latest/reference/spies.html) за об'єктом, базовий клас тест-кейса Laravel пропонує метод `spy` - зручну обгортку над методом `Mockery::spy`. Шпигуни схожі на моки; проте шпигуни записують усі взаємодії між собою та кодом, який тестується, дозволяючи робити твердження вже після виконання коду:

```php
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## Мокування фасадів

На відміну від традиційних викликів статичних методів, [фасади](/docs/{{version}}/facades) (зокрема й [фасади реального часу](/docs/{{version}}/facades#real-time-facades)) можна мокати. Це велика перевага над традиційними статичними методами, яка дає вам таку саму тестованість, як і при звичайному впровадженні залежностей. Під час тестування вам часто може знадобитися замокати виклик фасада Laravel, що відбувається в одному з ваших контролерів. Розгляньмо, наприклад, таку дію контролера:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * Retrieve a list of all users of the application.
     */
    public function index(): array
    {
        $value = Cache::get('key');

        return [
            // ...
        ];
    }
}
```

Ми можемо замокати виклик фасада `Cache` методом `expects`, який поверне екземпляр мока [Mockery](https://github.com/padraic/mockery). Оскільки фасади насправді розв'язуються й керуються [сервіс-контейнером](/docs/{{version}}/container) Laravel, вони куди тестованіші за звичайний статичний клас. Наприклад, замокаймо наш виклик методу `get` фасада `Cache`:

```php tab=Pest
<?php

use Illuminate\Support\Facades\Cache;

test('get index', function () {
    Cache::expects('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/users');

    // ...
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Support\Facades\Cache;
use Tests\TestCase;

class UserControllerTest extends TestCase
{
    public function test_get_index(): void
    {
        Cache::expects('get')
            ->with('key')
            ->andReturn('value');

        $response = $this->get('/users');

        // ...
    }
}
```

> [!WARNING]
> Вам не слід мокати фасад `Request`. Натомість передавайте потрібні дані до [методів тестування HTTP](/docs/{{version}}/http-tests) на кшталт `get` і `post` під час прогону тесту. Так само замість мокування фасада `Config` викликайте у своїх тестах метод `Config::set`.

<a name="facade-spies"></a>
### Шпигуни фасадів

Якщо ви хочете [шпигувати](http://docs.mockery.io/en/latest/reference/spies.html) за фасадом, викличте на ньому метод `spy`. Шпигуни схожі на моки; проте шпигуни записують усі взаємодії між собою та кодом, який тестується, дозволяючи робити твердження вже після виконання коду:

```php tab=Pest
<?php

use Illuminate\Support\Facades\Cache;

test('values are stored in cache', function () {
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->with('name', 'Taylor', 10);
});
```

```php tab=PHPUnit
use Illuminate\Support\Facades\Cache;

public function test_values_are_stored_in_cache(): void
{
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->with('name', 'Taylor', 10);
}
```

<a name="interacting-with-time"></a>
## Робота з часом

Під час тестування вам іноді може знадобитися змінити час, який повертають хелпери на кшталт `now` чи `Illuminate\Support\Carbon::now()`. На щастя, базовий клас функціональних тестів Laravel містить хелпери, що дозволяють маніпулювати поточним часом:

```php tab=Pest
test('time can be manipulated', function () {
    // Travel into the future...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // Travel into the past...
    $this->travel(-5)->hours();

    // Travel to an explicit time...
    $this->travelTo(now()->minus(hours: 6));

    // Return back to the present time...
    $this->travelBack();
});
```

```php tab=PHPUnit
public function test_time_can_be_manipulated(): void
{
    // Travel into the future...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // Travel into the past...
    $this->travel(-5)->hours();

    // Travel to an explicit time...
    $this->travelTo(now()->minus(hours: 6));

    // Return back to the present time...
    $this->travelBack();
}
```

Ви також можете передати різним методам подорожі в часі замикання. Його буде викликано із часом, замороженим на вказаній позначці. Коли замикання виконається, час піде далі як зазвичай:

```php
$this->travel(5)->days(function () {
    // Test something five days into the future...
});

$this->travelTo(now()->mins(days: 10), function () {
    // Test something during a given moment...
});
```

Метод `freezeTime` дозволяє заморозити поточний час. Так само метод `freezeSecond` заморозить поточний час, але на початку поточної секунди:

```php
use Illuminate\Support\Carbon;

// Freeze time and resume normal time after executing closure...
$this->freezeTime(function (Carbon $time) {
    // ...
});

// Freeze time at the current second and resume normal time after executing closure...
$this->freezeSecond(function (Carbon $time) {
    // ...
})
```

Як і слід очікувати, всі розглянуті вище методи передусім корисні для тестування поведінки застосунку, чутливої до часу, - наприклад, блокування неактивних дописів на форумі:

```php tab=Pest
use App\Models\Thread;

test('forum threads lock after one week of inactivity', function () {
    $thread = Thread::factory()->create();

    $this->travel(1)->week();

    expect($thread->isLockedByInactivity())->toBeTrue();
});
```

```php tab=PHPUnit
use App\Models\Thread;

public function test_forum_threads_lock_after_one_week_of_inactivity()
{
    $thread = Thread::factory()->create();

    $this->travel(1)->week();

    $this->assertTrue($thread->isLockedByInactivity());
}
```
