---
title: "Events"
---

- [Introdução](#introduction)
- [Gerando Events e Listeners](#generating-events-and-listeners)
- [Registrando Events e Listeners](#registering-events-and-listeners)
    - [Descoberta de Events](#event-discovery)
    - [Registrando Events Manualmente](#manually-registering-events)
    - [Listeners com Closures](#closure-listeners)
- [Definindo Events](#defining-events)
- [Definindo Listeners](#defining-listeners)
- [Event Listeners Enfileirados](#queued-event-listeners)
    - [Interagindo Manualmente com a Fila](#manually-interacting-with-the-queue)
    - [Event Listeners Enfileirados e Transações de Banco de Dados](#queued-event-listeners-and-database-transactions)
    - [Middleware de Listeners Enfileirados](#queued-listener-middleware)
    - [Listeners Enfileirados Criptografados](#encrypted-queued-listeners)
    - [Event Listeners Únicos](#unique-event-listeners)
        - [Mantendo Listeners Únicos Até o Início do Processamento](#keeping-listeners-unique-until-processing-begins)
        - [Bloqueios de Listeners Únicos](#unique-listener-locks)
    - [Event Listeners com Debounce](#debounced-event-listeners)
    - [Lidando com Jobs que Falharam](#handling-failed-jobs)
- [Despachando Events](#dispatching-events)
    - [Despachando Events Após Transações de Banco de Dados](#dispatching-events-after-database-transactions)
    - [Adiando Events](#deferring-events)
- [Event Subscribers](#event-subscribers)
    - [Escrevendo Event Subscribers](#writing-event-subscribers)
    - [Registrando Event Subscribers](#registering-event-subscribers)
- [Testes](#testing)
    - [Fazendo Fake de um Subconjunto de Events](#faking-a-subset-of-events)
    - [Fakes de Event com Escopo](#scoped-event-fakes)

<a id="introduction"></a>
## Introdução

Os events do Laravel fornecem uma implementação simples do padrão observer, permitindo que você se inscreva e escute vários events que ocorrem dentro da sua aplicação. As classes de event normalmente ficam armazenadas no diretório `app/Events`, enquanto seus listeners ficam em `app/Listeners`. Não se preocupe se você não vir esses diretórios na sua aplicação, pois eles serão criados para você conforme você gera events e listeners usando os comandos do console Artisan.

Events servem como uma ótima maneira de desacoplar vários aspectos da sua aplicação, já que um único event pode ter múltiplos listeners que não dependem uns dos outros. Por exemplo, você pode desejar enviar uma notificação do Slack ao seu usuário cada vez que um pedido for enviado. Em vez de acoplar seu código de processamento de pedidos ao seu código de notificação do Slack, você pode disparar um event `App\Events\OrderShipped` que um listener pode receber e usar para despachar uma notificação do Slack.

<a id="generating-events-and-listeners"></a>
## Gerando Events e Listeners

Para gerar events e listeners rapidamente, você pode usar os comandos Artisan `make:event` e `make:listener`:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

Por conveniência, você também pode invocar os comandos Artisan `make:event` e `make:listener` sem argumentos adicionais. Quando fizer isso, o Laravel irá automaticamente solicitar o nome da classe e, ao criar um listener, o event que ele deve escutar:

```shell
php artisan make:event

php artisan make:listener
```

<a id="registering-events-and-listeners"></a>
## Registrando Events e Listeners

<a id="event-discovery"></a>
### Descoberta de Events

Por padrão, o Laravel irá encontrar e registrar automaticamente seus event listeners ao escanear o diretório `Listeners` da sua aplicação. Quando o Laravel encontra qualquer método de uma classe listener que começa com `handle` ou `__invoke`, o Laravel registrará esses métodos como event listeners para o event que está indicado via type-hint na assinatura do método:

```php
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * Handle the event.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }
}
```

Você pode escutar múltiplos events usando os union types do PHP:

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

Se você planeja armazenar seus listeners em um diretório diferente ou dentro de múltiplos diretórios, você pode instruir o Laravel a escanear esses diretórios usando o método `withEvents` no arquivo `bootstrap/app.php` da sua aplicação:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

Você pode escanear listeners em múltiplos diretórios similares usando o caractere `*` como curinga:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

O comando `event:list` pode ser usado para listar todos os listeners registrados na sua aplicação:

```shell
php artisan event:list
```

<a id="event-discovery-in-production"></a>
#### Descoberta de Events em Produção

Para dar um ganho de velocidade à sua aplicação, você deve fazer cache de um manifesto de todos os listeners da sua aplicação usando os comandos Artisan `optimize` ou `event:cache`. Normalmente, esse comando deve ser executado como parte do [processo de deploy](../deployment/#optimization) da sua aplicação. Esse manifesto será usado pelo framework para acelerar o processo de registro de events. O comando `event:clear` pode ser usado para destruir o cache de events.

<a id="dynamic-event-discovery"></a>
#### Descoberta Dinâmica de Events

Para controlar dinamicamente se um determinado listener é descoberto, você pode implementar a interface `ShouldBeDiscovered` na classe listener e definir um método `shouldBeDiscovered` que retorna um valor booleano. Se o método retornar `false`, o listener não será registrado durante a descoberta de events:

```php
use Illuminate\Contracts\Events\ShouldBeDiscovered;

class SendPodcastNotification implements ShouldBeDiscovered
{
    /**
     * Handle the event.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }

    /**
     * Determine if the listener should be discovered.
     */
    public static function shouldBeDiscovered(): bool
    {
        return app()->environment('production');
    }
}
```

<a id="manually-registering-events"></a>
### Registrando Events Manualmente

Usando a facade `Event`, você pode registrar manualmente events e seus listeners correspondentes dentro do método `boot` do `AppServiceProvider` da sua aplicação:

```php
use App\Domain\Orders\Events\PodcastProcessed;
use App\Domain\Orders\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(
        PodcastProcessed::class,
        SendPodcastNotification::class,
    );
}
```

O comando `event:list` pode ser usado para listar todos os listeners registrados na sua aplicação:

```shell
php artisan event:list
```

<a id="closure-listeners"></a>
### Listeners com Closures

Normalmente, listeners são definidos como classes; no entanto, você também pode registrar manualmente event listeners baseados em closures no método `boot` do `AppServiceProvider` da sua aplicação:

```php
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (PodcastProcessed $event) {
        // ...
    });
}
```

<a id="queueable-anonymous-event-listeners"></a>
#### Event Listeners Anônimos Enfileiráveis

Ao registrar event listeners baseados em closures, você pode envolver a closure do listener na função `Illuminate\Events\queueable` para instruir o Laravel a executar o listener usando a [fila](../queues/):

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    }));
}
```

Assim como jobs enfileirados, você pode usar os métodos `onConnection`, `onQueue` e `delay` para personalizar a execução do listener enfileirado:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```

Se você gostaria de lidar com falhas de listeners anônimos enfileirados, você pode fornecer uma closure ao método `catch` ao definir o listener `queueable`. Essa closure receberá a instância do event e a instância `Throwable` que causou a falha do listener:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // The queued listener failed...
}));
```

<a id="wildcard-event-listeners"></a>
#### Event Listeners com Curinga

Você também pode registrar listeners usando o caractere `*` como parâmetro curinga, permitindo capturar múltiplos events no mesmo listener. Listeners com curinga recebem o nome do event como seu primeiro argumento e todo o array de dados do event como seu segundo argumento:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a id="defining-events"></a>
## Definindo Events

Uma classe de event é essencialmente um contêiner de dados que armazena as informações relacionadas ao event. Por exemplo, vamos supor que um event `App\Events\OrderShipped` receba um objeto do [Eloquent ORM](../eloquent/):

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderShipped
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    /**
     * Create a new event instance.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

Como você pode ver, essa classe de event não contém lógica. É um contêiner para a instância de `App\Models\Order` que foi comprada. A trait `SerializesModels` usada pelo event irá serializar graciosamente quaisquer models do Eloquent se o objeto do event for serializado usando a função `serialize` do PHP, como quando se utiliza [listeners enfileirados](#queued-event-listeners).

<a id="defining-listeners"></a>
## Definindo Listeners

A seguir, vamos dar uma olhada no listener para o nosso event de exemplo. Event listeners recebem instâncias de event no seu método `handle`. O comando Artisan `make:listener`, quando invocado com a opção `--event`, irá automaticamente importar a classe de event apropriada e aplicar o type-hint do event no método `handle`. Dentro do método `handle`, você pode executar quaisquer ações necessárias para responder ao event:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * Create the event listener.
     */
    public function __construct() {}

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Access the order using $event->order...
    }
}
```

> **Note:**
> Seus event listeners também podem aplicar type-hint em quaisquer dependências de que precisem em seus construtores. Todos os event listeners são resolvidos através do [service container](../container/) do Laravel, então as dependências serão injetadas automaticamente.

<a id="stopping-the-propagation-of-an-event"></a>
#### Interrompendo a Propagação de um Event

Às vezes, você pode desejar interromper a propagação de um event para outros listeners. Você pode fazer isso retornando `false` do método `handle` do seu listener.

<a id="queued-event-listeners"></a>
## Event Listeners Enfileirados

Enfileirar listeners pode ser benéfico se o seu listener for executar uma tarefa lenta, como enviar um e-mail ou fazer uma requisição HTTP. Antes de usar listeners enfileirados, certifique-se de [configurar sua fila](../queues/) e iniciar um queue worker no seu servidor ou ambiente de desenvolvimento local.

Para especificar que um listener deve ser enfileirado, adicione a interface `ShouldQueue` à classe listener. Listeners gerados pelos comandos Artisan `make:listener` já têm essa interface importada no namespace atual, então você pode usá-la imediatamente:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

É isso! Agora, quando um event tratado por esse listener for despachado, o listener será automaticamente enfileirado pelo event dispatcher usando o [sistema de filas](../queues/) do Laravel. Se nenhuma exceção for lançada quando o listener for executado pela fila, o job enfileirado será automaticamente excluído após terminar o processamento.

<a id="customizing-the-queue-connection-queue-name"></a>
#### Personalizando a Conexão, o Nome e o Delay da Fila

Se você gostaria de personalizar a conexão de fila, o nome da fila ou o tempo de delay da fila de um event listener, você pode usar os atributos `Connection`, `Queue` e `Delay` na sua classe listener:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Connection;
use Illuminate\Queue\Attributes\Delay;
use Illuminate\Queue\Attributes\Queue;

#[Connection('sqs')]
#[Queue('listeners')]
#[Delay(60)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```
Se você gostaria de definir a conexão de fila, o nome da fila ou o delay do listener em tempo de execução, você pode definir os métodos `viaConnection`, `viaQueue` ou `withDelay` no listener:

```php
/**
 * Get the name of the listener's queue connection.
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * Get the name of the listener's queue.
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * Get the number of seconds before the job should be processed.
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

Se você gostaria que todos os seus listeners enfileirados usassem a mesma fila sem personalizar cada classe listener, você pode [rotear o contrato `ShouldQueue` para uma fila](../queues/#queue-routing).

<a id="conditionally-queueing-listeners"></a>
#### Enfileirando Listeners Condicionalmente

Às vezes, você pode precisar determinar se um listener deve ser enfileirado com base em alguns dados que só estão disponíveis em tempo de execução. Para fazer isso, um método `shouldQueue` pode ser adicionado a um listener para determinar se o listener deve ser enfileirado. Se o método `shouldQueue` retornar `false`, o listener não será enfileirado:

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * Reward a gift card to the customer.
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * Determine whether the listener should be queued.
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a id="manually-interacting-with-the-queue"></a>
### Interagindo Manualmente com a Fila

Se você precisar acessar manualmente os métodos `delete` e `release` do job de fila subjacente do listener, você pode fazer isso usando a trait `Illuminate\Queue\InteractsWithQueue`. Essa trait é importada por padrão nos listeners gerados e fornece acesso a esses métodos:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        if ($condition) {
            $this->release(30);
        }
    }
}
```

<a id="queued-event-listeners-and-database-transactions"></a>
### Event Listeners Enfileirados e Transações de Banco de Dados

Quando listeners enfileirados são despachados dentro de transações de banco de dados, eles podem ser processados pela fila antes que a transação de banco de dados tenha sido commitada. Quando isso acontece, quaisquer atualizações que você tenha feito em models ou registros de banco de dados durante a transação podem ainda não estar refletidas no banco de dados. Além disso, quaisquer models ou registros de banco de dados criados dentro da transação podem não existir no banco de dados. Se o seu listener depende desses models, erros inesperados podem ocorrer quando o job que despacha o listener enfileirado é processado.

Se a opção de configuração `after_commit` da conexão de fila estiver definida como `false`, você ainda pode indicar que um determinado listener enfileirado deve ser despachado após todas as transações de banco de dados abertas terem sido commitadas, implementando a interface `ShouldQueueAfterCommit` na classe listener:

```php
<?php

namespace App\Listeners;

use Illuminate\Contracts\Queue\ShouldQueueAfterCommit;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueueAfterCommit
{
    use InteractsWithQueue;
}
```

> **Note:**
> Para saber mais sobre como contornar esses problemas, revise a documentação sobre [jobs enfileirados e transações de banco de dados](../queues/#jobs-and-database-transactions).

<a id="queued-listener-middleware"></a>
### Middleware de Listeners Enfileirados

Listeners enfileirados também podem utilizar [job middleware](../queues/#job-middleware). Job middleware permitem que você envolva lógica personalizada em torno da execução de listeners enfileirados, reduzindo o boilerplate nos próprios listeners. Após criar um job middleware, ele pode ser anexado a um listener retornando-o do método `middleware` do listener:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use App\Jobs\Middleware\RateLimited;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }

    /**
     * Get the middleware the listener should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(OrderShipped $event): array
    {
        return [new RateLimited];
    }
}
```

<a id="encrypted-queued-listeners"></a>
#### Listeners Enfileirados Criptografados

O Laravel permite que você garanta a privacidade e a integridade dos dados de um listener enfileirado via [criptografia](../encryption/). Para começar, basta adicionar a interface `ShouldBeEncrypted` à classe listener. Uma vez que essa interface tenha sido adicionada à classe, o Laravel irá criptografar automaticamente o seu listener antes de enviá-lo para uma fila:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue, ShouldBeEncrypted
{
    // ...
}
```

<a id="unique-event-listeners"></a>
### Event Listeners Únicos

> **Warning:**
> Listeners únicos exigem um cache driver que suporte [locks](../cache/#atomic-locks). Atualmente, os cache drivers `memcached`, `redis`, `dynamodb`, `database`, `file` e `array` suportam bloqueios atômicos.

Às vezes, você pode querer garantir que apenas uma instância de um listener específico esteja na fila em qualquer momento. Você pode fazer isso implementando a interface `ShouldBeUnique` na sua classe listener:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    public function __invoke(LicenseSaved $event): void
    {
        // ...
    }
}
```

No exemplo acima, o listener `AcquireProductKey` é único. Assim, o listener não será enfileirado se outra instância do listener já estiver na fila e não tiver terminado o processamento. Isso garante que apenas uma chave de produto seja adquirida para cada licença, mesmo que a licença seja salva várias vezes em rápida sucessão.

Em certos casos, você pode querer definir uma "chave" específica que torne o listener único ou pode querer especificar um timeout após o qual o listener deixa de permanecer único. Para fazer isso, você pode definir as propriedades ou métodos `uniqueId` e `uniqueFor` na sua classe listener. Os métodos recebem a instância do event, permitindo que você use os dados do event para construir o valor de retorno:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    /**
     * The number of seconds after which the listener's unique lock will be released.
     *
     * @var int
     */
    public $uniqueFor = 3600;

    public function __invoke(LicenseSaved $event): void
    {
        // ...
    }

    /**
     * Get the unique ID for the listener.
     */
    public function uniqueId(LicenseSaved $event): string
    {
        return 'listener:'.$event->license->id;
    }
}
```

No exemplo acima, o listener `AcquireProductKey` é único por ID de licença. Assim, quaisquer novos despachos do listener para a mesma licença serão ignorados até que o listener existente tenha concluído o processamento. Isso evita que chaves de produto duplicadas sejam adquiridas para a mesma licença. Além disso, se o listener existente não for processado dentro de uma hora, o bloqueio único será liberado e outro listener com a mesma chave única poderá ser enfileirado.

> **Warning:**
> Se a sua aplicação despacha events de múltiplos servidores web ou contêineres, você deve garantir que todos os seus servidores estejam se comunicando com o mesmo servidor de cache central para que o Laravel possa determinar com precisão se um listener é único.

<a id="keeping-listeners-unique-until-processing-begins"></a>
#### Mantendo Listeners Únicos Até o Início do Processamento

Por padrão, listeners únicos são "destravados" após um listener concluir o processamento ou falhar todas as suas tentativas de retry. No entanto, pode haver situações em que você gostaria que seu listener fosse destravado imediatamente antes de ser processado. Para fazer isso, seu listener deve implementar o contrato `ShouldBeUniqueUntilProcessing` em vez do contrato `ShouldBeUnique`:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;
use Illuminate\Contracts\Queue\ShouldQueue;

class AcquireProductKey implements ShouldQueue, ShouldBeUniqueUntilProcessing
{
    // ...
}
```

<a id="unique-listener-locks"></a>
#### Bloqueios de Listeners Únicos

Nos bastidores, quando um listener `ShouldBeUnique` é despachado, o Laravel tenta adquirir um [lock](../cache/#atomic-locks) com a chave `uniqueId`. Se o lock já estiver em uso, o listener não é despachado. Esse lock é liberado quando o listener conclui o processamento ou falha todas as suas tentativas de retry. Por padrão, o Laravel usará o cache driver padrão para obter esse lock. No entanto, se você desejar usar outro driver para adquirir o lock, você pode definir um método `uniqueVia` que retorna o cache driver que deve ser usado:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * Get the cache driver for the unique listener lock.
     */
    public function uniqueVia(LicenseSaved $event): Repository
    {
        return Cache::driver('redis');
    }
}
```

> **Note:**
> Se você só precisa limitar o processamento concorrente de um listener, use o job middleware [WithoutOverlapping](../queues/#preventing-job-overlaps).

<a id="debounced-event-listeners"></a>
### Event Listeners com Debounce

Às vezes, você pode querer tratar apenas a instância mais recente de um event despachado repetidamente dentro de um curto período. Você pode fazer isso adicionando o atributo `DebounceFor` a um listener enfileirado:

```php
<?php

namespace App\Listeners;

use App\Events\ProductUpdated;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\DebounceFor;

#[DebounceFor(30)]
class UpdateProductSearchIndex implements ShouldQueue
{
    /**
     * Handle the event.
     */
    public function handle(ProductUpdated $event): void
    {
        // Update the product's search index...
    }

    /**
     * Get the debounce ID for the listener.
     */
    public function debounceId(ProductUpdated $event): string
    {
        return (string) $event->product->getKey();
    }
}
```

No exemplo acima, despachar repetidamente events `ProductUpdated` para o mesmo produto dentro de `30` segundos aplicará debounce ao listener de forma que apenas o event mais recente seja tratado. IDs de debounce diferentes são tratados de forma independente.

Se você gostaria de limitar por quanto tempo um event frequentemente despachado pode adiar um listener, você pode fornecer o argumento `maxWait` ao atributo `DebounceFor`:

```php
#[DebounceFor(30, maxWait: 120)]
class UpdateProductSearchIndex implements ShouldQueue
{
    // ...
}
```

Você pode personalizar o cache store usado para o rastreamento de debounce definindo um método `debounceVia` no seu listener. O método recebe a instância do event e deve retornar um cache repository:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

public function debounceVia(ProductUpdated $event): Repository
{
    return Cache::driver('redis');
}
```

Listeners com debounce e listeners únicos são mutuamente exclusivos. Um listener que usa o atributo `DebounceFor` não deve implementar `ShouldBeUnique`.

> **Warning:**
> Se a sua aplicação despacha events de múltiplos servidores web ou contêineres, você deve garantir que todos os seus servidores estejam se comunicando com o mesmo servidor de cache central.

<a id="handling-failed-jobs"></a>
### Lidando com Jobs que Falharam

Às vezes seus event listeners enfileirados podem falhar. Se o listener enfileirado exceder o número máximo de tentativas definido pelo seu queue worker, o método `failed` será chamado no seu listener. O método `failed` recebe a instância do event e o `Throwable` que causou a falha:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Throwable;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // ...
    }

    /**
     * Handle a job failure.
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```

<a id="specifying-queued-listener-maximum-attempts"></a>
#### Especificando o Número Máximo de Tentativas de um Listener Enfileirado

Se um dos seus listeners enfileirados estiver encontrando um erro, você provavelmente não quer que ele continue tentando novamente indefinidamente. Portanto, o Laravel fornece várias maneiras de especificar quantas vezes ou por quanto tempo um listener pode ser tentado.

Você pode usar o atributo `Tries` na sua classe listener para especificar quantas vezes o listener pode ser tentado antes de ser considerado como falho:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Queue\InteractsWithQueue;

#[Tries(5)]
class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    // ...
}
```

Como alternativa a definir quantas vezes um listener pode ser tentado antes de falhar, você pode definir um momento no qual o listener não deve mais ser tentado. Isso permite que um listener seja tentado qualquer número de vezes dentro de um determinado intervalo de tempo. Para definir o momento em que um listener não deve mais ser tentado, adicione um método `retryUntil` à sua classe listener. Esse método deve retornar uma instância de `DateTimeInterface`:

```php
use DateTimeInterface;

/**
 * Determine the time at which the listener should timeout.
 */
public function retryUntil(): DateTimeInterface
{
    return now()->plus(minutes: 5);
}
```

Se tanto `retryUntil` quanto `tries` estiverem definidos, o Laravel dá precedência ao método `retryUntil`.

<a id="specifying-queued-listener-backoff"></a>
#### Especificando o Backoff de um Listener Enfileirado

Se você gostaria de configurar quantos segundos o Laravel deve esperar antes de tentar novamente um listener que encontrou uma exceção, você pode usar o atributo `Backoff` na sua classe listener:

```php
<?php

namespace App\Listeners;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Backoff;

#[Backoff(3)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

Se você precisar de uma lógica mais complexa para determinar o tempo de backoff do listener, você pode definir um método `backoff` na sua classe listener:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

Você pode configurar facilmente backoffs "exponenciais" retornando um array de valores de backoff a partir do método `backoff`. Neste exemplo, o delay de retry será de 1 segundo para o primeiro retry, 5 segundos para o segundo retry, 10 segundos para o terceiro retry e 10 segundos para cada retry subsequente se houver mais tentativas restantes:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 *
 * @return list<int>
 */
public function backoff(OrderShipped $event): array
{
    return [1, 5, 10];
}
```

<a id="specifying-queued-listener-max-exceptions"></a>
#### Especificando o Máximo de Exceções de um Listener Enfileirado

Às vezes você pode desejar especificar que um listener enfileirado pode ser tentado muitas vezes, mas deve falhar se os retries forem acionados por um determinado número de exceções não tratadas (em oposição a ser liberado pelo método `release` diretamente). Para fazer isso, você pode usar os atributos `Tries` e `MaxExceptions` na sua classe listener:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\MaxExceptions;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Queue\InteractsWithQueue;

#[Tries(25)]
#[MaxExceptions(3)]
class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }
}
```

Neste exemplo, o listener será tentado novamente até 25 vezes. No entanto, o listener falhará se três exceções não tratadas forem lançadas pelo listener.

<a id="specifying-queued-listener-timeout"></a>
#### Especificando o Timeout de um Listener Enfileirado

Frequentemente, você sabe aproximadamente quanto tempo espera que seus listeners enfileirados levem. Por essa razão, o Laravel permite que você especifique um valor de "timeout". Se um listener estiver processando por mais tempo do que o número de segundos especificado pelo valor de timeout, o worker que processa o listener encerrará com um erro. Você pode definir o número máximo de segundos que um listener pode executar usando o atributo `Timeout` na sua classe listener:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Timeout;

#[Timeout(120)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

Se você gostaria de indicar que um listener deve ser marcado como falho em caso de timeout, você pode usar o atributo `FailOnTimeout` na classe listener:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\FailOnTimeout;

#[FailOnTimeout]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

<a id="dispatching-events"></a>
## Despachando Events

Para despachar um event, você pode chamar o método estático `dispatch` no event. Esse método é disponibilizado no event pela trait `Illuminate\Foundation\Events\Dispatchable`. Quaisquer argumentos passados para o método `dispatch` serão passados para o construtor do event:

```php
<?php

namespace App\Http\Controllers;

use App\Events\OrderShipped;
use App\Models\Order;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class OrderShipmentController extends Controller
{
    /**
     * Ship the given order.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // Order shipment logic...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

Se você gostaria de despachar um event condicionalmente, você pode usar os métodos `dispatchIf` e `dispatchUnless`:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> **Note:**
> Ao testar, pode ser útil afirmar que determinados events foram despachados sem realmente acionar seus listeners. Os [helpers de teste integrados](#testing) do Laravel tornam isso muito fácil.

<a id="dispatching-events-after-database-transactions"></a>
### Despachando Events Após Transações de Banco de Dados

Às vezes, você pode querer instruir o Laravel a despachar um event somente após a transação de banco de dados ativa ter sido commitada. Para fazer isso, você pode implementar a interface `ShouldDispatchAfterCommit` na classe de event.

Essa interface instrui o Laravel a não despachar o event até que a transação de banco de dados atual seja commitada. Se a transação falhar, o event será descartado. Se nenhuma transação de banco de dados estiver em andamento quando o event for despachado, o event será despachado imediatamente:

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Contracts\Events\ShouldDispatchAfterCommit;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderShipped implements ShouldDispatchAfterCommit
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    /**
     * Create a new event instance.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

<a id="deferring-events"></a>
### Adiando Events

Events adiados permitem que você atrase o despacho de model events e a execução de event listeners até que um bloco de código específico tenha sido concluído. Isso é particularmente útil quando você precisa garantir que todos os registros relacionados sejam criados antes que os event listeners sejam acionados.

Para adiar events, forneça uma closure ao método `Event::defer()`:

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

Todos os events acionados dentro da closure serão despachados após a closure ser executada. Isso garante que os event listeners tenham acesso a todos os registros relacionados que foram criados durante a execução adiada. Se uma exceção ocorrer dentro da closure, os events adiados não serão despachados.

Para adiar apenas events específicos, passe um array de events como o segundo argumento para o método `defer`:

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
}, ['eloquent.created: '.User::class]);
```

<a id="event-subscribers"></a>
## Event Subscribers

<a id="writing-event-subscribers"></a>
### Escrevendo Event Subscribers

Event subscribers são classes que podem se inscrever em múltiplos events de dentro da própria classe subscriber, permitindo que você defina vários event handlers dentro de uma única classe. Subscribers devem definir um método `subscribe`, que recebe uma instância de event dispatcher. Você pode chamar o método `listen` no dispatcher fornecido para registrar event listeners:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * Handle user login events.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * Handle user logout events.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * Register the listeners for the subscriber.
     */
    public function subscribe(Dispatcher $events): void
    {
        $events->listen(
            Login::class,
            [UserEventSubscriber::class, 'handleUserLogin']
        );

        $events->listen(
            Logout::class,
            [UserEventSubscriber::class, 'handleUserLogout']
        );
    }
}
```

Se os métodos do seu event listener estiverem definidos dentro do próprio subscriber, você pode achar mais conveniente retornar um array de events e nomes de métodos a partir do método `subscribe` do subscriber. O Laravel determinará automaticamente o nome da classe do subscriber ao registrar os event listeners:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * Handle user login events.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * Handle user logout events.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * Register the listeners for the subscriber.
     *
     * @return array<string, string>
     */
    public function subscribe(Dispatcher $events): array
    {
        return [
            Login::class => 'handleUserLogin',
            Logout::class => 'handleUserLogout',
        ];
    }
}
```

<a id="registering-event-subscribers"></a>
### Registrando Event Subscribers

Após escrever o subscriber, o Laravel registrará automaticamente os métodos handler dentro do subscriber se eles seguirem as [convenções de descoberta de events](#event-discovery) do Laravel. Caso contrário, você pode registrar manualmente seu subscriber usando o método `subscribe` da facade `Event`. Normalmente, isso deve ser feito dentro do método `boot` do `AppServiceProvider` da sua aplicação:

```php
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Event::subscribe(UserEventSubscriber::class);
    }
}
```

<a id="testing"></a>
## Testes

Ao testar código que despacha events, você pode desejar instruir o Laravel a não executar de fato os listeners do event, já que o código do listener pode ser testado diretamente e separadamente do código que despacha o event correspondente. Claro, para testar o próprio listener, você pode instanciar uma instância de listener e invocar o método `handle` diretamente no seu teste.

Usando o método `fake` da facade `Event`, você pode impedir que listeners sejam executados, executar o código em teste e, em seguida, afirmar quais events foram despachados pela sua aplicação usando os métodos `assertDispatched`, `assertNotDispatched` e `assertNothingDispatched`:

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;

test('orders can be shipped', function () {
    Event::fake();

    // Perform order shipping...

    // Assert that an event was dispatched...
    Event::assertDispatched(OrderShipped::class);

    // Assert an event was dispatched twice...
    Event::assertDispatched(OrderShipped::class, 2);

    // Assert an event was dispatched once...
    Event::assertDispatchedOnce(OrderShipped::class);

    // Assert an event was not dispatched...
    Event::assertNotDispatched(OrderFailedToShip::class);

    // Assert that no events were dispatched...
    Event::assertNothingDispatched();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * Test order shipping.
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // Perform order shipping...

        // Assert that an event was dispatched...
        Event::assertDispatched(OrderShipped::class);

        // Assert an event was dispatched twice...
        Event::assertDispatched(OrderShipped::class, 2);

        // Assert an event was dispatched once...
        Event::assertDispatchedOnce(OrderShipped::class);

        // Assert an event was not dispatched...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // Assert that no events were dispatched...
        Event::assertNothingDispatched();
    }
}
```

Você pode passar uma closure aos métodos `assertDispatched` ou `assertNotDispatched` a fim de afirmar que um event que passa em um determinado "teste de verdade" foi despachado. Se pelo menos um event que passa no teste de verdade fornecido foi despachado, então a asserção terá sucesso:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

Como alternativa, você pode passar um array de valores de propriedade esperados como o segundo argumento para `assertDispatched` ou `assertNotDispatched`:

```php
Event::assertDispatched(OrderShipped::class, ['order' => $order]);
```

Todas as propriedades especificadas devem corresponder. Os valores são comparados usando igualdade estrita, enquanto os models do Eloquent são comparados usando seu método `is`.

Se você simplesmente gostaria de afirmar que um event listener está escutando um determinado event, você pode usar o método `assertListening`:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> **Warning:**
> Após chamar `Event::fake()`, nenhum event listener será executado. Então, se seus testes usam model factories que dependem de events, como criar um UUID durante o event `creating` de um model, você deve chamar `Event::fake()` **após** usar suas factories.

<a id="faking-a-subset-of-events"></a>
### Fazendo Fake de um Subconjunto de Events

Se você quiser apenas fazer fake dos event listeners para um conjunto específico de events, você pode passá-los ao método `fake` ou `fakeFor`:

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // Other events are dispatched as normal...
    $order->update([
        // ...
    ]);
});
```

```php tab=PHPUnit
/**
 * Test order process.
 */
public function test_orders_can_be_processed(): void
{
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // Other events are dispatched as normal...
    $order->update([
        // ...
    ]);
}
```

Você pode fazer fake de todos os events, exceto de um conjunto de events especificados, usando o método `except`:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a id="scoped-event-fakes"></a>
### Fakes de Event com Escopo

Se você quiser apenas fazer fake dos event listeners para uma parte do seu teste, você pode usar o método `fakeFor`:

```php tab=Pest
<?php

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades\Event;

test('orders can be processed', function () {
    $order = Event::fakeFor(function () {
        $order = Order::factory()->create();

        Event::assertDispatched(OrderCreated::class);

        return $order;
    });

    // Events are dispatched as normal and observers will run...
    $order->update([
        // ...
    ]);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * Test order process.
     */
    public function test_orders_can_be_processed(): void
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // Events are dispatched as normal and observers will run...
        $order->update([
            // ...
        ]);
    }
}
```
