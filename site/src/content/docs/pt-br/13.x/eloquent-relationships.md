---
title: "Eloquent: Relacionamentos"
---

- [Introdução](#introduction)
- [Definindo Relacionamentos](#defining-relationships)
    - [Um para Um / Has One](#one-to-one)
    - [Um para Muitos / Has Many](#one-to-many)
    - [Um para Muitos (Inverso) / Belongs To](#one-to-many-inverse)
    - [Has One of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [Relacionamentos com Escopo](#scoped-relationships)
- [Relacionamentos Muitos para Muitos](#many-to-many)
    - [Recuperando Colunas da Tabela Intermediária](#retrieving-intermediate-table-columns)
    - [Filtrando Consultas via Colunas da Tabela Intermediária](#filtering-queries-via-intermediate-table-columns)
    - [Ordenando Consultas via Colunas da Tabela Intermediária](#ordering-queries-via-intermediate-table-columns)
    - [Definindo Modelos de Tabela Intermediária Personalizados](#defining-custom-intermediate-table-models)
        - [Hidratando Automaticamente Relacionamentos Pivot](#automatically-hydrating-pivot-relationships)
- [Relacionamentos Polimórficos](#polymorphic-relationships)
    - [Um para Um](#one-to-one-polymorphic-relations)
    - [Um para Muitos](#one-to-many-polymorphic-relations)
    - [Um de Muitos](#one-of-many-polymorphic-relations)
    - [Muitos para Muitos](#many-to-many-polymorphic-relations)
    - [Tipos Polimórficos Personalizados](#custom-polymorphic-types)
- [Relacionamentos Dinâmicos](#dynamic-relationships)
- [Consultando Relacionamentos](#querying-relations)
    - [Métodos de Relacionamento vs. Propriedades Dinâmicas](#relationship-methods-vs-dynamic-properties)
    - [Consultando Existência de Relacionamento](#querying-relationship-existence)
    - [Consultando Ausência de Relacionamento](#querying-relationship-absence)
    - [Consultando Relacionamentos Morph To](#querying-morph-to-relationships)
- [Agregando Modelos Relacionados](#aggregating-related-models)
    - [Contando Modelos Relacionados](#counting-related-models)
    - [Outras Funções de Agregação](#other-aggregate-functions)
    - [Contando Modelos Relacionados em Relacionamentos Morph To](#counting-related-models-on-morph-to-relationships)
- [Eager Loading](#eager-loading)
    - [Restringindo Eager Loads](#constraining-eager-loads)
    - [Lazy Eager Loading](#lazy-eager-loading)
    - [Eager Loading Automático](#automatic-eager-loading)
    - [Prevenindo Lazy Loading](#preventing-lazy-loading)
- [Inserindo e Atualizando Modelos Relacionados](#inserting-and-updating-related-models)
    - [O Método `save`](#the-save-method)
    - [O Método `create`](#the-create-method)
    - [Relacionamentos Belongs To](#updating-belongs-to-relationships)
    - [Relacionamentos Muitos para Muitos](#updating-many-to-many-relationships)
- [Atualizando Timestamps do Modelo Pai](#touching-parent-timestamps)

<a id="introduction"></a>
## Introdução

As tabelas do banco de dados frequentemente estão relacionadas umas com as outras. Por exemplo, uma postagem de blog pode ter muitos comentários ou um pedido pode estar relacionado ao usuário que o fez. O Eloquent torna fácil o gerenciamento e o trabalho com esses relacionamentos, e suporta uma variedade de relacionamentos comuns:

<div class="content-list" markdown="1">

- [Um para Um](#one-to-one)
- [Um para Muitos](#one-to-many)
- [Muitos para Muitos](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [Um para Um (Polimórfico)](#one-to-one-polymorphic-relations)
- [Um para Muitos (Polimórfico)](#one-to-many-polymorphic-relations)
- [Muitos para Muitos (Polimórfico)](#many-to-many-polymorphic-relations)

</div>

<a id="defining-relationships"></a>
## Definindo Relacionamentos

Os relacionamentos Eloquent são definidos como métodos nas suas classes de modelo. Uma vez que os relacionamentos também servem como poderosos [construtores de consulta](../queries/), definir relacionamentos como métodos fornece poderosas capacidades de encadeamento de métodos e consulta. Por exemplo, podemos encadear restrições de consulta adicionais neste relacionamento `posts`:

```php
$user->posts()->where('active', 1)->get();
```

Mas, antes de mergulhar muito fundo no uso de relacionamentos, vamos aprender como definir cada tipo de relacionamento suportado pelo Eloquent.

<a id="one-to-one"></a>
### Um para Um / Has One

Um relacionamento um para um é um tipo muito básico de relacionamento de banco de dados. Por exemplo, um modelo `User` pode estar associado a um modelo `Phone`. Para definir este relacionamento, vamos colocar um método `phone` no modelo `User`. O método `phone` deve chamar o método `hasOne` e retornar seu resultado. O método `hasOne` está disponível para o seu modelo através da classe base `Illuminate\Database\Eloquent\Model`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * Get the phone associated with the user.
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

O primeiro argumento passado para o método `hasOne` é o nome da classe do modelo relacionado. Uma vez que o relacionamento é definido, podemos recuperar o registro relacionado usando as propriedades dinâmicas do Eloquent. Propriedades dinâmicas permitem acessar métodos de relacionamento como se fossem propriedades definidas no modelo:

```php
$phone = User::find(1)->phone;
```

O Eloquent determina a chave estrangeira do relacionamento com base no nome do modelo pai. Neste caso, o modelo `Phone` é automaticamente assumido como tendo uma chave estrangeira `user_id`. Se você deseja sobrescrever esta convenção, pode passar um segundo argumento para o método `hasOne`:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

Além disso, o Eloquent assume que a chave estrangeira deve ter um valor correspondente à coluna da chave primária do pai. Em outras palavras, o Eloquent procurará o valor da coluna `id` do usuário na coluna `user_id` do registro `Phone`. Se você gostaria que o relacionamento usasse um valor de chave primária diferente de `id` ou a chave primária do seu modelo, pode passar um terceiro argumento para o método `hasOne`:

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a id="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### Definindo o Inverso do Relacionamento

Então, podemos acessar o modelo `Phone` a partir do nosso modelo `User`. Em seguida, vamos definir um relacionamento no modelo `Phone` que nos permita acessar o usuário que possui o telefone. Podemos definir o inverso de um relacionamento `hasOne` usando o método `belongsTo`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * Get the user that owns the phone.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

Ao invocar o método `user`, o Eloquent tentará encontrar um modelo `User` que tenha um `id` que corresponda à coluna `user_id` no modelo `Phone`.

O Eloquent determina o nome da chave estrangeira examinando o nome do método de relacionamento e adicionando o sufixo `_id`. Então, neste caso, o Eloquent assume que o modelo `Phone` tem uma coluna `user_id`. No entanto, se a chave estrangeira no modelo `Phone` não for `user_id`, você pode passar um nome de chave personalizado como o segundo argumento para o método `belongsTo`:

```php
/**
 * Get the user that owns the phone.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

Se o modelo pai não usar `id` como sua chave primária, ou se você deseja encontrar o modelo associado usando uma coluna diferente, pode passar um terceiro argumento para o método `belongsTo` especificando a chave personalizada da tabela pai:

```php
/**
 * Get the user that owns the phone.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a id="one-to-many"></a>
### Um para Muitos / Has Many

Um relacionamento um para muitos é usado para definir relacionamentos onde um único modelo é o pai de um ou mais modelos filhos. Por exemplo, uma postagem de blog pode ter um número infinito de comentários. Como todos os outros relacionamentos Eloquent, relacionamentos um para muitos são definidos definindo um método no seu modelo Eloquent:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * Get the comments for the blog post.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Lembre-se, o Eloquent determinará automaticamente a coluna de chave estrangeira apropriada para o modelo `Comment`. Por convenção, o Eloquent pegará o nome em "snake case" do modelo pai e adicionará o sufixo `_id`. Então, neste exemplo, o Eloquent assumirá que a coluna de chave estrangeira no modelo `Comment` é `post_id`.

Uma vez que o método de relacionamento foi definido, podemos acessar a [coleção](../eloquent-collections/) de comentários relacionados acessando a propriedade `comments`. Lembre-se, como o Eloquent fornece "propriedades dinâmicas de relacionamento", podemos acessar métodos de relacionamento como se fossem definidos como propriedades no modelo:

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

Como todos os relacionamentos também servem como construtores de consulta, você pode adicionar mais restrições à consulta de relacionamento chamando o método `comments` e continuando a encadear condições na consulta:

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

Assim como o método `hasOne`, você também pode sobrescrever as chaves estrangeira e local passando argumentos adicionais para o método `hasMany`:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a id="automatically-hydrating-parent-models-on-children"></a>
#### Hidratando Automaticamente Modelos Pais nos Filhos

Mesmo ao utilizar eager loading do Eloquent, problemas de consulta "N + 1" podem surgir se você tentar acessar o modelo pai a partir de um modelo filho enquanto itera pelos modelos filhos:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

No exemplo acima, um problema de consulta "N + 1" foi introduzido porque, embora os comentários tenham sido carregados antecipadamente para cada modelo `Post`, o Eloquent não hidrata automaticamente o `Post` pai em cada modelo `Comment` filho.

Se você gostaria que o Eloquent hidratasse automaticamente os modelos pais em seus filhos, pode invocar o método `chaperone` ao definir um relacionamento `hasMany`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * Get the comments for the blog post.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

Ou, se você gostaria de optar pela hidratação automática de pais em tempo de execução, pode invocar o modelo `chaperone` ao carregar o relacionamento antecipadamente:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a id="one-to-many-inverse"></a>
### Um para Muitos (Inverso) / Belongs To

Agora que podemos acessar todos os comentários de uma postagem, vamos definir um relacionamento para permitir que um comentário acesse sua postagem pai. Para definir o inverso de um relacionamento `hasMany`, defina um método de relacionamento no modelo filho que chama o método `belongsTo`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * Get the post that owns the comment.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

Uma vez que o relacionamento foi definido, podemos recuperar a postagem pai de um comentário acessando a "propriedade dinâmica de relacionamento" `post`:

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

No exemplo acima, o Eloquent tentará encontrar um modelo `Post` que tenha um `id` que corresponda à coluna `post_id` no modelo `Comment`.

O Eloquent determina o nome padrão da chave estrangeira examinando o nome do método de relacionamento e adicionando o sufixo `_` seguido do nome da coluna da chave primária do modelo pai. Então, neste exemplo, o Eloquent assumirá que a chave estrangeira do modelo `Post` na tabela `comments` é `post_id`.

No entanto, se a chave estrangeira para o seu relacionamento não seguir estas convenções, você pode passar um nome de chave estrangeira personalizado como o segundo argumento para o método `belongsTo`:

```php
/**
 * Get the post that owns the comment.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

Se o seu modelo pai não usar `id` como sua chave primária, ou se você deseja encontrar o modelo associado usando uma coluna diferente, pode passar um terceiro argumento para o método `belongsTo` especificando a chave personalizada da sua tabela pai:

```php
/**
 * Get the post that owns the comment.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a id="default-models"></a>
#### Modelos Padrão

Os relacionamentos `belongsTo`, `hasOne`, `hasOneThrough` e `morphOne` permitem que você defina um modelo padrão que será retornado se o relacionamento dado for `null`. Este padrão é frequentemente chamado de [padrão Null Object](https://en.wikipedia.org/wiki/Null_Object_pattern) e pode ajudar a remover verificações condicionais no seu código. No exemplo a seguir, a relação `user` retornará um modelo vazio `App\Models\User` se nenhum usuário estiver anexado ao modelo `Post`:

```php
/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

Para preencher o modelo padrão com atributos, você pode passar um array ou closure para o método `withDefault`:

```php
/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a id="querying-belongs-to-relationships"></a>
#### Consultando Relacionamentos Belongs To

Ao consultar os filhos de um relacionamento "belongs to", você pode construir manualmente a cláusula `where` para recuperar os modelos Eloquent correspondentes:

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

No entanto, você pode achar mais conveniente usar o método `whereBelongsTo`, que determinará automaticamente o relacionamento e a chave estrangeira apropriados para o modelo dado:

```php
$posts = Post::whereBelongsTo($user)->get();
```

Você também pode fornecer uma instância de [coleção](../eloquent-collections/) para o método `whereBelongsTo`. Ao fazer isso, o Laravel recuperará modelos que pertencem a qualquer um dos modelos pais dentro da coleção:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

Por padrão, o Laravel determinará o relacionamento associado ao modelo dado com base no nome da classe do modelo; no entanto, você pode especificar o nome do relacionamento manualmente fornecendo-o como o segundo argumento para o método `whereBelongsTo`:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a id="has-one-of-many"></a>
### Has One of Many

Às vezes um modelo pode ter muitos modelos relacionados, mas você deseja recuperar facilmente o modelo relacionado "mais recente" ou "mais antigo" do relacionamento. Por exemplo, um modelo `User` pode estar relacionado a muitos modelos `Order`, mas você deseja definir uma maneira conveniente de interagir com o pedido mais recente que o usuário fez. Você pode fazer isso usando o tipo de relacionamento `hasOne` combinado com os métodos `ofMany`:

```php
/**
 * Get the user's most recent order.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

Da mesma forma, você pode definir um método para recuperar o modelo relacionado "mais antigo", ou primeiro, de um relacionamento:

```php
/**
 * Get the user's oldest order.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

Por padrão, os métodos `latestOfMany` e `oldestOfMany` recuperarão o modelo relacionado mais recente ou mais antigo com base na chave primária do modelo, que deve ser ordenável. No entanto, às vezes você pode desejar recuperar um único modelo de um relacionamento maior usando um critério de ordenação diferente.

Por exemplo, usando o método `ofMany`, você pode recuperar o pedido mais caro do usuário. O método `ofMany` aceita a coluna ordenável como seu primeiro argumento e qual função de agregação (`min` ou `max`) aplicar ao consultar o modelo relacionado:

```php
/**
 * Get the user's largest order.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> **Aviso:**
> Porque o PostgreSQL não suporta a execução da função `MAX` contra colunas UUID, não é atualmente possível usar relacionamentos one-of-many em combinação com colunas UUID do PostgreSQL.

<a id="converting-many-relationships-to-has-one-relationships"></a>
#### Convertendo Relacionamentos "Many" em Relacionamentos Has One

Frequentemente, ao recuperar um único modelo usando os métodos `latestOfMany`, `oldestOfMany` ou `ofMany`, você já tem um relacionamento "has many" definido para o mesmo modelo. Por conveniência, o Laravel permite que você converta facilmente este relacionamento em um relacionamento "has one" invocando o método `one` no relacionamento:

```php
/**
 * Get the user's orders.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * Get the user's largest order.
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

Você também pode usar o método `one` para converter relacionamentos `HasManyThrough` em relacionamentos `HasOneThrough`:

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a id="advanced-has-one-of-many-relationships"></a>
#### Relacionamentos Has One of Many Avançados

É possível construir relacionamentos "has one of many" mais avançados. Por exemplo, um modelo `Product` pode ter muitos modelos `Price` associados que são retidos no sistema mesmo após novos preços serem publicados. Além disso, novos dados de preço para o produto podem ser publicados antecipadamente para entrar em vigor em uma data futura através de uma coluna `published_at`.

Então, em resumo, precisamos recuperar o preço publicado mais recente onde a data de publicação não é no futuro. Além disso, se dois preços tiverem a mesma data de publicação, preferiremos o preço com o maior ID. Para fazer isso, devemos passar um array para o método `ofMany` que contém as colunas ordenáveis que determinam o preço mais recente. Além disso, um closure será fornecido como o segundo argumento para o método `ofMany`. Este closure será responsável por adicionar restrições adicionais de data de publicação à consulta de relacionamento:

```php
/**
 * Get the current pricing for the product.
 */
public function currentPricing(): HasOne
{
    return $this->hasOne(Price::class)->ofMany([
        'published_at' => 'max',
        'id' => 'max',
    ], function (Builder $query) {
        $query->where('published_at', '<', now());
    });
}
```

<a id="has-one-through"></a>
### Has One Through

O relacionamento "has-one-through" define um relacionamento um para um com outro modelo. No entanto, este relacionamento indica que o modelo declarante pode ser combinado com uma instância de outro modelo prosseguindo _através_ de um terceiro modelo.

Por exemplo, em uma aplicação de oficina mecânica, cada modelo `Mechanic` pode estar associado a um modelo `Car`, e cada modelo `Car` pode estar associado a um modelo `Owner`. Embora o mecânico e o proprietário não tenham um relacionamento direto no banco de dados, o mecânico pode acessar o proprietário _através_ do modelo `Car`. Vamos olhar as tabelas necessárias para definir este relacionamento:

```text
mechanics
    id - integer
    name - string

cars
    id - integer
    model - string
    mechanic_id - integer

owners
    id - integer
    name - string
    car_id - integer
```

Agora que examinamos a estrutura da tabela para o relacionamento, vamos definir o relacionamento no modelo `Mechanic`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

O primeiro argumento passado para o método `hasOneThrough` é o nome do modelo final que desejamos acessar, enquanto o segundo argumento é o nome do modelo intermediário.

Ou, se os relacionamentos relevantes já foram definidos em todos os modelos envolvidos no relacionamento, você pode definir fluentemente um relacionamento "has-one-through" invocando o método `through` e fornecendo os nomes desses relacionamentos. Por exemplo, se o modelo `Mechanic` tem um relacionamento `cars` e o modelo `Car` tem um relacionamento `owner`, você pode definir um relacionamento "has-one-through" conectando o mecânico e o proprietário assim:

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```

<a id="has-one-through-key-conventions"></a>
#### Convenções de Chave

As convenções típicas de chave estrangeira do Eloquent serão usadas ao executar as consultas do relacionamento. Se você deseja personalizar as chaves do relacionamento, pode passá-las como o terceiro e quarto argumentos para o método `hasOneThrough`. O terceiro argumento é o nome da chave estrangeira no modelo intermediário. O quarto argumento é o nome da chave estrangeira no modelo final. O quinto argumento é a chave local, enquanto o sexto argumento é a chave local do modelo intermediário:

```php
class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // Foreign key on the cars table...
            'car_id', // Foreign key on the owners table...
            'id', // Local key on the mechanics table...
            'id' // Local key on the cars table...
        );
    }
}
```

Ou, como discutido anteriormente, se os relacionamentos relevantes já foram definidos em todos os modelos envolvidos no relacionamento, você pode definir fluentemente um relacionamento "has-one-through" invocando o método `through` e fornecendo os nomes desses relacionamentos. Esta abordagem oferece a vantagem de reutilizar as convenções de chave já definidas nos relacionamentos existentes:

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```

<a id="has-many-through"></a>
### Has Many Through

O relacionamento "has-many-through" fornece uma maneira conveniente de acessar relações distantes através de uma relação intermediária. Por exemplo, vamos supor que estamos construindo uma plataforma de implantação como o [Laravel Cloud](https://cloud.laravel.com). Um modelo `Application` pode acessar muitos modelos `Deployment` através de um modelo intermediário `Environment`. Usando este exemplo, você pode facilmente reunir todas as implantações para uma determinada aplicação. Vamos olhar as tabelas necessárias para definir este relacionamento:

```text
applications
    id - integer
    name - string

environments
    id - integer
    application_id - integer
    name - string

deployments
    id - integer
    environment_id - integer
    commit_hash - string
```

Agora que examinamos a estrutura da tabela para o relacionamento, vamos definir o relacionamento no modelo `Application`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Application extends Model
{
    /**
     * Get all of the deployments for the application.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

O primeiro argumento passado para o método `hasManyThrough` é o nome do modelo final que desejamos acessar, enquanto o segundo argumento é o nome do modelo intermediário.

Ou, se os relacionamentos relevantes já foram definidos em todos os modelos envolvidos no relacionamento, você pode definir fluentemente um relacionamento "has-many-through" invocando o método `through` e fornecendo os nomes desses relacionamentos. Por exemplo, se o modelo `Application` tem um relacionamento `environments` e o modelo `Environment` tem um relacionamento `deployments`, você pode definir um relacionamento "has-many-through" conectando a aplicação e as implantações assim:

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

Embora a tabela do modelo `Deployment` não contenha uma coluna `application_id`, a relação `hasManyThrough` fornece acesso às implantações de uma aplicação via `$application->deployments`. Para recuperar esses modelos, o Eloquent inspeciona a coluna `application_id` na tabela do modelo intermediário `Environment`. Após encontrar os IDs de ambiente relevantes, eles são usados para consultar a tabela do modelo `Deployment`.

<a id="has-many-through-key-conventions"></a>
#### Convenções de Chave

As convenções típicas de chave estrangeira do Eloquent serão usadas ao executar as consultas do relacionamento. Se você deseja personalizar as chaves do relacionamento, pode passá-las como o terceiro e quarto argumentos para o método `hasManyThrough`. O terceiro argumento é o nome da chave estrangeira no modelo intermediário. O quarto argumento é o nome da chave estrangeira no modelo final. O quinto argumento é a chave local, enquanto o sexto argumento é a chave local do modelo intermediário:

```php
class Application extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'application_id', // Foreign key on the environments table...
            'environment_id', // Foreign key on the deployments table...
            'id', // Local key on the applications table...
            'id' // Local key on the environments table...
        );
    }
}
```

Ou, como discutido anteriormente, se os relacionamentos relevantes já foram definidos em todos os modelos envolvidos no relacionamento, você pode definir fluentemente um relacionamento "has-many-through" invocando o método `through` e fornecendo os nomes desses relacionamentos. Esta abordagem oferece a vantagem de reutilizar as convenções de chave já definidas nos relacionamentos existentes:

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

<a id="scoped-relationships"></a>
### Relacionamentos com Escopo

É comum adicionar métodos adicionais aos modelos que restringem relacionamentos. Por exemplo, você pode adicionar um método `featuredPosts` a um modelo `User` que restringe o relacionamento mais amplo `posts` com uma restrição `where` adicional:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * Get the user's posts.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * Get the user's featured posts.
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

No entanto, se você tentar criar um modelo através do método `featuredPosts`, seu atributo `featured` não seria definido como `true`. Se você gostaria de criar modelos através de métodos de relacionamento e também especificar atributos que devem ser adicionados a todos os modelos criados através desse relacionamento, pode usar o método `withAttributes` ao construir a consulta de relacionamento:

```php
/**
 * Get the user's featured posts.
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

O método `withAttributes` adicionará condições `where` à consulta usando os atributos fornecidos, e também adicionará os atributos fornecidos a quaisquer modelos criados através do método de relacionamento:

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

Para instruir o método `withAttributes` a não adicionar condições `where` à consulta, você pode definir o argumento `asConditions` como `false`:

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

<a id="many-to-many"></a>
## Relacionamentos Muitos para Muitos

Relacionamentos muitos para muitos são ligeiramente mais complicados que os relacionamentos `hasOne` e `hasMany`. Um exemplo de relacionamento muitos para muitos é um usuário que tem muitas funções e essas funções também são compartilhadas por outros usuários na aplicação. Por exemplo, um usuário pode ser atribuído à função de "Autor" e "Editor"; no entanto, essas funções também podem ser atribuídas a outros usuários. Então, um usuário tem muitas funções e uma função tem muitos usuários.

<a id="many-to-many-table-structure"></a>
#### Estrutura da Tabela

Para definir este relacionamento, três tabelas de banco de dados são necessárias: `users`, `roles` e `role_user`. A tabela `role_user` é derivada da ordem alfabética dos nomes dos modelos relacionados e contém as colunas `user_id` e `role_id`. Esta tabela é usada como uma tabela intermediária vinculando os usuários e as funções.

Lembre-se, como uma função pode pertencer a muitos usuários, não podemos simplesmente colocar uma coluna `user_id` na tabela `roles`. Isso significaria que uma função poderia pertencer a um único usuário. Para fornecer suporte para funções atribuídas a múltiplos usuários, a tabela `role_user` é necessária. Podemos resumir a estrutura da tabela do relacionamento assim:

```text
users
    id - integer
    name - string

roles
    id - integer
    name - string

role_user
    user_id - integer
    role_id - integer
```

<a id="many-to-many-model-structure"></a>
#### Estrutura do Modelo

Relacionamentos muitos para muitos são definidos escrevendo um método que retorna o resultado do método `belongsToMany`. O método `belongsToMany` é fornecido pela classe base `Illuminate\Database\Eloquent\Model` que é usada por todos os modelos Eloquent da sua aplicação. Por exemplo, vamos definir um método `roles` no nosso modelo `User`. O primeiro argumento passado para este método é o nome da classe do modelo relacionado:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class User extends Model
{
    /**
     * The roles that belong to the user.
     */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }
}
```

Uma vez que o relacionamento é definido, você pode acessar as funções do usuário usando a propriedade dinâmica de relacionamento `roles`:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```

Como todos os relacionamentos também servem como construtores de consulta, você pode adicionar mais restrições à consulta de relacionamento chamando o método `roles` e continuando a encadear condições na consulta:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

Para determinar o nome da tabela intermediária do relacionamento, o Eloquent juntará os dois nomes de modelos relacionados em ordem alfabética. No entanto, você é livre para sobrescrever esta convenção. Você pode fazê-lo passando um segundo argumento para o método `belongsToMany`:

```php
return $this->belongsToMany(Role::class, 'role_user');
```

Além de personalizar o nome da tabela intermediária, você também pode personalizar os nomes das colunas das chaves na tabela passando argumentos adicionais para o método `belongsToMany`. O terceiro argumento é o nome da chave estrangeira do modelo no qual você está definindo o relacionamento, enquanto o quarto argumento é o nome da chave estrangeira do modelo que você está fazendo join:

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a id="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### Definindo o Inverso do Relacionamento

Para definir o "inverso" de um relacionamento muitos para muitos, você deve definir um método no modelo relacionado que também retorne o resultado do método `belongsToMany`. Para completar nosso exemplo de usuário / função, vamos definir o método `users` no modelo `Role`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * The users that belong to the role.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class);
    }
}
```

Como você pode ver, o relacionamento é definido exatamente da mesma forma que seu modelo `User` counterpart, com a exceção de referenciar o modelo `App\Models\User`. Como estamos reutilizando o método `belongsToMany`, todas as opções habituais de personalização de tabela e chave estão disponíveis ao definir o "inverso" de relacionamentos muitos para muitos.

<a id="retrieving-intermediate-table-columns"></a>
### Recuperando Colunas da Tabela Intermediária

Como você já aprendeu, trabalhar com relações muitos para muitos requer a presença de uma tabela intermediária. o Eloquent fornece algumas maneiras muito úteis de interagir com esta tabela. Por exemplo, vamos supor que nosso modelo `User` tenha muitos modelos `Role` aos quais está relacionado. Após acessar este relacionamento, podemos acessar a tabela intermediária usando o atributo `pivot` nos modelos:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

Observe que cada modelo `Role` que recuperamos é automaticamente atribuído um atributo `pivot`. Este atributo contém um modelo representando a tabela intermediária.

Por padrão, apenas as chaves do modelo estarão presentes no modelo `pivot`. Se sua tabela intermediária contém atributos extras, você deve especificá-los ao definir o relacionamento:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

Se você gostaria que sua tabela intermediária tivesse timestamps `created_at` e `updated_at` automaticamente mantidos pelo Eloquent, chame o método `withTimestamps` ao definir o relacionamento:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> **Aviso:**
> Tabelas intermediárias que utilizam timestamps mantidos automaticamente pelo Eloquent são obrigadas a ter ambas as colunas de timestamp `created_at` e `updated_at`.

<a id="customizing-the-pivot-attribute-name"></a>
#### Personalizando o Nome do Atributo `pivot`

Como observado anteriormente, atributos da tabela intermediária podem ser acessados nos modelos através do atributo `pivot`. No entanto, você é livre para personalizar o nome deste atributo para refletir melhor seu propósito dentro da sua aplicação.

Por exemplo, se sua aplicação contém usuários que podem se inscrever em podcasts, você provavelmente tem um relacionamento muitos para muitos entre usuários e podcasts. Se este for o caso, você pode desejar renomear seu atributo de tabela intermediária para `subscription` em vez de `pivot`. Isso pode ser feito usando o método `as` ao definir o relacionamento:

```php
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();
```

Uma vez que o atributo personalizado de tabela intermediária foi especificado, você pode acessar os dados da tabela intermediária usando o nome personalizado:

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a id="filtering-queries-via-intermediate-table-columns"></a>
### Filtrando Consultas via Colunas da Tabela Intermediária

Você também pode filtrar os resultados retornados por consultas de relacionamento `belongsToMany` usando os métodos `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull` e `wherePivotNotNull` ao definir o relacionamento:

```php
return $this->belongsToMany(Role::class)
    ->wherePivot('approved', 1);

return $this->belongsToMany(Role::class)
    ->wherePivotIn('priority', [1, 2]);

return $this->belongsToMany(Role::class)
    ->wherePivotNotIn('priority', [1, 2]);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNull('expired_at');

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNotNull('expired_at');
```

O `wherePivot` adiciona uma restrição de cláusula where à consulta, mas não adiciona o valor especificado ao criar novos modelos através do relacionamento definido. Se você precisa tanto consultar quanto criar relacionamentos com um valor pivot particular, pode usar o método `withPivotValue`:

```php
return $this->belongsToMany(Role::class)
    ->withPivotValue('approved', 1);
```

<a id="ordering-queries-via-intermediate-table-columns"></a>
### Ordenando Consultas via Colunas da Tabela Intermediária

Você pode ordenar os resultados retornados por consultas de relacionamento `belongsToMany` usando os métodos `orderByPivot` e `orderByPivotDesc`. No exemplo a seguir, recuperaremos todas as insígnias mais recentes para o usuário:

```php
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivotDesc('created_at');
```

<a id="defining-custom-intermediate-table-models"></a>
### Definindo Modelos de Tabela Intermediária Personalizados

Se você gostaria de definir um modelo personalizado para representar a tabela intermediária do seu relacionamento muitos para muitos, pode chamar o método `using` ao definir o relacionamento. Modelos pivot personalizados dão a oportunidade de definir comportamento adicional no modelo pivot, como métodos e casts.

Modelos pivot personalizados muitos para muitos devem estender a classe `Illuminate\Database\Eloquent\Relations\Pivot`, enquanto modelos pivot personalizados polimórficos muitos para muitos devem estender a classe `Illuminate\Database\Eloquent\Relations\MorphPivot`. Por exemplo, podemos definir um modelo `Role` que usa um modelo pivot personalizado `RoleUser`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * The users that belong to the role.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

Ao definir o modelo `RoleUser`, você deve estender a classe `Illuminate\Database\Eloquent\Relations\Pivot`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\Pivot;

class RoleUser extends Pivot
{
    // ...
}
```

> **Aviso:**
> Modelos pivot não podem usar o trait `SoftDeletes`. Se você precisa fazer soft delete de registros pivot, considere converter seu modelo pivot em um modelo Eloquent real.

<a id="custom-pivot-models-and-incrementing-ids"></a>
#### Modelos Pivot Personalizados e IDs Incrementais

Se você definiu um relacionamento muitos para muitos que usa um modelo pivot personalizado, e esse modelo pivot tem uma chave primária auto-incrementável, você deve garantir que sua classe de modelo pivot personalizado use o atributo `Table` com `incrementing` definido como `true`:

```php
use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Relations\Pivot;

#[Table(incrementing: true)]
class RoleUser extends Pivot
{
    // ...
}
```

<a id="automatically-hydrating-pivot-relationships"></a>
#### Hidratando Automaticamente Relacionamentos Pivot

Quando um modelo pivot personalizado define relacionamentos `belongsTo` para os modelos declarante e relacionado, você pode invocar `chaperone` para hidratar automaticamente esses relacionamentos em cada modelo pivot. Isso evita consultas adicionais ao acessar os modelos através do pivot:

```php
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\Pivot;

class RoleUser extends Pivot
{
    public function role(): BelongsTo
    {
        return $this->belongsTo(Role::class);
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}

class Role extends Model
{
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)
            ->using(RoleUser::class)
            ->chaperone();
    }
}
```

O Eloquent tentará inferir os nomes dos relacionamentos pivot. Se seu modelo pivot usa nomes não padrão, passe os nomes dos relacionamentos declarante e relacionado para `chaperone`:

```php
return $this->belongsToMany(User::class)
    ->using(RoleUser::class)
    ->chaperone(declaring: 'role', related: 'user');
```

<a id="polymorphic-relationships"></a>
## Relacionamentos Polimórficos

Um relacionamento polimórfico permite que o modelo filho pertença a mais de um tipo de modelo usando uma única associação. Por exemplo, imagine que você está construindo uma aplicação que permite aos usuários compartilhar postagens de blog e vídeos. Em tal aplicação, um modelo `Comment` pode pertencer tanto ao modelo `Post` quanto ao modelo `Video`.

<a id="one-to-one-polymorphic-relations"></a>
### Um para Um (Polimórfico)

<a id="one-to-one-polymorphic-table-structure"></a>
#### Estrutura da Tabela

Uma relação polimórfica um para um é semelhante a uma relação típica um para um; no entanto, o modelo filho pode pertencer a mais de um tipo de modelo usando uma única associação. Por exemplo, uma postagem de `Post` e um `User` podem compartilhar uma relação polimórfica com um modelo `Image`. Usar uma relação polimórfica um para um permite que você tenha uma única tabela de imagens únicas que podem ser associadas a postagens e usuários. Primeiro, vamos examinar a estrutura da tabela:

```text
posts
    id - integer
    name - string

users
    id - integer
    name - string

images
    id - integer
    url - string
    imageable_type - string
    imageable_id - integer
```

Observe as colunas `imageable_id` e `imageable_type` na tabela `images`. A coluna `imageable_id` conterá o valor de ID da postagem ou usuário, enquanto a coluna `imageable_type` conterá o nome da classe do modelo pai. A coluna `imageable_type` é usada pelo Eloquent para determinar qual "tipo" de modelo pai retornar ao acessar a relação `imageable`. Neste caso, a coluna conteria `App\Models\Post` ou `App\Models\User`.

<a id="one-to-one-polymorphic-model-structure"></a>
#### Estrutura do Modelo

Em seguida, vamos examinar as definições de modelo necessárias para construir este relacionamento:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Image extends Model
{
    /**
     * Get the parent imageable model (user or post).
     */
    public function imageable(): MorphTo
    {
        return $this->morphTo();
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphOne;

class Post extends Model
{
    /**
     * Get the post's image.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphOne;

class User extends Model
{
    /**
     * Get the user's image.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a id="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### Recuperando o Relacionamento

Uma vez que sua tabela de banco de dados e modelos estão definidos, você pode acessar os relacionamentos através dos seus modelos. Por exemplo, para recuperar a imagem de uma postagem, podemos acessar a propriedade dinâmica de relacionamento `image`:

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

Você pode recuperar o pai do modelo polimórfico acessando o nome do método que realiza a chamada para `morphTo`. Neste caso, é o método `imageable` no modelo `Image`. Então, vamos acessar esse método como uma propriedade dinâmica de relacionamento:

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

A relação `imageable` no modelo `Image` retornará uma instância `Post` ou `User`, dependendo de qual tipo de modelo possui a imagem.

<a id="morph-one-to-one-key-conventions"></a>
#### Convenções de Chave

Se necessário, você pode especificar o nome das colunas "id" e "type" utilizadas pelo seu modelo filho polimórfico. Se você fizer isso, garanta que sempre passe o nome do relacionamento como o primeiro argumento para o método `morphTo`. Tipicamente, este valor deve corresponder ao nome do método, então você pode usar a constante `__FUNCTION__` do PHP:

```php
/**
 * Get the model that the image belongs to.
 */
public function imageable(): MorphTo
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a id="one-to-many-polymorphic-relations"></a>
### Um para Muitos (Polimórfico)

<a id="one-to-many-polymorphic-table-structure"></a>
#### Estrutura da Tabela

Uma relação polimórfica um para muitos é semelhante a uma relação típica um para muitos; no entanto, o modelo filho pode pertencer a mais de um tipo de modelo usando uma única associação. Por exemplo, imagine que os usuários da sua aplicação podem "comentar" em postagens e vídeos. Usando relacionamentos polimórficos, você pode usar uma única tabela `comments` para conter comentários para ambas postagens e vídeos. Primeiro, vamos examinar a estrutura da tabela necessária para construir este relacionamento:

```text
posts
    id - integer
    title - string
    body - text

videos
    id - integer
    title - string
    url - string

comments
    id - integer
    body - text
    commentable_type - string
    commentable_id - integer
```

<a id="one-to-many-polymorphic-model-structure"></a>
#### Estrutura do Modelo

Em seguida, vamos examinar as definições de modelo necessárias para construir este relacionamento:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Comment extends Model
{
    /**
     * Get the parent commentable model (post or video).
     */
    public function commentable(): MorphTo
    {
        return $this->morphTo();
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphMany;

class Post extends Model
{
    /**
     * Get all of the post's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphMany;

class Video extends Model
{
    /**
     * Get all of the video's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a id="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### Recuperando o Relacionamento

Uma vez que sua tabela de banco de dados e modelos estão definidos, você pode acessar os relacionamentos através das propriedades dinâmicas de relacionamento do seu modelo. Por exemplo, para acessar todos os comentários de uma postagem, podemos usar a propriedade dinâmica `comments`:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```

Você também pode recuperar o pai de um modelo filho polimórfico acessando o nome do método que realiza a chamada para `morphTo`. Neste caso, é o método `commentable` no modelo `Comment`. Então, vamos acessar esse método como uma propriedade dinâmica de relacionamento para acessar o modelo pai do comentário:

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

A relação `commentable` no modelo `Comment` retornará uma instância `Post` ou `Video`, dependendo de qual tipo de modelo é o pai do comentário.

<a id="polymorphic-automatically-hydrating-parent-models-on-children"></a>
#### Hidratando Automaticamente Modelos Pais nos Filhos

Mesmo ao utilizar eager loading do Eloquent, problemas de consulta "N + 1" podem surgir se você tentar acessar o modelo pai a partir de um modelo filho enquanto itera pelos modelos filhos:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->commentable->title;
    }
}
```

No exemplo acima, um problema de consulta "N + 1" foi introduzido porque, embora os comentários tenham sido carregados antecipadamente para cada modelo `Post`, o Eloquent não hidrata automaticamente o `Post` pai em cada modelo `Comment` filho.

Se você gostaria que o Eloquent hidratasse automaticamente os modelos pais em seus filhos, pode invocar o método `chaperone` ao definir um relacionamento `morphMany`:

```php
class Post extends Model
{
    /**
     * Get all of the post's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable')->chaperone();
    }
}
```

Ou, se você gostaria de optar pela hidratação automática de pais em tempo de execução, pode invocar o modelo `chaperone` ao carregar o relacionamento antecipadamente:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a id="one-of-many-polymorphic-relations"></a>
### Um de Muitos (Polimórfico)

Às vezes um modelo pode ter muitos modelos relacionados, mas você deseja recuperar facilmente o modelo relacionado "mais recente" ou "mais antigo" do relacionamento. Por exemplo, um modelo `User` pode estar relacionado a muitos modelos `Image`, mas você deseja definir uma maneira conveniente de interagir com a imagem mais recente que o usuário carregou. Você pode fazer isso usando o tipo de relacionamento `morphOne` combinado com os métodos `ofMany`:

```php
/**
 * Get the user's most recent image.
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

Da mesma forma, você pode definir um método para recuperar o modelo relacionado "mais antigo", ou primeiro, de um relacionamento:

```php
/**
 * Get the user's oldest image.
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

Por padrão, os métodos `latestOfMany` e `oldestOfMany` recuperarão o modelo relacionado mais recente ou mais antigo com base na chave primária do modelo, que deve ser ordenável. No entanto, às vezes você pode desejar recuperar um único modelo de um relacionamento maior usando um critério de ordenação diferente.

Por exemplo, usando o método `ofMany`, você pode recuperar a imagem mais "curtida" do usuário. O método `ofMany` aceita a coluna ordenável como seu primeiro argumento e qual função de agregação (`min` ou `max`) aplicar ao consultar o modelo relacionado:

```php
/**
 * Get the user's most popular image.
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> **Nota:**
> É possível construir relacionamentos "one of many" mais avançados. Para mais informações, consulte a [documentação de has one of many](#advanced-has-one-of-many-relationships).

<a id="many-to-many-polymorphic-relations"></a>
### Muitos para Muitos (Polimórfico)

<a id="many-to-many-polymorphic-table-structure"></a>
#### Estrutura da Tabela

Relacionamentos polimórficos muitos para muitos são ligeiramente mais complicados que os relacionamentos "morph one" e "morph many". Por exemplo, um modelo `Post` e um modelo `Video` podem compartilhar uma relação polimórfica com um modelo `Tag`. Usar um relacionamento polimórfico muitos para muitos nesta situação permitiria que sua aplicação tivesse uma única tabela de tags únicas que podem ser associadas a postagens ou vídeos. Primeiro, vamos examinar a estrutura da tabela necessária para construir este relacionamento:

```text
posts
    id - integer
    name - string

videos
    id - integer
    name - string

tags
    id - integer
    name - string

taggables
    tag_id - integer
    taggable_type - string
    taggable_id - integer
```

> **Nota:**
> Antes de mergulhar em relacionamentos polimórficos muitos para muitos, você pode se beneficiar da leitura da documentação sobre [relacionamentos muitos para muitos](#many-to-many) típicos.

<a id="many-to-many-polymorphic-model-structure"></a>
#### Estrutura do Modelo

Em seguida, estamos prontos para definir os relacionamentos nos modelos. Os modelos `Post` e `Video` conterão ambos um método `tags` que chama o método `morphToMany` fornecido pela classe base do modelo Eloquent.

O método `morphToMany` aceita o nome do modelo relacionado, bem como o "nome do relacionamento". Com base no nome que atribuímos ao nome da nossa tabela intermediária e as chaves que ela contém, nos referiremos ao relacionamento como "taggable":

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Post extends Model
{
    /**
     * Get all of the tags for the post.
     */
    public function tags(): MorphToMany
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a id="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### Definindo o Inverso do Relacionamento

Em seguida, no modelo `Tag`, você deve definir um método para cada um dos seus possíveis modelos pai. Então, neste exemplo, definiremos um método `posts` e um método `videos`. Ambos os métodos devem retornar o resultado do método `morphedByMany`.

O método `morphedByMany` aceita o nome do modelo relacionado, bem como o "nome do relacionamento". Com base no nome que atribuímos ao nome da nossa tabela intermediária e as chaves que ela contém, nos referiremos ao relacionamento como "taggable":

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Tag extends Model
{
    /**
     * Get all of the posts that are assigned this tag.
     */
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * Get all of the videos that are assigned this tag.
     */
    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a id="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### Recuperando o Relacionamento

Uma vez que sua tabela de banco de dados e modelos estão definidos, você pode acessar os relacionamentos através dos seus modelos. Por exemplo, para acessar todas as tags de uma postagem, você pode usar a propriedade dinâmica de relacionamento `tags`:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```

Você pode recuperar o pai de uma relação polimórfica a partir do modelo filho polimórfico acessando o nome do método que realiza a chamada para `morphedByMany`. Neste caso, são os métodos `posts` ou `videos` no modelo `Tag`:

```php
use App\Models\Tag;

$tag = Tag::find(1);

foreach ($tag->posts as $post) {
    // ...
}

foreach ($tag->videos as $video) {
    // ...
}
```

<a id="custom-polymorphic-types"></a>
### Tipos Polimórficos Personalizados

Por padrão, o Laravel usará o nome completo da classe qualificada para armazenar o "tipo" do modelo relacionado. Por exemplo, dado o exemplo de relacionamento um para muitos acima onde um modelo `Comment` pode pertencer a um modelo `Post` ou `Video`, o `commentable_type` padrão seria `App\Models\Post` ou `App\Models\Video`, respectivamente. No entanto, você pode desejar desacoplar esses valores da estrutura interna da sua aplicação.

Por exemplo, em vez de usar os nomes dos modelos como o "tipo", podemos usar strings simples como `post` e `video`. Ao fazer isso, os valores da coluna "tipo" polimórfica no nosso banco de dados permanecerão válidos mesmo se os modelos forem renomeados:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

Você pode chamar o método `enforceMorphMap` no método `boot` da sua classe `App\Providers\AppServiceProvider` ou criar um provedor de serviço separado se desejar.

Você pode determinar o alias morph de um modelo em tempo de execução usando o método `getMorphClass` do modelo. Inversamente, você pode determinar o nome completo da classe qualificada associado a um alias morph usando o método `Relation::getMorphedModel`:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> **Aviso:**
> Ao adicionar um "morph map" à sua aplicação existente, cada valor de coluna morphable `*_type` no seu banco de dados que ainda contém uma classe qualificada completa precisará ser convertido para seu nome de "mapa".

<a id="dynamic-relationships"></a>
### Relacionamentos Dinâmicos

Você pode usar o método `resolveRelationUsing` para definir relações entre modelos Eloquent em tempo de execução. Embora não seja tipicamente recomendado para desenvolvimento normal de aplicações, isso pode ocasionalmente ser útil ao desenvolver pacotes Laravel.

O método `resolveRelationUsing` aceita o nome do relacionamento desejado como seu primeiro argumento. O segundo argumento passado para o método deve ser um closure que aceita a instância do modelo e retorna uma definição de relacionamento Eloquent válida. Tipicamente, você deve configurar relacionamentos dinâmicos dentro do método boot de um [provedor de serviço](../providers/):

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> **Aviso:**
> Ao definir relacionamentos dinâmicos, sempre forneça argumentos explícitos de nome de chave para os métodos de relacionamento Eloquent.

<a id="querying-relations"></a>
## Consultando Relacionamentos

Como todos os relacionamentos Eloquent são definidos via métodos, você pode chamar esses métodos para obter uma instância do relacionamento sem realmente executar uma consulta para carregar os modelos relacionados. Além disso, todos os tipos de relacionamentos Eloquent também servem como [construtores de consulta](../queries/), permitindo que você continue a encadear restrições na consulta de relacionamento antes de finalmente executar a consulta SQL contra o seu banco de dados.

Por exemplo, imagine uma aplicação de blog na qual um modelo `User` tem muitos modelos `Post` associados:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * Get all of the posts for the user.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

Você pode consultar o relacionamento `posts` e adicionar restrições adicionais ao relacionamento assim:

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

Você pode usar qualquer um dos métodos do [construtor de consulta](../queries/) do Laravel no relacionamento, então certifique-se de explorar a documentação do construtor de consulta para aprender sobre todos os métodos disponíveis para você.

<a id="chaining-orwhere-clauses-after-relationships"></a>
#### Encadeando Cláusulas `orWhere` Após Relacionamentos

Como demonstrado no exemplo acima, você é livre para adicionar restrições adicionais aos relacionamentos ao consultá-los. No entanto, tenha cuidado ao encadear cláusulas `orWhere` em um relacionamento, pois as cláusulas `orWhere` serão agrupadas logicamente no mesmo nível que a restrição do relacionamento:

```php
$user->posts()
    ->where('active', 1)
    ->orWhere('votes', '>=', 100)
    ->get();
```

O exemplo acima gerará o seguinte SQL. Como você pode ver, a cláusula `or` instrui a consulta a retornar _qualquer_ postagem com mais de 100 votos. A consulta não está mais restrita a um usuário específico:

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

Na maioria das situações, você deve usar [agrupamentos lógicos](../queries/#logical-grouping) para agrupar as verificações condicionais entre parênteses:

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
            ->orWhere('votes', '>=', 100);
    })
    ->get();
```

O exemplo acima produzirá o seguinte SQL. Observe que o agrupamento lógico agrupou corretamente as restrições e a consulta permanece restrita a um usuário específico:

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a id="relationship-methods-vs-dynamic-properties"></a>
### Métodos de Relacionamento vs. Propriedades Dinâmicas

Se você não precisa adicionar restrições adicionais a uma consulta de relacionamento Eloquent, pode acessar o relacionamento como se fosse uma propriedade. Por exemplo, continuando a usar nossos modelos de exemplo `User` e `Post`, podemos acessar todas as postagens de um usuário assim:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```

Propriedades dinâmicas de relacionamento realizam "lazy loading", significando que elas só carregarão seus dados de relacionamento quando você realmente acessá-las. Por causa disso, os desenvolvedores frequentemente usam [eager loading](#eager-loading) para pré-carregar relacionamentos que sabem que serão acessados após carregar o modelo. O eager loading fornece uma redução significativa nas consultas SQL que devem ser executadas para carregar as relações de um modelo.

<a id="querying-relationship-existence"></a>
### Consultando Existência de Relacionamento

Ao recuperar registros de modelos, você pode desejar limitar seus resultados com base na existência de um relacionamento. Por exemplo, imagine que você deseja recuperar todas as postagens de blog que têm pelo menos um comentário. Para fazer isso, você pode passar o nome do relacionamento para os métodos `has` e `orHas`:

```php
use App\Models\Post;

// Retrieve all posts that have at least one comment...
$posts = Post::has('comments')->get();
```

Você também pode especificar um operador e valor de contagem para personalizar ainda mais a consulta:

```php
// Retrieve all posts that have three or more comments...
$posts = Post::has('comments', '>=', 3)->get();
```

Declarações `has` aninhadas podem ser construídas usando notação de "ponto". Por exemplo, você pode recuperar todas as postagens que têm pelo menos um comentário que tem pelo menos uma imagem:

```php
// Retrieve posts that have at least one comment with images...
$posts = Post::has('comments.images')->get();
```

Se você precisa de ainda mais poder, pode usar os métodos `whereHas` e `orWhereHas` para definir restrições de consulta adicionais nas suas consultas `has`, como inspecionar o conteúdo de um comentário:

```php
use Illuminate\Database\Eloquent\Builder;

// Retrieve posts with at least one comment containing words like code%...
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// Retrieve posts with at least ten comments containing words like code%...
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> **Aviso:**
> O Eloquent atualmente não suporta a consulta de existência de relacionamento entre bancos de dados. Os relacionamentos devem existir dentro do mesmo banco de dados.

<a id="many-to-many-relationship-existence-queries"></a>
#### Consultas de Existência de Relacionamento Muitos para Muitos

O método `whereAttachedTo` pode ser usado para consultar modelos que têm um anexo muitos para muitos a um modelo ou coleção de modelos:

```php
$users = User::whereAttachedTo($role)->get();
```

Você também pode fornecer uma instância de [coleção](../eloquent-collections/) para o método `whereAttachedTo`. Ao fazer isso, o Laravel recuperará modelos que estão anexados a qualquer um dos modelos dentro da coleção:

```php
$tags = Tag::whereLike('name', '%laravel%')->get();

$posts = Post::whereAttachedTo($tags)->get();
```

<a id="inline-relationship-existence-queries"></a>
#### Consultas de Existência de Relacionamento Inline

Se você gostaria de consultar a existência de um relacionamento com uma única condição where simples anexada à consulta de relacionamento, pode achar mais conveniente usar os métodos `whereRelation`, `orWhereRelation`, `whereMorphRelation` e `orWhereMorphRelation`. Por exemplo, podemos consultar todas as postagens que têm comentários não aprovados:

```php
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

Claro, como chamadas ao método `where` do construtor de consulta, você também pode especificar um operador:

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->minus(hours: 1)
)->get();
```

<a id="querying-relationship-absence"></a>
### Consultando Ausência de Relacionamento

Ao recuperar registros de modelos, você pode desejar limitar seus resultados com base na ausência de um relacionamento. Por exemplo, imagine que você deseja recuperar todas as postagens de blog que **não** têm nenhum comentário. Para fazer isso, você pode passar o nome do relacionamento para os métodos `doesntHave` e `orDoesntHave`:

```php
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

Se você precisa de ainda mais poder, pode usar os métodos `whereDoesntHave` e `orWhereDoesntHave` para adicionar restrições de consulta adicionais às suas consultas `doesntHave`, como inspecionar o conteúdo de um comentário:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

Você pode usar notação de "ponto" para executar uma consulta contra um relacionamento aninhado. Por exemplo, a seguinte consulta recuperará todas as postagens que não têm comentários, bem como postagens que têm comentários onde nenhum dos comentários é de usuários banidos:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 1);
})->get();
```

<a id="querying-morph-to-relationships"></a>
### Consultando Relacionamentos Morph To

Para consultar a existência de relacionamentos "morph to", você pode usar os métodos `whereHasMorph` e `whereDoesntHaveMorph`. Esses métodos aceitam o nome do relacionamento como seu primeiro argumento. Em seguida, os métodos aceitam os nomes dos modelos relacionados que você deseja incluir na consulta. Finalmente, você pode fornecer um closure que personaliza a consulta de relacionamento:

```php
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// Retrieve comments associated to posts or videos with a title like code%...
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// Retrieve comments associated to posts with a title not like code%...
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

Você pode ocasionalmente precisar adicionar restrições de consulta com base no "tipo" do modelo polimórfico relacionado. O closure passado para o método `whereHasMorph` pode receber um valor `$type` como seu segundo argumento. Este argumento permite que você inspecione o "tipo" da consulta que está sendo construída:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query, string $type) {
        $column = $type === Post::class ? 'content' : 'title';

        $query->where($column, 'like', 'code%');
    }
)->get();
```

Às vezes você pode querer consultar os filhos do pai de um relacionamento "morph to". Você pode fazer isso usando os métodos `whereMorphedTo` e `whereNotMorphedTo`, que determinarão automaticamente o mapeamento de tipo morph apropriado para o modelo dado. Esses métodos aceitam o nome do relacionamento `morphTo` como seu primeiro argumento e o modelo pai relacionado como seu segundo argumento:

```php
$comments = Comment::whereMorphedTo('commentable', $post)
    ->orWhereMorphedTo('commentable', $video)
    ->get();
```

<a id="querying-all-morph-to-related-models"></a>
#### Consultando Todos os Modelos Relacionados

Em vez de passar um array de possíveis modelos polimórficos, você pode fornecer `*` como um valor curinga. Isso instruirá o Laravel a recuperar todos os possíveis tipos polimórficos do banco de dados. O Laravel executará uma consulta adicional para realizar esta operação:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a id="aggregating-related-models"></a>
## Agregando Modelos Relacionados

<a id="counting-related-models"></a>
### Contando Modelos Relacionados

Às vezes você pode querer contar o número de modelos relacionados para um determinado relacionamento sem realmente carregar os modelos. Para fazer isso, você pode usar o método `withCount`. O método `withCount` colocará um atributo `{relation}_count` nos modelos resultantes:

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

Passando um array para o método `withCount`, você pode adicionar as "contagens" para múltiplas relações, bem como adicionar restrições adicionais às consultas:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

Você também pode criar um alias para o resultado da contagem de relacionamento, permitindo múltiplas contagens no mesmo relacionamento:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount([
    'comments',
    'comments as pending_comments_count' => function (Builder $query) {
        $query->where('approved', false);
    },
])->get();

echo $posts[0]->comments_count;
echo $posts[0]->pending_comments_count;
```

<a id="deferred-count-loading"></a>
#### Carregamento Diferido de Contagem

Usando o método `loadCount`, você pode carregar uma contagem de relacionamento após o modelo pai já ter sido recuperado:

```php
$book = Book::first();

$book->loadCount('genres');
```

Se você precisa definir restrições de consulta adicionais na consulta de contagem, pode passar um array indexado pelos relacionamentos que deseja contar. Os valores do array devem ser closures que recebem a instância do construtor de consulta:

```php
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}]);
```

<a id="relationship-counting-and-custom-select-statements"></a>
#### Contagem de Relacionamento e Declarações Select Personalizadas

Se você está combinando `withCount` com uma declaração `select`, certifique-se de chamar `withCount` após o método `select`:

```php
$posts = Post::select(['title', 'body'])
    ->withCount('comments')
    ->get();
```

<a id="other-aggregate-functions"></a>
### Outras Funções de Agregação

Além do método `withCount`, o Eloquent fornece os métodos `withMin`, `withMax`, `withAvg`, `withSum` e `withExists`. Esses métodos colocarão um atributo `{relation}_{function}_{column}` nos seus modelos resultantes:

```php
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

Se você deseja acessar o resultado da função de agregação usando outro nome, pode especificar seu próprio alias:

```php
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

Assim como o método `loadCount`, versões diferidas desses métodos também estão disponíveis. Essas operações de agregação adicionais podem ser realizadas em modelos Eloquent que já foram recuperados:

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```

Se você está combinando esses métodos de agregação com uma declaração `select`, certifique-se de chamar os métodos de agregação após o método `select`:

```php
$posts = Post::select(['title', 'body'])
    ->withExists('comments')
    ->get();
```

<a id="counting-related-models-on-morph-to-relationships"></a>
### Contando Modelos Relacionados em Relacionamentos Morph To

Se você gostaria de fazer eager load de um relacionamento "morph to", bem como contagens de modelos relacionados para as várias entidades que podem ser retornadas por esse relacionamento, pode utilizar o método `with` em combinação com o método `morphWithCount` do relacionamento `morphTo`.

Neste exemplo, vamos supor que os modelos `Photo` e `Post` podem criar modelos `ActivityFeed`. Vamos assumir que o modelo `ActivityFeed` define um relacionamento "morph to" chamado `parentable` que nos permite recuperar o modelo pai `Photo` ou `Post` para uma determinada instância `ActivityFeed`. Além disso, vamos supor que os modelos `Photo` "have many" modelos `Tag` e os modelos `Post` "have many" modelos `Comment`.

Agora, vamos imaginar que queremos recuperar instâncias `ActivityFeed` e fazer eager load dos modelos pai `parentable` para cada instância `ActivityFeed`. Além disso, queremos recuperar o número de tags associadas a cada foto pai e o número de comentários associados a cada postagem pai:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$activities = ActivityFeed::with([
    'parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWithCount([
            Photo::class => ['tags'],
            Post::class => ['comments'],
        ]);
    }])->get();
```

<a id="morph-to-deferred-count-loading"></a>
#### Carregamento Diferido de Contagem

Vamos supor que já recuperamos um conjunto de modelos `ActivityFeed` e agora gostaríamos de carregar as contagens de relacionamentos aninhados para os vários modelos `parentable` associados aos feeds de atividade. Você pode usar o método `loadMorphCount` para fazer isso:

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a id="eager-loading"></a>
## Eager Loading

Ao acessar relacionamentos Eloquent como propriedades, os modelos relacionados são "lazy loaded". Isso significa que os dados do relacionamento não são realmente carregados até que você primeiro acesse a propriedade. No entanto, o Eloquent pode fazer "eager loading" dos relacionamentos no momento em que você consulta o modelo pai. O eager loading alivia o problema de consulta "N + 1". Para ilustrar o problema de consulta N + 1, considere um modelo `Book` que "belongs to" um modelo `Author`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * Get the author that wrote the book.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }
}
```

Agora, vamos recuperar todos os livros e seus autores:

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

Este loop executará uma consulta para recuperar todos os livros na tabela do banco de dados, e então outra consulta para cada livro a fim de recuperar o autor do livro. Então, se tivermos 25 livros, o código acima executaria 26 consultas: uma para o livro original, e 25 consultas adicionais para recuperar o autor de cada livro.

Felizmente, podemos usar eager loading para reduzir esta operação para apenas duas consultas. Ao construir uma consulta, você pode especificar quais relacionamentos devem ser carregados antecipadamente usando o método `with`:

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

Para esta operação, apenas duas consultas serão executadas - uma consulta para recuperar todos os livros e uma consulta para recuperar todos os autores de todos os livros:

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a id="eager-loading-multiple-relationships"></a>
#### Eager Loading de Múltiplos Relacionamentos

Às vezes você pode precisar fazer eager load de vários relacionamentos diferentes. Para fazer isso, basta passar um array de relacionamentos para o método `with`:

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a id="nested-eager-loading"></a>
#### Eager Loading Aninhado

Para fazer eager load dos relacionamentos de um relacionamento, você pode usar a sintaxe de "ponto". Por exemplo, vamos fazer eager load de todos os autores do livro e todos os contatos pessoais do autor:

```php
$books = Book::with('author.contacts')->get();
```

Alternativamente, você pode especificar relacionamentos de eager loading aninhados fornecendo um array aninhado para o método `with`, o que pode ser conveniente ao fazer eager load de múltiplos relacionamentos aninhados:

```php
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a id="nested-eager-loading-morphto-relationships"></a>
#### Eager Loading Aninhado de Relacionamentos `morphTo`

Se você gostaria de fazer eager load de um relacionamento `morphTo`, bem como relacionamentos aninhados nas várias entidades que podem ser retornadas por esse relacionamento, pode usar o método `with` em combinação com o método `morphWith` do relacionamento `morphTo`. Para ajudar a ilustrar este método, vamos considerar o seguinte modelo:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

Neste exemplo, vamos supor que os modelos `Event`, `Photo` e `Post` podem criar modelos `ActivityFeed`. Além disso, vamos supor que os modelos `Event` pertencem a um modelo `Calendar`, os modelos `Photo` estão associados a modelos `Tag`, e os modelos `Post` pertencem a um modelo `Author`.

Usando essas definições de modelo e relacionamentos, podemos recuperar instâncias do modelo `ActivityFeed` e fazer eager load de todos os modelos `parentable` e seus respectivos relacionamentos aninhados:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$activities = ActivityFeed::query()
    ->with(['parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWith([
            Event::class => ['calendar'],
            Photo::class => ['tags'],
            Post::class => ['author'],
        ]);
    }])->get();
```

<a id="eager-loading-specific-columns"></a>
#### Eager Loading de Colunas Específicas

Você pode não precisar sempre de cada coluna dos relacionamentos que está recuperando. Por esta razão, o Eloquent permite que você especifique quais colunas do relacionamento você gostaria de recuperar:

```php
$books = Book::with('author:id,name,book_id')->get();
```

> **Aviso:**
> Ao usar este recurso, você deve sempre incluir a coluna `id` e quaisquer colunas de chave estrangeira relevantes na lista de colunas que deseja recuperar.

<a id="eager-loading-by-default"></a>
#### Eager Loading por Padrão

Às vezes você pode querer sempre carregar alguns relacionamentos ao recuperar um modelo. Para fazer isso, você pode definir uma propriedade `$with` no modelo:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * The relationships that should always be loaded.
     *
     * @var array
     */
    protected $with = ['author'];

    /**
     * Get the author that wrote the book.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * Get the genre of the book.
     */
    public function genre(): BelongsTo
    {
        return $this->belongsTo(Genre::class);
    }
}
```

Se você gostaria de remover um item da propriedade `$with` para uma única consulta, pode usar o método `without`:

```php
$books = Book::without('author')->get();
```

Se você gostaria de sobrescrever todos os itens dentro da propriedade `$with` para uma única consulta, pode usar o método `withOnly`:

```php
$books = Book::withOnly('genre')->get();
```

<a id="constraining-eager-loads"></a>
### Restringindo Eager Loads

Às vezes você pode desejar fazer eager load de um relacionamento, mas também especificar condições de consulta adicionais para a consulta de eager loading. Você pode fazer isso passando um array de relacionamentos para o método `with` onde a chave do array é um nome de relacionamento e o valor do array é um closure que adiciona restrições adicionais à consulta de eager loading:

```php
use App\Models\User;

$users = User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

Neste exemplo, o Eloquent só fará eager load de postagens onde a coluna `title` da postagem contém a palavra `code`. Você pode chamar outros métodos do [construtor de consulta](../queries/) para personalizar ainda mais a operação de eager loading:

```php
$users = User::with(['posts' => function ($query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

<a id="constraining-eager-loading-of-morph-to-relationships"></a>
#### Restringindo Eager Loading de Relacionamentos `morphTo`

Se você está fazendo eager load de um relacionamento `morphTo`, o Eloquent executará múltiplas consultas para buscar cada tipo de modelo relacionado. Você pode adicionar restrições adicionais a cada uma dessas consultas usando o método `constrain` da relação `MorphTo`:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$comments = Comment::with(['commentable' => function (MorphTo $morphTo) {
    $morphTo->constrain([
        Post::class => function ($query) {
            $query->whereNull('hidden_at');
        },
        Video::class => function ($query) {
            $query->where('type', 'educational');
        },
    ]);
}])->get();
```

Neste exemplo, o Eloquent só fará eager load de postagens que não foram ocultadas e vídeos que têm um valor `type` de "educational".

<a id="constraining-eager-loads-with-relationship-existence"></a>
#### Restringindo Eager Loads com Existência de Relacionamento

Você pode às vezes se encontrar precisando verificar a existência de um relacionamento enquanto simultaneamente carrega o relacionamento com base nas mesmas condições. Por exemplo, você pode desejar recuperar apenas modelos `User` que têm modelos `Post` filhos correspondentes a uma determinada condição de consulta, enquanto também faz eager load das postagens correspondentes. Você pode fazer isso usando o método `withWhereHas`:

```php
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

<a id="lazy-eager-loading"></a>
### Lazy Eager Loading

Às vezes você pode precisar fazer eager load de um relacionamento após o modelo pai já ter sido recuperado. Por exemplo, isso pode ser útil se você precisa decidir dinamicamente se deve carregar modelos relacionados:

```php
use App\Models\Book;

$books = Book::all();

if ($condition) {
    $books->load('author', 'publisher');
}
```

Se você precisa definir restrições de consulta adicionais na consulta de eager loading, pode passar um array indexado pelos relacionamentos que deseja carregar. Os valores do array devem ser instâncias de closure que recebem a instância da consulta:

```php
$author->load(['books' => function ($query) {
    $query->orderBy('published_date', 'asc');
}]);
```

Para carregar um relacionamento apenas quando ele ainda não foi carregado, use o método `loadMissing`:

```php
$book->loadMissing('author');
```

<a id="nested-lazy-eager-loading-morphto"></a>
#### Lazy Eager Loading Aninhado e `morphTo`

Se você gostaria de fazer eager load de um relacionamento `morphTo`, bem como relacionamentos aninhados nas várias entidades que podem ser retornadas por esse relacionamento, pode usar o método `loadMorph`.

Este método aceita o nome do relacionamento `morphTo` como seu primeiro argumento, e um array de pares modelo / relacionamento como seu segundo argumento. Para ajudar a ilustrar este método, vamos considerar o seguinte modelo:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

Neste exemplo, vamos supor que os modelos `Event`, `Photo` e `Post` podem criar modelos `ActivityFeed`. Além disso, vamos supor que os modelos `Event` pertencem a um modelo `Calendar`, os modelos `Photo` estão associados a modelos `Tag`, e os modelos `Post` pertencem a um modelo `Author`.

Usando essas definições de modelo e relacionamentos, podemos recuperar instâncias do modelo `ActivityFeed` e fazer eager load de todos os modelos `parentable` e seus respectivos relacionamentos aninhados:

```php
$activities = ActivityFeed::with('parentable')
    ->get()
    ->loadMorph('parentable', [
        Event::class => ['calendar'],
        Photo::class => ['tags'],
        Post::class => ['author'],
    ]);
```

<a id="automatic-eager-loading"></a>
### Eager Loading Automático

Em muitos casos, o Laravel pode fazer eager load automaticamente dos relacionamentos que você acessa. Para habilitar o eager loading automático, você deve invocar o método `Model::automaticallyEagerLoadRelationships` dentro do método `boot` do `AppServiceProvider` da sua aplicação:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::automaticallyEagerLoadRelationships();
}
```

Quando este recurso está habilitado, o Laravel tentará carregar automaticamente quaisquer relacionamentos que você acessa que não foram previamente carregados. Por exemplo, considere o seguinte cenário:

```php
use App\Models\User;

$users = User::all();

foreach ($users as $user) {
    foreach ($user->posts as $post) {
        foreach ($post->comments as $comment) {
            echo $comment->content;
        }
    }
}
```

Tipicamente, o código acima executaria uma consulta para cada usuário a fim de recuperar suas postagens, bem como uma consulta para cada postagem para recuperar seus comentários. No entanto, quando o recurso `automaticallyEagerLoadRelationships` foi habilitado, o Laravel fará automaticamente [lazy eager load](#lazy-eager-loading) das postagens para todos os usuários na coleção de usuários quando você tenta acessar as postagens em qualquer um dos usuários recuperados. Da mesma forma, quando você tenta acessar os comentários para qualquer postagem recuperada, todos os comentários serão lazy eager loaded para todas as postagens que foram originalmente recuperadas.

Se você não deseja habilitar globalmente o eager loading automático, ainda pode habilitar este recurso para uma única instância de coleção Eloquent invocando o método `withRelationshipAutoloading` na coleção:

```php
$users = User::where('vip', true)->get();

return $users->withRelationshipAutoloading();
```

<a id="preventing-lazy-loading"></a>
### Prevenindo Lazy Loading

Como discutido anteriormente, fazer eager load dos relacionamentos pode frequentemente fornecer benefícios significativos de desempenho para sua aplicação. Portanto, se você desejar, pode instruir o Laravel a sempre prevenir o lazy loading de relacionamentos. Para fazer isso, você pode invocar o método `preventLazyLoading` oferecido pela classe base do modelo Eloquent. Tipicamente, você deve chamar este método dentro do método `boot` da classe `AppServiceProvider` da sua aplicação.

O método `preventLazyLoading` aceita um argumento booleano opcional que indica se o lazy loading deve ser prevenido. Por exemplo, você pode desejar apenas desabilitar o lazy loading em ambientes não-produção para que seu ambiente de produção continue funcionando normalmente mesmo se um relacionamento lazy loaded estiver acidentalmente presente no código de produção:

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

Após prevenir o lazy loading, o Eloquent lançará uma exceção `Illuminate\Database\LazyLoadingViolationException` quando sua aplicação tentar fazer lazy load de qualquer relacionamento Eloquent.

Você pode personalizar o comportamento das violações de lazy loading usando o método `handleLazyLoadingViolationUsing`. Por exemplo, usando este método, você pode instruir que as violações de lazy loading sejam apenas registradas em log em vez de interromper a execução da aplicação com exceções:

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a id="inserting-and-updating-related-models"></a>
## Inserindo e Atualizando Modelos Relacionados

<a id="the-save-method"></a>
### O Método `save`

O Eloquent fornece métodos convenientes para adicionar novos modelos a relacionamentos. Por exemplo, talvez você precise adicionar um novo comentário a uma postagem. Em vez de definir manualmente o atributo `post_id` no modelo `Comment`, você pode inserir o comentário usando o método `save` do relacionamento:

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

Observe que não acessamos o relacionamento `comments` como uma propriedade dinâmica. Em vez disso, chamamos o método `comments` para obter uma instância do relacionamento. O método `save` adicionará automaticamente o valor apropriado `post_id` ao novo modelo `Comment`.

Se você precisa salvar múltiplos modelos relacionados, pode usar o método `saveMany`:

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

Os métodos `save` e `saveMany` persistirão as instâncias de modelo fornecidas, mas não adicionarão os modelos recém-persistidos a quaisquer relacionamentos em memória que já estão carregados no modelo pai. Se você planeja acessar o relacionamento após usar os métodos `save` ou `saveMany`, pode desejar usar o método `refresh` para recarregar o modelo e seus relacionamentos:

```php
$post->comments()->save($comment);

$post->refresh();

// All comments, including the newly saved comment...
$post->comments;
```

<a id="the-push-method"></a>
#### Salvando Modelos e Relacionamentos Recursivamente

Se você gostaria de `save` seu modelo e todos os seus relacionamentos associados, pode usar o método `push`. Neste exemplo, o modelo `Post` será salvo, bem como seus comentários e os autores dos comentários:

```php
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

O método `pushQuietly` pode ser usado para salvar um modelo e seus relacionamentos associados sem disparar nenhum evento:

```php
$post->pushQuietly();
```

<a id="the-create-method"></a>
### O Método `create`

Além dos métodos `save` e `saveMany`, você também pode usar o método `create`, que aceita um array de atributos, cria um modelo e o insere no banco de dados. A diferença entre `save` e `create` é que `save` aceita uma instância completa de modelo Eloquent, enquanto `create` aceita um `array` PHP simples. O modelo recém-criado será retornado pelo método `create`:

```php
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

Você pode usar o método `createMany` para criar múltiplos modelos relacionados:

```php
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

Os métodos `createQuietly` e `createManyQuietly` podem ser usados para criar modelo(s) sem despachar nenhum evento:

```php
$user = User::find(1);

$user->posts()->createQuietly([
    'title' => 'Post title.',
]);

$user->posts()->createManyQuietly([
    ['title' => 'First post.'],
    ['title' => 'Second post.'],
]);
```

Você também pode usar os métodos `findOrNew`, `firstOrNew`, `firstOrCreate` e `updateOrCreate` para [criar e atualizar modelos em relacionamentos](../eloquent/#upserts).

> **Nota:**
> Antes de usar o método `create`, certifique-se de revisar a documentação de [mass assignment](../eloquent/#mass-assignment).

<a id="updating-belongs-to-relationships"></a>
### Relacionamentos Belongs To

Se você gostaria de atribuir um modelo filho a um novo modelo pai, pode usar o método `associate`. Neste exemplo, o modelo `User` define um relacionamento `belongsTo` com o modelo `Account`. Este método `associate` definirá a chave estrangeira no modelo filho:

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

Para remover um modelo pai de um modelo filho, você pode usar o método `dissociate`. Este método definirá a chave estrangeira do relacionamento como `null`:

```php
$user->account()->dissociate();

$user->save();
```

<a id="updating-many-to-many-relationships"></a>
### Relacionamentos Muitos para Muitos

<a id="attaching-detaching"></a>
#### Anexando / Desanexando

O Eloquent também fornece métodos para tornar o trabalho com relacionamentos muitos para mais convenientes. Por exemplo, vamos imaginar que um usuário pode ter muitas funções e uma função pode ter muitos usuários. Você pode usar o método `attach` para anexar uma função a um usuário inserindo um registro na tabela intermediária do relacionamento:

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

Ao anexar um relacionamento a um modelo, você também pode passar um array de dados adicionais para serem inseridos na tabela intermediária:

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```

Às vezes pode ser necessário remover uma função de um usuário. Para remover um registro de relacionamento muitos para muitos, use o método `detach`. O método `detach` deletará o registro apropriado da tabela intermediária; no entanto, ambos os modelos permanecerão no banco de dados:

```php
// Detach a single role from the user...
$user->roles()->detach($roleId);

// Detach all roles from the user...
$user->roles()->detach();
```

Por conveniência, `attach` e `detach` também aceitam arrays de IDs como entrada:

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a id="syncing-associations"></a>
#### Sincronizando Associações

Você também pode usar o método `sync` para construir associações muitos para muitos. O método `sync` aceita um array de IDs para colocar na tabela intermediária. Quaisquer IDs que não estão no array fornecido serão removidos da tabela intermediária. Então, após esta operação ser concluída, apenas os IDs no array fornecido existirão na tabela intermediária:

```php
$user->roles()->sync([1, 2, 3]);
```

Você também pode passar valores adicionais da tabela intermediária com os IDs:

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

Se você gostaria de inserir os mesmos valores da tabela intermediária com cada um dos IDs de modelo sincronizados, pode usar o método `syncWithPivotValues`:

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

Se você não deseja desanexar IDs existentes que estão faltando no array fornecido, pode usar o método `syncWithoutDetaching`:

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a id="toggling-associations"></a>
#### Alternando Associações

O relacionamento muitos para muitos também fornece um método `toggle` que "alterna" o status de anexo dos IDs de modelo relacionado fornecidos. Se o ID fornecido está atualmente anexado, ele será desanexado. Da mesma forma, se está atualmente desanexado, ele será anexado:

```php
$user->roles()->toggle([1, 2, 3]);
```

Você também pode passar valores adicionais da tabela intermediária com os IDs:

```php
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a id="transactional-pivot-operations"></a>
#### Operações Pivot Transacionais

Cada uma das operações pivot discutidas acima também tem uma variante `OrFail` (`attachOrFail`, `detachOrFail`, `syncOrFail`, `syncWithoutDetachingOrFail` e `toggleOrFail`) que envolve a operação dentro de uma transação de banco de dados, para que todas as alterações sejam automaticamente revertidas se uma exceção for lançada:

```php
$user->roles()->attachOrFail([1, 2, 3]);

$user->roles()->syncOrFail([1, 2, 3]);
```

<a id="updating-a-record-on-the-intermediate-table"></a>
#### Atualizando um Registro na Tabela Intermediária

Se você precisa atualizar uma linha existente na tabela intermediária do seu relacionamento, pode usar o método `updateExistingPivot`. Este método aceita a chave estrangeira do registro intermediário e um array de atributos para atualizar:

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a id="touching-parent-timestamps"></a>
## Atualizando Timestamps do Modelo Pai

Quando um modelo define um relacionamento `belongsTo` ou `belongsToMany` com outro modelo, como um `Comment` que pertence a um `Post`, é às vezes útil atualizar o timestamp do pai quando o modelo filho é atualizado.

Por exemplo, quando um modelo `Comment` é atualizado, você pode querer automaticamente "touch" o timestamp `updated_at` do `Post` proprietário para que ele seja definido com a data e hora atuais. Para fazer isso, você pode usar o atributo `Touches` no seu modelo filho contendo os nomes dos relacionamentos que devem ter seus timestamps `updated_at` atualizados quando o modelo filho é atualizado:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Touches;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Touches(['post'])]
class Comment extends Model
{
    /**
     * Get the post that the comment belongs to.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

> **Aviso:**
> Os timestamps do modelo pai só serão atualizados se o modelo filho for atualizado usando o método `save` do Eloquent.