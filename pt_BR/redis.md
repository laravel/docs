# Redis

- [Introdução](#introduction)
- [Utilização Básica](#basic-usage)
    - [Múltiplos Comandos](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## Introdução

[Redis](http://redis.io) é um banco de dados para persistência no modelo Key/Value. Ele é comumente conhecido como um "Storage Engine Server" onde as keys contém [strings](http://redis.io/topics/data-types#strings), [hashes](http://redis.io/topics/data-types#hashes), [lists](http://redis.io/topics/data-types#lists), [sets](http://redis.io/topics/data-types#sets), e [sets sortidos](http://redis.io/topics/data-types#sorted-sets). Antes de usar o Redis com Laravel você precisará instalar o package `predis/predis` (~1.0) via Composer.

<a name="configuration"></a>
### Configuração

A configuração do Redis na sua aplicação deve ser feita no arquivo `config/database.php`. Dentro deste arquivo você encontrará um array `redis` contendo os servidores Redis utilizados pela sua aplicação:

    'redis' => [

        'cluster' => false,

        'default' => [
            'host'     => '127.0.0.1',
            'port'     => 6379,
            'database' => 0,
        ],

    ],

A configuração padrão geralmente é suficiente para ambiente de desenvolvimento. Entretanto, fique livre para modificar esse array de acordo com o seu ambiente. Simplesmente dê a cada servidor Redis um nome e especifique o host e a porta.

A opção `cluster` dirá ao Cliente Redis do Laravel para realizar a fragmentação client-side em todos os seus nodes Redis, possibilitando  que você acumule os nodes e crie uma grande quantia de RAM disponível. A fragmentação client-side não lida com falhas, portanto é altamente recomendado que dados em cache estejam  disponíveis a partir de outro armazenamento de dados primário.

Também é possível adicionar um array `options` na sua configuração do Redis, possibilitando que você especifique um conjunto de [opções do cliente](https://github.com/nrk/predis/wiki/Client-Options) Predis.

Se o seu servidor Redis requer autenticação, você pode fornecer uma senha adicionando um campo `password` no seu array de configuração.

> **Nota:** Se você possui a extensão Redis para PHP instalada via PECL, você vai precisar mudar o nome do alias Redis no arquivo `config/app.php`.

<a name="basic-usage"></a>
## Utilização básica

Você pode interagir com o Redis chamando vários métodos disponíveis no [facade](/docs/{{version}}/facades) `Redis`. O facade suporta métodos dinâmicos, ou seja, qualquer [comando Redis](http://redis.io/commands) utilizando o facade será passado diretamente ao servidor Redis. No exemplo abaixo nós chamaremos o comando `GET` do Redis utilizando o método `get`  do facade:

    <?php

    namespace App\Http\Controllers;

    use Redis;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * Show the profile for the given user.
         *
         * @param  int  $id
         * @return Response
         */
        public function showProfile($id)
        {
            $user = Redis::get('user:profile:'.$id);

            return view('user.profile', ['user' => $user]);
        }
    }

Como foi mencionado acima, você pode chamar qualquer comando Redis pelo facade `Redis`. O Laravel usa métodos "mágicos" para passar os comandos para o servidor Redis, então simplesmente passe os argumentos esperados pelo comando:

    Redis::set('name', 'Taylor');

    $values = Redis::lrange('names', 5, 10);

Caso queira, você pode passar os comandos para o servidor usando o método `command`. Esse método aceita o nome do comando como primeiro argumento e um array de valores como segundo argumento:

    $values = Redis::command('lrange', ['name', 5, 10]);

#### Usando Múltiplas Conexões Redis

Você pode receber uma instância do Redis usando o método `Redis::connection`:

    $redis = Redis::connection();

Ele irá retornar uma instância do servidor Redis padrão para você. Se não estiver utilizando clusters, você pode passar o nome do servidor como um argumento no método `connection` para receber uma instância de um servidor específico como definido no seu arquivo de configuração do Redis:

    $redis = Redis::connection('other');

<a name="pipelining-commands"></a>
### Múltiplos Comandos

Múltiplos comandos podem enviados para o servidor em uma única operação. O método `pipeline` aceita como argumento uma `Closure` que receberá uma instância do Redis. Você pode informar todos os seus comandos para esta instância Redis e todos eles serão executados dentro de uma única operação :

    Redis::pipeline(function ($pipe) {
        for ($i = 0; $i < 1000; $i++) {
            $pipe->set("key:$i", $i);
        }
    });

<a name="pubsub"></a>
## Pub / Sub

O Laravel também provê uma interface para executar os métodos `publish` e `subscribe`. Estes comandos Redis possibilitam que você aguarde por mensagens em um determinado "canal". Você pode publicar mensagens em um canal através de outra aplicação ou utilizar outra linguagem de programação, possibilitando uma integração fácil entre aplicações / processos.

Primeiramente, vamos criar um listener em um canal Redis utilizando o método `subscribe`. Nós colocaremos esse método dentro de um [comando do Artisan](/docs/{{version}}/artisan). Assim, chamar o método `subscribe` iniciará um processo em tempo real:

    <?php

    namespace App\Console\Commands;

    use Redis;
    use Illuminate\Console\Command;

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
         *
         * @return mixed
         */
        public function handle()
        {
            Redis::subscribe(['test-channel'], function($message) {
                echo $message;
            });
        }
    }

Agora nós podemos publicar mensagens neste canal utilizando o método `publish`:

    Route::get('publish', function () {
        // Route logic...

        Redis::publish('test-channel', json_encode(['foo' => 'bar']));
    });

#### Assinaturas Coringa

Utilizando o método `psubscribe` você pode assinar um canal coringa, o que é util para capturar todas as mensagens em todos os canais. O nome do canal será passado na variável `$channel` como segundo argumento no callback `Closure`:

    Redis::psubscribe(['*'], function($message, $channel) {
        echo $message;
    });

    Redis::psubscribe(['users.*'], function($message, $channel) {
        echo $message;
    });
