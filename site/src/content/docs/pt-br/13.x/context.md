---
title: "Contexto"
---

- [Introdução](#introduction)
    - [Como Funciona](#how-it-works)
- [Capturando Contexto](#capturing-context)
    - [Pilhas](#stacks)
- [Recuperando Contexto](#retrieving-context)
    - [Verificando a Existência de Itens](#determining-item-existence)
- [Removendo Contexto](#removing-context)
- [Contexto Oculto](#hidden-context)
- [Eventos](#events)
    - [Desidratação](#dehydrating)
    - [Hidratação](#hydrated)

<a id="introduction"></a>
## Introdução

As capacidades de "contexto" do Laravel permitem que você capture, recupere e compartilhe informações ao longo das requisições, jobs e comandos executados dentro da sua aplicação. Essas informações capturadas também são incluídas nos logs gravados pela sua aplicação, dando a você uma visão mais profunda do histórico de execução ao redor de um log, que ocorreu antes de a entrada de log ser gravada, e permitindo rastrear fluxos de execução em todo um sistema distribuído.

<a id="how-it-works"></a>
### Como Funciona

A melhor forma de entender as capacidades de contexto do Laravel é vê-las em ação usando os recursos de logging integrados. Para começar, você pode [adicionar informações ao contexto](#capturing-context) usando a facade `Context`. Neste exemplo, usaremos um [middleware](../middleware/) para adicionar a URL da requisição e um ID de rastreamento único ao contexto em cada requisição recebida:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AddContext
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): Response
    {
        Context::add('url', $request->url());
        Context::add('trace_id', Str::uuid()->toString());

        return $next($request);
    }
}
```

As informações adicionadas ao contexto são automaticamente anexadas como metadados a quaisquer [entradas de log](../logging/) gravadas durante a requisição. Anexar o contexto como metadados permite diferenciar as informações passadas a entradas de log individuais das informações compartilhadas por meio de `Context`. Por exemplo, imagine que gravamos a seguinte entrada de log:

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

O log gravado conterá o `auth_id` passado à entrada de log, mas também conterá o `url` e o `trace_id` do contexto como metadados:

```text
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

As informações adicionadas ao contexto também ficam disponíveis para jobs despachados para a fila. Por exemplo, imagine que despachamos um job `ProcessPodcast` para a fila após adicionar algumas informações ao contexto:

```php
// In our middleware...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// In our controller...
ProcessPodcast::dispatch($podcast);
```

Quando o job é despachado, quaisquer informações atualmente armazenadas no contexto são capturadas e compartilhadas com o job. As informações capturadas são então reidratadas no contexto atual enquanto o job está sendo executado. Assim, se o método `handle` do nosso job gravar um log:

```php
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    // ...

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        Log::info('Processing podcast.', [
            'podcast_id' => $this->podcast->id,
        ]);

        // ...
    }
}
```

A entrada de log resultante conterá as informações que foram adicionadas ao contexto durante a requisição que originalmente despachou o job:

```text
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

Embora tenhamos focado nos recursos de logging integrados ao contexto do Laravel, a documentação a seguir ilustrará como o contexto permite compartilhar informações através da fronteira entre requisição HTTP e job enfileirado, e até como adicionar [dados de contexto ocultos](#hidden-context) que não são gravados nas entradas de log.

<a id="capturing-context"></a>
## Capturando Contexto

Você pode armazenar informações no contexto atual usando o método `add` da facade `Context`:

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

Para adicionar múltiplos itens de uma só vez, você pode passar um array associativo ao método `add`:

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

O método `add` sobrescreverá qualquer valor existente que compartilhe a mesma chave. Se você quiser adicionar informações ao contexto somente quando a chave ainda não existir, pode usar o método `addIf`:

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

O contexto também oferece métodos práticos para incrementar ou decrementar uma determinada chave. Ambos os métodos aceitam pelo menos um argumento: a chave a ser rastreada. Um segundo argumento pode ser informado para especificar a quantidade pela qual a chave deve ser incrementada ou decrementada:

```php
Context::increment('records_added');
Context::increment('records_added', 5);

Context::decrement('records_added');
Context::decrement('records_added', 5);
```

<a id="conditional-context"></a>
#### Contexto Condicional

O método `when` pode ser usado para adicionar dados ao contexto com base em uma condição informada. A primeira closure fornecida ao método `when` será invocada se a condição informada for avaliada como `true`, enquanto a segunda closure será invocada se a condição for avaliada como `false`:

```php
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Context;

Context::when(
    Auth::user()->isAdmin(),
    fn ($context) => $context->add('permissions', Auth::user()->permissions),
    fn ($context) => $context->add('permissions', []),
);
```

<a id="scoped-context"></a>
#### Contexto com Escopo

O método `scope` oferece uma forma de modificar temporariamente o contexto durante a execução de um determinado callback e restaurar o contexto ao seu estado original quando o callback terminar de executar. Além disso, você pode passar dados extras que devem ser mesclados ao contexto (como segundo e terceiro argumentos) enquanto a closure é executada.

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\Log;

Context::add('trace_id', 'abc-999');
Context::addHidden('user_id', 123);

Context::scope(
    function () {
        Context::add('action', 'adding_friend');

        $userId = Context::getHidden('user_id');

        Log::debug("Adding user [{$userId}] to friends list.");
        // Adding user [987] to friends list.  {"trace_id":"abc-999","user_name":"taylor_otwell","action":"adding_friend"}
    },
    data: ['user_name' => 'taylor_otwell'],
    hidden: ['user_id' => 987],
);

Context::all();
// [
//     'trace_id' => 'abc-999',
// ]

Context::allHidden();
// [
//     'user_id' => 123,
// ]
```

> **Aviso:**
> Se um objeto dentro do contexto for modificado dentro da closure com escopo, essa mutação será refletida fora do escopo.

<a id="stacks"></a>
### Pilhas

O contexto oferece a capacidade de criar "pilhas", que são listas de dados armazenadas na ordem em que foram adicionadas. Você pode adicionar informações a uma pilha invocando o método `push`:

```php
use Illuminate\Support\Facades\Context;

Context::push('breadcrumbs', 'first_value');

Context::push('breadcrumbs', 'second_value', 'third_value');

Context::get('breadcrumbs');
// [
//     'first_value',
//     'second_value',
//     'third_value',
// ]
```

Pilhas podem ser úteis para capturar informações históricas sobre uma requisição, como eventos que estão acontecendo ao longo da sua aplicação. Por exemplo, você poderia criar um listener de evento que adiciona à pilha toda vez que uma query é executada, capturando o SQL da query e sua duração como uma tupla:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

// In AppServiceProvider.php...
DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

Você pode verificar se um valor está em uma pilha usando os métodos `stackContains` e `hiddenStackContains`:

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

Os métodos `stackContains` e `hiddenStackContains` também aceitam uma closure como segundo argumento, permitindo mais controle sobre a operação de comparação de valores:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});
```

<a id="retrieving-context"></a>
## Recuperando Contexto

Você pode recuperar informações do contexto usando o método `get` da facade `Context`:

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

Os métodos `only` e `except` podem ser usados para recuperar um subconjunto das informações do contexto:

```php
$data = Context::only(['first_key', 'second_key']);

$data = Context::except(['first_key']);
```

O método `pull` pode ser usado para recuperar informações do contexto e removê-las imediatamente do contexto:

```php
$value = Context::pull('key');
```

Se dados de contexto estiverem armazenados em uma [pilha](#stacks), você pode remover itens da pilha usando o método `pop`:

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs');
// second_value

Context::get('breadcrumbs');
// ['first_value']
```

Os métodos `remember` e `rememberHidden` podem ser usados para recuperar informações do contexto, definindo o valor do contexto como o valor retornado pela closure informada caso a informação solicitada não exista:

```php
$permissions = Context::remember(
    'user-permissions',
    fn () => $user->permissions,
);
```

Se você quiser recuperar todas as informações armazenadas no contexto, pode invocar o método `all`:

```php
$data = Context::all();
```

<a id="determining-item-existence"></a>
### Verificando a Existência de Itens

Você pode usar os métodos `has` e `missing` para verificar se o contexto possui algum valor armazenado para a chave informada:

```php
use Illuminate\Support\Facades\Context;

if (Context::has('key')) {
    // ...
}

if (Context::missing('key')) {
    // ...
}
```

O método `has` retornará `true` independentemente do valor armazenado. Assim, por exemplo, uma chave com valor `null` será considerada presente:

```php
Context::add('key', null);

Context::has('key');
// true
```

<a id="removing-context"></a>
## Removendo Contexto

O método `forget` pode ser usado para remover uma chave e seu valor do contexto atual:

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

Você pode remover várias chaves de uma só vez informando um array ao método `forget`:

```php
Context::forget(['first_key', 'second_key']);
```

<a id="hidden-context"></a>
## Contexto Oculto

O contexto oferece a capacidade de armazenar dados "ocultos". Essas informações ocultas não são anexadas aos logs e não são acessíveis pelos métodos de recuperação de dados documentados acima. O contexto fornece um conjunto diferente de métodos para interagir com as informações de contexto ocultas:

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

Os métodos "ocultos" espelham a funcionalidade dos métodos não ocultos documentados acima:

```php
Context::addHidden(/* ... */);
Context::addHiddenIf(/* ... */);
Context::pushHidden(/* ... */);
Context::getHidden(/* ... */);
Context::pullHidden(/* ... */);
Context::popHidden(/* ... */);
Context::onlyHidden(/* ... */);
Context::exceptHidden(/* ... */);
Context::allHidden(/* ... */);
Context::hasHidden(/* ... */);
Context::missingHidden(/* ... */);
Context::forgetHidden(/* ... */);
```

<a id="events"></a>
## Eventos

O Context dispara dois eventos que permitem interceptar os processos de hidratação e desidratação do contexto.

Para ilustrar como esses eventos podem ser usados, imagine que, em um middleware da sua aplicação, você define o valor de configuração `app.locale` com base no header `Accept-Language` da requisição HTTP recebida. Os eventos do Context permitem capturar esse valor durante a requisição e restaurá-lo na fila, garantindo que as notificações enviadas pela fila tenham o valor correto de `app.locale`. Podemos usar os eventos do context e os dados [ocultos](#hidden-context) para atingir isso, o que será ilustrado na documentação a seguir.

<a id="dehydrating"></a>
### Desidratação

Sempre que um job é despachado para a fila, os dados do contexto são "desidratados" e capturados junto ao payload do job. O método `Context::dehydrating` permite registrar uma closure que será invocada durante o processo de desidratação. Dentro dessa closure, você pode fazer alterações nos dados que serão compartilhados com o job enfileirado.

Normalmente, você deve registrar os callbacks `dehydrating` dentro do método `boot` da classe `AppServiceProvider` da sua aplicação:

```php
use Illuminate\Log\Context\Repository;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Facades\Context;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Context::dehydrating(function (Repository $context) {
        $context->addHidden('locale', Config::get('app.locale'));
    });
}
```

> **Nota:**
> Você não deve usar a facade `Context` dentro do callback `dehydrating`, pois isso alterará o contexto do processo atual. Certifique-se de fazer alterações apenas no repositório passado ao callback.

<a id="hydrated"></a>
### Hidratação

Sempre que um job enfileirado começa a ser executado na fila, qualquer contexto que foi compartilhado com o job é "hidratado" de volta ao contexto atual. O método `Context::hydrated` permite registrar uma closure que será invocada durante o processo de hidratação.

Normalmente, você deve registrar os callbacks `hydrated` dentro do método `boot` da classe `AppServiceProvider` da sua aplicação:

```php
use Illuminate\Log\Context\Repository;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Facades\Context;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Context::hydrated(function (Repository $context) {
        if ($context->hasHidden('locale')) {
            Config::set('app.locale', $context->getHidden('locale'));
        }
    });
}
```

> **Nota:**
> Você não deve usar a facade `Context` dentro do callback `hydrated`; em vez disso, certifique-se de fazer alterações apenas no repositório passado ao callback.
