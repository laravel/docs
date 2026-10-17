---
title: "Eloquent: Serialização"
---

- [Introdução](#introduction)
- [Serializando Models e Collections](#serializing-models-and-collections)
    - [Serializando para Arrays](#serializing-to-arrays)
    - [Serializando para JSON](#serializing-to-json)
- [Ocultando Atributos do JSON](#hiding-attributes-from-json)
- [Adicionando Valores ao JSON](#appending-values-to-json)
- [Serialização de Datas](#date-serialization)

<a id="introduction"></a>
## Introdução

Ao construir APIs usando o Laravel, você frequentemente precisará converter seus models e relacionamentos em arrays ou JSON. O Eloquent inclui métodos convenientes para fazer essas conversões, bem como para controlar quais atributos são incluídos na representação serializada dos seus models.

> **Note:**
> Para uma maneira ainda mais robusta de lidar com a serialização JSON de models e collections do Eloquent, confira a documentação sobre [Eloquent API resources](/en/eloquent-resources/).

<a id="serializing-models-and-collections"></a>
## Serializando Models e Collections

<a id="serializing-to-arrays"></a>
### Serializando para Arrays

Para converter um model e seus [relacionamentos](/en/eloquent-relationships/) carregados em um array, você deve usar o método `toArray`. Esse método é recursivo, portanto, todos os atributos e todos os relacionamentos (incluindo os relacionamentos dos relacionamentos) serão convertidos em arrays:

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

O método `attributesToArray` pode ser usado para converter os atributos de um model em um array, mas não seus relacionamentos:

```php
$user = User::first();

return $user->attributesToArray();
```

Você também pode converter [collections](/en/eloquent-collections/) inteiras de models em arrays chamando o método `toArray` na instância da collection:

```php
$users = User::all();

return $users->toArray();
```

<a id="serializing-to-json"></a>
### Serializando para JSON

Para converter um model em JSON, você deve usar o método `toJson`. Assim como o `toArray`, o método `toJson` é recursivo, portanto, todos os atributos e relacionamentos serão convertidos em JSON. Você também pode especificar quaisquer opções de codificação JSON que sejam [suportadas pelo PHP](https://secure.php.net/manual/en/function.json-encode.php):

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

Alternativamente, você pode converter um model ou collection em uma string, o que chamará automaticamente o método `toJson` no model ou na collection:

```php
return (string) User::find(1);
```

Como os models e collections são convertidos em JSON quando convertidos em string, você pode retornar objetos Eloquent diretamente das rotas ou controllers da sua aplicação. O Laravel serializará automaticamente seus models e collections do Eloquent em JSON quando eles forem retornados de rotas ou controllers:

```php
Route::get('/users', function () {
    return User::all();
});
```

<a id="relationships"></a>
#### Relacionamentos

Quando um model do Eloquent é convertido em JSON, seus relacionamentos carregados serão automaticamente incluídos como atributos no objeto JSON. Além disso, embora os métodos de relacionamento do Eloquent sejam definidos usando nomes de método em "camel case", o atributo JSON de um relacionamento será em "snake case".

<a id="hiding-attributes-from-json"></a>
## Ocultando Atributos do JSON

Às vezes, você pode querer limitar os atributos, como senhas, que são incluídos na representação em array ou JSON do seu model. Para fazer isso, você pode usar o atributo `Hidden` no seu model. Os atributos que estiverem listados no atributo `Hidden` não serão incluídos na representação serializada do seu model:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Hidden;
use Illuminate\Database\Eloquent\Model;

#[Hidden(['password'])]
class User extends Model
{
    // ...
}
```


> **Note:**
> Para ocultar relacionamentos, adicione o nome do método do relacionamento ao atributo `Hidden` do seu model do Eloquent.

Alternativamente, você pode usar o atributo `Visible` para definir uma "lista de permissões" de atributos que devem ser incluídos na representação em array e JSON do seu model. Todos os atributos que não estiverem presentes no atributo `Visible` serão ocultados quando o model for convertido em um array ou JSON:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Visible;
use Illuminate\Database\Eloquent\Model;

#[Visible(['first_name', 'last_name'])]
class User extends Model
{
    // ...
}
```

<a id="temporarily-modifying-attribute-visibility"></a>
#### Modificando Temporariamente a Visibilidade dos Atributos

Se você quiser tornar visíveis, em uma determinada instância do model, alguns atributos que normalmente estão ocultos, você pode usar os métodos `makeVisible` ou `mergeVisible`. O método `makeVisible` retorna a instância do model:

```php
return $user->makeVisible('attribute')->toArray();

return $user->mergeVisible(['name', 'email'])->toArray();
```

Da mesma forma, se você quiser ocultar alguns atributos que normalmente são visíveis, você pode usar os métodos `makeHidden` ou `mergeHidden`:

```php
return $user->makeHidden('attribute')->toArray();

return $user->mergeHidden(['name', 'email'])->toArray();
```

Se você quiser substituir temporariamente todos os atributos visíveis ou ocultos, pode usar os métodos `setVisible` e `setHidden`, respectivamente:

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a id="appending-values-to-json"></a>
## Adicionando Valores ao JSON

Ocasionalmente, ao converter models em arrays ou JSON, você pode querer adicionar atributos que não possuem uma coluna correspondente no seu banco de dados. Para fazer isso, primeiro defina um [accessor](/en/eloquent-mutators/) para o valor:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Determine if the user is an administrator.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

Se você quiser que o accessor seja sempre adicionado às representações em array e JSON do seu model, pode usar o atributo `Appends` no seu model. Observe que os nomes dos atributos são normalmente referenciados usando sua representação serializada em "snake case", mesmo que o método PHP do accessor seja definido usando "camel case":

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Appends;
use Illuminate\Database\Eloquent\Model;

#[Appends(['is_admin'])]
class User extends Model
{
    // ...
}
```

Depois que o atributo for adicionado à lista `appends`, ele será incluído tanto na representação em array quanto na representação JSON do model. Os atributos no array `appends` também respeitarão as configurações `visible` e `hidden` definidas no model.

<a id="appending-at-run-time"></a>
#### Adicionando em Tempo de Execução

Em tempo de execução, você pode instruir uma instância do model a adicionar atributos adicionais usando os métodos `append` ou `mergeAppends`. Ou, você pode usar o método `setAppends` para substituir todo o array de propriedades adicionadas de uma determinada instância do model:

```php
return $user->append('is_admin')->toArray();

return $user->mergeAppends(['is_admin', 'status'])->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

Da mesma forma, se você quiser remover todas as propriedades adicionadas de um model, pode usar o método `withoutAppends`:

```php
return $user->withoutAppends()->toArray();
```

<a id="date-serialization"></a>
## Serialização de Datas

<a id="customizing-the-default-date-format"></a>
#### Personalizando o Formato de Data Padrão

Você pode personalizar o formato de serialização padrão substituindo o método `serializeDate`. Esse método não afeta como suas datas são formatadas para armazenamento no banco de dados:

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a id="customizing-the-date-format-per-attribute"></a>
#### Personalizando o Formato de Data por Atributo

Você pode personalizar o formato de serialização de atributos de data individuais do Eloquent especificando o formato de data nas [declarações de cast](/en/eloquent-mutators/#attribute-casting) do model:

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```
