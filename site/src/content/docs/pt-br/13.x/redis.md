---
title: "Redis"
---

- [Introdução](#introduction)
- [Configuração](#configuration)
    - [Clusters](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Interagindo Com o Redis](#interacting-with-redis)
    - [Transações](#transactions)
    - [Pipelining de Comandos](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a id="introduction"></a>
## Introdução

O [Redis](https://redis.io) é um armazenamento de chave-valor avançado e de código aberto. Ele é frequentemente chamado de servidor de estruturas de dados, já que as chaves podem conter [strings](https://redis.io/docs/latest/develop/data-types/strings/), [hashes](https://redis.io/docs/latest/develop/data-types/hashes/), [lists](https://redis.io/docs/latest/develop/data-types/lists/), [sets](https://redis.io/docs/latest/develop/data-types/sets/) e [sorted sets](https://redis.io/docs/latest/develop/data-types/sorted-sets/).

Antes de usar o Redis com o Laravel, recomendamos que você instale e use a extensão PHP [PhpRedis](https://github.com/phpredis/phpredis) via PECL. A extensão é mais complexa de instalar em comparação com pacotes PHP "user-land", mas pode gerar melhor desempenho para aplicações que fazem uso intenso do Redis. Se você estiver usando o [Laravel Sail](../sail/), essa extensão já está instalada no container Docker da sua aplicação.

Se você não conseguir instalar a extensão PhpRedis, pode instalar o pacote `predis/predis` via Composer. O Predis é um cliente Redis escrito inteiramente em PHP e não requer nenhuma extensão adicional:

```shell
composer require predis/predis
```

<a id="configuration"></a>
## Configuração

Você pode configurar as definições de Redis da sua aplicação através do arquivo de configuração `config/database.php`. Dentro desse arquivo, você verá um array `redis` contendo os servidores Redis utilizados pela sua aplicação:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug((string) env('APP_NAME', 'laravel')).'-database-'),
    ],

    'default' => [
        'url' => env('REDIS_URL'),
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'username' => env('REDIS_USERNAME'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', '6379'),
        'database' => env('REDIS_DB', '0'),
    ],

    'cache' => [
        'url' => env('REDIS_URL'),
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'username' => env('REDIS_USERNAME'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', '6379'),
        'database' => env('REDIS_CACHE_DB', '1'),
    ],

],
```

Cada servidor Redis definido no seu arquivo de configuração deve ter um nome, host e uma porta, a menos que você defina uma única URL para representar a conexão Redis:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug((string) env('APP_NAME', 'laravel')).'-database-'),
    ],

    'default' => [
        'url' => 'tcp://127.0.0.1:6379?database=0',
    ],

    'cache' => [
        'url' => 'tls://user:password@127.0.0.1:6380?database=1',
    ],

],
```

<a id="configuring-the-connection-scheme"></a>
#### Configurando o Esquema de Conexão

Por padrão, os clientes Redis usarão o esquema `tcp` ao se conectar aos seus servidores Redis; no entanto, você pode usar criptografia TLS / SSL especificando uma opção de configuração `scheme` no array de configuração do seu servidor Redis:

```php
'default' => [
    'scheme' => 'tls',
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
],
```

<a id="clusters"></a>
### Clusters

Se a sua aplicação estiver utilizando um cluster de servidores Redis, você deve definir esses clusters dentro de uma chave `clusters` da sua configuração do Redis. Essa chave de configuração não existe por padrão, então você precisará criá-la dentro do arquivo de configuração `config/database.php` da sua aplicação:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug((string) env('APP_NAME', 'laravel')).'-database-'),
    ],

    'clusters' => [
        'default' => [
            [
                'url' => env('REDIS_URL'),
                'host' => env('REDIS_HOST', '127.0.0.1'),
                'username' => env('REDIS_USERNAME'),
                'password' => env('REDIS_PASSWORD'),
                'port' => env('REDIS_PORT', '6379'),
                'database' => env('REDIS_DB', '0'),
            ],
        ],
    ],

    // ...
],
```

Por padrão, o Laravel usará o clustering nativo do Redis, já que o valor de configuração `options.cluster` está definido como `redis`. O clustering do Redis é uma ótima opção padrão, pois lida com o failover de forma elegante.

O Laravel também suporta sharding no lado do cliente ao usar o Predis. No entanto, o sharding no lado do cliente não lida com failover; portanto, ele é adequado principalmente para dados em cache transitórios que estão disponíveis a partir de outro armazenamento de dados primário.

Se você quiser usar sharding no lado do cliente em vez do clustering nativo do Redis, pode remover o valor de configuração `options.cluster` dentro do arquivo de configuração `config/database.php` da sua aplicação:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'clusters' => [
        // ...
    ],

    // ...
],
```

<a id="predis"></a>
### Predis

Se você quiser que a sua aplicação interaja com o Redis através do pacote Predis, deve garantir que o valor da variável de ambiente `REDIS_CLIENT` seja `predis`:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

Além das opções de configuração padrão, o Predis suporta [parâmetros de conexão](https://github.com/nrk/predis/wiki/Connection-Parameters) adicionais que podem ser definidos para cada um dos seus servidores Redis. Para utilizar essas opções de configuração adicionais, adicione-as à configuração do seu servidor Redis no arquivo de configuração `config/database.php` da sua aplicação:

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'read_write_timeout' => 60,
],
```

<a id="phpredis"></a>
### PhpRedis

Por padrão, o Laravel usará a extensão PhpRedis para se comunicar com o Redis. O cliente que o Laravel usará para se comunicar com o Redis é ditado pelo valor da opção de configuração `redis.client`, que normalmente reflete o valor da variável de ambiente `REDIS_CLIENT`:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

Além das opções de configuração padrão, o PhpRedis suporta os seguintes parâmetros de conexão adicionais: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout` e `context`. Você pode adicionar qualquer uma dessas opções à configuração do seu servidor Redis no arquivo de configuração `config/database.php`:

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'read_timeout' => 60,
    'context' => [
        // 'auth' => ['username', 'secret'],
        // 'stream' => ['verify_peer' => false],
    ],
],
```

<a id="retry-and-backoff-configuration"></a>
#### Configuração de Retry e Backoff

As opções `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base` e `backoff_cap` podem ser usadas para configurar como o cliente PhpRedis deve tentar se reconectar a um servidor Redis. Os seguintes algoritmos de backoff são suportados: `default`, `decorrelated_jitter`, `equal_jitter`, `exponential`, `uniform` e `constant`:

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'max_retries' => env('REDIS_MAX_RETRIES', 3),
    'backoff_algorithm' => env('REDIS_BACKOFF_ALGORITHM', 'decorrelated_jitter'),
    'backoff_base' => env('REDIS_BACKOFF_BASE', 100),
    'backoff_cap' => env('REDIS_BACKOFF_CAP', 1000),
],
```

O Laravel repete automaticamente comandos de leitura seguros uma vez após uma falha de conexão transitória. Você pode usar a opção `command_retries` para configurar o número de tentativas para todos os comandos Redis:

```php
'default' => [
    // ...
    'command_retries' => env('REDIS_COMMAND_RETRIES', 0),
],
```

O Predis 3.4.0 e versões posteriores suportam configuração de retry e backoff integrada através da classe `Retry`. Você pode configurar as tentativas usando a opção `max_retries` e configurar a estratégia de backoff usando a opção `retry`. A opção `retry` deve ser um array com chave em uma das seguintes classes de estratégia: `NoBackoff`, `EqualBackoff` ou `ExponentialBackoff`:

```php
use Predis\Retry\Strategy\ExponentialBackoff;

'default' => [
    'url' => env('REDIS_URL'),
    // ...
    'retry' => [
        ExponentialBackoff::class => [
            env('REDIS_BACKOFF_BASE', 100),
            env('REDIS_BACKOFF_CAP', 1000),
            true, // Enable jitter...
        ],
    ],
    'max_retries' => env('REDIS_MAX_RETRIES', 3),
],
```

Ao usar o Predis com um cluster Redis, você pode definir a configuração de retry na opção `parameters` da sua configuração de cluster:

```php
use Predis\Retry\Strategy\NoBackoff;

'clusters' => [
    'default' => [
        // ...
    ],
],

'options' => [
    'cluster' => env('REDIS_CLUSTER', 'redis'),
    'parameters' => [
        'retry' => [
            NoBackoff::class => [],
        ],
        'max_retries' => env('REDIS_MAX_RETRIES', 3),
    ],
],
```

<a id="unix-socket-connections"></a>
#### Conexões por Socket Unix

As conexões Redis também podem ser configuradas para usar sockets Unix em vez de TCP. Isso pode oferecer desempenho aprimorado ao eliminar a sobrecarga do TCP para conexões a instâncias Redis no mesmo servidor que a sua aplicação. Para configurar o Redis para usar um socket Unix, defina a variável de ambiente `REDIS_HOST` como o caminho do socket Redis e a variável de ambiente `REDIS_PORT` como `0`:

```env
REDIS_HOST=/run/redis/redis.sock
REDIS_PORT=0
```

<a id="phpredis-serialization"></a>
#### Serialização e Compressão do PhpRedis

A extensão PhpRedis também pode ser configurada para usar uma variedade de serializadores e algoritmos de compressão. Esses algoritmos podem ser configurados através do array `options` da sua configuração do Redis:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug((string) env('APP_NAME', 'laravel')).'-database-'),
        'serializer' => Redis::SERIALIZER_MSGPACK,
        'compression' => Redis::COMPRESSION_LZ4,
    ],

    // ...
],
```

Os serializadores atualmente suportados incluem: `Redis::SERIALIZER_NONE` (padrão), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY` e `Redis::SERIALIZER_MSGPACK`.

