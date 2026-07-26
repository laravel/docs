---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Тестування HTTP

- [Вступ](#introduction)
- [Виконання запитів](#making-requests)
    - [Налаштування заголовків запиту](#customizing-request-headers)
    - [Cookie](#cookies)
    - [Сесія / автентифікація](#session-and-authentication)
    - [Налагодження відповідей](#debugging-responses)
    - [Обробка винятків](#exception-handling)
- [Тестування JSON API](#testing-json-apis)
    - [Плавне тестування JSON](#fluent-json-testing)
- [Тестування завантаження файлів](#testing-file-uploads)
- [Тестування представлень](#testing-views)
    - [Рендеринг Blade і компонентів](#rendering-blade-and-components)
- [Кешування маршрутів](#caching-routes)
- [Доступні твердження](#available-assertions)
    - [Твердження щодо відповіді](#response-assertions)
    - [Твердження щодо автентифікації](#authentication-assertions)
    - [Твердження щодо валідації](#validation-assertions)

<a name="introduction"></a>
## Вступ

Laravel надає дуже плавний API для виконання HTTP-запитів до вашого застосунку та перевірки відповідей. Погляньте, наприклад, на такий функціональний тест:

```php tab=Pest
<?php

test('the application returns a successful response', function () {
    $response = $this->get('/');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_the_application_returns_a_successful_response(): void
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

Метод `get` виконує до застосунку запит `GET`, а метод `assertStatus` перевіряє, що повернена відповідь має заданий код статусу HTTP. Окрім цього простого твердження, Laravel містить різні твердження для перевірки заголовків відповіді, її вмісту, структури JSON тощо.

<a name="making-requests"></a>
## Виконання запитів

Щоб виконати запит до вашого застосунку, викличте у своєму тесті методи `get`, `post`, `put`, `patch` чи `delete`. Ці методи не роблять «справжнього» HTTP-запиту до застосунку. Натомість увесь мережевий запит симулюється всередині.

Замість екземпляра `Illuminate\Http\Response` тестові методи запитів повертають екземпляр `Illuminate\Testing\TestResponse`, який надає [різні корисні твердження](#available-assertions) для перевірки відповідей вашого застосунку:

```php tab=Pest
<?php

test('basic request', function () {
    $response = $this->get('/');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_a_basic_request(): void
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

Загалом кожен ваш тест має робити лише один запит до застосунку. Якщо в межах одного тестового методу виконується кілька запитів, поведінка може бути несподіваною.

> [!NOTE]
> Для зручності під час прогону тестів `middleware` CSRF автоматично вимикається.

<a name="customizing-request-headers"></a>
### Налаштування заголовків запиту

Метод `withHeaders` дозволяє налаштувати заголовки запиту, перш ніж його буде надіслано до застосунку. Цей метод дозволяє додати до запиту будь-які власні заголовки:

```php tab=Pest
<?php

test('interacting with headers', function () {
    $response = $this->withHeaders([
        'X-Header' => 'Value',
    ])->post('/user', ['name' => 'Sally']);

    $response->assertStatus(201);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     */
    public function test_interacting_with_headers(): void
    {
        $response = $this->withHeaders([
            'X-Header' => 'Value',
        ])->post('/user', ['name' => 'Sally']);

        $response->assertStatus(201);
    }
}
```

<a name="cookies"></a>
### Cookie

Методи `withCookie` чи `withCookies` дозволяють задати значення cookie перед виконанням запиту. Метод `withCookie` приймає двома аргументами ім'я та значення cookie, а метод `withCookies` - масив пар ім'я / значення:

```php tab=Pest
<?php

test('interacting with cookies', function () {
    $response = $this->withCookie('color', 'blue')->get('/');

    $response = $this->withCookies([
        'color' => 'blue',
        'name' => 'Taylor',
    ])->get('/');

    //
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_interacting_with_cookies(): void
    {
        $response = $this->withCookie('color', 'blue')->get('/');

        $response = $this->withCookies([
            'color' => 'blue',
            'name' => 'Taylor',
        ])->get('/');

        //
    }
}
```

<a name="session-and-authentication"></a>
### Сесія / автентифікація

Laravel надає кілька хелперів для роботи із сесією під час тестування HTTP. Спершу ви можете задати дані сесії заданим масивом через метод `withSession`. Це стає в пригоді, коли треба наповнити сесію даними перед запитом до вашого застосунку:

```php tab=Pest
<?php

test('interacting with the session', function () {
    $response = $this->withSession(['banned' => false])->get('/');

    //
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_interacting_with_the_session(): void
    {
        $response = $this->withSession(['banned' => false])->get('/');

        //
    }
}
```

Сесію в Laravel зазвичай використовують, щоб зберігати стан поточного автентифікованого користувача. Тому допоміжний метод `actingAs` дає простий спосіб автентифікувати заданого користувача як поточного. Наприклад, ми можемо скористатися [фабрикою моделі](/docs/{{version}}/eloquent-factories), щоб згенерувати й автентифікувати користувача:

```php tab=Pest
<?php

use App\Models\User;

test('an action that requires authentication', function () {
    $user = User::factory()->create();

    $response = $this->actingAs($user)
        ->withSession(['banned' => false])
        ->get('/');

    //
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Models\User;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_an_action_that_requires_authentication(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)
            ->withSession(['banned' => false])
            ->get('/');

        //
    }
}
```

Ви також можете вказати, який гард слід використати для автентифікації заданого користувача, передавши ім'я гарда другим аргументом до методу `actingAs`. Переданий методу `actingAs` гард стане також гардом за замовчуванням на час тесту:

```php
$this->actingAs($user, 'web');
```

Якщо ви хочете переконатися, що запит неавтентифікований, скористайтеся методом `actingAsGuest`:

```php
$this->actingAsGuest();
```

<a name="debugging-responses"></a>
### Налагодження відповідей

Після виконання тестового запиту до вашого застосунку методи `dump`, `dumpHeaders` та `dumpSession` дозволяють оглянути й налагодити вміст відповіді:

```php tab=Pest
<?php

test('basic test', function () {
    $response = $this->get('/');

    $response->dump();
    $response->dumpHeaders();
    $response->dumpSession();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_basic_test(): void
    {
        $response = $this->get('/');

        $response->dump();
        $response->dumpHeaders();
        $response->dumpSession();
    }
}
```

Або ж ви можете скористатися методами `dd`, `ddHeaders`, `ddBody`, `ddJson` та `ddSession`, щоб вивести інформацію про відповідь і зупинити виконання:

```php tab=Pest
<?php

test('basic test', function () {
    $response = $this->get('/');

    $response->dd();
    $response->ddHeaders();
    $response->ddBody();
    $response->ddJson();
    $response->ddSession();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_basic_test(): void
    {
        $response = $this->get('/');

        $response->dd();
        $response->ddHeaders();
        $response->ddBody();
        $response->ddJson();
        $response->ddSession();
    }
}
```

<a name="exception-handling"></a>
### Обробка винятків

Іноді вам може знадобитися перевірити, що ваш застосунок кидає певний виняток. Для цього ви можете «підробити» обробник винятків через фасад `Exceptions`. Коли обробник підроблено, ви можете скористатися методами `assertReported` та `assertNotReported`, щоб робити твердження щодо винятків, кинутих під час запиту:

```php tab=Pest
<?php

use App\Exceptions\InvalidOrderException;
use Illuminate\Support\Facades\Exceptions;

test('exception is thrown', function () {
    Exceptions::fake();

    $response = $this->get('/order/1');

    // Assert an exception was thrown...
    Exceptions::assertReported(InvalidOrderException::class);

    // Assert against the exception...
    Exceptions::assertReported(function (InvalidOrderException $e) {
        return $e->getMessage() === 'The order was invalid.';
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Exceptions\InvalidOrderException;
use Illuminate\Support\Facades\Exceptions;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_exception_is_thrown(): void
    {
        Exceptions::fake();

        $response = $this->get('/');

        // Assert an exception was thrown...
        Exceptions::assertReported(InvalidOrderException::class);

        // Assert against the exception...
        Exceptions::assertReported(function (InvalidOrderException $e) {
            return $e->getMessage() === 'The order was invalid.';
        });
    }
}
```

Методи `assertNotReported` та `assertNothingReported` дозволяють перевірити, що заданий виняток не було кинуто під час запиту або що винятків не було взагалі:

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

Ви можете повністю вимкнути обробку винятків для конкретного запиту, викликавши метод `withoutExceptionHandling` перед його виконанням:

```php
$response = $this->withoutExceptionHandling()->get('/');
```

Крім того, якщо ви хочете переконатися, що ваш застосунок не використовує можливостей, які оголошено застарілими в мові PHP чи у ваших бібліотеках, викличте перед запитом метод `withoutDeprecationHandling`. Коли обробку застарілих можливостей вимкнено, попередження про них перетворюються на винятки, і тест провалюється:

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

Метод `assertThrows` дозволяє перевірити, що код усередині заданого замикання кидає виняток указаного типу:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

Якщо ви хочете оглянути кинутий виняток і зробити щодо нього твердження, передайте замикання другим аргументом до методу `assertThrows`:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

Метод `assertDoesntThrow` дозволяє перевірити, що код усередині заданого замикання не кидає жодних винятків:

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
## Тестування JSON API

Laravel також надає кілька хелперів для тестування JSON API та їхніх відповідей. Наприклад, методи `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson` та `optionsJson` дозволяють виконувати JSON-запити з різними HTTP-дієсловами. Ви також можете легко передавати цим методам дані та заголовки. Для початку напишімо тест, який робить запит `POST` до `/api/user` і перевіряє, що повернулися очікувані JSON-дані:

```php tab=Pest
<?php

test('making an api request', function () {
    $response = $this->postJson('/api/user', ['name' => 'Sally']);

    $response
        ->assertStatus(201)
        ->assertJson([
            'created' => true,
        ]);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     */
    public function test_making_an_api_request(): void
    {
        $response = $this->postJson('/api/user', ['name' => 'Sally']);

        $response
            ->assertStatus(201)
            ->assertJson([
                'created' => true,
            ]);
    }
}
```

Крім того, до даних JSON-відповіді можна звертатися як до змінних масиву на самій відповіді - так зручно перевіряти окремі значення, повернені в JSON:

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> Метод `assertJson` перетворює відповідь на масив, щоб перевірити, що заданий масив присутній у JSON-відповіді застосунку. Тож якщо в JSON-відповіді є й інші властивості, цей тест усе одно пройде, доки заданий фрагмент є у відповіді.

<a name="verifying-exact-match"></a>
#### Перевірка точного збігу JSON

Як згадувалося раніше, метод `assertJson` дозволяє перевірити, що фрагмент JSON присутній у JSON-відповіді. Якщо ви хочете переконатися, що заданий масив **точно збігається** з JSON, поверненим вашим застосунком, скористайтеся методом `assertExactJson`:

```php tab=Pest
<?php

test('asserting an exact json match', function () {
    $response = $this->postJson('/user', ['name' => 'Sally']);

    $response
        ->assertStatus(201)
        ->assertExactJson([
            'created' => true,
        ]);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     */
    public function test_asserting_an_exact_json_match(): void
    {
        $response = $this->postJson('/user', ['name' => 'Sally']);

        $response
            ->assertStatus(201)
            ->assertExactJson([
                'created' => true,
            ]);
    }
}
```

<a name="verifying-json-paths"></a>
#### Твердження щодо шляхів у JSON

Якщо ви хочете переконатися, що JSON-відповідь містить задані дані за вказаним шляхом, скористайтеся методом `assertJsonPath`:

```php tab=Pest
<?php

test('asserting a json path value', function () {
    $response = $this->postJson('/user', ['name' => 'Sally']);

    $response
        ->assertStatus(201)
        ->assertJsonPath('team.owner.name', 'Darian');
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     */
    public function test_asserting_a_json_paths_value(): void
    {
        $response = $this->postJson('/user', ['name' => 'Sally']);

        $response
            ->assertStatus(201)
            ->assertJsonPath('team.owner.name', 'Darian');
    }
}
```

Метод `assertJsonPath` також приймає замикання, яке дозволяє динамічно вирішити, чи має твердження пройти:

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

Якщо вам потрібно перевірити кілька шляхів у JSON одночасно, скористайтеся методом `assertJsonPaths`. Очікуване значення для кожного шляху також може бути замиканням:

```php
$response->assertJsonPaths([
    'team.owner.name' => 'Darian',
    'team.owner.email' => fn (string $email) => str($email)->is('*@laravel.com'),
    'team.members.0.name' => 'Sally',
]);
```

Метод `assertJsonMissingPaths` дозволяє перевірити, що кількох шляхів у JSON у відповіді немає:

```php
$response->assertJsonMissingPaths([
    'team.owner.password',
    'team.members.0.api_token',
]);
```

<a name="fluent-json-testing"></a>
### Плавне тестування JSON

Laravel також пропонує гарний спосіб плавно тестувати JSON-відповіді вашого застосунку. Для початку передайте замикання методу `assertJson`. Це замикання буде викликано з екземпляром `Illuminate\Testing\Fluent\AssertableJson`, через який можна робити твердження щодо JSON, поверненого вашим застосунком. Метод `where` дозволяє робити твердження щодо конкретного атрибута JSON, а метод `missing` - перевіряти, що певного атрибута в JSON немає:

```php tab=Pest
use Illuminate\Testing\Fluent\AssertableJson;

test('fluent json', function () {
    $response = $this->getJson('/users/1');

    $response
        ->assertJson(fn (AssertableJson $json) =>
            $json->where('id', 1)
                ->where('name', 'Victoria Faith')
                ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                ->whereNot('status', 'pending')
                ->missing('password')
                ->etc()
        );
});
```

```php tab=PHPUnit
use Illuminate\Testing\Fluent\AssertableJson;

/**
 * A basic functional test example.
 */
public function test_fluent_json(): void
{
    $response = $this->getJson('/users/1');

    $response
        ->assertJson(fn (AssertableJson $json) =>
            $json->where('id', 1)
                ->where('name', 'Victoria Faith')
                ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                ->whereNot('status', 'pending')
                ->missing('password')
                ->etc()
        );
}
```

#### Як працює метод `etc`

У прикладі вище ви могли помітити, що наприкінці ланцюжка тверджень ми викликали метод `etc`. Цей метод повідомляє Laravel, що в об'єкті JSON можуть бути й інші атрибути. Якщо метод `etc` не використати, тест провалиться, коли в об'єкті JSON виявляться інші атрибути, щодо яких ви не робили тверджень.

Задум такої поведінки - захистити вас від ненавмисного розкриття чутливої інформації у ваших JSON-відповідях, змушуючи або явно зробити твердження щодо атрибута, або явно дозволити додаткові атрибути методом `etc`.

Проте майте на увазі: відсутність методу `etc` у вашому ланцюжку тверджень не гарантує, що додаткові атрибути не додаються до масивів, вкладених у ваш об'єкт JSON. Метод `etc` гарантує лише те, що додаткових атрибутів немає на тому рівні вкладеності, на якому його викликано.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### Перевірка наявності / відсутності атрибутів

Щоб перевірити, що атрибут присутній чи відсутній, скористайтеся методами `has` та `missing`:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

Крім того, методи `hasAll` та `missingAll` дозволяють перевірити наявність чи відсутність кількох атрибутів одночасно:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

Метод `hasAny` дозволяє визначити, чи присутній хоча б один атрибут із заданого списку:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### Твердження щодо колекцій JSON

Часто ваш маршрут повертатиме JSON-відповідь із кількома елементами - наприклад, кількома користувачами:

```php
Route::get('/users', function () {
    return User::all();
});
```

У таких випадках ми можемо скористатися методом `has` плавного об'єкта JSON, щоб робити твердження щодо користувачів у відповіді. Наприклад, перевірмо, що JSON-відповідь містить трьох користувачів. Далі зробімо кілька тверджень щодо першого користувача в колекції методом `first`. Метод `first` приймає замикання, яке отримує інший придатний до тверджень JSON-рядок, - з ним ми можемо робити твердження щодо першого об'єкта колекції:

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has(3)
            ->first(fn (AssertableJson $json) =>
                $json->where('id', 1)
                    ->where('name', 'Victoria Faith')
                    ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                    ->missing('password')
                    ->etc()
            )
    );
```

Якщо ви хочете зробити ті самі твердження щодо кожного елемента колекції JSON, скористайтеся методом `each`:

```php
$response
  ->assertJson(fn (AssertableJson $json) =>
      $json->has(3)
          ->each(fn (AssertableJson $json) =>
              $json->whereType('id', 'integer')
                  ->whereType('name', 'string')
                  ->whereType('email', 'string')
                  ->missing('password')
                  ->etc()
          )
  );
```

<a name="scoping-json-collection-assertions"></a>
#### Обмеження тверджень щодо колекцій JSON

Іноді маршрути вашого застосунку повертатимуть колекції JSON з іменованими ключами:

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

Тестуючи такі маршрути, ви можете скористатися методом `has`, щоб перевірити кількість елементів у колекції. Крім того, метод `has` дозволяє обмежити ланцюжок тверджень:

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
            ->has('users', 3)
            ->has('users.0', fn (AssertableJson $json) =>
                $json->where('id', 1)
                    ->where('name', 'Victoria Faith')
                    ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                    ->missing('password')
                    ->etc()
            )
    );
```

Проте замість двох окремих викликів методу `has` для перевірки колекції `users` ви можете зробити один виклик, передавши замикання третім параметром. У такому разі замикання буде викликано автоматично й обмежено першим елементом колекції:

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
            ->has('users', 3, fn (AssertableJson $json) =>
                $json->where('id', 1)
                    ->where('name', 'Victoria Faith')
                    ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                    ->missing('password')
                    ->etc()
            )
    );
```

<a name="asserting-json-types"></a>
#### Перевірка типів у JSON

Ви можете захотіти лише перевірити, що властивості JSON-відповіді мають певний тип. Клас `Illuminate\Testing\Fluent\AssertableJson` надає для цього методи `whereType` та `whereAllType`:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

Ви можете вказати кілька типів через символ `|` або передати масив типів другим параметром до методу `whereType`. Твердження буде успішним, якщо значення у відповіді має будь-який із перелічених типів:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

Методи `whereType` та `whereAllType` розпізнають такі типи: `string`, `integer`, `double`, `boolean`, `array` та `null`.

<a name="testing-file-uploads"></a>
## Тестування завантаження файлів

Клас `Illuminate\Http\UploadedFile` має метод `fake`, який дозволяє генерувати фіктивні файли чи зображення для тестування. У поєднанні з методом `fake` фасада `Storage` це суттєво спрощує тестування завантаження файлів. Наприклад, ви можете поєднати ці дві можливості, щоб легко протестувати форму завантаження аватара:

```php tab=Pest
<?php

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

test('avatars can be uploaded', function () {
    Storage::fake('avatars');

    $file = UploadedFile::fake()->image('avatar.jpg');

    $response = $this->post('/avatar', [
        'avatar' => $file,
    ]);

    Storage::disk('avatars')->assertExists($file->hashName());
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_avatars_can_be_uploaded(): void
    {
        Storage::fake('avatars');

        $file = UploadedFile::fake()->image('avatar.jpg');

        $response = $this->post('/avatar', [
            'avatar' => $file,
        ]);

        Storage::disk('avatars')->assertExists($file->hashName());
    }
}
```

Якщо ви хочете перевірити, що заданого файлу не існує, скористайтеся методом `assertMissing`, який надає фасад `Storage`:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### Налаштування фіктивних файлів

Створюючи файли методом `fake` класу `UploadedFile`, ви можете вказати ширину, висоту й розмір зображення (у кілобайтах), щоб краще перевірити правила валідації вашого застосунку:

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

Окрім зображень, ви можете створювати файли будь-якого іншого типу методом `create`:

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

За потреби ви можете передати методу аргумент `$mimeType`, щоб явно вказати MIME-тип, який має повертати файл:

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## Тестування представлень

Laravel також дозволяє відрендерити представлення, не виконуючи симульованого HTTP-запиту до застосунку. Для цього викличте у своєму тесті метод `view`. Метод `view` приймає ім'я представлення та необов'язковий масив даних. Він повертає екземпляр `Illuminate\Testing\TestView`, який пропонує кілька методів для зручних тверджень щодо вмісту представлення:

```php tab=Pest
<?php

test('a welcome view can be rendered', function () {
    $view = $this->view('welcome', ['name' => 'Taylor']);

    $view->assertSee('Taylor');
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_a_welcome_view_can_be_rendered(): void
    {
        $view = $this->view('welcome', ['name' => 'Taylor']);

        $view->assertSee('Taylor');
    }
}
```

Клас `TestView` надає такі методи тверджень: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee` та `assertDontSeeText`.

За потреби ви можете отримати сирий відрендерений вміст представлення, привівши екземпляр `TestView` до рядка:

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### Передавання помилок

Деякі представлення можуть залежати від помилок, переданих у [глобальному контейнері помилок Laravel](/docs/{{version}}/validation#quick-displaying-the-validation-errors). Щоб наповнити контейнер помилок повідомленнями, скористайтеся методом `withViewErrors`:

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Рендеринг Blade і компонентів

За потреби ви можете скористатися методом `blade`, щоб обчислити й відрендерити сирий рядок [Blade](/docs/{{version}}/blade). Як і метод `view`, метод `blade` повертає екземпляр `Illuminate\Testing\TestView`:

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

Метод `component` дозволяє обчислити й відрендерити [компонент Blade](/docs/{{version}}/blade#components). Метод `component` повертає екземпляр `Illuminate\Testing\TestComponent`:

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="caching-routes"></a>
## Кешування маршрутів

Перед прогоном тесту Laravel завантажує свіжий екземпляр застосунку, зокрема збирає всі визначені маршрути. Якщо у вашому застосунку багато файлів маршрутів, вам може знадобитися додати до тест-кейсів трейт `Illuminate\Foundation\Testing\WithCachedRoutes`. У тестах, що використовують цей трейт, маршрути будуються один раз і зберігаються в пам'яті - тобто процес збирання маршрутів виконується лише раз для всього вашого набору тестів:

```php tab=Pest
<?php

use App\Http\Controllers\UserController;
use Illuminate\Foundation\Testing\WithCachedRoutes;

pest()->use(WithCachedRoutes::class);

test('basic example', function () {
    $this->get(action([UserController::class, 'index']));

    // ...
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Http\Controllers\UserController;
use Illuminate\Foundation\Testing\WithCachedRoutes;
use Tests\TestCase;

class BasicTest extends TestCase
{
    use WithCachedRoutes;

    /**
     * A basic functional test example.
     */
    public function test_basic_example(): void
    {
        $response = $this->get(action([UserController::class, 'index']));

        // ...
    }
}
```

<a name="available-assertions"></a>
## Доступні твердження

<a name="response-assertions"></a>
### Твердження щодо відповіді

Клас `Illuminate\Testing\TestResponse` у Laravel надає різні власні методи тверджень, якими ви можете скористатися під час тестування свого застосунку. Ці твердження доступні на відповіді, яку повертають тестові методи `json`, `get`, `post`, `put` та `delete`:

<style>
    .collection-method-list > p {
        columns: 14.4em 2; -moz-columns: 14.4em 2; -webkit-columns: 14.4em 2;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

<div class="collection-method-list" markdown="1">

[assertAccepted](#assert-accepted)
[assertBadRequest](#assert-bad-request)
[assertClientError](#assert-client-error)
[assertConflict](#assert-conflict)
[assertCookie](#assert-cookie)
[assertCookieExpired](#assert-cookie-expired)
[assertCookieNotExpired](#assert-cookie-not-expired)
[assertCookieMissing](#assert-cookie-missing)
[assertCreated](#assert-created)
[assertDontSee](#assert-dont-see)
[assertDontSeeText](#assert-dont-see-text)
[assertDownload](#assert-download)
[assertExactJson](#assert-exact-json)
[assertExactJsonStructure](#assert-exact-json-structure)
[assertFailedDependency](#assert-failed-dependency)
[assertForbidden](#assert-forbidden)
[assertFound](#assert-found)
[assertGone](#assert-gone)
[assertHeader](#assert-header)
[assertHeaderContains](#assert-header-contains)
[assertHeaderMissing](#assert-header-missing)
[assertInternalServerError](#assert-internal-server-error)
[assertJson](#assert-json)
[assertJsonCount](#assert-json-count)
[assertJsonFragment](#assert-json-fragment)
[assertJsonIsArray](#assert-json-is-array)
[assertJsonIsObject](#assert-json-is-object)
[assertJsonMissing](#assert-json-missing)
[assertJsonMissingExact](#assert-json-missing-exact)
[assertJsonMissingValidationErrors](#assert-json-missing-validation-errors)
[assertJsonPath](#assert-json-path)
[assertJsonPaths](#assert-json-paths)
[assertJsonMissingPath](#assert-json-missing-path)
[assertJsonMissingPaths](#assert-json-missing-paths)
[assertJsonStructure](#assert-json-structure)
[assertJsonValidationErrors](#assert-json-validation-errors)
[assertJsonValidationErrorFor](#assert-json-validation-error-for)
[assertLocation](#assert-location)
[assertMethodNotAllowed](#assert-method-not-allowed)
[assertMovedPermanently](#assert-moved-permanently)
[assertContent](#assert-content)
[assertNoContent](#assert-no-content)
[assertStreamed](#assert-streamed)
[assertStreamedContent](#assert-streamed-content)
[assertNotFound](#assert-not-found)
[assertOk](#assert-ok)
[assertPaymentRequired](#assert-payment-required)
[assertPlainCookie](#assert-plain-cookie)
[assertRedirect](#assert-redirect)
[assertRedirectBack](#assert-redirect-back)
[assertRedirectBackWithErrors](#assert-redirect-back-with-errors)
[assertRedirectBackWithoutErrors](#assert-redirect-back-without-errors)
[assertRedirectContains](#assert-redirect-contains)
[assertRedirectToRoute](#assert-redirect-to-route)
[assertRedirectToSignedRoute](#assert-redirect-to-signed-route)
[assertRequestTimeout](#assert-request-timeout)
[assertSee](#assert-see)
[assertSeeInOrder](#assert-see-in-order)
[assertSeeText](#assert-see-text)
[assertSeeTextInOrder](#assert-see-text-in-order)
[assertServerError](#assert-server-error)
[assertServiceUnavailable](#assert-service-unavailable)
[assertSessionHas](#assert-session-has)
[assertSessionHasInput](#assert-session-has-input)
[assertSessionHasAll](#assert-session-has-all)
[assertSessionHasErrors](#assert-session-has-errors)
[assertSessionHasErrorsIn](#assert-session-has-errors-in)
[assertSessionHasNoErrors](#assert-session-has-no-errors)
[assertSessionDoesntHaveErrors](#assert-session-doesnt-have-errors)
[assertSessionMissing](#assert-session-missing)
[assertSessionMissingInput](#assert-session-missing-input)
[assertStatus](#assert-status)
[assertSuccessful](#assert-successful)
[assertTooManyRequests](#assert-too-many-requests)
[assertUnauthorized](#assert-unauthorized)
[assertUnprocessable](#assert-unprocessable)
[assertUnsupportedMediaType](#assert-unsupported-media-type)
[assertValid](#assert-valid)
[assertInvalid](#assert-invalid)
[assertViewHas](#assert-view-has)
[assertViewHasAll](#assert-view-has-all)
[assertViewIs](#assert-view-is)
[assertViewMissing](#assert-view-missing)

</div>

<a name="assert-accepted"></a>
#### assertAccepted

Перевіряє, що відповідь має код статусу HTTP «accepted» (202):

```php
$response->assertAccepted();
```

<a name="assert-bad-request"></a>
#### assertBadRequest

Перевіряє, що відповідь має код статусу HTTP «bad request» (400):

```php
$response->assertBadRequest();
```

<a name="assert-client-error"></a>
#### assertClientError

Перевіряє, що відповідь має код статусу HTTP клієнтської помилки (>= 400, < 500):

```php
$response->assertClientError();
```

<a name="assert-conflict"></a>
#### assertConflict

Перевіряє, що відповідь має код статусу HTTP «conflict» (409):

```php
$response->assertConflict();
```

<a name="assert-cookie"></a>
#### assertCookie

Перевіряє, що відповідь містить заданий cookie:

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### assertCookieExpired

Перевіряє, що відповідь містить заданий cookie і що його термін дії минув:

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

Перевіряє, що відповідь містить заданий cookie і що його термін дії не минув:

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

Перевіряє, що відповідь не містить заданого cookie:

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### assertCreated

Перевіряє, що відповідь має код статусу HTTP 201:

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### assertDontSee

Перевіряє, що заданого рядка немає у відповіді, поверненій застосунком. Це твердження автоматично екранує заданий рядок, якщо ви не передасте другим аргументом `false`:

```php
$response->assertDontSee($value, $escape = true);
```

<a name="assert-dont-see-text"></a>
#### assertDontSeeText

Перевіряє, що заданого рядка немає в тексті відповіді. Це твердження автоматично екранує заданий рядок, якщо ви не передасте другим аргументом `false`. Перед перевіркою метод пропускає вміст відповіді через PHP-функцію `strip_tags`:

```php
$response->assertDontSeeText($value, $escape = true);
```

<a name="assert-download"></a>
#### assertDownload

Перевіряє, що відповідь є «завантаженням». Зазвичай це означає, що викликаний маршрут повернув відповідь `Response::download`, `BinaryFileResponse` чи `Storage::download`:

```php
$response->assertDownload();
```

За бажання ви можете перевірити, що файлу для завантаження було призначено задане ім'я:

```php
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### assertExactJson

Перевіряє, що відповідь точно збігається із заданими даними JSON:

```php
$response->assertExactJson(array $data);
```

<a name="assert-exact-json-structure"></a>
#### assertExactJsonStructure

Перевіряє, що відповідь точно збігається із заданою структурою JSON:

```php
$response->assertExactJsonStructure(array $data);
```

Цей метод - суворіший варіант [assertJsonStructure](#assert-json-structure). На відміну від `assertJsonStructure`, він провалиться, якщо відповідь містить будь-які ключі, не включені явно до очікуваної структури JSON.

<a name="assert-failed-dependency"></a>
#### assertFailedDependency

Перевіряє, що відповідь має код статусу HTTP «failed dependency» (424):

```php
$response->assertFailedDependency();
```

<a name="assert-forbidden"></a>
#### assertForbidden

Перевіряє, що відповідь має код статусу HTTP «forbidden» (403):

```php
$response->assertForbidden();
```

<a name="assert-found"></a>
#### assertFound

Перевіряє, що відповідь має код статусу HTTP «found» (302):

```php
$response->assertFound();
```

<a name="assert-gone"></a>
#### assertGone

Перевіряє, що відповідь має код статусу HTTP «gone» (410):

```php
$response->assertGone();
```

<a name="assert-header"></a>
#### assertHeader

Перевіряє, що у відповіді присутній заданий заголовок із заданим значенням:

```php
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-contains"></a>
#### assertHeaderContains

Перевіряє, що заданий заголовок містить задане значення-підрядок:

```php
$response->assertHeaderContains($headerName, $value);
```

<a name="assert-header-missing"></a>
#### assertHeaderMissing

Перевіряє, що заданого заголовка у відповіді немає:

```php
$response->assertHeaderMissing($headerName);
```

<a name="assert-internal-server-error"></a>
#### assertInternalServerError

Перевіряє, що відповідь має код статусу HTTP «Internal Server Error» (500):

```php
$response->assertInternalServerError();
```

<a name="assert-json"></a>
#### assertJson

Перевіряє, що відповідь містить задані дані JSON:

```php
$response->assertJson(array $data, $strict = false);
```

Метод `assertJson` перетворює відповідь на масив, щоб перевірити, що заданий масив присутній у JSON-відповіді застосунку. Тож якщо в JSON-відповіді є й інші властивості, цей тест усе одно пройде, доки заданий фрагмент є у відповіді.

<a name="assert-json-count"></a>
#### assertJsonCount

Перевіряє, що JSON відповіді містить масив з очікуваною кількістю елементів за заданим ключем:

```php
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### assertJsonFragment

Перевіряє, що відповідь містить задані дані JSON будь-де у відповіді:

```php
Route::get('/users', function () {
    return [
        'users' => [
            [
                'name' => 'Taylor Otwell',
            ],
        ],
    ];
});

$response->assertJsonFragment(['name' => 'Taylor Otwell']);
```

<a name="assert-json-is-array"></a>
#### assertJsonIsArray

Перевіряє, що JSON відповіді є масивом:

```php
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
#### assertJsonIsObject

Перевіряє, що JSON відповіді є об'єктом:

```php
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
#### assertJsonMissing

Перевіряє, що відповідь не містить заданих даних JSON:

```php
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

Перевіряє, що відповідь не містить точно заданих даних JSON:

```php
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

Перевіряє, що у відповіді немає помилок валідації JSON для заданих ключів:

```php
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> Загальніший метод [assertValid](#assert-valid) дозволяє перевірити, що у відповіді немає помилок валідації, повернених як JSON, **і** що жодних помилок не було передано до сховища сесії.

<a name="assert-json-path"></a>
#### assertJsonPath

Перевіряє, що відповідь містить задані дані за вказаним шляхом:

```php
$response->assertJsonPath($path, $expectedValue);
```

Наприклад, якщо ваш застосунок повертає таку JSON-відповідь:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

Ви можете перевірити, що властивість `name` об'єкта `user` дорівнює заданому значенню, ось так:

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-paths"></a>
#### assertJsonPaths

Перевіряє, що відповідь містить задані дані за вказаними шляхами:

```php
$response->assertJsonPaths(array $paths);
```

Наприклад, ви можете перевірити кілька значень у відповіді одночасно:

```php
$response->assertJsonPaths([
    'user.name' => 'Steve Schoger',
    'user.email' => fn (string $email) => str($email)->endsWith('@laravel.com'),
]);
```

<a name="assert-json-missing-path"></a>
#### assertJsonMissingPath

Перевіряє, що відповідь не містить заданого шляху:

```php
$response->assertJsonMissingPath($path);
```

Наприклад, якщо ваш застосунок повертає таку JSON-відповідь:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

Ви можете перевірити, що вона не містить властивості `email` об'єкта `user`:

```php
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-missing-paths"></a>
#### assertJsonMissingPaths

Перевіряє, що відповідь не містить заданих шляхів:

```php
$response->assertJsonMissingPaths($paths);
```

Наприклад, ви можете перевірити, що у відповіді немає кількох шляхів:

```php
$response->assertJsonMissingPaths([
    'user.email',
    'user.password',
]);
```

<a name="assert-json-structure"></a>
#### assertJsonStructure

Перевіряє, що відповідь має задану структуру JSON:

```php
$response->assertJsonStructure(array $structure);
```

Наприклад, якщо JSON-відповідь вашого застосунку містить такі дані:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

Ви можете перевірити, що структура JSON відповідає вашим очікуванням, ось так:

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

Іноді JSON-відповіді вашого застосунку можуть містити масиви об'єктів:

```json
{
    "user": [
        {
            "name": "Steve Schoger",
            "age": 55,
            "location": "Earth"
        },
        {
            "name": "Mary Schoger",
            "age": 60,
            "location": "Earth"
        }
    ]
}
```

У цій ситуації ви можете скористатися символом `*`, щоб перевірити структуру всіх об'єктів масиву:

```php
$response->assertJsonStructure([
    'user' => [
        '*' => [
             'name',
             'age',
             'location'
        ]
    ]
]);
```

<a name="assert-json-validation-errors"></a>
#### assertJsonValidationErrors

Перевіряє, що відповідь має задані помилки валідації JSON для заданих ключів. Цей метод варто використовувати, коли ви перевіряєте відповіді, у яких помилки валідації повертаються структурою JSON, а не передаються до сесії:

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> Загальніший метод [assertInvalid](#assert-invalid) дозволяє перевірити, що у відповіді є помилки валідації, повернені як JSON, **або** що помилки було передано до сховища сесії.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

Перевіряє, що відповідь має будь-які помилки валідації JSON для заданого ключа:

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-method-not-allowed"></a>
#### assertMethodNotAllowed

Перевіряє, що відповідь має код статусу HTTP «method not allowed» (405):

```php
$response->assertMethodNotAllowed();
```

<a name="assert-moved-permanently"></a>
#### assertMovedPermanently

Перевіряє, що відповідь має код статусу HTTP «moved permanently» (301):

```php
$response->assertMovedPermanently();
```

<a name="assert-location"></a>
#### assertLocation

Перевіряє, що відповідь має заданий URI у заголовку `Location`:

```php
$response->assertLocation($uri);
```

<a name="assert-content"></a>
#### assertContent

Перевіряє, що заданий рядок збігається з вмістом відповіді:

```php
$response->assertContent($value);
```

<a name="assert-no-content"></a>
#### assertNoContent

Перевіряє, що відповідь має заданий код статусу HTTP і не має вмісту:

```php
$response->assertNoContent($status = 204);
```

<a name="assert-streamed"></a>
#### assertStreamed

Перевіряє, що відповідь була потоковою:

    $response->assertStreamed();

<a name="assert-streamed-content"></a>
#### assertStreamedContent

Перевіряє, що заданий рядок збігається з вмістом потокової відповіді:

```php
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
#### assertNotFound

Перевіряє, що відповідь має код статусу HTTP «not found» (404):

```php
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### assertOk

Перевіряє, що відповідь має код статусу HTTP 200:

```php
$response->assertOk();
```

<a name="assert-payment-required"></a>
#### assertPaymentRequired

Перевіряє, що відповідь має код статусу HTTP «payment required» (402):

```php
$response->assertPaymentRequired();
```

<a name="assert-plain-cookie"></a>
#### assertPlainCookie

Перевіряє, що відповідь містить заданий незашифрований cookie:

```php
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
#### assertRedirect

Перевіряє, що відповідь є перенаправленням на заданий URI:

```php
$response->assertRedirect($uri = null);
```

<a name="assert-redirect-back"></a>
#### assertRedirectBack

Перевіряє, чи є відповідь перенаправленням назад на попередню сторінку:

```php
$response->assertRedirectBack();
```

<a name="assert-redirect-back-with-errors"></a>
#### assertRedirectBackWithErrors

Перевіряє, чи є відповідь перенаправленням назад на попередню сторінку і чи [сесія містить задані помилки](#assert-session-has-errors):

```php
$response->assertRedirectBackWithErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

<a name="assert-redirect-back-without-errors"></a>
#### assertRedirectBackWithoutErrors

Перевіряє, чи є відповідь перенаправленням назад на попередню сторінку і чи сесія не містить жодних повідомлень про помилки:

```php
$response->assertRedirectBackWithoutErrors();
```

<a name="assert-redirect-contains"></a>
#### assertRedirectContains

Перевіряє, чи є відповідь перенаправленням на URI, що містить заданий рядок:

```php
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

Перевіряє, що відповідь є перенаправленням на заданий [іменований маршрут](/docs/{{version}}/routing#named-routes):

```php
$response->assertRedirectToRoute($name, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

Перевіряє, що відповідь є перенаправленням на заданий [підписаний маршрут](/docs/{{version}}/urls#signed-urls):

```php
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-request-timeout"></a>
#### assertRequestTimeout

Перевіряє, що відповідь має код статусу HTTP «request timeout» (408):

```php
$response->assertRequestTimeout();
```

<a name="assert-see"></a>
#### assertSee

Перевіряє, що заданий рядок є у відповіді. Це твердження автоматично екранує заданий рядок, якщо ви не передасте другим аргументом `false`:

```php
$response->assertSee($value, $escape = true);
```

<a name="assert-see-in-order"></a>
#### assertSeeInOrder

Перевіряє, що задані рядки є у відповіді саме в такому порядку. Це твердження автоматично екранує задані рядки, якщо ви не передасте другим аргументом `false`:

```php
$response->assertSeeInOrder(array $values, $escape = true);
```

<a name="assert-see-text"></a>
#### assertSeeText

Перевіряє, що заданий рядок є в тексті відповіді. Це твердження автоматично екранує заданий рядок, якщо ви не передасте другим аргументом `false`. Перед перевіркою вміст відповіді буде пропущено через PHP-функцію `strip_tags`:

```php
$response->assertSeeText($value, $escape = true);
```

<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

Перевіряє, що задані рядки є в тексті відповіді саме в такому порядку. Це твердження автоматично екранує задані рядки, якщо ви не передасте другим аргументом `false`. Перед перевіркою вміст відповіді буде пропущено через PHP-функцію `strip_tags`:

```php
$response->assertSeeTextInOrder(array $values, $escape = true);
```

<a name="assert-server-error"></a>
#### assertServerError

Перевіряє, що відповідь має код статусу HTTP серверної помилки (>= 500 , < 600):

```php
$response->assertServerError();
```

<a name="assert-service-unavailable"></a>
#### assertServiceUnavailable

Перевіряє, що відповідь має код статусу HTTP «Service Unavailable» (503):

```php
$response->assertServiceUnavailable();
```

<a name="assert-session-has"></a>
#### assertSessionHas

Перевіряє, що сесія містить заданий фрагмент даних:

```php
$response->assertSessionHas($key, $value = null);
```

За потреби другим аргументом до методу `assertSessionHas` можна передати замикання. Твердження пройде, якщо замикання поверне `true`:

```php
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

Перевіряє, що сесія має задане значення в [масиві переданих даних форми](/docs/{{version}}/responses#redirecting-with-flashed-session-data):

```php
$response->assertSessionHasInput($key, $value = null);
```

За потреби другим аргументом до методу `assertSessionHasInput` можна передати замикання. Твердження пройде, якщо замикання поверне `true`:

```php
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

Перевіряє, що сесія містить заданий масив пар ключ / значення:

```php
$response->assertSessionHasAll(array $data);
```

Наприклад, якщо сесія вашого застосунку містить ключі `name` та `status`, ви можете перевірити, що обидва існують і мають указані значення, ось так:

```php
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

Перевіряє, що сесія містить помилку для заданих `$keys`. Якщо `$keys` - асоціативний масив, перевіряє, що сесія містить конкретне повідомлення про помилку (значення) для кожного поля (ключа). Цей метод варто використовувати, тестуючи маршрути, які передають помилки валідації до сесії, а не повертають їх структурою JSON:

```php
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

Наприклад, щоб перевірити, що поля `name` та `email` мають передані до сесії повідомлення про помилки валідації, викличте метод `assertSessionHasErrors` ось так:

```php
$response->assertSessionHasErrors(['name', 'email']);
```

Або ж ви можете перевірити, що задане поле має конкретне повідомлення про помилку валідації:

```php
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> Загальніший метод [assertInvalid](#assert-invalid) дозволяє перевірити, що у відповіді є помилки валідації, повернені як JSON, **або** що помилки було передано до сховища сесії.

<a name="assert-session-has-errors-in"></a>
#### assertSessionHasErrorsIn

Перевіряє, що сесія містить помилку для заданих `$keys` у конкретному [контейнері помилок](/docs/{{version}}/validation#named-error-bags). Якщо `$keys` - асоціативний масив, перевіряє, що сесія містить конкретне повідомлення про помилку (значення) для кожного поля (ключа) в межах цього контейнера:

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

Перевіряє, що сесія не має помилок валідації:

```php
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

Перевіряє, що сесія не має помилок валідації для заданих ключів:

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> Загальніший метод [assertValid](#assert-valid) дозволяє перевірити, що у відповіді немає помилок валідації, повернених як JSON, **і** що жодних помилок не було передано до сховища сесії.

<a name="assert-session-missing"></a>
#### assertSessionMissing

Перевіряє, що сесія не містить заданого ключа:

```php
$response->assertSessionMissing($key);
```

<a name="assert-session-missing-input"></a>
#### assertSessionMissingInput

Перевіряє, що в сесії немає заданого ключа в масиві переданих даних форми:

```php
$response->assertSessionMissingInput($key);
```

<a name="assert-status"></a>
#### assertStatus

Перевіряє, що відповідь має заданий код статусу HTTP:

```php
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### assertSuccessful

Перевіряє, що відповідь має успішний код статусу HTTP (>= 200 і < 300):

```php
$response->assertSuccessful();
```

<a name="assert-too-many-requests"></a>
#### assertTooManyRequests

Перевіряє, що відповідь має код статусу HTTP «too many requests» (429):

```php
$response->assertTooManyRequests();
```

<a name="assert-unauthorized"></a>
#### assertUnauthorized

Перевіряє, що відповідь має код статусу HTTP «unauthorized» (401):

```php
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### assertUnprocessable

Перевіряє, що відповідь має код статусу HTTP «unprocessable entity» (422):

```php
$response->assertUnprocessable();
```

<a name="assert-unsupported-media-type"></a>
#### assertUnsupportedMediaType

Перевіряє, що відповідь має код статусу HTTP «unsupported media type» (415):

```php
$response->assertUnsupportedMediaType();
```

<a name="assert-valid"></a>
#### assertValid

Перевіряє, що у відповіді немає помилок валідації для заданих ключів. Цей метод можна використовувати для перевірки відповідей, у яких помилки валідації повертаються структурою JSON або передаються до сесії:

```php
// Assert that no validation errors are present...
$response->assertValid();

// Assert that the given keys do not have validation errors...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### assertInvalid

Перевіряє, що у відповіді є помилки валідації для заданих ключів. Цей метод можна використовувати для перевірки відповідей, у яких помилки валідації повертаються структурою JSON або передаються до сесії:

```php
$response->assertInvalid(['name', 'email']);
```

Ви також можете перевірити, що заданий ключ має конкретне повідомлення про помилку валідації. При цьому ви можете передати повне повідомлення або лише невелику його частину:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

Якщо ви хочете перевірити, що задані поля - єдині з помилками валідації, скористайтеся методом `assertOnlyInvalid`:

```php
$response->assertOnlyInvalid(['name', 'email']);
```

<a name="assert-view-has"></a>
#### assertViewHas

Перевіряє, що представлення відповіді містить заданий фрагмент даних:

```php
$response->assertViewHas($key, $value = null);
```

Передавши замикання другим аргументом до методу `assertViewHas`, ви зможете оглянути конкретний фрагмент даних представлення й зробити щодо нього твердження:

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

Крім того, до даних представлення можна звертатися як до змінних масиву на відповіді - так їх зручно оглядати:

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### assertViewHasAll

Перевіряє, що представлення відповіді має заданий перелік даних:

```php
$response->assertViewHasAll(array $data);
```

Цей метод дозволяє перевірити, що представлення просто містить дані за заданими ключами:

```php
$response->assertViewHasAll([
    'name',
    'email',
]);
```

Або ж ви можете перевірити, що дані представлення присутні й мають конкретні значення:

```php
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### assertViewIs

Перевіряє, що маршрут повернув задане представлення:

```php
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### assertViewMissing

Перевіряє, що заданий ключ даних не було передано до представлення, поверненого у відповіді застосунку:

```php
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### Твердження щодо автентифікації

Laravel також надає різні твердження, пов'язані з автентифікацією, якими ви можете скористатися у функціональних тестах свого застосунку. Зверніть увагу: ці методи викликаються на самому тестовому класі, а не на екземплярі `Illuminate\Testing\TestResponse`, який повертають методи на кшталт `get` і `post`.

<a name="assert-authenticated"></a>
#### assertAuthenticated

Перевіряє, що користувач автентифікований:

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### assertGuest

Перевіряє, що користувач не автентифікований:

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

Перевіряє, що автентифікований конкретний користувач:

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## Твердження щодо валідації

Laravel надає два основні твердження, пов'язані з валідацією, які дозволяють переконатися, що дані у вашому запиті були дійсними чи недійсними.

<a name="validation-assert-valid"></a>
#### assertValid

Перевіряє, що у відповіді немає помилок валідації для заданих ключів. Цей метод можна використовувати для перевірки відповідей, у яких помилки валідації повертаються структурою JSON або передаються до сесії:

```php
// Assert that no validation errors are present...
$response->assertValid();

// Assert that the given keys do not have validation errors...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### assertInvalid

Перевіряє, що у відповіді є помилки валідації для заданих ключів. Цей метод можна використовувати для перевірки відповідей, у яких помилки валідації повертаються структурою JSON або передаються до сесії:

```php
$response->assertInvalid(['name', 'email']);
```

Ви також можете перевірити, що заданий ключ має конкретне повідомлення про помилку валідації. При цьому ви можете передати повне повідомлення або лише невелику його частину:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```
