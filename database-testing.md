---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Тестування бази даних

- [Вступ](#introduction)
    - [Скидання бази даних після кожного тесту](#resetting-the-database-after-each-test)
- [Фабрики моделей](#model-factories)
- [Запуск сідерів](#running-seeders)
- [Доступні твердження](#available-assertions)

<a name="introduction"></a>
## Вступ

Laravel надає різні корисні інструменти й твердження, які полегшують тестування застосунків, що працюють із базою даних. До того ж фабрики моделей і сідери Laravel роблять створення тестових записів безболісним - через моделі Eloquent і зв'язки вашого застосунку. Усі ці потужні можливості ми розглянемо далі в цій документації.

<a name="resetting-the-database-after-each-test"></a>
### Скидання бази даних після кожного тесту

Перш ніж рухатися далі, обговорімо, як скидати вашу базу даних після кожного тесту, щоб дані з попереднього тесту не заважали наступним. Про це подбає трейт `Illuminate\Foundation\Testing\RefreshDatabase`, що входить до Laravel. Просто застосуйте цей трейт до свого тестового класу:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\RefreshDatabase;

pest()->use(RefreshDatabase::class);

test('basic example', function () {
    $response = $this->get('/');

    // ...
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    use RefreshDatabase;

    /**
     * A basic functional test example.
     */
    public function test_basic_example(): void
    {
        $response = $this->get('/');

        // ...
    }
}
```

Трейт `Illuminate\Foundation\Testing\RefreshDatabase` не мігрує вашу базу даних, якщо схема актуальна. Натомість він лише виконує тест у межах транзакції бази даних. Тому будь-які записи, додані до бази тест-кейсами, які не використовують цей трейт, можуть залишитися в базі.

Якщо ви хочете повністю скинути базу даних, скористайтеся натомість трейтами `Illuminate\Foundation\Testing\DatabaseMigrations` чи `Illuminate\Foundation\Testing\DatabaseTruncation`. Проте обидва ці варіанти значно повільніші за трейт `RefreshDatabase`.

<a name="model-factories"></a>
## Фабрики моделей

Під час тестування вам може знадобитися вставити в базу кілька записів перед виконанням тесту. Замість того щоб вручну вказувати значення кожного стовпця при створенні цих тестових даних, Laravel дозволяє описати набір атрибутів за замовчуванням для кожної з ваших [моделей Eloquent](/docs/{{version}}/eloquent) через [фабрики моделей](/docs/{{version}}/eloquent-factories).

Щоб дізнатися більше про створення й використання фабрик моделей, зверніться до повної [документації про фабрики моделей](/docs/{{version}}/eloquent-factories). Коли фабрику моделі визначено, ви можете скористатися нею у своєму тесті, щоб створювати моделі:

```php tab=Pest
use App\Models\User;

test('models can be instantiated', function () {
    $user = User::factory()->create();

    // ...
});
```

```php tab=PHPUnit
use App\Models\User;

public function test_models_can_be_instantiated(): void
{
    $user = User::factory()->create();

    // ...
}
```

<a name="running-seeders"></a>
## Запуск сідерів

Якщо ви хочете скористатися [сідерами бази даних](/docs/{{version}}/seeding), щоб наповнити базу під час функціонального тесту, викличте метод `seed`. За замовчуванням метод `seed` виконає `DatabaseSeeder`, який має запустити всі інші ваші сідери. Або ж ви можете передати методу `seed` ім'я конкретного класу сідера:

```php tab=Pest
<?php

use Database\Seeders\OrderStatusSeeder;
use Database\Seeders\TransactionStatusSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;

pest()->use(RefreshDatabase::class);

test('orders can be created', function () {
    // Run the DatabaseSeeder...
    $this->seed();

    // Run a specific seeder...
    $this->seed(OrderStatusSeeder::class);

    // ...

    // Run an array of specific seeders...
    $this->seed([
        OrderStatusSeeder::class,
        TransactionStatusSeeder::class,
        // ...
    ]);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Database\Seeders\OrderStatusSeeder;
use Database\Seeders\TransactionStatusSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    use RefreshDatabase;

    /**
     * Test creating a new order.
     */
    public function test_orders_can_be_created(): void
    {
        // Run the DatabaseSeeder...
        $this->seed();

        // Run a specific seeder...
        $this->seed(OrderStatusSeeder::class);

        // ...

        // Run an array of specific seeders...
        $this->seed([
            OrderStatusSeeder::class,
            TransactionStatusSeeder::class,
            // ...
        ]);
    }
}
```

Або ж ви можете вказати Laravel автоматично наповнювати базу перед кожним тестом, що використовує трейт `RefreshDatabase`. Для цього додайте атрибут `Seed` до вашого базового тестового класу:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\Attributes\Seed;
use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

#[Seed]
abstract class TestCase extends BaseTestCase
{
}
```

Коли присутній атрибут `Seed`, перед кожним тестом, що використовує трейт `RefreshDatabase`, буде запущено клас `Database\Seeders\DatabaseSeeder`. Проте ви можете вказати конкретний сідер, який слід виконати, застосувавши до вашого тестового класу атрибут `Seeder`:

```php
<?php

namespace Tests\Feature;

use Database\Seeders\OrderStatusSeeder;
use Illuminate\Foundation\Testing\Attributes\Seeder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

#[Seeder(OrderStatusSeeder::class)]
class OrderTest extends TestCase
{
    use RefreshDatabase;

    // ...
}
```

<a name="available-assertions"></a>
## Доступні твердження

Laravel надає кілька тверджень щодо бази даних для ваших функціональних тестів на [Pest](https://pestphp.com) чи [PHPUnit](https://phpunit.de). Кожне з них ми розглянемо нижче.

<a name="assert-database-count"></a>
#### assertDatabaseCount

Перевіряє, що таблиця в базі даних містить задану кількість записів:

```php
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-empty"></a>
#### assertDatabaseEmpty

Перевіряє, що таблиця в базі даних не містить записів:

```php
$this->assertDatabaseEmpty('users');
```

<a name="assert-database-has"></a>
#### assertDatabaseHas

Перевіряє, що таблиця в базі даних містить записи, які відповідають заданим умовам запиту ключ / значення:

```php
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

Перевіряє, що таблиця в базі даних не містить записів, які відповідають заданим умовам запиту ключ / значення:

```php
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### assertSoftDeleted

Метод `assertSoftDeleted` дозволяє перевірити, що задану модель Eloquent було «м'яко видалено»:

```php
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
#### assertNotSoftDeleted

Метод `assertNotSoftDeleted` дозволяє перевірити, що задану модель Eloquent не було «м'яко видалено»:

```php
$this->assertNotSoftDeleted($user);
```

<a name="assert-model-exists"></a>
#### assertModelExists

Перевіряє, що задана модель чи колекція моделей існує в базі даних:

```php
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
#### assertModelMissing

Перевіряє, що заданої моделі чи колекції моделей немає в базі даних:

```php
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a name="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

Метод `expectsDatabaseQueryCount` можна викликати на початку тесту, щоб указати загальну кількість запитів до бази даних, яку ви очікуєте під час прогону. Якщо фактична кількість виконаних запитів не збігається точно з очікуваною, тест провалиться:

```php
$this->expectsDatabaseQueryCount(5);

// Test...
```
