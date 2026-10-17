---
title: "Eloquent: Factories"
---

- [Introdução](#introduction)
- [Definindo Model Factories](#defining-model-factories)
    - [Gerando Factories](#generating-factories)
    - [States de Factory](#factory-states)
    - [Callbacks de Factory](#factory-callbacks)
- [Criando Models Usando Factories](#creating-models-using-factories)
    - [Instanciando Models](#instantiating-models)
    - [Persistindo Models](#persisting-models)
    - [Sequences](#sequences)
- [Relacionamentos de Factory](#factory-relationships)
    - [Relacionamentos Has Many](#has-many-relationships)
    - [Relacionamentos Belongs To](#belongs-to-relationships)
    - [Relacionamentos Many to Many](#many-to-many-relationships)
    - [Relacionamentos Polimórficos](#polymorphic-relationships)
    - [Definindo Relacionamentos Dentro de Factories](#defining-relationships-within-factories)
    - [Reciclando um Model Existente para Relacionamentos](#recycling-an-existing-model-for-relationships)

<a id="introduction"></a>
## Introdução

Ao testar sua aplicação ou popular seu banco de dados (seeding), você pode precisar inserir alguns registros no seu banco de dados. Em vez de especificar manualmente o valor de cada coluna, o Laravel permite que você defina um conjunto de atributos padrão para cada um dos seus [models do Eloquent](../eloquent/) usando model factories.

Para ver um exemplo de como escrever uma factory, dê uma olhada no arquivo `database/factories/UserFactory.php` na sua aplicação. Essa factory está incluída em todas as novas aplicações Laravel e contém a seguinte definição de factory:

```php
namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\User>
 */
class UserFactory extends Factory
{
    /**
     * The current password being used by the factory.
     */
    protected static ?string $password;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => static::$password ??= Hash::make('password'),
            'remember_token' => Str::random(10),
        ];
    }

    /**
     * Indicate that the model's email address should be unverified.
     */
    public function unverified(): static
    {
        return $this->state(fn (array $attributes) => [
            'email_verified_at' => null,
        ]);
    }
}
```

Como você pode ver, na sua forma mais básica, factories são classes que estendem a classe factory base do Laravel e definem um método `definition`. O método `definition` retorna o conjunto padrão de valores de atributos que devem ser aplicados ao criar um model usando a factory.

Através do helper `fake`, as factories têm acesso à biblioteca PHP [Faker](https://github.com/FakerPHP/Faker), que permite gerar convenientemente vários tipos de dados aleatórios para testes e seeding.

> **Note:**
> Você pode alterar o locale do Faker da sua aplicação atualizando a opção `faker_locale` no seu arquivo de configuração `config/app.php`.

<a id="defining-model-factories"></a>
## Definindo Model Factories

<a id="generating-factories"></a>
### Gerando Factories

Para criar uma factory, execute o [comando Artisan](../artisan/) `make:factory`:

```shell
php artisan make:factory PostFactory
```

A nova classe factory será colocada no seu diretório `database/factories`.

<a id="factory-and-model-discovery-conventions"></a>
#### Convenções de Descoberta de Model e Factory

Depois de definir suas factories, você pode usar o método estático `factory` fornecido aos seus models pela trait `Illuminate\Database\Eloquent\Factories\HasFactory` para instanciar uma instância de factory para aquele model.

O método `factory` da trait `HasFactory` usará convenções para determinar a factory apropriada para o model ao qual a trait está atribuída. Especificamente, o método procurará por uma factory no namespace `Database\Factories` que tenha um nome de classe correspondente ao nome do model e com o sufixo `Factory`. Se essas convenções não se aplicarem à sua aplicação ou factory específica, você pode adicionar o atributo `UseFactory` ao model para especificar manualmente a factory do model:

```php
use Illuminate\Database\Eloquent\Attributes\UseFactory;
use Database\Factories\Administration\FlightFactory;

#[UseFactory(FlightFactory::class)]
class Flight extends Model
{
    // ...
}
```

Alternativamente, você pode sobrescrever o método `newFactory` no seu model para retornar diretamente uma instância da factory correspondente do model:

```php
use Database\Factories\Administration\FlightFactory;

/**
 * Create a new factory instance for the model.
 */
protected static function newFactory()
{
    return FlightFactory::new();
}
```

Em seguida, use o atributo `UseModel` na factory correspondente para especificar o model:

```php
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Attributes\UseModel;
use Illuminate\Database\Eloquent\Factories\Factory;

#[UseModel(Flight::class)]
class FlightFactory extends Factory
{
    // ...
}
```

<a id="factory-states"></a>
### States de Factory

Métodos de manipulação de state permitem que você defina modificações discretas que podem ser aplicadas às suas model factories em qualquer combinação. Por exemplo, sua factory `Database\Factories\UserFactory` pode conter um método de state `suspended` que modifica um de seus valores de atributo padrão.

Métodos de transformação de state normalmente chamam o método `state` fornecido pela classe factory base do Laravel. O método `state` aceita uma closure que receberá o array de atributos brutos definidos para a factory e deve retornar um array de atributos a serem modificados:

```php
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * Indicate that the user is suspended.
 */
public function suspended(): Factory
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    });
}
```

<a id="trashed-state"></a>
#### State "Trashed"

Se o seu model do Eloquent pode ser [soft deleted](../eloquent/#soft-deleting), você pode invocar o método de state `trashed` integrado para indicar que o model criado já deve estar "soft deleted". Você não precisa definir manualmente o state `trashed`, pois ele está automaticamente disponível para todas as factories:

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a id="factory-callbacks"></a>
### Callbacks de Factory

Callbacks de factory são registrados usando os métodos `afterMaking` e `afterCreating` e permitem que você execute tarefas adicionais após criar (make) ou persistir (create) um model. Você deve registrar esses callbacks definindo um método `configure` na sua classe factory. Esse método será chamado automaticamente pelo Laravel quando a factory for instanciada:

```php
namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class UserFactory extends Factory
{
    /**
     * Configure the model factory.
     */
    public function configure(): static
    {
        return $this->afterMaking(function (User $user) {
            // ...
        })->afterCreating(function (User $user) {
            // ...
        });
    }

    // ...
}
```

Você também pode registrar callbacks de factory dentro de métodos de state para executar tarefas adicionais que são específicas de um determinado state:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * Indicate that the user is suspended.
 */
public function suspended(): Factory
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    })->afterMaking(function (User $user) {
        // ...
    })->afterCreating(function (User $user) {
        // ...
    });
}
```

<a id="creating-models-using-factories"></a>
## Criando Models Usando Factories

<a id="instantiating-models"></a>
### Instanciando Models

Depois de definir suas factories, você pode usar o método estático `factory` fornecido aos seus models pela trait `Illuminate\Database\Eloquent\Factories\HasFactory` para instanciar uma instância de factory para aquele model. Vamos dar uma olhada em alguns exemplos de criação de models. Primeiro, usaremos o método `make` para criar models sem persisti-los no banco de dados:

```php
use App\Models\User;

$user = User::factory()->make();
```

Você pode criar uma coleção de muitos models usando o método `count`:

```php
$users = User::factory()->count(3)->make();
```

<a id="applying-states"></a>
#### Aplicando States

Você também pode aplicar qualquer um dos seus [states](#factory-states) aos models. Se você gostaria de aplicar múltiplas transformações de state aos models, basta chamar os métodos de transformação de state diretamente:

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a id="overriding-attributes"></a>
#### Sobrescrevendo Atributos

Se você gostaria de sobrescrever alguns dos valores padrão dos seus models, você pode passar um array de valores ao método `make`. Apenas os atributos especificados serão substituídos, enquanto o restante dos atributos permanece definido com seus valores padrão conforme especificado pela factory:

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

Alternativamente, o método `state` pode ser chamado diretamente na instância da factory para realizar uma transformação de state inline:

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> **Note:**
> A [proteção contra mass assignment](../eloquent/#mass-assignment) é automaticamente desabilitada ao criar models usando factories.

<a id="persisting-models"></a>
### Persistindo Models

O método `create` instancia instâncias de model e as persiste no banco de dados usando o método `save` do Eloquent:

```php
use App\Models\User;

// Create a single App\Models\User instance...
$user = User::factory()->create();

// Create three App\Models\User instances...
$users = User::factory()->count(3)->create();
```

Você pode sobrescrever os atributos padrão de model da factory passando um array de atributos ao método `create`:

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a id="sequences"></a>
### Sequences

Às vezes você pode desejar alternar o valor de um determinado atributo de model para cada model criado. Você pode fazer isso definindo uma transformação de state como uma sequence. Por exemplo, você pode desejar alternar o valor de uma coluna `admin` entre `Y` e `N` para cada usuário criado:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        ['admin' => 'Y'],
        ['admin' => 'N'],
    ))
    ->create();
```

Neste exemplo, cinco usuários serão criados com um valor `admin` de `Y` e cinco usuários serão criados com um valor `admin` de `N`.

Se necessário, você pode incluir uma closure como um valor de sequence. A closure será invocada cada vez que a sequence precisar de um novo valor:

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

Dentro de uma closure de sequence, você pode acessar a propriedade `$index` na instância de sequence que é injetada na closure. A propriedade `$index` contém o número de iterações pela sequence que ocorreram até o momento:

```php
$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index],
    ))
    ->create();
```

Por conveniência, sequences também podem ser aplicadas usando o método `sequence`, que simplesmente invoca o método `state` internamente. O método `sequence` aceita uma closure ou arrays de atributos sequenciados:

```php
$users = User::factory()
    ->count(2)
    ->sequence(
        ['name' => 'First User'],
        ['name' => 'Second User'],
    )
    ->create();
```

<a id="factory-relationships"></a>
## Relacionamentos de Factory

<a id="has-many-relationships"></a>
### Relacionamentos Has Many

A seguir, vamos explorar a construção de relacionamentos de model do Eloquent usando os métodos fluentes de factory do Laravel. Primeiro, vamos supor que nossa aplicação tenha um model `App\Models\User` e um model `App\Models\Post`. Além disso, vamos supor que o model `User` define um relacionamento `hasMany` com `Post`. Podemos criar um usuário que tenha três posts usando o método `has` fornecido pelas factories do Laravel. O método `has` aceita uma instância de factory:

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

Por convenção, ao passar um model `Post` para o método `has`, o Laravel assumirá que o model `User` deve ter um método `posts` que define o relacionamento. Se necessário, você pode especificar explicitamente o nome do relacionamento que você gostaria de manipular:

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

Claro, você pode realizar manipulações de state nos models relacionados. Além disso, você pode passar uma transformação de state baseada em closure se a sua mudança de state exigir acesso ao model pai:

```php
$user = User::factory()
    ->has(
        Post::factory()
            ->count(3)
            ->state(function (array $attributes, User $user) {
                return ['user_type' => $user->type];
            })
    )
    ->create();
```

<a id="has-many-relationships-using-magic-methods"></a>
#### Usando Magic Methods

Por conveniência, você pode usar os magic methods de relacionamento de factory do Laravel para construir relacionamentos. Por exemplo, o exemplo a seguir usará convenção para determinar que os models relacionados devem ser criados através de um método de relacionamento `posts` no model `User`:

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

Ao usar magic methods para criar relacionamentos de factory, você pode passar um array de atributos para sobrescrever nos models relacionados:

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

Você também pode passar múltiplos arrays de atributos para criar models relacionados com state por model. O Laravel aplicará cada array em sequência:

```php
$user = User::factory()
    ->hasPosts(
        ['title' => 'First Post'],
        ['title' => 'Second Post'],
        ['title' => 'Third Post'],
    )
    ->create();
```

Você pode fornecer uma transformação de state baseada em closure se a sua mudança de state exigir acesso ao model pai:

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a id="belongs-to-relationships"></a>
### Relacionamentos Belongs To

Agora que exploramos como construir relacionamentos "has many" usando factories, vamos explorar o inverso do relacionamento. O método `for` pode ser usado para definir o model pai ao qual os models criados pela factory pertencem. Por exemplo, podemos criar três instâncias do model `App\Models\Post` que pertencem a um único usuário:

```php
use App\Models\Post;
use App\Models\User;

$posts = Post::factory()
    ->count(3)
    ->for(User::factory()->state([
        'name' => 'Jessica Archer',
    ]))
    ->create();
```

Se você já tem uma instância de model pai que deve ser associada aos models que você está criando, você pode passar a instância do model ao método `for`:

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a id="belongs-to-relationships-using-magic-methods"></a>
#### Usando Magic Methods

Por conveniência, você pode usar os magic methods de relacionamento de factory do Laravel para definir relacionamentos "belongs to". Por exemplo, o exemplo a seguir usará convenção para determinar que os três posts devem pertencer ao relacionamento `user` no model `Post`:

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a id="many-to-many-relationships"></a>
### Relacionamentos Many to Many

Assim como [relacionamentos has many](#has-many-relationships), relacionamentos "many to many" podem ser criados usando o método `has`:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a id="pivot-table-attributes"></a>
#### Atributos da Tabela Pivot

Se você precisar definir atributos que devem ser definidos na tabela pivot / intermediária que liga os models, você pode usar o método `hasAttached`. Esse método aceita um array de nomes e valores de atributos da tabela pivot como seu segundo argumento:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->hasAttached(
        Role::factory()->count(3),
        ['active' => true]
    )
    ->create();
```

Você pode fornecer uma transformação de state baseada em closure se a sua mudança de state exigir acesso ao model relacionado:

```php
$user = User::factory()
    ->hasAttached(
        Role::factory()
            ->count(3)
            ->state(function (array $attributes, User $user) {
                return ['name' => $user->name.' Role'];
            }),
        ['active' => true]
    )
    ->create();
```

Você também pode passar um array de arrays pivot para fornecer dados pivot únicos para cada model relacionado:

```php
$user = User::factory()
    ->hasAttached(
        Role::factory(),
        [
            ['active' => true],
            ['active' => false],
        ]
    )
    ->create();
```

Se você já tem instâncias de model que gostaria de anexar aos models que você está criando, você pode passar as instâncias de model ao método `hasAttached`. Neste exemplo, as mesmas três roles serão anexadas a todos os três usuários:

```php
$roles = Role::factory()->count(3)->create();

$users = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a id="many-to-many-relationships-using-magic-methods"></a>
#### Usando Magic Methods

Por conveniência, você pode usar os magic methods de relacionamento de factory do Laravel para definir relacionamentos many to many. Por exemplo, o exemplo a seguir usará convenção para determinar que os models relacionados devem ser criados através de um método de relacionamento `roles` no model `User`:

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a id="polymorphic-relationships"></a>
### Relacionamentos Polimórficos

[Relacionamentos polimórficos](../eloquent-relationships/#polymorphic-relationships) também podem ser criados usando factories. Relacionamentos polimórficos "morph many" são criados da mesma forma que relacionamentos "has many" típicos. Por exemplo, se um model `App\Models\Post` tem um relacionamento `morphMany` com um model `App\Models\Comment`:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a id="morph-to-relationships"></a>
#### Relacionamentos Morph To

Magic methods não podem ser usados para criar relacionamentos `morphTo`. Em vez disso, o método `for` deve ser usado diretamente e o nome do relacionamento deve ser fornecido explicitamente. Por exemplo, imagine que o model `Comment` tem um método `commentable` que define um relacionamento `morphTo`. Nesta situação, podemos criar três comentários que pertencem a um único post usando o método `for` diretamente:

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a id="polymorphic-many-to-many-relationships"></a>
#### Relacionamentos Polimórficos Many to Many

Relacionamentos polimórficos "many to many" (`morphToMany` / `morphedByMany`) podem ser criados exatamente como relacionamentos "many to many" não polimórficos:

```php
use App\Models\Tag;
use App\Models\Video;

$video = Video::factory()
    ->hasAttached(
        Tag::factory()->count(3),
        ['public' => true]
    )
    ->create();
```

Claro, o magic method `has` também pode ser usado para criar relacionamentos polimórficos "many to many":

```php
$video = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a id="defining-relationships-within-factories"></a>
### Definindo Relacionamentos Dentro de Factories

Para definir um relacionamento dentro da sua model factory, você normalmente atribuirá uma nova instância de factory à chave estrangeira do relacionamento. Isso normalmente é feito para os relacionamentos "inversos", como relacionamentos `belongsTo` e `morphTo`. Por exemplo, se você gostaria de criar um novo usuário ao criar um post, você pode fazer o seguinte:

```php
use App\Models\User;

/**
 * Define the model's default state.
 *
 * @return array<string, mixed>
 */
public function definition(): array
{
    return [
        'user_id' => User::factory(),
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

Se as colunas do relacionamento dependem da factory que o define, você pode atribuir uma closure a um atributo. A closure receberá o array de atributos avaliados da factory:

```php
/**
 * Define the model's default state.
 *
 * @return array<string, mixed>
 */
public function definition(): array
{
    return [
        'user_id' => User::factory(),
        'user_type' => function (array $attributes) {
            return User::find($attributes['user_id'])->type;
        },
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

<a id="recycling-an-existing-model-for-relationships"></a>
### Reciclando um Model Existente para Relacionamentos

Se você tem models que compartilham um relacionamento comum com outro model, você pode usar o método `recycle` para garantir que uma única instância do model relacionado seja reciclada para todos os relacionamentos criados pela factory.

Por exemplo, imagine que você tenha os models `Airline`, `Flight` e `Ticket`, onde o ticket pertence a uma airline e a um flight, e o flight também pertence a uma airline. Ao criar tickets, você provavelmente desejará a mesma airline tanto para o ticket quanto para o flight, então você pode passar uma instância de airline ao método `recycle`:

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

Você pode achar o método `recycle` particularmente útil se você tem models que pertencem a um usuário ou equipe em comum.

O método `recycle` também aceita uma coleção de models existentes. Quando uma coleção é fornecida ao método `recycle`, um model aleatório da coleção será escolhido quando a factory precisar de um model daquele tipo:

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```
