---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Хелпери

- [Вступ](#introduction)
- [Доступні методи](#available-methods)
- [Інші утиліти](#other-utilities)
    - [Бенчмаркінг](#benchmarking)
    - [Дата й час](#dates)
    - [Відкладені функції](#deferred-functions)
    - [Лотерея](#lottery)
    - [Конвеєр](#pipeline)
    - [Sleep](#sleep)
    - [Timebox](#timebox)
    - [URI](#uri)

<a name="introduction"></a>
## Вступ

Laravel містить чимало глобальних «хелперів» - PHP-функцій. Багато з них використовує сам фреймворк; проте ви вільні користуватися ними і у власних застосунках, якщо вважаєте їх зручними.

<a name="available-methods"></a>
## Доступні методи

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
</style>

<a name="arrays-and-objects-method-list"></a>
### Масиви та об'єкти

<div class="collection-method-list" markdown="1">

[Arr::accessible](#method-array-accessible)
[Arr::add](#method-array-add)
[Arr::array](#method-array-array)
[Arr::boolean](#method-array-boolean)
[Arr::collapse](#method-array-collapse)
[Arr::crossJoin](#method-array-crossjoin)
[Arr::divide](#method-array-divide)
[Arr::dot](#method-array-dot)
[Arr::every](#method-array-every)
[Arr::except](#method-array-except)
[Arr::exceptValues](#method-array-except-values)
[Arr::exists](#method-array-exists)
[Arr::first](#method-array-first)
[Arr::flatten](#method-array-flatten)
[Arr::float](#method-array-float)
[Arr::forget](#method-array-forget)
[Arr::from](#method-array-from)
[Arr::get](#method-array-get)
[Arr::has](#method-array-has)
[Arr::hasAll](#method-array-hasall)
[Arr::hasAny](#method-array-hasany)
[Arr::integer](#method-array-integer)
[Arr::isAssoc](#method-array-isassoc)
[Arr::isList](#method-array-islist)
[Arr::join](#method-array-join)
[Arr::keyBy](#method-array-keyby)
[Arr::last](#method-array-last)
[Arr::map](#method-array-map)
[Arr::mapSpread](#method-array-map-spread)
[Arr::mapWithKeys](#method-array-map-with-keys)
[Arr::only](#method-array-only)
[Arr::onlyValues](#method-array-only-values)
[Arr::partition](#method-array-partition)
[Arr::pluck](#method-array-pluck)
[Arr::prepend](#method-array-prepend)
[Arr::prependKeysWith](#method-array-prependkeyswith)
[Arr::pull](#method-array-pull)
[Arr::push](#method-array-push)
[Arr::query](#method-array-query)
[Arr::random](#method-array-random)
[Arr::reject](#method-array-reject)
[Arr::select](#method-array-select)
[Arr::set](#method-array-set)
[Arr::shuffle](#method-array-shuffle)
[Arr::sole](#method-array-sole)
[Arr::some](#method-array-some)
[Arr::sort](#method-array-sort)
[Arr::sortDesc](#method-array-sort-desc)
[Arr::sortRecursive](#method-array-sort-recursive)
[Arr::string](#method-array-string)
[Arr::take](#method-array-take)
[Arr::toCssClasses](#method-array-to-css-classes)
[Arr::toCssStyles](#method-array-to-css-styles)
[Arr::undot](#method-array-undot)
[Arr::where](#method-array-where)
[Arr::whereNotNull](#method-array-where-not-null)
[Arr::wrap](#method-array-wrap)
[data_fill](#method-data-fill)
[data_get](#method-data-get)
[data_set](#method-data-set)
[data_forget](#method-data-forget)
[head](#method-head)
[last](#method-last)
</div>

<a name="numbers-method-list"></a>
### Числа

<div class="collection-method-list" markdown="1">

[Number::abbreviate](#method-number-abbreviate)
[Number::clamp](#method-number-clamp)
[Number::currency](#method-number-currency)
[Number::defaultCurrency](#method-default-currency)
[Number::defaultLocale](#method-default-locale)
[Number::fileSize](#method-number-file-size)
[Number::forHumans](#method-number-for-humans)
[Number::format](#method-number-format)
[Number::ordinal](#method-number-ordinal)
[Number::pairs](#method-number-pairs)
[Number::parse](#method-number-parse)
[Number::parseInt](#method-number-parse-int)
[Number::parseFloat](#method-number-parse-float)
[Number::percentage](#method-number-percentage)
[Number::spell](#method-number-spell)
[Number::spellOrdinal](#method-number-spell-ordinal)
[Number::trim](#method-number-trim)
[Number::useLocale](#method-number-use-locale)
[Number::withLocale](#method-number-with-locale)
[Number::useCurrency](#method-number-use-currency)
[Number::withCurrency](#method-number-with-currency)

</div>

<a name="paths-method-list"></a>
### Шляхи

<div class="collection-method-list" markdown="1">

[app_path](#method-app-path)
[base_path](#method-base-path)
[config_path](#method-config-path)
[database_path](#method-database-path)
[lang_path](#method-lang-path)
[public_path](#method-public-path)
[resource_path](#method-resource-path)
[storage_path](#method-storage-path)

</div>

<a name="urls-method-list"></a>
### URL

<div class="collection-method-list" markdown="1">

[action](#method-action)
[asset](#method-asset)
[route](#method-route)
[secure_asset](#method-secure-asset)
[secure_url](#method-secure-url)
[to_action](#method-to-action)
[to_route](#method-to-route)
[uri](#method-uri)
[url](#method-url)

</div>

<a name="miscellaneous-method-list"></a>
### Різне

<div class="collection-method-list" markdown="1">

[abort](#method-abort)
[abort_if](#method-abort-if)
[abort_unless](#method-abort-unless)
[app](#method-app)
[auth](#method-auth)
[back](#method-back)
[bcrypt](#method-bcrypt)
[blank](#method-blank)
[broadcast](#method-broadcast)
[broadcast_if](#method-broadcast-if)
[broadcast_unless](#method-broadcast-unless)
[cache](#method-cache)
[class_uses_recursive](#method-class-uses-recursive)
[collect](#method-collect)
[config](#method-config)
[context](#method-context)
[cookie](#method-cookie)
[csrf_field](#method-csrf-field)
[csrf_token](#method-csrf-token)
[decrypt](#method-decrypt)
[dd](#method-dd)
[dispatch](#method-dispatch)
[dispatch_sync](#method-dispatch-sync)
[dump](#method-dump)
[encrypt](#method-encrypt)
[env](#method-env)
[event](#method-event)
[fake](#method-fake)
[filled](#method-filled)
[info](#method-info)
[literal](#method-literal)
[logger](#method-logger)
[method_field](#method-method-field)
[now](#method-now)
[old](#method-old)
[once](#method-once)
[optional](#method-optional)
[policy](#method-policy)
[redirect](#method-redirect)
[report](#method-report)
[report_if](#method-report-if)
[report_unless](#method-report-unless)
[request](#method-request)
[rescue](#method-rescue)
[resolve](#method-resolve)
[response](#method-response)
[retry](#method-retry)
[session](#method-session)
[tap](#method-tap)
[throw_if](#method-throw-if)
[throw_unless](#method-throw-unless)
[today](#method-today)
[trait_uses_recursive](#method-trait-uses-recursive)
[transform](#method-transform)
[validator](#method-validator)
[value](#method-value)
[view](#method-view)
[with](#method-with)
[when](#method-when)

</div>

<a name="arrays"></a>
## Масиви та об'єкти

<a name="method-array-accessible"></a>
#### `Arr::accessible()` {.collection-method .first-collection-method}

Метод `Arr::accessible` визначає, чи є задане значення доступним як масив:

```php
use Illuminate\Support\Arr;
use Illuminate\Support\Collection;

$isAccessible = Arr::accessible(['a' => 1, 'b' => 2]);

// true

$isAccessible = Arr::accessible(new Collection);

// true

$isAccessible = Arr::accessible('abc');

// false

$isAccessible = Arr::accessible(new stdClass);

// false
```

<a name="method-array-add"></a>
#### `Arr::add()` {.collection-method}

Метод `Arr::add` додає до масиву задану пару ключ / значення, якщо такого ключа в масиві ще немає або він має значення `null`:

```php
use Illuminate\Support\Arr;

$array = Arr::add(['name' => 'Desk'], 'price', 100);

// ['name' => 'Desk', 'price' => 100]

$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-array"></a>
#### `Arr::array()` {.collection-method}

Метод `Arr::array` дістає значення з глибоко вкладеного масиву за «крапковою» нотацією (так само, як [Arr::get()](#method-array-get)), але викидає `InvalidArgumentException`, якщо запитане значення не є `array`:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$value = Arr::array($array, 'languages');

// ['PHP', 'Ruby']

$value = Arr::array($array, 'name');

// throws InvalidArgumentException
```

<a name="method-array-boolean"></a>
#### `Arr::boolean()` {.collection-method}

Метод `Arr::boolean` дістає значення з глибоко вкладеного масиву за «крапковою» нотацією (так само, як [Arr::get()](#method-array-get)), але викидає `InvalidArgumentException`, якщо запитане значення не є `boolean`:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'available' => true];

$value = Arr::boolean($array, 'available');

// true

$value = Arr::boolean($array, 'name');

// throws InvalidArgumentException
```


<a name="method-array-collapse"></a>
#### `Arr::collapse()` {.collection-method}

Метод `Arr::collapse` згортає масив масивів або колекцій в один масив:

```php
use Illuminate\Support\Arr;

$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-array-crossjoin"></a>
#### `Arr::crossJoin()` {.collection-method}

Метод `Arr::crossJoin` перехресно поєднує задані масиви, повертаючи декартів добуток з усіма можливими комбінаціями:

```php
use Illuminate\Support\Arr;

$matrix = Arr::crossJoin([1, 2], ['a', 'b']);

/*
    [
        [1, 'a'],
        [1, 'b'],
        [2, 'a'],
        [2, 'b'],
    ]
*/

$matrix = Arr::crossJoin([1, 2], ['a', 'b'], ['I', 'II']);

/*
    [
        [1, 'a', 'I'],
        [1, 'a', 'II'],
        [1, 'b', 'I'],
        [1, 'b', 'II'],
        [2, 'a', 'I'],
        [2, 'a', 'II'],
        [2, 'b', 'I'],
        [2, 'b', 'II'],
    ]
*/
```

<a name="method-array-divide"></a>
#### `Arr::divide()` {.collection-method}

Метод `Arr::divide` повертає два масиви: один з ключами, другий зі значеннями заданого масиву:

```php
use Illuminate\Support\Arr;

[$keys, $values] = Arr::divide(['name' => 'Desk']);

// $keys: ['name']

// $values: ['Desk']
```

<a name="method-array-dot"></a>
#### `Arr::dot()` {.collection-method}

Метод `Arr::dot` сплющує багатовимірний масив в одновимірний, використовуючи «крапкову» нотацію для позначення вкладеності:

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$flattened = Arr::dot($array);

// ['products.desk.price' => 100]
```

<a name="method-array-every"></a>
#### `Arr::every()` {.collection-method}

Метод `Arr::every` переконується, що всі значення масиву проходять заданий тест:

```php
use Illuminate\Support\Arr;

$array = [1, 2, 3];

Arr::every($array, fn ($i) => $i > 0);

// true

Arr::every($array, fn ($i) => $i > 2);

// false
```

<a name="method-array-except"></a>
#### `Arr::except()` {.collection-method}

Метод `Arr::except` вилучає з масиву задані пари ключ / значення:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$filtered = Arr::except($array, ['price']);

// ['name' => 'Desk']
```

<a name="method-array-except-values"></a>
#### `Arr::exceptValues()` {.collection-method}

Метод `Arr::exceptValues` вилучає з масиву вказані значення:

```php
use Illuminate\Support\Arr;

$array = ['foo', 'bar', 'baz', 'qux'];

$filtered = Arr::exceptValues($array, ['foo', 'baz']);

// ['bar', 'qux']
```

Ви також можете передати `true` в аргумент `strict`, щоб під час фільтрування використовувати строге порівняння типів:

```php
use Illuminate\Support\Arr;

$array = [1, '1', 2, '2'];

$filtered = Arr::exceptValues($array, [1, 2], strict: true);

// ['1', '2']
```

<a name="method-array-exists"></a>
#### `Arr::exists()` {.collection-method}

Метод `Arr::exists` перевіряє, чи існує заданий ключ у переданому масиві:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'John Doe', 'age' => 17];

$exists = Arr::exists($array, 'name');

// true

$exists = Arr::exists($array, 'salary');

// false
```

<a name="method-array-first"></a>
#### `Arr::first()` {.collection-method}

Метод `Arr::first` повертає перший елемент масиву, який проходить заданий тест:

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300];

$first = Arr::first($array, function (int $value, int $key) {
    return $value >= 150;
});

// 200
```

Третім параметром методу можна передати значення за замовчуванням. Його буде повернуто, якщо жодне значення не пройде тест:

```php
use Illuminate\Support\Arr;

$first = Arr::first($array, $callback, $default);
```

<a name="method-array-flatten"></a>
#### `Arr::flatten()` {.collection-method}

Метод `Arr::flatten` сплющує багатовимірний масив в одновимірний:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$flattened = Arr::flatten($array);

// ['Joe', 'PHP', 'Ruby']
```

<a name="method-array-float"></a>
#### `Arr::float()` {.collection-method}

Метод `Arr::float` дістає значення з глибоко вкладеного масиву за «крапковою» нотацією (так само, як [Arr::get()](#method-array-get)), але викидає `InvalidArgumentException`, якщо запитане значення не є `float`:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'balance' => 123.45];

$value = Arr::float($array, 'balance');

// 123.45

$value = Arr::float($array, 'name');

// throws InvalidArgumentException
```

<a name="method-array-forget"></a>
#### `Arr::forget()` {.collection-method}

Метод `Arr::forget` вилучає задані пари ключ / значення з глибоко вкладеного масиву за «крапковою» нотацією:

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::forget($array, 'products.desk');

// ['products' => []]
```

<a name="method-array-from"></a>
#### `Arr::from()` {.collection-method}

Метод `Arr::from` перетворює різні типи вводу на звичайний PHP-масив. Він підтримує низку типів, зокрема масиви, об'єкти та кілька поширених інтерфейсів Laravel - `Arrayable`, `Enumerable`, `Jsonable` та `JsonSerializable`. Крім того, він обробляє екземпляри `Traversable` і `WeakMap`:

```php
use Illuminate\Support\Arr;

Arr::from((object) ['foo' => 'bar']); // ['foo' => 'bar']

class TestJsonableObject implements Jsonable
{
    public function toJson($options = 0)
    {
        return json_encode(['foo' => 'bar']);
    }
}

Arr::from(new TestJsonableObject); // ['foo' => 'bar']
```

<a name="method-array-get"></a>
#### `Arr::get()` {.collection-method}

Метод `Arr::get` дістає значення з глибоко вкладеного масиву за «крапковою» нотацією:

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$price = Arr::get($array, 'products.desk.price');

// 100
```

Метод `Arr::get` також приймає значення за замовчуванням, яке буде повернуто, якщо вказаного ключа в масиві немає:

```php
use Illuminate\Support\Arr;

$discount = Arr::get($array, 'products.desk.discount', 0);

// 0
```

<a name="method-array-has"></a>
#### `Arr::has()` {.collection-method}

Метод `Arr::has` перевіряє, чи існує в масиві заданий елемент або елементи, за «крапковою» нотацією:

```php
use Illuminate\Support\Arr;

$array = ['product' => ['name' => 'Desk', 'price' => 100]];

$contains = Arr::has($array, 'product.name');

// true

$contains = Arr::has($array, ['product.price', 'product.discount']);

// false
```

<a name="method-array-hasall"></a>
#### `Arr::hasAll()` {.collection-method}

Метод `Arr::hasAll` визначає, чи існують у заданому масиві всі вказані ключі, за «крапковою» нотацією:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Taylor', 'language' => 'PHP'];

Arr::hasAll($array, ['name']); // true
Arr::hasAll($array, ['name', 'language']); // true
Arr::hasAll($array, ['name', 'IDE']); // false
```

<a name="method-array-hasany"></a>
#### `Arr::hasAny()` {.collection-method}

Метод `Arr::hasAny` перевіряє, чи існує в масиві хоч один елемент із заданого набору, за «крапковою» нотацією:

```php
use Illuminate\Support\Arr;

$array = ['product' => ['name' => 'Desk', 'price' => 100]];

$contains = Arr::hasAny($array, 'product.name');

// true

$contains = Arr::hasAny($array, ['product.name', 'product.discount']);

// true

$contains = Arr::hasAny($array, ['category', 'product.discount']);

// false
```

<a name="method-array-integer"></a>
#### `Arr::integer()` {.collection-method}

Метод `Arr::integer` дістає значення з глибоко вкладеного масиву за «крапковою» нотацією (так само, як [Arr::get()](#method-array-get)), але викидає `InvalidArgumentException`, якщо запитане значення не є `int`:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'age' => 42];

$value = Arr::integer($array, 'age');

// 42

$value = Arr::integer($array, 'name');

// throws InvalidArgumentException
```

<a name="method-array-isassoc"></a>
#### `Arr::isAssoc()` {.collection-method}

Метод `Arr::isAssoc` повертає `true`, якщо заданий масив є асоціативним. Масив вважається «асоціативним», якщо він не має послідовних числових ключів, що починаються з нуля:

```php
use Illuminate\Support\Arr;

$isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

// true

$isAssoc = Arr::isAssoc([1, 2, 3]);

// false
```

<a name="method-array-islist"></a>
#### `Arr::isList()` {.collection-method}

Метод `Arr::isList` повертає `true`, якщо ключі заданого масиву - послідовні цілі числа, що починаються з нуля:

```php
use Illuminate\Support\Arr;

$isList = Arr::isList(['foo', 'bar', 'baz']);

// true

$isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

// false
```

<a name="method-array-join"></a>
#### `Arr::join()` {.collection-method}

Метод `Arr::join` склеює елементи масиву рядком. Третім аргументом цього методу ви можете вказати рядок, яким приєднується останній елемент масиву:

```php
use Illuminate\Support\Arr;

$array = ['Tailwind', 'Alpine', 'Laravel', 'Livewire'];

$joined = Arr::join($array, ', ');

// Tailwind, Alpine, Laravel, Livewire

$joined = Arr::join($array, ', ', ', and ');

// Tailwind, Alpine, Laravel, and Livewire
```

<a name="method-array-keyby"></a>
#### `Arr::keyBy()` {.collection-method}

Метод `Arr::keyBy` робить заданий ключ ключем масиву. Якщо кілька елементів мають однаковий ключ, у новому масиві залишиться тільки останній:

```php
use Illuminate\Support\Arr;

$array = [
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
];

$keyed = Arr::keyBy($array, 'product_id');

/*
    [
        'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
        'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]
*/
```

<a name="method-array-last"></a>
#### `Arr::last()` {.collection-method}

Метод `Arr::last` повертає останній елемент масиву, який проходить заданий тест:

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function (int $value, int $key) {
    return $value >= 150;
});

// 300
```

Третім аргументом методу можна передати значення за замовчуванням. Його буде повернуто, якщо жодне значення не пройде тест:

```php
use Illuminate\Support\Arr;

$last = Arr::last($array, $callback, $default);
```

<a name="method-array-map"></a>
#### `Arr::map()` {.collection-method}

Метод `Arr::map` проходить масив і передає кожне значення та ключ до заданого колбека. Значення масиву замінюється тим, що повернув колбек:

```php
use Illuminate\Support\Arr;

$array = ['first' => 'james', 'last' => 'kirk'];

$mapped = Arr::map($array, function (string $value, string $key) {
    return ucfirst($value);
});

// ['first' => 'James', 'last' => 'Kirk']
```

<a name="method-array-map-spread"></a>
#### `Arr::mapSpread()` {.collection-method}

Метод `Arr::mapSpread` проходить масив, передаючи значення кожного вкладеного елемента до заданого замикання. Замикання вільне змінити елемент і повернути його, утворюючи так новий масив змінених елементів:

```php
use Illuminate\Support\Arr;

$array = [
    [0, 1],
    [2, 3],
    [4, 5],
    [6, 7],
    [8, 9],
];

$mapped = Arr::mapSpread($array, function (int $even, int $odd) {
    return $even + $odd;
});

/*
    [1, 5, 9, 13, 17]
*/
```

<a name="method-array-map-with-keys"></a>
#### `Arr::mapWithKeys()` {.collection-method}

Метод `Arr::mapWithKeys` проходить масив і передає кожне значення до заданого колбека. Колбек має повернути асоціативний масив з єдиною парою ключ / значення:

```php
use Illuminate\Support\Arr;

$array = [
    [
        'name' => 'John',
        'department' => 'Sales',
        'email' => 'john@example.com',
    ],
    [
        'name' => 'Jane',
        'department' => 'Marketing',
        'email' => 'jane@example.com',
    ]
];

$mapped = Arr::mapWithKeys($array, function (array $item, int $key) {
    return [$item['email'] => $item['name']];
});

/*
    [
        'john@example.com' => 'John',
        'jane@example.com' => 'Jane',
    ]
*/
```

<a name="method-array-only"></a>
#### `Arr::only()` {.collection-method}

Метод `Arr::only` повертає із заданого масиву лише вказані пари ключ / значення:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

$slice = Arr::only($array, ['name', 'price']);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-only-values"></a>
#### `Arr::onlyValues()` {.collection-method}

Метод `Arr::onlyValues` повертає з масиву лише вказані значення:

```php
use Illuminate\Support\Arr;

$array = ['foo', 'bar', 'baz', 'qux'];

$filtered = Arr::onlyValues($array, ['foo', 'baz']);

// ['foo', 'baz']
```

Ви також можете передати `true` в аргумент `strict`, щоб під час фільтрування використовувати строге порівняння типів:

```php
use Illuminate\Support\Arr;

$array = [1, '1', 2, '2'];

$filtered = Arr::onlyValues($array, [1, 2], strict: true);

// [1, 2]
```

<a name="method-array-partition"></a>
#### `Arr::partition()` {.collection-method}

Метод `Arr::partition` можна поєднати з деструктуризацією масивів PHP, щоб відділити елементи, які проходять заданий тест, від тих, які його не проходять:

```php
<?php

use Illuminate\Support\Arr;

$numbers = [1, 2, 3, 4, 5, 6];

[$underThree, $equalOrAboveThree] = Arr::partition($numbers, function (int $i) {
    return $i < 3;
});

dump($underThree);

// [1, 2]

dump($equalOrAboveThree);

// [3, 4, 5, 6]
```

<a name="method-array-pluck"></a>
#### `Arr::pluck()` {.collection-method}

Метод `Arr::pluck` дістає з масиву всі значення за заданим ключем:

```php
use Illuminate\Support\Arr;

$array = [
    ['developer' => ['id' => 1, 'name' => 'Taylor']],
    ['developer' => ['id' => 2, 'name' => 'Abigail']],
];

$names = Arr::pluck($array, 'developer.name');

// ['Taylor', 'Abigail']
```

Ви також можете вказати, за яким ключем має будуватися отриманий список:

```php
use Illuminate\Support\Arr;

$names = Arr::pluck($array, 'developer.name', 'developer.id');

// [1 => 'Taylor', 2 => 'Abigail']
```

<a name="method-array-prepend"></a>
#### `Arr::prepend()` {.collection-method}

Метод `Arr::prepend` додає елемент на початок масиву:

```php
use Illuminate\Support\Arr;

$array = ['one', 'two', 'three', 'four'];

$array = Arr::prepend($array, 'zero');

// ['zero', 'one', 'two', 'three', 'four']
```

За потреби ви можете вказати ключ, який слід використати для значення:

```php
use Illuminate\Support\Arr;

$array = ['price' => 100];

$array = Arr::prepend($array, 'Desk', 'name');

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-prependkeyswith"></a>
#### `Arr::prependKeysWith()` {.collection-method}

Метод `Arr::prependKeysWith` додає заданий префікс до всіх назв ключів асоціативного масиву:

```php
use Illuminate\Support\Arr;

$array = [
    'name' => 'Desk',
    'price' => 100,
];

$keyed = Arr::prependKeysWith($array, 'product.');

/*
    [
        'product.name' => 'Desk',
        'product.price' => 100,
    ]
*/
```

<a name="method-array-pull"></a>
#### `Arr::pull()` {.collection-method}

Метод `Arr::pull` повертає й вилучає з масиву пару ключ / значення:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$name = Arr::pull($array, 'name');

// $name: Desk

// $array: ['price' => 100]
```

Третім аргументом методу можна передати значення за замовчуванням. Його буде повернуто, якщо ключа не існує:

```php
use Illuminate\Support\Arr;

$value = Arr::pull($array, $key, $default);
```

<a name="method-array-push"></a>
#### `Arr::push()` {.collection-method}

Метод `Arr::push` додає елемент до масиву за «крапковою» нотацією. Якщо за заданим ключем масиву немає, його буде створено:

```php
use Illuminate\Support\Arr;

$array = [];

Arr::push($array, 'office.furniture', 'Desk');

// $array: ['office' => ['furniture' => ['Desk']]]
```

<a name="method-array-query"></a>
#### `Arr::query()` {.collection-method}

Метод `Arr::query` перетворює масив на рядок запиту:

```php
use Illuminate\Support\Arr;

$array = [
    'name' => 'Taylor',
    'order' => [
        'column' => 'created_at',
        'direction' => 'desc'
    ]
];

Arr::query($array);

// name=Taylor&order[column]=created_at&order[direction]=desc
```

<a name="method-array-random"></a>
#### `Arr::random()` {.collection-method}

Метод `Arr::random` повертає випадкове значення з масиву:

```php
use Illuminate\Support\Arr;

$array = [1, 2, 3, 4, 5];

$random = Arr::random($array);

// 4 - (retrieved randomly)
```

Необов'язковим другим аргументом ви можете вказати кількість елементів, які слід повернути. Зверніть увагу: якщо передати цей аргумент, буде повернуто масив, навіть коли потрібен лише один елемент:

```php
use Illuminate\Support\Arr;

$items = Arr::random($array, 2);

// [2, 5] - (retrieved randomly)
```

<a name="method-array-reject"></a>
#### `Arr::reject()` {.collection-method}

Метод `Arr::reject` вилучає елементи з масиву за допомогою заданого замикання:

```php
use Illuminate\Support\Arr;

$array = [100, '200', 300, '400', 500];

$filtered = Arr::reject($array, function (string|int $value, int $key) {
    return is_string($value);
});

// [0 => 100, 2 => 300, 4 => 500]
```

<a name="method-array-select"></a>
#### `Arr::select()` {.collection-method}

Метод `Arr::select` вибирає з масиву масив значень:

```php
use Illuminate\Support\Arr;

$array = [
    ['id' => 1, 'name' => 'Desk', 'price' => 200],
    ['id' => 2, 'name' => 'Table', 'price' => 150],
    ['id' => 3, 'name' => 'Chair', 'price' => 300],
];

Arr::select($array, ['name', 'price']);

// [['name' => 'Desk', 'price' => 200], ['name' => 'Table', 'price' => 150], ['name' => 'Chair', 'price' => 300]]
```

<a name="method-array-set"></a>
#### `Arr::set()` {.collection-method}

Метод `Arr::set` встановлює значення в глибоко вкладеному масиві за «крапковою» нотацією:

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::set($array, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<a name="method-array-shuffle"></a>
#### `Arr::shuffle()` {.collection-method}

Метод `Arr::shuffle` випадково перемішує елементи масиву:

```php
use Illuminate\Support\Arr;

$array = Arr::shuffle([1, 2, 3, 4, 5]);

// [3, 2, 5, 1, 4] - (generated randomly)
```

<a name="method-array-sole"></a>
#### `Arr::sole()` {.collection-method}

Метод `Arr::sole` дістає з масиву єдине значення за допомогою заданого замикання. Якщо заданий тест проходить більше ніж одне значення масиву, буде викинуто виняток `Illuminate\Support\MultipleItemsFoundException`. Якщо тест не проходить жодне значення, буде викинуто виняток `Illuminate\Support\ItemNotFoundException`:

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$value = Arr::sole($array, fn (string $value) => $value === 'Desk');

// 'Desk'
```

<a name="method-array-some"></a>
#### `Arr::some()` {.collection-method}

Метод `Arr::some` переконується, що заданий тест проходить щонайменше одне значення масиву:

```php
use Illuminate\Support\Arr;

$array = [1, 2, 3];

Arr::some($array, fn ($i) => $i > 2);

// true
```

<a name="method-array-sort"></a>
#### `Arr::sort()` {.collection-method}

Метод `Arr::sort` сортує масив за його значеннями:

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sort($array);

// ['Chair', 'Desk', 'Table']
```

Ви також можете відсортувати масив за результатами заданого замикання:

```php
use Illuminate\Support\Arr;

$array = [
    ['name' => 'Desk'],
    ['name' => 'Table'],
    ['name' => 'Chair'],
];

$sorted = array_values(Arr::sort($array, function (array $value) {
    return $value['name'];
}));

/*
    [
        ['name' => 'Chair'],
        ['name' => 'Desk'],
        ['name' => 'Table'],
    ]
*/
```

<a name="method-array-sort-desc"></a>
#### `Arr::sortDesc()` {.collection-method}

Метод `Arr::sortDesc` сортує масив за його значеннями у спадному порядку:

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sortDesc($array);

// ['Table', 'Desk', 'Chair']
```

Ви також можете відсортувати масив за результатами заданого замикання:

```php
use Illuminate\Support\Arr;

$array = [
    ['name' => 'Desk'],
    ['name' => 'Table'],
    ['name' => 'Chair'],
];

$sorted = array_values(Arr::sortDesc($array, function (array $value) {
    return $value['name'];
}));

/*
    [
        ['name' => 'Table'],
        ['name' => 'Desk'],
        ['name' => 'Chair'],
    ]
*/
```

<a name="method-array-sort-recursive"></a>
#### `Arr::sortRecursive()` {.collection-method}

Метод `Arr::sortRecursive` рекурсивно сортує масив, використовуючи функцію `sort` для підмасивів з числовими індексами та функцію `ksort` для асоціативних підмасивів:

```php
use Illuminate\Support\Arr;

$array = [
    ['Roman', 'Taylor', 'Li'],
    ['PHP', 'Ruby', 'JavaScript'],
    ['one' => 1, 'two' => 2, 'three' => 3],
];

$sorted = Arr::sortRecursive($array);

/*
    [
        ['JavaScript', 'PHP', 'Ruby'],
        ['one' => 1, 'three' => 3, 'two' => 2],
        ['Li', 'Roman', 'Taylor'],
    ]
*/
```

Якщо ви хочете отримати результати у спадному порядку, скористайтеся методом `Arr::sortRecursiveDesc`.

```php
$sorted = Arr::sortRecursiveDesc($array);
```

<a name="method-array-string"></a>
#### `Arr::string()` {.collection-method}

Метод `Arr::string` дістає значення з глибоко вкладеного масиву за «крапковою» нотацією (так само, як [Arr::get()](#method-array-get)), але викидає `InvalidArgumentException`, якщо запитане значення не є `string`:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$value = Arr::string($array, 'name');

// Joe

$value = Arr::string($array, 'languages');

// throws InvalidArgumentException
```

<a name="method-array-take"></a>
#### `Arr::take()` {.collection-method}

Метод `Arr::take` повертає новий масив із вказаною кількістю елементів:

```php
use Illuminate\Support\Arr;

$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, 3);

// [0, 1, 2]
```

Ви також можете передати від'ємне ціле число, щоб узяти вказану кількість елементів з кінця масиву:

```php
$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, -2);

// [4, 5]
```

<a name="method-array-to-css-classes"></a>
#### `Arr::toCssClasses()` {.collection-method}

Метод `Arr::toCssClasses` умовно збирає рядок CSS-класів. Метод приймає масив класів, де ключ масиву містить клас або класи, які ви хочете додати, а значення є булевим виразом. Якщо елемент масиву має числовий ключ, він завжди потрапить до згенерованого списку класів:

```php
use Illuminate\Support\Arr;

$isActive = false;
$hasError = true;

$array = ['p-4', 'font-bold' => $isActive, 'bg-red' => $hasError];

$classes = Arr::toCssClasses($array);

/*
    'p-4 bg-red'
*/
```

<a name="method-array-to-css-styles"></a>
#### `Arr::toCssStyles()` {.collection-method}

Метод `Arr::toCssStyles` умовно збирає рядок CSS-стилів. Метод приймає масив CSS-оголошень, де ключ масиву містить CSS-оголошення, яке ви хочете додати, а значення є булевим виразом. Якщо елемент масиву має числовий ключ, він завжди потрапить до зібраного рядка CSS-стилів:

```php
use Illuminate\Support\Arr;

$hasColor = true;

$array = ['background-color: blue', 'color: blue' => $hasColor];

$classes = Arr::toCssStyles($array);

/*
    'background-color: blue; color: blue;'
*/
```

Цей метод лежить в основі можливості Laravel [зливати класи з мішком атрибутів Blade-компонента](/docs/{{version}}/blade#conditionally-merge-classes), а також [директиви Blade](/docs/{{version}}/blade#conditional-classes) `@class`.

<a name="method-array-undot"></a>
#### `Arr::undot()` {.collection-method}

Метод `Arr::undot` розгортає одновимірний масив з «крапковою» нотацією на багатовимірний:

```php
use Illuminate\Support\Arr;

$array = [
    'user.name' => 'Kevin Malone',
    'user.occupation' => 'Accountant',
];

$array = Arr::undot($array);

// ['user' => ['name' => 'Kevin Malone', 'occupation' => 'Accountant']]
```

<a name="method-array-where"></a>
#### `Arr::where()` {.collection-method}

Метод `Arr::where` фільтрує масив за допомогою заданого замикання:

```php
use Illuminate\Support\Arr;

$array = [100, '200', 300, '400', 500];

$filtered = Arr::where($array, function (string|int $value, int $key) {
    return is_string($value);
});

// [1 => '200', 3 => '400']
```

<a name="method-array-where-not-null"></a>
#### `Arr::whereNotNull()` {.collection-method}

Метод `Arr::whereNotNull` вилучає із заданого масиву всі значення `null`:

```php
use Illuminate\Support\Arr;

$array = [0, null];

$filtered = Arr::whereNotNull($array);

// [0 => 0]
```

<a name="method-array-wrap"></a>
#### `Arr::wrap()` {.collection-method}

Метод `Arr::wrap` загортає задане значення в масив. Якщо задане значення вже є масивом, його буде повернуто без змін:

```php
use Illuminate\Support\Arr;

$string = 'Laravel';

$array = Arr::wrap($string);

// ['Laravel']
```

Якщо задане значення - `null`, буде повернуто порожній масив:

```php
use Illuminate\Support\Arr;

$array = Arr::wrap(null);

// []
```

<a name="method-data-fill"></a>
#### `data_fill()` {.collection-method}

Функція `data_fill` встановлює відсутнє значення у вкладеному масиві чи об'єкті за «крапковою» нотацією:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_fill($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 100]]]

data_fill($data, 'products.desk.discount', 10);

// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

Ця функція також приймає зірочки як підстановки й заповнить ціль відповідно:

```php
$data = [
    'products' => [
        ['name' => 'Desk 1', 'price' => 100],
        ['name' => 'Desk 2'],
    ],
];

data_fill($data, 'products.*.price', 200);

/*
    [
        'products' => [
            ['name' => 'Desk 1', 'price' => 100],
            ['name' => 'Desk 2', 'price' => 200],
        ],
    ]
*/
```

<a name="method-data-get"></a>
#### `data_get()` {.collection-method}

Функція `data_get` дістає значення з вкладеного масиву чи об'єкта за «крапковою» нотацією:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

$price = data_get($data, 'products.desk.price');

// 100
```

Функція `data_get` також приймає значення за замовчуванням, яке буде повернуто, якщо вказаного ключа не знайдено:

```php
$discount = data_get($data, 'products.desk.discount', 0);

// 0
```

Функція також приймає підстановки у вигляді зірочок, які можуть вказувати на будь-який ключ масиву чи об'єкта:

```php
$data = [
    'product-one' => ['name' => 'Desk 1', 'price' => 100],
    'product-two' => ['name' => 'Desk 2', 'price' => 150],
];

data_get($data, '*.name');

// ['Desk 1', 'Desk 2'];
```

Плейсхолдери `{first}` та `{last}` дозволяють дістати перший чи останній елементи масиву:

```php
$flight = [
    'segments' => [
        ['from' => 'LHR', 'departure' => '9:00', 'to' => 'IST', 'arrival' => '15:00'],
        ['from' => 'IST', 'departure' => '16:00', 'to' => 'PKX', 'arrival' => '20:00'],
    ],
];

data_get($flight, 'segments.{first}.arrival');

// 15:00
```

<a name="method-data-set"></a>
#### `data_set()` {.collection-method}

Функція `data_set` встановлює значення у вкладеному масиві чи об'єкті за «крапковою» нотацією:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

Ця функція також приймає підстановки у вигляді зірочок і встановить значення в цілі відповідно:

```php
$data = [
    'products' => [
        ['name' => 'Desk 1', 'price' => 100],
        ['name' => 'Desk 2', 'price' => 150],
    ],
];

data_set($data, 'products.*.price', 200);

/*
    [
        'products' => [
            ['name' => 'Desk 1', 'price' => 200],
            ['name' => 'Desk 2', 'price' => 200],
        ],
    ]
*/
```

За замовчуванням будь-які наявні значення перезаписуються. Якщо ви хочете встановити значення, лише коли його ще немає, передайте четвертим аргументом функції `false`:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200, overwrite: false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-data-forget"></a>
#### `data_forget()` {.collection-method}

Функція `data_forget` вилучає значення з вкладеного масиву чи об'єкта за «крапковою» нотацією:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_forget($data, 'products.desk.price');

// ['products' => ['desk' => []]]
```

Ця функція також приймає підстановки у вигляді зірочок і вилучить значення в цілі відповідно:

```php
$data = [
    'products' => [
        ['name' => 'Desk 1', 'price' => 100],
        ['name' => 'Desk 2', 'price' => 150],
    ],
];

data_forget($data, 'products.*.price');

/*
    [
        'products' => [
            ['name' => 'Desk 1'],
            ['name' => 'Desk 2'],
        ],
    ]
*/
```

<a name="method-head"></a>
#### `head()` {.collection-method}

Функція `head` повертає перший елемент заданого масиву. Якщо масив порожній, буде повернуто `false`:

```php
$array = [100, 200, 300];

$first = head($array);

// 100
```

<a name="method-last"></a>
#### `last()` {.collection-method}

Функція `last` повертає останній елемент заданого масиву. Якщо масив порожній, буде повернуто `false`:

```php
$array = [100, 200, 300];

$last = last($array);

// 300
```

<a name="numbers"></a>
## Числа

<a name="method-number-abbreviate"></a>
#### `Number::abbreviate()` {.collection-method}

Метод `Number::abbreviate` повертає зручний для читання формат переданого числового значення зі скороченням одиниць:

```php
use Illuminate\Support\Number;

$number = Number::abbreviate(1000);

// 1K

$number = Number::abbreviate(489939);

// 490K

$number = Number::abbreviate(1230000, precision: 2);

// 1.23M
```

<a name="method-number-clamp"></a>
#### `Number::clamp()` {.collection-method}

Метод `Number::clamp` гарантує, що задане число лишається у вказаному діапазоні. Якщо число менше за мінімум, повертається мінімальне значення. Якщо число більше за максимум, повертається максимальне значення:

```php
use Illuminate\Support\Number;

$number = Number::clamp(105, min: 10, max: 100);

// 100

$number = Number::clamp(5, min: 10, max: 100);

// 10

$number = Number::clamp(10, min: 10, max: 100);

// 10

$number = Number::clamp(20, min: 10, max: 100);

// 20
```

<a name="method-number-currency"></a>
#### `Number::currency()` {.collection-method}

Метод `Number::currency` повертає рядкове представлення заданого значення у вигляді валюти:

```php
use Illuminate\Support\Number;

$currency = Number::currency(1000);

// $1,000.00

$currency = Number::currency(1000, in: 'EUR');

// €1,000.00

$currency = Number::currency(1000, in: 'EUR', locale: 'de');

// 1.000,00 €

$currency = Number::currency(1000, in: 'EUR', locale: 'de', precision: 0);

// 1.000 €
```

<a name="method-default-currency"></a>
#### `Number::defaultCurrency()` {.collection-method}

Метод `Number::defaultCurrency` повертає валюту за замовчуванням, яку використовує клас `Number`:

```php
use Illuminate\Support\Number;

$currency = Number::defaultCurrency();

// USD
```

<a name="method-default-locale"></a>
#### `Number::defaultLocale()` {.collection-method}

Метод `Number::defaultLocale` повертає локаль за замовчуванням, яку використовує клас `Number`:

```php
use Illuminate\Support\Number;

$locale = Number::defaultLocale();

// en
```

<a name="method-number-file-size"></a>
#### `Number::fileSize()` {.collection-method}

Метод `Number::fileSize` повертає рядкове представлення заданої кількості байтів у вигляді розміру файлу:

```php
use Illuminate\Support\Number;

$size = Number::fileSize(1024);

// 1 KB

$size = Number::fileSize(1024 * 1024);

// 1 MB

$size = Number::fileSize(1024, precision: 2);

// 1.00 KB
```

<a name="method-number-for-humans"></a>
#### `Number::forHumans()` {.collection-method}

Метод `Number::forHumans` повертає зручний для читання формат переданого числового значення:

```php
use Illuminate\Support\Number;

$number = Number::forHumans(1000);

// 1 thousand

$number = Number::forHumans(489939);

// 490 thousand

$number = Number::forHumans(1230000, precision: 2);

// 1.23 million
```

<a name="method-number-format"></a>
#### `Number::format()` {.collection-method}

Метод `Number::format` форматує задане число в рядок відповідно до локалі:

```php
use Illuminate\Support\Number;

$number = Number::format(100000);

// 100,000

$number = Number::format(100000, precision: 2);

// 100,000.00

$number = Number::format(100000.123, maxPrecision: 2);

// 100,000.12

$number = Number::format(100000, locale: 'de');

// 100.000
```

<a name="method-number-ordinal"></a>
#### `Number::ordinal()` {.collection-method}

Метод `Number::ordinal` повертає порядкове представлення числа:

```php
use Illuminate\Support\Number;

$number = Number::ordinal(1);

// 1st

$number = Number::ordinal(2);

// 2nd

$number = Number::ordinal(21);

// 21st
```

<a name="method-number-pairs"></a>
#### `Number::pairs()` {.collection-method}

Метод `Number::pairs` генерує масив пар чисел (піддіапазонів) на основі заданого діапазону й кроку. Цей метод стане в пригоді, коли треба розділити великий діапазон чисел на менші, зручні піддіапазони - наприклад, для пагінації чи пакетної обробки. Метод `pairs` повертає масив масивів, де кожен внутрішній масив представляє пару (піддіапазон) чисел:

```php
use Illuminate\Support\Number;

$result = Number::pairs(25, 10);

// [[0, 9], [10, 19], [20, 25]]

$result = Number::pairs(25, 10, offset: 0);

// [[0, 10], [10, 20], [20, 25]]
```

<a name="method-number-parse"></a>
#### `Number::parse()` {.collection-method}

Метод `Number::parse` розбирає локалізований числовий рядок за допомогою PHP-класу `NumberFormatter`:

```php
use Illuminate\Support\Number;

$result = Number::parse('10,123', locale: 'en');

// 10123.0

$result = Number::parse('10,123', locale: 'fr');

// 10.123
```

<a name="method-number-parse-int"></a>
#### `Number::parseInt()` {.collection-method}

Метод `Number::parseInt` розбирає рядок на ціле число відповідно до вказаної локалі:

```php
use Illuminate\Support\Number;

$result = Number::parseInt('10.123');

// (int) 10

$result = Number::parseInt('10,123', locale: 'fr');

// (int) 10
```

<a name="method-number-parse-float"></a>
#### `Number::parseFloat()` {.collection-method}

Метод `Number::parseFloat` розбирає рядок на число з рухомою комою відповідно до вказаної локалі:

```php
use Illuminate\Support\Number;

$result = Number::parseFloat('10');

// (float) 10.0

$result = Number::parseFloat('10', locale: 'fr');

// (float) 10.0
```

<a name="method-number-percentage"></a>
#### `Number::percentage()` {.collection-method}

Метод `Number::percentage` повертає рядкове представлення заданого значення у вигляді відсотка:

```php
use Illuminate\Support\Number;

$percentage = Number::percentage(10);

// 10%

$percentage = Number::percentage(10, precision: 2);

// 10.00%

$percentage = Number::percentage(10.123, maxPrecision: 2);

// 10.12%

$percentage = Number::percentage(10, precision: 2, locale: 'de');

// 10,00%
```

<a name="method-number-spell"></a>
#### `Number::spell()` {.collection-method}

Метод `Number::spell` перетворює задане число на рядок зі слів:

```php
use Illuminate\Support\Number;

$number = Number::spell(102);

// one hundred and two

$number = Number::spell(88, locale: 'fr');

// quatre-vingt-huit
```

Аргумент `after` дозволяє вказати значення, після якого всі числа слід писати словами:

```php
$number = Number::spell(10, after: 10);

// 10

$number = Number::spell(11, after: 10);

// eleven
```

Аргумент `until` дозволяє вказати значення, до якого всі числа слід писати словами:

```php
$number = Number::spell(5, until: 10);

// five

$number = Number::spell(10, until: 10);

// 10
```

<a name="method-number-spell-ordinal"></a>
#### `Number::spellOrdinal()` {.collection-method}

Метод `Number::spellOrdinal` повертає порядкове представлення числа у вигляді рядка зі слів:

```php
use Illuminate\Support\Number;

$number = Number::spellOrdinal(1);

// first

$number = Number::spellOrdinal(2);

// second

$number = Number::spellOrdinal(21);

// twenty-first
```

<a name="method-number-trim"></a>
#### `Number::trim()` {.collection-method}

Метод `Number::trim` вилучає всі кінцеві нулі після десяткової крапки заданого числа:

```php
use Illuminate\Support\Number;

$number = Number::trim(12.0);

// 12

$number = Number::trim(12.30);

// 12.3
```

<a name="method-number-use-locale"></a>
#### `Number::useLocale()` {.collection-method}

Метод `Number::useLocale` глобально задає локаль чисел за замовчуванням, що впливає на форматування чисел і валюти під час наступних викликів методів класу `Number`:

```php
use Illuminate\Support\Number;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Number::useLocale('de');
}
```

<a name="method-number-with-locale"></a>
#### `Number::withLocale()` {.collection-method}

Метод `Number::withLocale` виконує задане замикання із вказаною локаллю, а після виконання колбека відновлює оригінальну локаль:

```php
use Illuminate\Support\Number;

$number = Number::withLocale('de', function () {
    return Number::format(1500);
});
```

<a name="method-number-use-currency"></a>
#### `Number::useCurrency()` {.collection-method}

Метод `Number::useCurrency` глобально задає валюту чисел за замовчуванням, що впливає на форматування валюти під час наступних викликів методів класу `Number`:

```php
use Illuminate\Support\Number;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Number::useCurrency('GBP');
}
```

<a name="method-number-with-currency"></a>
#### `Number::withCurrency()` {.collection-method}

Метод `Number::withCurrency` виконує задане замикання із вказаною валютою, а після виконання колбека відновлює оригінальну валюту:

```php
use Illuminate\Support\Number;

$number = Number::withCurrency('GBP', function () {
    // ...
});
```

<a name="paths"></a>
## Шляхи

<a name="method-app-path"></a>
#### `app_path()` {.collection-method}

Функція `app_path` повертає повний шлях до каталогу `app` вашого застосунку. Ви також можете скористатися функцією `app_path`, щоб згенерувати повний шлях до файлу відносно каталогу застосунку:

```php
$path = app_path();

$path = app_path('Http/Controllers/Controller.php');
```

<a name="method-base-path"></a>
#### `base_path()` {.collection-method}

Функція `base_path` повертає повний шлях до кореневого каталогу вашого застосунку. Ви також можете скористатися функцією `base_path`, щоб згенерувати повний шлях до заданого файлу відносно кореня проєкту:

```php
$path = base_path();

$path = base_path('vendor/bin');
```

<a name="method-config-path"></a>
#### `config_path()` {.collection-method}

Функція `config_path` повертає повний шлях до каталогу `config` вашого застосунку. Ви також можете скористатися функцією `config_path`, щоб згенерувати повний шлях до заданого файлу в каталозі конфігурації застосунку:

```php
$path = config_path();

$path = config_path('app.php');
```

<a name="method-database-path"></a>
#### `database_path()` {.collection-method}

Функція `database_path` повертає повний шлях до каталогу `database` вашого застосунку. Ви також можете скористатися функцією `database_path`, щоб згенерувати повний шлях до заданого файлу в каталозі бази даних:

```php
$path = database_path();

$path = database_path('factories/UserFactory.php');
```

<a name="method-lang-path"></a>
#### `lang_path()` {.collection-method}

Функція `lang_path` повертає повний шлях до каталогу `lang` вашого застосунку. Ви також можете скористатися функцією `lang_path`, щоб згенерувати повний шлях до заданого файлу в цьому каталозі:

```php
$path = lang_path();

$path = lang_path('en/messages.php');
```

> [!NOTE]
> За замовчуванням каркас застосунку Laravel не містить каталогу `lang`. Якщо ви хочете налаштувати мовні файли Laravel, опублікуйте їх командою Artisan `lang:publish`.

<a name="method-public-path"></a>
#### `public_path()` {.collection-method}

Функція `public_path` повертає повний шлях до каталогу `public` вашого застосунку. Ви також можете скористатися функцією `public_path`, щоб згенерувати повний шлях до заданого файлу в каталозі public:

```php
$path = public_path();

$path = public_path('css/app.css');
```

<a name="method-resource-path"></a>
#### `resource_path()` {.collection-method}

Функція `resource_path` повертає повний шлях до каталогу `resources` вашого застосунку. Ви також можете скористатися функцією `resource_path`, щоб згенерувати повний шлях до заданого файлу в каталозі resources:

```php
$path = resource_path();

$path = resource_path('sass/app.scss');
```

<a name="method-storage-path"></a>
#### `storage_path()` {.collection-method}

Функція `storage_path` повертає повний шлях до каталогу `storage` вашого застосунку. Ви також можете скористатися функцією `storage_path`, щоб згенерувати повний шлях до заданого файлу в каталозі storage:

```php
$path = storage_path();

$path = storage_path('app/file.txt');
```

<a name="urls"></a>
## URL

<a name="method-action"></a>
#### `action()` {.collection-method}

Функція `action` генерує URL для заданої дії контролера:

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

Якщо метод приймає параметри маршруту, передайте їх другим аргументом:

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="method-asset"></a>
#### `asset()` {.collection-method}

Функція `asset` генерує URL для ресурсу, використовуючи поточну схему запиту (HTTP чи HTTPS):

```php
$url = asset('img/photo.jpg');
```

Ви можете налаштувати хост URL ресурсів, задавши змінну `ASSET_URL` у файлі `.env`. Це стане в пригоді, якщо ви розміщуєте ресурси на зовнішньому сервісі на кшталт Amazon S3 чи іншого CDN:

```php
// ASSET_URL=http://example.com/assets

$url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg
```

<a name="method-route"></a>
#### `route()` {.collection-method}

Функція `route` генерує URL для заданого [іменованого маршруту](/docs/{{version}}/routing#named-routes):

```php
$url = route('route.name');
```

Якщо маршрут приймає параметри, передайте їх другим аргументом функції:

```php
$url = route('route.name', ['id' => 1]);
```

За замовчуванням функція `route` генерує абсолютний URL. Якщо ви хочете згенерувати відносний URL, передайте третім аргументом функції `false`:

```php
$url = route('route.name', ['id' => 1], false);
```

<a name="method-secure-asset"></a>
#### `secure_asset()` {.collection-method}

Функція `secure_asset` генерує URL для ресурсу через HTTPS:

```php
$url = secure_asset('img/photo.jpg');
```

<a name="method-secure-url"></a>
#### `secure_url()` {.collection-method}

Функція `secure_url` генерує повний HTTPS-URL до заданого шляху. Додаткові сегменти URL можна передати другим аргументом функції:

```php
$url = secure_url('user/profile');

$url = secure_url('user/profile', [1]);
```

<a name="method-to-action"></a>
#### `to_action()` {.collection-method}

Функція `to_action` генерує [HTTP-відповідь із перенаправленням](/docs/{{version}}/responses#redirects) для заданої дії контролера:

```php
use App\Http\Controllers\UserController;

return to_action([UserController::class, 'show'], ['user' => 1]);
```

За потреби ви можете передати третім і четвертим аргументами методу `to_action` HTTP-статус, який слід призначити перенаправленню, і будь-які додаткові заголовки відповіді:

```php
return to_action(
    [UserController::class, 'show'],
    ['user' => 1],
    302,
    ['X-Framework' => 'Laravel']
);
```

<a name="method-to-route"></a>
#### `to_route()` {.collection-method}

Функція `to_route` генерує [HTTP-відповідь із перенаправленням](/docs/{{version}}/responses#redirects) для заданого [іменованого маршруту](/docs/{{version}}/routing#named-routes):

```php
return to_route('users.show', ['user' => 1]);
```

За потреби ви можете передати третім і четвертим аргументами методу `to_route` HTTP-статус, який слід призначити перенаправленню, і будь-які додаткові заголовки відповіді:

```php
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

<a name="method-uri"></a>
#### `uri()` {.collection-method}

Функція `uri` генерує [плавний екземпляр URI](#uri) для заданого URI:

```php
$uri = uri('https://example.com')
    ->withPath('/users')
    ->withQuery(['page' => 1]);
```

Якщо функції `uri` передано масив із парою «контролер - метод», яку можна викликати, функція створить екземпляр `Uri` для шляху маршруту цього методу контролера:

```php
use App\Http\Controllers\UserController;

$uri = uri([UserController::class, 'show'], ['user' => $user]);
```

Якщо контролер викликаємий, ви можете просто передати назву його класу:

```php
use App\Http\Controllers\UserIndexController;

$uri = uri(UserIndexController::class);
```

Якщо значення, передане функції `uri`, збігається з іменем [іменованого маршруту](/docs/{{version}}/routing#named-routes), буде згенеровано екземпляр `Uri` для шляху цього маршруту:

```php
$uri = uri('users.show', ['user' => $user]);
```

<a name="method-url"></a>
#### `url()` {.collection-method}

Функція `url` генерує повний URL до заданого шляху:

```php
$url = url('user/profile');

$url = url('user/profile', [1]);
```

Якщо шлях не передано, повертається екземпляр `Illuminate\Routing\UrlGenerator`:

```php
$current = url()->current();

$full = url()->full();

$previous = url()->previous();
```

Докладніше про роботу з функцією `url` читайте в [документації з генерації URL](/docs/{{version}}/urls#generating-urls).

<a name="miscellaneous"></a>
## Різне

<a name="method-abort"></a>
#### `abort()` {.collection-method}

Функція `abort` викидає [HTTP-виняток](/docs/{{version}}/errors#http-exceptions), який відрендерить [обробник винятків](/docs/{{version}}/errors#handling-exceptions):

```php
abort(403);
```

Ви також можете передати повідомлення винятку й власні заголовки HTTP-відповіді, які слід надіслати браузеру:

```php
abort(403, 'Unauthorized.', $headers);
```

<a name="method-abort-if"></a>
#### `abort_if()` {.collection-method}

Функція `abort_if` викидає HTTP-виняток, якщо заданий булевий вираз дає `true`:

```php
abort_if(! Auth::user()->isAdmin(), 403);
```

Як і методу `abort`, ви можете передати функції третім аргументом текст відповіді винятку, а четвертим - масив власних заголовків відповіді.

<a name="method-abort-unless"></a>
#### `abort_unless()` {.collection-method}

Функція `abort_unless` викидає HTTP-виняток, якщо заданий булевий вираз дає `false`:

```php
abort_unless(Auth::user()->isAdmin(), 403);
```

Як і методу `abort`, ви можете передати функції третім аргументом текст відповіді винятку, а четвертим - масив власних заголовків відповіді.

<a name="method-app"></a>
#### `app()` {.collection-method}

Функція `app` повертає екземпляр [сервіс-контейнера](/docs/{{version}}/container):

```php
$container = app();
```

Ви можете передати назву класу чи інтерфейсу, щоб розв'язати його з контейнера:

```php
$api = app('HelpSpot\API');
```

<a name="method-auth"></a>
#### `auth()` {.collection-method}

Функція `auth` повертає екземпляр [автентифікатора](/docs/{{version}}/authentication). Ви можете скористатися нею як альтернативою фасаду `Auth`:

```php
$user = auth()->user();
```

За потреби ви можете вказати, до якого гарда хочете звернутися:

```php
$user = auth('admin')->user();
```

<a name="method-back"></a>
#### `back()` {.collection-method}

Функція `back` генерує [HTTP-відповідь із перенаправленням](/docs/{{version}}/responses#redirects) на попереднє місце користувача:

```php
return back($status = 302, $headers = [], $fallback = '/');

return back();
```

<a name="method-bcrypt"></a>
#### `bcrypt()` {.collection-method}

Функція `bcrypt` [хешує](/docs/{{version}}/hashing) задане значення алгоритмом Bcrypt. Ви можете скористатися цією функцією як альтернативою фасаду `Hash`:

```php
$password = bcrypt('my-secret-password');
```

<a name="method-blank"></a>
#### `blank()` {.collection-method}

Функція `blank` визначає, чи є задане значення «порожнім»:

```php
blank('');
blank('   ');
blank(null);
blank(collect());

// true

blank(0);
blank(true);
blank(false);

// false
```

Протилежність `blank` - функція [filled](#method-filled).

<a name="method-broadcast"></a>
#### `broadcast()` {.collection-method}

Функція `broadcast` [надсилає](/docs/{{version}}/broadcasting) задану [подію](/docs/{{version}}/events) її слухачам:

```php
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```

<a name="method-broadcast-if"></a>
#### `broadcast_if()` {.collection-method}

Функція `broadcast_if` [надсилає](/docs/{{version}}/broadcasting) задану [подію](/docs/{{version}}/events) її слухачам, якщо заданий булевий вираз дає `true`:

```php
broadcast_if($user->isActive(), new UserRegistered($user));

broadcast_if($user->isActive(), new UserRegistered($user))->toOthers();
```

<a name="method-broadcast-unless"></a>
#### `broadcast_unless()` {.collection-method}

Функція `broadcast_unless` [надсилає](/docs/{{version}}/broadcasting) задану [подію](/docs/{{version}}/events) її слухачам, якщо заданий булевий вираз дає `false`:

```php
broadcast_unless($user->isBanned(), new UserRegistered($user));

broadcast_unless($user->isBanned(), new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
#### `cache()` {.collection-method}

Функція `cache` дозволяє отримувати значення з [кешу](/docs/{{version}}/cache). Якщо заданого ключа в кеші немає, буде повернуто необов'язкове значення за замовчуванням:

```php
$value = cache('key');

$value = cache('key', 'default');
```

Ви можете додавати елементи до кешу, передавши функції масив пар ключ / значення. Також слід передати кількість секунд або тривалість, протягом якої закешоване значення вважатиметься дійсним:

```php
cache(['key' => 'value'], 300);

cache(['key' => 'value'], now()->plus(seconds: 10));
```

<a name="method-class-uses-recursive"></a>
#### `class_uses_recursive()` {.collection-method}

Функція `class_uses_recursive` повертає всі трейти, які використовує клас, включно з трейтами всіх його батьківських класів:

```php
$traits = class_uses_recursive(App\Models\User::class);
```

<a name="method-collect"></a>
#### `collect()` {.collection-method}

Функція `collect` створює екземпляр [колекції](/docs/{{version}}/collections) із заданого значення:

```php
$collection = collect(['Taylor', 'Abigail']);
```

<a name="method-config"></a>
#### `config()` {.collection-method}

Функція `config` отримує значення змінної [конфігурації](/docs/{{version}}/configuration). До значень конфігурації звертаються за «крапковим» синтаксисом, який містить назву файлу та потрібну опцію. Ви також можете передати значення за замовчуванням, яке буде повернуто, якщо опції конфігурації не існує:

```php
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

Ви можете задавати змінні конфігурації під час виконання, передавши масив пар ключ / значення. Проте зауважте: ця функція впливає лише на значення конфігурації для поточного запиту й не оновлює ваших справжніх значень конфігурації:

```php
config(['app.debug' => true]);
```

<a name="method-context"></a>
#### `context()` {.collection-method}

Функція `context` отримує значення з поточного [контексту](/docs/{{version}}/context). Ви також можете передати значення за замовчуванням, яке буде повернуто, якщо ключа контексту не існує:

```php
$value = context('trace_id');

$value = context('trace_id', $default);
```

Ви можете задавати значення контексту, передавши масив пар ключ / значення:

```php
use Illuminate\Support\Str;

context(['trace_id' => Str::uuid()->toString()]);
```

<a name="method-cookie"></a>
#### `cookie()` {.collection-method}

Функція `cookie` створює новий екземпляр [cookie](/docs/{{version}}/requests#cookies):

```php
$cookie = cookie('name', 'value', $minutes);
```

<a name="method-csrf-field"></a>
#### `csrf_field()` {.collection-method}

Функція `csrf_field` генерує HTML-поле `hidden` зі значенням CSRF-токена. Наприклад, із [синтаксисом Blade](/docs/{{version}}/blade):

```blade
{{ csrf_field() }}
```

<a name="method-csrf-token"></a>
#### `csrf_token()` {.collection-method}

Функція `csrf_token` дістає значення поточного CSRF-токена:

```php
$token = csrf_token();
```

<a name="method-decrypt"></a>
#### `decrypt()` {.collection-method}

Функція `decrypt` [розшифровує](/docs/{{version}}/encryption) задане значення. Ви можете скористатися цією функцією як альтернативою фасаду `Crypt`:

```php
$password = decrypt($value);
```

Протилежність `decrypt` - функція [encrypt](#method-encrypt).

<a name="method-dd"></a>
#### `dd()` {.collection-method}

Функція `dd` виводить задані змінні та припиняє виконання скрипта:

```php
dd($value);

dd($value1, $value2, $value3, ...);
```

Якщо ви не хочете зупиняти виконання скрипта, скористайтеся натомість функцією [dump](#method-dump).

<a name="method-dispatch"></a>
#### `dispatch()` {.collection-method}

Функція `dispatch` кладе задане [завдання](/docs/{{version}}/queues#creating-jobs) до [черги завдань](/docs/{{version}}/queues) Laravel:

```php
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dispatch-sync"></a>
#### `dispatch_sync()` {.collection-method}

Функція `dispatch_sync` кладе задане завдання до черги [sync](/docs/{{version}}/queues#synchronous-dispatching), тож воно обробляється негайно:

```php
dispatch_sync(new App\Jobs\SendEmails);
```

<a name="method-dump"></a>
#### `dump()` {.collection-method}

Функція `dump` виводить задані змінні:

```php
dump($value);

dump($value1, $value2, $value3, ...);
```

Якщо ви хочете припинити виконання скрипта після виведення змінних, скористайтеся натомість функцією [dd](#method-dd).

<a name="method-encrypt"></a>
#### `encrypt()` {.collection-method}

Функція `encrypt` [шифрує](/docs/{{version}}/encryption) задане значення. Ви можете скористатися цією функцією як альтернативою фасаду `Crypt`:

```php
$secret = encrypt('my-secret-value');
```

Протилежність `encrypt` - функція [decrypt](#method-decrypt).

<a name="method-env"></a>
#### `env()` {.collection-method}

Функція `env` дістає значення [змінної середовища](/docs/{{version}}/configuration#environment-configuration) або повертає значення за замовчуванням:

```php
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!WARNING]
> Якщо під час розгортання ви виконуєте команду `config:cache`, переконайтеся, що викликаєте функцію `env` лише у файлах конфігурації. Щойно конфігурацію закешовано, файл `.env` не завантажується, і всі виклики функції `env` повертатимуть зовнішні змінні середовища - на рівні сервера чи системи - або `null`.

<a name="method-event"></a>
#### `event()` {.collection-method}

Функція `event` диспетчеризує задану [подію](/docs/{{version}}/events) її слухачам:

```php
event(new UserRegistered($user));
```

<a name="method-fake"></a>
#### `fake()` {.collection-method}

Функція `fake` розв'язує з контейнера сінглтон [Faker](https://github.com/FakerPHP/Faker), що стане в пригоді для створення фейкових даних у фабриках моделей, наповненні бази, тестах і прототипуванні представлень:

```blade
@for ($i = 0; $i < 10; $i++)
    <dl>
        <dt>Name</dt>
        <dd>{{ fake()->name() }}</dd>

        <dt>Email</dt>
        <dd>{{ fake()->unique()->safeEmail() }}</dd>
    </dl>
@endfor
```

За замовчуванням функція `fake` використовує опцію конфігурації `app.faker_locale` у вашому `config/app.php`. Зазвичай цю опцію задають через змінну середовища `APP_FAKER_LOCALE`. Ви також можете вказати локаль, передавши її функції `fake`. Для кожної локалі буде розв'язано окремий сінглтон:

```php
fake('nl_NL')->name()
```

<a name="method-filled"></a>
#### `filled()` {.collection-method}

Функція `filled` визначає, чи не є задане значення «порожнім»:

```php
filled(0);
filled(true);
filled(false);

// true

filled('');
filled('   ');
filled(null);
filled(collect());

// false
```

Протилежність `filled` - функція [blank](#method-blank).

<a name="method-info"></a>
#### `info()` {.collection-method}

Функція `info` запише інформацію до [логу](/docs/{{version}}/logging) вашого застосунку:

```php
info('Some helpful information!');
```

Функції також можна передати масив контекстних даних:

```php
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-literal"></a>
#### `literal()` {.collection-method}

Функція `literal` створює новий екземпляр [stdClass](https://www.php.net/manual/en/class.stdclass.php), де задані іменовані аргументи стають властивостями:

```php
$obj = literal(
    name: 'Joe',
    languages: ['PHP', 'Ruby'],
);

$obj->name; // 'Joe'
$obj->languages; // ['PHP', 'Ruby']
```

<a name="method-logger"></a>
#### `logger()` {.collection-method}

Функція `logger` дозволяє записати до [логу](/docs/{{version}}/logging) повідомлення рівня `debug`:

```php
logger('Debug message');
```

Функції також можна передати масив контекстних даних:

```php
logger('User has logged in.', ['id' => $user->id]);
```

Якщо функції не передано значення, буде повернуто екземпляр [логера](/docs/{{version}}/logging):

```php
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>
#### `method_field()` {.collection-method}

Функція `method_field` генерує HTML-поле `hidden`, яке містить підмінене значення HTTP-дієслова форми. Наприклад, із [синтаксисом Blade](/docs/{{version}}/blade):

```blade
<form method="POST">
    {{ method_field('DELETE') }}
</form>
```

<a name="method-now"></a>
#### `now()` {.collection-method}

Функція `now` створює новий екземпляр `Illuminate\Support\Carbon` для поточного часу:

```php
$now = now();
```

<a name="method-old"></a>
#### `old()` {.collection-method}

Функція `old` [дістає](/docs/{{version}}/requests#retrieving-input) значення [старого вводу](/docs/{{version}}/requests#old-input), збереженого в сесії:

```php
$value = old('value');

$value = old('value', 'default');
```

Оскільки «значення за замовчуванням», яке передають другим аргументом функції `old`, часто є атрибутом моделі Eloquent, Laravel дозволяє просто передати другим аргументом усю модель Eloquent. У такому разі Laravel вважатиме, що перший аргумент функції `old` - це назва атрибута Eloquent, який слід узяти за «значення за замовчуванням»:

```blade
{{ old('name', $user->name) }}

// Is equivalent to...

{{ old('name', $user) }}
```

<a name="method-once"></a>
#### `once()` {.collection-method}

Функція `once` виконує заданий колбек і кешує результат у пам'яті на час запиту. Будь-які наступні виклики функції `once` з тим самим колбеком повертатимуть раніше закешований результат:

```php
function random(): int
{
    return once(function () {
        return random_int(1, 1000);
    });
}

random(); // 123
random(); // 123 (cached result)
random(); // 123 (cached result)
```

Коли функцію `once` виконано зсередини екземпляра об'єкта, закешований результат буде унікальним для цього екземпляра:

```php
<?php

class NumberService
{
    public function all(): array
    {
        return once(fn () => [1, 2, 3]);
    }
}

$service = new NumberService;

$service->all();
$service->all(); // (cached result)

$secondService = new NumberService;

$secondService->all();
$secondService->all(); // (cached result)
```
<a name="method-optional"></a>
#### `optional()` {.collection-method}

Функція `optional` приймає будь-який аргумент і дозволяє звертатися до властивостей або викликати методи цього об'єкта. Якщо заданий об'єкт - `null`, властивості й методи повернуть `null` замість того, щоб спричинити помилку:

```php
return optional($user->address)->street;

{!! old('name', optional($user)->name) !!}
```

Функція `optional` також приймає замикання другим аргументом. Замикання буде викликано, якщо значення, передане першим аргументом, не є null:

```php
return optional(User::find($id), function (User $user) {
    return $user->name;
});
```

<a name="method-policy"></a>
#### `policy()` {.collection-method}

Метод `policy` дістає екземпляр [політики](/docs/{{version}}/authorization#creating-policies) для заданого класу:

```php
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
#### `redirect()` {.collection-method}

Функція `redirect` повертає [HTTP-відповідь із перенаправленням](/docs/{{version}}/responses#redirects) або, якщо викликана без аргументів, екземпляр редиректора:

```php
return redirect($to = null, $status = 302, $headers = [], $secure = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
#### `report()` {.collection-method}

Функція `report` повідомить про виняток через ваш [обробник винятків](/docs/{{version}}/errors#handling-exceptions):

```php
report($e);
```

Функція `report` також приймає рядок як аргумент. Коли функції передано рядок, вона створить виняток із цим рядком як повідомленням:

```php
report('Something went wrong.');
```

<a name="method-report-if"></a>
#### `report_if()` {.collection-method}

Функція `report_if` повідомить про виняток через ваш [обробник винятків](/docs/{{version}}/errors#handling-exceptions), якщо заданий булевий вираз дає `true`:

```php
report_if($shouldReport, $e);

report_if($shouldReport, 'Something went wrong.');
```

<a name="method-report-unless"></a>
#### `report_unless()` {.collection-method}

Функція `report_unless` повідомить про виняток через ваш [обробник винятків](/docs/{{version}}/errors#handling-exceptions), якщо заданий булевий вираз дає `false`:

```php
report_unless($reportingDisabled, $e);

report_unless($reportingDisabled, 'Something went wrong.');
```

<a name="method-request"></a>
#### `request()` {.collection-method}

Функція `request` повертає поточний екземпляр [запиту](/docs/{{version}}/requests) або дістає значення поля вводу з поточного запиту:

```php
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
#### `rescue()` {.collection-method}

Функція `rescue` виконує задане замикання й ловить будь-які винятки, що трапляються під час його виконання. Усі спіймані винятки буде надіслано вашому [обробнику винятків](/docs/{{version}}/errors#handling-exceptions); проте обробка запиту продовжиться:

```php
return rescue(function () {
    return $this->method();
});
```

Ви також можете передати функції `rescue` другий аргумент. Це буде значення «за замовчуванням», яке слід повернути, якщо під час виконання замикання станеться виняток:

```php
return rescue(function () {
    return $this->method();
}, false);

return rescue(function () {
    return $this->method();
}, function () {
    return $this->failure();
});
```

Функції `rescue` можна передати аргумент `report`, щоб визначити, чи слід повідомляти про виняток через функцію `report`:

```php
return rescue(function () {
    return $this->method();
}, report: function (Throwable $throwable) {
    return $throwable instanceof InvalidArgumentException;
});
```

<a name="method-resolve"></a>
#### `resolve()` {.collection-method}

Функція `resolve` розв'язує задану назву класу чи інтерфейсу в екземпляр через [сервіс-контейнер](/docs/{{version}}/container):

```php
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
#### `response()` {.collection-method}

Функція `response` створює екземпляр [відповіді](/docs/{{version}}/responses) або отримує екземпляр фабрики відповідей:

```php
return response('Hello World', 200, $headers);

return response()->json(['foo' => 'bar'], 200, $headers);
```

<a name="method-retry"></a>
#### `retry()` {.collection-method}

Функція `retry` намагається виконати заданий колбек, доки не буде досягнуто заданої максимальної кількості спроб. Якщо колбек не викидає винятку, буде повернуто його значення. Якщо колбек викидає виняток, спробу буде автоматично повторено. Якщо максимальну кількість спроб перевищено, виняток буде викинуто:

```php
return retry(5, function () {
    // Attempt 5 times while resting 100ms between attempts...
}, 100);
```

Тривалість паузи також приймає екземпляр `CarbonInterval`:

```php
use function Illuminate\Support\seconds;

return retry(5, function () {
    // Attempt 5 times while resting 5 seconds between attempts...
}, seconds(5));
```

Якщо ви хочете вручну обчислювати кількість мілісекунд паузи між спробами, передайте третім аргументом функції `retry` замикання:

```php
use Exception;

return retry(5, function () {
    // ...
}, function (int $attempt, Exception $exception) {
    return $attempt * 100;
});
```

Для зручності ви можете передати першим аргументом функції `retry` масив. За цим масивом визначатиметься, скільки мілісекунд чекати між наступними спробами:

```php
return retry([100, 200], function () {
    // Sleep for 100ms on first retry, 200ms on second retry...
});
```

Щоб повторювати спроби лише за певних умов, передайте четвертим аргументом функції `retry` замикання:

```php
use App\Exceptions\TemporaryException;
use Exception;

return retry(5, function () {
    // ...
}, 100, function (Exception $exception) {
    return $exception instanceof TemporaryException;
});
```

<a name="method-session"></a>
#### `session()` {.collection-method}

Функція `session` дозволяє отримувати або задавати значення [сесії](/docs/{{version}}/session):

```php
$value = session('key');
```

Ви можете задавати значення, передавши функції масив пар ключ / значення:

```php
session(['chairs' => 7, 'instruments' => 3]);
```

Якщо функції не передано значення, буде повернуто сховище сесії:

```php
$value = session()->get('key');

session()->put('key', $value);
```

<a name="method-tap"></a>
#### `tap()` {.collection-method}

Функція `tap` приймає два аргументи: довільне `$value` і замикання. `$value` буде передано до замикання, а потім повернуто функцією `tap`. Значення, яке повертає замикання, не має значення:

```php
$user = tap(User::first(), function (User $user) {
    $user->name = 'Taylor';

    $user->save();
});
```

Якщо функції `tap` не передано замикання, ви можете викликати будь-який метод на заданому `$value`. Значенням, яке поверне викликаний метод, завжди буде `$value`, незалежно від того, що метод справді повертає у своєму описі. Наприклад, метод Eloquent `update` зазвичай повертає ціле число. Проте ми можемо змусити метод повернути саму модель, зробивши виклик `update` ланцюжком через функцію `tap`:

```php
$user = tap($user)->update([
    'name' => $name,
    'email' => $email,
]);
```

Щоб додати до класу метод `tap`, додайте до нього трейт `Illuminate\Support\Traits\Tappable`. Метод `tap` цього трейта приймає єдиним аргументом Closure. Сам екземпляр об'єкта буде передано до Closure, а потім повернуто методом `tap`:

```php
return $user->tap(function (User $user) {
    // ...
});
```

<a name="method-throw-if"></a>
#### `throw_if()` {.collection-method}

Функція `throw_if` викидає заданий виняток, якщо заданий булевий вираз дає `true`:

```php
throw_if(! Auth::user()->isAdmin(), AuthorizationException::class);

throw_if(
    ! Auth::user()->isAdmin(),
    AuthorizationException::class,
    'You are not allowed to access this page.'
);
```

<a name="method-throw-unless"></a>
#### `throw_unless()` {.collection-method}

Функція `throw_unless` викидає заданий виняток, якщо заданий булевий вираз дає `false`:

```php
throw_unless(Auth::user()->isAdmin(), AuthorizationException::class);

throw_unless(
    Auth::user()->isAdmin(),
    AuthorizationException::class,
    'You are not allowed to access this page.'
);
```

<a name="method-today"></a>
#### `today()` {.collection-method}

Функція `today` створює новий екземпляр `Illuminate\Support\Carbon` для поточної дати:

```php
$today = today();
```

<a name="method-trait-uses-recursive"></a>
#### `trait_uses_recursive()` {.collection-method}

Функція `trait_uses_recursive` повертає всі трейти, які використовує трейт:

```php
$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

<a name="method-transform"></a>
#### `transform()` {.collection-method}

Функція `transform` виконує замикання над заданим значенням, якщо воно не [порожнє](#method-blank), і повертає значення, яке повернуло замикання:

```php
$callback = function (int $value) {
    return $value * 2;
};

$result = transform(5, $callback);

// 10
```

Третім аргументом функції можна передати значення за замовчуванням або замикання. Його буде повернуто, якщо задане значення порожнє:

```php
$result = transform(null, $callback, 'The value is blank');

// The value is blank
```

<a name="method-validator"></a>
#### `validator()` {.collection-method}

Функція `validator` створює новий екземпляр [валідатора](/docs/{{version}}/validation) із заданими аргументами. Ви можете скористатися нею як альтернативою фасаду `Validator`:

```php
$validator = validator($data, $rules, $messages);
```

<a name="method-value"></a>
#### `value()` {.collection-method}

Функція `value` повертає передане їй значення. Проте, якщо ви передасте функції замикання, воно буде виконане, і буде повернуто його результат:

```php
$result = value(true);

// true

$result = value(function () {
    return false;
});

// false
```

Функції `value` можна передати додаткові аргументи. Якщо перший аргумент - замикання, додаткові параметри буде передано замиканню як аргументи, інакше їх буде проігноровано:

```php
$result = value(function (string $name) {
    return $name;
}, 'Taylor');

// 'Taylor'
```

<a name="method-view"></a>
#### `view()` {.collection-method}

Функція `view` дістає екземпляр [представлення](/docs/{{version}}/views):

```php
return view('auth.login');
```

<a name="method-with"></a>
#### `with()` {.collection-method}

Функція `with` повертає передане їй значення. Якщо другим аргументом функції передано замикання, воно буде виконане, і буде повернуто його результат:

```php
$callback = function (mixed $value) {
    return is_numeric($value) ? $value * 2 : 0;
};

$result = with(5, $callback);

// 10

$result = with(null, $callback);

// 0

$result = with(5, null);

// 5
```

<a name="method-when"></a>
#### `when()` {.collection-method}

Функція `when` повертає передане їй значення, якщо задана умова дає `true`. Інакше повертається `null`. Якщо другим аргументом функції передано замикання, воно буде виконане, і буде повернуто його результат:

```php
$value = when(true, 'Hello World');

$value = when(true, fn () => 'Hello World');
```

Функція `when` насамперед корисна для умовного рендерингу HTML-атрибутів:

```blade
<div {!! when($condition, 'wire:poll="calculate"') !!}>
    ...
</div>
```

<a name="other-utilities"></a>
## Інші утиліти

<a name="benchmarking"></a>
### Бенчмаркінг

Інколи вам може захотітися швидко перевірити швидкодію певних частин застосунку. У таких випадках скористайтеся допоміжним класом `Benchmark`, щоб виміряти, скільки мілісекунд потрібно заданим колбекам на виконання:

```php
<?php

use App\Models\User;
use Illuminate\Support\Benchmark;

Benchmark::dd(fn () => User::find(1)); // 0.1 ms

Benchmark::dd([
    'Scenario 1' => fn () => User::count(), // 0.5 ms
    'Scenario 2' => fn () => User::all()->count(), // 20.0 ms
]);
```

За замовчуванням задані колбеки виконуються один раз (одна ітерація), а їхня тривалість відображається в браузері / консолі.

Щоб викликати колбек більше одного разу, вкажіть другим аргументом методу кількість ітерацій. Коли колбек виконується кілька разів, клас `Benchmark` поверне середню кількість мілісекунд, витрачених на його виконання по всіх ітераціях:

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

Інколи вам може захотітися виміряти виконання колбека й водночас отримати значення, яке він повертає. Метод `value` поверне кортеж зі значенням, яке повернув колбек, і кількістю мілісекунд, витрачених на його виконання:

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### Дата й час

Laravel містить [Carbon](https://carbon.nesbot.com/guide/getting-started/introduction.html) - потужну бібліотеку для роботи з датою й часом. Щоб створити новий екземпляр `Carbon`, викличте функцію `now`. Ця функція глобально доступна у вашому застосунку Laravel:

```php
$now = now();
```

Або ж ви можете створити новий екземпляр `Carbon` через клас `Illuminate\Support\Carbon`:

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Laravel також розширює екземпляри `Carbon` методами `plus` і `minus`, які дозволяють легко змінювати дату й час екземпляра:

```php
return now()->plus(minutes: 5);
return now()->plus(hours: 8);
return now()->plus(weeks: 4);

return now()->minus(minutes: 5);
return now()->minus(hours: 8);
return now()->minus(weeks: 4);
```

Докладний огляд Carbon і його можливостей ви знайдете в [офіційній документації Carbon](https://carbon.nesbot.com/guide/getting-started/introduction.html).

<a name="interval-functions"></a>
#### Функції інтервалів

Laravel також пропонує функції `milliseconds`, `seconds`, `minutes`, `hours`, `days`, `weeks`, `months` та `years`, які повертають екземпляри `CarbonInterval`, що розширюють PHP-клас [DateInterval](https://www.php.net/manual/en/class.dateinterval.php). Ці функції можна використовувати всюди, де Laravel приймає екземпляр `DateInterval`:

```php
use Illuminate\Support\Facades\Cache;

use function Illuminate\Support\{minutes};

Cache::put('metrics', $metrics, minutes(10));
```

<a name="deferred-functions"></a>
### Відкладені функції

Хоч [завдання в черзі](/docs/{{version}}/queues) Laravel і дозволяють ставити задачі в чергу на фонову обробку, інколи у вас є прості задачі, які хочеться відкласти, не налаштовуючи й не підтримуючи довгограючого воркера черги.

Відкладені функції дозволяють відкласти виконання замикання до моменту, коли HTTP-відповідь уже надіслано користувачеві, - і застосунок і далі здається швидким та чуйним. Щоб відкласти виконання замикання, просто передайте його функції `Illuminate\Support\defer`:

```php
use App\Services\Metrics;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use function Illuminate\Support\defer;

Route::post('/orders', function (Request $request) {
    // Create order...

    defer(fn () => Metrics::reportOrder($order));

    return $order;
});
```

За замовчуванням відкладені функції виконуються, лише якщо HTTP-відповідь, команда Artisan чи завдання в черзі, з яких викликано `Illuminate\Support\defer`, завершилися успішно. Це означає, що відкладені функції не виконаються, якщо запит дасть HTTP-відповідь `4xx` чи `5xx`. Якщо ви хочете, щоб відкладена функція виконувалася завжди, додайте до неї ланцюжком метод `always`:

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

> [!WARNING]
> Якщо у вас встановлено [розширення PHP Swoole](https://www.php.net/manual/en/book.swoole.php), функція `defer` Laravel може конфліктувати з власною глобальною функцією `defer` від Swoole, що призведе до помилок вебсервера. Обов'язково викликайте хелпер `defer` Laravel, явно вказавши простір імен: `use function Illuminate\Support\defer;`

<a name="cancelling-deferred-functions"></a>
#### Скасування відкладених функцій

Якщо вам потрібно скасувати відкладену функцію до її виконання, скористайтеся методом `forget`, щоб скасувати функцію за її іменем. Щоб назвати відкладену функцію, передайте другий аргумент функції `Illuminate\Support\defer`:

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="disabling-deferred-functions-in-tests"></a>
#### Вимкнення відкладених функцій у тестах

Пишучи тести, буває корисно вимкнути відкладені функції. Ви можете викликати у своєму тесті `withoutDefer`, щоб Laravel виконував усі відкладені функції негайно:

```php tab=Pest
test('without defer', function () {
    $this->withoutDefer();

    // ...
});
```

```php tab=PHPUnit
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_without_defer(): void
    {
        $this->withoutDefer();

        // ...
    }
}
```

Якщо ви хочете вимкнути відкладені функції для всіх тестів у тест-кейсі, викличте метод `withoutDefer` у методі `setUp` вашого базового класу `TestCase`:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void// [tl! add:start]
    {
        parent::setUp();

        $this->withoutDefer();
    }// [tl! add:end]
}
```

<a name="lottery"></a>
### Лотерея

Клас лотереї Laravel дозволяє виконувати колбеки на основі заданих шансів. Це особливо корисно, коли ви хочете виконувати код лише для певного відсотка вхідних запитів:

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

Ви можете поєднувати клас лотереї Laravel з іншими можливостями фреймворку. Наприклад, ви можете хотіти повідомляти обробнику винятків лише про невеликий відсоток повільних запитів. А оскільки клас лотереї є викликаємим, ми можемо передати його екземпляр до будь-якого методу, який приймає щось викликаєме:

```php
use Carbon\CarbonInterval;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Lottery;

DB::whenQueryingForLongerThan(
    CarbonInterval::seconds(2),
    Lottery::odds(1, 100)->winner(fn () => report('Querying > 2 seconds.')),
);
```

<a name="testing-lotteries"></a>
#### Тестування лотерей

Laravel надає кілька простих методів, які дозволяють легко тестувати виклики лотереї у вашому застосунку:

```php
// Lottery will always win...
Lottery::alwaysWin();

// Lottery will always lose...
Lottery::alwaysLose();

// Lottery will win then lose, and finally return to normal behavior...
Lottery::fix([true, false]);

// Lottery will return to normal behavior...
Lottery::determineResultsNormally();
```

<a name="pipeline"></a>
### Конвеєр

Фасад `Pipeline` Laravel надає зручний спосіб «пропустити» заданий ввід через низку викликаємих класів, замикань чи колбеків, даючи кожному класу можливість оглянути чи змінити ввід і викликати наступний елемент конвеєра:

```php
use Closure;
use App\Models\User;
use Illuminate\Support\Facades\Pipeline;

$user = Pipeline::send($user)
    ->through([
        function (User $user, Closure $next) {
            // ...

            return $next($user);
        },
        function (User $user, Closure $next) {
            // ...

            return $next($user);
        },
    ])
    ->then(fn (User $user) => $user);
```

Як бачите, кожен викликаємий клас чи замикання в конвеєрі отримує ввід і замикання `$next`. Виклик замикання `$next` викличе наступний елемент конвеєра. Як ви могли помітити, це дуже схоже на [middleware](/docs/{{version}}/middleware).

Коли останній елемент конвеєра викликає замикання `$next`, буде викликано колбек, переданий методу `then`. Зазвичай цей колбек просто повертає заданий ввід. Для зручності, якщо ви просто хочете повернути ввід після обробки, скористайтеся методом `thenReturn`.

Звісно, як уже зазначалося, ви не обмежені замиканнями в конвеєрі. Ви можете передавати й викликаємі класи. Якщо передано назву класу, його буде створено через [сервіс-контейнер](/docs/{{version}}/container) Laravel, що дозволяє впровадити залежності у викликаємий клас:

```php
$user = Pipeline::send($user)
    ->through([
        GenerateProfilePhoto::class,
        ActivateSubscription::class,
        SendWelcomeEmail::class,
    ])
    ->thenReturn();
```

Метод `withinTransaction` можна викликати на конвеєрі, щоб автоматично огорнути всі його кроки однією транзакцією бази даних:

```php
$user = Pipeline::send($user)
    ->withinTransaction()
    ->through([
        ProcessOrder::class,
        TransferFunds::class,
        UpdateInventory::class,
    ])
    ->thenReturn();
```

<a name="sleep"></a>
### Sleep

Клас `Sleep` Laravel - це легка обгортка над нативними функціями PHP `sleep` та `usleep`, яка забезпечує кращу тестованість і водночас надає зручний для розробника API для роботи з часом:

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

Клас `Sleep` пропонує різноманітні методи для роботи з різними одиницями часу:

```php
// Return a value after sleeping...
$result = Sleep::for(1)->second()->then(fn () => 1 + 1);

// Sleep while a given value is true...
Sleep::for(1)->second()->while(fn () => shouldKeepSleeping());

// Pause execution for 90 seconds...
Sleep::for(1.5)->minutes();

// Pause execution for 2 seconds...
Sleep::for(2)->seconds();

// Pause execution for 500 milliseconds...
Sleep::for(500)->milliseconds();

// Pause execution for 5,000 microseconds...
Sleep::for(5000)->microseconds();

// Pause execution until a given time...
Sleep::until(now()->plus(minutes: 1));

// Alias of PHP's native "sleep" function...
Sleep::sleep(2);

// Alias of PHP's native "usleep" function...
Sleep::usleep(5000);
```

Щоб легко поєднувати одиниці часу, скористайтеся методом `and`:

```php
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### Тестування Sleep

Коли ви тестуєте код, який використовує клас `Sleep` чи нативні функції sleep у PHP, ваш тест зупинятиме виконання. Як ви й очікуєте, це суттєво сповільнює набір тестів. Наприклад, уявіть, що ви тестуєте такий код:

```php
$waiting = /* ... */;

$seconds = 1;

while ($waiting) {
    Sleep::for($seconds++)->seconds();

    $waiting = /* ... */;
}
```

Зазвичай тестування цього коду тривало б _щонайменше_ секунду. На щастя, клас `Sleep` дозволяє «підмінити» паузи, тож наш набір тестів лишається швидким:

```php tab=Pest
it('waits until ready', function () {
    Sleep::fake();

    // ...
});
```

```php tab=PHPUnit
public function test_it_waits_until_ready()
{
    Sleep::fake();

    // ...
}
```

Коли клас `Sleep` підмінено, справжню паузу у виконанні буде пропущено, і тест стане значно швидшим.

Щойно клас `Sleep` підмінено, можна робити перевірки очікуваних «пауз». Щоб проілюструвати це, уявімо, що ми тестуємо код, який зупиняє виконання тричі, і кожна пауза довша на секунду. Методом `assertSequence` ми можемо перевірити, що наш код «спав» належний час, і водночас лишити тест швидким:

```php tab=Pest
it('checks if ready three times', function () {
    Sleep::fake();

    // ...

    Sleep::assertSequence([
        Sleep::for(1)->second(),
        Sleep::for(2)->seconds(),
        Sleep::for(3)->seconds(),
    ]);
}
```

```php tab=PHPUnit
public function test_it_checks_if_ready_three_times()
{
    Sleep::fake();

    // ...

    Sleep::assertSequence([
        Sleep::for(1)->second(),
        Sleep::for(2)->seconds(),
        Sleep::for(3)->seconds(),
    ]);
}
```

Звісно, клас `Sleep` пропонує й низку інших перевірок, якими ви можете скористатися під час тестування:

```php
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// Assert that sleep was called 3 times...
Sleep::assertSleptTimes(3);

// Assert against the duration of sleep...
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// Assert that the Sleep class was never invoked...
Sleep::assertNeverSlept();

// Assert that, even if Sleep was called, no execution paused occurred...
Sleep::assertInsomniac();
```

Інколи буває корисно виконувати якусь дію щоразу, коли трапляється підмінена пауза. Для цього передайте колбек методу `whenFakingSleep`. У прикладі нижче ми користуємося [хелперами маніпуляції часом](/docs/{{version}}/mocking#interacting-with-time) Laravel, щоб миттєво просувати час на тривалість кожної паузи:

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // Progress time when faking sleep...
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

Оскільки просування часу - поширена потреба, метод `fake` приймає аргумент `syncWithCarbon`, який тримає Carbon синхронізованим під час пауз у тесті:

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1 second ago
```

Laravel використовує клас `Sleep` усередині, коли зупиняє виконання. Наприклад, хелпер [retry](#method-retry) під час пауз користується класом `Sleep`, що покращує тестованість роботи з цим хелпером.

<a name="timebox"></a>
### Timebox

Клас `Timebox` Laravel гарантує, що заданий колбек завжди виконується фіксований час, навіть якщо насправді завершується раніше. Це особливо корисно для криптографічних операцій і перевірок автентифікації користувачів, де зловмисники могли б скористатися різницею в часі виконання, щоб вивідати чутливу інформацію.

Якщо виконання перевищує фіксовану тривалість, `Timebox` не має ефекту. Розробник сам має обрати достатньо довгу фіксовану тривалість, щоб урахувати найгірші сценарії.

Метод call приймає замикання й ліміт часу в мікросекундах, після чого виконує замикання й чекає, доки не буде досягнуто ліміту:

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

Якщо всередині замикання викинуто виняток, цей клас дотримається заданої затримки й перевикине виняток після неї.

<a name="uri"></a>
### URI

Клас `Uri` Laravel надає зручний і плавний інтерфейс для створення URI та роботи з ними. Цей клас обгортає функціональність пакета League URI й безшовно інтегрується із системою маршрутизації Laravel.

Створити екземпляр `Uri` легко за допомогою статичних методів:

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// Generate a URI instance from the given string...
$uri = Uri::of('https://example.com/path');

// Generate URI instances to paths, named routes, or controller actions...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->plus(minutes: 5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// Generate a URI instance from the current request URL...
$uri = $request->uri();
```

Щойно ви маєте екземпляр URI, ви можете плавно його змінювати:

```php
$uri = Uri::of('https://example.com')
    ->withScheme('http')
    ->withHost('test.com')
    ->withPort(8000)
    ->withPath('/users')
    ->withQuery(['page' => 2])
    ->withFragment('section-1');
```

<a name="inspecting-uris"></a>
#### Огляд URI

Клас `Uri` також дозволяє легко оглядати різні складові URI:

```php
$scheme = $uri->scheme();
$authority = $uri->authority();
$host = $uri->host();
$port = $uri->port();
$path = $uri->path();
$segments = $uri->pathSegments();
$query = $uri->query();
$fragment = $uri->fragment();
```

<a name="manipulating-query-strings"></a>
#### Робота з рядками запиту

Клас `Uri` пропонує кілька методів для роботи з рядком запиту URI. Метод `withQuery` дозволяє злити додаткові параметри до наявного рядка запиту:

```php
$uri = $uri->withQuery(['sort' => 'name']);
```

Метод `withQueryIfMissing` дозволяє злити додаткові параметри до наявного рядка запиту, якщо заданих ключів у ньому ще немає:

```php
$uri = $uri->withQueryIfMissing(['page' => 1]);
```

Метод `replaceQuery` дозволяє повністю замінити наявний рядок запиту новим:

```php
$uri = $uri->replaceQuery(['page' => 1]);
```

Метод `pushOntoQuery` дозволяє додати додаткові параметри до параметра рядка запиту, який має значення-масив:

```php
$uri = $uri->pushOntoQuery('filter', ['active', 'pending']);
```

Метод `withoutQuery` дозволяє вилучити параметри з рядка запиту:

```php
$uri = $uri->withoutQuery(['page']);
```

<a name="generating-responses-from-uris"></a>
#### Генерація відповідей з URI

Метод `redirect` дозволяє згенерувати екземпляр `RedirectResponse` до заданого URI:

```php
$uri = Uri::of('https://example.com');

return $uri->redirect();
```

Або ж ви можете просто повернути екземпляр `Uri` з маршруту чи дії контролера - і буде автоматично згенеровано відповідь із перенаправленням на цей URI:

```php
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Uri;

Route::get('/redirect', function () {
    return Uri::to('/index')
        ->withQuery(['sort' => 'name']);
});
```
