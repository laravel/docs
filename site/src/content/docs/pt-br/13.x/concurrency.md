---
title: "Concorrência"
---

- [Introdução](#introduction)
- [Executando Tarefas Concorrentes](#running-concurrent-tasks)
    - [Resultados Nomeados](#named-results)
    - [Timeouts de Tarefas](#task-timeouts)
- [Adiando Tarefas Concorrentes](#deferring-concurrent-tasks)

<a id="introduction"></a>
## Introdução

Às vezes, você pode precisar executar várias tarefas lentas que não dependem umas das outras. Em muitos casos, melhorias significativas de desempenho podem ser obtidas executando as tarefas de forma concorrente. A facade `Concurrency` do Laravel fornece uma API simples e conveniente para executar closures de forma concorrente.

<a id="how-it-works"></a>
#### Como Funciona

O Laravel alcança concorrência serializando os closures fornecidos e despachando-os para um comando Artisan oculto da CLI, que desserializa os closures e os invoca dentro de seu próprio processo PHP. Depois que o closure é invocado, o valor resultante é serializado de volta para o processo pai.

A facade `Concurrency` suporta três drivers: `process` (o padrão), `fork` e `sync`.

O driver `fork` oferece desempenho melhorado em comparação com o driver padrão `process`, mas só pode ser usado no contexto CLI do PHP, pois o PHP não suporta fork durante requisições web. Antes de usar o driver `fork`, você precisa instalar o pacote `spatie/fork`:

```shell
composer require spatie/fork
```

O driver `sync` é útil principalmente durante os testes, quando você deseja desabilitar toda a concorrência e simplesmente executar os closures fornecidos em sequência dentro do processo pai.

<a id="running-concurrent-tasks"></a>
## Executando Tarefas Concorrentes

Para executar tarefas concorrentes, você pode invocar o método `run` da facade `Concurrency`. O método `run` aceita um array de closures que devem ser executados simultaneamente em processos PHP filhos:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
]);
```

Para usar um driver específico, você pode usar o método `driver`:

```php
$results = Concurrency::driver('fork')->run(...);
```

Ou, para alterar o driver de concorrência padrão, você deve publicar o arquivo de configuração `concurrency` por meio do comando Artisan `config:publish` e atualizar a opção `default` dentro do arquivo:

```shell
php artisan config:publish concurrency
```

<a id="named-results"></a>
### Resultados Nomeados

Se você quiser acessar os resultados das tarefas concorrentes pelo nome em vez da posição, pode fornecer um array associativo de closures. Cada resultado será retornado usando a mesma chave do seu closure correspondente:

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

<a id="task-timeouts"></a>
### Timeouts de Tarefas

Ao usar o driver `process` (o padrão), você pode especificar o número máximo de segundos que uma tarefa concorrente pode executar antes de ser encerrada, fornecendo um timeout ao método `run`:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
], timeout: 30);
```

Você também pode fornecer uma instância `CarbonInterval` se preferir uma definição de timeout mais expressiva:

```php
use Illuminate\Support\Facades\Concurrency;

use function Illuminate\Support\seconds;

Concurrency::run([...], timeout: seconds(30));
```

<a id="deferring-concurrent-tasks"></a>
## Adiando Tarefas Concorrentes

Se você quiser executar um array de closures de forma concorrente, mas não estiver interessado nos resultados retornados por esses closures, considere usar o método `defer`. Quando o método `defer` é invocado, os closures fornecidos não são executados imediatamente. Em vez disso, o Laravel os executará de forma concorrente após a resposta HTTP ter sido enviada ao usuário:

```php
use App\Services\Metrics;
use Illuminate\Support\Facades\Concurrency;

Concurrency::defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);
```
