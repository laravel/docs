# 集合

- [簡介](#introduction)
- [建立集合](#creating-collections)
- [可用的方法](#available-methods)

<a name="introduction"></a>
## 簡介

`Illuminate\Support\Collection` 類別提供一個流暢、便利的封裝來操控陣列資料。舉個例子，查看下列的程式碼。我們將用 `collect` 輔助方法從陣列建立一個新的集合實例，並對每一個元素執行 `strtoupper` 函式，然後移除所有的空元素：

    $collection = collect(['taylor', 'abigail', null])->map(function ($name) {
        return strtoupper($name);
    })
    ->reject(function ($name) {
        return empty($name);
    });


如你所見，`Collection` 類別允許你鏈結它的方法以對底層的陣列流暢地進行映射與刪減。一般來說，每一個 `Collection` 方法會回傳一個全新的 `Collection` 實例。

<a name="creating-collections"></a>
## 建立集合

如上所述，`collect` 輔助方法會用傳入的陣列回傳一個新的 `Illuminate\Support\Collection` 實例。所以要建立一個集合就這麼簡單：

    $collection = collect([1, 2, 3]);

預設 [Eloquent](/docs/{{version}}/eloquent) 模型的集合總是以 `Collection` 實例回傳；然而，你可以任意在你應用程式適當的地方使用 `Collection` 類別。

<a name="available-methods"></a>
## 可用的方法

在這份文件剩餘的部份，我們將會探討每一個 `Collection` 類別上可用的方法。要記得的是，所有方法都能被鏈結以流暢地操控底層的陣列。此外，幾乎是所有的方法都會回傳新的 `Collection` 實例，讓你保留原版的集合以備不時之需。

你可以從這張表格中選擇任一方法看使用的範例：

<style>
    #collection-method-list > p {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        column-gap: 2em; -moz-column-gap: 2em; -webkit-column-gap: 2em;
    }

    #collection-method-list a {
        display: block;
    }
</style>

<div id="collection-method-list" markdown="1">
[all](#method-all)
[chunk](#method-chunk)
[collapse](#method-collapse)
[contains](#method-contains)
[count](#method-count)
[diff](#method-diff)
[each](#method-each)
[filter](#method-filter)
[first](#method-first)
[flatten](#method-flatten)
[flip](#method-flip)
[forget](#method-forget)
[forPage](#method-forpage)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[implode](#method-implode)
[intersect](#method-intersect)
[isEmpty](#method-isempty)
[keyBy](#method-keyby)
[keys](#method-keys)
[last](#method-last)
[map](#method-map)
[merge](#method-merge)
[pluck](#method-pluck)
[pop](#method-pop)
[prepend](#method-prepend)
[pull](#method-pull)
[push](#method-push)
[put](#method-put)
[random](#method-random)
[reduce](#method-reduce)
[reject](#method-reject)
[reverse](#method-reverse)
[search](#method-search)
[shift](#method-shift)
[shuffle](#method-shuffle)
[slice](#method-slice)
[sort](#method-sort)
[sortBy](#method-sortby)
[sortByDesc](#method-sortbydesc)
[splice](#method-splice)
[sum](#method-sum)
[take](#method-take)
[toArray](#method-toarray)
[toJson](#method-tojson)
[transform](#method-transform)
[unique](#method-unique)
[values](#method-values)
[where](#method-where)
[whereLoose](#method-whereloose)
[zip](#method-zip)
</div>

<a name="method-listing"></a>
## 方法清單

<style>
    #collection-method code {
        font-size: 14px;
    }

    #collection-method:not(.first-collection-method) {
        margin-top: 50px;
    }
</style>

<a name="method-all"></a>
#### `all()` {#collection-method .first-collection-method}

`all` 方法單純地回傳該集合所代表的底層陣列：

    collect([1, 2, 3])->all();

    // [1, 2, 3]

<a name="method-chunk"></a>
#### `chunk()` {#collection-method}

`chunk` 方法將集合拆成多個給定大小的較小集合：

    $collection = collect([1, 2, 3, 4, 5, 6, 7]);

    $chunks = $collection->chunk(4);

    $chunks->toArray();

    // [[1, 2, 3, 4], [5, 6, 7]]

這個方法在有用到如[Bootstrap](http://getbootstrap.com/css/#grid)之類網格系統的[視圖](/docs/{{version}}/views)內特別有用。想像你有一個 [Eloquent](/docs/{{version}}/eloquent) 模型的集合要顯示在一個網格內：

    @foreach ($products->chunk(3) as $chunk)
        <div class="row">
            @foreach ($chunk as $product)
                <div class="col-xs-4">{{ $product->name }}</div>
            @endforeach
        </div>
    @endforeach

<a name="method-collapse"></a>
#### `collapse()` {#collection-method}

`collapse` 方法將多個陣列組成的集合折疊成單一陣列集合：

    $collection = collect([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

    $collapsed = $collection->collapse();

    $collapsed->all();

    // [1, 2, 3, 4, 5, 6, 7, 8, 9]

<a name="method-contains"></a>
#### `contains()` {#collection-method}

`contains` 方法用來判斷該集合是否含有指定的項目：

    $collection = collect(['name' => 'Desk', 'price' => 100]);

    $collection->contains('Desk');

    // true

    $collection->contains('New York');

    // false

你可以傳入 `contains` 方法一對鍵/值組合，用來判斷該組合是否存在於集合內：

    $collection = collect([
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Chair', 'price' => 100],
    ]);

    $collection->contains('product', 'Bookcase');

    // false

最後，你也可以傳入一個回呼函式到 `contains` 方法內執行你自己的判斷式：

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->contains(function ($key, $value) {
        return $value > 5;
    });

    // false

<a name="method-count"></a>
#### `count()` {#collection-method}

`count` 方法回傳該集合內的項目總數：

    $collection = collect([1, 2, 3, 4]);

    $collection->count();

    // 4

<a name="method-diff"></a>
#### `diff()` {#collection-method}

`diff` 方法拿該集合與其他集合或純 PHP `陣列`進行比較：

    $collection = collect([1, 2, 3, 4, 5]);

    $diff = $collection->diff([2, 4, 6, 8]);

    $diff->all();

    // [1, 3, 5]

<a name="method-each"></a>
#### `each()` {#collection-method}

`each` 方法遍歷集合中的項目，並將之傳入給定的回呼函式：

    $collection = $collection->each(function ($item, $key) {
        //
    });

讓你的回呼函式回傳 `false` 以中斷迴圈：

    $collection = $collection->each(function ($item, $key) {
        if (/* some condition */) {
            return false;
        }
    });

<a name="method-filter"></a>
#### `filter()` {#collection-method}

`filter` 方法以給定的回呼函式篩選集合，只留下那些通過判斷測試的項目：

    $collection = collect([1, 2, 3, 4]);

    $filtered = $collection->filter(function ($item) {
        return $item > 2;
    });

    $filtered->all();

    // [3, 4]

與 `filter` 相對的方法可以檢視 [reject](#method-reject)。

<a name="method-first"></a>
#### `first()` {#collection-method}

`first` 方法回傳集合中，第一個通過給定測試的元素：

    collect([1, 2, 3, 4])->first(function ($key, $value) {
        return $value > 2;
    });

    // 3

你也可以不傳入參數使用 `first` 方法以取得集合中第一個元素。如果集合是空的，則會回傳 `null`：

    collect([1, 2, 3, 4])->first();

    // 1

<a name="method-flatten"></a>
#### `flatten()` {#collection-method}

`flatten` 方法將多維集合轉為一維集合：

    $collection = collect(['name' => 'taylor', 'languages' => ['php', 'javascript']]);

    $flattened = $collection->flatten();

    $flattened->all();

    // ['taylor', 'php', 'javascript'];

<a name="method-flip"></a>
#### `flip()` {#collection-method}

`flip` 方法將集合中的鍵值和對應的數值進行互換：

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $flipped = $collection->flip();

    $flipped->all();

    // ['taylor' => 'name', 'laravel' => 'framework']

<a name="method-forget"></a>
#### `forget()` {#collection-method}

`forget` 方法以鍵值自集合移除掉一個項目：

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $collection->forget('name');

    $collection->all();

    // [framework' => 'laravel']

> **注意：**與大多數其他集合的方法不同，`forget` 不會回傳修改過後的新集合；它會直接修改它被呼叫的集合。

<a name="method-forpage"></a>
#### `forPage()` {#collection-method}

`forPage` 方法回傳含有可以用來在給定頁碼顯示的項目的新集合：

    $collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9])->forPage(2, 3);

    $collection->all();

    // [4, 5, 6]

這個方法要求頁碼和每個頁面要顯示的項目數目。

<a name="method-get"></a>
#### `get()` {#collection-method}

`get` 方法回傳給定鍵值的項目。如果該鍵值不存在，則回傳 `null`：

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $value = $collection->get('name');

    // taylor

你可以選擇性地傳入一個預設值為第二個參數：

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $value = $collection->get('foo', 'default-value');

    // default-value

你甚至可以傳入回呼函式當預設值。如果指定的鍵值不存在，就會回傳回呼函式的執行結果：

    $collection->get('email', function () {
        return 'default-value';
    });

    // default-value

<a name="method-groupby"></a>
#### `groupBy()` {#collection-method}

`groupBy` 方法根據給定的鍵值將集合內的項目進行分組：

    $collection = collect([
        ['account_id' => 'account-x10', 'product' => 'Chair'],
        ['account_id' => 'account-x10', 'product' => 'Bookcase'],
        ['account_id' => 'account-x11', 'product' => 'Desk'],
    ]);

    $grouped = $collection->groupBy('account_id');

    $grouped->toArray();

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

In addition to passing a string `key`, you may also pass a callback. The callback should return the value you wish to key the group by:

    $grouped = $collection->groupBy(function ($item, $key) {
        return substr($item['account_id'], -3);
    });

    $grouped->toArray();

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

<a name="method-has"></a>
#### `has()` {#collection-method}

`has` 方法用來確認集合中是否含有給定的鍵值：

    $collection = collect(['account_id' => 1, 'product' => 'Desk']);

    $collection->has('email');

    // false

<a name="method-implode"></a>
#### `implode()` {#collection-method}

`implode` 方法連接集合中的項目。它的參數依集合中的項目類型而定。

假如集合含有陣列或物件，你應該傳入你希望連接的屬性的鍵值，以及你希望放在數值之間的「黏著」字串：

    $collection = collect([
        ['account_id' => 1, 'product' => 'Desk'],
        ['account_id' => 2, 'product' => 'Chair'],
    ]);

    $collection->implode('product', ', ');

    // Desk, Chair

假如集合只含有簡單的字串或數字，就只要傳入黏著字串作該方法唯一的參數：

    collect([1, 2, 3, 4, 5])->implode('-');

    // '1-2-3-4-5'

<a name="method-intersect"></a>
#### `intersect()` {#collection-method}

`intersect` 方法移除任何給定`陣列`或集合內所沒有的數值：

    $collection = collect(['Desk', 'Sofa', 'Chair']);

    $intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

    $intersect->all();

    // [0 => 'Desk', 2 => 'Chair']

如你所見，最後出來的集合將會保留原始集合的鍵值。

<a name="method-isempty"></a>
#### `isEmpty()` {#collection-method}

假如集合是空的，`isEmpty` 方法會回傳 `true`：否則回傳 `false`：

    collect([])->isEmpty();

    // true

<a name="method-keyby"></a>
#### `keyBy()` {#collection-method}

Keys the collection by the given key:

    $collection = collect([
        ['product_id' => 'prod-100', 'name' => 'desk'],
        ['product_id' => 'prod-200', 'name' => 'chair'],
    ]);

    $keyed = $collection->keyBy('product_id');

    $keyed->all();

    /*
        [
            'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
            'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
        ]
    */

If multiple items have the same key, only the last one will appear in the new collection.

You may also pass your own callback, which should return the value to key the collection by:

    $keyed = $collection->keyBy(function ($item) {
        return strtoupper($item['product_id']);
    });

    $keyed->all();

    /*
        [
            'PROD-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
            'PROD-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
        ]
    */


<a name="method-keys"></a>
#### `keys()` {#collection-method}

`keys` 方法回傳該集合所有的鍵值：

    $collection = collect([
        'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
        'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]);

    $keys = $collection->keys();

    $keys->all();

    // ['prod-100', 'prod-200']

<a name="method-last"></a>
#### `last()` {#collection-method}

`last` 方法回傳集合中，最後一個通過給定測試的元素：

    collect([1, 2, 3, 4])->last(function ($key, $value) {
        return $value < 3;
    });

    // 2

你也可以不傳入參數使用 `last` 方法以取得集合中最後一個元素。如果集合是空的，則會回傳 `null`：

    collect([1, 2, 3, 4])->last();

    // 4

<a name="method-map"></a>
#### `map()` {#collection-method}

`map` 方法遍歷整個集合並將每一個數值傳入給定的回呼函式。回呼函式可以任意修改並回傳項目，於是形成修改過的項目組成的新集合：

    $collection = collect([1, 2, 3, 4, 5]);

    $multiplied = $collection->map(function ($item, $key) {
        return $item * 2;
    });

    $multiplied->all();

    // [2, 4, 6, 8, 10]

> **注意：**正如集合大多數其他的方法一樣，`map` 回傳一個新集合實例；它並沒有修改被呼叫的集合。假如你想改變原始的集合，得使用 [`transform`](#method-transform) 方法。

<a name="method-merge"></a>
#### `merge()` {#collection-method}

The `merge` method merges the given array into the collection. Any string key in the array matching a string key in the collection will overwrite the value in the collection:

    $collection = collect(['product_id' => 1, 'name' => 'Desk']);

    $merged = $collection->merge(['price' => 100, 'discount' => false]);

    $merged->all();

    // ['product_id' => 1, 'name' => 'Desk', 'price' => 100, 'discount' => false]

If the given array's keys are numeric, the values will be appended to the end of the collection:

    $collection = collect(['Desk', 'Chair']);

    $merged = $collection->merge(['Bookcase', 'Door']);

    $merged->all();

    // ['Desk', 'Chair', 'Bookcase', 'Door']

<a name="method-pluck"></a>
#### `pluck()` {#collection-method}

The `pluck` method retrieves all of the collection values for a given key:

    $collection = collect([
        ['product_id' => 'prod-100', 'name' => 'Desk'],
        ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]);

    $plucked = $collection->pluck('name');

    $plucked->all();

    // ['Desk', 'Chair']

You may also specify how you wish the resulting collection to be keyed:

    $plucked = $collection->pluck('name', 'product_id');

    $plucked->all();

    // ['prod-100' => 'Desk', 'prod-200' => 'Chair']

<a name="method-pop"></a>
#### `pop()` {#collection-method}

The `pop` method removes and returns the last item from the collection:

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->pop();

    // 5

    $collection->all();

    // [1, 2, 3, 4]

<a name="method-prepend"></a>
#### `prepend()` {#collection-method}

The `prepend` method adds an item to the beginning of the collection:

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->prepend(0);

    $collection->all();

    // [0, 1, 2, 3, 4, 5]

<a name="method-pull"></a>
#### `pull()` {#collection-method}

The `pull` method removes and returns an item from the collection by its key:

    $collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

    $collection->pull('name');

    // 'Desk'

    $collection->all();

    // ['product_id' => 'prod-100']

<a name="method-push"></a>
#### `push()` {#collection-method}

The `push` method appends an item to the end of the collection:

    $collection = collect([1, 2, 3, 4]);

    $collection->push(5);

    $collection->all();

    // [1, 2, 3, 4, 5]

<a name="method-put"></a>
#### `put()` {#collection-method}

The `put` method sets the given key and value in the collection:

    $collection = collect(['product_id' => 1, 'name' => 'Desk']);

    $collection->put('price', 100);

    $collection->all();

    // ['product_id' => 1, 'name' => 'Desk', 'price' => 100]

<a name="method-random"></a>
#### `random()` {#collection-method}

The `random` method returns a random item from the collection:

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->random();

    // 4 - (retrieved randomly)

You may optionally pass an integer to `random`. If that integer is more than `1`, a collection of items is returned:

    $random = $collection->random(3);

    $random->all();

    // [2, 4, 5] - (retrieved randomly)

<a name="method-reduce"></a>
#### `reduce()` {#collection-method}

The `reduce` method reduces the collection to a single value, passing the result of each iteration into the subsequent iteration:

    $collection = collect([1, 2, 3]);

    $total = $collection->reduce(function ($carry, $item) {
        return $carry + $item;
    });

    // 6

The value for `$carry` on the first iteration is `null`; however, you may specify its initial value by passing a second argument to `reduce`:

    $collection->reduce(function ($carry, $item) {
        return $carry + $item;
    }, 4);

    // 10

<a name="method-reject"></a>
#### `reject()` {#collection-method}

The `reject` method filters the collection using the given callback. The callback should return `true` for any items it wishes to remove from the resulting collection:

    $collection = collect([1, 2, 3, 4]);

    $filtered = $collection->reject(function ($item) {
        return $item > 2;
    });

    $filtered->all();

    // [1, 2]

For the inverse of the `reject` method, see the [`filter`](#method-filter) method.

<a name="method-reverse"></a>
#### `reverse()` {#collection-method}

The `reverse` method reverses the order of the collection's items:

    $collection = collect([1, 2, 3, 4, 5]);

    $reversed = $collection->reverse();

    $reversed->all();

    // [5, 4, 3, 2, 1]

<a name="method-search"></a>
#### `search()` {#collection-method}

The `search` method searches the collection for the given value and returns its key if found. If the item is not found, `false` is returned.

    $collection = collect([2, 4, 6, 8]);

    $collection->search(4);

    // 1

The search is done using a "loose" comparison. To use strict comparison, pass `true` as the second argument to the method:

    $collection->search('4', true);

    // false

Alternatively, you may pass in your own callback to search for the first item that passes your truth test:

    $collection->search(function ($item, $key) {
        return $item > 5;
    });

    // 2

<a name="method-shift"></a>
#### `shift()` {#collection-method}

The `shift` method removes and returns the first item from the collection:

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->shift();

    // 1

    $collection->all();

    // [2, 3, 4, 5]

<a name="method-shuffle"></a>
#### `shuffle()` {#collection-method}

The `shuffle` method randomly shuffles the items in the collection:

    $collection = collect([1, 2, 3, 4, 5]);

    $shuffled = $collection->shuffle();

    $shuffled->all();

    // [3, 2, 5, 1, 4] // (generated randomly)

<a name="method-slice"></a>
#### `slice()` {#collection-method}

The `slice` method returns a slice of the collection starting at the given index:

    $collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

    $slice = $collection->slice(4);

    $slice->all();

    // [5, 6, 7, 8, 9, 10]

If you would like to limit the size of the returned slice, pass the desired size as the second argument to the method:

    $slice = $collection->slice(4, 2);

    $slice->all();

    // [5, 6]

The returned slice will have new, numerically indexed keys. If you wish to preserve the original keys, pass `true` as the third argument to the method.

<a name="method-sort"></a>
#### `sort()` {#collection-method}

The `sort` method sorts the collection:

    $collection = collect([5, 3, 1, 2, 4]);

    $sorted = $collection->sort();

    $sorted->values()->all();

    // [1, 2, 3, 4, 5]

The sorted collection keeps the original array keys. In this example we used the [`values`](#method-values) method to reset the keys to consecutively numbered indexes.

For sorting a collection of nested arrays or objects, see the [`sortBy`](#method-sortby) and [`sortByDesc`](#method-sortbydesc) methods.

If your sorting needs are more advanced, you may pass a callback to `sort` with your own algorithm. Refer to the PHP documentation on [`usort`](http://php.net/manual/en/function.usort.php#refsect1-function.usort-parameters), which is what the collection's `sort` method calls under the hood.

<a name="method-sortby"></a>
#### `sortBy()` {#collection-method}

The `sortBy` method sorts the collection by the given key:

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

The sorted collection keeps the original array keys. In this example we used the [`values`](#method-values) method to reset the keys to consecutively numbered indexes.

You can also pass your own callback to determine how to sort the collection values:

    $collection = collect([
        ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
        ['name' => 'Chair', 'colors' => ['Black']],
        ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
    ]);

    $sorted = $collection->sortBy(function ($product, $key) {
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

<a name="method-sortbydesc"></a>
#### `sortByDesc()` {#collection-method}

This method has the same signature as the [`sortBy`](#method-sortby) method, but will sort the collection in the opposite order.

<a name="method-splice"></a>
#### `splice()` {#collection-method}

The `splice` method removes and returns a slice of items starting at the specified index:

    $collection = collect([1, 2, 3, 4, 5]);

    $chunk = $collection->splice(2);

    $chunk->all();

    // [3, 4, 5]

    $collection->all();

    // [1, 2]

You may pass a second argument to limit the size of the resulting chunk:

    $collection = collect([1, 2, 3, 4, 5]);

    $chunk = $collection->splice(2, 1);

    $chunk->all();

    // [3]

    $collection->all();

    // [1, 2, 4, 5]

In addition, you can pass a third argument containing the new items to replace the items removed from the collection:

    $collection = collect([1, 2, 3, 4, 5]);

    $chunk = $collection->splice(2, 1, [10, 11]);

    $chunk->all();

    // [3]

    $collection->all();

    // [1, 2, 10, 11, 4, 5]

<a name="method-sum"></a>
#### `sum()` {#collection-method}

The `sum` method returns the sum of all items in the collection:

    collect([1, 2, 3, 4, 5])->sum();

    // 15

If the collection contains nested arrays or objects, you should pass a key to use for determining which values to sum:

    $collection = collect([
        ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
        ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
    ]);

    $collection->sum('pages');

    // 1272

In addition, you may pass your own callback to determine which values of the collection to sum:

    $collection = collect([
        ['name' => 'Chair', 'colors' => ['Black']],
        ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
        ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
    ]);

    $collection->sum(function ($product) {
        return count($product['colors']);
    });

    // 6

<a name="method-take"></a>
#### `take()` {#collection-method}

The `take` method returns a new collection with the specified number of items:

    $collection = collect([0, 1, 2, 3, 4, 5]);

    $chunk = $collection->take(3);

    $chunk->all();

    // [0, 1, 2]

You may also pass a negative integer to take the specified amount of items from the end of the collection:

    $collection = collect([0, 1, 2, 3, 4, 5]);

    $chunk = $collection->take(-2);

    $chunk->all();

    // [4, 5]

<a name="method-toarray"></a>
#### `toArray()` {#collection-method}

The `toArray` method converts the collection into a plain PHP `array`. If the collection's values are [Eloquent](/docs/{{version}}/eloquent) models, the models will also be converted to arrays:

    $collection = collect(['name' => 'Desk', 'price' => 200]);

    $collection->toArray();

    /*
        [
            ['name' => 'Desk', 'price' => 200],
        ]
    */

> **Note:** `toArray` also converts all of its nested objects to an array. If you want to get the underlying array as is, use the [`all`](#method-all) method instead.

<a name="method-tojson"></a>
#### `toJson()` {#collection-method}

The `toJson` method converts the collection into JSON:

    $collection = collect(['name' => 'Desk', 'price' => 200]);

    $collection->toJson();

    // '{"name":"Desk","price":200}'

<a name="method-transform"></a>
#### `transform()` {#collection-method}

The `transform` method iterates over the collection and calls the given callback with each item in the collection. The items in the collection will be replaced by the values returned by the callback:

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->transform(function ($item, $key) {
        return $item * 2;
    });

    $collection->all();

    // [2, 4, 6, 8, 10]

> **Note:** Unlike most other collection methods, `transform` modifies the collection itself. If you wish to create a new collection instead, use the [`map`](#method-map) method.

<a name="method-unique"></a>
#### `unique()` {#collection-method}

The `unique` method returns all of the unique items in the collection:

    $collection = collect([1, 1, 2, 2, 3, 4, 2]);

    $unique = $collection->unique();

    $unique->values()->all();

    // [1, 2, 3, 4]

The returned collection keeps the original array keys. In this example we used the [`values`](#method-values) method to reset the keys to consecutively numbered indexes.

When dealing with nested arrays or objects, you may specify the key used to determine uniqueness:

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

You may also pass your own callback to determine item uniqueness:

    $unique = $collection->unique(function ($item) {
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

<a name="method-values"></a>
#### `values()` {#collection-method}

The `values` method returns a new collection with the keys reset to consecutive integers:

    $collection = collect([
        10 => ['product' => 'Desk', 'price' => 200],
        11 => ['product' => 'Desk', 'price' => 200]
    ]);

    $values = $collection->values();

    $values->all();

    /*
        [
            0 => ['product' => 'Desk', 'price' => 200],
            1 => ['product' => 'Desk', 'price' => 200],
        ]
    */
<a name="method-where"></a>
#### `where()` {#collection-method}

The `where` method filters the collection by a given key / value pair:

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

The `where` method uses strict comparisons when checking item values. Use the [`whereLoose`](#where-loose) method to filter using "loose" comparisons.

<a name="method-whereloose"></a>
#### `whereLoose()` {#collection-method}

This method has the same signature as the [`where`](#method-where) method; however, all values are compared using "loose" comparisons.

<a name="method-zip"></a>
#### `zip()` {#collection-method}

The `zip` method merges together the values of the given array with the values of the collection at the corresponding index:

    $collection = collect(['Chair', 'Desk']);

    $zipped = $collection->zip([100, 200]);

    $zipped->all();

    // [['Chair', 100], ['Desk', 200]]