Os algoritmos de compressão suportados incluem: `Redis::COMPRESSION_NONE` (padrão), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD` e `Redis::COMPRESSION_LZ4`.

<a id="interacting-with-redis"></a>
## Interagindo Com o Redis

Você pode interagir com o Redis chamando vários métodos na [facade](../facades/) `Redis`. A facade `Redis` suporta métodos dinâmicos, o que significa que você pode chamar qualquer [comando Redis](https://redis.io/commands) na facade e o comando será passado diretamente ao Redis. Neste exemplo, chamaremos o comando `GET` do Redis chamando o método `get` na facade `Redis`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Redis;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => Redis::get('user:profile:'.$id)
        ]);
    }
}
```

Como mencionado acima, você pode chamar qualquer um dos comandos do Redis na facade `Redis`. O Laravel usa métodos mágicos para passar os comandos ao servidor Redis. Se um comando Redis espera argumentos, você deve passá-los para o método correspondente da facade:

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

Alternativamente, você pode passar comandos ao servidor usando o método `command` da facade `Redis`, que aceita o nome do comando como seu primeiro argumento e um array de valores como seu segundo argumento:

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a id="using-multiple-redis-connections"></a>
#### Usando Múltiplas Conexões Redis

O arquivo de configuração `config/database.php` da sua aplicação permite que você defina múltiplas conexões / servidores Redis. Você pode obter uma conexão com uma conexão Redis específica usando o método `connection` da facade `Redis`:

