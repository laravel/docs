---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Колекції

- [Вступ](#introduction)
    - [Створення колекцій](#creating-collections)
    - [Розширення колекцій](#extending-collections)
- [Доступні методи](#available-methods)
- [Повідомлення вищого порядку](#higher-order-messages)
- [Ліниві колекції](#lazy-collections)
    - [Вступ](#lazy-collection-introduction)
    - [Створення лінивих колекцій](#creating-lazy-collections)
    - [Контракт Enumerable](#the-enumerable-contract)
    - [Методи лінивих колекцій](#lazy-collection-methods)

<a name="introduction"></a>
## Вступ

Клас `Illuminate\Support\Collection` надає зручну плавну обгортку для роботи з масивами даних. Наприклад, погляньте на код нижче. Ми скористаємося хелпером `collect`, щоб створити новий екземпляр колекції з масиву, застосуємо до кожного елемента функцію `strtoupper`, а потім приберемо всі порожні елементи:

```php
$collection = collect(['Taylor', 'Abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

Як бачите, клас `Collection` дозволяє ланцюжком викликати свої методи, щоб плавно виконувати map і reduce над масивом під капотом. Загалом колекції незмінні: кожен метод `Collection` повертає цілком новий екземпляр `Collection`.

<a name="creating-collections"></a>
### Створення колекцій

Як згадано вище, хелпер `collect` повертає новий екземпляр `Illuminate\Support\Collection` для заданого масиву. Тож створити колекцію - простіше простого:

```php
$collection = collect([1, 2, 3]);
```

Ви також можете створити колекцію методами [make](#method-make) та [fromJson](#method-fromjson).

> [!NOTE]
> Результати запитів [Eloquent](/docs/{{version}}/eloquent) завжди повертаються як екземпляри `Collection`.

<a name="extending-collections"></a>
### Розширення колекцій

Колекції «макрові»: це дозволяє додавати до класу `Collection` додаткові методи під час виконання. Метод `macro` класу `Illuminate\Support\Collection` приймає замикання, яке виконається, коли ваш макрос буде викликано. Замикання макросу має доступ до інших методів колекції через `$this`, ніби це справжній метод класу колекції. Наприклад, код нижче додає до класу `Collection` метод `toUpper`:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Str;

Collection::macro('toUpper', function () {
    return $this->map(function (string $value) {
        return Str::upper($value);
    });
});

$collection = collect(['first', 'second']);

$upper = $collection->toUpper();

// ['FIRST', 'SECOND']
```

Зазвичай макроси колекцій оголошують у методі `boot` [сервіс-провайдера](/docs/{{version}}/providers).

<a name="macro-arguments"></a>
#### Аргументи макросів

За потреби ви можете описувати макроси, які приймають додаткові аргументи:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Lang;

Collection::macro('toLocale', function (string $locale) {
    return $this->map(function (string $value) use ($locale) {
        return Lang::get($value, [], $locale);
    });
});

$collection = collect(['first', 'second']);

$translated = $collection->toLocale('es');

// ['primero', 'segundo'];
```

<a name="available-methods"></a>
## Доступні методи

Більшу частину решти документації про колекції ми присвятимо кожному методу, доступному в класі `Collection`. Пам'ятайте: усі ці методи можна ланцюжком поєднувати, щоб плавно маніпулювати масивом під капотом. Ба більше, майже кожен метод повертає новий екземпляр `Collection`, тож за потреби ви можете зберегти оригінальну копію колекції:

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

<div class="collection-method-list" markdown="1">

[after](#method-after)
[all](#method-all)
[average](#method-average)
[avg](#method-avg)
[before](#method-before)
[chunk](#method-chunk)
[chunkWhile](#method-chunkwhile)
[collapse](#method-collapse)
[collapseWithKeys](#method-collapsewithkeys)
[collect](#method-collect)
[combine](#method-combine)
[concat](#method-concat)
[contains](#method-contains)
[containsStrict](#method-containsstrict)
[count](#method-count)
[countBy](#method-countBy)
[crossJoin](#method-crossjoin)
[dd](#method-dd)
[diff](#method-diff)
[diffAssoc](#method-diffassoc)
[diffAssocUsing](#method-diffassocusing)
[diffKeys](#method-diffkeys)
[doesntContain](#method-doesntcontain)
[doesntContainStrict](#method-doesntcontainstrict)
[dot](#method-dot)
[dump](#method-dump)
[duplicates](#method-duplicates)
[duplicatesStrict](#method-duplicatesstrict)
[each](#method-each)
[eachSpread](#method-eachspread)
[ensure](#method-ensure)
[every](#method-every)
[except](#method-except)
[filter](#method-filter)
[first](#method-first)
[firstOrFail](#method-first-or-fail)
[firstWhere](#method-first-where)
[flatMap](#method-flatmap)
[flatten](#method-flatten)
[flip](#method-flip)
[forget](#method-forget)
[forPage](#method-forpage)
[fromJson](#method-fromjson)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[hasAny](#method-hasany)
[hasMany](#method-hasmany)
[hasSole](#method-hassole)
[implode](#method-implode)
[intersect](#method-intersect)
[intersectUsing](#method-intersectusing)
[intersectAssoc](#method-intersectAssoc)
[intersectAssocUsing](#method-intersectassocusing)
[intersectByKeys](#method-intersectbykeys)
[isEmpty](#method-isempty)
[isNotEmpty](#method-isnotempty)
[join](#method-join)
[keyBy](#method-keyby)
[keys](#method-keys)
[last](#method-last)
[lazy](#method-lazy)
[macro](#method-macro)
[make](#method-make)
[map](#method-map)
[mapInto](#method-mapinto)
[mapSpread](#method-mapspread)
[mapToGroups](#method-maptogroups)
[mapWithKeys](#method-mapwithkeys)
[max](#method-max)
[median](#method-median)
[merge](#method-merge)
[mergeRecursive](#method-mergerecursive)
[min](#method-min)
[mode](#method-mode)
[multiply](#method-multiply)
[nth](#method-nth)
[only](#method-only)
[pad](#method-pad)
[partition](#method-partition)
[percentage](#method-percentage)
[pipe](#method-pipe)
[pipeInto](#method-pipeinto)
[pipeThrough](#method-pipethrough)
[pluck](#method-pluck)
[pop](#method-pop)
[prepend](#method-prepend)
[pull](#method-pull)
[push](#method-push)
[put](#method-put)
[random](#method-random)
[range](#method-range)
[reduce](#method-reduce)
[reduceInto](#method-reduce-into)
[reduceSpread](#method-reduce-spread)
[reject](#method-reject)
[replace](#method-replace)
[replaceRecursive](#method-replacerecursive)
[reverse](#method-reverse)
[search](#method-search)
[select](#method-select)
[shift](#method-shift)
[shuffle](#method-shuffle)
[skip](#method-skip)
[skipUntil](#method-skipuntil)
[skipWhile](#method-skipwhile)
[slice](#method-slice)
[sliding](#method-sliding)
[sole](#method-sole)
[some](#method-some)
[sort](#method-sort)
[sortBy](#method-sortby)
[sortByDesc](#method-sortbydesc)
[sortDesc](#method-sortdesc)
[sortKeys](#method-sortkeys)
[sortKeysDesc](#method-sortkeysdesc)
[sortKeysUsing](#method-sortkeysusing)
[splice](#method-splice)
[split](#method-split)
[splitIn](#method-splitin)
[sum](#method-sum)
[take](#method-take)
[takeUntil](#method-takeuntil)
[takeWhile](#method-takewhile)
[tap](#method-tap)
[times](#method-times)
[toArray](#method-toarray)
[toJson](#method-tojson)
[toPrettyJson](#method-to-pretty-json)
[transform](#method-transform)
[undot](#method-undot)
[union](#method-union)
[unique](#method-unique)
[uniqueStrict](#method-uniquestrict)
[unless](#method-unless)
[unlessEmpty](#method-unlessempty)
[unlessNotEmpty](#method-unlessnotempty)
[unwrap](#method-unwrap)
[value](#method-value)
[values](#method-values)
[when](#method-when)
[whenEmpty](#method-whenempty)
[whenNotEmpty](#method-whennotempty)
[where](#method-where)
[whereStrict](#method-wherestrict)
[whereBetween](#method-wherebetween)
[whereIn](#method-wherein)
[whereInStrict](#method-whereinstrict)
[whereInstanceOf](#method-whereinstanceof)
[whereNotBetween](#method-wherenotbetween)
[whereNotIn](#method-wherenotin)
[whereNotInStrict](#method-wherenotinstrict)
[whereNotNull](#method-wherenotnull)
[whereNull](#method-wherenull)
[wrap](#method-wrap)
[zip](#method-zip)

</div>

<a name="method-listing"></a>
## Перелік методів

<style>
    .collection-method code {
        font-size: 14px;
    }

    .collection-method:not(.first-collection-method) {
        margin-top: 50px;
    }
</style>

<a name="method-after"></a>
#### `after()` {.collection-method .first-collection-method}

Метод `after` повертає елемент після заданого. Якщо заданий елемент не знайдено або він останній, повертається `null`:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->after(3);

// 4

$collection->after(5);

// null
```

Цей метод шукає заданий елемент за «нестрогим» порівнянням: рядок із цілим значенням вважається рівним цілому числу з тим самим значенням. Щоб скористатися «строгим» порівнянням, передайте методу аргумент `strict`:

```php
collect([2, 4, 6, 8])->after('4', strict: true);

// null
```

Як варіант, ви можете передати власне замикання, щоб знайти перший елемент, який проходить заданий тест:

```php
collect([2, 4, 6, 8])->after(function (int $item, int $key) {
    return $item > 5;
});

// 8
```

<a name="method-all"></a>
#### `all()` {.collection-method}

Метод `all` повертає масив, який лежить в основі колекції:

```php
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
#### `average()` {.collection-method}

Аліас методу [avg](#method-avg).

<a name="method-avg"></a>
#### `avg()` {.collection-method}

Метод `avg` повертає [середнє значення](https://en.wikipedia.org/wiki/Average) заданого ключа:

```php
$average = collect([
    ['foo' => 10],
    ['foo' => 10],
    ['foo' => 20],
    ['foo' => 40]
])->avg('foo');

// 20

$average = collect([1, 1, 2, 4])->avg();

// 2
```

<a name="method-before"></a>
#### `before()` {.collection-method}

Метод `before` протилежний методу [after](#method-after). Він повертає елемент перед заданим. Якщо заданий елемент не знайдено або він перший, повертається `null`:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->before(3);

// 2

$collection->before(1);

// null

collect([2, 4, 6, 8])->before('4', strict: true);

// null

collect([2, 4, 6, 8])->before(function (int $item, int $key) {
    return $item > 5;
});

// 4
```

<a name="method-chunk"></a>
#### `chunk()` {.collection-method}

Метод `chunk` розбиває колекцію на кілька менших колекцій заданого розміру:

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

Цей метод особливо корисний у [представленнях](/docs/{{version}}/views) під час роботи з сітковими системами на кшталт [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/). Наприклад, уявіть колекцію моделей [Eloquent](/docs/{{version}}/eloquent), яку ви хочете показати сіткою:

```blade
@foreach ($products->chunk(3) as $chunk)
    <div class="row">
        @foreach ($chunk as $product)
            <div class="col-xs-4">{{ $product->name }}</div>
        @endforeach
    </div>
@endforeach
```

<a name="method-chunkwhile"></a>
#### `chunkWhile()` {.collection-method}

Метод `chunkWhile` розбиває колекцію на кілька менших колекцій на основі результату заданого колбека. Змінна `$chunk`, яку передано до замикання, дозволяє перевірити попередній елемент:

```php
$collection = collect(str_split('AABBCCCD'));

$chunks = $collection->chunkWhile(function (string $value, int $key, Collection $chunk) {
    return $value === $chunk->last();
});

$chunks->all();

// [['A', 'A'], ['B', 'B'], ['C', 'C', 'C'], ['D']]
```

<a name="method-collapse"></a>
#### `collapse()` {.collection-method}

Метод `collapse` згортає колекцію масивів або колекцій в одну плоску колекцію:

```php
$collection = collect([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]);

$collapsed = $collection->collapse();

$collapsed->all();

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-collapsewithkeys"></a>
#### `collapseWithKeys()` {.collection-method}

Метод `collapseWithKeys` сплющує колекцію масивів або колекцій в одну колекцію, зберігаючи оригінальні ключі. Якщо колекція вже плоска, він поверне порожню колекцію:

```php
$collection = collect([
    ['first'  => collect([1, 2, 3])],
    ['second' => [4, 5, 6]],
    ['third'  => collect([7, 8, 9])]
]);

$collapsed = $collection->collapseWithKeys();

$collapsed->all();

// [
//     'first'  => [1, 2, 3],
//     'second' => [4, 5, 6],
//     'third'  => [7, 8, 9],
// ]
```

<a name="method-collect"></a>
#### `collect()` {.collection-method}

Метод `collect` повертає новий екземпляр `Collection` з елементами, які наразі є в колекції:

```php
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

Метод `collect` насамперед корисний для перетворення [лінивих колекцій](#lazy-collections) на звичайні екземпляри `Collection`:

```php
$lazyCollection = LazyCollection::make(function () {
    yield 1;
    yield 2;
    yield 3;
});

$collection = $lazyCollection->collect();

$collection::class;

// 'Illuminate\Support\Collection'

$collection->all();

// [1, 2, 3]
```

> [!NOTE]
> Метод `collect` особливо корисний, коли ви маєте екземпляр `Enumerable` і потребуєте неліниву колекцію. Оскільки `collect()` є частиною контракту `Enumerable`, ви можете сміливо користуватися ним, щоб отримати екземпляр `Collection`.

<a name="method-combine"></a>
#### `combine()` {.collection-method}

Метод `combine` поєднує значення колекції як ключі зі значеннями іншого масиву або колекції:

```php
$collection = collect(['name', 'age']);

$combined = $collection->combine(['George', 29]);

$combined->all();

// ['name' => 'George', 'age' => 29]
```

<a name="method-concat"></a>
#### `concat()` {.collection-method}

Метод `concat` додає значення заданого масиву або колекції в кінець іншої колекції:

```php
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

Метод `concat` числово переіндексовує ключі елементів, доданих до оригінальної колекції. Щоб зберегти ключі в асоціативних колекціях, дивіться метод [merge](#method-merge).

<a name="method-contains"></a>
#### `contains()` {.collection-method}

Метод `contains` визначає, чи містить колекція заданий елемент. Ви можете передати методу `contains` замикання, щоб визначити, чи існує в колекції елемент, який проходить заданий тест:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function (int $value, int $key) {
    return $value > 5;
});

// false
```

Як варіант, ви можете передати методу `contains` рядок, щоб визначити, чи містить колекція задане значення елемента:

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

Ви також можете передати методу `contains` пару ключ / значення, і він визначить, чи існує задана пара в колекції:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

Перевіряючи значення елементів, метод `contains` використовує «нестрогі» порівняння: рядок із цілим значенням вважається рівним цілому числу з тим самим значенням. Щоб фільтрувати зі «строгими» порівняннями, скористайтеся методом [containsStrict](#method-containsstrict).

Протилежність `contains` - метод [doesntContain](#method-doesntcontain).

<a name="method-containsstrict"></a>
#### `containsStrict()` {.collection-method}

Цей метод має ту саму сигнатуру, що й метод [contains](#method-contains); проте всі значення порівнюються «строго».

> [!NOTE]
> Поведінка цього методу змінюється під час роботи з [колекціями Eloquent](/docs/{{version}}/eloquent-collections#method-contains).

<a name="method-count"></a>
#### `count()` {.collection-method}

Метод `count` повертає загальну кількість елементів у колекції:

```php
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
#### `countBy()` {.collection-method}

Метод `countBy` рахує входження значень у колекції. За замовчуванням метод рахує входження кожного елемента, що дозволяє порахувати певні «типи» елементів у колекції:

```php
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

Ви можете передати методу `countBy` замикання, щоб порахувати всі елементи за власним значенням:

```php
$collection = collect(['alice@gmail.com', 'bob@yahoo.com', 'carlos@gmail.com']);

$counted = $collection->countBy(function (string $email) {
    return substr(strrchr($email, '@'), 1);
});

$counted->all();

// ['gmail.com' => 2, 'yahoo.com' => 1]
```

<a name="method-crossjoin"></a>
#### `crossJoin()` {.collection-method}

Метод `crossJoin` перехресно поєднує значення колекції із заданими масивами чи колекціями, повертаючи декартів добуток з усіма можливими комбінаціями:

```php
$collection = collect([1, 2]);

$matrix = $collection->crossJoin(['a', 'b']);

$matrix->all();

/*
    [
        [1, 'a'],
        [1, 'b'],
        [2, 'a'],
        [2, 'b'],
    ]
*/

$collection = collect([1, 2]);

$matrix = $collection->crossJoin(['a', 'b'], ['I', 'II']);

$matrix->all();

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

<a name="method-dd"></a>
#### `dd()` {.collection-method}

Метод `dd` виводить елементи колекції та припиняє виконання скрипта:

```php
$collection = collect(['John Doe', 'Jane Doe']);

$collection->dd();

/*
    array:2 [
        0 => "John Doe"
        1 => "Jane Doe"
    ]
*/
```

Якщо ви не хочете зупиняти виконання скрипта, скористайтеся натомість методом [dump](#method-dump).

<a name="method-diff"></a>
#### `diff()` {.collection-method}

Метод `diff` порівнює колекцію з іншою колекцією або звичайним PHP-масивом `array` за значеннями. Цей метод поверне значення оригінальної колекції, яких немає в заданій колекції:

```php
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!NOTE]
> Поведінка цього методу змінюється під час роботи з [колекціями Eloquent](/docs/{{version}}/eloquent-collections#method-diff).

<a name="method-diffassoc"></a>
#### `diffAssoc()` {.collection-method}

Метод `diffAssoc` порівнює колекцію з іншою колекцією або звичайним PHP-масивом `array` за ключами та значеннями. Цей метод поверне пари ключ / значення оригінальної колекції, яких немає в заданій колекції:

```php
$collection = collect([
    'color' => 'orange',
    'type' => 'fruit',
    'remain' => 6,
]);

$diff = $collection->diffAssoc([
    'color' => 'yellow',
    'type' => 'fruit',
    'remain' => 3,
    'used' => 6,
]);

$diff->all();

// ['color' => 'orange', 'remain' => 6]
```

<a name="method-diffassocusing"></a>
#### `diffAssocUsing()` {.collection-method}

На відміну від `diffAssoc`, `diffAssocUsing` приймає задану користувачем функцію-колбек для порівняння індексів:

```php
$collection = collect([
    'color' => 'orange',
    'type' => 'fruit',
    'remain' => 6,
]);

$diff = $collection->diffAssocUsing([
    'Color' => 'yellow',
    'Type' => 'fruit',
    'Remain' => 3,
], 'strnatcasecmp');

$diff->all();

// ['color' => 'orange', 'remain' => 6]
```

Колбек має бути функцією порівняння, яка повертає ціле число менше, рівне або більше за нуль. Докладніше дивіться в документації PHP про [array_diff_uassoc](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters) - саме цю функцію PHP метод `diffAssocUsing` використовує під капотом.

<a name="method-diffkeys"></a>
#### `diffKeys()` {.collection-method}

Метод `diffKeys` порівнює колекцію з іншою колекцією або звичайним PHP-масивом `array` за ключами. Цей метод поверне пари ключ / значення оригінальної колекції, яких немає в заданій колекції:

```php
$collection = collect([
    'one' => 10,
    'two' => 20,
    'three' => 30,
    'four' => 40,
    'five' => 50,
]);

$diff = $collection->diffKeys([
    'two' => 2,
    'four' => 4,
    'six' => 6,
    'eight' => 8,
]);

$diff->all();

// ['one' => 10, 'three' => 30, 'five' => 50]
```

<a name="method-doesntcontain"></a>
#### `doesntContain()` {.collection-method}

Метод `doesntContain` визначає, чи не містить колекція заданий елемент. Ви можете передати методу `doesntContain` замикання, щоб визначити, чи не існує в колекції елемента, який проходить заданий тест:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function (int $value, int $key) {
    return $value < 5;
});

// false
```

Як варіант, ви можете передати методу `doesntContain` рядок, щоб визначити, чи не містить колекція задане значення елемента:

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->doesntContain('Table');

// true

$collection->doesntContain('Desk');

// false
```

Ви також можете передати методу `doesntContain` пару ключ / значення, і він визначить, чи не існує задана пара в колекції:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->doesntContain('product', 'Bookcase');

// true
```

Перевіряючи значення елементів, метод `doesntContain` використовує «нестрогі» порівняння: рядок із цілим значенням вважається рівним цілому числу з тим самим значенням.

<a name="method-doesntcontainstrict"></a>
#### `doesntContainStrict()` {.collection-method}

Цей метод має ту саму сигнатуру, що й метод [doesntContain](#method-doesntcontain); проте всі значення порівнюються «строго».

<a name="method-dot"></a>
#### `dot()` {.collection-method}

Метод `dot` сплющує багатовимірну колекцію в одновимірну, використовуючи «крапкову» нотацію для позначення вкладеності:

```php
$collection = collect(['products' => ['desk' => ['price' => 100]]]);

$flattened = $collection->dot();

$flattened->all();

// ['products.desk.price' => 100]
```

<a name="method-dump"></a>
#### `dump()` {.collection-method}

Метод `dump` виводить елементи колекції:

```php
$collection = collect(['John Doe', 'Jane Doe']);

$collection->dump();

/*
    array:2 [
        0 => "John Doe"
        1 => "Jane Doe"
    ]
*/
```

Якщо ви хочете припинити виконання скрипта після виведення колекції, скористайтеся натомість методом [dd](#method-dd).

<a name="method-duplicates"></a>
#### `duplicates()` {.collection-method}

Метод `duplicates` дістає й повертає значення-дублікати з колекції:

```php
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

Якщо колекція містить масиви або об'єкти, ви можете передати ключ атрибутів, які треба перевірити на дублікати:

```php
$employees = collect([
    ['email' => 'abigail@example.com', 'position' => 'Developer'],
    ['email' => 'james@example.com', 'position' => 'Designer'],
    ['email' => 'victoria@example.com', 'position' => 'Developer'],
]);

$employees->duplicates('position');

// [2 => 'Developer']
```

<a name="method-duplicatesstrict"></a>
#### `duplicatesStrict()` {.collection-method}

Цей метод має ту саму сигнатуру, що й метод [duplicates](#method-duplicates); проте всі значення порівнюються «строго».

<a name="method-each"></a>
#### `each()` {.collection-method}

Метод `each` проходить елементи колекції й передає кожен елемент до замикання:

```php
$collection = collect([1, 2, 3, 4]);

$collection->each(function (int $item, int $key) {
    // ...
});
```

Якщо ви хочете припинити обхід елементів, поверніть із замикання `false`:

```php
$collection->each(function (int $item, int $key) {
    if (/* condition */) {
        return false;
    }
});
```

<a name="method-eachspread"></a>
#### `eachSpread()` {.collection-method}

Метод `eachSpread` проходить елементи колекції, передаючи значення кожного вкладеного елемента до заданого колбека:

```php
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function (string $name, int $age) {
    // ...
});
```

Ви можете припинити обхід елементів, повернувши з колбека `false`:

```php
$collection->eachSpread(function (string $name, int $age) {
    return false;
});
```

<a name="method-ensure"></a>
#### `ensure()` {.collection-method}

Метод `ensure` дозволяє перевірити, що всі елементи колекції належать до заданого типу чи списку типів. Інакше буде викинуто `UnexpectedValueException`:

```php
return $collection->ensure(User::class);

return $collection->ensure([User::class, Customer::class]);
```

Можна вказати й примітивні типи на кшталт `string`, `int`, `float`, `bool` та `array`:

```php
return $collection->ensure('int');
```

> [!WARNING]
> Метод `ensure` не гарантує, що елементи інших типів не буде додано до колекції пізніше.

<a name="method-every"></a>
#### `every()` {.collection-method}

Метод `every` дозволяє перевірити, що всі елементи колекції проходять заданий тест:

```php
collect([1, 2, 3, 4])->every(function (int $value, int $key) {
    return $value > 2;
});

// false
```

Якщо колекція порожня, метод `every` поверне true:

```php
$collection = collect([]);

$collection->every(function (int $value, int $key) {
    return $value > 2;
});

// true
```

<a name="method-except"></a>
#### `except()` {.collection-method}

Метод `except` повертає всі елементи колекції, окрім тих, що мають вказані ключі:

```php
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

Протилежність `except` - метод [only](#method-only).

> [!NOTE]
> Поведінка цього методу змінюється під час роботи з [колекціями Eloquent](/docs/{{version}}/eloquent-collections#method-except).

<a name="method-filter"></a>
#### `filter()` {.collection-method}

Метод `filter` фільтрує колекцію заданим колбеком, лишаючи тільки ті елементи, які проходять заданий тест:

```php
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

Якщо колбек не передано, буде вилучено всі елементи колекції, еквівалентні `false`:

```php
$collection = collect([1, 2, 3, null, false, '', 0, []]);

$collection->filter()->all();

// [1, 2, 3]
```

Протилежність `filter` - метод [reject](#method-reject).

<a name="method-first"></a>
#### `first()` {.collection-method}

Метод `first` повертає перший елемент колекції, який проходить заданий тест:

```php
collect([1, 2, 3, 4])->first(function (int $value, int $key) {
    return $value > 2;
});

// 3
```

Ви також можете викликати метод `first` без аргументів, щоб отримати перший елемент колекції. Якщо колекція порожня, повертається `null`:

```php
collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-or-fail"></a>
#### `firstOrFail()` {.collection-method}

Метод `firstOrFail` ідентичний методу `first`; проте, якщо результату не знайдено, буде викинуто виняток `Illuminate\Support\ItemNotFoundException`:

```php
collect([1, 2, 3, 4])->firstOrFail(function (int $value, int $key) {
    return $value > 5;
});

// Throws ItemNotFoundException...
```

Ви також можете викликати метод `firstOrFail` без аргументів, щоб отримати перший елемент колекції. Якщо колекція порожня, буде викинуто виняток `Illuminate\Support\ItemNotFoundException`:

```php
collect([])->firstOrFail();

// Throws ItemNotFoundException...
```

<a name="method-first-where"></a>
#### `firstWhere()` {.collection-method}

Метод `firstWhere` повертає перший елемент колекції із заданою парою ключ / значення:

```php
$collection = collect([
    ['name' => 'Regena', 'age' => null],
    ['name' => 'Linda', 'age' => 14],
    ['name' => 'Diego', 'age' => 23],
    ['name' => 'Linda', 'age' => 84],
]);

$collection->firstWhere('name', 'Linda');

// ['name' => 'Linda', 'age' => 14]
```

Ви також можете викликати метод `firstWhere` з оператором порівняння:

```php
$collection->firstWhere('age', '>=', 18);

// ['name' => 'Diego', 'age' => 23]
```

Як і методу [where](#method-where), методу `firstWhere` можна передати один аргумент. У такому разі `firstWhere` поверне перший елемент, у якого значення заданого ключа є «істинним»:

```php
$collection->firstWhere('age');

// ['name' => 'Linda', 'age' => 14]
```

<a name="method-flatmap"></a>
#### `flatMap()` {.collection-method}

Метод `flatMap` проходить колекцію й передає кожне значення до заданого замикання. Замикання вільне змінити елемент і повернути його, утворюючи так нову колекцію змінених елементів. Потім масив сплющується на один рівень:

```php
$collection = collect([
    ['name' => 'Sally'],
    ['school' => 'Arkansas'],
    ['age' => 28]
]);

$flattened = $collection->flatMap(function (array $values) {
    return array_map('strtoupper', $values);
});

$flattened->all();

// ['name' => 'SALLY', 'school' => 'ARKANSAS', 'age' => '28'];
```

<a name="method-flatten"></a>
#### `flatten()` {.collection-method}

Метод `flatten` сплющує багатовимірну колекцію в одновимірну:

```php
$collection = collect([
    'name' => 'Taylor',
    'languages' => [
        'PHP', 'JavaScript'
    ]
]);

$flattened = $collection->flatten();

$flattened->all();

// ['Taylor', 'PHP', 'JavaScript'];
```

За потреби ви можете передати методу `flatten` аргумент «глибини»:

```php
$collection = collect([
    'Apple' => [
        [
            'name' => 'iPhone 6S',
            'brand' => 'Apple'
        ],
    ],
    'Samsung' => [
        [
            'name' => 'Galaxy S7',
            'brand' => 'Samsung'
        ],
    ],
]);

$products = $collection->flatten(1);

$products->values()->all();

/*
    [
        ['name' => 'iPhone 6S', 'brand' => 'Apple'],
        ['name' => 'Galaxy S7', 'brand' => 'Samsung'],
    ]
*/
```

У цьому прикладі виклик `flatten` без глибини сплющив би й вкладені масиви, давши `['iPhone 6S', 'Apple', 'Galaxy S7', 'Samsung']`. Глибина дозволяє вказати, на скільки рівнів сплющувати вкладені масиви.

<a name="method-flip"></a>
#### `flip()` {.collection-method}

Метод `flip` міняє місцями ключі колекції з відповідними значеннями:

```php
$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

$flipped = $collection->flip();

$flipped->all();

// ['Taylor' => 'name', 'Laravel' => 'framework']
```

<a name="method-forget"></a>
#### `forget()` {.collection-method}

Метод `forget` вилучає елемент з колекції за його ключем:

```php
$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

// Forget a single key...
$collection->forget('name');

// ['framework' => 'Laravel']

// Forget multiple keys...
$collection->forget(['name', 'framework']);

// []
```

> [!WARNING]
> На відміну від більшості інших методів колекції, `forget` не повертає нову змінену колекцію: він змінює й повертає ту колекцію, на якій його викликано.

<a name="method-forpage"></a>
#### `forPage()` {.collection-method}

Метод `forPage` повертає нову колекцію з елементами, які були б на заданій сторінці. Першим аргументом метод приймає номер сторінки, другим - кількість елементів на сторінці:

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunk = $collection->forPage(2, 3);

$chunk->all();

// [4, 5, 6]
```

<a name="method-fromjson"></a>
#### `fromJson()` {.collection-method}

Статичний метод `fromJson` створює новий екземпляр колекції, декодуючи заданий JSON-рядок PHP-функцією `json_decode`:

```php
use Illuminate\Support\Collection;

$json = json_encode([
    'name' => 'Taylor Otwell',
    'role' => 'Developer',
    'status' => 'Active',
]);

$collection = Collection::fromJson($json);
```

<a name="method-get"></a>
#### `get()` {.collection-method}

Метод `get` повертає елемент за заданим ключем. Якщо ключа не існує, повертається `null`:

```php
$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

$value = $collection->get('name');

// Taylor
```

Другим аргументом ви можете передати значення за замовчуванням:

```php
$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

$value = $collection->get('age', 34);

// 34
```

Як значення за замовчуванням методу можна передати навіть колбек. Якщо вказаного ключа не існує, буде повернуто результат колбека:

```php
$collection->get('email', function () {
    return 'taylor@example.com';
});

// taylor@example.com
```

<a name="method-groupby"></a>
#### `groupBy()` {.collection-method}

Метод `groupBy` групує елементи колекції за заданим ключем:

```php
$collection = collect([
    ['account_id' => 'account-x10', 'product' => 'Chair'],
    ['account_id' => 'account-x10', 'product' => 'Bookcase'],
    ['account_id' => 'account-x11', 'product' => 'Desk'],
]);

$grouped = $collection->groupBy('account_id');

$grouped->all();

/*
    [
        'account-x10' => [
            ['account_id' => 'account-x10', 'product' => 'Chair'],
            ['account_id' => 'account-x10', 'product' => 'Bookcase'],
        ],
        'account-x11' => [
            ['account_id' => 'account-x11', 'product' => 'Desk'],
        ],
    ]
*/
```

Замість рядкового `key` ви можете передати колбек. Колбек має повернути значення, за яким ви хочете згрупувати:

```php
$grouped = $collection->groupBy(function (array $item, int $key) {
    return substr($item['account_id'], -3);
});

$grouped->all();

/*
    [
        'x10' => [
            ['account_id' => 'account-x10', 'product' => 'Chair'],
            ['account_id' => 'account-x10', 'product' => 'Bookcase'],
        ],
        'x11' => [
            ['account_id' => 'account-x11', 'product' => 'Desk'],
        ],
    ]
*/
```

Кілька критеріїв групування можна передати масивом. Кожен елемент масиву буде застосовано до відповідного рівня багатовимірного масиву:

```php
$data = new Collection([
    10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],
    20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],
    30 => ['user' => 3, 'skill' => 2, 'roles' => ['Role_1']],
    40 => ['user' => 4, 'skill' => 2, 'roles' => ['Role_2']],
]);

$result = $data->groupBy(['skill', function (array $item) {
    return $item['roles'];
}], preserveKeys: true);

/*
[
    1 => [
        'Role_1' => [
            10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],
            20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],
        ],
        'Role_2' => [
            20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],
        ],
        'Role_3' => [
            10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],
        ],
    ],
    2 => [
        'Role_1' => [
            30 => ['user' => 3, 'skill' => 2, 'roles' => ['Role_1']],
        ],
        'Role_2' => [
            40 => ['user' => 4, 'skill' => 2, 'roles' => ['Role_2']],
        ],
    ],
];
*/
```

<a name="method-has"></a>
#### `has()` {.collection-method}

Метод `has` визначає, чи існує заданий ключ у колекції:

```php
$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

$collection->has('product');

// true

$collection->has(['product', 'amount']);

// true

$collection->has(['amount', 'price']);

// false
```

<a name="method-hasany"></a>
#### `hasAny()` {.collection-method}

Метод `hasAny` визначає, чи існує в колекції хоч один із заданих ключів:

```php
$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

$collection->hasAny(['product', 'price']);

// true

$collection->hasAny(['name', 'price']);

// false
```

<a name="method-hasmany"></a>
#### `hasMany()` {.collection-method}

Метод `hasMany` визначає, чи містить колекція кілька елементів:

```php
collect([])->hasMany();

// false

collect(['1'])->hasMany();

// false

collect([1, 2, 3])->hasMany();

// true

collect([
    ['age' => 2],
    ['age' => 3],
])->hasMany(fn ($item) => $item['age'] === 2)

// false
```

<a name="method-hassole"></a>
#### `hasSole()` {.collection-method}

Метод `hasSole` визначає, чи містить колекція єдиний елемент - за потреби той, що відповідає заданим критеріям:

```php
collect([])->hasSole();

// false

collect(['1'])->hasSole();

// true

collect([1, 2, 3])->hasSole(fn (int $item) => $item === 2);

// true
```

<a name="method-implode"></a>
#### `implode()` {.collection-method}

Метод `implode` склеює елементи колекції. Його аргументи залежать від типу елементів у колекції. Якщо колекція містить масиви або об'єкти, передайте ключ атрибутів, які треба склеїти, і рядок-«клей», який слід поставити між значеннями:

```php
$collection = collect([
    ['account_id' => 1, 'product' => 'Desk'],
    ['account_id' => 2, 'product' => 'Chair'],
]);

$collection->implode('product', ', ');

// 'Desk, Chair'
```

Якщо колекція містить прості рядки чи числові значення, передайте методу «клей» єдиним аргументом:

```php
collect([1, 2, 3, 4, 5])->implode('-');

// '1-2-3-4-5'
```

Якщо ви хочете відформатувати значення, які склеюються, передайте методу `implode` замикання:

```php
$collection->implode(function (array $item, int $key) {
    return strtoupper($item['product']);
}, ', ');

// 'DESK, CHAIR'
```

<a name="method-intersect"></a>
#### `intersect()` {.collection-method}

Метод `intersect` вилучає з оригінальної колекції всі значення, яких немає в заданому масиві чи колекції. Отримана колекція збереже ключі оригінальної:

```php
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

> [!NOTE]
> Поведінка цього методу змінюється під час роботи з [колекціями Eloquent](/docs/{{version}}/eloquent-collections#method-intersect).

<a name="method-intersectusing"></a>
#### `intersectUsing()` {.collection-method}

Метод `intersectUsing` вилучає з оригінальної колекції всі значення, яких немає в заданому масиві чи колекції, порівнюючи значення власним колбеком. Отримана колекція збереже ключі оригінальної:

```php
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersectUsing(['desk', 'chair', 'bookcase'], function (string $a, string $b) {
    return strcasecmp($a, $b);
});

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

<a name="method-intersectAssoc"></a>
#### `intersectAssoc()` {.collection-method}

Метод `intersectAssoc` порівнює оригінальну колекцію з іншою колекцією чи масивом, повертаючи пари ключ / значення, які є в усіх заданих колекціях:

```php
$collection = collect([
    'color' => 'red',
    'size' => 'M',
    'material' => 'cotton'
]);

$intersect = $collection->intersectAssoc([
    'color' => 'blue',
    'size' => 'M',
    'material' => 'polyester'
]);

$intersect->all();

// ['size' => 'M']
```

<a name="method-intersectassocusing"></a>
#### `intersectAssocUsing()` {.collection-method}

Метод `intersectAssocUsing` порівнює оригінальну колекцію з іншою колекцією чи масивом, повертаючи пари ключ / значення, які є в обох, і визначає рівність ключів та значень власним колбеком порівняння:

```php
$collection = collect([
    'color' => 'red',
    'Size' => 'M',
    'material' => 'cotton',
]);

$intersect = $collection->intersectAssocUsing([
    'color' => 'blue',
    'size' => 'M',
    'material' => 'polyester',
], function (string $a, string $b) {
    return strcasecmp($a, $b);
});

$intersect->all();

// ['Size' => 'M']
```

<a name="method-intersectbykeys"></a>
#### `intersectByKeys()` {.collection-method}

Метод `intersectByKeys` вилучає з оригінальної колекції всі ключі та їхні значення, яких немає в заданому масиві чи колекції:

```php
$collection = collect([
    'serial' => 'UX301', 'type' => 'screen', 'year' => 2009,
]);

$intersect = $collection->intersectByKeys([
    'reference' => 'UX404', 'type' => 'tab', 'year' => 2011,
]);

$intersect->all();

// ['type' => 'screen', 'year' => 2009]
```

<a name="method-isempty"></a>
#### `isEmpty()` {.collection-method}

Метод `isEmpty` повертає `true`, якщо колекція порожня; інакше повертається `false`:

```php
collect([])->isEmpty();

// true
```

<a name="method-isnotempty"></a>
#### `isNotEmpty()` {.collection-method}

Метод `isNotEmpty` повертає `true`, якщо колекція не порожня; інакше повертається `false`:

```php
collect([])->isNotEmpty();

// false
```

<a name="method-join"></a>
#### `join()` {.collection-method}

Метод `join` склеює значення колекції рядком. Другим аргументом цього методу ви можете вказати, як до рядка слід додати останній елемент:

```php
collect(['a', 'b', 'c'])->join(', '); // 'a, b, c'
collect(['a', 'b', 'c'])->join(', ', ', and '); // 'a, b, and c'
collect(['a', 'b'])->join(', ', ' and '); // 'a and b'
collect(['a'])->join(', ', ' and '); // 'a'
collect([])->join(', ', ' and '); // ''
```

<a name="method-keyby"></a>
#### `keyBy()` {.collection-method}

Метод `keyBy` робить заданий ключ ключем колекції. Якщо кілька елементів мають однаковий ключ, у новій колекції залишиться тільки останній:

```php
$collection = collect([
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$keyed = $collection->keyBy('product_id');

$keyed->all();

/*
    [
        'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
        'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]
*/
```

Ви також можете передати методу колбек. Колбек має повернути значення, яке стане ключем колекції:

```php
$keyed = $collection->keyBy(function (array $item, int $key) {
    return strtoupper($item['product_id']);
});

$keyed->all();

/*
    [
        'PROD-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
        'PROD-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]
*/
```

<a name="method-keys"></a>
#### `keys()` {.collection-method}

Метод `keys` повертає всі ключі колекції:

```php
$collection = collect([
    'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
    'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$keys = $collection->keys();

$keys->all();

// ['prod-100', 'prod-200']
```

<a name="method-last"></a>
#### `last()` {.collection-method}

Метод `last` повертає останній елемент колекції, який проходить заданий тест:

```php
collect([1, 2, 3, 4])->last(function (int $value, int $key) {
    return $value < 3;
});

// 2
```

Ви також можете викликати метод `last` без аргументів, щоб отримати останній елемент колекції. Якщо колекція порожня, повертається `null`:

```php
collect([1, 2, 3, 4])->last();

// 4
```

<a name="method-lazy"></a>
#### `lazy()` {.collection-method}

Метод `lazy` повертає новий екземпляр [LazyCollection](#lazy-collections) з масиву елементів під капотом:

```php
$lazyCollection = collect([1, 2, 3, 4])->lazy();

$lazyCollection::class;

// Illuminate\Support\LazyCollection

$lazyCollection->all();

// [1, 2, 3, 4]
```

Це особливо корисно, коли вам потрібно виконати перетворення над величезною `Collection` з великою кількістю елементів:

```php
$count = $hugeCollection
    ->lazy()
    ->where('country', 'FR')
    ->where('balance', '>', '100')
    ->count();
```

Перетворивши колекцію на `LazyCollection`, ми уникаємо виділення купи додаткової пам'яті. Хоч оригінальна колекція й далі тримає _свої_ значення в пам'яті, наступні фільтри цього вже не роблять. Тож під час фільтрування результатів колекції додаткова пам'ять практично не виділяється.

<a name="method-macro"></a>
#### `macro()` {.collection-method}

Статичний метод `macro` дозволяє додавати методи до класу `Collection` під час виконання. Докладніше дивіться в документації про [розширення колекцій](#extending-collections).

<a name="method-make"></a>
#### `make()` {.collection-method}

Статичний метод `make` створює новий екземпляр колекції. Дивіться розділ [Створення колекцій](#creating-collections).

```php
use Illuminate\Support\Collection;

$collection = Collection::make([1, 2, 3]);
```

<a name="method-map"></a>
#### `map()` {.collection-method}

Метод `map` проходить колекцію й передає кожне значення до заданого колбека. Колбек вільний змінити елемент і повернути його, утворюючи так нову колекцію змінених елементів:

```php
$collection = collect([1, 2, 3, 4, 5]);

$multiplied = $collection->map(function (int $item, int $key) {
    return $item * 2;
});

$multiplied->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> Як і більшість інших методів колекції, `map` повертає новий екземпляр колекції: він не змінює ту колекцію, на якій його викликано. Якщо ви хочете перетворити оригінальну колекцію, скористайтеся методом [transform](#method-transform).

<a name="method-mapinto"></a>
#### `mapInto()` {.collection-method}

Метод `mapInto()` проходить колекцію, створюючи новий екземпляр заданого класу й передаючи значення в конструктор:

```php
class Currency
{
    /**
     * Create a new currency instance.
     */
    function __construct(
        public string $code,
    ) {}
}

$collection = collect(['USD', 'EUR', 'GBP']);

$currencies = $collection->mapInto(Currency::class);

$currencies->all();

// [Currency('USD'), Currency('EUR'), Currency('GBP')]
```

<a name="method-mapspread"></a>
#### `mapSpread()` {.collection-method}

Метод `mapSpread` проходить елементи колекції, передаючи значення кожного вкладеного елемента до заданого замикання. Замикання вільне змінити елемент і повернути його, утворюючи так нову колекцію змінених елементів:

```php
$collection = collect([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunks = $collection->chunk(2);

$sequence = $chunks->mapSpread(function (int $even, int $odd) {
    return $even + $odd;
});

$sequence->all();

// [1, 5, 9, 13, 17]
```

<a name="method-maptogroups"></a>
#### `mapToGroups()` {.collection-method}

Метод `mapToGroups` групує елементи колекції заданим замиканням. Замикання має повернути асоціативний масив з єдиною парою ключ / значення, утворюючи так нову колекцію згрупованих значень:

```php
$collection = collect([
    [
        'name' => 'John Doe',
        'department' => 'Sales',
    ],
    [
        'name' => 'Jane Doe',
        'department' => 'Sales',
    ],
    [
        'name' => 'Johnny Doe',
        'department' => 'Marketing',
    ]
]);

$grouped = $collection->mapToGroups(function (array $item, int $key) {
    return [$item['department'] => $item['name']];
});

$grouped->all();

/*
    [
        'Sales' => ['John Doe', 'Jane Doe'],
        'Marketing' => ['Johnny Doe'],
    ]
*/

$grouped->get('Sales')->all();

// ['John Doe', 'Jane Doe']
```

<a name="method-mapwithkeys"></a>
#### `mapWithKeys()` {.collection-method}

Метод `mapWithKeys` проходить колекцію й передає кожне значення до заданого колбека. Колбек має повернути асоціативний масив з єдиною парою ключ / значення:

```php
$collection = collect([
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
]);

$keyed = $collection->mapWithKeys(function (array $item, int $key) {
    return [$item['email'] => $item['name']];
});

$keyed->all();

/*
    [
        'john@example.com' => 'John',
        'jane@example.com' => 'Jane',
    ]
*/
```

<a name="method-max"></a>
#### `max()` {.collection-method}

Метод `max` повертає максимальне значення заданого ключа:

```php
$max = collect([
    ['foo' => 10],
    ['foo' => 20]
])->max('foo');

// 20

$max = collect([1, 2, 3, 4, 5])->max();

// 5
```

<a name="method-median"></a>
#### `median()` {.collection-method}

Метод `median` повертає [медіанне значення](https://en.wikipedia.org/wiki/Median) заданого ключа:

```php
$median = collect([
    ['foo' => 10],
    ['foo' => 10],
    ['foo' => 20],
    ['foo' => 40]
])->median('foo');

// 15

$median = collect([1, 1, 2, 4])->median();

// 1.5
```

<a name="method-merge"></a>
#### `merge()` {.collection-method}

Метод `merge` зливає заданий масив чи колекцію з оригінальною колекцією. Якщо рядковий ключ у заданих елементах збігається з рядковим ключем в оригінальній колекції, значення заданого елемента перезапише значення в оригінальній колекції:

```php
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->merge(['price' => 200, 'discount' => false]);

$merged->all();

// ['product_id' => 1, 'price' => 200, 'discount' => false]
```

Якщо ключі заданого елемента числові, значення буде додано в кінець колекції:

```php
$collection = collect(['Desk', 'Chair']);

$merged = $collection->merge(['Bookcase', 'Door']);

$merged->all();

// ['Desk', 'Chair', 'Bookcase', 'Door']
```

<a name="method-mergerecursive"></a>
#### `mergeRecursive()` {.collection-method}

Метод `mergeRecursive` рекурсивно зливає заданий масив чи колекцію з оригінальною колекцією. Якщо рядковий ключ у заданих елементах збігається з рядковим ключем в оригінальній колекції, значення цих ключів зливаються в масив - і так рекурсивно:

```php
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->mergeRecursive([
    'product_id' => 2,
    'price' => 200,
    'discount' => false
]);

$merged->all();

// ['product_id' => [1, 2], 'price' => [100, 200], 'discount' => false]
```

<a name="method-min"></a>
#### `min()` {.collection-method}

Метод `min` повертає мінімальне значення заданого ключа:

```php
$min = collect([
    ['foo' => 10],
    ['foo' => 20]
])->min('foo');

// 10

$min = collect([1, 2, 3, 4, 5])->min();

// 1
```

<a name="method-mode"></a>
#### `mode()` {.collection-method}

Метод `mode` повертає [моду](https://en.wikipedia.org/wiki/Mode_(statistics)) заданого ключа:

```php
$mode = collect([
    ['foo' => 10],
    ['foo' => 10],
    ['foo' => 20],
    ['foo' => 40]
])->mode('foo');

// [10]

$mode = collect([1, 1, 2, 4])->mode();

// [1]

$mode = collect([1, 1, 2, 2])->mode();

// [1, 2]
```

<a name="method-multiply"></a>
#### `multiply()` {.collection-method}

Метод `multiply` створює вказану кількість копій усіх елементів колекції:

```php
$users = collect([
    ['name' => 'User #1', 'email' => 'user1@example.com'],
    ['name' => 'User #2', 'email' => 'user2@example.com'],
])->multiply(3);

/*
    [
        ['name' => 'User #1', 'email' => 'user1@example.com'],
        ['name' => 'User #2', 'email' => 'user2@example.com'],
        ['name' => 'User #1', 'email' => 'user1@example.com'],
        ['name' => 'User #2', 'email' => 'user2@example.com'],
        ['name' => 'User #1', 'email' => 'user1@example.com'],
        ['name' => 'User #2', 'email' => 'user2@example.com'],
    ]
*/
```

<a name="method-nth"></a>
#### `nth()` {.collection-method}

Метод `nth` створює нову колекцію з кожного n-го елемента:

```php
$collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

$collection->nth(4);

// ['a', 'e']
```

Другим аргументом ви можете передати початковий зсув:

```php
$collection->nth(4, 1);

// ['b', 'f']
```

<a name="method-only"></a>
#### `only()` {.collection-method}

Метод `only` повертає елементи колекції з вказаними ключами:

```php
$collection = collect([
    'product_id' => 1,
    'name' => 'Desk',
    'price' => 100,
    'discount' => false
]);

$filtered = $collection->only(['product_id', 'name']);

$filtered->all();

// ['product_id' => 1, 'name' => 'Desk']
```

Протилежність `only` - метод [except](#method-except).

> [!NOTE]
> Поведінка цього методу змінюється під час роботи з [колекціями Eloquent](/docs/{{version}}/eloquent-collections#method-only).

<a name="method-pad"></a>
#### `pad()` {.collection-method}

Метод `pad` заповнює масив заданим значенням, доки той не досягне вказаного розміру. Цей метод поводиться як PHP-функція [array_pad](https://secure.php.net/manual/en/function.array-pad.php).

Щоб доповнити зліва, вкажіть від'ємний розмір. Якщо абсолютне значення заданого розміру менше або дорівнює довжині масиву, доповнення не відбудеться:

```php
$collection = collect(['A', 'B', 'C']);

$filtered = $collection->pad(5, 0);

$filtered->all();

// ['A', 'B', 'C', 0, 0]

$filtered = $collection->pad(-5, 0);

$filtered->all();

// [0, 0, 'A', 'B', 'C']
```

<a name="method-partition"></a>
#### `partition()` {.collection-method}

Метод `partition` можна поєднати з деструктуризацією масивів PHP, щоб відділити елементи, які проходять заданий тест, від тих, які його не проходять:

```php
$collection = collect([1, 2, 3, 4, 5, 6]);

[$underThree, $equalOrAboveThree] = $collection->partition(function (int $i) {
    return $i < 3;
});

$underThree->all();

// [1, 2]

$equalOrAboveThree->all();

// [3, 4, 5, 6]
```

> [!NOTE]
> Поведінка цього методу змінюється під час роботи з [колекціями Eloquent](/docs/{{version}}/eloquent-collections#method-partition).

<a name="method-percentage"></a>
#### `percentage()` {.collection-method}

Метод `percentage` дозволяє швидко визначити відсоток елементів колекції, які проходять заданий тест:

```php
$collection = collect([1, 1, 2, 2, 2, 3]);

$percentage = $collection->percentage(fn (int $value) => $value === 1);

// 33.33
```

За замовчуванням відсоток округлюється до двох знаків після коми. Проте ви можете змінити цю поведінку, передавши методу другий аргумент:

```php
$percentage = $collection->percentage(fn (int $value) => $value === 1, precision: 3);

// 33.333
```

<a name="method-pipe"></a>
#### `pipe()` {.collection-method}

Метод `pipe` передає колекцію до заданого замикання й повертає результат його виконання:

```php
$collection = collect([1, 2, 3]);

$piped = $collection->pipe(function (Collection $collection) {
    return $collection->sum();
});

// 6
```

<a name="method-pipeinto"></a>
#### `pipeInto()` {.collection-method}

Метод `pipeInto` створює новий екземпляр заданого класу й передає колекцію в конструктор:

```php
class ResourceCollection
{
    /**
     * Create a new ResourceCollection instance.
     */
    public function __construct(
        public Collection $collection,
    ) {}
}

$collection = collect([1, 2, 3]);

$resource = $collection->pipeInto(ResourceCollection::class);

$resource->collection->all();

// [1, 2, 3]
```

<a name="method-pipethrough"></a>
#### `pipeThrough()` {.collection-method}

Метод `pipeThrough` передає колекцію до заданого масиву замикань і повертає результат їх виконання:

```php
use Illuminate\Support\Collection;

$collection = collect([1, 2, 3]);

$result = $collection->pipeThrough([
    function (Collection $collection) {
        return $collection->merge([4, 5]);
    },
    function (Collection $collection) {
        return $collection->sum();
    },
]);

// 15
```

<a name="method-pluck"></a>
#### `pluck()` {.collection-method}

Метод `pluck` дістає всі значення за заданим ключем:

```php
$collection = collect([
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$plucked = $collection->pluck('name');

$plucked->all();

// ['Desk', 'Chair']
```

Ви також можете вказати, за яким ключем має будуватися отримана колекція:

```php
$plucked = $collection->pluck('name', 'product_id');

$plucked->all();

// ['prod-100' => 'Desk', 'prod-200' => 'Chair']
```

Метод `pluck` також підтримує отримання вкладених значень за «крапковою» нотацією:

```php
$collection = collect([
    [
        'name' => 'Laracon',
        'speakers' => [
            'first_day' => ['Rosa', 'Judith'],
        ],
    ],
    [
        'name' => 'VueConf',
        'speakers' => [
            'first_day' => ['Abigail', 'Joey'],
        ],
    ],
]);

$plucked = $collection->pluck('speakers.first_day');

$plucked->all();

// [['Rosa', 'Judith'], ['Abigail', 'Joey']]
```

Якщо трапляються однакові ключі, до отриманої колекції потрапить останній відповідний елемент:

```php
$collection = collect([
    ['brand' => 'Tesla',  'color' => 'red'],
    ['brand' => 'Pagani', 'color' => 'white'],
    ['brand' => 'Tesla',  'color' => 'black'],
    ['brand' => 'Pagani', 'color' => 'orange'],
]);

$plucked = $collection->pluck('color', 'brand');

$plucked->all();

// ['Tesla' => 'black', 'Pagani' => 'orange']
```

<a name="method-pop"></a>
#### `pop()` {.collection-method}

Метод `pop` вилучає й повертає останній елемент колекції. Якщо колекція порожня, буде повернуто `null`:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop();

// 5

$collection->all();

// [1, 2, 3, 4]
```

Ви можете передати методу `pop` ціле число, щоб вилучити й повернути кілька елементів з кінця колекції:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop(3);

// collect([5, 4, 3])

$collection->all();

// [1, 2]
```

<a name="method-prepend"></a>
#### `prepend()` {.collection-method}

Метод `prepend` додає елемент на початок колекції:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->prepend(0);

$collection->all();

// [0, 1, 2, 3, 4, 5]
```

Другим аргументом ви можете вказати ключ доданого елемента:

```php
$collection = collect(['one' => 1, 'two' => 2]);

$collection->prepend(0, 'zero');

$collection->all();

// ['zero' => 0, 'one' => 1, 'two' => 2]
```

<a name="method-pull"></a>
#### `pull()` {.collection-method}

Метод `pull` вилучає й повертає елемент колекції за його ключем:

```php
$collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

$collection->pull('name');

// 'Desk'

$collection->all();

// ['product_id' => 'prod-100']
```

<a name="method-push"></a>
#### `push()` {.collection-method}

Метод `push` додає елемент у кінець колекції:

```php
$collection = collect([1, 2, 3, 4]);

$collection->push(5);

$collection->all();

// [1, 2, 3, 4, 5]
```

Ви також можете передати кілька елементів, щоб додати їх у кінець колекції:

```php
$collection = collect([1, 2, 3, 4]);

$collection->push(5, 6, 7);
 
$collection->all();
 
// [1, 2, 3, 4, 5, 6, 7]
```

<a name="method-put"></a>
#### `put()` {.collection-method}

Метод `put` встановлює в колекції заданий ключ і значення:

```php
$collection = collect(['product_id' => 1, 'name' => 'Desk']);

$collection->put('price', 100);

$collection->all();

// ['product_id' => 1, 'name' => 'Desk', 'price' => 100]
```

<a name="method-random"></a>
#### `random()` {.collection-method}

Метод `random` повертає випадковий елемент колекції:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->random();

// 4 - (retrieved randomly)
```

Ви можете передати `random` ціле число, щоб вказати, скільки елементів дістати випадково. Коли ви явно передаєте кількість потрібних елементів, завжди повертається колекція:

```php
$random = $collection->random(3);

$random->all();

// [2, 4, 5] - (retrieved randomly)
```

Якщо в екземплярі колекції менше елементів, ніж запитано, метод `random` викине `InvalidArgumentException`.

Метод `random` також приймає замикання, яке отримає поточний екземпляр колекції:

```php
use Illuminate\Support\Collection;

$random = $collection->random(fn (Collection $items) => min(10, count($items)));

$random->all();

// [1, 2, 3, 4, 5] - (retrieved randomly)
```

<a name="method-range"></a>
#### `range()` {.collection-method}

Метод `range` повертає колекцію з цілими числами у вказаному діапазоні:

```php
$collection = collect()->range(3, 6);

$collection->all();

// [3, 4, 5, 6]
```

<a name="method-reduce"></a>
#### `reduce()` {.collection-method}

Метод `reduce` зводить колекцію до єдиного значення, передаючи результат кожної ітерації до наступної:

```php
$collection = collect([1, 2, 3]);

$total = $collection->reduce(function (?int $carry, int $item) {
    return $carry + $item;
});

// 6
```

На першій ітерації значенням `$carry` є `null`; проте ви можете задати його початкове значення, передавши `reduce` другий аргумент:

```php
$collection->reduce(function (int $carry, int $item) {
    return $carry + $item;
}, 4);

// 10
```

Метод `reduce` також передає до заданого колбека ключі масиву:

```php
$collection = collect([
    'usd' => 1400,
    'gbp' => 1200,
    'eur' => 1000,
]);

$ratio = [
    'usd' => 1,
    'gbp' => 1.37,
    'eur' => 1.22,
];

$collection->reduce(function (int $carry, int $value, string $key) use ($ratio) {
    return $carry + ($value * $ratio[$key]);
}, 0);

// 4264
```

<a name="method-reduce-into"></a>
#### `reduceInto()` {.collection-method}

Метод `reduceInto` зводить колекцію до єдиного значення, змінюючи задане початкове значення. На відміну від методу `reduce`, заданий колбек не мусить повертати накопичене значення:

```php
class OrderStats
{
    public int $total = 0;

    public int $count = 0;
}

$orders = collect([
    ['amount' => 100],
    ['amount' => 250],
    ['amount' => 50],
]);

$stats = $orders->reduceInto(new OrderStats, function (OrderStats $stats, array $order) {
    $stats->total += $order['amount'];
    $stats->count++;
});

$stats->total;

// 400
```

Коли ви зводите до скаляра чи масиву, приймайте його в колбеку за посиланням, щоб ваші зміни застосовувалися до оригінального значення:

```php
$collection = collect([1, 2, 3, 4, 5]);

$even = $collection->reduceInto([], function (array &$result, int $value) {
    if ($value % 2 === 0) {
        $result[] = $value;
    }
});

// [2, 4]
```

<a name="method-reduce-spread"></a>
#### `reduceSpread()` {.collection-method}

Метод `reduceSpread` зводить колекцію до масиву значень, передаючи результати кожної ітерації до наступної. Цей метод схожий на `reduce`; проте він може приймати кілька початкових значень:

```php
[$creditsRemaining, $batch] = Image::where('status', 'unprocessed')
    ->get()
    ->reduceSpread(function (int $creditsRemaining, Collection $batch, Image $image) {
        if ($creditsRemaining >= $image->creditsRequired()) {
            $batch->push($image);

            $creditsRemaining -= $image->creditsRequired();
        }

        return [$creditsRemaining, $batch];
    }, $creditsAvailable, collect());
```

<a name="method-reject"></a>
#### `reject()` {.collection-method}

Метод `reject` фільтрує колекцію заданим замиканням. Замикання має повернути `true`, якщо елемент слід вилучити з отриманої колекції:

```php
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->reject(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [1, 2]
```

Протилежність методу `reject` - метод [filter](#method-filter).

<a name="method-replace"></a>
#### `replace()` {.collection-method}

Метод `replace` поводиться подібно до `merge`; проте, окрім перезапису відповідних елементів із рядковими ключами, `replace` перезапише й елементи колекції з відповідними числовими ключами:

```php
$collection = collect(['Taylor', 'Abigail', 'James']);

$replaced = $collection->replace([1 => 'Victoria', 3 => 'Finn']);

$replaced->all();

// ['Taylor', 'Victoria', 'James', 'Finn']
```

<a name="method-replacerecursive"></a>
#### `replaceRecursive()` {.collection-method}

Метод `replaceRecursive` поводиться подібно до `replace`, але заходить у масиви й застосовує той самий процес заміни до внутрішніх значень:

```php
$collection = collect([
    'Taylor',
    'Abigail',
    [
        'James',
        'Victoria',
        'Finn'
    ]
]);

$replaced = $collection->replaceRecursive([
    'Charlie',
    2 => [1 => 'King']
]);

$replaced->all();

// ['Charlie', 'Abigail', ['James', 'King', 'Finn']]
```

<a name="method-reverse"></a>
#### `reverse()` {.collection-method}

Метод `reverse` обертає порядок елементів колекції, зберігаючи оригінальні ключі:

```php
$collection = collect(['a', 'b', 'c', 'd', 'e']);

$reversed = $collection->reverse();

$reversed->all();

/*
    [
        4 => 'e',
        3 => 'd',
        2 => 'c',
        1 => 'b',
        0 => 'a',
    ]
*/
```

<a name="method-search"></a>
#### `search()` {.collection-method}

Метод `search` шукає в колекції задане значення й повертає його ключ, якщо знайшов. Якщо елемент не знайдено, повертається `false`:

```php
$collection = collect([2, 4, 6, 8]);

$collection->search(4);

// 1
```

Пошук виконується «нестрогим» порівнянням: рядок із цілим значенням вважається рівним цілому числу з тим самим значенням. Щоб скористатися «строгим» порівнянням, передайте другим аргументом методу `true`:

```php
collect([2, 4, 6, 8])->search('4', strict: true);

// false
```

Як варіант, ви можете передати власне замикання, щоб знайти перший елемент, який проходить заданий тест:

```php
collect([2, 4, 6, 8])->search(function (int $item, int $key) {
    return $item > 5;
});

// 2
```

<a name="method-select"></a>
#### `select()` {.collection-method}

Метод `select` вибирає з колекції задані ключі - подібно до інструкції `SELECT` в SQL:

```php
$users = collect([
    ['name' => 'Taylor Otwell', 'role' => 'Developer', 'status' => 'active'],
    ['name' => 'Victoria Faith', 'role' => 'Researcher', 'status' => 'active'],
]);

$users->select(['name', 'role']);

/*
    [
        ['name' => 'Taylor Otwell', 'role' => 'Developer'],
        ['name' => 'Victoria Faith', 'role' => 'Researcher'],
    ],
*/
```

<a name="method-shift"></a>
#### `shift()` {.collection-method}

Метод `shift` вилучає й повертає перший елемент колекції:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift();

// 1

$collection->all();

// [2, 3, 4, 5]
```

Ви можете передати методу `shift` ціле число, щоб вилучити й повернути кілька елементів з початку колекції:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift(3);

// collect([1, 2, 3])

$collection->all();

// [4, 5]
```

<a name="method-shuffle"></a>
#### `shuffle()` {.collection-method}

Метод `shuffle` випадково перемішує елементи колекції:

```php
$collection = collect([1, 2, 3, 4, 5]);

$shuffled = $collection->shuffle();

$shuffled->all();

// [3, 2, 5, 1, 4] - (generated randomly)
```

<a name="method-skip"></a>
#### `skip()` {.collection-method}

Метод `skip` повертає нову колекцію, з початку якої вилучено задану кількість елементів:

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$collection = $collection->skip(4);

$collection->all();

// [5, 6, 7, 8, 9, 10]
```

<a name="method-skipuntil"></a>
#### `skipUntil()` {.collection-method}

Метод `skipUntil` пропускає елементи колекції, доки заданий колбек повертає `false`. Щойно колбек поверне `true`, усі решта елементів колекції буде повернуто як нову колекцію:

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [3, 4]
```

Ви також можете передати методу `skipUntil` просте значення, щоб пропускати всі елементи, доки не знайдеться задане значення:

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(3);

$subset->all();

// [3, 4]
```

> [!WARNING]
> Якщо заданого значення не знайдено або колбек ніколи не повертає `true`, метод `skipUntil` поверне порожню колекцію.

<a name="method-skipwhile"></a>
#### `skipWhile()` {.collection-method}

Метод `skipWhile` пропускає елементи колекції, доки заданий колбек повертає `true`. Щойно колбек поверне `false`, усі решта елементів колекції буде повернуто як нову колекцію:

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipWhile(function (int $item) {
    return $item <= 3;
});

$subset->all();

// [4]
```

> [!WARNING]
> Якщо колбек ніколи не повертає `false`, метод `skipWhile` поверне порожню колекцію.

<a name="method-slice"></a>
#### `slice()` {.collection-method}

Метод `slice` повертає зріз колекції, що починається із заданого індексу:

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$slice = $collection->slice(4);

$slice->all();

// [5, 6, 7, 8, 9, 10]
```

Якщо ви хочете обмежити розмір поверненого зрізу, передайте потрібний розмір другим аргументом методу:

```php
$slice = $collection->slice(4, 2);

$slice->all();

// [5, 6]
```

За замовчуванням повернений зріз збереже ключі. Якщо ви не хочете зберігати оригінальні ключі, переіндексувати їх можна методом [values](#method-values).

<a name="method-sliding"></a>
#### `sliding()` {.collection-method}

Метод `sliding` повертає нову колекцію фрагментів, що дають вигляд елементів колекції через «ковзне вікно»:

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(2);

$chunks->toArray();

// [[1, 2], [2, 3], [3, 4], [4, 5]]
```

Це особливо корисно в поєднанні з методом [eachSpread](#method-eachspread):

```php
$transactions->sliding(2)->eachSpread(function (Collection $previous, Collection $current) {
    $current->total = $previous->total + $current->amount;
});
```

Другим аргументом ви можете передати «крок», який визначає відстань між першими елементами сусідніх фрагментів:

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(3, step: 2);

$chunks->toArray();

// [[1, 2, 3], [3, 4, 5]]
```

<a name="method-sole"></a>
#### `sole()` {.collection-method}

Метод `sole` повертає перший елемент колекції, який проходить заданий тест, - але тільки якщо тест проходить рівно один елемент:

```php
collect([1, 2, 3, 4])->sole(function (int $value, int $key) {
    return $value === 2;
});

// 2
```

Ви також можете передати методу `sole` пару ключ / значення, і він поверне перший елемент колекції, який відповідає заданій парі, - але тільки якщо їй відповідає рівно один елемент:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->sole('product', 'Chair');

// ['product' => 'Chair', 'price' => 100]
```

Як варіант, ви можете викликати метод `sole` без аргументів, щоб отримати перший елемент колекції, якщо в ній лише один елемент:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
]);

$collection->sole();

// ['product' => 'Desk', 'price' => 200]
```

Якщо в колекції немає елементів, які має повернути метод `sole`, буде викинуто виняток `\Illuminate\Collections\ItemNotFoundException`. Якщо повернути слід більше ніж один елемент, буде викинуто `\Illuminate\Collections\MultipleItemsFoundException`.

<a name="method-some"></a>
#### `some()` {.collection-method}

Аліас методу [contains](#method-contains).

<a name="method-sort"></a>
#### `sort()` {.collection-method}

Метод `sort` сортує колекцію. Відсортована колекція зберігає оригінальні ключі масиву, тож у прикладі нижче ми скористаємося методом [values](#method-values), щоб скинути ключі до послідовних числових індексів:

```php
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sort();

$sorted->values()->all();

// [1, 2, 3, 4, 5]
```

Якщо ваші потреби в сортуванні складніші, передайте `sort` колбек із власним алгоритмом. Зверніться до документації PHP про [uasort](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters) - саме її метод `sort` колекції використовує під капотом.

> [!NOTE]
> Якщо вам потрібно відсортувати колекцію вкладених масивів чи об'єктів, дивіться методи [sortBy](#method-sortby) та [sortByDesc](#method-sortbydesc).

<a name="method-sortby"></a>
#### `sortBy()` {.collection-method}

Метод `sortBy` сортує колекцію за заданим ключем. Відсортована колекція зберігає оригінальні ключі масиву, тож у прикладі нижче ми скористаємося методом [values](#method-values), щоб скинути ключі до послідовних числових індексів:

```php
$collection = collect([
    ['name' => 'Desk', 'price' => 200],
    ['name' => 'Chair', 'price' => 100],
    ['name' => 'Bookcase', 'price' => 150],
]);

$sorted = $collection->sortBy('price');

$sorted->values()->all();

/*
    [
        ['name' => 'Chair', 'price' => 100],
        ['name' => 'Bookcase', 'price' => 150],
        ['name' => 'Desk', 'price' => 200],
    ]
*/
```

Другим аргументом метод `sortBy` приймає [прапорці сортування](https://www.php.net/manual/en/function.sort.php):

```php
$collection = collect([
    ['title' => 'Item 1'],
    ['title' => 'Item 12'],
    ['title' => 'Item 3'],
]);

$sorted = $collection->sortBy('title', SORT_NATURAL);

$sorted->values()->all();

/*
    [
        ['title' => 'Item 1'],
        ['title' => 'Item 3'],
        ['title' => 'Item 12'],
    ]
*/
```

Як варіант, ви можете передати власне замикання, щоб визначити, як сортувати значення колекції:

```php
$collection = collect([
    ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
    ['name' => 'Chair', 'colors' => ['Black']],
    ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
]);

$sorted = $collection->sortBy(function (array $product, int $key) {
    return count($product['colors']);
});

$sorted->values()->all();

/*
    [
        ['name' => 'Chair', 'colors' => ['Black']],
        ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
        ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
    ]
*/
```

Якщо ви хочете відсортувати колекцію за кількома атрибутами, передайте методу `sortBy` масив операцій сортування. Кожна операція має бути масивом з атрибута, за яким ви хочете сортувати, і напрямку сортування:

```php
$collection = collect([
    ['name' => 'Taylor Otwell', 'age' => 34],
    ['name' => 'Abigail Otwell', 'age' => 30],
    ['name' => 'Taylor Otwell', 'age' => 36],
    ['name' => 'Abigail Otwell', 'age' => 32],
]);

$sorted = $collection->sortBy([
    ['name', 'asc'],
    ['age', 'desc'],
]);

$sorted->values()->all();

/*
    [
        ['name' => 'Abigail Otwell', 'age' => 32],
        ['name' => 'Abigail Otwell', 'age' => 30],
        ['name' => 'Taylor Otwell', 'age' => 36],
        ['name' => 'Taylor Otwell', 'age' => 34],
    ]
*/
```

Сортуючи колекцію за кількома атрибутами, ви також можете передати замикання, які описують кожну операцію сортування:

```php
$collection = collect([
    ['name' => 'Taylor Otwell', 'age' => 34],
    ['name' => 'Abigail Otwell', 'age' => 30],
    ['name' => 'Taylor Otwell', 'age' => 36],
    ['name' => 'Abigail Otwell', 'age' => 32],
]);

$sorted = $collection->sortBy([
    fn (array $a, array $b) => $a['name'] <=> $b['name'],
    fn (array $a, array $b) => $b['age'] <=> $a['age'],
]);

$sorted->values()->all();

/*
    [
        ['name' => 'Abigail Otwell', 'age' => 32],
        ['name' => 'Abigail Otwell', 'age' => 30],
        ['name' => 'Taylor Otwell', 'age' => 36],
        ['name' => 'Taylor Otwell', 'age' => 34],
    ]
*/
```

<a name="method-sortbydesc"></a>
#### `sortByDesc()` {.collection-method}

Цей метод має ту саму сигнатуру, що й метод [sortBy](#method-sortby), але сортує колекцію у зворотному порядку.

<a name="method-sortdesc"></a>
#### `sortDesc()` {.collection-method}

Цей метод сортує колекцію у зворотному порядку відносно методу [sort](#method-sort):

```php
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sortDesc();

$sorted->values()->all();

// [5, 4, 3, 2, 1]
```

На відміну від `sort`, передати замикання до `sortDesc` не можна. Натомість скористайтеся методом [sort](#method-sort) і оберніть своє порівняння.

<a name="method-sortkeys"></a>
#### `sortKeys()` {.collection-method}

Метод `sortKeys` сортує колекцію за ключами асоціативного масиву під капотом:

```php
$collection = collect([
    'id' => 22345,
    'first' => 'John',
    'last' => 'Doe',
]);

$sorted = $collection->sortKeys();

$sorted->all();

/*
    [
        'first' => 'John',
        'id' => 22345,
        'last' => 'Doe',
    ]
*/
```

<a name="method-sortkeysdesc"></a>
#### `sortKeysDesc()` {.collection-method}

Цей метод має ту саму сигнатуру, що й метод [sortKeys](#method-sortkeys), але сортує колекцію у зворотному порядку.

<a name="method-sortkeysusing"></a>
#### `sortKeysUsing()` {.collection-method}

Метод `sortKeysUsing` сортує колекцію за ключами асоціативного масиву під капотом за допомогою колбека:

```php
$collection = collect([
    'ID' => 22345,
    'first' => 'John',
    'last' => 'Doe',
]);

$sorted = $collection->sortKeysUsing('strnatcasecmp');

$sorted->all();

/*
    [
        'first' => 'John',
        'ID' => 22345,
        'last' => 'Doe',
    ]
*/
```

Колбек має бути функцією порівняння, яка повертає ціле число менше, рівне або більше за нуль. Докладніше дивіться в документації PHP про [uksort](https://www.php.net/manual/en/function.uksort.php#refsect1-function.uksort-parameters) - саме цю функцію PHP метод `sortKeysUsing` використовує під капотом.

<a name="method-splice"></a>
#### `splice()` {.collection-method}

Метод `splice` вилучає й повертає зріз елементів, що починається із вказаного індексу:

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2);

$chunk->all();

// [3, 4, 5]

$collection->all();

// [1, 2]
```

Другим аргументом ви можете обмежити розмір отриманої колекції:

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2, 1);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 4, 5]
```

Крім того, третім аргументом ви можете передати нові елементи, які замінять вилучені з колекції:

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2, 1, [10, 11]);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 10, 11, 4, 5]
```

<a name="method-split"></a>
#### `split()` {.collection-method}

Метод `split` розбиває колекцію на задану кількість груп:

```php
$collection = collect([1, 2, 3, 4, 5]);

$groups = $collection->split(3);

$groups->all();

// [[1, 2], [3, 4], [5]]
```

<a name="method-splitin"></a>
#### `splitIn()` {.collection-method}

Метод `splitIn` розбиває колекцію на задану кількість груп, повністю заповнюючи всі групи, крім останньої, а решту віддаючи останній:

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$groups = $collection->splitIn(3);

$groups->all();

// [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
```

<a name="method-sum"></a>
#### `sum()` {.collection-method}

Метод `sum` повертає суму всіх елементів колекції:

```php
collect([1, 2, 3, 4, 5])->sum();

// 15
```

Якщо колекція містить вкладені масиви чи об'єкти, передайте ключ, за яким визначатиметься, які значення підсумовувати:

```php
$collection = collect([
    ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
    ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
]);

$collection->sum('pages');

// 1272
```

Крім того, ви можете передати власне замикання, щоб визначити, які значення колекції підсумовувати:

```php
$collection = collect([
    ['name' => 'Chair', 'colors' => ['Black']],
    ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
    ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
]);

$collection->sum(function (array $product) {
    return count($product['colors']);
});

// 6
```

<a name="method-take"></a>
#### `take()` {.collection-method}

Метод `take` повертає нову колекцію із вказаною кількістю елементів:

```php
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(3);

$chunk->all();

// [0, 1, 2]
```

Ви також можете передати від'ємне ціле число, щоб узяти вказану кількість елементів з кінця колекції:

```php
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(-2);

$chunk->all();

// [4, 5]
```

<a name="method-takeuntil"></a>
#### `takeUntil()` {.collection-method}

Метод `takeUntil` повертає елементи колекції, доки заданий колбек не поверне `true`:

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [1, 2]
```

Ви також можете передати методу `takeUntil` просте значення, щоб отримати елементи, доки не знайдеться задане значення:

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(3);

$subset->all();

// [1, 2]
```

> [!WARNING]
> Якщо заданого значення не знайдено або колбек ніколи не повертає `true`, метод `takeUntil` поверне всі елементи колекції.

<a name="method-takewhile"></a>
#### `takeWhile()` {.collection-method}

Метод `takeWhile` повертає елементи колекції, доки заданий колбек не поверне `false`:

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeWhile(function (int $item) {
    return $item < 3;
});

$subset->all();

// [1, 2]
```

> [!WARNING]
> Якщо колбек ніколи не повертає `false`, метод `takeWhile` поверне всі елементи колекції.

<a name="method-tap"></a>
#### `tap()` {.collection-method}

Метод `tap` передає колекцію до заданого колбека, дозволяючи «вклинитися» в колекцію в певній точці й щось зробити з елементами, не впливаючи на саму колекцію. Далі метод `tap` повертає колекцію:

```php
collect([2, 4, 3, 1, 5])
    ->sort()
    ->tap(function (Collection $collection) {
        Log::debug('Values after sorting', $collection->values()->all());
    })
    ->shift();

// 1
```

<a name="method-times"></a>
#### `times()` {.collection-method}

Статичний метод `times` створює нову колекцію, викликаючи задане замикання вказану кількість разів:

```php
$collection = Collection::times(10, function (int $number) {
    return $number * 9;
});

$collection->all();

// [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]
```

<a name="method-toarray"></a>
#### `toArray()` {.collection-method}

Метод `toArray` перетворює колекцію на звичайний PHP-масив `array`. Якщо значення колекції - моделі [Eloquent](/docs/{{version}}/eloquent), моделі також буде перетворено на масиви:

```php
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toArray();

/*
    [
        ['name' => 'Desk', 'price' => 200],
    ]
*/
```

> [!WARNING]
> `toArray` також перетворює на масив усі вкладені об'єкти колекції, які є екземплярами `Arrayable`. Якщо ви хочете отримати сирий масив під капотом колекції, скористайтеся натомість методом [all](#method-all).

<a name="method-tojson"></a>
#### `toJson()` {.collection-method}

Метод `toJson` перетворює колекцію на серіалізований JSON-рядок:

```php
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toJson();

// '{"name":"Desk", "price":200}'
```

<a name="method-to-pretty-json"></a>
#### `toPrettyJson()` {.collection-method}

Метод `toPrettyJson` перетворює колекцію на відформатований JSON-рядок з опцією `JSON_PRETTY_PRINT`:

```php
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toPrettyJson();
```

<a name="method-transform"></a>
#### `transform()` {.collection-method}

Метод `transform` проходить колекцію й викликає заданий колбек з кожним її елементом. Елементи колекції буде замінено значеннями, які повернув колбек:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->transform(function (int $item, int $key) {
    return $item * 2;
});

$collection->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> На відміну від більшості інших методів колекції, `transform` змінює саму колекцію. Якщо ви натомість хочете створити нову колекцію, скористайтеся методом [map](#method-map).

<a name="method-undot"></a>
#### `undot()` {.collection-method}

Метод `undot` розгортає одновимірну колекцію з «крапковою» нотацією на багатовимірну:

```php
$person = collect([
    'name.first_name' => 'Marie',
    'name.last_name' => 'Valentine',
    'address.line_1' => '2992 Eagle Drive',
    'address.line_2' => '',
    'address.suburb' => 'Detroit',
    'address.state' => 'MI',
    'address.postcode' => '48219'
]);

$person = $person->undot();

$person->toArray();

/*
    [
        "name" => [
            "first_name" => "Marie",
            "last_name" => "Valentine",
        ],
        "address" => [
            "line_1" => "2992 Eagle Drive",
            "line_2" => "",
            "suburb" => "Detroit",
            "state" => "MI",
            "postcode" => "48219",
        ],
    ]
*/
```

<a name="method-union"></a>
#### `union()` {.collection-method}

Метод `union` додає заданий масив до колекції. Якщо заданий масив містить ключі, які вже є в оригінальній колекції, перевагу матимуть значення оригінальної колекції:

```php
$collection = collect([1 => ['a'], 2 => ['b']]);

$union = $collection->union([3 => ['c'], 1 => ['d']]);

$union->all();

// [1 => ['a'], 2 => ['b'], 3 => ['c']]
```

<a name="method-unique"></a>
#### `unique()` {.collection-method}

Метод `unique` повертає всі унікальні елементи колекції. Повернена колекція зберігає оригінальні ключі масиву, тож у прикладі нижче ми скористаємося методом [values](#method-values), щоб скинути ключі до послідовних числових індексів:

```php
$collection = collect([1, 1, 2, 2, 3, 4, 2]);

$unique = $collection->unique();

$unique->values()->all();

// [1, 2, 3, 4]
```

Працюючи з вкладеними масивами чи об'єктами, ви можете вказати ключ, за яким визначається унікальність:

```php
$collection = collect([
    ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
    ['name' => 'iPhone 5', 'brand' => 'Apple', 'type' => 'phone'],
    ['name' => 'Apple Watch', 'brand' => 'Apple', 'type' => 'watch'],
    ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
    ['name' => 'Galaxy Gear', 'brand' => 'Samsung', 'type' => 'watch'],
]);

$unique = $collection->unique('brand');

$unique->values()->all();

/*
    [
        ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
        ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
    ]
*/
```

Нарешті, ви можете передати методу `unique` власне замикання, щоб вказати, яке значення визначає унікальність елемента:

```php
$unique = $collection->unique(function (array $item) {
    return $item['brand'].$item['type'];
});

$unique->values()->all();

/*
    [
        ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
        ['name' => 'Apple Watch', 'brand' => 'Apple', 'type' => 'watch'],
        ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
        ['name' => 'Galaxy Gear', 'brand' => 'Samsung', 'type' => 'watch'],
    ]
*/
```

Перевіряючи значення елементів, метод `unique` використовує «нестрогі» порівняння: рядок із цілим значенням вважається рівним цілому числу з тим самим значенням. Щоб фільтрувати зі «строгими» порівняннями, скористайтеся методом [uniqueStrict](#method-uniquestrict).

> [!NOTE]
> Поведінка цього методу змінюється під час роботи з [колекціями Eloquent](/docs/{{version}}/eloquent-collections#method-unique).

<a name="method-uniquestrict"></a>
#### `uniqueStrict()` {.collection-method}

Цей метод має ту саму сигнатуру, що й метод [unique](#method-unique); проте всі значення порівнюються «строго».

<a name="method-unless"></a>
#### `unless()` {.collection-method}

Метод `unless` виконає заданий колбек, якщо перший переданий методу аргумент не є `true`. До замикання буде передано екземпляр колекції та перший аргумент, переданий методу `unless`:

```php
$collection = collect([1, 2, 3]);

$collection->unless(true, function (Collection $collection, bool $value) {
    return $collection->push(4);
});

$collection->unless(false, function (Collection $collection, bool $value) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

Методу `unless` можна передати другий колбек. Він виконається, коли перший аргумент, переданий методу `unless`, є `true`:

```php
$collection = collect([1, 2, 3]);

$collection->unless(true, function (Collection $collection, bool $value) {
    return $collection->push(4);
}, function (Collection $collection, bool $value) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

Протилежність `unless` - метод [when](#method-when).

<a name="method-unlessempty"></a>
#### `unlessEmpty()` {.collection-method}

Аліас методу [whenNotEmpty](#method-whennotempty).

<a name="method-unlessnotempty"></a>
#### `unlessNotEmpty()` {.collection-method}

Аліас методу [whenEmpty](#method-whenempty).

<a name="method-unwrap"></a>
#### `unwrap()` {.collection-method}

Статичний метод `unwrap` повертає елементи колекції із заданого значення, якщо це доречно:

```php
Collection::unwrap(collect('John Doe'));

// ['John Doe']

Collection::unwrap(['John Doe']);

// ['John Doe']

Collection::unwrap('John Doe');

// 'John Doe'
```

<a name="method-value"></a>
#### `value()` {.collection-method}

Метод `value` дістає задане значення з першого елемента колекції:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Speaker', 'price' => 400],
]);

$value = $collection->value('price');

// 200
```

<a name="method-values"></a>
#### `values()` {.collection-method}

Метод `values` повертає нову колекцію з ключами, скинутими до послідовних цілих чисел:

```php
$collection = collect([
    10 => ['product' => 'Desk', 'price' => 200],
    11 => ['product' => 'Speaker', 'price' => 400],
]);

$values = $collection->values();

$values->all();

/*
    [
        0 => ['product' => 'Desk', 'price' => 200],
        1 => ['product' => 'Speaker', 'price' => 400],
    ]
*/
```

<a name="method-when"></a>
#### `when()` {.collection-method}

Метод `when` виконає заданий колбек, коли перший переданий методу аргумент є `true`. До замикання буде передано екземпляр колекції та перший аргумент, переданий методу `when`:

```php
$collection = collect([1, 2, 3]);

$collection->when(true, function (Collection $collection, bool $value) {
    return $collection->push(4);
});

$collection->when(false, function (Collection $collection, bool $value) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 4]
```

Методу `when` можна передати другий колбек. Він виконається, коли перший аргумент, переданий методу `when`, є `false`:

```php
$collection = collect([1, 2, 3]);

$collection->when(false, function (Collection $collection, bool $value) {
    return $collection->push(4);
}, function (Collection $collection, bool $value) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

Протилежність `when` - метод [unless](#method-unless).

<a name="method-whenempty"></a>
#### `whenEmpty()` {.collection-method}

Метод `whenEmpty` виконає заданий колбек, коли колекція порожня:

```php
$collection = collect(['Michael', 'Tom']);

$collection->whenEmpty(function (Collection $collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Michael', 'Tom']

$collection = collect();

$collection->whenEmpty(function (Collection $collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Adam']
```

Методу `whenEmpty` можна передати друге замикання, яке виконається, коли колекція не порожня:

```php
$collection = collect(['Michael', 'Tom']);

$collection->whenEmpty(function (Collection $collection) {
    return $collection->push('Adam');
}, function (Collection $collection) {
    return $collection->push('Taylor');
});

$collection->all();

// ['Michael', 'Tom', 'Taylor']
```

Протилежність `whenEmpty` - метод [whenNotEmpty](#method-whennotempty).

<a name="method-whennotempty"></a>
#### `whenNotEmpty()` {.collection-method}

Метод `whenNotEmpty` виконає заданий колбек, коли колекція не порожня:

```php
$collection = collect(['Michael', 'Tom']);

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Michael', 'Tom', 'Adam']

$collection = collect();

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('Adam');
});

$collection->all();

// []
```

Методу `whenNotEmpty` можна передати друге замикання, яке виконається, коли колекція порожня:

```php
$collection = collect();

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('Adam');
}, function (Collection $collection) {
    return $collection->push('Taylor');
});

$collection->all();

// ['Taylor']
```

Протилежність `whenNotEmpty` - метод [whenEmpty](#method-whenempty).

<a name="method-where"></a>
#### `where()` {.collection-method}

Метод `where` фільтрує колекцію за заданою парою ключ / значення:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->where('price', 100);

$filtered->all();

/*
    [
        ['product' => 'Chair', 'price' => 100],
        ['product' => 'Door', 'price' => 100],
    ]
*/
```

Перевіряючи значення елементів, метод `where` використовує «нестрогі» порівняння: рядок із цілим значенням вважається рівним цілому числу з тим самим значенням. Щоб фільтрувати зі «строгими» порівняннями, скористайтеся методом [whereStrict](#method-wherestrict), а щоб фільтрувати за значеннями `null` - методами [whereNull](#method-wherenull) та [whereNotNull](#method-wherenotnull).

За бажанням другим параметром ви можете передати оператор порівняння. Підтримуються оператори: '===', '!==', '!=', '==', '=', '<>', '>', '<', '>=' та '<=':

```php
$collection = collect([
    ['name' => 'Jim', 'platform' => 'Mac'],
    ['name' => 'Sally', 'platform' => 'Mac'],
    ['name' => 'Sue', 'platform' => 'Linux'],
]);

$filtered = $collection->where('platform', '!=', 'Linux');

$filtered->all();

/*
    [
        ['name' => 'Jim', 'platform' => 'Mac'],
        ['name' => 'Sally', 'platform' => 'Mac'],
    ]
*/
```

<a name="method-wherestrict"></a>
#### `whereStrict()` {.collection-method}

Цей метод має ту саму сигнатуру, що й метод [where](#method-where); проте всі значення порівнюються «строго».

<a name="method-wherebetween"></a>
#### `whereBetween()` {.collection-method}

Метод `whereBetween` фільтрує колекцію, перевіряючи, чи потрапляє значення вказаного елемента в заданий діапазон:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 80],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Pencil', 'price' => 30],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->whereBetween('price', [100, 200]);

$filtered->all();

/*
    [
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Bookcase', 'price' => 150],
        ['product' => 'Door', 'price' => 100],
    ]
*/
```

<a name="method-wherein"></a>
#### `whereIn()` {.collection-method}

Метод `whereIn` вилучає з колекції елементи, значення яких за вказаним ключем не міститься в заданому масиві:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->whereIn('price', [150, 200]);

$filtered->all();

/*
    [
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Bookcase', 'price' => 150],
    ]
*/
```

Перевіряючи значення елементів, метод `whereIn` використовує «нестрогі» порівняння: рядок із цілим значенням вважається рівним цілому числу з тим самим значенням. Щоб фільтрувати зі «строгими» порівняннями, скористайтеся методом [whereInStrict](#method-whereinstrict).

<a name="method-whereinstrict"></a>
#### `whereInStrict()` {.collection-method}

Цей метод має ту саму сигнатуру, що й метод [whereIn](#method-wherein); проте всі значення порівнюються «строго».

<a name="method-whereinstanceof"></a>
#### `whereInstanceOf()` {.collection-method}

Метод `whereInstanceOf` фільтрує колекцію за заданим типом класу:

```php
use App\Models\User;
use App\Models\Post;

$collection = collect([
    new User,
    new User,
    new Post,
]);

$filtered = $collection->whereInstanceOf(User::class);

$filtered->all();

// [App\Models\User, App\Models\User]
```

<a name="method-wherenotbetween"></a>
#### `whereNotBetween()` {.collection-method}

Метод `whereNotBetween` фільтрує колекцію, перевіряючи, чи лежить значення вказаного елемента поза заданим діапазоном:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 80],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Pencil', 'price' => 30],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->whereNotBetween('price', [100, 200]);

$filtered->all();

/*
    [
        ['product' => 'Chair', 'price' => 80],
        ['product' => 'Pencil', 'price' => 30],
    ]
*/
```

<a name="method-wherenotin"></a>
#### `whereNotIn()` {.collection-method}

Метод `whereNotIn` вилучає з колекції елементи, значення яких за вказаним ключем міститься в заданому масиві:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->whereNotIn('price', [150, 200]);

$filtered->all();

/*
    [
        ['product' => 'Chair', 'price' => 100],
        ['product' => 'Door', 'price' => 100],
    ]
*/
```

Перевіряючи значення елементів, метод `whereNotIn` використовує «нестрогі» порівняння: рядок із цілим значенням вважається рівним цілому числу з тим самим значенням. Щоб фільтрувати зі «строгими» порівняннями, скористайтеся методом [whereNotInStrict](#method-wherenotinstrict).

<a name="method-wherenotinstrict"></a>
#### `whereNotInStrict()` {.collection-method}

Цей метод має ту саму сигнатуру, що й метод [whereNotIn](#method-wherenotin); проте всі значення порівнюються «строго».

<a name="method-wherenotnull"></a>
#### `whereNotNull()` {.collection-method}

Метод `whereNotNull` повертає елементи колекції, у яких заданий ключ не є `null`:

```php
$collection = collect([
    ['name' => 'Desk'],
    ['name' => null],
    ['name' => 'Bookcase'],
    ['name' => 0],
    ['name' => ''],
]);

$filtered = $collection->whereNotNull('name');

$filtered->all();

/*
    [
        ['name' => 'Desk'],
        ['name' => 'Bookcase'],
        ['name' => 0],
        ['name' => ''],
    ]
*/
```

<a name="method-wherenull"></a>
#### `whereNull()` {.collection-method}

Метод `whereNull` повертає елементи колекції, у яких заданий ключ є `null`:

```php
$collection = collect([
    ['name' => 'Desk'],
    ['name' => null],
    ['name' => 'Bookcase'],
    ['name' => 0],
    ['name' => ''],
]);

$filtered = $collection->whereNull('name');

$filtered->all();

/*
    [
        ['name' => null],
    ]
*/
```

<a name="method-wrap"></a>
#### `wrap()` {.collection-method}

Статичний метод `wrap` загортає задане значення в колекцію, якщо це доречно:

```php
use Illuminate\Support\Collection;

$collection = Collection::wrap('John Doe');

$collection->all();

// ['John Doe']

$collection = Collection::wrap(['John Doe']);

$collection->all();

// ['John Doe']

$collection = Collection::wrap(collect('John Doe'));

$collection->all();

// ['John Doe']
```

<a name="method-zip"></a>
#### `zip()` {.collection-method}

Метод `zip` зливає значення заданого масиву зі значеннями оригінальної колекції за відповідними індексами:

```php
$collection = collect(['Chair', 'Desk']);

$zipped = $collection->zip([100, 200]);

$zipped->all();

// [['Chair', 100], ['Desk', 200]]
```

<a name="higher-order-messages"></a>
## Повідомлення вищого порядку

Колекції також підтримують «повідомлення вищого порядку» - скорочення для поширених дій над колекціями. Повідомлення вищого порядку надають такі методи колекції: [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile) та [unique](#method-unique).

Доступ до кожного повідомлення вищого порядку здійснюється як до динамічної властивості екземпляра колекції. Наприклад, скористаймося повідомленням вищого порядку `each`, щоб викликати метод на кожному об'єкті колекції:

```php
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

Так само ми можемо скористатися повідомленням вищого порядку `sum`, щоб зібрати загальну кількість «голосів» для колекції користувачів:

```php
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## Ліниві колекції

<a name="lazy-collection-introduction"></a>
### Вступ

> [!WARNING]
> Перш ніж вивчати ліниві колекції Laravel, приділіть трохи часу знайомству з [генераторами PHP](https://www.php.net/manual/en/language.generators.overview.php).

Щоб доповнити й без того потужний клас `Collection`, клас `LazyCollection` використовує [генератори](https://www.php.net/manual/en/language.generators.overview.php) PHP, які дозволяють працювати з дуже великими наборами даних, тримаючи споживання пам'яті низьким.

Наприклад, уявіть, що вашому застосунку потрібно обробити багатогігабайтний файл логу, скориставшись методами колекцій Laravel для розбору логів. Замість читати весь файл у пам'ять одразу ліниві колекції дозволяють тримати в пам'яті лише невелику частину файлу за раз:

```php
use App\Models\LogEntry;
use Illuminate\Support\LazyCollection;

LazyCollection::make(function () {
    $handle = fopen('log.txt', 'r');

    while (($line = fgets($handle)) !== false) {
        yield $line;
    }

    fclose($handle);
})->chunk(4)->map(function (array $lines) {
    return LogEntry::fromLines($lines);
})->each(function (LogEntry $logEntry) {
    // Process the log entry...
});
```

Або уявіть, що вам потрібно пройти 10 000 моделей Eloquent. Зі звичайними колекціями Laravel усі 10 000 моделей Eloquent доведеться завантажити в пам'ять одночасно:

```php
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

Проте метод `cursor` конструктора запитів повертає екземпляр `LazyCollection`. Це дозволяє й далі виконувати один-єдиний запит до бази, але тримати в пам'яті лише одну модель Eloquent за раз. У цьому прикладі колбек `filter` не виконується, доки ми справді не пройдемо кожного користувача окремо, - і це різко знижує споживання пам'яті:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

<a name="creating-lazy-collections"></a>
### Створення лінивих колекцій

Щоб створити екземпляр лінивої колекції, передайте методу `make` колекції функцію-генератор PHP:

```php
use Illuminate\Support\LazyCollection;

LazyCollection::make(function () {
    $handle = fopen('log.txt', 'r');

    while (($line = fgets($handle)) !== false) {
        yield $line;
    }

    fclose($handle);
});
```

<a name="the-enumerable-contract"></a>
### Контракт Enumerable

Майже всі методи, доступні в класі `Collection`, доступні й у класі `LazyCollection`. Обидва ці класи реалізують контракт `Illuminate\Support\Enumerable`, який описує такі методи:

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

<div class="collection-method-list" markdown="1">

[all](#method-all)
[average](#method-average)
[avg](#method-avg)
[chunk](#method-chunk)
[chunkWhile](#method-chunkwhile)
[collapse](#method-collapse)
[collect](#method-collect)
[combine](#method-combine)
[concat](#method-concat)
[contains](#method-contains)
[containsStrict](#method-containsstrict)
[count](#method-count)
[countBy](#method-countBy)
[crossJoin](#method-crossjoin)
[dd](#method-dd)
[diff](#method-diff)
[diffAssoc](#method-diffassoc)
[diffKeys](#method-diffkeys)
[dump](#method-dump)
[duplicates](#method-duplicates)
[duplicatesStrict](#method-duplicatesstrict)
[each](#method-each)
[eachSpread](#method-eachspread)
[every](#method-every)
[except](#method-except)
[filter](#method-filter)
[first](#method-first)
[firstOrFail](#method-first-or-fail)
[firstWhere](#method-first-where)
[flatMap](#method-flatmap)
[flatten](#method-flatten)
[flip](#method-flip)
[forPage](#method-forpage)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[implode](#method-implode)
[intersect](#method-intersect)
[intersectAssoc](#method-intersectAssoc)
[intersectByKeys](#method-intersectbykeys)
[isEmpty](#method-isempty)
[isNotEmpty](#method-isnotempty)
[join](#method-join)
[keyBy](#method-keyby)
[keys](#method-keys)
[last](#method-last)
[macro](#method-macro)
[make](#method-make)
[map](#method-map)
[mapInto](#method-mapinto)
[mapSpread](#method-mapspread)
[mapToGroups](#method-maptogroups)
[mapWithKeys](#method-mapwithkeys)
[max](#method-max)
[median](#method-median)
[merge](#method-merge)
[mergeRecursive](#method-mergerecursive)
[min](#method-min)
[mode](#method-mode)
[nth](#method-nth)
[only](#method-only)
[pad](#method-pad)
[partition](#method-partition)
[pipe](#method-pipe)
[pluck](#method-pluck)
[random](#method-random)
[reduce](#method-reduce)
[reduceInto](#method-reduce-into)
[reject](#method-reject)
[replace](#method-replace)
[replaceRecursive](#method-replacerecursive)
[reverse](#method-reverse)
[search](#method-search)
[shuffle](#method-shuffle)
[skip](#method-skip)
[slice](#method-slice)
[sole](#method-sole)
[some](#method-some)
[sort](#method-sort)
[sortBy](#method-sortby)
[sortByDesc](#method-sortbydesc)
[sortKeys](#method-sortkeys)
[sortKeysDesc](#method-sortkeysdesc)
[split](#method-split)
[sum](#method-sum)
[take](#method-take)
[tap](#method-tap)
[times](#method-times)
[toArray](#method-toarray)
[toJson](#method-tojson)
[union](#method-union)
[unique](#method-unique)
[uniqueStrict](#method-uniquestrict)
[unless](#method-unless)
[unlessEmpty](#method-unlessempty)
[unlessNotEmpty](#method-unlessnotempty)
[unwrap](#method-unwrap)
[values](#method-values)
[when](#method-when)
[whenEmpty](#method-whenempty)
[whenNotEmpty](#method-whennotempty)
[where](#method-where)
[whereStrict](#method-wherestrict)
[whereBetween](#method-wherebetween)
[whereIn](#method-wherein)
[whereInStrict](#method-whereinstrict)
[whereInstanceOf](#method-whereinstanceof)
[whereNotBetween](#method-wherenotbetween)
[whereNotIn](#method-wherenotin)
[whereNotInStrict](#method-wherenotinstrict)
[wrap](#method-wrap)
[zip](#method-zip)

</div>

> [!WARNING]
> Методи, які змінюють колекцію (такі як `shift`, `pop`, `prepend` тощо), у класі `LazyCollection` **недоступні**.

<a name="lazy-collection-methods"></a>
### Методи лінивих колекцій

Окрім методів, описаних у контракті `Enumerable`, клас `LazyCollection` містить такі методи:

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()` {.collection-method}

Метод `takeUntilTimeout` повертає нову ліниву колекцію, яка перебиратиме значення до вказаного моменту. Після цього моменту колекція припинить перебір:

```php
$lazyCollection = LazyCollection::times(INF)
    ->takeUntilTimeout(now()->plus(minutes: 1));

$lazyCollection->each(function (int $number) {
    dump($number);

    sleep(1);
});

// 1
// 2
// ...
// 58
// 59
```

Щоб проілюструвати використання цього методу, уявіть застосунок, який надсилає рахунки з бази даних через курсор. Ви могли б описати [заплановане завдання](/docs/{{version}}/scheduling), яке запускається кожні 15 хвилин і обробляє рахунки щонайбільше 14 хвилин:

```php
use App\Models\Invoice;
use Illuminate\Support\Carbon;

Invoice::pending()->cursor()
    ->takeUntilTimeout(
        Carbon::createFromTimestamp(LARAVEL_START)->add(14, 'minutes')
    )
    ->each(fn (Invoice $invoice) => $invoice->submit());
```

<a name="method-tapEach"></a>
#### `tapEach()` {.collection-method}

Якщо метод `each` викликає заданий колбек для кожного елемента колекції одразу, то метод `tapEach` викликає заданий колбек лише тоді, коли елементи по одному дістаються зі списку:

```php
// Nothing has been dumped so far...
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// Three items are dumped...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-throttle"></a>
#### `throttle()` {.collection-method}

Метод `throttle` пригальмовує ліниву колекцію так, що кожне значення повертається через вказану кількість секунд. Цей метод особливо корисний у ситуаціях, коли ви працюєте із зовнішніми API, які обмежують частоту вхідних запитів:

```php
use App\Models\User;

User::where('vip', true)
    ->cursor()
    ->throttle(seconds: 1)
    ->each(function (User $user) {
        // Call external API...
    });
```

<a name="method-remember"></a>
#### `remember()` {.collection-method}

Метод `remember` повертає нову ліниву колекцію, яка запам'ятає вже перебрані значення й не діставатиме їх знову під час наступних перебирань колекції:

```php
// No query has been executed yet...
$users = User::cursor()->remember();

// The query is executed...
// The first 5 users are hydrated from the database...
$users->take(5)->all();

// First 5 users come from the collection's cache...
// The rest are hydrated from the database...
$users->take(20)->all();
```

<a name="method-with-heartbeat"></a>
#### `withHeartbeat()` {.collection-method}

Метод `withHeartbeat` дозволяє виконувати колбек через регулярні проміжки часу, доки перебирається лінива колекція. Це особливо корисно для тривалих операцій, які потребують періодичних службових дій - наприклад, продовження блокувань чи надсилання оновлень прогресу:

```php
use Carbon\CarbonInterval;
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('generate-reports', seconds: 60 * 5);

if ($lock->get()) {
    try {
        Report::where('status', 'pending')
            ->lazy()
            ->withHeartbeat(
                CarbonInterval::minutes(4),
                fn () => $lock->extend(CarbonInterval::minutes(5))
            )
            ->each(fn ($report) => $report->process());
    } finally {
        $lock->release();
    }
}
```
