---
title: "Filas"
---

- [Introdução](#introduction)
    - [Conexões vs. Filas](#connections-vs-queues)
    - [Notas sobre Drivers e Pré-requisitos](#driver-prerequisites)
- [Criando Jobs](#creating-jobs)
    - [Gerando Classes de Job](#generating-job-classes)
    - [Estrutura da Classe](#class-structure)
    - [Jobs Únicos](#unique-jobs)
    - [Jobs com Debounce](#debounced-jobs)
    - [Jobs Criptografados](#encrypted-jobs)
- [Middleware de Job](#job-middleware)
    - [Limitação de Taxa](#rate-limiting)
    - [Prevenindo Sobreposição de Jobs](#preventing-job-overlaps)
    - [Limitando Exceções](#throttling-exceptions)
    - [Liberando Jobs](#releasing-jobs)
    - [Ignorando Jobs](#skipping-jobs)
- [Despachando Jobs](#dispatching-jobs)
    - [Despacho Adiado](#delayed-dispatching)
    - [Despacho Síncrono](#synchronous-dispatching)
    - [Despacho em Massa](#bulk-dispatching)
    - [Preparando Jobs Antes do Despacho](#preparing-jobs-before-dispatch)
    - [Jobs e Transações de Banco de Dados](#jobs-and-database-transactions)
    - [Encadeamento de Jobs](#job-chaining)
    - [Personalizando a Fila e a Conexão](#customizing-the-queue-and-connection)
    - [Especificando Número Máximo de Tentativas / Valores de Timeout](#max-job-attempts-and-timeout)
    - [SQS FIFO e Filas Justas](#sqs-fifo-and-fair-queues)
    - [Failover de Fila](#queue-failover)
    - [Tratamento de Erros](#error-handling)
- [Processamento em Lote de Jobs](#job-batching)
    - [Definindo Jobs em Lote](#defining-batchable-jobs)
    - [Despachando Lotes](#dispatching-batches)
    - [Encadeamentos e Lotes](#chains-and-batches)
    - [Adicionando Jobs a Lotes](#adding-jobs-to-batches)
    - [Inspecionando Lotes](#inspecting-batches)
    - [Cancelando Lotes](#cancelling-batches)
    - [Falhas em Lotes](#batch-failures)
    - [Podando Lotes](#pruning-batches)
    - [Armazenando Lotes no DynamoDB](#storing-batches-in-dynamodb)
- [Enfileirando Closures](#queueing-closures)
- [Executando o Worker da Fila](#running-the-queue-worker)
    - [O Comando `queue:work`](#the-queue-work-command)
    - [Prioridades de Fila](#queue-priorities)
    - [Workers de Fila e Deploy](#queue-workers-and-deployment)
    - [Reagindo a Sinais do Worker](#reacting-to-worker-signals)
    - [Expiração e Timeouts de Jobs](#job-expirations-and-timeouts)
    - [Pausando e Retomando Workers de Fila](#pausing-and-resuming-queue-workers)
- [Configuração do Supervisor](#supervisor-configuration)
- [Lidando com Jobs Falhos](#dealing-with-failed-jobs)
    - [Limpando Jobs Falhos](#cleaning-up-after-failed-jobs)
    - [Reexecutando Jobs Falhos](#retrying-failed-jobs)
    - [Ignorando Models Ausentes](#ignoring-missing-models)
    - [Podando Jobs Falhos](#pruning-failed-jobs)
    - [Armazenando Jobs Falhos no DynamoDB](#storing-failed-jobs-in-dynamodb)
    - [Desabilitando o Armazenamento de Jobs Falhos](#disabling-failed-job-storage)
    - [Eventos de Jobs Falhos](#failed-job-events)
- [Limpando Jobs das Filas](#clearing-jobs-from-queues)
- [Monitorando Suas Filas](#monitoring-your-queues)
- [Testes](#testing)
    - [Simulando um Subconjunto de Jobs](#faking-a-subset-of-jobs)
    - [Testando Encadeamentos de Jobs](#testing-job-chains)
    - [Testando Lotes de Jobs](#testing-job-batches)
    - [Testando Interações entre Job e Fila](#testing-job-queue-interactions)
- [Eventos de Job](#job-events)

<a id="introduction"></a>
## Introdução

Ao construir sua aplicação web, você pode ter algumas tarefas, como analisar e armazenar um arquivo CSV enviado, que levam tempo demais para serem executadas durante uma requisição web típica. Felizmente, o Laravel permite que você crie facilmente jobs enfileirados que podem ser processados em segundo plano. Ao mover tarefas demoradas para uma fila, sua aplicação pode responder às requisições web com grande velocidade e oferecer uma experiência melhor aos seus clientes.

As filas do Laravel fornecem uma API de enfileiramento unificada para diversos backends de fila, como [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io) ou mesmo um banco de dados relacional.

As opções de configuração de filas do Laravel são armazenadas no arquivo de configuração `config/queue.php` da sua aplicação. Neste arquivo, você encontrará as configurações de conexão para cada um dos drivers de fila incluídos no framework, incluindo os drivers de banco de dados, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io) e [Beanstalkd](https://beanstalkd.github.io/), além de um driver síncrono que executa os jobs imediatamente (para uso durante o desenvolvimento ou testes). Também é incluído um driver de fila `null`, que descarta os jobs enfileirados.

> **Nota:**
> O Laravel Horizon é um painel e sistema de configuração elegante para suas filas baseadas em Redis. Confira a [documentação completa do Horizon](/en/horizon/) para mais informações.

<a id="connections-vs-queues"></a>
### Conexões vs. Filas

Antes de começar com as filas do Laravel, é importante entender a distinção entre "conexões" e "filas". No seu arquivo de configuração `config/queue.php`, existe um array de configuração `connections`. Esta opção define as conexões com os serviços de fila de backend, como Amazon SQS, Beanstalk ou Redis. No entanto, qualquer conexão de fila pode ter várias "filas", que podem ser vistas como diferentes pilhas ou montes de jobs enfileirados.

Observe que cada exemplo de configuração de conexão no arquivo de configuração `queue` contém um atributo `queue`. Esta é a fila padrão para a qual os jobs serão despachados quando enviados para uma determinada conexão. Em outras palavras, se você despachar um job sem definir explicitamente para qual fila ele deve ser despachado, o job será colocado na fila definida no atributo `queue` da configuração da conexão:

```php
use App\Jobs\ProcessPodcast;

// This job is sent to the default connection's default queue...
ProcessPodcast::dispatch();

// This job is sent to the default connection's "emails" queue...
ProcessPodcast::dispatch()->onQueue('emails');
```

Algumas aplicações podem nunca precisar enviar jobs para múltiplas filas, preferindo ter apenas uma fila simples. No entanto, enviar jobs para várias filas pode ser especialmente útil para aplicações que desejam priorizar ou segmentar como os jobs são processados, já que o worker de fila do Laravel permite especificar quais filas ele deve processar por prioridade. Por exemplo, se você enviar jobs para uma fila `high`, pode executar um worker que dê a eles maior prioridade de processamento:

```shell
php artisan queue:work --queue=high,default
```

<a id="driver-prerequisites"></a>
### Notas sobre Drivers e Pré-requisitos

<a id="database"></a>
#### Database

Para usar o driver de fila `database`, você precisará de uma tabela de banco de dados para armazenar os jobs. Tipicamente, isso está incluído na [migração de banco de dados](../migrations/) padrão do Laravel `0001_01_01_000002_create_jobs_table.php`; no entanto, se sua aplicação não contém esta migração, você pode usar o comando Artisan `make:queue-table` para criá-la:

```shell
php artisan make:queue-table

php artisan migrate
```

<a id="redis"></a>
#### Redis

Para usar o driver de fila `redis`, você deve configurar uma conexão com o banco de dados Redis no arquivo de configuração `config/database.php`.

> **Aviso:**
> As opções `serializer` e `compression` do Redis não são suportadas pelo driver de fila `redis`.

<a id="redis-cluster"></a>
##### Redis Cluster

Se sua conexão de fila Redis usar um [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering), os nomes das suas filas devem conter uma [hash tag de chave](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags). Isso é necessário para garantir que todas as chaves Redis de uma determinada fila sejam colocadas no mesmo slot de hash:

```php
'redis' => [
    'driver' => 'redis',
    'connection' => env('REDIS_QUEUE_CONNECTION', 'default'),
    'queue' => env('REDIS_QUEUE', '{default}'),
    'retry_after' => env('REDIS_QUEUE_RETRY_AFTER', 90),
    'block_for' => null,
    'after_commit' => false,
],
```

<a id="blocking"></a>
##### Bloqueio

Ao usar a fila Redis, você pode usar a opção de configuração `block_for` para especificar por quanto tempo o driver deve aguardar até que um job esteja disponível antes de iterar pelo loop do worker e consultar novamente o banco de dados Redis.

Ajustar este valor de acordo com a carga da sua fila pode ser mais eficiente do que consultar continuamente o banco de dados Redis em busca de novos jobs. Por exemplo, você pode definir o valor como `5` para indicar que o driver deve bloquear por cinco segundos enquanto aguarda a disponibilidade de um job:

```php
'redis' => [
    'driver' => 'redis',
    'connection' => env('REDIS_QUEUE_CONNECTION', 'default'),
    'queue' => env('REDIS_QUEUE', 'default'),
    'retry_after' => env('REDIS_QUEUE_RETRY_AFTER', 90),
    'block_for' => 5,
    'after_commit' => false,
],
```

> **Aviso:**
> Definir `block_for` como `0` fará com que os workers de fila bloqueiem indefinidamente até que um job esteja disponível. Isso também impedirá que sinais como `SIGTERM` sejam tratados até que o próximo job seja processado.

<a id="sqs-overflow-storage"></a>
#### Armazenamento de Overflow do SQS

O Amazon SQS limita o tamanho máximo do payload de uma mensagem enfileirada. Se você precisar despachar jobs com payloads que podem exceder esse limite, pode configurar o Laravel para armazenar payloads SQS grandes demais em um cache store e enviar um ponteiro pelo SQS. Para habilitar este recurso, adicione um array `overflow` à configuração da sua conexão de fila SQS:

```php
'sqs' => [
    'driver' => 'sqs',
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'prefix' => env('SQS_PREFIX', 'https://sqs.us-east-1.amazonaws.com/your-account-id'),
    'queue' => env('SQS_QUEUE', 'default'),
    'suffix' => env('SQS_SUFFIX'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'after_commit' => false,
    'overflow' => [
        'enabled' => env('SQS_OVERFLOW_ENABLED', false),
        'store' => env('SQS_OVERFLOW_STORE'),
        'always' => false,
        'delete_after_processing' => true,
        'flush_on_clear' => env('SQS_OVERFLOW_FLUSH_ON_CLEAR', false),
    ],
],
```

Quando o armazenamento de overflow está habilitado, o Laravel armazenará no cache store configurado os payloads que tenham pelo menos 1 MB. Se a opção `always` for `true`, todo payload SQS será armazenado no cache store, independentemente do seu tamanho. Como os jobs enfileirados precisarão recuperar seus payloads do cache store quando forem processados, você deve escolher um store que consiga reter os payloads até que seus workers os processem. Por padrão, os payloads armazenados são excluídos após seus jobs serem processados com sucesso e removidos do SQS.

Se a opção `flush_on_clear` for `true`, o cache store de overflow configurado será limpo quando o comando `queue:clear` limpar a fila SQS. Como limpar um cache store pode remover todos os itens dele, você deve configurar o armazenamento de overflow do SQS para usar um cache store dedicado ao habilitar esta opção.

<a id="other-driver-prerequisites"></a>
#### Outros Pré-requisitos de Drivers

As seguintes dependências são necessárias para os drivers de fila listados. Essas dependências podem ser instaladas pelo gerenciador de pacotes Composer:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ^7.0|^8.0`
- Redis: `predis/predis ~3.0` ou a extensão PHP phpredis
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a id="creating-jobs"></a>
## Criando Jobs

<a id="generating-job-classes"></a>
### Gerando Classes de Job

Por padrão, todos os jobs enfileiráveis da sua aplicação são armazenados no diretório `app/Jobs`. Se o diretório `app/Jobs` não existir, ele será criado quando você executar o comando Artisan `make:job`:

```shell
php artisan make:job ProcessPodcast
```

A classe gerada implementará a interface `Illuminate\Contracts\Queue\ShouldQueue`, indicando ao Laravel que o job deve ser enviado para a fila para ser executado de forma assíncrona.

> **Nota:**
> Os stubs de job podem ser personalizados usando [publicação de stubs](/en/artisan/#stub-customization).

<a id="class-structure"></a>
### Estrutura da Classe

As classes de job são muito simples, normalmente contendo apenas um método `handle` que é invocado quando o job é processado pela fila. Para começar, vejamos um exemplo de classe de job. Neste exemplo, vamos fingir que gerenciamos um serviço de publicação de podcasts e precisamos processar os arquivos de podcast enviados antes que sejam publicados:

```php
<?php

namespace App\Jobs;

use App\Models\Podcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(AudioProcessor $processor): void
    {
        // Process uploaded podcast...
    }
}
```

Neste exemplo, observe que conseguimos passar um [model Eloquent](/en/eloquent/) diretamente para o construtor do job enfileirado. Por causa da trait `Queueable` que o job utiliza, os models Eloquent e seus relacionamentos carregados serão serializados e desserializados de forma transparente durante o processamento do job.

Se o seu job enfileirado aceitar um model Eloquent em seu construtor, apenas o identificador do model será serializado na fila. Quando o job for realmente tratado, o sistema de filas recuperará automaticamente a instância completa do model e seus relacionamentos carregados do banco de dados. Essa abordagem de serialização de models permite que payloads de job muito menores sejam enviados ao seu driver de fila.

<a id="handle-method-dependency-injection"></a>
#### Injeção de Dependências no Método `handle`

O método `handle` é invocado quando o job é processado pela fila. Observe que podemos usar type-hints para dependências no método `handle` do job. O [container de serviço](/en/container/) do Laravel injeta essas dependências automaticamente.

Se você quiser ter controle total sobre como o container injeta dependências no método `handle`, pode usar o método `bindMethod` do container. O método `bindMethod` aceita um callback que recebe o job e o container. Dentro do callback, você está livre para invocar o método `handle` como desejar. Tipicamente, você deve chamar este método a partir do método `boot` do seu [service provider](/en/providers/) `App\Providers\AppServiceProvider`:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> **Aviso:**
> Dados binários, como o conteúdo bruto de uma imagem, devem ser passados pela função `base64_encode` antes de serem enviados para um job enfileirado. Caso contrário, o job pode não ser serializado corretamente em JSON ao ser colocado na fila.

<a id="handling-relationships"></a>
#### Relacionamentos Enfileirados

Como todos os relacionamentos de models Eloquent carregados também são serializados quando um job é enfileirado, a string serializada do job às vezes pode ficar bastante grande. Além disso, quando um job é desserializado e os relacionamentos dos models são recuperados do banco de dados, eles serão recuperados por completo. Quaisquer restrições de relacionamento aplicadas antes de o model ser serializado durante o processo de enfileiramento do job não serão aplicadas quando o job for desserializado. Portanto, se você deseja trabalhar com um subconjunto de um determinado relacionamento, deve restringir novamente esse relacionamento dentro do seu job enfileirado.

Ou, para impedir que relacionamentos sejam serializados, você pode chamar o método `withoutRelations` no model ao definir o valor de uma propriedade. Este método retornará uma instância do model sem seus relacionamentos carregados:

```php
/**
 * Create a new job instance.
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

Se você precisar remover apenas relações específicas mantendo as demais, pode usar o método `withoutRelation`:

```php
$this->podcast = $podcast->withoutRelation('comments');
```

Se você estiver usando [promoção de propriedades no construtor do PHP](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion) e quiser indicar que um model Eloquent não deve ter seus relacionamentos serializados, pode usar o atributo `WithoutRelations`:

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * Create a new job instance.
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

Por conveniência, se você quiser serializar todos os models sem relacionamentos, pode aplicar o atributo `WithoutRelations` à classe inteira, em vez de aplicá-lo a cada model:

```php
<?php

namespace App\Jobs;

use App\Models\DistributionPlatform;
use App\Models\Podcast;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\WithoutRelations;

#[WithoutRelations]
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```

Se um job receber uma coleção ou array de models Eloquent em vez de um único model, os models dentro dessa coleção não terão seus relacionamentos restaurados quando o job for desserializado e executado. Isso serve para evitar uso excessivo de recursos em jobs que lidam com grandes quantidades de models.

<a id="unique-jobs"></a>
### Jobs Únicos

> **Aviso:**
> Jobs únicos exigem um driver de cache que suporte [locks](/en/cache/#atomic-locks). Atualmente, os drivers de cache `memcached`, `redis`, `dynamodb`, `database`, `file` e `array` suportam locks atômicos.

> **Aviso:**
> As restrições de job único não se aplicam a jobs dentro de lotes.

Às vezes, você pode querer garantir que apenas uma instância de um job específico esteja na fila em um determinado momento. Você pode fazer isso implementando a interface `ShouldBeUnique` na sua classe de job. Esta interface não exige que você defina nenhum método adicional na sua classe:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

No exemplo acima, o job `UpdateSearchIndex` é único. Assim, o job não será despachado se outra instância do job já estiver na fila e ainda não tiver terminado de ser processada.

Em certos casos, você pode querer definir uma "chave" específica que torne o job único, ou pode querer especificar um timeout após o qual o job deixa de ser único. Para isso, você pode usar o atributo `UniqueFor` e definir um método `uniqueId` na sua classe de job:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Queue\Attributes\UniqueFor;

#[UniqueFor(3600)]
class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * The product instance.
     *
     * @var \App\Models\Product
     */
    public $product;

    /**
     * Get the unique ID for the job.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

No exemplo acima, o job `UpdateSearchIndex` é único por um ID de produto. Assim, qualquer novo despacho do job com o mesmo ID de produto será ignorado até que o job existente termine de ser processado. Além disso, se o job existente não for processado dentro de uma hora, o lock único será liberado e outro job com a mesma chave única poderá ser despachado para a fila.

> **Aviso:**
> Se sua aplicação despachar jobs a partir de múltiplos servidores web ou contêineres, você deve garantir que todos os seus servidores estejam se comunicando com o mesmo servidor de cache central, para que o Laravel possa determinar com precisão se um job é único.

<a id="keeping-jobs-unique-until-processing-begins"></a>
#### Mantendo Jobs Únicos Até o Início do Processamento

Por padrão, jobs únicos são "desbloqueados" após um job terminar de ser processado ou falhar em todas as suas tentativas de retry. No entanto, pode haver situações em que você queira que seu job seja desbloqueado imediatamente antes de ser processado. Para isso, seu job deve implementar o contrato `ShouldBeUniqueUntilProcessing` em vez do contrato `ShouldBeUnique`:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUniqueUntilProcessing
{
    // ...
}
```

<a id="unique-job-locks"></a>
#### Locks de Jobs Únicos

Nos bastidores, quando um job `ShouldBeUnique` é despachado, o Laravel tenta adquirir um [lock](/en/cache/#atomic-locks) com a chave `uniqueId`. Se o lock já estiver em posse de outro processo, o job não é despachado. Este lock é liberado quando o job termina de ser processado ou falha em todas as suas tentativas de retry. Por padrão, o Laravel usará o driver de cache padrão para obter este lock. No entanto, se você desejar usar outro driver para adquirir o lock, pode definir um método `uniqueVia` que retorna o driver de cache que deve ser usado:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * Get the cache driver for the unique job lock.
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> **Nota:**
> Se você só precisar limitar o processamento concorrente de um job, use o middleware de job [WithoutOverlapping](/en/queues/#preventing-job-overlaps) em vez disso.

<a id="debounced-jobs"></a>
### Jobs com Debounce

Às vezes, você pode querer garantir que, quando o mesmo job for despachado muitas vezes em um curto intervalo, apenas o despacho mais recente seja de fato executado. Você pode fazer isso adicionando o atributo `DebounceFor` ao seu job:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\DebounceFor;

#[DebounceFor(30)]
class UpdateSearchIndex implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(public int $productId)
    {
    }

    /**
     * Get the debounce ID for the job.
     */
    public function debounceId(): string
    {
        return (string) $this->productId;
    }
}
```

No exemplo acima, despachar repetidamente `UpdateSearchIndex` para o mesmo produto dentro de `30` segundos fará com que o job sofra debounce, de modo que apenas o despacho mais recente seja executado.

Se você quiser limitar por quanto tempo um job despachado novamente com frequência pode ser adiado, pode fornecer o argumento `maxWait` ao atributo `DebounceFor`:

```php
#[DebounceFor(30, maxWait: 120)]
class UpdateSearchIndex implements ShouldQueue
{
    use Queueable;

    // ...
}
```

Você pode personalizar o cache store usado para rastrear o debounce definindo um método `debounceVia` no seu job:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

public function debounceVia(): Repository
{
    return Cache::driver('redis');
}
```

Se um job com debounce for substituído por um despacho mais recente, o Laravel despachará o evento `Illuminate\Queue\Events\JobDebounced` e removerá da fila o job substituído.

> **Aviso:**
> Jobs com debounce e jobs únicos são mutuamente exclusivos. Um job que usa o atributo `DebounceFor` não deve implementar `ShouldBeUnique`.

> **Aviso:**
> Se sua aplicação despachar jobs com debounce a partir de múltiplos servidores web ou contêineres, você deve garantir que todos os seus servidores estejam se comunicando com o mesmo servidor de cache central.

<a id="encrypted-jobs"></a>
### Jobs Criptografados

O Laravel permite garantir a privacidade e a integridade dos dados de um job por meio de [criptografia](/en/encryption/). Para começar, basta adicionar a interface `ShouldBeEncrypted` à classe do job. Depois que essa interface for adicionada à classe, o Laravel criptografará automaticamente o seu job antes de enviá-lo para a fila:

```php
<?php

use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;

class UpdateSearchIndex implements ShouldQueue, ShouldBeEncrypted
{
    // ...
}
```

<a id="job-middleware"></a>
## Middleware de Job

Os middlewares de job permitem envolver lógica personalizada em torno da execução de jobs enfileirados, reduzindo o código repetitivo dentro dos próprios jobs. Por exemplo, considere o seguinte método `handle`, que utiliza os recursos de limitação de taxa do Redis do Laravel para permitir que apenas um job seja processado a cada cinco segundos:

```php
use Illuminate\Support\Facades\Redis;

/**
 * Execute the job.
 */
public function handle(): void
{
    Redis::throttle('key')->block(0)->allow(1)->every(5)->then(function () {
        info('Lock obtained...');

        // Handle job...
    }, function () {
        // Could not obtain lock...

        return $this->release(5);
    });
}
```

Embora este código seja válido, a implementação do método `handle` fica confusa, pois está poluída com a lógica de limitação de taxa do Redis. Além disso, essa lógica de limitação precisa ser duplicada para qualquer outro job que queiramos limitar. Em vez de limitar a taxa dentro do método handle, podemos definir um middleware de job que trate da limitação de taxa:

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * Process the queued job.
     *
     * @param  \Closure(object): void  $next
     */
    public function handle(object $job, Closure $next): void
    {
        Redis::throttle('key')
            ->block(0)->allow(1)->every(5)
            ->then(function () use ($job, $next) {
                // Lock obtained...

                $next($job);
            }, function () use ($job) {
                // Could not obtain lock...

                $job->release(5);
            });
    }
}
```

Como você pode ver, assim como o [middleware de rota](/en/middleware/), os middlewares de job recebem o job que está sendo processado e um callback que deve ser invocado para continuar o processamento do job.

Você pode gerar uma nova classe de middleware de job usando o comando Artisan `make:job-middleware`. Após criar um middleware de job, ele pode ser anexado a um job retornando-o no método `middleware` do job. Este método não existe nos jobs gerados pelo comando Artisan `make:job`, então você precisará adicioná-lo manualmente à sua classe de job:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> **Nota:**
> Middlewares de job também podem ser atribuídos a [listeners de eventos enfileiráveis](/en/events/#queued-event-listeners), [mailables](/en/mail/#queueing-mail) e [notificações](/en/notifications/#queueing-notifications).

<a id="rate-limiting"></a>
### Limitação de Taxa

Embora acabamos de demonstrar como escrever seu próprio middleware de job de limitação de taxa, o Laravel na verdade inclui um middleware de limitação de taxa que você pode utilizar para limitar a taxa de jobs. Assim como os [limitadores de taxa de rota](/en/routing/#defining-rate-limiters), os limitadores de taxa de jobs são definidos usando o método `for` da facade `RateLimiter`.

Por exemplo, você pode querer permitir que os usuários façam backup de seus dados uma vez por hora, sem impor esse limite aos clientes premium. Para isso, você pode definir um `RateLimiter` no método `boot` do seu `AppServiceProvider`:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    RateLimiter::for('backups', function (object $job) {
        return $job->user->vipCustomer()
            ? Limit::none()
            : Limit::perHour(1)->by($job->user->id);
    });
}
```

No exemplo acima, definimos um limite de taxa por hora; no entanto, você pode facilmente definir um limite de taxa baseado em minutos usando o método `perMinute`. Além disso, você pode passar qualquer valor que desejar para o método `by` do limite de taxa; porém, esse valor é mais comumente usado para segmentar os limites de taxa por cliente:

```php
return Limit::perMinute(50)->by($job->user->id);
```

Depois de definir seu limite de taxa, você pode anexar o limitador de taxa ao seu job usando o middleware `Illuminate\Queue\Middleware\RateLimited`. Cada vez que o job exceder o limite de taxa, este middleware liberará o job de volta para a fila com um atraso apropriado, baseado na duração do limite de taxa:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

Liberar um job limitado por taxa de volta para a fila ainda incrementará o número total de `attempts` do job. Você pode querer ajustar os atributos `Tries` e `MaxExceptions` na sua classe de job de acordo com isso. Ou, você pode querer usar o [método retryUntil](#time-based-attempts) para definir por quanto tempo o job não deve mais ser tentado.

Usando o método `releaseAfter`, você também pode especificar o número de segundos que devem decorrer antes que o job liberado seja tentado novamente:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

Se você não quiser que um job seja tentado novamente quando estiver limitado por taxa, pode usar o método `dontRelease`:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

<a id="rate-limiting-with-redis"></a>
#### Limitação de Taxa com Redis

Se você estiver usando Redis, pode usar o middleware `Illuminate\Queue\Middleware\RateLimitedWithRedis`, que é ajustado especificamente para o Redis e é mais eficiente que o middleware básico de limitação de taxa:

```php
use Illuminate\Queue\Middleware\RateLimitedWithRedis;

public function middleware(): array
{
    return [new RateLimitedWithRedis('backups')];
}
```

O método `connection` pode ser usado para especificar qual conexão Redis o middleware deve usar:

```php
return [(new RateLimitedWithRedis('backups'))->connection('limiter')];
```

<a id="preventing-job-overlaps"></a>
### Prevenindo Sobreposição de Jobs

O Laravel inclui um middleware `Illuminate\Queue\Middleware\WithoutOverlapping` que permite prevenir a sobreposição de jobs com base em uma chave arbitrária. Isso pode ser útil quando um job enfileirado está modificando um recurso que deve ser modificado apenas por um job por vez.

Por exemplo, imagine que você tenha um job enfileirado que atualiza a pontuação de crédito de um usuário e você deseja evitar sobreposições de jobs de atualização de pontuação de crédito para o mesmo ID de usuário. Para isso, você pode retornar o middleware `WithoutOverlapping` no método `middleware` do seu job:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

Liberar um job sobreposto de volta para a fila ainda incrementará o número total de tentativas do job. Você pode querer ajustar os atributos `Tries` e `MaxExceptions` na sua classe de job de acordo com isso. Por exemplo, deixar `Tries` como 1, como é por padrão, impediria que qualquer job sobreposto fosse tentado novamente mais tarde.

Quaisquer jobs sobrepostos do mesmo tipo serão liberados de volta para a fila. Você também pode especificar o número de segundos que devem decorrer antes que o job liberado seja tentado novamente:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

Se você quiser excluir imediatamente quaisquer jobs sobrepostos para que eles não sejam tentados novamente, pode usar o método `dontRelease`:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

O middleware `WithoutOverlapping` é baseado no recurso de locks atômicos do Laravel. Às vezes, seu job pode falhar inesperadamente ou sofrer timeout de tal forma que o lock não seja liberado. Por isso, você pode definir explicitamente um tempo de expiração para o lock usando o método `expireAfter`. Por exemplo, o exemplo abaixo instruirá o Laravel a liberar o lock `WithoutOverlapping` três minutos após o job ter começado a ser processado:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> **Aviso:**
> O middleware `WithoutOverlapping` exige um driver de cache que suporte [locks](/en/cache/#atomic-locks). Atualmente, os drivers de cache `memcached`, `redis`, `dynamodb`, `database`, `file` e `array` suportam locks atômicos.

<a id="sharing-lock-keys"></a>
#### Compartilhando Chaves de Lock Entre Classes de Job

Por padrão, o middleware `WithoutOverlapping` apenas evitará sobreposições de jobs da mesma classe. Assim, embora duas classes de job diferentes possam usar a mesma chave de lock, não será evitada a sobreposição entre elas. No entanto, você pode instruir o Laravel a aplicar a chave entre classes de job usando o método `shared`:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

class ProviderIsDown
{
    // ...

    public function middleware(): array
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}

class ProviderIsUp
{
    // ...

    public function middleware(): array
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}
```

<a id="throttling-exceptions"></a>
### Limitando Exceções

O Laravel inclui um middleware `Illuminate\Queue\Middleware\ThrottlesExceptions` que permite limitar exceções. Quando o job lança um determinado número de exceções, todas as tentativas seguintes de executar o job são adiadas até que um intervalo de tempo especificado tenha decorrido. Este middleware é particularmente útil para jobs que interagem com serviços de terceiros instáveis.

Por exemplo, imagine um job enfileirado que interage com uma API de terceiros que começa a lançar exceções. Para limitar as exceções, você pode retornar o middleware `ThrottlesExceptions` no método `middleware` do seu job. Tipicamente, este middleware deve ser combinado com um job que implemente [tentativas baseadas em tempo](#time-based-attempts):

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * Determine the time at which the job should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 30);
}
```

O primeiro argumento do construtor aceito pelo middleware é o número de exceções que o job pode lançar antes de ser limitado, enquanto o segundo argumento do construtor é o número de segundos que devem decorrer antes que o job seja tentado novamente após ter sido limitado. No exemplo de código acima, se o job lançar 10 exceções consecutivas, aguardaremos 5 minutos antes de tentar o job novamente, respeitando o limite de tempo de 30 minutos.

Quando um job lança uma exceção, mas o limite de exceções ainda não foi atingido, o job normalmente será tentado novamente imediatamente. No entanto, você pode especificar o número de minutos pelo qual esse job deve ser adiado chamando o método `backoff` ao anexar o middleware ao job:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

O método `backoff` também aceita um closure que recebe a exceção lançada, permitindo que o atraso seja determinado dinamicamente:

```php
use App\Exceptions\RateLimitedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;
use Throwable;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(
        fn (Throwable $throwable) => $throwable instanceof RateLimitedException
            ? $throwable->retryAfterMinutes()
            : 5
    )];
}
```

Internamente, este middleware usa o sistema de cache do Laravel para implementar a limitação de taxa, e o nome da classe do job é utilizado como "chave" do cache. Você pode substituir esta chave chamando o método `by` ao anexar o middleware ao seu job. Isso pode ser útil se você tiver vários jobs interagindo com o mesmo serviço de terceiros e quiser que eles compartilhem um "balde" de limitação comum, garantindo que respeitem um único limite compartilhado:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

Por padrão, este middleware limitará todas as exceções. Você pode modificar esse comportamento invocando o método `when` ao anexar o middleware ao seu job. A exceção só será limitada se o closure fornecido ao método `when` retornar `true`:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->when(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```

Diferentemente do método `when`, que libera o job de volta para a fila ou lança uma exceção, o método `deleteWhen` permite excluir o job por completo quando uma determinada exceção ocorre:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

Se você quiser que as exceções limitadas sejam reportadas ao handler de exceções da sua aplicação, pode fazer isso invocando o método `report` ao anexar o middleware ao seu job. Opcionalmente, você pode fornecer um closure ao método `report`, e a exceção só será reportada se o closure fornecido retornar `true`:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->report(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```

<a id="throttling-exceptions-with-redis"></a>
#### Limitando Exceções com Redis

Se você estiver usando Redis, pode usar o middleware `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis`, que é ajustado especificamente para o Redis e é mais eficiente que o middleware básico de limitação de exceções:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis;

public function middleware(): array
{
    return [new ThrottlesExceptionsWithRedis(10, 10 * 60)];
}
```

O método `connection` pode ser usado para especificar qual conexão Redis o middleware deve usar:

```php
return [(new ThrottlesExceptionsWithRedis(10, 10 * 60))->connection('limiter')];
```

<a id="releasing-jobs"></a>
### Liberando Jobs

O middleware `Release` permite liberar um job de volta para a fila sem executá-lo. O método `Release::when` liberará o job se a condição fornecida for avaliada como `true`, enquanto o método `Release::unless` liberará o job se a condição for avaliada como `false`:

```php
use Illuminate\Queue\Middleware\Release;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Release::when($condition, releaseAfter: 60),
    ];
}
```

Liberar um job de volta para a fila ainda incrementará o número total de tentativas do job. Você pode querer ajustar os atributos `Tries` e `MaxExceptions` na sua classe de job de acordo com isso.

Você também pode passar um `Closure` aos métodos `when` e `unless` para uma avaliação condicional mais complexa:

```php
use Illuminate\Queue\Middleware\Release;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Release::when(function (): bool {
            return ! $this->order->isPaid();
        }, releaseAfter: 60),
    ];
}
```

<a id="skipping-jobs"></a>
### Ignorando Jobs

O middleware `Skip` permite especificar que um job deve ser ignorado / excluído sem precisar modificar a lógica do job. O método `Skip::when` excluirá o job se a condição fornecida for avaliada como `true`, enquanto o método `Skip::unless` excluirá o job se a condição for avaliada como `false`:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

Você também pode passar um `Closure` aos métodos `when` e `unless` para uma avaliação condicional mais complexa:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Skip::when(function (): bool {
            return $this->shouldSkip();
        }),
    ];
}
```

<a id="dispatching-jobs"></a>
## Despachando Jobs

Depois de escrever sua classe de job, você pode despachá-la usando o método `dispatch` no próprio job. Os argumentos passados ao método `dispatch` serão entregues ao construtor do job:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast);

        return redirect('/podcasts');
    }
}
```

Se você quiser despachar um job condicionalmente, pode usar os métodos `dispatchIf` e `dispatchUnless`:

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

Em novas aplicações Laravel, a conexão `database` é definida como a fila padrão. Você pode especificar uma conexão de fila padrão diferente alterando a variável de ambiente `QUEUE_CONNECTION` no arquivo `.env` da sua aplicação.

<a id="delayed-dispatching"></a>
### Despacho Adiado

Se você quiser especificar que um job não deve estar imediatamente disponível para processamento por um worker de fila, pode usar o método `delay` ao despachar o job. Por exemplo, vamos especificar que um job não deve estar disponível para processamento até 10 minutos após ter sido despachado:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast)
            ->delay(now()->plus(minutes: 10));

        return redirect('/podcasts');
    }
}
```

Em alguns casos, os jobs podem ter um atraso padrão configurado. Se você precisar ignorar esse atraso e despachar um job para processamento imediato, pode usar o método `withoutDelay`:

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> **Aviso:**
> O serviço de fila Amazon SQS tem um tempo máximo de atraso de 15 minutos.

<a id="synchronous-dispatching"></a>
### Despacho Síncrono

Se você quiser despachar um job imediatamente (de forma síncrona), pode usar o método `dispatchSync`. Ao usar este método, o job não será enfileirado e será executado imediatamente dentro do processo atual:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatchSync($podcast);

        return redirect('/podcasts');
    }
}
```

<a id="deferred-dispatching"></a>
#### Despacho Diferido

Usando o despacho síncrono diferido, você pode despachar um job para ser processado durante o processo atual, mas depois que a resposta HTTP tiver sido enviada ao usuário. Isso permite processar jobs "enfileirados" de forma síncrona sem prejudicar a experiência do usuário na aplicação. Para adiar a execução de um job síncrono, despache o job para a conexão `deferred`:

```php
RecordDelivery::dispatch($order)->onConnection('deferred');
```

A conexão `deferred` também serve como a [fila de failover](#queue-failover) padrão.

De forma semelhante, a conexão `background` processa jobs depois que a resposta HTTP foi enviada ao usuário; no entanto, o job é processado em um processo PHP gerado separadamente, permitindo que o PHP-FPM / worker da aplicação fique disponível para tratar outra requisição HTTP recebida:

```php
RecordDelivery::dispatch($order)->onConnection('background');
```

<a id="bulk-dispatching"></a>
### Despacho em Massa

Se você precisar despachar muitos jobs independentes de uma só vez e não precisar de rastreamento de [lotes](#job-batching) ou callbacks, pode usar o método `bulk` da facade `Bus`. O Laravel agrupará os jobs por conexão de fila e nome de fila configurados e enviará cada grupo para a fila apropriada em massa:

```php
use App\Jobs\ProcessUser;
use Illuminate\Support\Facades\Bus;

Bus::bulk(
    $users->map(fn ($user) => new ProcessUser($user))
);
```

<a id="preparing-jobs-before-dispatch"></a>
### Preparando Jobs Antes do Despacho

Se um job precisar preparar ou inspecionar seu estado antes de ser enviado para a fila, ele pode implementar a interface `Illuminate\Contracts\Queue\PreparesForDispatch`. O Laravel invocará o método `prepareForDispatch` do job antes de despachá-lo. Se este método retornar `false`, o job não será despachado:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\PreparesForDispatch;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Support\Facades\Cache;

class SyncPodcasts implements PreparesForDispatch, ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public array $podcastIds,
    ) {}

    /**
     * Prepare the job before dispatching.
     */
    public function prepareForDispatch(): bool
    {
        return collect($this->podcastIds)
            ->reject(fn (int $id) => Cache::has("podcast-syncing:{$id}"))
            ->isNotEmpty();
    }
}
```

<a id="jobs-and-database-transactions"></a>
### Jobs e Transações de Banco de Dados

Embora seja perfeitamente aceitável despachar jobs dentro de transações de banco de dados, você deve tomar cuidado especial para garantir que seu job realmente consiga ser executado com sucesso. Ao despachar um job dentro de uma transação, é possível que o job seja processado por um worker antes que a transação pai tenha sido confirmada (commit). Quando isso acontece, quaisquer atualizações que você tenha feito em models ou registros do banco de dados durante a(s) transação(ões) podem ainda não estar refletidas no banco de dados. Além disso, quaisquer models ou registros criados dentro da(s) transação(ões) podem não existir no banco de dados.

Felizmente, o Laravel oferece vários métodos para contornar esse problema. Primeiro, você pode definir a opção de conexão `after_commit` no array de configuração da sua conexão de fila:

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

Quando a opção `after_commit` é `true`, você pode despachar jobs dentro de transações de banco de dados; no entanto, o Laravel aguardará até que as transações de banco de dados pai abertas sejam confirmadas antes de realmente despachar o job. Naturalmente, se nenhuma transação de banco de dados estiver aberta no momento, o job será despachado imediatamente.

Se uma transação for revertida (rollback) devido a uma exceção ocorrida durante a transação, os jobs que foram despachados durante essa transação serão descartados.

> **Nota:**
> Definir a opção de configuração `after_commit` como `true` também fará com que quaisquer listeners de eventos enfileirados, mailables, notificações e eventos de broadcast sejam despachados somente após todas as transações de banco de dados abertas terem sido confirmadas.

<a id="specifying-commit-dispatch-behavior-inline"></a>
#### Especificando o Comportamento de Despacho Após o Commit em Linha

Se você não definir a opção de configuração de conexão de fila `after_commit` como `true`, ainda poderá indicar que um job específico deve ser despachado após todas as transações de banco de dados abertas terem sido confirmadas. Para isso, você pode encadear o método `afterCommit` na sua operação de despacho:

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

Da mesma forma, se a opção de configuração `after_commit` estiver definida como `true`, você pode indicar que um job específico deve ser despachado imediatamente, sem aguardar a confirmação de quaisquer transações de banco de dados abertas:

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a id="job-chaining"></a>
### Encadeamento de Jobs

O encadeamento de jobs permite especificar uma lista de jobs enfileirados que devem ser executados em sequência após o job principal ter sido executado com sucesso. Se um job na sequência falhar, os demais jobs não serão executados. Para executar uma cadeia de jobs enfileirados, você pode usar o método `chain` fornecido pela facade `Bus`. O barramento de comandos (command bus) do Laravel é um componente de nível mais baixo sobre o qual o despacho de jobs enfileirados é construído:

```php
use App\Jobs\OptimizePodcast;
use App\Jobs\ProcessPodcast;
use App\Jobs\ReleasePodcast;
use Illuminate\Support\Facades\Bus;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->dispatch();
```

Além de encadear instâncias de classes de job, você também pode encadear closures:

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    function () {
        Podcast::update(/* ... */);
    },
])->dispatch();
```

> **Aviso:**
> Excluir jobs usando o método `$this->delete()` dentro do job não impedirá que os jobs encadeados sejam processados. A cadeia só deixará de ser executada se um job nela falhar.

<a id="chain-connection-queue"></a>
#### Conexão e Fila da Cadeia

Se você quiser especificar a conexão e a fila que devem ser usadas para os jobs encadeados, pode usar os métodos `onConnection` e `onQueue`. Esses métodos especificam a conexão de fila e o nome da fila que devem ser usados, a menos que o job enfileirado seja explicitamente atribuído a outra conexão / fila:

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a id="adding-jobs-to-the-chain"></a>
#### Adicionando Jobs à Cadeia

Ocasionalmente, pode ser necessário inserir no início ou acrescentar ao final um job em uma cadeia de jobs existente a partir de outro job dessa mesma cadeia. Você pode fazer isso usando os métodos `prependToChain` e `appendToChain`:

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    // ...

    // Prepend to the current chain, run job immediately after current job...
    $this->prependToChain(new TranscribePodcast);

    // Append to the current chain, run job at end of chain...
    $this->appendToChain(new TranscribePodcast);
}
```

<a id="chain-failures"></a>
#### Falhas na Cadeia

Ao encadear jobs, você pode usar o método `catch` para especificar um closure que deve ser invocado caso um job dentro da cadeia falhe. O callback fornecido receberá a instância de `Throwable` que causou a falha do job:

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // A job within the chain has failed...
})->dispatch();
```

> **Aviso:**
> Como os callbacks de cadeia são serializados e executados posteriormente pela fila do Laravel, você não deve usar a variável `$this` dentro de callbacks de cadeia.

<a id="customizing-the-queue-and-connection"></a>
### Personalizando a Fila e a Conexão

<a id="dispatching-to-a-particular-queue"></a>
#### Despachando para uma Fila Específica

Ao enviar jobs para diferentes filas, você pode "categorizar" seus jobs enfileirados e até priorizar quantos workers atribuir a cada fila. Lembre-se de que isso não envia jobs para diferentes "conexões" de fila definidas no arquivo de configuração da fila, mas apenas para filas específicas dentro de uma única conexão. Para especificar a fila, use o método `onQueue` ao despachar o job:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onQueue('processing');

        return redirect('/podcasts');
    }
}
```

Alternativamente, você pode especificar a fila do job chamando o método `onQueue` dentro do construtor do job:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a id="dispatching-to-a-particular-connection"></a>
#### Despachando para uma Conexão Específica

Se sua aplicação interage com várias conexões de fila, você pode especificar em qual conexão enviar um job usando o método `onConnection`:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');

        return redirect('/podcasts');
    }
}
```

Você pode encadear os métodos `onConnection` e `onQueue` para especificar a conexão e a fila de um job:

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

Alternativamente, você pode especificar a conexão do job chamando o método `onConnection` dentro do construtor do job:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a id="queue-routing"></a>
#### Roteamento de Filas

Você pode usar o método `route` da facade `Queue` para definir uma conexão e uma fila padrão para classes de job específicas. Isso é útil quando você quer garantir que determinados jobs sempre usem filas específicas, sem precisar especificar a conexão ou a fila no próprio job.

Além de rotear classes de job específicas, você também pode passar uma interface, uma trait ou uma classe pai para o método `route`. Quando você faz isso, qualquer job que implemente a interface, use a trait ou estenda a classe pai utilizará automaticamente a conexão e a fila configuradas.

Tipicamente, você deve chamar o método `route` a partir do método `boot` de um service provider:

```php
use App\Concerns\RequiresVideo;
use App\Jobs\ProcessPodcast;
use App\Jobs\ProcessVideo;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Support\Facades\Queue;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Queue::route(ProcessPodcast::class, connection: 'redis', queue: 'podcasts');
    Queue::route(RequiresVideo::class, queue: 'video');
    Queue::route(ShouldBroadcast::class, queue: 'events');
}
```

Quando uma conexão é especificada sem uma fila, o job será enviado para a fila padrão:

```php
Queue::route(ProcessPodcast::class, connection: 'redis');
```

Você também pode rotear várias classes de job de uma só vez passando um array ao método `route`:

```php
Queue::route([
    ProcessPodcast::class => ['redis', 'podcasts'], // Connection and queue
    ProcessVideo::class => 'videos', // Queue only (uses default connection)
]);
```

> **Nota:**
> O roteamento de filas ainda pode ser sobrescrito pelo job, job a job.

Você pode usar o método `forward` para encaminhar jobs de uma fila para outra fila e / ou conexão. Isso é útil quando você precisa mudar a infraestrutura de filas sem modificar jobs individuais ou os locais de despacho:

```php
Queue::forward('reports', 'reports.fifo', 'sqs');
Queue::forward('payments', connection: 'sqs');
Queue::forward('updates', 'notifications');
```

Você também pode encaminhar várias filas de uma só vez passando um array:

```php
Queue::forward([
    'reports' => 'reports.fifo',
    'emails' => 'emails.fifo',
], connection: 'sqs');
```

Uma conexão explícita configurada em um job tem precedência sobre uma conexão encaminhada.

<a id="max-job-attempts-and-timeout"></a>
### Especificando Número Máximo de Tentativas / Valores de Timeout

<a id="max-attempts"></a>
#### Número Máximo de Tentativas

As tentativas de job são um conceito central do sistema de filas do Laravel e sustentam muitos recursos avançados. Embora possam parecer confusas à primeira vista, é importante entender como funcionam antes de modificar a configuração padrão.

Quando um job é despachado, ele é enviado para a fila. Um worker então o pega e tenta executá-lo. Isso é uma tentativa de job.

No entanto, uma tentativa não significa necessariamente que o método `handle` do job foi executado. As tentativas também podem ser "consumidas" de várias maneiras:

<div class="content-list" markdown="1">

- O job encontra uma exceção não tratada durante a execução.
- O job é liberado manualmente de volta para a fila usando `$this->release()`.
- Um middleware como `WithoutOverlapping` ou `RateLimited` não consegue adquirir um lock e libera o job.
- O job sofreu timeout.
- O método `handle` do job é executado e concluído sem lançar uma exceção.

</div>

Provavelmente você não quer continuar tentando um job indefinidamente. Por isso, o Laravel oferece várias formas de especificar quantas vezes ou por quanto tempo um job pode ser tentado.

> **Nota:**
> Por padrão, o Laravel tentará executar um job apenas uma vez. Se seu job usar middleware como `WithoutOverlapping` ou `RateLimited`, ou se você estiver liberando jobs manualmente, provavelmente precisará aumentar o número de tentativas permitidas por meio da opção `tries`.

Uma abordagem para especificar o número máximo de vezes que um job pode ser tentado é usar a opção `--tries` na linha de comando do Artisan. Isso se aplicará a todos os jobs processados pelo worker, a menos que o job que está sendo processado especifique quantas vezes pode ser tentado:

```shell
php artisan queue:work --tries=3
```

Se um job exceder seu número máximo de tentativas, ele será considerado um job "falho". Para mais informações sobre como lidar com jobs falhos, consulte a [documentação de jobs falhos](#dealing-with-failed-jobs). Se `--tries=0` for informado ao comando `queue:work`, o job será tentado novamente indefinidamente.

Você pode adotar uma abordagem mais granular definindo o número máximo de vezes que um job pode ser tentado na própria classe do job, usando o atributo `Tries`. Se o número máximo de tentativas for especificado no job, ele terá precedência sobre o valor `--tries` informado na linha de comando:

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\Tries;

#[Tries(5)]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

Se você precisar de controle dinâmico sobre o número máximo de tentativas de um job específico, pode definir um método `tries` no job:

```php
/**
 * Determine number of times the job may be attempted.
 */
public function tries(): int
{
    return 5;
}
```

<a id="time-based-attempts"></a>
#### Tentativas Baseadas em Tempo

Como alternativa a definir quantas vezes um job pode ser tentado antes de falhar, você pode definir um momento a partir do qual o job não deve mais ser tentado. Isso permite que um job seja tentado quantas vezes forem necessárias dentro de um determinado intervalo de tempo. Para definir o momento em que um job não deve mais ser tentado, adicione um método `retryUntil` à sua classe de job. Este método deve retornar uma instância de `DateTime`:

```php
use DateTime;

/**
 * Determine the time at which the job should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 10);
}
```

Se os métodos `retryUntil` e `tries` forem ambos definidos, o Laravel dará precedência ao método `retryUntil`.

> **Nota:**
> Você também pode definir um atributo `Tries` ou um método `retryUntil` em seus [listeners de eventos enfileirados](/en/events/#queued-event-listeners) e [notificações enfileiradas](/en/notifications/#queueing-notifications).

<a id="max-exceptions"></a>
#### Máximo de Exceções

Às vezes, você pode querer especificar que um job pode ser tentado muitas vezes, mas que deve falhar se as novas tentativas forem acionadas por um determinado número de exceções não tratadas (em vez de ser liberado diretamente pelo método `release`). Para isso, você pode usar os atributos `Tries` e `MaxExceptions` na sua classe de job:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\MaxExceptions;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Support\Facades\Redis;

#[Tries(25)]
#[MaxExceptions(3)]
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        Redis::throttle('key')->allow(10)->every(60)->then(function () {
            // Lock obtained, process the podcast...
        }, function () {
            // Unable to obtain lock...
            return $this->release(10);
        });
    }
}
```

Neste exemplo, o job é liberado por dez segundos caso a aplicação não consiga obter um lock do Redis e continuará sendo tentado até 25 vezes. No entanto, o job falhará se três exceções não tratadas forem lançadas por ele.

Por padrão, uma tentativa que termina porque o processo do worker travou ou foi encerrado, como quando fica sem memória, não conta para o número máximo de exceções do job. Se você quiser que essas tentativas contem como exceção, pode adicionar o atributo `CountCrashesAsExceptions` à sua classe de job:

```php
use Illuminate\Queue\Attributes\CountCrashesAsExceptions;
use Illuminate\Queue\Attributes\MaxExceptions;
use Illuminate\Queue\Attributes\Tries;

#[Tries(25)]
#[MaxExceptions(3)]
#[CountCrashesAsExceptions]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

Quando este atributo está presente, o worker armazena um marcador no cache da sua aplicação enquanto o job está sendo processado. Se o marcador ainda existir quando o job for tentado novamente, a tentativa anterior será contabilizada como uma exceção.

<a id="stopping-retries-by-exception"></a>
#### Interrompendo Novas Tentativas por Exceção

Às vezes, uma exceção indica que um job enfileirado deve falhar imediatamente, em vez de ser liberado para outra tentativa. Você pode configurar os tipos de exceção que devem interromper as novas tentativas de um job usando o método de exceção `dontRetry` no arquivo `bootstrap/app.php` da sua aplicação:

```php
use App\Exceptions\InvalidPodcastSourceException;
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontRetry([
        InvalidPodcastSourceException::class,
    ]);
})
```

Se você precisar de mais controle sobre quando as novas tentativas devem parar, pode fornecer um closure ao método `dontRetryWhen`. Quando o closure retornar `true`, o job será marcado como falho e não será tentado novamente:

```php
use App\Exceptions\PodcastProcessingException;
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontRetryWhen(function (PodcastProcessingException $e) {
        return $e->reason() === 'Subscription expired';
    });
})
```

<a id="timeout"></a>
#### Timeout

Muitas vezes, você sabe mais ou menos quanto tempo espera que seus jobs enfileirados levem para ser concluídos. Por esse motivo, o Laravel permite especificar um valor de "timeout". Por padrão, o valor de timeout é de 60 segundos. Se um job estiver sendo processado por mais tempo do que o número de segundos especificado pelo valor de timeout, o worker que processa o job será encerrado com um erro. Tipicamente, o worker será reiniciado automaticamente por um [gerenciador de processos configurado no seu servidor](#supervisor-configuration).

O número máximo de segundos que os jobs podem executar pode ser especificado usando a opção `--timeout` na linha de comando do Artisan:

```shell
php artisan queue:work --timeout=30
```

Se o job exceder seu número máximo de tentativas por sofrer timeouts sucessivos, ele será marcado como falho.

Você também pode definir o número máximo de segundos que um job deve ter permissão para executar usando o atributo `Timeout` na classe do job. Se o timeout for especificado no job, ele terá precedência sobre qualquer timeout informado na linha de comando:

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\Timeout;

#[Timeout(120)]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

Às vezes, processos com bloqueio de IO, como sockets ou conexões HTTP de saída, podem não respeitar o timeout especificado. Por isso, ao usar esses recursos, você deve sempre tentar especificar um timeout também pelas suas próprias APIs. Por exemplo, ao usar o [Guzzle](https://docs.guzzlephp.org), você deve sempre especificar um valor de timeout de conexão e de requisição.

> **Aviso:**
> A extensão PHP [PCNTL](https://www.php.net/manual/en/book.pcntl.php) deve estar instalada para que seja possível especificar timeouts de jobs. Além disso, o valor de "timeout" de um job deve sempre ser menor que seu valor de ["retry after"](#job-expiration). Caso contrário, o job pode ser tentado novamente antes de realmente ter terminado de executar ou sofrer timeout. A opção `--timeout` não tem efeito quando o comando `queue:work` é invocado com a opção `--once`.

<a id="failing-on-timeout"></a>
#### Falhando por Timeout

Se você quiser indicar que um job deve ser marcado como [falho](#dealing-with-failed-jobs) em caso de timeout, pode usar o atributo `FailOnTimeout` na classe do job:

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\FailOnTimeout;

#[FailOnTimeout]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```

> **Nota:**
> Por padrão, quando um job sofre timeout, ele consome uma tentativa e é liberado de volta para a fila (se novas tentativas forem permitidas). No entanto, se você configurar o job para falhar em caso de timeout, ele não será tentado novamente, independentemente do valor definido em tries.

<a id="sqs-fifo-and-fair-queues"></a>
### SQS FIFO e Filas Justas

O Laravel oferece suporte às filas [Amazon SQS FIFO (First-In-First-Out)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fifo-queues.html) e [justas (fair)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fair-queues.html). Filas FIFO permitem processar os jobs exatamente na ordem em que foram enviados, garantindo processamento exatamente uma vez por meio da deduplicação de mensagens.

Filas FIFO exigem um ID de grupo de mensagens para determinar quais jobs podem ser processados em paralelo. Jobs com o mesmo ID de grupo são processados sequencialmente, enquanto mensagens com IDs de grupo diferentes podem ser processadas simultaneamente.

O Laravel oferece um método fluente `onGroup` para especificar o ID do grupo de mensagens ao despachar jobs:

```php
ProcessOrder::dispatch($order)
    ->onGroup("customer-{$order->customer_id}");
```

Se você despachar um job para uma fila FIFO do SQS sem especificar um grupo de mensagens, o Laravel usará o nome da fila como ID do grupo de mensagens.

Filas FIFO do SQS suportam deduplicação de mensagens para garantir processamento exatamente uma vez. Implemente um método `deduplicationId` na sua classe de job para fornecer um ID de deduplicação personalizado:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessSubscriptionRenewal implements ShouldQueue
{
    use Queueable;

    // ...

    /**
     * Get the job's deduplication ID.
     */
    public function deduplicationId(): string
    {
        return "renewal-{$this->subscription->id}";
    }
}
```

<a id="fair-queues"></a>
#### Filas Justas

Se você estiver usando uma fila padrão do SQS, definir um grupo de mensagens habilita o enfileiramento justo. Em outras palavras, depois que você atribui grupos, o SQS os utilizará para manter uma entrega justa entre tenants / cargas de trabalho. Nenhuma configuração adicional do Laravel é necessária.

Em vez de chamar `onGroup` no momento do despacho, você também pode definir um método `messageGroup` diretamente no job:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessOrder implements ShouldQueue
{
    use Queueable;

    // ...

    /**
     * Get the job's message group.
     */
    public function messageGroup(): string
    {
        return "customer-{$this->order->customer_id}";
    }
}
```

<a id="fifo-listeners-mail-and-notifications"></a>
#### Listeners, E-mails e Notificações em FIFO

Ao utilizar filas FIFO, você também precisará definir grupos de mensagens em listeners, e-mails e notificações. Alternativamente, você pode despachar instâncias enfileiradas desses objetos para uma fila não FIFO.

Para definir o grupo de mensagens de um [listener de evento enfileirado](/en/events/#queued-event-listeners), defina um método `messageGroup` no listener. Você também pode, opcionalmente, definir um método `deduplicator`, que recebe o evento e deve retornar um closure que gera o ID de deduplicação:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Closure;

class SendShipmentNotification
{
    // ...

    /**
     * Get the job's message group.
     */
    public function messageGroup(): string
    {
        return 'shipments';
    }

    /**
     * Get the job's deduplicator.
     */
    public function deduplicator(OrderShipped $event): Closure
    {
        return fn () => "shipment-notification-{$event->order->id}";
    }
}
```

Ao enviar uma [mensagem de e-mail](/en/mail/) que será enfileirada em uma fila FIFO, você deve invocar o método `onGroup` e, opcionalmente, o método `withDeduplicator` ao enviar a notificação:

```php
use App\Mail\InvoicePaid;
use Illuminate\Support\Facades\Mail;

$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

Mail::to($request->user())->send($invoicePaid);
```

Ao enviar uma [notificação](/en/notifications/) que será enfileirada em uma fila FIFO, você deve invocar o método `onGroup` e, opcionalmente, o método `withDeduplicator` ao enviar a notificação:

```php
use App\Notifications\InvoicePaid;

$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

$user->notify($invoicePaid);
```

<a id="queue-failover"></a>
### Failover de Fila

O driver de fila `failover` fornece uma funcionalidade de failover automático ao enviar jobs para a fila. Se a conexão de fila primária da configuração `failover` falhar por qualquer motivo, o Laravel tentará automaticamente enviar o job para a próxima conexão configurada na lista. Isso é especialmente útil para garantir alta disponibilidade em ambientes de produção, onde a confiabilidade da fila é crítica.

Para configurar uma conexão de fila de failover, especifique o driver `failover` e forneça um array com os nomes das conexões a serem tentadas, em ordem. Por padrão, o Laravel inclui um exemplo de configuração de failover no arquivo de configuração `config/queue.php` da sua aplicação:

```php
'failover' => [
    'driver' => 'failover',
    'connections' => [
        'redis',
        'database',
        'sync',
    ],
],
```

Depois de configurar uma conexão que usa o driver `failover`, você precisará definir a conexão de failover como sua conexão de fila padrão no arquivo `.env` da sua aplicação para utilizar a funcionalidade de failover:

```ini
QUEUE_CONNECTION=failover
```

Em seguida, inicie pelo menos um worker para cada conexão da lista de conexões de failover:

```shell
php artisan queue:work redis
php artisan queue:work database
```

> **Nota:**
> Você não precisa executar um worker para conexões que usam os drivers de fila `sync`, `background` ou `deferred`, já que esses drivers processam os jobs dentro do processo PHP atual.

Quando uma operação de conexão de fila falha e o failover é ativado, o Laravel despachará o evento `Illuminate\Queue\Events\QueueFailedOver`, permitindo que você reporte ou registre em log que uma conexão de fila falhou.

> **Nota:**
> Se você usar o Laravel Horizon, lembre-se de que o Horizon gerencia apenas filas Redis. Se sua lista de failover incluir `database`, você deve executar um processo `php artisan queue:work database` comum junto com o Horizon.

<a id="error-handling"></a>
### Tratamento de Erros

Se uma exceção for lançada enquanto o job está sendo processado, o job será automaticamente liberado de volta para a fila para que possa ser tentado novamente. O job continuará sendo liberado até ter sido tentado o número máximo de vezes permitido pela sua aplicação. O número máximo de tentativas é definido pela opção `--tries` usada no comando Artisan `queue:work`. Alternativamente, o número máximo de tentativas pode ser definido na própria classe do job. Mais informações sobre como executar o worker da fila [podem ser encontradas abaixo](#running-the-queue-worker).

<a id="manually-releasing-a-job"></a>
#### Liberando um Job Manualmente

Às vezes, você pode querer liberar manualmente um job de volta para a fila para que ele possa ser tentado novamente mais tarde. Você pode fazer isso chamando o método `release`:

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    // ...

    $this->release();
}
```

Por padrão, o método `release` liberará o job de volta para a fila para processamento imediato. No entanto, você pode instruir a fila a não disponibilizar o job para processamento até que um determinado número de segundos tenha decorrido, passando um inteiro ou uma instância de data para o método `release`:

```php
$this->release(10);

$this->release(now()->plus(seconds: 10));
```

<a id="manually-failing-a-job"></a>
#### Falhando um Job Manualmente

Ocasionalmente, pode ser necessário marcar manualmente um job como "falho". Para isso, você pode chamar o método `fail`:

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    // ...

    $this->fail();
}
```

Se você quiser marcar seu job como falho por causa de uma exceção que capturou, pode passar a exceção para o método `fail`. Ou, por conveniência, pode passar uma mensagem de erro em string, que será convertida em uma exceção para você:

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> **Nota:**
> Para mais informações sobre jobs falhos, consulte a [documentação sobre como lidar com falhas de jobs](#dealing-with-failed-jobs).

<a id="fail-jobs-on-exceptions"></a>
#### Falhando Jobs em Exceções Específicas

O [middleware de job](#job-middleware) `FailOnException` permite interromper novas tentativas quando exceções específicas são lançadas. Isso permite tentar novamente em exceções transitórias, como erros de APIs externas, mas falhar o job permanentemente em exceções persistentes, como quando as permissões de um usuário são revogadas:

```php
<?php

namespace App\Jobs;

use App\Models\User;
use Illuminate\Auth\Access\AuthorizationException;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Queue\Middleware\FailOnException;
use Illuminate\Support\Facades\Http;

#[Tries(3)]
class SyncChatHistory implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        $this->user->authorize('sync-chat-history');

        $response = Http::throw()->get(
            "https://chat.laravel.test/?user={$this->user->uuid}"
        );

        // ...
    }

    /**
     * Get the middleware the job should pass through.
     */
    public function middleware(): array
    {
        return [
            new FailOnException([AuthorizationException::class])
        ];
    }
}
```

<a id="job-batching"></a>
## Processamento em Lote de Jobs

O recurso de processamento em lote de jobs do Laravel permite executar facilmente um grupo de jobs em paralelo e, em seguida, realizar alguma ação quando o lote de jobs tiver terminado de executar.

Antes de começar, você deve criar uma migração de banco de dados para construir uma tabela que conterá metainformações sobre seus lotes de jobs, como seu percentual de conclusão. Essa migração pode ser gerada usando o comando Artisan `make:queue-batches-table`:

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a id="defining-batchable-jobs"></a>
### Definindo Jobs em Lote

Para definir um job que pode ser agrupado em lote, você deve [criar um job enfileirável](#creating-jobs) normalmente; no entanto, deve adicionar a trait `Illuminate\Bus\Batchable` à classe do job. Essa trait fornece acesso a um método `batch`, que pode ser usado para recuperar o lote atual no qual o job está sendo executado:

```php
<?php

namespace App\Jobs;

use Illuminate\Bus\Batchable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ImportCsv implements ShouldQueue
{
    use Batchable, Queueable;

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            // Determine if the batch has been cancelled...

            return;
        }

        // Import a portion of the CSV file...
    }
}
```

<a id="dispatching-batches"></a>
### Despachando Lotes

Para despachar um lote de jobs, você deve usar o método `batch` da facade `Bus`. Naturalmente, o processamento em lote é útil principalmente quando combinado com callbacks de conclusão. Assim, você pode usar os métodos `then`, `catch` e `finally` para definir callbacks de conclusão para o lote. Cada um desses callbacks receberá uma instância de `Illuminate\Bus\Batch` quando for invocado.

Ao executar vários workers de fila, os jobs do lote serão processados em paralelo. Portanto, a ordem em que os jobs terminam pode não ser a mesma ordem em que foram adicionados ao lote. Consulte nossa documentação sobre [encadeamentos e lotes de jobs](#chains-and-batches) para informações sobre como executar uma série de jobs em sequência.

Neste exemplo, vamos imaginar que estamos enfileirando um lote de jobs, em que cada um processa um determinado número de linhas de um arquivo CSV:

```php
use App\Jobs\ImportCsv;
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;
use Throwable;

$batch = Bus::batch([
    new ImportCsv(1, 100),
    new ImportCsv(101, 200),
    new ImportCsv(201, 300),
    new ImportCsv(301, 400),
    new ImportCsv(401, 500),
])->before(function (Batch $batch) {
    // The batch has been created but no jobs have been added...
})->progress(function (Batch $batch) {
    // A single job has completed successfully...
})->then(function (Batch $batch) {
    // All jobs completed successfully...
})->catch(function (Batch $batch, Throwable $e) {
    // Batch job failure detected...
})->finally(function (Batch $batch) {
    // The batch has finished executing...
})->dispatch();

return $batch->id;
```

O ID do lote, que pode ser acessado pela propriedade `$batch->id`, pode ser usado para [consultar o barramento de comandos do Laravel](#inspecting-batches) e obter informações sobre o lote após ele ter sido despachado.

> **Aviso:**
> Como os callbacks de lote são serializados e executados posteriormente pela fila do Laravel, você não deve usar a variável `$this` dentro dos callbacks. Além disso, como os jobs em lote são envolvidos por transações de banco de dados, instruções de banco de dados que disparam commits implícitos não devem ser executadas dentro dos jobs.

<a id="naming-batches"></a>
#### Nomeando Lotes

Algumas ferramentas, como o [Laravel Horizon](/en/horizon/) e o [Laravel Telescope](/en/telescope/), podem fornecer informações de depuração mais amigáveis para os lotes se eles forem nomeados. Para atribuir um nome arbitrário a um lote, você pode chamar o método `name` ao definir o lote:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->name('Import CSV')->dispatch();
```

<a id="batch-connection-queue"></a>
#### Conexão e Fila do Lote

Se você quiser especificar a conexão e a fila que devem ser usadas para os jobs em lote, pode usar os métodos `onConnection` e `onQueue`. Todos os jobs em lote devem ser executados na mesma conexão e fila:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a id="chains-and-batches"></a>
### Encadeamentos e Lotes

Você pode definir um conjunto de [jobs encadeados](#job-chaining) dentro de um lote colocando os jobs encadeados dentro de um array. Por exemplo, podemos executar duas cadeias de jobs em paralelo e executar um callback quando ambas as cadeias de jobs tiverem terminado de ser processadas:

```php
use App\Jobs\ReleasePodcast;
use App\Jobs\SendPodcastReleaseNotification;
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;

Bus::batch([
    [
        new ReleasePodcast(1),
        new SendPodcastReleaseNotification(1),
    ],
    [
        new ReleasePodcast(2),
        new SendPodcastReleaseNotification(2),
    ],
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->dispatch();
```

Inversamente, você pode executar lotes de jobs dentro de uma [cadeia](#job-chaining) definindo lotes dentro da cadeia. Por exemplo, você poderia primeiro executar um lote de jobs para liberar vários podcasts e depois um lote de jobs para enviar as notificações de lançamento:

```php
use App\Jobs\FlushPodcastCache;
use App\Jobs\ReleasePodcast;
use App\Jobs\SendPodcastReleaseNotification;
use Illuminate\Support\Facades\Bus;

Bus::chain([
    new FlushPodcastCache,
    Bus::batch([
        new ReleasePodcast(1),
        new ReleasePodcast(2),
    ]),
    Bus::batch([
        new SendPodcastReleaseNotification(1),
        new SendPodcastReleaseNotification(2),
    ]),
])->dispatch();
```

<a id="adding-jobs-to-batches"></a>
### Adicionando Jobs a Lotes

Às vezes, pode ser útil adicionar jobs adicionais a um lote a partir de dentro de um job em lote. Este padrão pode ser útil quando você precisa colocar em lote milhares de jobs, cujo despacho durante uma requisição web levaria tempo demais. Assim, em vez disso, você pode querer despachar um lote inicial de jobs "carregadores" que preenchem o lote com ainda mais jobs:

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->name('Import Contacts')->dispatch();
```

Neste exemplo, usaremos o job `LoadImportBatch` para preencher o lote com jobs adicionais. Para isso, podemos usar o método `add` na instância do lote, que pode ser acessada pelo método `batch` do job:

```php
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * Execute the job.
 */
public function handle(): void
{
    if ($this->batch()->cancelled()) {
        return;
    }

    $this->batch()->add(Collection::times(1000, function () {
        return new ImportContacts;
    }));
}
```

> **Aviso:**
> Você só pode adicionar jobs a um lote a partir de dentro de um job que pertença ao mesmo lote.

<a id="inspecting-batches"></a>
### Inspecionando Lotes

A instância `Illuminate\Bus\Batch` fornecida aos callbacks de conclusão do lote possui uma variedade de propriedades e métodos para ajudá-lo a interagir e inspecionar um determinado lote de jobs:

```php
// The UUID of the batch...
$batch->id;

// The name of the batch (if applicable)...
$batch->name;

// The number of jobs assigned to the batch...
$batch->totalJobs;

// The number of jobs that have not been processed by the queue...
$batch->pendingJobs;

// The number of jobs that have failed...
$batch->failedJobs;

// The number of jobs that have been processed thus far...
$batch->processedJobs();

// The completion percentage of the batch (0-100)...
$batch->progress();

// Indicates if the batch has finished executing...
$batch->finished();

// Cancel the execution of the batch...
$batch->cancel();

// Indicates if the batch has been cancelled...
$batch->cancelled();
```

<a id="returning-batches-from-routes"></a>
#### Retornando Lotes a Partir de Rotas

Todas as instâncias de `Illuminate\Bus\Batch` são serializáveis em JSON, o que significa que você pode retorná-las diretamente de uma das rotas da sua aplicação para obter um payload JSON contendo informações sobre o lote, incluindo seu progresso de conclusão. Isso facilita exibir informações sobre o progresso de conclusão do lote na interface da sua aplicação.

Para recuperar um lote pelo seu ID, você pode usar o método `findBatch` da facade `Bus`:

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a id="cancelling-batches"></a>
### Cancelando Lotes

Às vezes, você pode precisar cancelar a execução de um determinado lote. Isso pode ser feito chamando o método `cancel` na instância `Illuminate\Bus\Batch`:

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    if ($this->user->exceedsImportLimit()) {
        $this->batch()->cancel();

        return;
    }

    if ($this->batch()->cancelled()) {
        return;
    }
}
```

Como você deve ter notado nos exemplos anteriores, jobs em lote normalmente devem verificar se o lote correspondente foi cancelado antes de continuar a execução. No entanto, por conveniência, você pode atribuir o [middleware](#job-middleware) `SkipIfBatchCancelled` ao job. Como o nome indica, este middleware instruirá o Laravel a não processar o job se o lote correspondente tiver sido cancelado:

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a id="batch-failures"></a>
### Falhas em Lotes

Quando um job em lote falha, o callback `catch` (se atribuído) será invocado. Este callback é invocado apenas para o primeiro job que falha dentro do lote.

<a id="allowing-failures"></a>
#### Permitindo Falhas

Quando um job dentro de um lote falha, o Laravel marca automaticamente o lote como "cancelado". Se desejar, você pode desabilitar esse comportamento para que a falha de um job não marque automaticamente o lote como cancelado. Isso pode ser feito chamando o método `allowFailures` ao despachar o lote:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->allowFailures()->dispatch();
```

Opcionalmente, você pode fornecer um closure ao método `allowFailures`, que será executado a cada falha de job:

```php
$batch = Bus::batch([
    // ...
])->allowFailures(function (Batch $batch, $exception) {
    // Handle individual job failures...
})->dispatch();
```

<a id="retrying-failed-batch-jobs"></a>
#### Reexecutando Jobs em Lote Falhos

Por conveniência, o Laravel fornece um comando Artisan `queue:retry-batch` que permite reexecutar facilmente todos os jobs falhos de um determinado lote. Este comando aceita o UUID do lote cujos jobs falhos devem ser reexecutados:

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a id="pruning-batches"></a>
### Podando Lotes

Sem a poda, a tabela `job_batches` pode acumular registros muito rapidamente. Para mitigar isso, você deve [agendar](/en/scheduling/) o comando Artisan `queue:prune-batches` para ser executado diariamente:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

Por padrão, todos os lotes finalizados que tenham mais de 24 horas serão podados. Você pode usar a opção `hours` ao chamar o comando para determinar por quanto tempo os dados dos lotes devem ser retidos. Por exemplo, o comando a seguir excluirá todos os lotes que foram finalizados há mais de 48 horas:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

Às vezes, sua tabela `job_batches` pode acumular registros de lotes que nunca foram concluídos com sucesso, como lotes em que um job falhou e esse job nunca foi reexecutado com sucesso. Você pode instruir o comando `queue:prune-batches` a podar esses registros de lotes não finalizados usando a opção `unfinished`:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

Da mesma forma, sua tabela `job_batches` também pode acumular registros de lotes cancelados. Você pode instruir o comando `queue:prune-batches` a podar esses registros de lotes cancelados usando a opção `cancelled`:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a id="storing-batches-in-dynamodb"></a>
### Armazenando Lotes no DynamoDB

O Laravel também oferece suporte ao armazenamento de metainformações de lotes no [DynamoDB](https://aws.amazon.com/dynamodb) em vez de em um banco de dados relacional. No entanto, você precisará criar manualmente uma tabela no DynamoDB para armazenar todos os registros de lotes.

Tipicamente, esta tabela deve se chamar `job_batches`, mas você deve nomeá-la com base no valor do item de configuração `queue.batching.table` dentro do arquivo de configuração `queue` da sua aplicação.

<a id="dynamodb-batch-table-configuration"></a>
#### Configuração da Tabela de Lotes no DynamoDB

A tabela `job_batches` deve ter uma chave de partição primária do tipo string chamada `application` e uma chave de classificação primária do tipo string chamada `id`. A parte `application` da chave conterá o nome da sua aplicação, conforme definido pelo valor de configuração `name` dentro do arquivo de configuração `app` da sua aplicação. Como o nome da aplicação faz parte da chave da tabela do DynamoDB, você pode usar a mesma tabela para armazenar lotes de jobs de múltiplas aplicações Laravel.

Além disso, você pode definir um atributo `ttl` para sua tabela se quiser aproveitar a [poda automática de lotes](#pruning-batches-in-dynamodb).

<a id="dynamodb-configuration"></a>
#### Configuração do DynamoDB

Em seguida, instale o AWS SDK para que sua aplicação Laravel possa se comunicar com o Amazon DynamoDB:

```shell
composer require aws/aws-sdk-php
```

Depois, defina o valor da opção de configuração `queue.batching.driver` como `dynamodb`. Além disso, você deve definir as opções de configuração `key`, `secret` e `region` dentro do array de configuração `batching`. Essas opções serão usadas para autenticação na AWS. Ao usar o driver `dynamodb`, a opção de configuração `queue.batching.database` é desnecessária:

```php
'batching' => [
    'driver' => env('QUEUE_BATCHING_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
],
```

<a id="pruning-batches-in-dynamodb"></a>
#### Podando Lotes no DynamoDB

Ao utilizar o [DynamoDB](https://aws.amazon.com/dynamodb) para armazenar informações de lotes de jobs, os comandos típicos de poda usados para podar lotes armazenados em um banco de dados relacional não funcionarão. Em vez disso, você pode utilizar a [funcionalidade nativa de TTL do DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) para remover automaticamente os registros de lotes antigos.

Se você tiver definido sua tabela do DynamoDB com um atributo `ttl`, pode definir parâmetros de configuração para instruir o Laravel a respeito de como podar os registros de lotes. O valor de configuração `queue.batching.ttl_attribute` define o nome do atributo que armazena o TTL, enquanto o valor de configuração `queue.batching.ttl` define o número de segundos após os quais um registro de lote pode ser removido da tabela do DynamoDB, em relação à última vez em que o registro foi atualizado:

```php
'batching' => [
    'driver' => env('QUEUE_BATCHING_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
    'ttl_attribute' => 'ttl',
    'ttl' => 60 * 60 * 24 * 7, // 7 days...
],
```

<a id="queueing-closures"></a>
## Enfileirando Closures

Em vez de despachar uma classe de job para a fila, você também pode despachar um closure. Isso é ótimo para tarefas rápidas e simples que precisam ser executadas fora do ciclo da requisição atual. Ao despachar closures para a fila, o conteúdo de código do closure é assinado criptograficamente para que não possa ser modificado em trânsito:

```php
use App\Models\Podcast;

$podcast = Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

Para atribuir um nome ao closure enfileirado, que pode ser usado por painéis de monitoramento de filas e também exibido pelo comando `queue:work`, você pode usar o método `name`:

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

Usando o método `catch`, você pode fornecer um closure que deve ser executado se o closure enfileirado não for concluído com sucesso após esgotar todas as [tentativas de retry configuradas](#max-job-attempts-and-timeout) da sua fila:

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // This job has failed...
});
```

> **Aviso:**
> Como os callbacks `catch` são serializados e executados posteriormente pela fila do Laravel, você não deve usar a variável `$this` dentro dos callbacks `catch`.

<a id="running-the-queue-worker"></a>
## Executando o Worker da Fila

<a id="the-queue-work-command"></a>
### O Comando `queue:work`

O Laravel inclui um comando Artisan que inicia um worker de fila e processa novos jobs à medida que são enviados para a fila. Você pode executar o worker usando o comando Artisan `queue:work`. Observe que, depois que o comando `queue:work` é iniciado, ele continuará em execução até ser interrompido manualmente ou até você fechar o terminal:

```shell
php artisan queue:work
```

> **Nota:**
> Para manter o processo `queue:work` executando permanentemente em segundo plano, você deve usar um monitor de processos como o [Supervisor](#supervisor-configuration) para garantir que o worker de fila não pare de executar.

Você pode incluir a flag `-v` ao invocar o comando `queue:work` se quiser que os IDs dos jobs processados, os nomes das conexões e os nomes das filas sejam incluídos na saída do comando:

```shell
php artisan queue:work -v
```

Lembre-se de que os workers de fila são processos de longa duração e armazenam o estado da aplicação inicializada na memória. Como resultado, eles não perceberão alterações na sua base de código depois de iniciados. Portanto, durante o processo de deploy, certifique-se de [reiniciar seus workers de fila](#queue-workers-and-deployment). Além disso, lembre-se de que qualquer estado estático criado ou modificado pela sua aplicação não será redefinido automaticamente entre os jobs.

Alternativamente, você pode executar o comando `queue:listen`. Ao usar o comando `queue:listen`, você não precisa reiniciar manualmente o worker quando quiser recarregar seu código atualizado ou redefinir o estado da aplicação; porém, este comando é significativamente menos eficiente do que o comando `queue:work`:

```shell
php artisan queue:listen
```

<a id="running-multiple-queue-workers"></a>
#### Executando Múltiplos Workers de Fila

Para atribuir múltiplos workers a uma fila e processar jobs simultaneamente, basta iniciar vários processos `queue:work`. Isso pode ser feito localmente por meio de várias abas no seu terminal ou, em produção, usando as configurações do seu gerenciador de processos. [Ao usar o Supervisor](#supervisor-configuration), você pode usar o valor de configuração `numprocs`.

<a id="specifying-the-connection-queue"></a>
#### Especificando a Conexão e a Fila

Você também pode especificar qual conexão de fila o worker deve utilizar. O nome da conexão passado ao comando `work` deve corresponder a uma das conexões definidas no seu arquivo de configuração `config/queue.php`:

```shell
php artisan queue:work redis
```

Por padrão, o comando `queue:work` processa apenas os jobs da fila padrão de uma determinada conexão. No entanto, você pode personalizar ainda mais o seu worker de fila processando apenas filas específicas de uma determinada conexão. Por exemplo, se todos os seus e-mails forem processados em uma fila `emails` na sua conexão de fila `redis`, você pode executar o seguinte comando para iniciar um worker que processe apenas essa fila:

```shell
php artisan queue:work redis --queue=emails
```

<a id="processing-a-specified-number-of-jobs"></a>
#### Processando um Número Específico de Jobs

A opção `--once` pode ser usada para instruir o worker a processar apenas um único job da fila:

```shell
php artisan queue:work --once
```

A opção `--max-jobs` pode ser usada para instruir o worker a processar o número de jobs informado e então encerrar. Essa opção pode ser útil combinada com o [Supervisor](#supervisor-configuration), para que seus workers sejam reiniciados automaticamente após processar um determinado número de jobs, liberando qualquer memória que tenham acumulado:

```shell
php artisan queue:work --max-jobs=1000
```

<a id="processing-all-queued-jobs-then-exiting"></a>
#### Processando Todos os Jobs Enfileirados e Depois Encerrando

A opção `--stop-when-empty` pode ser usada para instruir o worker a processar todos os jobs e então encerrar de forma graciosa. Essa opção pode ser útil ao processar filas do Laravel dentro de um contêiner Docker, se você quiser desligar o contêiner após a fila estar vazia:

```shell
php artisan queue:work --stop-when-empty
```

<a id="processing-jobs-for-a-given-number-of-seconds"></a>
#### Processando Jobs Por um Determinado Número de Segundos

A opção `--max-time` pode ser usada para instruir o worker a processar jobs pelo número de segundos informado e então encerrar. Essa opção pode ser útil combinada com o [Supervisor](#supervisor-configuration), para que seus workers sejam reiniciados automaticamente após processar jobs por um determinado período, liberando qualquer memória que tenham acumulado:

```shell
# Process jobs for one hour and then exit...
php artisan queue:work --max-time=3600
```

<a id="worker-sleep-duration"></a>
#### Duração de Suspensão do Worker

Quando há jobs disponíveis na fila, o worker continuará processando jobs sem nenhum atraso entre eles. No entanto, a opção `sleep` determina por quantos segundos o worker ficará "em suspensão" se não houver jobs disponíveis. Naturalmente, enquanto estiver em suspensão, o worker não processará nenhum novo job:

```shell
php artisan queue:work --sleep=3
```

<a id="maintenance-mode-queues"></a>
#### Modo de Manutenção e Filas

Enquanto sua aplicação estiver em [modo de manutenção](/en/configuration/#maintenance-mode), nenhum job enfileirado será tratado. Os jobs continuarão sendo tratados normalmente assim que a aplicação sair do modo de manutenção.

Para forçar seus workers de fila a processar jobs mesmo que o modo de manutenção esteja habilitado, você pode usar a opção `--force`:

```shell
php artisan queue:work --force
```

<a id="resource-considerations"></a>
#### Considerações sobre Recursos

A opção `--memory` especifica o limite de memória em megabytes no qual o worker deve encerrar. Por padrão, esse limite é de 128 megabytes. Você também pode especificar uma porcentagem do `memory_limit` configurado do PHP:

```shell
php artisan queue:work --memory=60%
```

Limites baseados em porcentagem exigem um `memory_limit` finito no PHP. Se o limite de memória do PHP for ilimitado (`-1`), use um limite em megabytes. Um monitor de processos como o [Supervisor](#supervisor-configuration) pode reiniciar automaticamente o worker após ele encerrar.

Workers de fila daemon não "reinicializam" o framework antes de processar cada job. Portanto, você deve liberar quaisquer recursos pesados após a conclusão de cada job. Por exemplo, se você estiver fazendo [manipulação de imagens](/en/images/) com a [biblioteca GD](https://www.php.net/manual/en/book.image.php), deve liberar a memória com `imagedestroy` quando terminar de processar a imagem.

<a id="queue-priorities"></a>
### Prioridades de Fila

Às vezes, você pode querer priorizar a forma como suas filas são processadas. Por exemplo, no seu arquivo de configuração `config/queue.php`, você pode definir a `queue` padrão para sua conexão `redis` como `low`. No entanto, ocasionalmente você pode querer enviar um job para uma fila de alta prioridade, assim:

```php
dispatch((new Job)->onQueue('high'));
```

Para iniciar um worker que verifique se todos os jobs da fila `high` são processados antes de prosseguir para quaisquer jobs da fila `low`, passe uma lista de nomes de filas separada por vírgulas ao comando `work`:

```shell
php artisan queue:work --queue=high,low
```

<a id="queue-workers-and-deployment"></a>
### Workers de Fila e Deploy

Como os workers de fila são processos de longa duração, eles não perceberão alterações no seu código sem serem reiniciados. Assim, a forma mais simples de fazer deploy de uma aplicação que usa workers de fila é reiniciar os workers durante o processo de deploy. Você pode reiniciar todos os workers de forma graciosa executando o comando `queue:restart`:

```shell
php artisan queue:restart
```

Este comando instruirá todos os workers de fila a encerrarem graciosamente após terminarem de processar o job atual, para que nenhum job existente seja perdido. Como os workers de fila encerrarão quando o comando `queue:restart` for executado, você deve estar executando um gerenciador de processos como o [Supervisor](#supervisor-configuration) para reiniciar automaticamente os workers de fila.

> **Nota:**
> A fila usa o [cache](/en/cache/) para armazenar os sinais de reinicialização, portanto, verifique se um driver de cache está devidamente configurado para sua aplicação antes de usar este recurso.

<a id="reacting-to-worker-signals"></a>
### Reagindo a Sinais do Worker

Quando um worker de fila recebe um sinal de término, como `SIGQUIT`, `SIGTERM` ou `SIGINT` enquanto processa um job, o worker concluirá o job atual antes de encerrar. No entanto, seu job pode precisar reagir ao sinal antes que o processo seja interrompido pelo seu servidor ou orquestrador de contêineres. Por exemplo, um job de importação de longa duração pode precisar parar de buscar novos registros e salvar seu progresso atual.

Para reagir a sinais do worker de dentro de um job, implemente a interface `Illuminate\Contracts\Queue\Interruptible` e defina um método `interrupted` no seu job. O número do sinal recebido pelo worker será passado ao método `interrupted`:

```php
<?php

namespace App\Jobs;

use App\Models\Import;
use Illuminate\Contracts\Queue\Interruptible;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ImportProducts implements ShouldQueue, Interruptible
{
    use Queueable;

    protected bool $shouldStop = false;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Import $import,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        foreach ($this->import->pendingRows() as $row) {
            if ($this->shouldStop) {
                break;
            }

            // Import the product row...
        }

        $this->import->saveProgress();
    }

    /**
     * Handle a signal received by the queue worker.
     */
    public function interrupted(int $signal): void
    {
        $this->shouldStop = true;
    }
}
```

O método `interrupted` só é invocado quando o worker recebe um sinal de processo enquanto o job está em execução. Ele não substitui os [timeouts](#worker-timeouts) nem o [método `failed`](#cleaning-up-after-failed-jobs) do job.

<a id="job-expirations-and-timeouts"></a>
### Expiração e Timeouts de Jobs

<a id="job-expiration"></a>
#### Expiração de Jobs

No seu arquivo de configuração `config/queue.php`, cada conexão de fila define uma opção `retry_after`. Esta opção especifica quantos segundos a conexão de fila deve aguardar antes de tentar novamente um job que está sendo processado. Por exemplo, se o valor de `retry_after` for definido como `90`, o job será liberado de volta para a fila se estiver em processamento por 90 segundos sem ter sido liberado ou excluído. Tipicamente, você deve definir o valor de `retry_after` como o número máximo de segundos que seus jobs razoavelmente levam para ser concluídos.

> **Aviso:**
> A única conexão de fila que não contém um valor `retry_after` é o Amazon SQS. O SQS tentará novamente o job com base no [Default Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html), que é gerenciado no console da AWS.

<a id="worker-timeouts"></a>
#### Timeouts do Worker

O comando Artisan `queue:work` expõe uma opção `--timeout`. Por padrão, o valor de `--timeout` é de 60 segundos. Se um job estiver em processamento por mais tempo do que o número de segundos especificado pelo valor de timeout, o worker que processa o job será encerrado com um erro. Tipicamente, o worker será reiniciado automaticamente por um [gerenciador de processos configurado no seu servidor](#supervisor-configuration):

```shell
php artisan queue:work --timeout=60
```

A opção de configuração `retry_after` e a opção de CLI `--timeout` são diferentes, mas funcionam juntas para garantir que os jobs não sejam perdidos e que sejam processados com sucesso apenas uma vez.

> **Aviso:**
> O valor de `--timeout` deve sempre ser ao menos alguns segundos menor que o valor de configuração `retry_after`. Isso garantirá que um worker que esteja processando um job travado seja sempre encerrado antes que o job seja tentado novamente. Se a opção `--timeout` for maior que o valor de configuração `retry_after`, seus jobs poderão ser processados duas vezes.

<a id="pausing-and-resuming-queue-workers"></a>
### Pausando e Retomando Workers de Fila

Às vezes, você pode precisar impedir temporariamente que um worker de fila processe novos jobs sem interromper o worker por completo. Por exemplo, você pode querer pausar o processamento de jobs durante uma manutenção do sistema. O Laravel fornece os comandos Artisan `queue:pause` e `queue:continue` para pausar e retomar workers de fila.

Para pausar uma fila específica, informe o nome da conexão de fila e o nome da fila:

```shell
php artisan queue:pause database:default
```

Neste exemplo, `database` é o nome da conexão de fila e `default` é o nome da fila. Assim que uma fila for pausada, quaisquer workers que estejam processando jobs dessa fila continuarão concluindo o job atual, mas não pegarão nenhum novo job até que a fila seja retomada.

Para pausar o processamento de jobs de todas as filas em todas as conexões, use a opção `--all`:

```shell
php artisan queue:pause --all
```

Para retomar o processamento de jobs em uma fila pausada, use o comando `queue:continue`:

```shell
php artisan queue:continue database:default
```

Para retomar o processamento de jobs de todas as filas em todas as conexões, use a opção `--all` com o comando `queue:resume`:

```shell
php artisan queue:resume --all
```

Após retomar uma fila, os workers começarão a processar novos jobs dessa fila imediatamente. Retomar todas as filas não retoma as filas que foram pausadas individualmente. Observe que pausar uma fila não interrompe o processo do worker em si - apenas impede que o worker processe novos jobs da fila especificada.

<a id="worker-restart-and-pause-signals"></a>
#### Sinais de Reinicialização e Pausa do Worker

Por padrão, os workers de fila consultam o driver de cache em busca de sinais de reinicialização e pausa a cada iteração de job. Embora essa consulta seja essencial para responder aos comandos `queue:restart` e `queue:pause`, ela introduz uma pequena sobrecarga de desempenho.

Se você precisar otimizar o desempenho e não exigir esses recursos de interrupção, pode desabilitar globalmente essa consulta chamando o método `withoutInterruptionPolling` na facade `Queue`. Isso normalmente deve ser feito no método `boot` do seu `AppServiceProvider`:

```php
use Illuminate\Support\Facades\Queue;

/**
 * Bootstrap any application services.
 */
public function boot(): void
