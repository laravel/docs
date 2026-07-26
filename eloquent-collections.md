---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Eloquent: колекції

- [Вступ](#introduction)
- [Доступні методи](#available-methods)
- [Власні колекції](#custom-collections)

<a name="introduction"></a>
## Вступ

Усі методи Eloquent, що повертають більш ніж одну модель, повертають екземпляри класу `Illuminate\Database\Eloquent\Collection` - зокрема й результати методу `get` та отримані через зв'язок. Об'єкт колекції Eloquent розширює [базову колекцію](/docs/{{version}}/collections) Laravel, тож він природно успадковує десятки методів для плавної роботи з масивом моделей Eloquent, що лежить у його основі. Обов'язково перегляньте документацію з колекцій Laravel, щоб дізнатися про всі ці корисні методи!

Усі колекції є також ітераторами, тож ви можете обходити їх у циклі, наче звичайні PHP-масиви:

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

Проте, як уже згадувалося, колекції значно потужніші за масиви й дають цілу низку операцій map / reduce, які можна зчіплювати ланцюжком через інтуїтивний інтерфейс. Наприклад, ми можемо прибрати всі неактивні моделі, а потім зібрати імена решти користувачів:

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Перетворення колекцій Eloquent

Хоча більшість методів колекції Eloquent повертають новий екземпляр колекції Eloquent, методи `collapse`, `flatten`, `flip`, `keys`, `pluck` і `zip` повертають екземпляр [базової колекції](/docs/{{version}}/collections). Так само, якщо операція `map` повертає колекцію, у якій немає жодної моделі Eloquent, її буде перетворено на екземпляр базової колекції.

<a name="available-methods"></a>
## Доступні методи

Усі колекції Eloquent розширюють об'єкт базової [колекції Laravel](/docs/{{version}}/collections#available-methods), тож успадковують усі потужні методи базового класу колекцій.

Крім того, клас `Illuminate\Database\Eloquent\Collection` має надмножину методів для роботи з колекціями ваших моделей. Більшість методів повертають екземпляри `Illuminate\Database\Eloquent\Collection`; проте деякі - як-от `modelKeys` - повертають екземпляр `Illuminate\Support\Collection`.

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

<a name="method-append"></a>
#### `append($attributes)` {.collection-method .first-collection-method}

Методом `append` можна вказати, що атрибут слід [додавати](/docs/{{version}}/eloquent-serialization#appending-values-to-json) для кожної моделі в колекції. Метод приймає масив атрибутів або один атрибут:

```php
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)` {.collection-method}

Методом `contains` можна визначити, чи міститься в колекції заданий екземпляр моделі. Метод приймає первинний ключ або екземпляр моделі:

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)` {.collection-method}

Метод `diff` повертає всі моделі, яких немає в заданій колекції:

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)` {.collection-method}

Метод `except` повертає всі моделі, які не мають заданих первинних ключів:

```php
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)` {.collection-method}

Метод `find` повертає модель, первинний ключ якої збігається із заданим. Якщо `$key` - екземпляр моделі, `find` спробує повернути модель із таким самим первинним ключем. Якщо `$key` - масив ключів, `find` поверне всі моделі, чиї первинні ключі є в цьому масиві:

```php
$users = User::all();

$user = $users->find(1);
```

<a name="method-find-or-fail"></a>
#### `findOrFail($key)` {.collection-method}

Метод `findOrFail` повертає модель, первинний ключ якої збігається із заданим, або викидає виняток `Illuminate\Database\Eloquent\ModelNotFoundException`, якщо відповідної моделі в колекції немає:

```php
$users = User::all();

$user = $users->findOrFail(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])` {.collection-method}

Метод `fresh` дістає з бази даних свіжий екземпляр кожної моделі в колекції. Крім того, будь-які вказані зв'язки буде жадібно завантажено:

```php
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)` {.collection-method}

Метод `intersect` повертає всі моделі, які є також у заданій колекції:

```php
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)` {.collection-method}

Метод `load` жадібно завантажує задані зв'язки для всіх моделей у колекції:

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)` {.collection-method}

Метод `loadMissing` жадібно завантажує задані зв'язки для всіх моделей у колекції, якщо ці зв'язки ще не завантажено:

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
#### `modelKeys()` {.collection-method}

Метод `modelKeys` повертає первинні ключі всіх моделей у колекції:

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)` {.collection-method}

Метод `makeVisible` [робить видимими атрибути](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json), які зазвичай «приховані» в кожній моделі колекції:

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)` {.collection-method}

Метод `makeHidden` [приховує атрибути](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json), які зазвичай «видимі» в кожній моделі колекції:

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-mergeVisible"></a>
#### `mergeVisible($attributes)` {.collection-method}

Метод `mergeVisible` [робить видимими додаткові атрибути](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json), зберігаючи наявні видимі атрибути:

```php
$users = $users->mergeVisible(['middle_name']);
```

<a name="method-mergeHidden"></a>
#### `mergeHidden($attributes)` {.collection-method}

Метод `mergeHidden` [приховує додаткові атрибути](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json), зберігаючи наявні приховані атрибути:

```php
$users = $users->mergeHidden(['last_login_at']);
```

<a name="method-only"></a>
#### `only($keys)` {.collection-method}

Метод `only` повертає всі моделі, які мають задані первинні ключі:

```php
$users = $users->only([1, 2, 3]);
```

<a name="method-partition"></a>
#### `partition` {.collection-method}

Метод `partition` повертає екземпляр `Illuminate\Support\Collection`, що містить екземпляри колекцій `Illuminate\Database\Eloquent\Collection`:

```php
$partition = $users->partition(fn ($user) => $user->age > 18);

dump($partition::class);    // Illuminate\Support\Collection
dump($partition[0]::class); // Illuminate\Database\Eloquent\Collection
dump($partition[1]::class); // Illuminate\Database\Eloquent\Collection
```

<a name="method-setAppends"></a>
#### `setAppends($attributes)` {.collection-method}

Метод `setAppends` тимчасово перевизначає всі [додані атрибути](/docs/{{version}}/eloquent-serialization#appending-values-to-json) кожної моделі в колекції:

```php
$users = $users->setAppends(['is_admin']);
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)` {.collection-method}

Метод `setVisible` [тимчасово перевизначає](/docs/{{version}}/eloquent-serialization#temporarily-modifying-attribute-visibility) всі видимі атрибути кожної моделі в колекції:

```php
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)` {.collection-method}

Метод `setHidden` [тимчасово перевизначає](/docs/{{version}}/eloquent-serialization#temporarily-modifying-attribute-visibility) всі приховані атрибути кожної моделі в колекції:

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()` {.collection-method}

