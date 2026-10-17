---
title: "Eloquent: Coleções"
---

- [Introdução](#introduction)
- [Métodos Disponíveis](#available-methods)
- [Coleções Personalizadas](#custom-collections)

<a id="introduction"></a>
## Introdução

Todos os métodos do Eloquent que retornam mais de um resultado de model retornarão instâncias da classe `Illuminate\Database\Eloquent\Collection`, incluindo resultados recuperados pelo método `get` ou acessados por meio de um relacionamento. O objeto de coleção do Eloquent estende a [coleção base](../collections/) do Laravel, por isso herda naturalmente dezenas de métodos usados para trabalhar de forma fluente com o array subjacente de models do Eloquent. Certifique-se de revisar a documentação de coleções do Laravel para conhecer todos esses métodos úteis!

Todas as coleções também funcionam como iteradores, permitindo que você percorra-as como se fossem arrays simples do PHP:

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

No entanto, como mencionado anteriormente, as coleções são muito mais poderosas do que arrays e expõem uma variedade de operações de map / reduce que podem ser encadeadas usando uma interface intuitiva. Por exemplo, podemos remover todos os models inativos e, em seguida, obter o primeiro nome de cada usuário restante:

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a id="eloquent-collection-conversion"></a>
#### Conversão de Coleção Eloquent

Embora a maioria dos métodos de coleção do Eloquent retorne uma nova instância de coleção do Eloquent, os métodos `collapse`, `flatten`, `flip`, `keys`, `pluck` e `zip` retornam uma instância de [coleção base](../collections/). Da mesma forma, se uma operação `map` retornar uma coleção que não contenha nenhum model do Eloquent, ela será convertida em uma instância de coleção base.

<a id="available-methods"></a>
## Métodos Disponíveis

Todas as coleções do Eloquent estendem o objeto base de [coleção do Laravel](../collections/#available-methods); portanto, herdam todos os métodos poderosos fornecidos pela classe de coleção base.

Além disso, a classe `Illuminate\Database\Eloquent\Collection` fornece um conjunto de métodos adicionais para auxiliar no gerenciamento das suas coleções de models. A maioria dos métodos retorna instâncias de `Illuminate\Database\Eloquent\Collection`; no entanto, alguns métodos, como `pluck`, retornam uma instância de `Illuminate\Support\Collection`.

<style>
    .collection-method-list > p {
        columns: 14.4em 1; -moz-columns: 14.4em 1; -webkit-columns: 14.4em 1;
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

<div class="collection-method-list" markdown="1">

[append](#method-append)
[contains](#method-contains)
[diff](#method-diff)
[except](#method-except)
[find](#method-find)
[findOrFail](#method-find-or-fail)
[fresh](#method-fresh)
[intersect](#method-intersect)
[load](#method-load)
[loadMissing](#method-loadMissing)
[modelKeys](#method-modelKeys)
[makeVisible](#method-makeVisible)
[makeHidden](#method-makeHidden)
[mergeVisible](#method-mergeVisible)
[mergeHidden](#method-mergeHidden)
[only](#method-only)
[partition](#method-partition)
[setAppends](#method-setAppends)
[setVisible](#method-setVisible)
[setHidden](#method-setHidden)
[toQuery](#method-toquery)
[unique](#method-unique)
[withoutAppends](#method-withoutAppends)

</div>

<a id="method-append"></a>
#### `append($attributes)` {.collection-method .first-collection-method}

O método `append` pode ser usado para indicar que um atributo deve ser [anexado](../eloquent-serialization/#appending-values-to-json) a cada model da coleção. Este método aceita um array de atributos ou um único atributo:

```php
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a id="method-contains"></a>
#### `contains($key, $operator = null, $value = null)` {.collection-method}

O método `contains` pode ser usado para determinar se uma determinada instância de model está contida na coleção. Este método aceita uma chave primária ou uma instância de model:

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a id="method-diff"></a>
#### `diff($items)` {.collection-method}

O método `diff` retorna todos os models que não estão presentes na coleção fornecida:

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a id="method-except"></a>
#### `except($keys)` {.collection-method}

O método `except` retorna todos os models que não possuem as chaves primárias informadas:

```php
$users = $users->except([1, 2, 3]);
```

<a id="method-find"></a>
#### `find($key)` {.collection-method}

O método `find` retorna o model cuja chave primária corresponde à chave informada. Se `$key` for uma instância de model, `find` tentará retornar um model que corresponda à chave primária. Se `$key` for um array de chaves, `find` retornará todos os models cuja chave primária esteja no array informado:

```php
$users = User::all();

$user = $users->find(1);
```

<a id="method-find-or-fail"></a>
#### `findOrFail($key)` {.collection-method}

O método `findOrFail` retorna o model cuja chave primária corresponde à chave informada ou lança uma exceção `Illuminate\Database\Eloquent\ModelNotFoundException` caso nenhum model correspondente seja encontrado na coleção:

```php
$users = User::all();

$user = $users->findOrFail(1);
```

<a id="method-fresh"></a>
#### `fresh($with = [])` {.collection-method}

O método `fresh` recupera uma instância nova de cada model da coleção a partir do banco de dados. Além disso, quaisquer relacionamentos especificados serão carregados antecipadamente (eager loading):

```php
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a id="method-intersect"></a>
#### `intersect($items)` {.collection-method}

O método `intersect` retorna todos os models que também estão presentes na coleção fornecida:

```php
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a id="method-load"></a>
#### `load($relations)` {.collection-method}

O método `load` carrega antecipadamente (eager load) os relacionamentos informados para todos os models da coleção:

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a id="method-loadMissing"></a>
#### `loadMissing($relations)` {.collection-method}

O método `loadMissing` carrega antecipadamente (eager load) os relacionamentos informados para todos os models da coleção, caso esses relacionamentos ainda não estejam carregados:

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a id="method-modelKeys"></a>
#### `modelKeys()` {.collection-method}

O método `modelKeys` retorna as chaves primárias de todos os models da coleção:

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a id="method-makeVisible"></a>
#### `makeVisible($attributes)` {.collection-method}

O método `makeVisible` [torna visíveis](../eloquent-serialization/#hiding-attributes-from-json) os atributos que normalmente estão "ocultos" em cada model da coleção:

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a id="method-makeHidden"></a>
#### `makeHidden($attributes)` {.collection-method}

O método `makeHidden` [oculta atributos](../eloquent-serialization/#hiding-attributes-from-json) que normalmente estão "visíveis" em cada model da coleção:

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a id="method-mergeVisible"></a>
#### `mergeVisible($attributes)` {.collection-method}

O método `mergeVisible` [torna visíveis atributos adicionais](../eloquent-serialization/#hiding-attributes-from-json), mantendo os atributos visíveis já existentes:

```php
$users = $users->mergeVisible(['middle_name']);
```

<a id="method-mergeHidden"></a>
#### `mergeHidden($attributes)` {.collection-method}

O método `mergeHidden` [oculta atributos adicionais](../eloquent-serialization/#hiding-attributes-from-json), mantendo os atributos ocultos já existentes:

```php
$users = $users->mergeHidden(['last_login_at']);
```

<a id="method-only"></a>
#### `only($keys)` {.collection-method}

O método `only` retorna todos os models que possuem as chaves primárias informadas:

```php
$users = $users->only([1, 2, 3]);
```

<a id="method-partition"></a>
#### `partition` {.collection-method}

O método `partition` retorna uma instância de `Illuminate\Support\Collection` contendo instâncias de coleção `Illuminate\Database\Eloquent\Collection`:

```php
$partition = $users->partition(fn ($user) => $user->age > 18);

dump($partition::class);    // Illuminate\Support\Collection
dump($partition[0]::class); // Illuminate\Database\Eloquent\Collection
dump($partition[1]::class); // Illuminate\Database\Eloquent\Collection
```

<a id="method-setAppends"></a>
#### `setAppends($attributes)` {.collection-method}

O método `setAppends` sobrescreve temporariamente todos os [atributos anexados](../eloquent-serialization/#appending-values-to-json) em cada model da coleção:

```php
$users = $users->setAppends(['is_admin']);
```

<a id="method-setVisible"></a>
#### `setVisible($attributes)` {.collection-method}

O método `setVisible` [sobrescreve temporariamente](../eloquent-serialization/#temporarily-modifying-attribute-visibility) todos os atributos visíveis em cada model da coleção:

```php
$users = $users->setVisible(['id', 'name']);
```

<a id="method-setHidden"></a>
#### `setHidden($attributes)` {.collection-method}

O método `setHidden` [sobrescreve temporariamente](../eloquent-serialization/#temporarily-modifying-attribute-visibility) todos os atributos ocultos em cada model da coleção:

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a id="method-toquery"></a>
#### `toQuery()` {.collection-method}

O método `toQuery` retorna uma instância do query builder do Eloquent contendo uma restrição `whereIn` sobre as chaves primárias dos models da coleção:

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a id="method-unique"></a>
#### `unique($key = null, $strict = false)` {.collection-method}

O método `unique` retorna todos os models únicos da coleção. Quaisquer models com a mesma chave primária de outro model da coleção são removidos:

```php
$users = $users->unique();
```

<a id="method-withoutAppends"></a>
#### `withoutAppends()` {.collection-method}

O método `withoutAppends` remove temporariamente todos os [atributos anexados](../eloquent-serialization/#appending-values-to-json) em cada model da coleção:

```php
$users = $users->withoutAppends();
```

<a id="custom-collections"></a>
## Coleções Personalizadas

Se você quiser usar um objeto `Collection` personalizado ao interagir com um determinado model, pode adicionar o atributo `CollectedBy` ao seu model:

```php
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Attributes\CollectedBy;
use Illuminate\Database\Eloquent\Model;

#[CollectedBy(UserCollection::class)]
class User extends Model
{
    // ...
}
```

Alternativamente, você pode definir um método `newCollection` no seu model:

```php
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Create a new Eloquent Collection instance.
     *
     * @param  array<int, \Illuminate\Database\Eloquent\Model>  $models
     * @return \Illuminate\Database\Eloquent\Collection<int, \Illuminate\Database\Eloquent\Model>
     */
    public function newCollection(array $models = []): Collection
    {
        $collection = new UserCollection($models);

        if (Model::isAutomaticallyEagerLoadingRelationships()) {
            $collection->withRelationshipAutoloading();
        }

        return $collection;
    }
}
```

Assim que você tiver definido um método `newCollection` ou adicionado o atributo `CollectedBy` ao seu model, você receberá uma instância da sua coleção personalizada sempre que o Eloquent normalmente retornaria uma instância de `Illuminate\Database\Eloquent\Collection`.

Se você quiser usar uma coleção personalizada para todos os models da sua aplicação, deve definir o método `newCollection` em uma classe base de model que seja estendida por todos os models da sua aplicação.
