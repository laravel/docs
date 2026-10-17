---
title: "Testes de Banco de Dados"
---

- [Introdução](#introduction)
    - [Redefinindo o Banco de Dados Após Cada Teste](#resetting-the-database-after-each-test)
- [Factories de Model](#model-factories)
- [Executando Seeders](#running-seeders)
- [Asserções Disponíveis](#available-assertions)

<a id="introduction"></a>
## Introdução

O Laravel fornece uma variedade de ferramentas e asserções úteis para facilitar o teste de aplicações orientadas a banco de dados. Além disso, as factories de model e os seeders do Laravel tornam simples criar registros de banco de dados para teste usando os models Eloquent e os relacionamentos da sua aplicação. Discutiremos todos esses recursos poderosos na documentação a seguir.

<a id="resetting-the-database-after-each-test"></a>
### Redefinindo o Banco de Dados Após Cada Teste

Antes de avançarmos, vamos discutir como redefinir seu banco de dados após cada um dos seus testes, para que os dados de um teste anterior não interfiram nos testes seguintes. A trait `Illuminate\Foundation\Testing\RefreshDatabase` incluída no Laravel cuida disso para você. Basta usar a trait na sua classe de teste:

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

A trait `Illuminate\Foundation\Testing\RefreshDatabase` não migra o seu banco de dados se o schema já estiver atualizado. Em vez disso, ela apenas executa o teste dentro de uma transação de banco de dados. Portanto, quaisquer registros adicionados ao banco de dados por casos de teste que não usem esta trait ainda podem existir no banco de dados.

Se você quiser redefinir totalmente o banco de dados, pode usar as traits `Illuminate\Foundation\Testing\DatabaseMigrations` ou `Illuminate\Foundation\Testing\DatabaseTruncation`. No entanto, ambas as opções são significativamente mais lentas do que a trait `RefreshDatabase`.

<a id="model-factories"></a>
## Factories de Model

Ao testar, você pode precisar inserir alguns registros no seu banco de dados antes de executar seu teste. Em vez de especificar manualmente o valor de cada coluna ao criar esses dados de teste, o Laravel permite que você defina um conjunto de atributos padrão para cada um dos seus [models Eloquent](../eloquent/) usando [factories de model](../eloquent-factories/).

Para saber mais sobre como criar e utilizar factories de model para criar models, consulte a documentação completa sobre [factories de model](../eloquent-factories/). Depois de definir uma factory de model, você pode utilizá-la no seu teste para criar models:

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

<a id="running-seeders"></a>
## Executando Seeders

Se você quiser usar [seeders de banco de dados](../seeding/) para popular seu banco de dados durante um teste de funcionalidade, pode invocar o método `seed`. Por padrão, o método `seed` executará o `DatabaseSeeder`, que deve executar todos os seus outros seeders. Alternativamente, você pode passar o nome de uma classe de seeder específica para o método `seed`:

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

Alternativamente, você pode instruir o Laravel a popular automaticamente o banco de dados antes de cada teste que use a trait `RefreshDatabase`. Para isso, adicione o atributo `Seed` à sua classe base de teste:

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

Quando o atributo `Seed` estiver presente, o teste executará a classe `Database\Seeders\DatabaseSeeder` antes de cada teste que use a trait `RefreshDatabase`. No entanto, você pode especificar um seeder específico a ser executado usando o atributo `Seeder` na sua classe de teste:

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

<a id="available-assertions"></a>
## Asserções Disponíveis

O Laravel fornece várias asserções de banco de dados para seus testes de funcionalidade do [Pest](https://pestphp.com) ou do [PHPUnit](https://phpunit.de). Discutiremos cada uma dessas asserções a seguir.

<a id="assert-database-count"></a>
#### assertDatabaseCount

Verifica se uma tabela do banco de dados contém o número de registros informado:

```php
$this->assertDatabaseCount('users', 5);
```

<a id="assert-database-empty"></a>
#### assertDatabaseEmpty

Verifica se uma tabela do banco de dados não contém nenhum registro:

```php
$this->assertDatabaseEmpty('users');
```

<a id="assert-database-has"></a>
#### assertDatabaseHas

Verifica se uma tabela do banco de dados contém registros que correspondam às restrições de consulta chave / valor informadas:

```php
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a id="assert-database-missing"></a>
#### assertDatabaseMissing

Verifica se uma tabela do banco de dados não contém registros que correspondam às restrições de consulta chave / valor informadas:

```php
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a id="assert-deleted"></a>
#### assertSoftDeleted

O método `assertSoftDeleted` pode ser usado para verificar se um determinado model Eloquent foi "soft deleted":

```php
$this->assertSoftDeleted($user);
```

<a id="assert-not-deleted"></a>
#### assertNotSoftDeleted

O método `assertNotSoftDeleted` pode ser usado para verificar se um determinado model Eloquent não foi "soft deleted":

```php
$this->assertNotSoftDeleted($user);
```

<a id="assert-model-exists"></a>
#### assertModelExists

Verifica se um determinado model ou coleção de models existe no banco de dados:

```php
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a id="assert-model-missing"></a>
#### assertModelMissing

Verifica se um determinado model ou coleção de models não existe no banco de dados:

```php
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a id="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

O método `expectsDatabaseQueryCount` pode ser invocado no início do seu teste para especificar o número total de consultas ao banco de dados que você espera serem executadas durante o teste. Se o número real de consultas executadas não corresponder exatamente a essa expectativa, o teste falhará:

```php
$this->expectsDatabaseQueryCount(5);

// Test...
```