```php
$redis = Redis::connection('connection-name');
```

Para obter uma instância da conexão Redis padrão, você pode chamar o método `connection` sem nenhum argumento adicional:

```php
$redis = Redis::connection();
```

<a id="transactions"></a>
### Transações

O método `transaction` da facade `Redis` fornece um wrapper conveniente em torno dos comandos nativos `MULTI` e `EXEC` do Redis. O método `transaction` aceita um closure como seu único argumento. Esse closure receberá uma instância de conexão Redis e poderá emitir quaisquer comandos que desejar para essa instância. Todos os comandos Redis emitidos dentro do closure serão executados em uma única transação atômica:

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> **Aviso:**
> Ao definir uma transação Redis, você não pode recuperar nenhum valor da conexão Redis. Lembre-se de que sua transação é executada como uma única operação atômica e essa operação não é executada até que todo o seu closure tenha terminado de executar seus comandos.

#### Scripts Lua

O método `eval` fornece outra maneira de executar múltiplos comandos Redis em uma única operação atômica. No entanto, o método `eval` tem o benefício de poder interagir com e inspecionar os valores das chaves Redis durante essa operação. Os scripts Redis são escritos na [linguagem de programação Lua](https://www.lua.org).

O método `eval` pode ser um pouco assustador no início, mas vamos explorar um exemplo básico para quebrar o gelo. O método `eval` espera vários argumentos. Primeiro, você deve passar o script Lua (como uma string) para o método. Em segundo lugar, você deve passar o número de chaves (como um inteiro) com as quais o script interage. Em terceiro lugar, você deve passar os nomes dessas chaves. Por fim, você pode passar quaisquer outros argumentos adicionais que precise acessar dentro do seu script.

Neste exemplo, incrementaremos um contador, inspecionaremos seu novo valor e incrementaremos um segundo contador se o valor do primeiro contador for maior que cinco. Por fim, retornaremos o valor do primeiro contador:

```php
$value = Redis::eval(<<<'LUA'
    local counter = redis.call("incr", KEYS[1])

    if counter > 5 then
        redis.call("incr", KEYS[2])
    end

    return counter
LUA, 2, 'first-counter', 'second-counter');
```

> **Aviso:**
> Por favor, consulte a [documentação do Redis](https://redis.io/commands/eval) para mais informações sobre scripting no Redis.

<a id="pipelining-commands"></a>
### Pipelining de Comandos

Às vezes, você pode precisar executar dezenas de comandos Redis. Em vez de fazer uma viagem de rede ao seu servidor Redis para cada comando, você pode usar o método `pipeline`. O método `pipeline` aceita um argumento: um closure que recebe uma instância do Redis. Você pode emitir todos os seus comandos para essa instância do Redis e todos eles serão enviados ao servidor Redis ao mesmo tempo para reduzir as viagens de rede ao servidor. Os comandos ainda serão executados na ordem em que foram emitidos:

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::pipeline(function (Redis $pipe) {
    for ($i = 0; $i < 1000; $i++) {
        $pipe->set("key:$i", $i);
    }
});
```

<a id="pubsub"></a>
## Pub / Sub

O Laravel fornece uma interface conveniente para os comandos `publish` e `subscribe` do Redis. Esses comandos Redis permitem que você escute mensagens em um determinado "canal". Você pode publicar mensagens no canal a partir de outra aplicação, ou mesmo usando outra linguagem de programação, permitindo uma comunicação fácil entre aplicações e processos.

Primeiro, vamos configurar um listener de canal usando o método `subscribe`. Colocaremos essa chamada de método dentro de um [comando Artisan](../artisan/), já que chamar o método `subscribe` inicia um processo de longa duração:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Redis;

class RedisSubscribe extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'redis:subscribe';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Subscribe to a Redis channel';

    /**
     * Execute the console command.
     */
    public function handle(): void
    {
        Redis::subscribe(['test-channel'], function (string $message) {
            echo $message;
        });
    }
}
```

Agora podemos publicar mensagens no canal usando o método `publish`:

```php
use Illuminate\Support\Facades\Redis;

Route::get('/publish', function () {
    // ...

    Redis::publish('test-channel', json_encode([
        'name' => 'Adam Wathan'
    ]));
});
```

<a id="wildcard-subscriptions"></a>
#### Assinaturas com Curinga

Usando o método `psubscribe`, você pode se inscrever em um canal curinga, o que pode ser útil para capturar todas as mensagens em todos os canais. O nome do canal será passado como o segundo argumento para o closure fornecido:

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```
