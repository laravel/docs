---
title: "Banco de Dados: Primeiros Passos"
---

- [Introdução](#introduction)
    - [Configuração](#configuration)
    - [Conexões de Leitura e Escrita](#read-and-write-connections)
    - [Conexões PostgreSQL com Pool](#pooled-postgresql-connections)
- [Executando Consultas SQL](#running-queries)
    - [Usando Múltiplas Conexões de Banco de Dados](#using-multiple-database-connections)
    - [Executando Consultas Analíticas no Vitess](#running-analytical-queries-on-vitess)
    - [Ouvindo Eventos de Consulta](#listening-for-query-events)
    - [Monitorando o Tempo Cumulativo de Consultas](#monitoring-cumulative-query-time)
- [Transações de Banco de Dados](#database-transactions)
- [Conectando à CLI do Banco de Dados](#connecting-to-the-database-cli)
- [Inspecionando Seus Bancos de Dados](#inspecting-your-databases)
- [Monitorando Seus Bancos de Dados](#monitoring-your-databases)

<a id="introduction"></a>
## Introdução

Quase toda aplicação web moderna interage com um banco de dados. O Laravel torna a interação com bancos de dados extremamente simples através de uma variedade de bancos de dados suportados, usando SQL puro, um [query builder fluente](../queries/) e o [ORM Eloquent](../eloquent/). Atualmente, o Laravel fornece suporte de primeira mão para cinco bancos de dados:

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([Política de Versões](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([Política de Versões](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([Política de Versões](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+ ([Política de Versões](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

Adicionalmente, o MongoDB é suportado através do pacote `mongodb/laravel-mongodb`, que é oficialmente mantido pela MongoDB. Confira a documentação do [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) para mais informações.

<a id="configuration"></a>
### Configuração

A configuração para os serviços de banco de dados do Laravel está localizada no arquivo de configuração `config/database.php` da sua aplicação. Neste arquivo, você pode definir todas as suas conexões de banco de dados, bem como especificar qual conexão deve ser usada por padrão. A maioria das opções de configuração dentro deste arquivo é orientada pelos valores das variáveis de ambiente da sua aplicação. Exemplos para a maioria dos sistemas de banco de dados suportados pelo Laravel são fornecidos neste arquivo.

Por padrão, a [configuração de ambiente](../configuration/#environment-configuration) de exemplo do Laravel está pronta para uso com o [Laravel Sail](../sail/), que é uma configuração Docker para desenvolver aplicações Laravel na sua máquina local. No entanto, você é livre para modificar a configuração do seu banco de dados conforme necessário para o seu banco de dados local.

<a id="sqlite-configuration"></a>
#### Configuração do SQLite

Bancos de dados SQLite estão contidos em um único arquivo no seu sistema de arquivos. Você pode criar um novo banco de dados SQLite usando o comando `touch` no seu terminal: `touch database/database.sqlite`. Após o banco de dados ter sido criado, você pode facilmente configurar suas variáveis de ambiente para apontar para este banco de dados, colocando o caminho absoluto do banco de dados na variável de ambiente `DB_DATABASE`:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

Por padrão, as restrições de chave estrangeira estão habilitadas para conexões SQLite. Se você quiser desabilitá-las, deve definir a variável de ambiente `DB_FOREIGN_KEYS` como `false`:

```ini
DB_FOREIGN_KEYS=false
```

> **Nota:**
> Se você usar o [instalador do Laravel](../installation/#creating-a-laravel-project) para criar sua aplicação Laravel e selecionar SQLite como seu banco de dados, o Laravel criará automaticamente um arquivo `database/database.sqlite` e executará as [migrações de banco de dados](../migrations/) padrão para você.

<a id="mssql-configuration"></a>
#### Configuração do Microsoft SQL Server

Para usar um banco de dados Microsoft SQL Server, você deve garantir que tem as extensões PHP `sqlsrv` e `pdo_sqlsrv` instaladas, bem como quaisquer dependências que elas possam exigir, como o driver Microsoft SQL ODBC.

<a id="configuration-using-urls"></a>
#### Configuração Usando URLs

Tipicamente, as conexões de banco de dados são configuradas usando múltiplos valores de configuração como `host`, `database`, `username`, `password`, etc. Cada um desses valores de configuração tem sua própria variável de ambiente correspondente. Isso significa que, ao configurar as informações de conexão do seu banco de dados em um servidor de produção, você precisa gerenciar várias variáveis de ambiente.

Alguns provedores gerenciados de banco de dados, como AWS e Heroku, fornecem uma única "URL" de banco de dados que contém todas as informações de conexão do banco de dados em uma única string. Um exemplo de URL de banco de dados pode se parecer com o seguinte:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

Essas URLs tipicamente seguem uma convenção de esquema padrão:

```html
driver://username:password@host:port/database?options
```

Por conveniência, o Laravel suporta essas URLs como uma alternativa à configuração do seu banco de dados com múltiplas opções de configuração. Se a opção de configuração `url` (ou a variável de ambiente `DB_URL` correspondente) estiver presente, ela será usada para extrair as informações de conexão e credenciais do banco de dados.

<a id="read-and-write-connections"></a>
### Conexões de Leitura e Escrita

Às vezes, você pode querer usar uma conexão de banco de dados para instruções SELECT e outra para instruções INSERT, UPDATE e DELETE. O Laravel torna isso muito fácil, e as conexões apropriadas serão sempre usadas, quer você esteja usando consultas puras, o query builder ou o ORM Eloquent.

Para ver como as conexões de leitura / escrita devem ser configuradas, vamos observar este exemplo:

```php
'mysql' => [
    'driver' => 'mysql',
    
    'read' => [
        'host' => [
            '192.168.1.1',
            '196.168.1.2',
        ],
    ],
    'write' => [
        'host' => [
            '192.168.1.3',
        ],
    ],
    'sticky' => true,
    
    'port' => env('DB_PORT', '3306'),
    'database' => env('DB_DATABASE', 'laravel'),
    'username' => env('DB_USERNAME', 'root'),
    'password' => env('DB_PASSWORD', ''),
    'unix_socket' => env('DB_SOCKET', ''),
    'charset' => env('DB_CHARSET', 'utf8mb4'),
    'collation' => env('DB_COLLATION', 'utf8mb4_unicode_ci'),
    'prefix' => '',
    'prefix_indexes' => true,
    'strict' => true,
    'engine' => null,
    'options' => extension_loaded('pdo_mysql') ? array_filter([
        (PHP_VERSION_ID >= 80500 ? \Pdo\Mysql::ATTR_SSL_CA : \PDO::MYSQL_ATTR_SSL_CA) => env('MYSQL_ATTR_SSL_CA'),
    ]) : [],
],
```

Observe que três chaves foram adicionadas ao array de configuração: `read`, `write` e `sticky`. As chaves `read` e `write` têm valores de array contendo uma única chave: `host`. O restante das opções de banco de dados para as conexões `read` e `write` será mesclado a partir do array de configuração `mysql` principal.

Você só precisa colocar itens nos arrays `read` e `write` se quiser sobrescrever os valores do array `mysql` principal. Então, neste caso, `192.168.1.1` será usado como host para a conexão de "leitura", enquanto `192.168.1.3` será usado para a conexão de "escrita". As credenciais do banco de dados, o prefixo, o conjunto de caracteres e todas as outras opções no array `mysql` principal serão compartilhadas entre ambas as conexões. Quando existem múltiplos valores no array de configuração `host`, um host de banco de dados será escolhido aleatoriamente para cada requisição.

<a id="the-sticky-option"></a>
#### A Opção `sticky`

A opção `sticky` é um valor *opcional* que pode ser usado para permitir a leitura imediata de registros que foram escritos no banco de dados durante o ciclo de requisição atual. Se a opção `sticky` estiver habilitada e uma operação de "escrita" tiver sido realizada contra o banco de dados durante o ciclo de requisição atual, quaisquer operações de "leitura" posteriores usarão a conexão de "escrita". Isso garante que quaisquer dados escritos durante o ciclo de requisição possam ser lidos imediatamente de volta do banco de dados durante essa mesma requisição. Cabe a você decidir se este é o comportamento desejado para sua aplicação.

<a id="pooled-postgresql-connections"></a>
### Conexões PostgreSQL com Pool

Muitos provedores gerenciados de PostgreSQL oferecem pool de conexões em modo de transação através de serviços como PgBouncer ou proxy de conexões. Esses pools são ideais para consultas de aplicação, mas algumas operações de schema, migrações e comandos de manutenção exigem uma conexão direta com o banco de dados.

Para usar um pool de transações com PostgreSQL, configure a conexão com pool normalmente e forneça os detalhes da conexão direta através da opção de configuração `direct`:

```php
'pgsql' => [
    'driver' => 'pgsql',
    // ...
    'pooled' => env('DB_POOLED', false),
    'direct' => array_filter([
        'host' => env('DB_DIRECT_HOST'),
        'port' => env('DB_DIRECT_PORT'),
        'username' => env('DB_DIRECT_USERNAME'),
        'password' => env('DB_DIRECT_PASSWORD'),
        'sslmode' => env('DB_DIRECT_SSLMODE'),
    ]),
],
```

Quando uma conexão PostgreSQL é configurada como com pool, o Laravel habilita automaticamente prepares emulados para a conexão com pool. A conexão direta herda quaisquer opções não definidas explicitamente na configuração `direct` e usa prepares nativos por padrão.

O Laravel usa automaticamente a conexão direta para migrações, dumps e restaurações de schema, `db:wipe`, `db:show` e `db:table`. O comando `db` também usa a conexão direta por padrão quando o modo com pool está habilitado e uma conexão direta está configurada; você pode passar a opção `--pooled` para conectar-se à conexão com pool em vez disso:

```shell
php artisan db --pooled
```

Se você precisar usar explicitamente a conexão direta na sua aplicação, adicione o sufixo `::direct` ao nome da conexão:

```php
DB::connection('pgsql::direct')->statement('create extension if not exists "uuid-ossp"');
```

<a id="running-queries"></a>
## Executando Consultas SQL

Uma vez que você tenha configurado sua conexão de banco de dados, você pode executar consultas usando a facade `DB`. A facade `DB` fornece métodos para cada tipo de consulta: `select`, `update`, `insert`, `delete` e `statement`.

<a id="running-a-select-query"></a>
#### Executando uma Consulta Select

Para executar uma consulta SELECT básica, você pode usar o método `select` na facade `DB`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show a list of all of the application's users.
     */
    public function index(): View
    {
        $users = DB::select('select * from users where active = ?', [1]);

        return view('user.index', ['users' => $users]);
    }
}
```

O primeiro argumento passado para o método `select` é a consulta SQL, enquanto o segundo argumento são quaisquer vinculações de parâmetros que precisam ser vinculadas à consulta. Tipicamente, estes são os valores das restrições da cláusula `where`. A vinculação de parâmetros fornece proteção contra injeção de SQL.

O método `select` sempre retornará um `array` de resultados. Cada resultado dentro do array será um objeto `stdClass` do PHP representando um registro do banco de dados:

```php
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```

<a id="selecting-scalar-values"></a>
#### Selecionando Valores Escalares

Às vezes, sua consulta de banco de dados pode resultar em um único valor escalar. Em vez de ser obrigado a recuperar o resultado escalar da consulta a partir de um objeto de registro, o Laravel permite que você recupere esse valor diretamente usando o método `scalar`:

```php
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a id="selecting-multiple-result-sets"></a>
#### Selecionando Múltiplos Conjuntos de Resultados

Se sua aplicação chamar stored procedures que retornam múltiplos conjuntos de resultados, você pode usar o método `selectResultSets` para recuperar todos os conjuntos de resultados retornados pela stored procedure:

```php
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", [$request->user()->id]
);
```

<a id="using-named-bindings"></a>
#### Usando Vinculações Nomeadas

Em vez de usar `?` para representar suas vinculações de parâmetros, você pode executar uma consulta usando vinculações nomeadas:

```php
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a id="running-an-insert-statement"></a>
#### Executando uma Instrução Insert

Para executar uma instrução `insert`, você pode usar o método `insert` na facade `DB`. Assim como o `select`, este método aceita a consulta SQL como seu primeiro argumento e as vinculações como seu segundo argumento:

```php
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a id="running-an-update-statement"></a>
#### Executando uma Instrução Update

O método `update` deve ser usado para atualizar registros existentes no banco de dados. O número de linhas afetadas pela instrução é retornado pelo método:

```php
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```

<a id="running-a-delete-statement"></a>
#### Executando uma Instrução Delete

O método `delete` deve ser usado para deletar registros do banco de dados. Assim como o `update`, o número de linhas afetadas será retornado pelo método:

```php
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a id="running-a-general-statement"></a>
#### Executando uma Instrução Geral

Algumas instruções de banco de dados não retornam nenhum valor. Para esses tipos de operações, você pode usar o método `statement` na facade `DB`:

```php
DB::statement('drop table users');
```

<a id="running-an-unprepared-statement"></a>
#### Executando uma Instrução Não Preparada

Às vezes, você pode querer executar uma instrução SQL sem vincular nenhum valor. Você pode usar o método `unprepared` da facade `DB` para fazer isso:

```php
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> **Aviso:**
> Como instruções não preparadas não vinculam parâmetros, elas podem estar vulneráveis a injeção de SQL. Você nunca deve permitir valores controlados pelo usuário dentro de uma instrução não preparada.

<a id="implicit-commits-in-transactions"></a>
#### Commits Implícitos

Ao usar os métodos `statement` e `unprepared` da facade `DB` dentro de transações, você deve ter cuidado para evitar instruções que causem [commits implícitos](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html). Essas instruções farão com que o engine do banco de dados faça commit indiretamente de toda a transação, deixando o Laravel sem conhecimento do nível de transação do banco de dados. Um exemplo de tal instrução é a criação de uma tabela de banco de dados:

```php
DB::unprepared('create table a (col varchar(1) null)');
```

Por favor, consulte o manual do MySQL para [uma lista de todas as instruções](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) que acionam commits implícitos.

<a id="using-multiple-database-connections"></a>
### Usando Múltiplas Conexões de Banco de Dados

Se sua aplicação define múltiplas conexões no seu arquivo de configuração `config/database.php`, você pode acessar cada conexão através do método `connection` fornecido pela facade `DB`. O nome da conexão passado para o método `connection` deve corresponder a uma das conexões listadas no seu arquivo de configuração `config/database.php` ou configurada em tempo de execução usando o helper `config`:

```php
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

Você pode acessar a instância PDO bruta e subjacente de uma conexão usando o método `getPdo` em uma instância de conexão:

```php
$pdo = DB::connection()->getPdo();
```

<a id="running-analytical-queries-on-vitess"></a>
### Executando Consultas Analíticas no Vitess

Ao usar um banco de dados Vitess, como o PlanetScale, você pode usar o método `olap` para executar consultas analíticas usando a workload OLAP:

```php
use Illuminate\Support\Facades\DB;

$totals = DB::connection('mysql')->olap(fn ($connection) => $connection->table('orders')
    ->selectRaw('customer_id, sum(total) as total')
    ->groupBy('customer_id')
    ->get()
);
```

O Laravel define a workload em ambas as conexões de leitura e escrita e, em seguida, a redefine para OLTP quando o callback termina, mesmo que uma exceção seja lançada. O método `olap` retorna o resultado do callback. Em conexões MySQL que não usam Vitess, o callback é executado sem alterar a workload.

Você pode determinar se uma conexão MySQL está usando Vitess através do método `isVitess`:

```php
$isVitess = DB::connection('mysql')->isVitess();
```

<a id="listening-for-query-events"></a>
### Ouvindo Eventos de Consulta

Se você quiser especificar uma closure que é invocada para cada consulta SQL executada pela sua aplicação, você pode usar o método `listen` da facade `DB`. Este método pode ser útil para registrar logs de consultas ou depuração. Você pode registrar sua closure listener de consultas no método `boot` de um [service provider](../providers/):

```php
<?php

namespace App\Providers;

use Illuminate\Database\Events\QueryExecuted;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        DB::listen(function (QueryExecuted $query) {
            // $query->sql;
            // $query->bindings;
            // $query->time;
            // $query->toRawSql();
        });
    }
}
```

<a id="monitoring-cumulative-query-time"></a>
### Monitorando o Tempo Cumulativo de Consultas

Um gargalo de desempenho comum das aplicações web modernas é a quantidade de tempo que elas gastam consultando bancos de dados. Felizmente, o Laravel pode invocar uma closure ou callback de sua escolha quando ele gasta tempo demais consultando o banco de dados durante uma única requisição. Para começar, forneça um limite de tempo de consulta (em milissegundos) e uma closure ao método `whenQueryingForLongerThan`. Você pode invocar este método no método `boot` de um [service provider](../providers/):

```php
<?php

namespace App\Providers;

use Illuminate\Database\Connection;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;
use Illuminate\Database\Events\QueryExecuted;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        DB::whenQueryingForLongerThan(500, function (Connection $connection, QueryExecuted $event) {
            // Notify development team...
        });
    }
}
```

<a id="database-transactions"></a>
## Transações de Banco de Dados

Você pode usar o método `transaction` fornecido pela facade `DB` para executar um conjunto de operações dentro de uma transação de banco de dados. Se uma exceção for lançada dentro da closure da transação, a transação será automaticamente revertida (rollback) e a exceção será relançada. Se a closure for executada com sucesso, a transação será automaticamente confirmada (commit). Você não precisa se preocupar em reverter ou confirmar manualmente ao usar o método `transaction`:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```

<a id="handling-deadlocks"></a>
#### Lidando com Deadlocks

O método `transaction` aceita um segundo argumento opcional que define o número de vezes que uma transação deve ser repetida quando ocorre um deadlock. Uma vez que essas tentativas tenham se esgotado, uma exceção será lançada:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, attempts: 5);
```

<a id="manually-using-transactions"></a>
#### Usando Transações Manualmente

Se você quiser iniciar uma transação manualmente e ter controle completo sobre rollbacks e commits, você pode usar o método `beginTransaction` fornecido pela facade `DB`:

```php
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

Você pode reverter a transação através do método `rollBack`:

```php
DB::rollBack();
```

Por fim, você pode confirmar uma transação através do método `commit`:

```php
DB::commit();
```

> **Nota:**
> Os métodos de transação da facade `DB` controlam as transações tanto para o [query builder](../queries/) quanto para o [ORM Eloquent](../eloquent/).

<a id="connecting-to-the-database-cli"></a>
## Conectando à CLI do Banco de Dados

Se você quiser conectar-se à CLI do seu banco de dados, você pode usar o comando Artisan `db`:

```shell
php artisan db
```

Se necessário, você pode especificar um nome de conexão de banco de dados para conectar-se a uma conexão de banco de dados que não seja a conexão padrão:

```shell
php artisan db mysql
```

<a id="inspecting-your-databases"></a>
## Inspecionando Seus Bancos de Dados

Usando os comandos Artisan `db:show` e `db:table`, você pode obter informações valiosas sobre seu banco de dados e suas tabelas associadas. Para ver uma visão geral do seu banco de dados, incluindo seu tamanho, tipo, número de conexões abertas e um resumo de suas tabelas, você pode usar o comando `db:show`:

```shell
php artisan db:show
```

Você pode especificar qual conexão de banco de dados deve ser inspecionada fornecendo o nome da conexão de banco de dados ao comando através da opção `--database`:

```shell
php artisan db:show --database=pgsql
```

Se você quiser incluir contagens de linhas das tabelas e detalhes das views do banco de dados na saída do comando, você pode fornecer as opções `--counts` e `--views`, respectivamente. Em bancos de dados grandes, recuperar contagens de linhas e detalhes de views pode ser lento:

```shell
php artisan db:show --counts --views
```

Além disso, você pode usar os seguintes métodos do `Schema` para inspecionar seu banco de dados:

```php
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```

Se você quiser inspecionar uma conexão de banco de dados que não seja a conexão padrão da sua aplicação, você pode usar o método `connection`:

```php
$columns = Schema::connection('sqlite')->getColumns('users');
```

<a id="table-overview"></a>
#### Visão Geral da Tabela

Se você quiser obter uma visão geral de uma tabela individual dentro do seu banco de dados, você pode executar o comando Artisan `db:table`. Este comando fornece uma visão geral de uma tabela de banco de dados, incluindo suas colunas, tipos, atributos, chaves e índices:

```shell
php artisan db:table users
```

<a id="monitoring-your-databases"></a>
## Monitorando Seus Bancos de Dados

Usando o comando Artisan `db:monitor`, você pode instruir o Laravel a despachar um evento `Illuminate\Database\Events\DatabaseBusy` se o seu banco de dados estiver gerenciando mais do que um número especificado de conexões abertas.

Para começar, você deve agendar o comando `db:monitor` para [ser executado a cada minuto](../scheduling/). O comando aceita os nomes das configurações de conexão de banco de dados que você deseja monitorar, bem como o número máximo de conexões abertas que devem ser toleradas antes de despachar um evento:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

Agendar apenas este comando não é suficiente para disparar uma notificação alertando você sobre o número de conexões abertas. Quando o comando encontra um banco de dados que tem uma contagem de conexões abertas que excede seu limite, um evento `DatabaseBusy` será despachado. Você deve ouvir este evento dentro do `AppServiceProvider` da sua aplicação para enviar uma notificação a você ou à sua equipe de desenvolvimento:

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (DatabaseBusy $event) {
        Notification::route('mail', 'dev@example.com')
            ->notify(new DatabaseApproachingMaxConnections(
                $event->connectionName,
                $event->connections
            ));
    });
}
```
