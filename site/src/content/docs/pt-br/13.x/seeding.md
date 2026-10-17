---
title: "Banco de Dados: Seeding"
---

- [Introdução](#introduction)
- [Escrevendo Seeders](#writing-seeders)
    - [Usando Model Factories](#using-model-factories)
    - [Chamando Seeders Adicionais](#calling-additional-seeders)
    - [Silenciando Eventos de Model](#muting-model-events)
- [Executando Seeders](#running-seeders)

<a id="introduction"></a>
## Introdução

O Laravel inclui a capacidade de popular seu banco de dados com dados usando classes de seed. Todas as classes de seed são armazenadas no diretório `database/seeders`. Por padrão, uma classe `DatabaseSeeder` é definida para você. A partir dessa classe, você pode usar o método `call` para executar outras classes de seed, permitindo que você controle a ordem do seeding.

> **Nota:**
> A [proteção contra atribuição em massa](../eloquent/#mass-assignment) é automaticamente desabilitada durante o seeding do banco de dados.

<a id="writing-seeders"></a>
## Escrevendo Seeders

Para gerar um seeder, execute o [comando Artisan](../artisan/) `make:seeder`. Todos os seeders gerados pelo framework serão colocados no diretório `database/seeders`:

```shell
php artisan make:seeder UserSeeder
```

Uma classe de seeder contém apenas um método por padrão: `run`. Esse método é chamado quando o [comando Artisan](../artisan/) `db:seed` é executado. Dentro do método `run`, você pode inserir dados no seu banco de dados como quiser. Você pode usar o [query builder](../queries/) para inserir dados manualmente ou pode usar [model factories do Eloquent](../eloquent-factories/).

Como exemplo, vamos modificar a classe `DatabaseSeeder` padrão e adicionar uma instrução de inserção no banco de dados ao método `run`:

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

class DatabaseSeeder extends Seeder
{
    /**
     * Run the database seeders.
     */
    public function run(): void
    {
        DB::table('users')->insert([
            'name' => Str::random(10),
            'email' => Str::random(10).'@example.com',
            'password' => Hash::make('password'),
        ]);
    }
}
```

> **Nota:**
> Você pode fazer type-hint de quaisquer dependências que precise na assinatura do método `run`. Elas serão automaticamente resolvidas através do [service container](../container/) do Laravel.

<a id="using-model-factories"></a>
### Usando Model Factories

Obviamente, especificar manualmente os atributos de cada seed de model é trabalhoso. Em vez disso, você pode usar [model factories](../eloquent-factories/) para gerar convenientemente grandes quantidades de registros no banco de dados. Primeiro, revise a [documentação de model factory](../eloquent-factories/) para aprender como definir suas factories.

Por exemplo, vamos criar 50 usuários, cada um com um post relacionado:

```php
use App\Models\User;

/**
 * Run the database seeders.
 */
public function run(): void
{
    User::factory()
        ->count(50)
        ->hasPosts(1)
        ->create();
}
```

<a id="calling-additional-seeders"></a>
### Chamando Seeders Adicionais

Dentro da classe `DatabaseSeeder`, você pode usar o método `call` para executar classes de seed adicionais. Usar o método `call` permite dividir o seeding do seu banco de dados em múltiplos arquivos, para que nenhuma classe de seeder individual se torne grande demais. O método `call` aceita um array de classes de seeder que devem ser executadas:

```php
/**
 * Run the database seeders.
 */
public function run(): void
{
    $this->call([
        UserSeeder::class,
        PostSeeder::class,
        CommentSeeder::class,
    ]);
}
```

<a id="muting-model-events"></a>
### Silenciando Eventos de Model

Ao executar seeds, você pode querer impedir que os models despachem eventos. Você pode conseguir isso usando a trait `WithoutModelEvents`. Quando usada, a trait `WithoutModelEvents` garante que nenhum evento de model seja despachado, mesmo que classes de seed adicionais sejam executadas através do método `call`:

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * Run the database seeders.
     */
    public function run(): void
    {
        $this->call([
            UserSeeder::class,
        ]);
    }
}
```

<a id="running-seeders"></a>
## Executando Seeders

Você pode executar o comando Artisan `db:seed` para popular seu banco de dados. Por padrão, o comando `db:seed` executa a classe `Database\Seeders\DatabaseSeeder`, que por sua vez pode invocar outras classes de seed. No entanto, você pode usar a opção `--class` para especificar uma classe de seeder específica a ser executada individualmente:

```shell
php artisan db:seed

php artisan db:seed --class=UserSeeder
```

Você também pode popular seu banco de dados usando o comando `migrate:fresh` em combinação com a opção `--seed`, que descartará todas as tabelas e executará novamente todas as suas migrations. Esse comando é útil para reconstruir completamente seu banco de dados. A opção `--seeder` pode ser usada para especificar um seeder específico a ser executado:

```shell
php artisan migrate:fresh --seed

php artisan migrate:fresh --seed --seeder=UserSeeder
```

<a id="forcing-seeding-production"></a>
#### Forçando a Execução de Seeders em Produção

Algumas operações de seeding podem fazer com que você altere ou perca dados. Para proteger você de executar comandos de seeding contra seu banco de dados de produção, você será solicitado a confirmar antes que os seeders sejam executados no ambiente `production`. Para forçar a execução dos seeders sem uma solicitação de confirmação, use a flag `--force`:

```shell
php artisan db:seed --force
```
