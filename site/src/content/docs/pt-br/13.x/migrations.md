---
title: "Banco de Dados: Migrations"
---

- [Introdução](#introduction)
- [Gerando Migrations](#generating-migrations)
    - [Comprimindo Migrations](#squashing-migrations)
- [Estrutura da Migration](#migration-structure)
- [Executando Migrations](#running-migrations)
    - [Revertendo Migrations](#rolling-back-migrations)
- [Tabelas](#tables)
    - [Criando Tabelas](#creating-tables)
    - [Atualizando Tabelas](#updating-tables)
    - [Renomeando / Removendo Tabelas](#renaming-and-dropping-tables)
- [Colunas](#columns)
    - [Criando Colunas](#creating-columns)
    - [Tipos de Coluna Disponíveis](#available-column-types)
    - [Modificadores de Coluna](#column-modifiers)
    - [Modificando Colunas](#modifying-columns)
    - [Renomeando Colunas](#renaming-columns)
    - [Removendo Colunas](#dropping-columns)
- [Índices](#indexes)
    - [Criando Índices](#creating-indexes)
    - [Renomeando Índices](#renaming-indexes)
    - [Removendo Índices](#dropping-indexes)
    - [Restrições de Chave Estrangeira](#foreign-key-constraints)
- [Eventos](#events)

<a id="introduction"></a>
## Introdução

Migrations são como controle de versão para seu banco de dados, permitindo que sua equipe defina e compartilhe a definição do esquema do banco de dados da aplicação. Se você já precisou pedir a um colega para adicionar manualmente uma coluna ao seu esquema de banco de dados local após puxar suas alterações do controle de versão, você enfrentou o problema que as migrations do banco de dados resolvem.

A [facade](../facades/) `Schema` do Laravel fornece suporte independente de banco de dados para criar e manipular tabelas em todos os sistemas de banco de dados suportados pelo Laravel. Normalmente, as migrations usam essa facade para criar e modificar tabelas e colunas do banco de dados.

<a id="generating-migrations"></a>
## Gerando Migrations

Você pode usar o [comando Artisan](../artisan/) `make:migration` para gerar uma migration de banco de dados. A nova migration será colocada no diretório `database/migrations`. Cada nome de arquivo de migration contém um timestamp que permite ao Laravel determinar a ordem das migrations:

```shell
php artisan make:migration create_flights_table
```

O Laravel usará o nome da migration para tentar adivinhar o nome da tabela e se a migration criará ou não uma nova tabela. Se o Laravel conseguir determinar o nome da tabela a partir do nome da migration, ele pré-preencherá o arquivo de migration gerado com a tabela especificada. Caso contrário, você pode simplesmente especificar a tabela no arquivo de migration manualmente.

Se você quiser especificar um caminho personalizado para a migration gerada, pode usar a opção `--path` ao executar o comando `make:migration`. O caminho fornecido deve ser relativo ao caminho base da sua aplicação.

> **Nota:**
> Os stubs de migration podem ser personalizados usando [publicação de stubs](../artisan/#stub-customization).

<a id="squashing-migrations"></a>
### Comprimindo Migrations

Conforme você constrói sua aplicação, pode acumular cada vez mais migrations ao longo do tempo. Isso pode fazer com que seu diretório `database/migrations` fique inchado com potencialmente centenas de migrations. Se desejar, você pode "comprimir" suas migrations em um único arquivo SQL. Para começar, execute o comando `schema:dump`:

```shell
php artisan schema:dump

# Dump the current database schema and prune all existing migrations...
php artisan schema:dump --prune
```

Quando você executa esse comando, o Laravel gravará um arquivo "schema" no diretório `database/schema` da sua aplicação. O nome do arquivo de schema corresponderá à conexão de banco de dados. Agora, quando você tentar migrar seu banco de dados e nenhuma outra migration tiver sido executada, o Laravel primeiro executará as instruções SQL no arquivo de schema da conexão de banco de dados que você está usando. Após executar as instruções SQL do arquivo de schema, o Laravel executará quaisquer migrations restantes que não faziam parte do dump do schema.

Se os testes da sua aplicação usam uma conexão de banco de dados diferente daquela que você normalmente usa durante o desenvolvimento local, você deve garantir que tenha feito dump de um arquivo de schema usando essa conexão de banco de dados para que seus testes possam construir seu banco de dados. Você pode desejar fazer isso após fazer o dump da conexão de banco de dados que normalmente usa durante o desenvolvimento local:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

Você deve fazer commit do arquivo de schema do banco de dados no controle de versão para que outros novos desenvolvedores da sua equipe possam criar rapidamente a estrutura inicial do banco de dados da sua aplicação.

> **Aviso:**
> A compressão de migrations está disponível apenas para os bancos de dados MariaDB, MySQL, PostgreSQL e SQLite e utiliza o cliente de linha de comando do banco de dados.

<a id="migration-structure"></a>
## Estrutura da Migration

Uma classe de migration contém dois métodos: `up` e `down`. O método `up` é usado para adicionar novas tabelas, colunas ou índices ao seu banco de dados, enquanto o método `down` deve reverter as operações realizadas pelo método `up`.

Dentro de ambos os métodos, você pode usar o construtor de esquema do Laravel para criar e modificar tabelas de forma expressiva. Para aprender sobre todos os métodos disponíveis no construtor `Schema`, [confira sua documentação](#creating-tables). Por exemplo, a seguinte migration cria uma tabela `flights`:

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('flights', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('airline');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::drop('flights');
    }
};
```

<a id="setting-the-migration-connection"></a>
#### Definindo a Conexão da Migration

Se sua migration interagirá com uma conexão de banco de dados diferente da conexão de banco de dados padrão da sua aplicação, você deve definir a propriedade `$connection` da sua migration:

```php
/**
 * The database connection that should be used by the migration.
 *
 * @var string
 */
protected $connection = 'pgsql';

/**
 * Run the migrations.
 */
public function up(): void
{
    // ...
}
```

<a id="skipping-migrations"></a>
#### Ignorando Migrations

Às vezes, uma migration pode ser destinada a suportar um recurso que ainda não está ativo e você não deseja que ela seja executada ainda. Neste caso, você pode definir um método `shouldRun` na migration. Se o método `shouldRun` retornar `false`, a migration será ignorada:

```php
use App\Models\Flight;
use Laravel\Pennant\Feature;

/**
 * Determine if this migration should run.
 */
public function shouldRun(): bool
{
    return Feature::active(Flight::class);
}
```

<a id="running-migrations"></a>
## Executando Migrations

Para executar todas as suas migrations pendentes, execute o comando Artisan `migrate`:

```shell
php artisan migrate
```

Se você quiser ver quais migrations já foram executadas e quais ainda estão pendentes, pode usar o comando Artisan `migrate:status`:

```shell
php artisan migrate:status
```

Se você fornecer a opção `--step` ao comando `migrate`, o comando executará cada migration como seu próprio lote, permitindo que você reverter migrations individuais mais tarde usando o comando `migrate:rollback`:

```shell
php artisan migrate --step
```

Se você quiser ver as instruções SQL que serão executadas pelas migrations sem realmente executá-las, pode fornecer o sinalizador `--pretend` ao comando `migrate`:

```shell
php artisan migrate --pretend
```

<a id="isolating-migration-execution"></a>
#### Isolando a Execução da Migration

Se você está implantando sua aplicação em múltiplos servidores e executando migrations como parte do seu processo de implantação, provavelmente não deseja que dois servidores tentem migrar o banco de dados ao mesmo tempo. Para evitar isso, você pode usar a opção `isolated` ao invocar o comando `migrate`.

Quando a opção `isolated` é fornecida, o Laravel adquire um lock atômico usando o driver de cache da sua aplicação antes de tentar executar suas migrations. Todas as outras tentativas de executar o comando `migrate` enquanto esse lock estiver sendo mantido não serão executadas; no entanto, o comando ainda sairá com um código de status de saída bem-sucedido:

```shell
php artisan migrate --isolated
```

> **Aviso:**
> Para utilizar este recurso, sua aplicação deve estar usando o driver de cache `memcached`, `redis`, `dynamodb`, `database`, `file` ou `array` como driver de cache padrão da sua aplicação. Além disso, todos os servidores devem estar se comunicando com o mesmo servidor de cache central.

<a id="forcing-migrations-to-run-in-production"></a>
#### Forçando a Execução de Migrations em Produção

Algumas operações de migration são destrutivas, o que significa que podem causar perda de dados. Para protegê-lo de executar esses comandos em seu banco de dados de produção, você será solicitado a confirmar antes que os comandos sejam executados. Para forçar os comandos a serem executados sem um prompt, use o sinalizador `--force`:

```shell
php artisan migrate --force
```

<a id="rolling-back-migrations"></a>
### Revertendo Migrations

Para reverter a última operação de migration, você pode usar o comando Artisan `rollback`. Este comando reverte o último "lote" de migrations, que pode incluir múltiplos arquivos de migration:

```shell
php artisan migrate:rollback
```

Você pode reverter um número limitado de migrations fornecendo a opção `step` ao comando `rollback`. Por exemplo, o seguinte comando reverterá as últimas cinco migrations:

```shell
php artisan migrate:rollback --step=5
```

Você pode reverter um "lote" específico de migrations fornecendo a opção `batch` ao comando `rollback`, onde a opção `batch` corresponde a um valor de lote dentro da tabela de banco de dados `migrations` da sua aplicação. Por exemplo, o seguinte comando reverterá todas as migrations do lote três:

```shell
php artisan migrate:rollback --batch=3
```

Se você quiser ver as instruções SQL que serão executadas pelas migrations sem realmente executá-las, pode fornecer o sinalizador `--pretend` ao comando `migrate:rollback`:

```shell
php artisan migrate:rollback --pretend
```

O comando `migrate:reset` reverterá todas as migrations da sua aplicação:

```shell
php artisan migrate:reset
```

<a id="roll-back-migrate-using-a-single-command"></a>
#### Revertendo e Migrando Usando um Único Comando

O comando `migrate:refresh` reverterá todas as suas migrations e depois executará o comando `migrate`. Este comando efetivamente recria todo o seu banco de dados:

```shell
php artisan migrate:refresh

# Refresh the database and run all database seeds...
php artisan migrate:refresh --seed
```

Você pode reverter e re-migrar um número limitado de migrations fornecendo a opção `step` ao comando `refresh`. Por exemplo, o seguinte comando reverterá e re-migrará as últimas cinco migrations:

```shell
php artisan migrate:refresh --step=5
```

<a id="drop-all-tables-migrate"></a>
#### Removendo Todas as Tabelas e Migrando

O comando `migrate:fresh` removerá todas as tabelas do banco de dados e depois executará o comando `migrate`:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

Por padrão, o comando `migrate:fresh` remove apenas tabelas da conexão de banco de dados padrão. No entanto, você pode usar a opção `--database` para especificar a conexão de banco de dados que deve ser migrada. O nome da conexão de banco de dados deve corresponder a uma conexão definida no [arquivo de configuração](../configuration/) `database` da sua aplicação:

```shell
php artisan migrate:fresh --database=admin
```

> **Aviso:**
> O comando `migrate:fresh` removerá todas as tabelas do banco de dados, independentemente de seu prefixo. Este comando deve ser usado com cautela ao desenvolver em um banco de dados que é compartilhado com outras aplicações.

<a id="tables"></a>
## Tabelas

<a id="creating-tables"></a>
### Criando Tabelas

Para criar uma nova tabela de banco de dados, use o método `create` na facade `Schema`. O método `create` aceita dois argumentos: o primeiro é o nome da tabela, enquanto o segundo é um closure que recebe um objeto `Blueprint` que pode ser usado para definir a nova tabela:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('email');
    $table->timestamps();
});
```

Ao criar a tabela, você pode usar qualquer um dos [métodos de coluna](#creating-columns) do construtor de esquema para definir as colunas da tabela.

<a id="determining-table-column-existence"></a>
#### Determinando a Existência de Tabela / Coluna

Você pode determinar a existência de uma tabela, coluna ou índice usando os métodos `hasTable`, `hasColumn` e `hasIndex`:

```php
if (Schema::hasTable('users')) {
    // The "users" table exists...
}

if (Schema::hasColumn('users', 'email')) {
    // The "users" table exists and has an "email" column...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // The "users" table exists and has a unique index on the "email" column...
}
```

<a id="database-connection-table-options"></a>
#### Conexão de Banco de Dados e Opções de Tabela

Se você deseja realizar uma operação de esquema em uma conexão de banco de dados que não é a conexão padrão da sua aplicação, use o método `connection`:

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

Além disso, algumas outras propriedades e métodos podem ser usados para definir outros aspectos da criação da tabela. A propriedade `engine` pode ser usada para especificar o mecanismo de armazenamento da tabela ao usar MariaDB ou MySQL:

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

As propriedades `charset` e `collation` podem ser usadas para especificar o conjunto de caracteres e a ordenação para a tabela criada ao usar MariaDB ou MySQL:

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

O método `temporary` pode ser usado para indicar que a tabela deve ser "temporária". Tabelas temporárias são visíveis apenas para a sessão de banco de dados da conexão atual e são removidas automaticamente quando a conexão é fechada:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

Se você quiser adicionar um "comentário" a uma tabela de banco de dados, pode invocar o método `comment` na instância da tabela. Comentários de tabela são atualmente suportados apenas por MariaDB, MySQL e PostgreSQL:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a id="updating-tables"></a>
### Atualizando Tabelas

O método `table` na facade `Schema` pode ser usado para atualizar tabelas existentes. Assim como o método `create`, o método `table` aceita dois argumentos: o nome da tabela e um closure que recebe uma instância `Blueprint` que você pode usar para adicionar colunas ou índices à tabela:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a id="renaming-and-dropping-tables"></a>
### Renomeando / Removendo Tabelas

Para renomear uma tabela de banco de dados existente, use o método `rename`:

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

Para remover uma tabela existente, você pode usar os métodos `drop` ou `dropIfExists`:

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a id="renaming-tables-with-foreign-keys"></a>
#### Renomeando Tabelas com Chaves Estrangeiras

Antes de renomear uma tabela, você deve verificar se todas as restrições de chave estrangeira na tabela possuem um nome explícito nos seus arquivos de migration em vez de deixar o Laravel atribuir um nome baseado em convenção. Caso contrário, o nome da restrição de chave estrangeira se referirá ao nome antigo da tabela.

<a id="columns"></a>
## Colunas

<a id="creating-columns"></a>
### Criando Colunas

O método `table` na facade `Schema` pode ser usado para atualizar tabelas existentes. Assim como o método `create`, o método `table` aceita dois argumentos: o nome da tabela e um closure que recebe uma instância `Illuminate\Database\Schema\Blueprint` que você pode usar para adicionar colunas à tabela:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a id="available-column-types"></a>
### Tipos de Coluna Disponíveis

O blueprint do construtor de esquema oferece uma variedade de métodos que correspondem aos diferentes tipos de colunas que você pode adicionar às suas tabelas de banco de dados. Cada um dos métodos disponíveis está listado na tabela abaixo:

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .collection-method code {
        font-size: 14px;
    }

    .collection-method:not(.first-collection-method) {
        margin-top: 50px;
    }
</style>

<a id="booleans-method-list"></a>
#### Tipos Boolean

<div class="collection-method-list" markdown="1">

[boolean](#column-method-boolean)

</div>

<a id="strings-and-texts-method-list"></a>
#### Tipos String & Text

<div class="collection-method-list" markdown="1">

[char](#column-method-char)
[longText](#column-method-longText)
[mediumText](#column-method-mediumText)
[string](#column-method-string)
[text](#column-method-text)
[tinyText](#column-method-tinyText)

</div>

<a id="numbers--method-list"></a>
#### Tipos Numéricos

<div class="collection-method-list" markdown="1">

[bigIncrements](#column-method-bigIncrements)
[bigInteger](#column-method-bigInteger)
[decimal](#column-method-decimal)
[double](#column-method-double)
[float](#column-method-float)
[id](#column-method-id)
[increments](#column-method-increments)
[integer](#column-method-integer)
[mediumIncrements](#column-method-mediumIncrements)
[mediumInteger](#column-method-mediumInteger)
[smallIncrements](#column-method-smallIncrements)
[smallInteger](#column-method-smallInteger)
[tinyIncrements](#column-method-tinyIncrements)
[tinyInteger](#column-method-tinyInteger)
[unsignedBigInteger](#column-method-unsignedBigInteger)
[unsignedInteger](#column-method-unsignedInteger)
[unsignedMediumInteger](#column-method-unsignedMediumInteger)
[unsignedSmallInteger](#column-method-unsignedSmallInteger)
[unsignedTinyInteger](#column-method-unsignedTinyInteger)

</div>

<a id="dates-and-times-method-list"></a>
#### Tipos Date & Time

<div class="collection-method-list" markdown="1">

[dateTime](#column-method-dateTime)
[dateTimeTz](#column-method-dateTimeTz)
[date](#column-method-date)
[time](#column-method-time)
[timeTz](#column-method-timeTz)
[timestamp](#column-method-timestamp)
[timestamps](#column-method-timestamps)
[timestampsTz](#column-method-timestampsTz)
[softDeletes](#column-method-softDeletes)
[softDeletesTz](#column-method-softDeletesTz)
[year](#column-method-year)

</div>

<a id="binaries-method-list"></a>
#### Tipos Binary

<div class="collection-method-list" markdown="1">

[binary](#column-method-binary)

</div>

<a id="object-and-jsons-method-list"></a>
#### Tipos Object & Json

<div class="collection-method-list" markdown="1">

[json](#column-method-json)
[jsonb](#column-method-jsonb)

</div>

<a id="uuids-and-ulids-method-list"></a>
#### Tipos UUID & ULID

<div class="collection-method-list" markdown="1">

[ulid](#column-method-ulid)
[ulidMorphs](#column-method-ulidMorphs)
[uuid](#column-method-uuid)
[uuidMorphs](#column-method-uuidMorphs)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)

</div>

<a id="spatials-method-list"></a>
#### Tipos Spatial

<div class="collection-method-list" markdown="1">

[geography](#column-method-geography)
[geometry](#column-method-geometry)

</div>

<a id="relationship-method-list"></a>
#### Tipos de Relacionamento

<div class="collection-method-list" markdown="1">

[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[foreignUuidFor](#column-method-foreignUuidFor)
[morphs](#column-method-morphs)
[nullableMorphs](#column-method-nullableMorphs)

</div>

<a id="specifics-method-list"></a>
#### Tipos Especiais

<div class="collection-method-list" markdown="1">

[enum](#column-method-enum)
[set](#column-method-set)
[macAddress](#column-method-macAddress)
[ipAddress](#column-method-ipAddress)
[rememberToken](#column-method-rememberToken)
[vector](#column-method-vector)

</div>

<a id="column-method-bigIncrements"></a>
#### `bigIncrements()` {.collection-method .first-collection-method}

O método `bigIncrements` cria uma coluna equivalente a `UNSIGNED BIGINT` auto-incrementável (chave primária):

```php
$table->bigIncrements('id');
```

<a id="column-method-bigInteger"></a>
#### `bigInteger()` {.collection-method}

O método `bigInteger` cria uma coluna equivalente a `BIGINT`:

```php
$table->bigInteger('votes');
```

<a id="column-method-binary"></a>
#### `binary()` {.collection-method}

O método `binary` cria uma coluna equivalente a `BLOB`:

```php
$table->binary('photo');
```

Ao utilizar MySQL, MariaDB ou SQL Server, você pode passar os argumentos `length` e `fixed` para criar uma coluna equivalente a `VARBINARY` ou `BINARY`:

```php
$table->binary('data', length: 16); // VARBINARY(16)

$table->binary('data', length: 16, fixed: true); // BINARY(16)
```

<a id="column-method-boolean"></a>
#### `boolean()` {.collection-method}

O método `boolean` cria uma coluna equivalente a `BOOLEAN`:

```php
$table->boolean('confirmed');
```

<a id="column-method-char"></a>
#### `char()` {.collection-method}

O método `char` cria uma coluna equivalente a `CHAR` com um determinado comprimento:

```php
$table->char('name', length: 100);
```

<a id="column-method-dateTimeTz"></a>
#### `dateTimeTz()` {.collection-method}

O método `dateTimeTz` cria uma coluna equivalente a `DATETIME` (com fuso horário) com precisão opcional de frações de segundo:

```php
$table->dateTimeTz('created_at', precision: 0);
```

<a id="column-method-dateTime"></a>
#### `dateTime()` {.collection-method}

O método `dateTime` cria uma coluna equivalente a `DATETIME` com precisão opcional de frações de segundo:

```php
$table->dateTime('created_at', precision: 0);
```

<a id="column-method-date"></a>
#### `date()` {.collection-method}

O método `date` cria uma coluna equivalente a `DATE`:

```php
$table->date('created_at');
```

<a id="column-method-decimal"></a>
#### `decimal()` {.collection-method}

O método `decimal` cria uma coluna equivalente a `DECIMAL` com a precisão (dígitos totais) e escala (dígitos decimais) fornecidas:

```php
$table->decimal('amount', total: 8, places: 2);
```

<a id="column-method-double"></a>
#### `double()` {.collection-method}

O método `double` cria uma coluna equivalente a `DOUBLE`:

```php
$table->double('amount');
```

<a id="column-method-enum"></a>
#### `enum()` {.collection-method}

O método `enum` cria uma coluna equivalente a `ENUM` com os valores válidos fornecidos:

```php
$table->enum('difficulty', ['easy', 'hard']);
```

É claro que você pode usar o método `Enum::cases()` em vez de definir manualmente um array de valores permitidos:

```php
use App\Enums\Difficulty;

$table->enum('difficulty', Difficulty::cases());
```

<a id="column-method-float"></a>
#### `float()` {.collection-method}

O método `float` cria uma coluna equivalente a `FLOAT` com a precisão fornecida:

```php
$table->float('amount', precision: 53);
```

<a id="column-method-foreignId"></a>
#### `foreignId()` {.collection-method}

O método `foreignId` cria uma coluna equivalente a `UNSIGNED BIGINT`:

```php
$table->foreignId('user_id');
```

<a id="column-method-foreignIdFor"></a>
#### `foreignIdFor()` {.collection-method}

O método `foreignIdFor` adiciona uma coluna equivalente a `{column}_id` para uma determinada classe de modelo. O tipo da coluna será `UNSIGNED BIGINT`, `CHAR(36)` ou `CHAR(26)` dependendo do tipo de chave do modelo:

```php
$table->foreignIdFor(User::class);
```

<a id="column-method-foreignUlid"></a>
#### `foreignUlid()` {.collection-method}

O método `foreignUlid` cria uma coluna equivalente a `ULID`:

```php
$table->foreignUlid('user_id');
```

<a id="column-method-foreignUuid"></a>
#### `foreignUuid()` {.collection-method}

O método `foreignUuid` cria uma coluna equivalente a `UUID`:

```php
$table->foreignUuid('user_id');
```

<a id="column-method-foreignUuidFor"></a>
#### `foreignUuidFor()` {.collection-method}

O método `foreignUuidFor` adiciona uma coluna UUID equivalente a `{column}_id` para uma determinada classe de modelo:

```php
$table->foreignUuidFor(User::class);
```

<a id="column-method-geography"></a>
#### `geography()` {.collection-method}

O método `geography` cria uma coluna equivalente a `GEOGRAPHY` com o tipo espacial e SRID (Spatial Reference System Identifier) fornecidos:

```php
$table->geography('coordinates', subtype: 'point', srid: 4326);
```

> **Nota:**
> O suporte para tipos espaciais depende do seu driver de banco de dados. Por favor, consulte a documentação do seu banco de dados. Se sua aplicação estiver utilizando um banco de dados PostgreSQL, você deve instalar a extensão [PostGIS](https://postgis.net) antes que o método `geography` possa ser usado.

<a id="column-method-geometry"></a>
#### `geometry()` {.collection-method}

O método `geometry` cria uma coluna equivalente a `GEOMETRY` com o tipo espacial e SRID (Spatial Reference System Identifier) fornecidos:

```php
$table->geometry('positions', subtype: 'point', srid: 0);
```

> **Nota:**
> O suporte para tipos espaciais depende do seu driver de banco de dados. Por favor, consulte a documentação do seu banco de dados. Se sua aplicação estiver utilizando um banco de dados PostgreSQL, você deve instalar a extensão [PostGIS](https://postgis.net) antes que o método `geometry` possa ser usado.

<a id="column-method-id"></a>
#### `id()` {.collection-method}

O método `id` é um apelido do método `bigIncrements`. Por padrão, o método criará uma coluna `id`; no entanto, você pode passar um nome de coluna se quiser atribuir um nome diferente à coluna:

```php
$table->id();
```

<a id="column-method-increments"></a>
#### `increments()` {.collection-method}

O método `increments` cria uma coluna equivalente a `UNSIGNED INTEGER` auto-incrementável como chave primária:

```php
$table->increments('id');
```

<a id="column-method-integer"></a>
#### `integer()` {.collection-method}

O método `integer` cria uma coluna equivalente a `INTEGER`:

```php
$table->integer('votes');
```

<a id="column-method-ipAddress"></a>
#### `ipAddress()` {.collection-method}

O método `ipAddress` cria uma coluna equivalente a `VARCHAR`:

```php
$table->ipAddress('visitor');
```

Ao usar PostgreSQL, uma coluna `INET` será criada.

<a id="column-method-json"></a>
#### `json()` {.collection-method}

O método `json` cria uma coluna equivalente a `JSON`:

```php
$table->json('options');
```

Ao usar SQLite, uma coluna `TEXT` será criada.

<a id="column-method-jsonb"></a>
#### `jsonb()` {.collection-method}

O método `jsonb` cria uma coluna equivalente a `JSONB`:

```php
$table->jsonb('options');
```

Ao usar SQLite, uma coluna `TEXT` será criada.

<a id="column-method-longText"></a>
#### `longText()` {.collection-method}

O método `longText` cria uma coluna equivalente a `LONGTEXT`:

```php
$table->longText('description');
```

Ao utilizar MySQL ou MariaDB, você pode aplicar um conjunto de caracteres `binary` à coluna para criar uma coluna equivalente a `LONGBLOB`:

```php
$table->longText('data')->charset('binary'); // LONGBLOB
```

<a id="column-method-macAddress"></a>
#### `macAddress()` {.collection-method}

O método `macAddress` cria uma coluna destinada a armazenar um endereço MAC. Alguns sistemas de banco de dados, como PostgreSQL, possuem um tipo de coluna dedicado para este tipo de dados. Outros sistemas de banco de dados usarão uma coluna equivalente a string:

```php
$table->macAddress('device');
```

<a id="column-method-mediumIncrements"></a>
#### `mediumIncrements()` {.collection-method}

O método `mediumIncrements` cria uma coluna equivalente a `UNSIGNED MEDIUMINT` auto-incrementável como chave primária:

```php
$table->mediumIncrements('id');
```

<a id="column-method-mediumInteger"></a>
#### `mediumInteger()` {.collection-method}

O método `mediumInteger` cria uma coluna equivalente a `MEDIUMINT`:

```php
$table->mediumInteger('votes');
```

<a id="column-method-mediumText"></a>
#### `mediumText()` {.collection-method}

O método `mediumText` cria uma coluna equivalente a `MEDIUMTEXT`:

```php
$table->mediumText('description');
```

Ao utilizar MySQL ou MariaDB, você pode aplicar um conjunto de caracteres `binary` à coluna para criar uma coluna equivalente a `MEDIUMBLOB`:

```php
$table->mediumText('data')->charset('binary'); // MEDIUMBLOB
```

<a id="column-method-morphs"></a>
#### `morphs()` {.collection-method}

O método `morphs` é um método de conveniência que adiciona uma coluna equivalente a `VARCHAR` `{column}_type` e uma coluna equivalente a `{column}_id`. O tipo da coluna para `{column}_id` será `UNSIGNED BIGINT`, `CHAR(36)` ou `CHAR(26)` dependendo do tipo de chave do modelo.

Este método é destinado a ser usado ao definir as colunas necessárias para um [relacionamento polimórfico do Eloquent](../eloquent-relationships/). No exemplo a seguir, as colunas `taggable_type` e `taggable_id` seriam criadas:

```php
$table->morphs('taggable');
```

<a id="column-method-nullableMorphs"></a>
#### `nullableMorphs()` {.collection-method}

O método é semelhante ao método [morphs](#column-method-morphs); no entanto, as colunas criadas serão "nullable":

```php
$table->nullableMorphs('taggable');
```

<a id="column-method-nullableUlidMorphs"></a>
#### `nullableUlidMorphs()` {.collection-method}

O método é semelhante ao método [ulidMorphs](#column-method-ulidMorphs); no entanto, as colunas criadas serão "nullable":

```php
$table->nullableUlidMorphs('taggable');
```

<a id="column-method-nullableUuidMorphs"></a>
#### `nullableUuidMorphs()` {.collection-method}

O método é semelhante ao método [uuidMorphs](#column-method-uuidMorphs); no entanto, as colunas criadas serão "nullable":

```php
$table->nullableUuidMorphs('taggable');
```

<a id="column-method-rememberToken"></a>
#### `rememberToken()` {.collection-method}

O método `rememberToken` cria uma coluna nullable equivalente a `VARCHAR(100)` destinada a armazenar o [token de autenticação](../authentication/#remembering-users) "lembrar-me" atual:

```php
$table->rememberToken();
```

<a id="column-method-set"></a>
#### `set()` {.collection-method}

O método `set` cria uma coluna equivalente a `SET` com a lista de valores válidos fornecida:

```php
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a id="column-method-smallIncrements"></a>
#### `smallIncrements()` {.collection-method}

O método `smallIncrements` cria uma coluna equivalente a `UNSIGNED SMALLINT` auto-incrementável como chave primária:

```php
$table->smallIncrements('id');
```

<a id="column-method-smallInteger"></a>
#### `smallInteger()` {.collection-method}

O método `smallInteger` cria uma coluna equivalente a `SMALLINT`:

```php
$table->smallInteger('votes');
```

<a id="column-method-softDeletesTz"></a>
#### `softDeletesTz()` {.collection-method}

O método `softDeletesTz` adiciona uma coluna nullable `deleted_at` equivalente a `TIMESTAMP` (com fuso horário) com precisão opcional de frações de segundo. Esta coluna é destinada a armazenar o timestamp `deleted_at` necessário para a funcionalidade de "soft delete" do Eloquent:

```php
$table->softDeletesTz('deleted_at', precision: 0);
```

<a id="column-method-softDeletes"></a>
#### `softDeletes()` {.collection-method}

O método `softDeletes` adiciona uma coluna nullable `deleted_at` equivalente a `TIMESTAMP` com precisão opcional de frações de segundo. Esta coluna é destinada a armazenar o timestamp `deleted_at` necessário para a funcionalidade de "soft delete" do Eloquent:

```php
$table->softDeletes('deleted_at', precision: 0);
```

<a id="column-method-string"></a>
#### `string()` {.collection-method}

O método `string` cria uma coluna equivalente a `VARCHAR` do comprimento fornecido:

```php
$table->string('name', length: 100);
```

<a id="column-method-text"></a>
#### `text()` {.collection-method}

O método `text` cria uma coluna equivalente a `TEXT`:

```php
$table->text('description');
```

Ao utilizar MySQL ou MariaDB, você pode aplicar um conjunto de caracteres `binary` à coluna para criar uma coluna equivalente a `BLOB`:

```php
$table->text('data')->charset('binary'); // BLOB
```

<a id="column-method-timeTz"></a>
#### `timeTz()` {.collection-method}

O método `timeTz` cria uma coluna equivalente a `TIME` (com fuso horário) com precisão opcional de frações de segundo:

```php
$table->timeTz('sunrise', precision: 0);
```

<a id="column-method-time"></a>
#### `time()` {.collection-method}

O método `time` cria uma coluna equivalente a `TIME` com precisão opcional de frações de segundo:

```php
$table->time('sunrise', precision: 0);
```

<a id="column-method-timestampTz"></a>
#### `timestampTz()` {.collection-method}

O método `timestampTz` cria uma coluna equivalente a `TIMESTAMP` (com fuso horário) com precisão opcional de frações de segundo:

```php
$table->timestampTz('added_at', precision: 0);
```

<a id="column-method-timestamp"></a>
#### `timestamp()` {.collection-method}

O método `timestamp` cria uma coluna equivalente a `TIMESTAMP` com precisão opcional de frações de segundo:

```php
$table->timestamp('added_at', precision: 0);
```

<a id="column-method-timestampsTz"></a>
#### `timestampsTz()` {.collection-method}

O método `timestampsTz` cria colunas `created_at` e `updated_at` equivalentes a `TIMESTAMP` (com fuso horário) com precisão opcional de frações de segundo:

```php
$table->timestampsTz(precision: 0);
```

<a id="column-method-timestamps"></a>
#### `timestamps()` {.collection-method}

O método `timestamps` cria colunas `created_at` e `updated_at` equivalentes a `TIMESTAMP` com precisão opcional de frações de segundo:

```php
$table->timestamps(precision: 0);
```

<a id="column-method-tinyIncrements"></a>
#### `tinyIncrements()` {.collection-method}

O método `tinyIncrements` cria uma coluna equivalente a `UNSIGNED TINYINT` auto-incrementável como chave primária:

```php
$table->tinyIncrements('id');
```

<a id="column-method-tinyInteger"></a>
#### `tinyInteger()` {.collection-method}

O método `tinyInteger` cria uma coluna equivalente a `TINYINT`:

```php
$table->tinyInteger('votes');
```

<a id="column-method-tinyText"></a>
#### `tinyText()` {.collection-method}

O método `tinyText` cria uma coluna equivalente a `TINYTEXT`:

```php
$table->tinyText('notes');
```

Ao utilizar MySQL ou MariaDB, você pode aplicar um conjunto de caracteres `binary` à coluna para criar uma coluna equivalente a `TINYBLOB`:

```php
$table->tinyText('data')->charset('binary'); // TINYBLOB
```

<a id="column-method-unsignedBigInteger"></a>
#### `unsignedBigInteger()` {.collection-method}

O método `unsignedBigInteger` cria uma coluna equivalente a `UNSIGNED BIGINT`:

```php
$table->unsignedBigInteger('votes');
```

<a id="column-method-unsignedInteger"></a>
#### `unsignedInteger()` {.collection-method}

O método `unsignedInteger` cria uma coluna equivalente a `UNSIGNED INTEGER`:

```php
$table->unsignedInteger('votes');
```

<a id="column-method-unsignedMediumInteger"></a>
#### `unsignedMediumInteger()` {.collection-method}

O método `unsignedMediumInteger` cria uma coluna equivalente a `UNSIGNED MEDIUMINT`:

```php
$table->unsignedMediumInteger('votes');
```

<a id="column-method-unsignedSmallInteger"></a>
#### `unsignedSmallInteger()` {.collection-method}

O método `unsignedSmallInteger` cria uma coluna equivalente a `UNSIGNED SMALLINT`:

```php
$table->unsignedSmallInteger('votes');
```

<a id="column-method-unsignedTinyInteger"></a>
#### `unsignedTinyInteger()` {.collection-method}

O método `unsignedTinyInteger` cria uma coluna equivalente a `UNSIGNED TINYINT`:

```php
$table->unsignedTinyInteger('votes');
```

<a id="column-method-ulidMorphs"></a>
#### `ulidMorphs()` {.collection-method}

O método `ulidMorphs` é um método de conveniência que adiciona uma coluna equivalente a `VARCHAR` `{column}_type` e uma coluna equivalente a `CHAR(26)` `{column}_id`.

Este método é destinado a ser usado ao definir as colunas necessárias para um [relacionamento polimórfico do Eloquent](../eloquent-relationships/) que usa identificadores ULID. No exemplo a seguir, as colunas `taggable_type` e `taggable_id` seriam criadas:

```php
$table->ulidMorphs('taggable');
```

<a id="column-method-uuidMorphs"></a>
#### `uuidMorphs()` {.collection-method}

O método `uuidMorphs` é um método de conveniência que adiciona uma coluna equivalente a `VARCHAR` `{column}_type` e uma coluna equivalente a `CHAR(36)` `{column}_id`.

Este método é destinado a ser usado ao definir as colunas necessárias para um [relacionamento polimórfico do Eloquent](../eloquent-relationships/#polymorphic-relationships) que usa identificadores UUID. No exemplo a seguir, as colunas `taggable_type` e `taggable_id` seriam criadas:

```php
$table->uuidMorphs('taggable');
```

<a id="column-method-ulid"></a>
#### `ulid()` {.collection-method}

O método `ulid` cria uma coluna equivalente a `ULID`:

```php
$table->ulid('id');
```

<a id="column-method-uuid"></a>
#### `uuid()` {.collection-method}

O método `uuid` cria uma coluna equivalente a `UUID`:

```php
$table->uuid('id');
```

<a id="column-method-vector"></a>
#### `vector()` {.collection-method}

O método `vector` cria uma coluna equivalente a `vector`:

```php
$table->vector('embedding', dimensions: 1536);
```

Colunas vector são suportadas em conexões PostgreSQL usando a extensão `pgvector` e MariaDB 11.7 ou posterior. Ao utilizar PostgreSQL, o `pgvector` deve ser carregado antes que as colunas `vector` possam ser criadas:

```php
Schema::ensureVectorExtensionExists();
```

Para acelerar [consultas de similaridade vetorial](../queries/#vector-similarity-clauses), você pode adicionar um índice vetorial à coluna. Chamar o método `index` em uma coluna `vector` cria um índice vetorial usando distância de cosseno:

```php
$table->vector('embedding', dimensions: 1536)->index();
```

<a id="column-method-year"></a>
#### `year()` {.collection-method}

O método `year` cria uma coluna equivalente a `YEAR`:

```php
$table->year('birth_year');
```

<a id="column-modifiers"></a>
### Modificadores de Coluna

Além dos tipos de coluna listados acima, existem vários "modificadores" de coluna que você pode usar ao adicionar uma coluna a uma tabela de banco de dados. Por exemplo, para tornar a coluna "nullable", você pode usar o método `nullable`:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

A tabela a seguir contém todos os modificadores de coluna disponíveis. Esta lista não inclui [modificadores de índice](#creating-indexes):

<div class="overflow-auto">

| Modificador                         | Descrição                                                                                      |
| ----------------------------------- | ---------------------------------------------------------------------------------------------- |
| `->after('column')`                 | Coloca a coluna "após" outra coluna (MariaDB / MySQL).                                         |
| `->autoIncrement()`                 | Define colunas `INTEGER` como auto-incrementáveis (chave primária).                             |
| `->charset('utf8mb4')`              | Especifica um conjunto de caracteres para a coluna (MariaDB / MySQL).                          |
| `->collation('utf8mb4_unicode_ci')` | Especifica uma ordenação para a coluna.                                                        |
| `->comment('my comment')`           | Adiciona um comentário a uma coluna (MariaDB / MySQL / PostgreSQL).                            |
| `->default($value)`                 | Especifica um valor "padrão" para a coluna.                                                    |
| `->first()`                         | Coloca a coluna como "primeira" na tabela (MariaDB / MySQL).                                   |
| `->from($integer)`                  | Define o valor inicial de um campo auto-incrementável (MariaDB / MySQL / PostgreSQL).           |
| `->instant()`                       | Adiciona ou modifica a coluna usando uma operação instantânea (MySQL).                          |
| `->invisible()`                     | Torna a coluna "invisível" para consultas `SELECT *` (MariaDB / MySQL).                        |
| `->lock($mode)`                     | Especifica um modo de lock para a operação da coluna (MySQL).                                  |
| `->nullable($value = true)`         | Permite valores `NULL` serem inseridos na coluna.                                              |
| `->storedAs($expression)`           | Cria uma coluna gerada armazenada (MariaDB / MySQL / PostgreSQL / SQLite).                      |
| `->unsigned()`                      | Define colunas `INTEGER` como `UNSIGNED` (MariaDB / MySQL).                                    |
| `->using($expression)`              | Especifica uma expressão de conversão ao alterar o tipo da coluna (PostgreSQL).                 |
| `->useCurrent()`                    | Define colunas `TIMESTAMP` para usar `CURRENT_TIMESTAMP` como valor padrão.                     |
| `->useCurrentOnUpdate()`            | Define colunas `TIMESTAMP` para usar `CURRENT_TIMESTAMP` quando um registro é atualizado (MariaDB / MySQL). |
| `->virtualAs($expression)`          | Cria uma coluna gerada virtual (MariaDB / MySQL / SQLite).                                     |
| `->generatedAs($expression)`        | Cria uma coluna de identidade com opções de sequência especificadas (PostgreSQL).               |
| `->always()`                        | Define a precedência dos valores de sequência sobre a entrada para uma coluna de identidade (PostgreSQL). |

</div>

<a id="default-expressions"></a>
#### Expressões Padrão

O modificador `default` aceita um valor ou uma instância de `Illuminate\Database\Query\Expression`. Usar uma instância de `Expression` impedirá o Laravel de envolver o valor em aspas e permitirá que você use funções específicas do banco de dados. Uma situação onde isso é particularmente útil é quando você precisa atribuir valores padrão a colunas JSON:

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Query\Expression;
use Illuminate\Database\Migrations\Migration;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('flights', function (Blueprint $table) {
            $table->id();
            $table->json('movies')->default(new Expression('(JSON_ARRAY())'));
            $table->timestamps();
        });
    }
};
```

> **Aviso:**
> O suporte para expressões padrão depende do seu driver de banco de dados, versão do banco de dados e tipo do campo. Por favor, consulte a documentação do seu banco de dados.

<a id="column-order"></a>
#### Ordem das Colunas

Ao usar o banco de dados MariaDB ou MySQL, o método `after` pode ser usado para adicionar colunas após uma coluna existente no esquema:

```php
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a id="instant-column-operations"></a>
#### Operações de Coluna Instantâneas

Ao usar MySQL, você pode encadear o modificador `instant` em uma definição de coluna para indicar que a coluna deve ser adicionada ou modificada usando o algoritmo "instant" do MySQL. Este algoritmo permite que certas alterações de esquema sejam realizadas sem uma reconstrução completa da tabela, tornando-as quase instantâneas independentemente do tamanho da tabela:

```php
$table->string('name')->nullable()->instant();
```

Adições de colunas instantâneas só podem anexar colunas ao final da tabela, portanto o modificador `instant` não pode ser combinado com os modificadores `after` ou `first`. Além disso, o algoritmo não suporta todos os tipos de coluna ou operações. Se a operação solicitada for incompatível, o MySQL levantará um erro.

Por favor, consulte a [documentação do MySQL](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html) para determinar quais operações são compatíveis com modificações de coluna instantâneas.

<a id="ddl-locking"></a>
#### Locking DDL

Ao usar MySQL, você pode encadear o modificador `lock` em definições de coluna, índice ou chave estrangeira para controlar o locking de tabela durante operações de esquema. O MySQL suporta vários modos de lock: `none` permite leituras e escritas concorrentes, `shared` permite leituras concorrentes, mas bloqueia escritas, `exclusive` bloqueia todo acesso concorrente e `default` deixa o MySQL escolher o modo mais apropriado:

```php
$table->string('name')->lock('none');

$table->index('email')->lock('shared');
```

Se o modo de lock solicitado for incompatível com a operação, o MySQL levantará um erro. O modificador `lock` pode ser combinado com o modificador `instant` para otimizar ainda mais as alterações de esquema:

```php
$table->string('name')->instant()->lock('none');
```

<a id="modifying-columns"></a>
### Modificando Colunas

O método `change` permite que você modifique o tipo e os atributos de colunas existentes. Por exemplo, você pode desejar aumentar o tamanho de uma coluna `string`. Para ver o método `change` em ação, vamos aumentar o tamanho da coluna `name` de 25 para 50. Para isso, simplesmente definimos o novo estado da coluna e depois chamamos o método `change`:

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

Ao modificar uma coluna, você deve incluir explicitamente todos os modificadores que deseja manter na definição da coluna - qualquer atributo ausente será removido. Por exemplo, para reter os atributos `unsigned`, `default` e `comment`, você deve chamar cada modificador explicitamente ao alterar a coluna:

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

O método `change` não altera os índices da coluna. Portanto, você pode usar modificadores de índice para adicionar ou remover explicitamente um índice ao modificar a coluna:

```php
// Add an index...
$table->bigIncrements('id')->primary()->change();

// Drop an index...
$table->char('postal_code', 10)->unique(false)->change();
```

<a id="postgresql-column-modifications"></a>
#### Modificações de Coluna no PostgreSQL

Ao alterar o tipo de uma coluna no PostgreSQL, você pode usar o modificador `using` para especificar a expressão usada para converter os valores existentes:

```php
Schema::table('users', function (Blueprint $table) {
    $table->date('birthday')->using('birthday::date')->change();
});
```

<a id="renaming-columns"></a>
### Renomeando Colunas

Para renomear uma coluna, você pode usar o método `renameColumn` fornecido pelo construtor de esquema:

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a id="dropping-columns"></a>
### Removendo Colunas

Para remover uma coluna, você pode usar o método `dropColumn` no construtor de esquema:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

Você pode remover múltiplas colunas de uma tabela passando um array de nomes de colunas ao método `dropColumn`:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a id="available-command-aliases"></a>
#### Aliases de Comandos Disponíveis

O Laravel fornece vários métodos convenientes relacionados à remoção de tipos comuns de colunas. Cada um desses métodos é descrito na tabela abaixo:

<div class="overflow-auto">

| Comando                             | Descrição                                                    |
| ----------------------------------- | ------------------------------------------------------------ |
| `$table->dropMorphs('morphable');`  | Remove as colunas `morphable_type` e `morphable_id`.         |
| `$table->dropRememberToken();`      | Remove a coluna `remember_token`.                            |
| `$table->dropSoftDeletes();`        | Remove a coluna `deleted_at`.                                |
| `$table->dropSoftDeletesTz();`      | Alias do método `dropSoftDeletes()`.                         |
| `$table->dropTimestamps();`         | Remove as colunas `created_at` e `updated_at`.               |
| `$table->dropTimestampsTz();`       | Alias do método `dropTimestamps()`.                          |

</div>

<a id="indexes"></a>
## Índices

<a id="creating-indexes"></a>
### Criando Índices

O construtor de esquema do Laravel suporta vários tipos de índices. O exemplo a seguir cria uma nova coluna `email` e especifica que seus valores devem ser únicos. Para criar o índice, podemos encadear o método `unique` na definição da coluna:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

Alternativamente, você pode criar o índice após definir a coluna. Para fazer isso, você deve chamar o método `unique` no blueprint do construtor de esquema. Este método aceita o nome da coluna que deve receber um índice único:

```php
$table->unique('email');
```

Você pode até passar um array de colunas a um método de índice para criar um índice composto (ou composto):

```php
$table->index(['account_id', 'created_at']);
```

Ao criar um índice, o Laravel gerará automaticamente um nome de índice baseado na tabela, nomes das colunas e tipo do índice, mas você pode passar um segundo argumento ao método para especificar o nome do índice você mesmo:

```php
$table->unique('email', 'unique_email');
```

<a id="available-index-types"></a>
#### Tipos de Índice Disponíveis

A classe blueprint do construtor de esquema do Laravel fornece métodos para criar cada tipo de índice suportado pelo Laravel. Cada método de índice aceita um segundo argumento opcional para especificar o nome do índice. Se omitido, o nome será derivado dos nomes da tabela e coluna(s) usadas para o índice, bem como do tipo do índice. Cada um dos métodos de índice disponíveis é descrito na tabela abaixo:

<div class="overflow-auto">

| Comando                                          | Descrição                                                      |
| ------------------------------------------------ | -------------------------------------------------------------- |
| `$table->primary('id');`                         | Adiciona uma chave primária.                                   |
| `$table->primary(['id', 'parent_id']);`          | Adiciona chaves compostas.                                     |
| `$table->unique('email');`                       | Adiciona um índice único.                                      |
| `$table->index('state');`                        | Adiciona um índice.                                            |
| `$table->fullText('body');`                      | Adiciona um índice de texto completo (MariaDB / MySQL / PostgreSQL). |
| `$table->fullText('body')->language('english');` | Adiciona um índice de texto completo do idioma especificado (PostgreSQL). |
| `$table->spatialIndex('location');`              | Adiciona um índice espacial (exceto SQLite).                   |
| `$table->vectorIndex('embedding');`              | Adiciona um índice vetorial (MariaDB / PostgreSQL).            |

</div>

<a id="online-index-creation"></a>
#### Criação de Índice Online

Por padrão, criar um índice em uma tabela grande pode bloquear a tabela e impedir leituras ou escritas enquanto o índice está sendo construído. Ao usar PostgreSQL ou SQL Server, você pode encadear o método `online` em uma definição de índice para criar o índice sem bloquear a tabela, permitindo que sua aplicação continue lendo e gravando dados durante a criação do índice:

```php
$table->unique('email')->online();
```

Ao usar PostgreSQL, isso adiciona a opção `CONCURRENTLY` à instrução de criação de índice. Ao usar SQL Server, isso adiciona a opção `WITH (online = on)`.

Ao usar MySQL, você pode encadear o modificador `inplace` em uma definição de índice ou chave estrangeira para especificar que a operação deve usar o algoritmo `INPLACE`:

```php
$table->index('email')->inplace();

$table->foreign('user_id')->references('id')->on('users')->inplace();
```

O modificador `inplace` pode ser combinado com o modificador `lock` para controlar o locking de tabela durante a operação:

```php
$table->index('email')->inplace()->lock('none');
```

Ao usar o modificador `inplace` para uma operação de chave estrangeira, as verificações de chave estrangeira devem ser desabilitadas.

Consulte a [documentação do MySQL](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html) para determinar quais operações suportam o algoritmo `INPLACE` e os modos de lock.

<a id="renaming-indexes"></a>
### Renomeando Índices

Para renomear um índice, você pode usar o método `renameIndex` fornecido pelo blueprint do construtor de esquema. Este método aceita o nome atual do índice como primeiro argumento e o nome desejado como segundo argumento:

```php
$table->renameIndex('from', 'to');
```

<a id="dropping-indexes"></a>
### Removendo Índices

Para remover um índice, você deve especificar o nome do índice. Por padrão, o Laravel atribui automaticamente um nome de índice baseado no nome da tabela, no nome da coluna indexada e no tipo do índice. Aqui estão alguns exemplos:

<div class="overflow-auto">

| Comando                                                       | Descrição                                                  |
| ------------------------------------------------------------- | ---------------------------------------------------------- |
| `$table->dropPrimary('users_id_primary');`                    | Remove uma chave primária da tabela "users".               |
| `$table->dropUnique('users_email_unique');`                   | Remove um índice único da tabela "users".                  |
| `$table->dropIndex('geo_state_index');`                       | Remove um índice básico da tabela "geo".                   |
| `$table->dropFullText('posts_body_fulltext');`                | Remove um índice de texto completo da tabela "posts".      |
| `$table->dropSpatialIndex('geo_location_spatialindex');`      | Remove um índice espacial da tabela "geo" (exceto SQLite). |
| `$table->dropVectorIndex('documents_embedding_vectorindex');` | Remove um índice vetorial da tabela "documents".           |

</div>

Se você passar um array de colunas a um método que remove índices, o nome convencional do índice será gerado com base no nome da tabela, colunas e tipo do índice:

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // Drops index 'geo_state_index'
});
```

<a id="foreign-key-constraints"></a>
### Restrições de Chave Estrangeira

O Laravel também fornece suporte para criar restrições de chave estrangeira, que são usadas para forçar a integridade referencial no nível do banco de dados. Por exemplo, vamos definir uma coluna `user_id` na tabela `posts` que referencia a coluna `id` em uma tabela `users`:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

Como essa sintaxe é bastante verbosa, o Laravel fornece métodos adicionais, mais concisos, que usam convenções para proporcionar uma melhor experiência ao desenvolvedor. Ao usar o método `foreignId` para criar sua coluna, o exemplo acima pode ser reescrito assim:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

O método `foreignId` cria uma coluna equivalente a `UNSIGNED BIGINT`, enquanto o método `constrained` usará convenções para determinar a tabela e a coluna sendo referenciada. Se o nome da sua tabela não corresponder às convenções do Laravel, você pode fornecê-lo manualmente ao método `constrained`. Além disso, o nome que deve ser atribuído ao índice gerado pode ser especificado também:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

Você também pode especificar a ação desejada para as propriedades "on delete" e "on update" da restrição:

```php
$table->foreignId('user_id')
    ->constrained()
    ->onUpdate('cascade')
    ->onDelete('cascade');
```

Uma sintaxe expressiva alternativa também é fornecida para essas ações:

<div class="overflow-auto">

| Método                          | Descrição                                                       |
| ------------------------------- | --------------------------------------------------------------- |
| `$table->cascadeOnUpdate();`    | Atualizações devem ser em cascata.                               |
| `$table->restrictOnUpdate();`   | Atualizações devem ser restritas.                                |
| `$table->nullOnUpdate();`       | Atualizações devem definir o valor da chave estrangeira como nulo. |
| `$table->noActionOnUpdate();`   | Nenhuma ação em atualizações.                                   |
| `$table->cascadeOnDelete();`    | Exclusões devem ser em cascata.                                  |
| `$table->restrictOnDelete();`   | Exclusões devem ser restritas.                                   |
| `$table->nullOnDelete();`       | Exclusões devem definir o valor da chave estrangeira como nulo.  |
| `$table->noActionOnDelete();`   | Impede exclusões se existirem registros filhos.                  |

</div>

Quaisquer [modificadores de coluna](#column-modifiers) adicionais devem ser chamados antes do método `constrained`:

```php
$table->foreignId('user_id')
    ->nullable()
    ->constrained();
```

<a id="dropping-foreign-keys"></a>
#### Removendo Chaves Estrangeiras

Para remover uma chave estrangeira, você pode usar o método `dropForeign`, passando o nome da restrição de chave estrangeira a ser excluída como argumento. As restrições de chave estrangeira usam a mesma convenção de nomenclatura que os índices. Em outras palavras, o nome da restrição de chave estrangeira é baseado no nome da tabela e nas colunas na restrição, seguido de um sufixo "\_foreign":

```php
$table->dropForeign('posts_user_id_foreign');
```

Alternativamente, você pode passar um array contendo o nome da coluna que contém a chave estrangeira ao método `dropForeign`. O array será convertido em um nome de restrição de chave estrangeira usando as convenções de nomenclatura de restrição do Laravel:

```php
$table->dropForeign(['user_id']);
```

<a id="toggling-foreign-key-constraints"></a>
#### Alternando Restrições de Chave Estrangeira

Você pode habilitar ou desabilitar restrições de chave estrangeira dentro das suas migrations usando os seguintes métodos:

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // Constraints disabled within this closure...
});
```

> **Aviso:**
> O SQLite desabilita restrições de chave estrangeira por padrão. Ao usar SQLite, certifique-se de [habilitar o suporte a chaves estrangeiras](../database/#configuration) na configuração do seu banco de dados antes de tentar criá-las nas suas migrations.

<a id="events"></a>
## Eventos

Para conveniência, cada operação de migration despachará um [evento](../events/). Com exceção de `SchemaDumped` e `SchemaLoaded`, todos os seguintes eventos implementam a interface `Illuminate\Contracts\Database\Events\MigrationEvent`:

<div class="overflow-auto">

| Classe                                             | Descrição                                                      |
| -------------------------------------------------- | -------------------------------------------------------------- |
| `Illuminate\Database\Events\DatabaseRefreshed`     | O comando `migrate:fresh` ou `migrate:refresh` foi concluído.   |
| `Illuminate\Database\Events\MigrationsStarted`     | Um lote de migrations está prestes a ser executado.            |
| `Illuminate\Database\Events\MigrationsEnded`       | Um lote de migrations foi concluído.                           |
| `Illuminate\Database\Events\MigrationStarted`      | Uma única migration está prestes a ser executada.              |
| `Illuminate\Database\Events\MigrationEnded`        | Uma única migration foi concluída.                             |
| `Illuminate\Database\Events\NoPendingMigrations`   | Um comando de migration não encontrou migrations pendentes.    |
| `Illuminate\Database\Events\SchemaDumped`          | Um dump do esquema do banco de dados foi concluído.            |
| `Illuminate\Database\Events\SchemaLoaded`          | Um dump existente do esquema do banco de dados foi carregado.  |

</div>