---
title: "Mocks"
---

- [Introdução](#introduction)
- [Mockando Objetos](#mocking-objects)
- [Mockando Facades](#mocking-facades)
    - [Spies de Facades](#facade-spies)
- [Interagindo com o Tempo](#interacting-with-time)

<a id="introduction"></a>
## Introdução

Ao testar aplicações Laravel, você pode desejar "mockar" certos aspectos da sua aplicação para que eles não sejam realmente executados durante um determinado teste. Por exemplo, ao testar um controller que dispara um evento, você pode desejar mockar os listeners do evento para que eles não sejam realmente executados durante o teste. Isso permite testar apenas a resposta HTTP do controller, sem se preocupar com a execução dos listeners, já que eles podem ser testados em seu próprio caso de teste.

O Laravel fornece métodos auxiliares para mockar eventos, jobs e outras facades prontos para uso. Esses auxiliares fornecem, principalmente, uma camada de conveniência sobre o Mockery, para que você não precise fazer chamadas complicadas de métodos do Mockery manualmente.

<a id="mocking-objects"></a>
## Mockando Objetos

Ao mockar um objeto que será injetado na sua aplicação através do [service container](../container/) do Laravel, você precisará vincular sua instância mockada ao container como um binding do tipo `instance`. Isso instruirá o container a usar sua instância mockada do objeto em vez de construir o objeto por conta própria:

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

Para tornar isso mais conveniente, você pode usar o método `mock` fornecido pela classe base de teste do Laravel. Por exemplo, o exemplo a seguir é equivalente ao exemplo acima:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});
```

Você pode usar o método `partialMock` quando precisar mockar apenas alguns métodos de um objeto. Os métodos que não forem mockados serão executados normalmente quando chamados:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});
```

Da mesma forma, se você quiser fazer um [spy](http://docs.mockery.io/en/latest/reference/spies.html) em um objeto, a classe base de teste do Laravel oferece um método `spy` como um wrapper conveniente em torno do método `Mockery::spy`. Spies são semelhantes a mocks; no entanto, spies registram qualquer interação entre o spy e o código testado, permitindo que você faça asserções após a execução do código:

```php
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a id="mocking-facades"></a>
## Mockando Facades

Diferentemente das chamadas tradicionais a métodos estáticos, [facades](../facades/) (incluindo [facades em tempo real](../facades/#real-time-facades)) podem ser mockadas. Isso oferece uma grande vantagem em relação aos métodos estáticos tradicionais e concede a mesma testabilidade que você teria usando injeção de dependência tradicional. Ao testar, você frequentemente desejará mockar uma chamada a uma facade do Laravel que ocorre em um dos seus controllers. Por exemplo, considere a seguinte action de controller:

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

Podemos mockar a chamada à facade `Cache` usando o método `expects`, que retornará uma instância de um mock do [Mockery](https://github.com/padraic/mockery). Como as facades são de fato resolvidas e gerenciadas pelo [service container](../container/) do Laravel, elas têm muito mais testabilidade do que uma classe estática típica. Por exemplo, vamos mockar nossa chamada ao método `get` da facade `Cache`:

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

> **Aviso:**
> Você não deve mockar a facade `Request`. Em vez disso, passe a entrada desejada para os [métodos de teste HTTP](../http-tests/), como `get` e `post`, ao executar seu teste. Da mesma forma, em vez de mockar a facade `Config`, chame o método `Config::set` em seus testes.

<a id="facade-spies"></a>
### Spies de Facades

Se você quiser fazer um [spy](http://docs.mockery.io/en/latest/reference/spies.html) em uma facade, pode chamar o método `spy` na facade correspondente. Spies são semelhantes a mocks; no entanto, spies registram qualquer interação entre o spy e o código testado, permitindo que você faça asserções após a execução do código:

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

<a id="interacting-with-time"></a>
## Interagindo com o Tempo

Ao testar, você pode ocasionalmente precisar modificar o horário retornado por auxiliares como `now` ou `Illuminate\Support\Carbon::now()`. Felizmente, a classe base de testes de funcionalidade do Laravel inclui auxiliares que permitem manipular o horário atual:

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

Você também pode fornecer uma closure aos diversos métodos de viagem no tempo. A closure será invocada com o tempo congelado no horário especificado. Após a execução da closure, o tempo volta ao normal:

```php
$this->travel(5)->days(function () {
    // Test something five days into the future...
});

$this->travelTo(now()->minus(days: 10), function () {
    // Test something during a given moment...
});
```

O método `freezeTime` pode ser usado para congelar o horário atual. De forma semelhante, o método `freezeSecond` congelará o horário atual, mas no início do segundo atual:

```php
use Illuminate\Support\Carbon;

// Freeze time and resume normal time after executing closure...
$this->freezeTime(function (Carbon $time) {
    // ...
});

// Freeze time at the current second and resume normal time after executing closure...
$this->freezeSecond(function (Carbon $time) {
    // ...
});
```

Como você esperaria, todos os métodos discutidos acima são úteis principalmente para testar comportamentos da aplicação sensíveis ao tempo, como bloquear posts inativos em um fórum de discussão:

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
