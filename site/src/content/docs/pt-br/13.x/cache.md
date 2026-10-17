---
title: "Cache"
---

- [Introdução](#introduction)
- [Configuração](#configuration)
    - [Pré-requisitos do Driver](#driver-prerequisites)
- [Uso do Cache](#cache-usage)
    - [Obtendo uma Instância de Cache](#obtaining-a-cache-instance)
    - [Recuperando Itens do Cache](#retrieving-items-from-the-cache)
    - [Armazenando Itens no Cache](#storing-items-in-the-cache)
    - [Estendendo o Tempo de Vida do Item](#extending-item-lifetime)
    - [Removendo Itens do Cache](#removing-items-from-the-cache)
    - [Memoização de Cache](#cache-memoization)
    - [O Helper de Cache](#the-cache-helper)
- [Cache Tags](#cache-tags)
    - [Armazenando Itens de Cache com Tags](#storing-tagged-cache-items)
    - [Acessando Itens de Cache com Tags](#accessing-tagged-cache-items)
    - [Removendo Itens de Cache com Tags](#removing-tagged-cache-items)
- [Locks Atômicos](#atomic-locks)
    - [Gerenciando Locks](#managing-locks)
    - [Gerenciando Locks Entre Processos](#managing-locks-across-processes)
    - [Atualizando Locks](#refreshing-locks)
    - [Limitando Concorrência](#concurrency-limiting)
- [Failover de Cache](#cache-failover)
- [Adicionando Drivers de Cache Personalizados](#adding-custom-cache-drivers)
    - [Escrevendo o Driver](#writing-the-driver)
    - [Registrando o Driver](#registering-the-driver)
- [Eventos](#events)

<a id="introduction"></a>
## Introdução

Algumas das tarefas de recuperação ou processamento de dados realizadas pela sua aplicação podem ser intensivas de CPU ou levar vários segundos para serem concluídas. Quando este é o caso, é comum armazenar em cache os dados recuperados por um tempo para que possam ser recuperados rapidamente em requisições subsequentes para os mesmos dados. Os dados em cache são geralmente armazenados em um armazenamento de dados muito rápido como [Memcached](https://memcached.org) ou [Redis](https://redis.io).

Felizmente, o Laravel fornece uma API expressiva e unificada para vários backends de cache, permitindo que você aproveite a recuperação de dados ultrarrápida e acelere sua aplicação web.

<a id="configuration"></a>
## Configuração

O arquivo de configuração de cache da sua aplicação está localizado em `config/cache.php`. Neste arquivo, você pode especificar qual armazenamento de cache você gostaria de usar por padrão em toda a sua aplicação. O Laravel suporta backends de cache populares como [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), bancos de dados relacionais e discos de sistema de arquivos nativamente. Além disso, um driver de cache baseado em arquivo está disponível, enquanto os drivers de cache `array` e `null` fornecem backends de cache convenientes para seus testes automatizados.

O arquivo de configuração de cache também contém uma variedade de outras opções que você pode revisar. Por padrão, o Laravel está configurado para usar o driver de cache `database`, que armazena os objetos em cache serializados no banco de dados da sua aplicação.

<a id="driver-prerequisites"></a>
### Pré-requisitos do Driver

<a id="prerequisites-database"></a>
#### Database

Ao usar o driver de cache `database`, você precisará de uma tabela de banco de dados para conter os dados do cache. Tipicamente, isso está incluído na [migração de banco de dados](../migrations/) padrão `0001_01_01_000001_create_cache_table.php` do Laravel; no entanto, se sua aplicação não contém esta migração, você pode usar o comando Artisan `make:cache-table` para criá-la:

```shell
php artisan make:cache-table

php artisan migrate
```

<a id="memcached"></a>
#### Memcached

Usar o driver Memcached requer que o [pacote PECL Memcached](https://pecl.php.net/package/memcached) esteja instalado. Você pode listar todos os seus servidores Memcached no arquivo de configuração `config/cache.php`. Este arquivo já contém uma entrada `memcached.servers` para você começar:

```php
'memcached' => [
    // ...

    'servers' => [
        [
            'host' => env('MEMCACHED_HOST', '127.0.0.1'),
            'port' => env('MEMCACHED_PORT', 11211),
            'weight' => 100,
        ],
    ],
],
```

Se necessário, você pode definir a opção `host` como um caminho de socket UNIX. Se você fizer isso, a opção `port` deve ser definida como `0`:

```php
'memcached' => [
    // ...

    'servers' => [
        [
            'host' => '/var/run/memcached/memcached.sock',
            'port' => 0,
            'weight' => 100
        ],
    ],
],
```

<a id="redis"></a>
#### Redis

Antes de usar um cache Redis com o Laravel, você precisará instalar a extensão PHP PhpRedis via PECL ou instalar o pacote `predis/predis` via Composer. O [Laravel Sail](../sail/) já inclui esta extensão. Além disso, plataformas oficiais de aplicação Laravel como [Laravel Cloud](https://cloud.laravel.com) e [Laravel Forge](https://forge.laravel.com) têm a extensão PhpRedis instalada por padrão.

Para mais informações sobre configuração do Redis, consulte sua [página de documentação do Laravel](../redis/#configuration).

<a id="storage"></a>
#### Storage

O driver de cache `storage` permite armazenar valores em cache em qualquer um dos [discos de sistema de arquivos](../filesystem/) configurados da sua aplicação. Isso pode ser útil quando você deseja usar um disco existente, como um disco S3, como um armazenamento chave/valor de cache:

```php
'storage' => [
    'driver' => 'storage',
    'disk' => env('CACHE_STORAGE_DISK'),
    'path' => env('CACHE_STORAGE_PATH', 'framework/cache/data'),
],
```

<a id="dynamodb"></a>
#### DynamoDB

Antes de usar o driver de cache [DynamoDB](https://aws.amazon.com/dynamodb), você deve criar uma tabela DynamoDB para armazenar todos os dados em cache. Tipicamente, esta tabela deve ser nomeada `cache`. No entanto, você deve nomear a tabela com base no valor da configuração `stores.dynamodb.table` dentro do arquivo de configuração `cache`. O nome da tabela também pode ser definido via a variável de ambiente `DYNAMODB_CACHE_TABLE`.

Esta tabela também deve ter uma chave de partição string com um nome que corresponda ao valor do item de configuração `stores.dynamodb.attributes.key` dentro do arquivo de configuração `cache` da sua aplicação. Por padrão, a chave de partição deve ser nomeada `key`.

Tipicamente, o DynamoDB não removerá proativamente itens expirados de uma tabela. Portanto, você deve [habilitar Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) na tabela. Ao configurar as configurações de TTL da tabela, você deve definir o nome do atributo TTL como `expires_at`.

Em seguida, instale o AWS SDK para que sua aplicação Laravel possa se comunicar com o DynamoDB:

```shell
composer require aws/aws-sdk-php
```

Além disso, você deve garantir que os valores sejam fornecidos para as opções de configuração do armazenamento de cache DynamoDB. Tipicamente, essas opções, como `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`, devem ser definidas no arquivo de configuração `.env` da sua aplicação:

```php
'dynamodb' => [
    'driver' => 'dynamodb',
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => env('DYNAMODB_CACHE_TABLE', 'cache'),
    'endpoint' => env('DYNAMODB_ENDPOINT'),
],
```

<a id="mongodb"></a>
#### MongoDB

Se você estiver usando MongoDB, um driver de cache `mongodb` é fornecido pelo pacote oficial `mongodb/laravel-mongodb` e pode ser configurado usando uma conexão de banco de dados `mongodb`. O MongoDB suporta índices TTL, que podem ser usados para limpar automaticamente itens de cache expirados.

Para mais informações sobre configuração do MongoDB, por favor consulte a [documentação de Cache e Locks](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/) do MongoDB.

<a id="cache-usage"></a>
## Uso do Cache

<a id="obtaining-a-cache-instance"></a>
### Obtendo uma Instância de Cache

Para obter uma instância de armazenamento de cache, você pode usar a facade `Cache`, que é o que usaremos ao longo desta documentação. A facade `Cache` fornece acesso conveniente e conciso às implementações subjacentes dos contratos de cache do Laravel:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * Show a list of all users of the application.
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

<a id="accessing-multiple-cache-stores"></a>
#### Acessando Múltiplos Armazenamentos de Cache

Usando a facade `Cache`, você pode acessar vários armazenamentos de cache via o método `store`. A chave passada ao método `store` deve corresponder a um dos armazenamentos listados no array de configuração `stores` no seu arquivo de configuração `cache`:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```

<a id="retrieving-items-from-the-cache"></a>
### Recuperando Itens do Cache

O método `get` da facade `Cache` é usado para recuperar itens do cache. Se o item não existir no cache, `null` será retornado. Se você desejar, pode passar um segundo argumento ao método `get` especificando o valor padrão que você deseja que seja retornado se o item não existir:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

Você pode até passar um closure como valor padrão. O resultado do closure será retornado se o item especificado não existir no cache. Passar um closure permite que você adie a recuperação de valores padrão de um banco de dados ou outro serviço externo:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a id="determining-item-existence"></a>
#### Determinando a Existência do Item

O método `has` pode ser usado para determinar se um item existe no cache. Este método também retornará `false` se o item existir, mas seu valor for `null`:

```php
if (Cache::has('key')) {
    // ...
}
```

<a id="incrementing-decrementing-values"></a>
#### Incrementando / Decrementando Valores

Os métodos `increment` e `decrement` podem ser usados para ajustar o valor de itens inteiros no cache. Ambos os métodos aceitam um segundo argumento opcional indicando a quantidade pela qual incrementar ou decrementar o valor do item:

```php
// Initialize the value if it does not exist...
Cache::add('key', 0, now()->plus(hours: 4));

// Increment or decrement the value...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a id="retrieve-store"></a>
#### Recuperar e Armazenar

Às vezes, você pode desejar recuperar um item do cache, mas também armazenar um valor padrão se o item solicitado não existir. Por exemplo, você pode desejar recuperar todos os usuários do cache ou, se não existirem, recuperá-los do banco de dados e adicioná-los ao cache. Você pode fazer isso usando o método `Cache::remember`:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

Se o item não existir no cache, o closure passado ao método `remember` será executado e seu resultado será colocado no cache.

Se você precisa saber se o item foi recuperado do cache em vez de ser executado o closure fornecido, você pode usar o método `rememberWithWarmth`. Este método retorna um array contendo o valor em cache e um booleano indicando se o item estava "quente", significando que foi recuperado do cache e não resolvido a partir do closure:

```php
[$value, $warm] = Cache::rememberWithWarmth('users', $seconds, function () {
    return DB::table('users')->get();
});
```

Você pode usar o método `rememberForever` para recuperar um item do cache ou armazená-lo para sempre se não existir:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a id="swr"></a>
#### Stale While Revalidate

Ao usar o método `Cache::remember`, alguns usuários podem experimentar tempos de resposta lentos se o valor em cache tiver expirado. Para certos tipos de dados, pode ser útil permitir que dados parcialmente obsoletos sejam servidos enquanto o valor em cache é recalculado em segundo plano, evitando que alguns usuários experimentem tempos de resposta lentos enquanto os valores em cache são calculados. Isso é frequentemente referido como o padrão "stale-while-revalidate", e o método `Cache::flexible` fornece uma implementação deste padrão.

O método flexible aceita um array que especifica por quanto tempo o valor em cache é considerado "fresco" e quando ele se torna "obsoleto". O primeiro valor no array representa o número de segundos em que o cache é considerado fresco, enquanto o segundo valor define por quanto tempo ele pode ser servido como dados obsoletos antes que o recálculo seja necessário.

Se uma requisição for feita dentro do período fresco (antes do primeiro valor), o cache é retornado imediatamente sem recálculo. Se uma requisição for feita durante o período obsoleto (entre os dois valores), o valor obsoleto é servido ao usuário, e uma [função adiada](../helpers/#deferred-functions) é registrada para atualizar o valor em cache após a resposta ser enviada ao usuário. Se uma requisição for feita após o segundo valor, o cache é considerado expirado, e o valor é recalculado imediatamente, o que pode resultar em uma resposta mais lenta para o usuário:

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a id="retrieve-delete"></a>
#### Recuperar e Deletar

Se você precisa recuperar um item do cache e depois deletar o item, você pode usar o método `pull`. Como o método `get`, `null` será retornado se o item não existir no cache:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a id="storing-items-in-the-cache"></a>
### Armazenando Itens no Cache

Você pode usar o método `put` na facade `Cache` para armazenar itens no cache:

```php
Cache::put('key', 'value', $seconds = 10);
```

Se o tempo de armazenamento não for passado ao método `put`, o item será armazenado indefinidamente:

```php
Cache::put('key', 'value');
```

Em vez de passar o número de segundos como um inteiro, você também pode passar uma instância `DateTime` representando o tempo de expiração desejado do item em cache:

```php
Cache::put('key', 'value', now()->plus(minutes: 10));
```

<a id="store-if-not-present"></a>
#### Armazenar se Não Presente

O método `add` apenas adicionará o item ao cache se ele ainda não existir no armazenamento de cache. O método retornará `true` se o item for realmente adicionado ao cache. Caso contrário, o método retornará `false`. O método `add` é uma operação atômica:

```php
Cache::add('key', 'value', $seconds);
```

<a id="extending-item-lifetime"></a>
### Estendendo o Tempo de Vida do Item

O método `touch` permite que você estenda o tempo de vida (TTL) de um item de cache existente. O método `touch` retornará `true` se o item de cache existir e seu tempo de expiração tiver sido estendido com sucesso. Se o item não existir no cache, o método retornará `false`:

```php
Cache::touch('key', 3600);
```

Você pode fornecer uma instância `DateTimeInterface`, `DateInterval` ou `Carbon` para especificar um tempo de expiração exato:

```php
Cache::touch('key', now()->addHours(2));
```

<a id="storing-items-forever"></a>
#### Armazenando Itens Para Sempre

O método `forever` pode ser usado para armazenar um item no cache permanentemente. Como esses itens não expirarão, eles devem ser removidos manualmente do cache usando o método `forget`:

```php
Cache::forever('key', 'value');
```

> **Nota:**
> Se você estiver usando o driver Memcached, itens armazenados "para sempre" podem ser removidos quando o cache atingir seu limite de tamanho.

<a id="removing-items-from-the-cache"></a>
### Removendo Itens do Cache

Você pode remover itens do cache usando o método `forget`:

```php
Cache::forget('key');
```

Você também pode remover itens fornecendo um número zero ou negativo de segundos de expiração:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

Você pode limpar todo o cache usando o método `flush`:

```php
Cache::flush();
```

Você pode limpar todos os locks atômicos no cache usando o método `flushLocks`:

```php
Cache::flushLocks();
```

> **Aviso:**
> Limpar o cache não respeita o "prefixo" de cache configurado e removerá todas as entradas do cache. Considere isso cuidadosamente ao limpar um cache que é compartilhado por outras aplicações.

<a id="cache-memoization"></a>
### Memoização de Cache

O driver de cache `memo` do Laravel permite armazenar temporariamente valores de cache resolvidos em memória durante uma única requisição ou execução de job. Isso evita hits repetidos de cache dentro da mesma execução, melhorando significativamente o desempenho.

Para usar o cache memoizado, invoque o método `memo`:

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

O método `memo` aceita opcionalmente o nome de um armazenamento de cache, que especifica o armazenamento de cache subjacente que o driver memoizado irá decorar:

```php
// Using the default cache store...
$value = Cache::memo()->get('key');

// Using the Redis cache store...
$value = Cache::memo('redis')->get('key');
```

A primeira chamada `get` para uma determinada chave recupera o valor do seu armazenamento de cache, mas chamadas subsequentes dentro da mesma requisição ou job recuperarão o valor da memória:

```php
// Hits the cache...
$value = Cache::memo()->get('key');

// Does not hit the cache, returns memoized value...
$value = Cache::memo()->get('key');
```

Ao chamar métodos que modificam valores de cache (como `put`, `increment`, `remember`, etc.), o cache memoizado automaticamente esquece o valor memoizado e delega a chamada do método mutante ao armazenamento de cache subjacente:

```php
Cache::memo()->put('name', 'Taylor'); // Writes to underlying cache...
Cache::memo()->get('name');           // Hits underlying cache...
Cache::memo()->get('name');           // Memoized, does not hit cache...

Cache::memo()->put('name', 'Tim');    // Forgets memoized value, writes new value...
Cache::memo()->get('name');           // Hits underlying cache again...
```

<a id="the-cache-helper"></a>
### O Helper de Cache

Além de usar a facade `Cache`, você também pode usar a função global `cache` para recuperar e armazenar dados via o cache. Quando a função `cache` é chamada com um único argumento string, ela retornará o valor da chave fornecida:

```php
$value = cache('key');
```

Se você fornecer um array de pares chave/valor e um tempo de expiração para a função, ela armazenará valores no cache pela duração especificada:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->plus(minutes: 10));
```

Quando a função `cache` é chamada sem nenhum argumento, ela retorna uma instância da implementação de `Illuminate\Contracts\Cache\Factory`, permitindo que você chame outros métodos de cache:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> **Nota:**
> Ao testar chamadas para a função global `cache`, você pode usar o método `Cache::shouldReceive` como se estivesse [testando a facade](../mocking/#mocking-facades).

<a id="cache-tags"></a>
## Cache Tags

> **Aviso:**
> Cache tags não são suportadas ao usar os drivers de cache `file`, `dynamodb`, `database` ou `storage`.

<a id="storing-tagged-cache-items"></a>
### Armazenando Itens de Cache com Tags

Cache tags permitem que você etiquete itens relacionados no cache e depois limpe todos os valores em cache que foram atribuídos a uma determinada tag. Você pode acessar um cache com tags passando um array ordenado de nomes de tags. Por exemplo, vamos acessar um cache com tags e `put` um valor no cache:

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a id="accessing-tagged-cache-items"></a>
### Acessando Itens de Cache com Tags

Itens armazenados via tags não podem ser acessados sem também fornecer as tags que foram usadas para armazenar o valor. Para recuperar um item de cache com tags, passe a mesma lista ordenada de tags ao método `tags`, depois chame o método `get` com a chave que você deseja recuperar:

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a id="removing-tagged-cache-items"></a>
### Removendo Itens de Cache com Tags

Você pode limpar todos os itens que são atribuídos a uma tag ou lista de tags. Por exemplo, o código abaixo removeria todos os caches etiquetados com `people`, `authors`, ou ambos. Então, tanto `Anne` quanto `John` seriam removidos do cache:

```php
Cache::tags(['people', 'authors'])->flush();
```

Em contraste, o código abaixo removeria apenas valores em cache etiquetados com `authors`, então `Anne` seria removida, mas não `John`:

```php
Cache::tags('authors')->flush();
```

<a id="atomic-locks"></a>
## Locks Atômicos

> **Aviso:**
> Para utilizar este recurso, sua aplicação deve estar usando o driver de cache `memcached`, `redis`, `dynamodb`, `database`, `file` ou `array` como driver de cache padrão da aplicação. Além disso, todos os servidores devem estar se comunicando com o mesmo servidor de cache central.

<a id="managing-locks"></a>
### Gerenciando Locks

Locks atômicos permitem a manipulação de locks distribuídos sem se preocupar com condições de corrida. Por exemplo, o [Laravel Cloud](https://cloud.laravel.com) usa locks atômicos para garantir que apenas uma tarefa remota esteja sendo executada em um servidor por vez. Você pode criar e gerenciar locks usando o método `Cache::lock`:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // Lock acquired for 10 seconds...

    $lock->release();
}
```

O método `get` também aceita um closure. Após o closure ser executado, o Laravel liberará automaticamente o lock:

```php
Cache::lock('foo', 10)->get(function () {
    // Lock acquired for 10 seconds and automatically released...
});
```

Se o lock não estiver disponível no momento em que você o solicita, você pode instruir o Laravel a esperar por um número especificado de segundos. Se o lock não puder ser adquirido dentro do limite de tempo especificado, uma exceção `Illuminate\Contracts\Cache\LockTimeoutException` será lançada:

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // Lock acquired after waiting a maximum of 5 seconds...
} catch (LockTimeoutException $e) {
    // Unable to acquire lock...
} finally {
    $lock->release();
}
```

O exemplo acima pode ser simplificado passando um closure ao método `block`. Quando um closure é passado a este método, o Laravel tentará adquirir o lock pelo número especificado de segundos e liberará automaticamente o lock uma vez que o closure tenha sido executado:

```php
Cache::lock('foo', 10)->block(5, function () {
    // Lock acquired for 10 seconds after waiting a maximum of 5 seconds...
});
```

<a id="managing-locks-across-processes"></a>
### Gerenciando Locks Entre Processos

Às vezes, você pode desejar adquirir um lock em um processo e liberá-lo em outro processo. Por exemplo, você pode adquirir um lock durante uma requisição web e desejar liberar o lock no final de um job enfileirado que é disparado por aquela requisição. Neste cenário, você deve passar o "token de dono" escopado do lock ao job enfileirado para que o job possa reinstanciar o lock usando o token fornecido.

No exemplo abaixo, despacharemos um job enfileirado se um lock for adquirido com sucesso. Além disso, passaremos o token de dono do lock ao job enfileirado via o método `owner` do lock:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

Dentro do nosso job `ProcessPodcast`, podemos restaurar e liberar o lock usando o token de dono:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

Se você gostaria de liberar um lock sem respeitar seu dono atual, você pode usar o método `forceRelease`:

```php
Cache::lock('processing')->forceRelease();
```

<a id="refreshing-locks"></a>
### Atualizando Locks

Se você precisa estender a expiração de um lock que você atualmente possui, você pode usar o método `refresh`. Se nenhum número de segundos for fornecido, a duração original do lock será usada. Isso é útil para operações de longa duração onde você prefere adquirir um lock curto e periodicamente estendê-lo em vez de adquirir um lock com um tempo de expiração muito longo:

```php
$lock = Cache::lock('generate-reports', 60);

if ($lock->get()) {
    foreach ($reports as $report) {
        $report->generate();

        // Extend the lock for another 60 seconds...
        $lock->refresh();
    }

    $lock->release();
}
```

<a id="concurrency-limiting"></a>
### Limitando Concorrência

A funcionalidade de locks atômicos do Laravel também fornece algumas maneiras de limitar a execução concorrente de closures. Use `withoutOverlapping` quando você deseja permitir apenas uma instância em execução em toda a sua infraestrutura:

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired after waiting a maximum of 10 seconds...
});
```

Por padrão, o lock é mantido até que o closure termine de executar, e o método espera até 10 segundos para adquirir o lock. Você pode personalizar esses valores usando argumentos adicionais:

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired for 120 seconds after waiting a maximum of 5 seconds...
}, lockFor: 120, waitFor: 5);
```

Se o lock não puder ser adquirido dentro do tempo de espera especificado, uma exceção `Illuminate\Contracts\Cache\LockTimeoutException` será lançada.

Se você deseja paralelismo controlado, use o método `funnel` para definir um número máximo de execuções concorrentes. O método `funnel` funciona com qualquer driver de cache que suporte locks:

```php
Cache::funnel('foo')
    ->limit(3)
    ->releaseAfter(60)
    ->block(10)
    ->then(function () {
        // Concurrency lock acquired...
    }, function () {
        // Could not acquire concurrency lock...
    });
```

A chave `funnel` identifica o recurso sendo limitado. O método `limit` define o máximo de execuções concorrentes. O método `releaseAfter` define um timeout de segurança em segundos antes que um slot adquirido seja automaticamente liberado. O método `block` define quantos segundos esperar por um slot disponível.

Se você preferir tratar o timeout via exceções em vez de fornecer um closure de falha, você pode omitir o segundo closure. Uma exceção `Illuminate\Cache\Limiters\LimiterTimeoutException` será lançada se o lock não puder ser adquirido dentro do tempo de espera especificado:

```php
use Illuminate\Cache\Limiters\LimiterTimeoutException;

try {
    Cache::funnel('foo')
        ->limit(3)
        ->releaseAfter(60)
        ->block(10)
        ->then(function () {
            // Concurrency lock acquired...
        });
} catch (LimiterTimeoutException $e) {
    // Unable to acquire concurrency lock...
}
```

Se você gostaria de usar um armazenamento de cache específico para o limitador de concorrência, você pode invocar o método `funnel` no armazenamento desejado:

```php
Cache::store('redis')->funnel('foo')
    ->limit(3)
    ->block(10)
    ->then(function () {
        // Concurrency lock acquired using the "redis" store...
    });
```

> **Nota:**
> O método `funnel` requer que o armazenamento de cache implemente a interface `Illuminate\Contracts\Cache\LockProvider`. Se você tentar usar `funnel` com um armazenamento de cache que não suporta locks, uma `BadMethodCallException` será lançada.

<a id="cache-failover"></a>
## Failover de Cache

O driver de cache `failover` fornece funcionalidade de failover automático ao interagir com o cache. Se o armazenamento de cache principal do armazenamento `failover` falhar por qualquer motivo, o Laravel tentará automaticamente usar o próximo armazenamento configurado na lista. Isso é particularmente útil para garantir alta disponibilidade em ambientes de produção onde a confiabilidade do cache é crítica.

Para configurar um armazenamento de cache com failover, especifique o driver `failover` e forneça um array de nomes de armazenamentos para tentar em ordem. Por padrão, o Laravel inclui um exemplo de configuração de failover no arquivo de configuração `config/cache.php` da sua aplicação:

```php
'failover' => [
    'driver' => 'failover',
    'stores' => [
        'database',
        'array',
    ],
],
```

Uma vez que você tenha configurado um armazenamento que usa o driver `failover`, você precisará definir o armazenamento de failover como seu armazenamento de cache padrão no arquivo `.env` da sua aplicação para usar a funcionalidade de failover:

```ini
CACHE_STORE=failover
```

Quando uma operação de armazenamento de cache falha e o failover é ativado, o Laravel despachará o evento `Illuminate\Cache\Events\CacheFailedOver`, permitindo que você reporte ou registre que um armazenamento de cache falhou.

<a id="adding-custom-cache-drivers"></a>
## Adicionando Drivers de Cache Personalizados

<a id="writing-the-driver"></a>
### Escrevendo o Driver

Para criar nosso driver de cache personalizado, primeiro precisamos implementar o [contrato](../contracts/) `Illuminate\Contracts\Cache\Store`. Então, uma implementação de cache MongoDB pode se parecer com algo assim:

```php
<?php

namespace App\Extensions;

use Illuminate\Contracts\Cache\Store;

class MongoStore implements Store
{
    public function get($key) {}
    public function many(array $keys) {}
    public function put($key, $value, $seconds) {}
    public function putMany(array $values, $seconds) {}
    public function increment($key, $value = 1) {}
    public function decrement($key, $value = 1) {}
    public function forever($key, $value) {}
    public function touch($key, $seconds) {}
    public function forget($key) {}
    public function flush() {}
    public function getPrefix() {}
}
```

Nós apenas precisamos implementar cada um desses métodos usando uma conexão MongoDB. Para um exemplo de como implementar cada um desses métodos, dê uma olhada no `Illuminate\Cache\MemcachedStore` no [código fonte do framework Laravel](https://github.com/laravel/framework). Uma vez que nossa implementação esteja completa, podemos finalizar o registro do nosso driver personalizado chamando o método `extend` da facade `Cache`:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> **Nota:**
> Se você está se perguntando onde colocar o código do seu driver de cache personalizado, você poderia criar um namespace `Extensions` dentro do seu diretório `app`. No entanto, tenha em mente que o Laravel não tem uma estrutura de aplicação rígida e você é livre para organizar sua aplicação de acordo com suas preferências.

<a id="registering-the-driver"></a>
### Registrando o Driver

Para registrar o driver de cache personalizado com o Laravel, usaremos o método `extend` na facade `Cache`. Como outros provedores de serviço podem tentar ler valores em cache dentro de seus métodos `boot`, registraremos nosso driver personalizado dentro de um callback `booting`. Ao usar o callback `booting`, podemos garantir que o driver personalizado seja registrado logo antes que o método `boot` seja chamado nos provedores de serviço da nossa aplicação, mas após o método `register` ser chamado em todos os provedores de serviço. Registraremos nosso callback `booting` dentro do método `register` da classe `App\Providers\AppServiceProvider` da nossa aplicação:

```php
<?php

namespace App\Providers;

use App\Extensions\MongoStore;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->booting(function () {
             Cache::extend('mongo', function (Application $app) {
                 return Cache::repository(new MongoStore);
             });
         });
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        // ...
    }
}
```

O primeiro argumento passado ao método `extend` é o nome do driver. Isso corresponderá à sua opção `driver` no arquivo de configuração `config/cache.php`. O segundo argumento é um closure que deve retornar uma instância `Illuminate\Cache\Repository`. O closure receberá uma instância `$app`, que é uma instância do [container de serviço](../container/).

Uma vez que sua extensão seja registrada, atualize a variável de ambiente `CACHE_STORE` ou a opção `default` dentro do arquivo de configuração `config/cache.php` da sua aplicação para o nome da sua extensão.

<a id="events"></a>
## Eventos

Para executar código em cada operação de cache, você pode ouvir vários [eventos](../events/) despachados pelo cache:

<div class="overflow-auto">

| Nome do Evento                                      |
|-----------------------------------------------------|
| `Illuminate\Cache\Events\CacheFlushed`              |
| `Illuminate\Cache\Events\CacheFlushing`             |
| `Illuminate\Cache\Events\CacheFlushFailed`          |
| `Illuminate\Cache\Events\CacheLocksFlushed`         |
| `Illuminate\Cache\Events\CacheLocksFlushing`        |
| `Illuminate\Cache\Events\CacheLocksFlushFailed`     |
| `Illuminate\Cache\Events\CacheHit`                  |
| `Illuminate\Cache\Events\CacheMissed`               |
| `Illuminate\Cache\Events\ForgettingKey`             |
| `Illuminate\Cache\Events\KeyForgetFailed`           |
| `Illuminate\Cache\Events\KeyForgotten`              |
| `Illuminate\Cache\Events\KeyWriteFailed`            |
| `Illuminate\Cache\Events\KeyWritten`                |
| `Illuminate\Cache\Events\RetrievingKey`             |
| `Illuminate\Cache\Events\RetrievingManyKeys`        |
| `Illuminate\Cache\Events\WritingKey`                |
| `Illuminate\Cache\Events\WritingManyKeys`           |

</div>

Para aumentar o desempenho, você pode desabilitar eventos de cache definindo a opção de configuração `events` como `false` para um determinado armazenamento de cache no arquivo de configuração `config/cache.php` da sua aplicação:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```