Метод `toQuery` повертає екземпляр конструктора запитів Eloquent з обмеженням `whereIn` за первинними ключами моделей колекції:

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)` {.collection-method}

Метод `unique` повертає всі унікальні моделі колекції. Моделі з таким самим первинним ключем, як в іншої моделі колекції, буде прибрано:

```php
$users = $users->unique();
```

<a name="method-withoutAppends"></a>
#### `withoutAppends()` {.collection-method}

Метод `withoutAppends` тимчасово прибирає всі [додані атрибути](/docs/{{version}}/eloquent-serialization#appending-values-to-json) кожної моделі в колекції:

```php
$users = $users->withoutAppends();
```

<a name="custom-collections"></a>
## Власні колекції

Якщо ви хочете використовувати власний об'єкт `Collection` під час роботи з певною моделлю, додайте до неї атрибут `CollectedBy`:

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

Або ж ви можете описати в моделі метод `newCollection`:

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

Коли ви описали метод `newCollection` або додали до моделі атрибут `CollectedBy`, ви отримуватимете екземпляр власної колекції щоразу, коли Eloquent зазвичай повернув би екземпляр `Illuminate\Database\Eloquent\Collection`.

Якщо ви хочете використовувати власну колекцію для кожної моделі у вашому застосунку, опишіть метод `newCollection` у базовому класі моделі, який розширюють усі моделі вашого застосунку.
