---
title: "Eloquent: Primeiros Passos"
---

- [Introdução](#introduction)
- [Gerando Classes de Model](#generating-model-classes)
- [Convenções de Models Eloquent](#eloquent-model-conventions)
    - [Nomes de Tabelas](#table-names)
    - [Chaves Primárias](#primary-keys)
    - [Chaves UUID e ULID](#uuid-and-ulid-keys)
    - [Timestamps](#timestamps)
    - [Conexões com o Banco de Dados](#database-connections)
    - [Valores Padrão de Atributos](#default-attribute-values)
    - [Atualizando Atributos Após Escritas](#refreshing-attributes-after-writes)
    - [Configurando o Rigor do Eloquent](#configuring-eloquent-strictness)
- [Recuperando Models](#retrieving-models)
    - [Coleções](#collections)
    - [Dividindo Resultados em Blocos](#chunking-results)
    - [Dividindo em Blocos Usando Coleções Lazy](#chunking-using-lazy-collections)
    - [Cursores](#cursors)
    - [Subconsultas Avançadas](#advanced-subqueries)
- [Recuperando Models Únicos / Agregados](#retrieving-single-models)
    - [Recuperando ou Criando Models](#retrieving-or-creating-models)
    - [Recuperando Agregados](#retrieving-aggregates)
- [Inserindo e Atualizando Models](#inserting-and-updating-models)
    - [Inserções](#inserts)
    - [Atualizações](#updates)
    - [Atribuição em Massa](#mass-assignment)
    - [Upserts](#upserts)
- [Deletando Models](#deleting-models)
    - [Soft Delete](#soft-deleting)
    - [Consultando Models Com Soft Delete](#querying-soft-deleted-models)
- [Podando Models](#pruning-models)
- [Replicando Models](#replicating-models)
- [Escopos de Consulta](#query-scopes)
    - [Escopos Globais](#global-scopes)
    - [Escopos Locais](#local-scopes)
    - [Atributos Pendentes](#pending-attributes)
- [Comparando Models](#comparing-models)
- [Eventos](#events)
    - [Usando Closures](#events-using-closures)
    - [Observers](#observers)
    - [Silenciando Eventos](#muting-events)

<a id="introduction"></a>
## Introdução

O Laravel inclui o Eloquent, um mapeador objeto-relacional (ORM) que torna agradável interagir com o seu banco de dados. Ao usar o Eloquent, cada tabela do banco de dados possui um "Model" correspondente que é usado para interagir com essa tabela. Além de recuperar registros da tabela, os models Eloquent também permitem inserir, atualizar e deletar registros da tabela.

> **Nota:**
> Antes de começar, certifique-se de configurar uma conexão com o banco de dados no arquivo de configuração `config/database.php` da sua aplicação. Para mais informações sobre como configurar seu banco de dados, consulte [a documentação de configuração do banco de dados](../database/#configuration).

<a id="generating-model-classes"></a>
## Gerando Classes de Model

Para começar, vamos criar um model Eloquent. Os models normalmente ficam no diretório `app\Models` e estendem a classe `Illuminate\Database\Eloquent\Model`. Você pode usar o [comando Artisan](../artisan/) `make:model` para gerar um novo model:

```shell
php artisan make:model Flight
```

Se você quiser gerar uma [migração de banco de dados](../migrations/) ao gerar o model, pode usar a opção `--migration` ou `-m`:

```shell
php artisan make:model Flight --migration
```

Você pode gerar vários outros tipos de classes ao gerar um model, como factories, seeders, policies, controllers e form requests. Além disso, essas opções podem ser combinadas para criar várias classes de uma só vez:

```shell
# Generate a model and a FlightFactory class...
php artisan make:model Flight --factory
php artisan make:model Flight -f

# Generate a model and a FlightSeeder class...
php artisan make:model Flight --seed
php artisan make:model Flight -s

# Generate a model and a FlightController class...
php artisan make:model Flight --controller
php artisan make:model Flight -c

# Generate a model, FlightController resource class, and form request classes...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# Generate a model and a FlightPolicy class...
php artisan make:model Flight --policy

# Generate a model and a migration, factory, seeder, and controller...
php artisan make:model Flight -mfsc

# Shortcut to generate a model, migration, factory, seeder, policy, controller, and form requests...
php artisan make:model Flight --all
php artisan make:model Flight -a

# Generate a pivot model...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a id="inspecting-models"></a>
#### Inspecionando Models

Às vezes pode ser difícil identificar todos os atributos e relacionamentos disponíveis de um model apenas lendo o seu código. Em vez disso, experimente o comando Artisan `model:show`, que fornece uma visão geral conveniente de todos os atributos e relações do model:

```shell
php artisan model:show Flight
```

<a id="eloquent-model-conventions"></a>
## Convenções de Models Eloquent

Os models gerados pelo comando `make:model` serão colocados no diretório `app/Models`. Vamos examinar uma classe de model básica e discutir algumas das principais convenções do Eloquent:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    // ...
}
```

<a id="table-names"></a>
### Nomes de Tabelas

Depois de olhar o exemplo acima, você deve ter notado que não informamos ao Eloquent qual tabela do banco de dados corresponde ao nosso model `Flight`. Por convenção, o nome da classe no formato "snake case" e no plural será usado como nome da tabela, a menos que outro nome seja explicitamente especificado. Assim, neste caso, o Eloquent assumirá que o model `Flight` armazena registros na tabela `flights`, enquanto um model `AirTrafficController` armazenaria registros em uma tabela `air_traffic_controllers`.

Se a tabela do banco de dados correspondente ao seu model não seguir essa convenção, você pode especificar manualmente o nome da tabela do model usando o atributo `Table`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table('my_flights')]
class Flight extends Model
{
    // ...
}
```


<a id="primary-keys"></a>
### Chaves Primárias

O Eloquent também assume que a tabela do banco de dados correspondente a cada model possui uma coluna de chave primária chamada `id`. Se necessário, você pode especificar outra coluna que sirva como chave primária do seu model usando o argumento `key` no atributo `Table`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(key: 'flight_id')]
class Flight extends Model
{
    // ...
}
```

Além disso, o Eloquent assume que a chave primária é um valor inteiro incremental, o que significa que o Eloquent converterá automaticamente a chave primária para inteiro. Se você quiser usar uma chave primária não incremental ou não numérica, deve especificar os argumentos `keyType` e `incrementing` no atributo `Table`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(key: 'uuid', keyType: 'string', incrementing: false)]
class Flight extends Model
{
    // ...
}
```

Se você só precisar desabilitar IDs com auto incremento, pode usar o atributo `WithoutIncrementing`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\WithoutIncrementing;
use Illuminate\Database\Eloquent\Model;

#[WithoutIncrementing]
class Flight extends Model
{
    // ...
}
```

<a id="composite-primary-keys"></a>
#### Chaves Primárias "Compostas"

O Eloquent exige que cada model tenha pelo menos um "ID" de identificação única que possa servir como sua chave primária. Chaves primárias "compostas" não são suportadas pelos models Eloquent. No entanto, você é livre para adicionar índices únicos adicionais de múltiplas colunas às suas tabelas do banco de dados, além da chave primária de identificação única da tabela.

<a id="uuid-and-ulid-keys"></a>
### Chaves UUID e ULID

Em vez de usar inteiros com auto incremento como chaves primárias dos seus models Eloquent, você pode optar por usar UUIDs. UUIDs são identificadores alfanuméricos universalmente únicos com 36 caracteres.

Se você quiser que um model use uma chave UUID em vez de uma chave inteira com auto incremento, pode usar a trait `Illuminate\Database\Eloquent\Concerns\HasUuids` no model. É claro que você deve garantir que o model tenha uma [coluna de chave primária equivalente a UUID](../migrations/#column-method-uuid):

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUuids;

    // ...
}

$article = Article::create(['title' => 'Traveling to Europe']);

$article->id; // "018f2b5c-6a7f-7b12-9d6f-2f8a4e0c9c11"
```

Por padrão, a trait `HasUuids` gerará identificadores [UUIDv7](../strings/#method-str-uuid7) para os seus models. Esses UUIDs são mais eficientes para armazenamento indexado no banco de dados, pois podem ser ordenados lexicograficamente.

Você pode sobrescrever o processo de geração de UUID para um determinado model definindo um método `newUniqueId` no model. Além disso, você pode especificar quais colunas devem receber UUIDs definindo um método `uniqueIds` no model:

```php
use Ramsey\Uuid\Uuid;

/**
 * Generate a new UUID for the model.
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * Get the columns that should receive a unique identifier.
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

Se preferir, você pode optar por usar "ULIDs" em vez de UUIDs. ULIDs são semelhantes aos UUIDs; no entanto, têm apenas 26 caracteres. Assim como os UUIDs ordenados, os ULIDs são ordenáveis lexicograficamente para uma indexação eficiente no banco de dados. Para usar ULIDs, você deve usar a trait `Illuminate\Database\Eloquent\Concerns\HasUlids` no seu model. Você também deve garantir que o model tenha uma [coluna de chave primária equivalente a ULID](../migrations/#column-method-ulid):

```php
use Illuminate\Database\Eloquent\Concerns\HasUlids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUlids;

    // ...
}

$article = Article::create(['title' => 'Traveling to Asia']);

$article->id; // "01gd4d3tgrrfqeda94gdbtdk5c"
```

<a id="timestamps"></a>
### Timestamps

Por padrão, o Eloquent espera que as colunas `created_at` e `updated_at` existam na tabela do banco de dados correspondente ao seu model. O Eloquent definirá automaticamente os valores dessas colunas quando os models forem criados ou atualizados. Se você não quiser que essas colunas sejam gerenciadas automaticamente pelo Eloquent, pode definir `timestamps` como `false` no atributo `Table` do seu model:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(timestamps: false)]
class Flight extends Model
{
    // ...
}
```

Se você só precisar desabilitar os timestamps, pode usar o atributo `WithoutTimestamps`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\WithoutTimestamps;
use Illuminate\Database\Eloquent\Model;

#[WithoutTimestamps]
class Flight extends Model
{
    // ...
}
```

Se precisar personalizar o formato dos timestamps do seu model, pode usar o argumento `dateFormat` no atributo `Table`. Isso determina como os atributos de data são armazenados no banco de dados:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(dateFormat: 'U')]
class Flight extends Model
{
    // ...
}
```

Se você só precisar definir um formato de data, pode usar o atributo `DateFormat`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\DateFormat;
use Illuminate\Database\Eloquent\Model;

#[DateFormat('U')]
class Flight extends Model
{
    // ...
}
```

Se precisar personalizar os nomes das colunas usadas para armazenar os timestamps, pode definir as constantes `CREATED_AT` e `UPDATED_AT` no seu model:

```php
<?php

class Flight extends Model
{
    /**
     * The name of the "created at" column.
     *
     * @var string|null
     */
    public const CREATED_AT = 'creation_date';

    /**
     * The name of the "updated at" column.
     *
     * @var string|null
     */
    public const UPDATED_AT = 'updated_date';
}
```

Se você quiser realizar operações em um model sem que o timestamp `updated_at` dele seja modificado, pode operar sobre o model dentro de um closure passado ao método `withoutTimestamps`:

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a id="database-connections"></a>
### Conexões com o Banco de Dados

Por padrão, todos os models Eloquent usarão a conexão de banco de dados padrão configurada para a sua aplicação. Se você quiser especificar uma conexão diferente que deve ser usada ao interagir com um determinado model, pode usar o atributo `Connection`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Connection;
use Illuminate\Database\Eloquent\Model;

#[Connection('mysql')]
class Flight extends Model
{
    // ...
}
```

<a id="default-attribute-values"></a>
### Valores Padrão de Atributos

Por padrão, uma instância de model recém-instanciada não conterá nenhum valor de atributo. Se você quiser definir os valores padrão de alguns atributos do seu model, pode definir uma propriedade `$attributes` no seu model. Os valores de atributos colocados no array `$attributes` devem estar no seu formato bruto, "armazenável", como se tivessem acabado de ser lidos do banco de dados:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * The model's default values for attributes.
     *
     * @var array<string, mixed>
     */
    protected $attributes = [
        'options' => '[]',
        'delayed' => false,
    ];
}
```

<a id="refreshing-attributes-after-writes"></a>
### Atualizando Atributos Após Escritas

Se o seu banco de dados contiver colunas geradas, você pode configurar o Eloquent para atualizar atributos específicos depois que um model for inserido ou atualizado. Para isso, defina o atributo `Refreshes` no seu model:

```php
use Illuminate\Database\Eloquent\Attributes\Refreshes;

#[Refreshes('name')]
class User extends Model
{
    // ...
}
```

Você pode especificar vários atributos como um array:

```php
#[Refreshes(['name', 'slug'])]
```

Depois que o model for gravado, os atributos configurados serão atualizados a partir do banco de dados.

<a id="configuring-eloquent-strictness"></a>
### Configurando o Rigor do Eloquent

O Laravel oferece vários métodos que permitem configurar o comportamento e o "rigor" do Eloquent em diversas situações.

Primeiro, o método `preventLazyLoading` aceita um argumento booleano opcional que indica se o lazy loading deve ser impedido. Por exemplo, você pode desejar desabilitar o lazy loading apenas em ambientes que não sejam de produção, para que seu ambiente de produção continue funcionando normalmente mesmo que um relacionamento carregado de forma lazy esteja presente acidentalmente no código de produção. Normalmente, este método deve ser invocado no método `boot` do `AppServiceProvider` da sua aplicação:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

Além disso, você pode instruir o Laravel a lançar uma exceção ao tentar preencher um atributo não preenchível invocando o método `preventSilentlyDiscardingAttributes`. Isso pode ajudar a evitar erros inesperados durante o desenvolvimento local ao tentar definir um atributo que não foi adicionado ao array `fillable` do model:

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a id="retrieving-models"></a>
## Recuperando Models

Depois de criar um model e [sua tabela de banco de dados associada](../migrations/#generating-migrations), você está pronto para começar a recuperar dados do seu banco de dados. Você pode pensar em cada model Eloquent como um [query builder](../queries/) poderoso que permite consultar de forma fluente a tabela do banco de dados associada ao model. O método `all` do model recuperará todos os registros da tabela de banco de dados associada ao model:

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a id="building-queries"></a>
#### Construindo Consultas

O método `all` do Eloquent retornará todos os resultados da tabela do model. No entanto, como cada model Eloquent serve como um [query builder](../queries/), você pode adicionar restrições adicionais às consultas e, em seguida, invocar o método `get` para recuperar os resultados:

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> **Nota:**
> Como os models Eloquent são query builders, você deve revisar todos os métodos fornecidos pelo [query builder](../queries/) do Laravel. Você pode usar qualquer um desses métodos ao escrever suas consultas Eloquent.

<a id="refreshing-models"></a>
#### Atualizando Models

Se você já possui uma instância de um model Eloquent que foi recuperada do banco de dados, pode "atualizar" o model usando os métodos `fresh` e `refresh`. O método `fresh` recuperará novamente o model do banco de dados. A instância de model existente não será afetada:

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

O método `refresh` reidratará o model existente usando dados novos do banco de dados. Além disso, todos os seus relacionamentos carregados também serão atualizados:

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

Se você precisar atualizar um model e adquirir um lock pessimista dentro de uma transação, pode usar o método `refreshForUpdate`. Este método recarrega o model usando um lock `FOR UPDATE`:

```php
DB::transaction(function () use ($flight) {
    $flight->refreshForUpdate();

    // Update the locked model...
});
```

<a id="collections"></a>
### Coleções

Como vimos, métodos do Eloquent como `all` e `get` recuperam vários registros do banco de dados. No entanto, esses métodos não retornam um array PHP simples. Em vez disso, é retornada uma instância de `Illuminate\Database\Eloquent\Collection`.

A classe `Collection` do Eloquent estende a classe base `Illuminate\Support\Collection` do Laravel, que fornece [uma variedade de métodos úteis](../collections/#available-methods) para interagir com coleções de dados. Por exemplo, o método `reject` pode ser usado para remover models de uma coleção com base nos resultados de um closure invocado:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

Além dos métodos fornecidos pela classe base de coleções do Laravel, a classe de coleção do Eloquent oferece [alguns métodos extras](../eloquent-collections/#available-methods) destinados especificamente à interação com coleções de models Eloquent.

Como todas as coleções do Laravel implementam as interfaces iteráveis do PHP, você pode percorrer coleções como se fossem arrays:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a id="chunking-results"></a>
### Dividindo Resultados em Blocos

Sua aplicação pode ficar sem memória se você tentar carregar dezenas de milhares de registros do Eloquent por meio dos métodos `all` ou `get`. Em vez de usar esses métodos, o método `chunk` pode ser usado para processar grandes quantidades de models de forma mais eficiente.

O método `chunk` recuperará um subconjunto de models Eloquent, passando-os para um closure para processamento. Como apenas o bloco atual de models Eloquent é recuperado por vez, o método `chunk` proporcionará um uso de memória significativamente menor ao trabalhar com um grande número de models:

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

O primeiro argumento passado ao método `chunk` é o número de registros que você deseja receber por "bloco". O closure passado como segundo argumento será invocado para cada bloco recuperado do banco de dados. Uma consulta ao banco de dados será executada para recuperar cada bloco de registros passado ao closure.

Se você estiver filtrando os resultados do método `chunk` com base em uma coluna que também será atualizada enquanto itera sobre os resultados, deve usar o método `chunkById`. Usar o método `chunk` nesses cenários pode levar a resultados inesperados e inconsistentes. Internamente, o método `chunkById` sempre recuperará models com uma coluna `id` maior que o último model do bloco anterior:

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

Como os métodos `chunkById` e `lazyById` adicionam suas próprias condições "where" à consulta executada, você deve normalmente [agrupar logicamente](../queries/#logical-grouping) suas próprias condições dentro de um closure:

```php
Flight::where(function ($query) {
    $query->where('delayed', true)->orWhere('cancelled', true);
})->chunkById(200, function (Collection $flights) {
    $flights->each->update([
        'departed' => false,
        'cancelled' => true
    ]);
}, column: 'id');
```

<a id="chunking-using-lazy-collections"></a>
### Dividindo em Blocos Usando Coleções Lazy

O método `lazy` funciona de forma semelhante ao [método `chunk`](#chunking-results) no sentido de que, por baixo dos panos, ele executa a consulta em blocos. No entanto, em vez de passar cada bloco diretamente para um callback, o método `lazy` retorna uma [LazyCollection](../collections/#lazy-collections) "achatada" de models Eloquent, que permite interagir com os resultados como um único fluxo:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

Se você estiver filtrando os resultados do método `lazy` com base em uma coluna que também será atualizada enquanto itera sobre os resultados, deve usar o método `lazyById`. Internamente, o método `lazyById` sempre recuperará models com uma coluna `id` maior que o último model do bloco anterior:

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

Você pode filtrar os resultados em ordem decrescente de `id` usando o método `lazyByIdDesc`.

<a id="cursors"></a>
### Cursores

Assim como o método `lazy`, o método `cursor` pode ser usado para reduzir significativamente o consumo de memória da sua aplicação ao iterar sobre dezenas de milhares de registros de models Eloquent.

O método `cursor` executará apenas uma única consulta ao banco de dados; no entanto, os models Eloquent individuais não serão hidratados até que sejam efetivamente iterados. Portanto, apenas um model Eloquent é mantido na memória por vez durante a iteração sobre o cursor.

> **Aviso:**
> Como o método `cursor` mantém apenas um model Eloquent na memória por vez, ele não pode carregar relacionamentos de forma antecipada (eager loading). Se você precisar carregar relacionamentos de forma antecipada, considere usar [o método `lazy`](#chunking-using-lazy-collections).

Internamente, o método `cursor` usa [generators](https://www.php.net/manual/en/language.generators.overview.php) do PHP para implementar essa funcionalidade:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

O `cursor` retorna uma instância de `Illuminate\Support\LazyCollection`. [Coleções lazy](../collections/#lazy-collections) permitem usar muitos dos métodos de coleção disponíveis nas coleções típicas do Laravel, enquanto carregam apenas um model na memória por vez:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

Embora o método `cursor` use muito menos memória do que uma consulta regular (mantendo apenas um model Eloquent na memória por vez), ele ainda pode ficar sem memória com o tempo. Isso ocorre [porque o driver PDO do PHP armazena internamente em cache todos os resultados brutos da consulta em seu buffer](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php). Se você estiver lidando com um número muito grande de registros do Eloquent, considere usar [o método `lazy`](#chunking-using-lazy-collections).

<a id="advanced-subqueries"></a>
### Subconsultas Avançadas

<a id="subquery-selects"></a>
#### Subconsultas em Select

O Eloquent também oferece suporte avançado a subconsultas, o que permite extrair informações de tabelas relacionadas em uma única consulta. Por exemplo, imagine que temos uma tabela de `destinations` (destinos de voo) e uma tabela de `flights` (voos) para esses destinos. A tabela `flights` contém uma coluna `arrived_at` que indica quando o voo chegou ao destino.

Usando a funcionalidade de subconsulta disponível nos métodos `select` e `addSelect` do query builder, podemos selecionar todos os `destinations` e o nome do voo que chegou mais recentemente a cada destino, usando uma única consulta:

```php
use App\Models\Destination;
use App\Models\Flight;

return Destination::addSelect(['last_flight' => Flight::select('name')
    ->whereColumn('destination_id', 'destinations.id')
    ->orderByDesc('arrived_at')
    ->limit(1)
])->get();
```

<a id="subquery-ordering"></a>
#### Ordenação por Subconsulta

Além disso, a função `orderBy` do query builder oferece suporte a subconsultas. Continuando com nosso exemplo de voos, podemos usar essa funcionalidade para ordenar todos os destinos com base em quando o último voo chegou a cada destino. Novamente, isso pode ser feito durante a execução de uma única consulta ao banco de dados:

```php
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a id="retrieving-single-models"></a>
## Recuperando Models Únicos / Agregados

Além de recuperar todos os registros que correspondem a uma determinada consulta, você também pode recuperar registros únicos usando os métodos `find`, `first` ou `firstWhere`. Em vez de retornar uma coleção de models, esses métodos retornam uma única instância de model:

```php
use App\Models\Flight;

// Retrieve a model by its primary key...
$flight = Flight::find(1);

// Retrieve the first model matching the query constraints...
$flight = Flight::where('active', 1)->first();

// Alternative to retrieving the first model matching the query constraints...
$flight = Flight::firstWhere('active', 1);
```

Às vezes você pode querer executar alguma outra ação caso nenhum resultado seja encontrado. Os métodos `findOr` e `firstOr` retornarão uma única instância de model ou, se nenhum resultado for encontrado, executarão o closure fornecido. O valor retornado pelo closure será considerado o resultado do método:

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a id="not-found-exceptions"></a>
#### Exceções de Não Encontrado

Às vezes você pode querer lançar uma exceção se um model não for encontrado. Isso é particularmente útil em rotas ou controllers. Os métodos `findOrFail` e `firstOrFail` recuperarão o primeiro resultado da consulta; no entanto, se nenhum resultado for encontrado, uma `Illuminate\Database\Eloquent\ModelNotFoundException` será lançada:

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

Se a `ModelNotFoundException` não for capturada, uma resposta HTTP 404 é automaticamente enviada de volta ao cliente:

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a id="retrieving-or-creating-models"></a>
### Recuperando ou Criando Models

O método `firstOrCreate` tentará localizar um registro no banco de dados usando os pares coluna / valor fornecidos. Se o model não for encontrado no banco de dados, um registro será inserido com os atributos resultantes da mesclagem do primeiro argumento array com o segundo argumento array opcional.

O método `firstOrNew`, assim como o `firstOrCreate`, tentará localizar um registro no banco de dados que corresponda aos atributos fornecidos. No entanto, se um model não for encontrado, uma nova instância de model será retornada. Observe que o model retornado por `firstOrNew` ainda não foi persistido no banco de dados. Você precisará chamar manualmente o método `save` para persisti-lo:

```php
use App\Models\Flight;

// Retrieve flight by name or create it if it doesn't exist...
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// Retrieve flight by name or create it with the name, delayed, and arrival_time attributes...
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// Retrieve flight by name or instantiate a new Flight instance...
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// Retrieve flight by name or instantiate with the name, delayed, and arrival_time attributes...
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a id="retrieving-aggregates"></a>
### Recuperando Agregados

Ao interagir com models Eloquent, você também pode usar os métodos `count`, `sum`, `max` e outros [métodos de agregação](../queries/#aggregates) fornecidos pelo [query builder](../queries/) do Laravel. Como você pode esperar, esses métodos retornam um valor escalar em vez de uma instância de model Eloquent:

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a id="inserting-and-updating-models"></a>
## Inserindo e Atualizando Models

<a id="inserts"></a>
### Inserções

Claro que, ao usar o Eloquent, não precisamos apenas recuperar models do banco de dados. Também precisamos inserir novos registros. Felizmente, o Eloquent torna isso simples. Para inserir um novo registro no banco de dados, você deve instanciar um novo model e definir os atributos nele. Em seguida, chame o método `save` na instância do model:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * Store a new flight in the database.
     */
    public function store(Request $request): RedirectResponse
    {
        // Validate the request...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();

        return redirect('/flights');
    }
}
```

Neste exemplo, atribuímos o campo `name` da requisição HTTP recebida ao atributo `name` da instância do model `App\Models\Flight`. Quando invocamos o método `save`, um registro será inserido no banco de dados. Os timestamps `created_at` e `updated_at` do model serão definidos automaticamente quando o método `save` for chamado, portanto não há necessidade de defini-los manualmente.

Se você quiser salvar o model dentro de uma transação de banco de dados, pode usar o método `saveOrFail`. Se uma exceção for lançada durante o salvamento, a transação será automaticamente desfeita (rollback):

```php
$flight->saveOrFail();
```

Alternativamente, você pode usar o método `create` para "salvar" um novo model usando uma única instrução PHP. A instância do model inserido será retornada pelo método `create`:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

No entanto, antes de usar o método `create`, você precisará especificar um atributo `Fillable` ou `Guarded` na classe do seu model. Esses atributos são necessários porque todos os models Eloquent são protegidos contra vulnerabilidades de atribuição em massa por padrão. Para saber mais sobre atribuição em massa, consulte a [documentação de atribuição em massa](#mass-assignment).

<a id="updates"></a>
### Atualizações

O método `save` também pode ser usado para atualizar models que já existem no banco de dados. Para atualizar um model, você deve recuperá-lo e definir os atributos que deseja atualizar. Em seguida, deve chamar o método `save` do model. Novamente, o timestamp `updated_at` será atualizado automaticamente, portanto não há necessidade de definir seu valor manualmente:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

Se você quiser atualizar o model dentro de uma transação de banco de dados, pode usar o método `updateOrFail`. Se uma exceção for lançada durante a atualização, a transação será automaticamente desfeita (rollback):

```php
$flight->updateOrFail(['name' => 'Paris to London']);
```

Ocasionalmente, você pode precisar atualizar um model existente ou criar um novo model caso nenhum model correspondente exista. Assim como o método `firstOrCreate`, o método `updateOrCreate` persiste o model, portanto não há necessidade de chamar manualmente o método `save`.

No exemplo abaixo, se existir um voo com local de partida `Oakland` e local de destino `San Diego`, suas colunas `price` e `discounted` serão atualizadas. Se nenhum voo desse tipo existir, um novo voo será criado com os atributos resultantes da mesclagem do array do primeiro argumento com o array do segundo argumento:

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

Ao usar métodos como `firstOrCreate` ou `updateOrCreate`, você pode não saber se um novo model foi criado ou se um existente foi atualizado. A propriedade `wasRecentlyCreated` indica se o model foi criado durante o seu ciclo de vida atual:

```php
$flight = Flight::updateOrCreate(
    // ...
);

if ($flight->wasRecentlyCreated) {
    // New flight record was inserted...
}
```

<a id="mass-updates"></a>
#### Atualizações em Massa

Atualizações também podem ser realizadas em models que correspondem a uma determinada consulta. Neste exemplo, todos os voos que estão `active` e têm `destination` igual a `San Diego` serão marcados como atrasados:

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

O método `update` espera um array de pares coluna e valor representando as colunas que devem ser atualizadas. O método `update` retorna o número de linhas afetadas.

> **Aviso:**
> Ao emitir uma atualização em massa via Eloquent, os eventos de model `saving`, `saved`, `updating` e `updated` não serão disparados para os models atualizados. Isso ocorre porque os models nunca são realmente recuperados ao emitir uma atualização em massa.

<a id="examining-attribute-changes"></a>
#### Examinando Alterações de Atributos

O Eloquent fornece os métodos `isDirty`, `isClean` e `wasChanged` para examinar o estado interno do seu model e determinar como seus atributos mudaram desde que o model foi originalmente recuperado.

O método `isDirty` determina se algum dos atributos do model foi alterado desde que o model foi recuperado. Você pode passar um nome de atributo específico ou um array de atributos ao método `isDirty` para determinar se algum dos atributos está "sujo" (modificado). O método `isClean` determinará se um atributo permaneceu inalterado desde que o model foi recuperado. Este método também aceita um argumento opcional de atributo:

```php
use App\Models\User;

$user = User::create([
    'first_name' => 'Taylor',
    'last_name' => 'Otwell',
    'title' => 'Developer',
]);

$user->title = 'Painter';

$user->isDirty(); // true
$user->isDirty('title'); // true
$user->isDirty('first_name'); // false
$user->isDirty(['first_name', 'title']); // true

$user->isClean(); // false
$user->isClean('title'); // false
$user->isClean('first_name'); // true
$user->isClean(['first_name', 'title']); // false

$user->save();

$user->isDirty(); // false
$user->isClean(); // true
```

O método `wasChanged` determina se algum atributo foi alterado quando o model foi salvo pela última vez dentro do ciclo da requisição atual. Se necessário, você pode passar um nome de atributo para verificar se um atributo específico foi alterado:

```php
$user = User::create([
    'first_name' => 'Taylor',
    'last_name' => 'Otwell',
    'title' => 'Developer',
]);

$user->title = 'Painter';

$user->save();

$user->wasChanged(); // true
$user->wasChanged('title'); // true
$user->wasChanged(['title', 'slug']); // true
$user->wasChanged('first_name'); // false
$user->wasChanged(['first_name', 'title']); // true
```

O método `getOriginal` retorna um array contendo os atributos originais do model, independentemente de quaisquer alterações feitas no model desde que foi recuperado. Se necessário, você pode passar um nome de atributo específico para obter o valor original de um atributo específico:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // Array of original attributes...
```

O método `getChanges` retorna um array contendo os atributos que foram alterados quando o model foi salvo pela última vez, enquanto o método `getPrevious` retorna um array contendo os valores originais dos atributos antes de o model ser salvo pela última vez:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->update([
    'name' => 'Jack',
    'email' => 'jack@example.com',
]);

$user->getChanges();

/*
    [
        'name' => 'Jack',
        'email' => 'jack@example.com',
    ]
*/

$user->getPrevious();

/*
    [
        'name' => 'John',
        'email' => 'john@example.com',
    ]
*/
```

<a id="mass-assignment"></a>
### Atribuição em Massa

Você pode usar o método `create` para "salvar" um novo model usando uma única instrução PHP. A instância do model inserido será retornada pelo método:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

No entanto, antes de usar o método `create`, você precisará especificar um atributo `Fillable` ou `Guarded` na classe do seu model. Esses atributos são necessários porque todos os models Eloquent são protegidos contra vulnerabilidades de atribuição em massa por padrão.

Uma vulnerabilidade de atribuição em massa ocorre quando um usuário envia um campo inesperado na requisição HTTP e esse campo altera uma coluna do seu banco de dados que você não esperava. Por exemplo, um usuário mal-intencionado pode enviar um parâmetro `is_admin` por meio de uma requisição HTTP, que então é passado ao método `create` do seu model, permitindo que o usuário se eleve a administrador.

Assim, para começar, você deve definir quais atributos do model você deseja tornar atribuíveis em massa. Você pode fazer isso usando o atributo `Fillable` no model. Por exemplo, vamos tornar o atributo `name` do nosso model `Flight` atribuível em massa:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;

#[Fillable(['name'])]
class Flight extends Model
{
    // ...
}
```

Depois de especificar quais atributos são atribuíveis em massa, você pode usar o método `create` para inserir um novo registro no banco de dados. O método `create` retorna a instância do model recém-criado:

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

Se você já possui uma instância de model, pode usar o método `fill` para preenchê-la com um array de atributos:

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a id="mass-assignment-json-columns"></a>
#### Atribuição em Massa e Colunas JSON

Ao atribuir colunas JSON, a chave atribuível em massa de cada coluna deve ser especificada no atributo `Fillable` do seu model. Por segurança, o Laravel não oferece suporte à atualização de atributos JSON aninhados ao usar o atributo `Guarded`:

```php
use Illuminate\Database\Eloquent\Attributes\Fillable;

#[Fillable(['options->enabled'])]
class Flight extends Model
{
    // ...
}
```

<a id="allowing-mass-assignment"></a>
#### Permitindo Atribuição em Massa

Se você quiser tornar todos os atributos do seu model atribuíveis em massa, pode usar o atributo `Unguarded` no seu model. Se optar por remover a proteção do model, você deve tomar cuidado especial para sempre montar manualmente os arrays passados aos métodos `fill`, `create` e `update` do Eloquent:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Unguarded;
use Illuminate\Database\Eloquent\Model;

#[Unguarded]
class Flight extends Model
{
    // ...
}
```

<a id="mass-assignment-exceptions"></a>
#### Exceções de Atribuição em Massa

Por padrão, atributos que não estão incluídos no atributo `Fillable` são descartados silenciosamente ao realizar operações de atribuição em massa. Em produção, esse é o comportamento esperado; no entanto, durante o desenvolvimento local isso pode causar confusão sobre por que as alterações no model não estão tendo efeito.

Se desejar, você pode instruir o Laravel a lançar uma exceção ao tentar preencher um atributo não preenchível invocando o método `preventSilentlyDiscardingAttributes`. Normalmente, este método deve ser invocado no método `boot` da classe `AppServiceProvider` da sua aplicação:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```

<a id="upserts"></a>
### Upserts

O método `upsert` do Eloquent pode ser usado para atualizar ou criar registros em uma única operação atômica. O primeiro argumento do método consiste nos valores a serem inseridos ou atualizados, enquanto o segundo argumento lista a(s) coluna(s) que identificam de forma única os registros na tabela associada. O terceiro e último argumento do método é um array com as colunas que devem ser atualizadas caso um registro correspondente já exista no banco de dados. O método `upsert` definirá automaticamente os timestamps `created_at` e `updated_at` se os timestamps estiverem habilitados no model:

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> **Aviso:**
> Todos os bancos de dados, exceto o SQL Server, exigem que as colunas do segundo argumento do método `upsert` tenham um índice "primary" ou "unique". Além disso, os drivers de banco de dados MariaDB e MySQL ignoram o segundo argumento do método `upsert` e sempre usam os índices "primary" e "unique" da tabela para detectar registros existentes.

<a id="deleting-models"></a>
## Deletando Models

Para deletar um model, você pode chamar o método `delete` na instância do model:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

Se você quiser deletar o model dentro de uma transação de banco de dados, pode usar o método `deleteOrFail`. Se uma exceção for lançada durante a exclusão, a transação será automaticamente desfeita (rollback):

```php
$flight->deleteOrFail();
```

<a id="deleting-an-existing-model-by-its-primary-key"></a>
#### Deletando um Model Existente Pela Sua Chave Primária

No exemplo acima, estamos recuperando o model do banco de dados antes de chamar o método `delete`. No entanto, se você souber a chave primária do model, pode deletar o model sem recuperá-lo explicitamente, chamando o método `destroy`. Além de aceitar uma única chave primária, o método `destroy` aceita várias chaves primárias, um array de chaves primárias ou uma [coleção](../collections/) de chaves primárias:

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

Se você estiver utilizando [models com soft delete](#soft-deleting), pode deletar models permanentemente por meio do método `forceDestroy`:

```php
Flight::forceDestroy(1);
```

> **Aviso:**
> O método `destroy` carrega cada model individualmente e chama o método `delete` para que os eventos `deleting` e `deleted` sejam corretamente disparados para cada model.

<a id="deleting-models-using-queries"></a>
#### Deletando Models Usando Consultas

Claro que você pode construir uma consulta Eloquent para deletar todos os models que correspondem aos critérios da sua consulta. Neste exemplo, vamos deletar todos os voos marcados como inativos. Assim como nas atualizações em massa, as exclusões em massa não dispararão eventos de model para os models deletados:

```php
$deleted = Flight::where('active', 0)->delete();
```

Para deletar todos os models de uma tabela, você deve executar uma consulta sem adicionar nenhuma condição:

```php
$deleted = Flight::query()->delete();
```

> **Aviso:**
> Ao executar uma instrução de exclusão em massa via Eloquent, os eventos de model `deleting` e `deleted` não serão disparados para os models deletados. Isso ocorre porque os models nunca são realmente recuperados ao executar a instrução de exclusão.

<a id="soft-deleting"></a>
### Soft Delete

Além de remover de fato os registros do seu banco de dados, o Eloquent também pode fazer "soft delete" de models. Quando models sofrem soft delete, eles não são realmente removidos do banco de dados. Em vez disso, um atributo `deleted_at` é definido no model, indicando a data e hora em que o model foi "deletado". Para habilitar o soft delete em um model, adicione a trait `Illuminate\Database\Eloquent\SoftDeletes` ao model:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Flight extends Model
{
    use SoftDeletes;
}
```

> **Nota:**
> A trait `SoftDeletes` converterá automaticamente o atributo `deleted_at` para uma instância de `DateTime` / `Carbon` para você.

Você também deve adicionar a coluna `deleted_at` à sua tabela do banco de dados. O [schema builder](../migrations/) do Laravel contém um método auxiliar para criar essa coluna:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('flights', function (Blueprint $table) {
    $table->softDeletes();
});

Schema::table('flights', function (Blueprint $table) {
    $table->dropSoftDeletes();
});
```

Agora, quando você chamar o método `delete` no model, a coluna `deleted_at` será definida com a data e hora atuais. No entanto, o registro do model permanecerá na tabela. Ao consultar um model que utiliza soft delete, os models com soft delete serão automaticamente excluídos de todos os resultados de consulta.

Para determinar se uma determinada instância de model sofreu soft delete, você pode usar o método `trashed`:

```php
if ($flight->trashed()) {
    // ...
}
```

<a id="restoring-soft-deleted-models"></a>
#### Restaurando Models com Soft Delete

Às vezes você pode desejar "desfazer a exclusão" de um model com soft delete. Para restaurar um model com soft delete, você pode chamar o método `restore` em uma instância do model. O método `restore` definirá a coluna `deleted_at` do model como `null`:

```php
$flight->restore();
```

Você também pode usar o método `restore` em uma consulta para restaurar vários models. Novamente, assim como outras operações "em massa", isso não disparará nenhum evento de model para os models restaurados:

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

O método `restore` também pode ser usado ao construir consultas de [relacionamento](../eloquent-relationships/):

```php
$flight->history()->restore();
```

<a id="permanently-deleting-models"></a>
#### Deletando Models Permanentemente

Às vezes você pode precisar remover de fato um model do seu banco de dados. Você pode usar o método `forceDelete` para remover permanentemente um model com soft delete da tabela do banco de dados:

```php
$flight->forceDelete();
```

Você também pode usar o método `forceDelete` ao construir consultas de relacionamento do Eloquent:

```php
$flight->history()->forceDelete();
```

<a id="querying-soft-deleted-models"></a>
### Consultando Models Com Soft Delete

<a id="including-soft-deleted-models"></a>
#### Incluindo Models com Soft Delete

Como observado acima, models com soft delete são automaticamente excluídos dos resultados de consulta. No entanto, você pode forçar a inclusão de models com soft delete nos resultados de uma consulta chamando o método `withTrashed` na consulta:

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

O método `withTrashed` também pode ser chamado ao construir uma consulta de [relacionamento](../eloquent-relationships/):

```php
$flight->history()->withTrashed()->get();
```

<a id="retrieving-only-soft-deleted-models"></a>
#### Recuperando Apenas Models com Soft Delete

O método `onlyTrashed` recuperará **apenas** models com soft delete:

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a id="pruning-models"></a>
## Podando Models

Às vezes você pode querer deletar periodicamente models que não são mais necessários. Para isso, você pode adicionar a trait `Illuminate\Database\Eloquent\Prunable` ou `Illuminate\Database\Eloquent\MassPrunable` aos models que deseja podar periodicamente. Depois de adicionar uma das traits ao model, implemente um método `prunable` que retorne um query builder do Eloquent que resolva os models que não são mais necessários:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Prunable;

class Flight extends Model
{
    use Prunable;

    /**
     * Get the prunable model query.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```

Ao marcar models como `Prunable`, você também pode definir um método `pruning` no model. Este método será chamado antes de o model ser deletado. Esse método pode ser útil para deletar quaisquer recursos adicionais associados ao model, como arquivos armazenados, antes que ele seja removido permanentemente do banco de dados:

```php
/**
 * Prepare the model for pruning.
 */
protected function pruning(): void
{
    // ...
}
```

Depois de configurar seu model podável, você deve agendar o comando Artisan `model:prune` no arquivo `routes/console.php` da sua aplicação. Você é livre para escolher o intervalo apropriado em que esse comando deve ser executado:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

Nos bastidores, o comando `model:prune` detectará automaticamente models "Prunable" dentro do diretório `app/Models` da sua aplicação. Se os seus models estiverem em outro local, você pode usar a opção `--model` para especificar os nomes das classes dos models:

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

Se você quiser excluir certos models da poda enquanto poda todos os outros models detectados, pode usar a opção `--except`:

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

Você pode testar sua consulta `prunable` executando o comando `model:prune` com a opção `--pretend`. Quando em modo simulação, o comando `model:prune` apenas informará quantos registros seriam podados caso o comando fosse executado de fato:

```shell
php artisan model:prune --pretend
```

> **Aviso:**
> Models com soft delete serão deletados permanentemente (`forceDelete`) se corresponderem à consulta de poda.

<a id="mass-pruning"></a>
#### Poda em Massa

Quando models são marcados com a trait `Illuminate\Database\Eloquent\MassPrunable`, eles são deletados do banco de dados usando consultas de exclusão em massa. Portanto, o método `pruning` não será invocado, nem os eventos de model `deleting` e `deleted` serão disparados. Isso ocorre porque os models nunca são realmente recuperados antes da exclusão, tornando o processo de poda muito mais eficiente:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\MassPrunable;

class Flight extends Model
{
    use MassPrunable;

    /**
     * Get the prunable model query.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```


<a id="replicating-models"></a>
## Replicando Models

Você pode criar uma cópia não salva de uma instância de model existente usando o método `replicate`. Este método é particularmente útil quando você tem instâncias de model que compartilham muitos dos mesmos atributos:

```php
use App\Models\Address;

$shipping = Address::create([
    'type' => 'shipping',
    'line_1' => '123 Example Street',
    'city' => 'Victorville',
    'state' => 'CA',
    'postcode' => '90001',
]);

$billing = $shipping->replicate()->fill([
    'type' => 'billing'
]);

$billing->save();
```

Para excluir um ou mais atributos da replicação para o novo model, você pode passar um array ao método `replicate`:

```php
$flight = Flight::create([
    'destination' => 'LAX',
    'origin' => 'LHR',
    'last_flown' => '2020-03-04 11:00:00',
    'last_pilot_id' => 747,
]);

$flight = $flight->replicate([
    'last_flown',
    'last_pilot_id'
]);
```

<a id="query-scopes"></a>
## Escopos de Consulta

<a id="global-scopes"></a>
### Escopos Globais

Escopos globais permitem adicionar restrições a todas as consultas de um determinado model. A própria funcionalidade de [soft delete](#soft-deleting) do Laravel utiliza escopos globais para recuperar apenas models "não deletados" do banco de dados. Escrever seus próprios escopos globais pode ser uma forma conveniente e prática de garantir que todas as consultas de um determinado model recebam certas restrições.

<a id="generating-scopes"></a>
#### Gerando Escopos

Para gerar um novo escopo global, você pode invocar o comando Artisan `make:scope`, que colocará o escopo gerado no diretório `app/Models/Scopes` da sua aplicação:

```shell
php artisan make:scope AncientScope
```

<a id="writing-global-scopes"></a>
#### Escrevendo Escopos Globais

Escrever um escopo global é simples. Primeiro, use o comando `make:scope` para gerar uma classe que implementa a interface `Illuminate\Database\Eloquent\Scope`. A interface `Scope` exige que você implemente um método: `apply`. O método `apply` pode adicionar cláusulas `where` ou outros tipos de cláusulas à consulta conforme necessário:

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * Apply the scope to a given Eloquent query builder.
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->minus(years: 2000));
    }
}
```

> **Nota:**
> Se o seu escopo global estiver adicionando colunas à cláusula select da consulta, você deve usar o método `addSelect` em vez de `select`. Isso evitará a substituição não intencional da cláusula select existente da consulta.

<a id="applying-global-scopes"></a>
#### Aplicando Escopos Globais

Para atribuir um escopo global a um model, você pode simplesmente colocar o atributo `ScopedBy` no model:

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Attributes\ScopedBy;

#[ScopedBy([AncientScope::class])]
class User extends Model
{
    //
}
```

Ou você pode registrar manualmente o escopo global sobrescrevendo o método `booted` do model e invocando o método `addGlobalScope` do model. O método `addGlobalScope` aceita uma instância do seu escopo como seu único argumento:

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

Depois de adicionar o escopo do exemplo acima ao model `App\Models\User`, uma chamada ao método `User::all()` executará a seguinte consulta SQL:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a id="anonymous-global-scopes"></a>
#### Escopos Globais Anônimos

O Eloquent também permite definir escopos globais usando closures, o que é particularmente útil para escopos simples que não justificam uma classe separada. Ao definir um escopo global usando um closure, você deve fornecer um nome de escopo de sua escolha como primeiro argumento do método `addGlobalScope`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::addGlobalScope('ancient', function (Builder $builder) {
            $builder->where('created_at', '<', now()->minus(years: 2000));
        });
    }
}
```

<a id="removing-global-scopes"></a>
#### Removendo Escopos Globais

Se você quiser remover um escopo global para uma determinada consulta, pode usar o método `withoutGlobalScope`. Este método aceita o nome da classe do escopo global como seu único argumento:

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

Ou, se você definiu o escopo global usando um closure, deve passar o nome em string que você atribuiu ao escopo global:

```php
User::withoutGlobalScope('ancient')->get();
```

Se você quiser remover vários ou até todos os escopos globais da consulta, pode usar os métodos `withoutGlobalScopes` e `withoutGlobalScopesExcept`:

```php
// Remove all of the global scopes...
User::withoutGlobalScopes()->get();

// Remove some of the global scopes...
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();

// Remove all global scopes except the given ones...
User::withoutGlobalScopesExcept([
    SecondScope::class,
])->get();
```

<a id="local-scopes"></a>
### Escopos Locais

Escopos locais permitem definir conjuntos comuns de restrições de consulta que você pode reutilizar facilmente em toda a aplicação. Por exemplo, você pode precisar recuperar frequentemente todos os usuários considerados "populares". Para definir um escopo, adicione o atributo `Scope` a um método do Eloquent.

Escopos devem sempre retornar a mesma instância do query builder ou `void`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Scope a query to only include popular users.
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * Scope a query to only include active users.
     */
    #[Scope]
    protected function active(Builder $query): void
    {
        $query->where('active', 1);
    }
}
```

<a id="utilizing-a-local-scope"></a>
#### Utilizando um Escopo Local

Depois que o escopo for definido, você pode chamar os métodos de escopo ao consultar o model. Você pode até encadear chamadas de vários escopos:

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

Combinar vários escopos de model do Eloquent por meio do operador de consulta `or` pode exigir o uso de closures para obter o [agrupamento lógico](../queries/#logical-grouping) correto:

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

No entanto, como isso pode ser trabalhoso, o Laravel fornece um método `orWhere` de "ordem superior" que permite encadear escopos de forma fluente sem o uso de closures:

```php
$users = User::popular()->orWhere->active()->get();
```

<a id="dynamic-scopes"></a>
#### Escopos Dinâmicos

Às vezes você pode desejar definir um escopo que aceite parâmetros. Para começar, basta adicionar seus parâmetros adicionais à assinatura do método de escopo. Os parâmetros do escopo devem ser definidos após o parâmetro `$query`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Scope a query to only include users of a given type.
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

Depois que os argumentos esperados forem adicionados à assinatura do método de escopo, você pode passar os argumentos ao chamar o escopo:

```php
$users = User::ofType('admin')->get();
```

Métodos de escopo com atributo devem ser `protected`. Ao chamar um escopo com atributo de dentro da classe do model, chame o escopo por meio de uma instância de query builder, como `static::query()->ofType('admin')`, para garantir que a chamada seja roteada pelo tratamento de escopos do Eloquent.

<a id="pending-attributes"></a>
### Atributos Pendentes

Se você quiser usar escopos para criar models que têm os mesmos atributos usados para restringir o escopo, pode usar o método `withAttributes` ao construir a consulta do escopo:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * Scope the query to only include drafts.
     */
    #[Scope]
    protected function draft(Builder $query): void
    {
        $query->withAttributes([
            'hidden' => true,
        ]);
    }
}
```

O método `withAttributes` adicionará condições `where` à consulta usando os atributos fornecidos, e também adicionará os atributos fornecidos a quaisquer models criados por meio do escopo:

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

Para instruir o método `withAttributes` a não adicionar condições `where` à consulta, você pode definir o argumento `asConditions` como `false`:

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a id="comparing-models"></a>
## Comparando Models

Às vezes você pode precisar determinar se dois models são "os mesmos" ou não. Os métodos `is` e `isNot` podem ser usados para verificar rapidamente se dois models têm a mesma chave primária, tabela e conexão de banco de dados, ou não:

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

Os métodos `is` e `isNot` também estão disponíveis ao usar os relacionamentos `belongsTo`, `hasOne`, `morphTo` e `morphOne` [relacionamentos](../eloquent-relationships/). Este método é particularmente útil quando você deseja comparar um model relacionado sem executar uma consulta para recuperar esse model:

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a id="events"></a>
## Eventos

> **Nota:**
> Quer transmitir seus eventos do Eloquent diretamente para a sua aplicação do lado do cliente? Confira a [transmissão de eventos de model](../broadcasting/#model-broadcasting) do Laravel.

Models Eloquent disparam vários eventos, permitindo que você se conecte aos seguintes momentos do ciclo de vida de um model: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored` e `replicating`.

O evento `retrieved` será disparado quando um model existente for recuperado do banco de dados. Quando um novo model é salvo pela primeira vez, os eventos `creating` e `created` serão disparados. Os eventos `updating` / `updated` serão disparados quando um model existente for modificado e o método `save` for chamado. Os eventos `saving` / `saved` serão disparados quando um model for criado ou atualizado - mesmo que os atributos do model não tenham sido alterados. Nomes de eventos que terminam em `-ing` são disparados antes de quaisquer alterações no model serem persistidas, enquanto eventos que terminam em `-ed` são disparados após as alterações no model serem persistidas.

Para começar a escutar eventos de model, defina uma propriedade `$dispatchesEvents` no seu model Eloquent. Essa propriedade mapeia vários pontos do ciclo de vida do model Eloquent para suas próprias [classes de evento](../events/). Cada classe de evento de model deve esperar receber uma instância do model afetado por meio do seu construtor:

```php
<?php

namespace App\Models;

use App\Events\UserDeleted;
use App\Events\UserSaved;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * The event map for the model.
     *
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

Depois de definir e mapear seus eventos do Eloquent, você pode usar [ouvintes de eventos](../events/#defining-listeners) para tratar os eventos.

> **Aviso:**
> Ao emitir uma consulta de atualização ou exclusão em massa via Eloquent, os eventos de model `saved`, `updated`, `deleting` e `deleted` não serão disparados para os models afetados. Isso ocorre porque os models nunca são realmente recuperados ao realizar atualizações ou exclusões em massa.

<a id="events-using-closures"></a>
### Usando Closures

Em vez de usar classes de evento personalizadas, você pode registrar closures que são executados quando vários eventos de model são disparados. Normalmente, você deve registrar esses closures no método `booted` do seu model:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```

Se necessário, você pode utilizar [ouvintes de eventos anônimos enfileiráveis](../events/#queueable-anonymous-event-listeners) ao registrar eventos de model. Isso instruirá o Laravel a executar o ouvinte do evento do model em segundo plano, usando a [fila](../queues/) da sua aplicação:

```php
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```

<a id="observers"></a>
### Observers

<a id="defining-observers"></a>
#### Definindo Observers

Se você estiver escutando muitos eventos de um determinado model, pode usar observers para agrupar todos os seus ouvintes em uma única classe. As classes de observer têm nomes de métodos que refletem os eventos do Eloquent que você deseja escutar. Cada um desses métodos recebe o model afetado como seu único argumento. O comando Artisan `make:observer` é a maneira mais fácil de criar uma nova classe de observer:

```shell
php artisan make:observer UserObserver --model=User
```

Este comando colocará o novo observer no diretório `app/Observers` da sua aplicação. Se esse diretório não existir, o Artisan o criará para você. Seu novo observer ficará parecido com o seguinte:

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * Handle the User "created" event.
     */
    public function created(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "updated" event.
     */
    public function updated(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "deleted" event.
     */
    public function deleted(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "restored" event.
     */
    public function restored(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "forceDeleted" event.
     */
    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```

Para registrar um observer, você pode colocar o atributo `ObservedBy` no model correspondente:

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

Ou você pode registrar manualmente um observer invocando o método `observe` no model que deseja observar. Você pode registrar observers no método `boot` da classe `AppServiceProvider` da sua aplicação:

```php
use App\Models\User;
use App\Observers\UserObserver;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    User::observe(UserObserver::class);
}
```

> **Nota:**
> Há eventos adicionais que um observer pode escutar, como `saving` e `retrieved`. Esses eventos são descritos na documentação de [eventos](#events).

<a id="observers-and-database-transactions"></a>
#### Observers e Transações de Banco de Dados

Quando models estão sendo criados dentro de uma transação de banco de dados, você pode querer instruir um observer a executar seus manipuladores de evento somente após a transação de banco de dados ser confirmada (commit). Você pode fazer isso implementando a interface `ShouldHandleEventsAfterCommit` no seu observer. Se não houver uma transação de banco de dados em andamento, os manipuladores de evento serão executados imediatamente:

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    /**
     * Handle the User "created" event.
     */
    public function created(User $user): void
    {
        // ...
    }
}
```

<a id="muting-events"></a>
### Silenciando Eventos

Você pode ocasionalmente precisar "silenciar" temporariamente todos os eventos disparados por um model. Você pode fazer isso usando o método `withoutEvents`. O método `withoutEvents` aceita um closure como seu único argumento. Qualquer código executado dentro desse closure não disparará eventos de model, e qualquer valor retornado pelo closure será retornado pelo método `withoutEvents`:

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a id="saving-a-single-model-without-events"></a>
#### Salvando um Único Model Sem Eventos

Às vezes você pode desejar "salvar" um determinado model sem disparar nenhum evento. Você pode fazer isso usando o método `saveQuietly`:

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

Você também pode "atualizar", "deletar", fazer "soft delete", "restaurar" e "replicar" um determinado model sem disparar nenhum evento:

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
