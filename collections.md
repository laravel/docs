# 集合

- [簡介](#introduction)
- [建立集合](#creating-collections)
- [可用的方法](#available-methods)

<a name="introduction"></a>
## 簡介

`Illuminate\Support\Collection` 類別提供一個流暢、便利的封裝來操控陣列資料。舉個例子，查看下列的程式碼。我們將用 `collect` 輔助方法從陣列建立一個新的集合實例，對每一個元素執行 `strtoupper` 函式，然後移除所有的空元素：

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

預設 [Eloquent](/docs/{{version}}/eloquent) 模型的集合總是以 `Collection` 實例回傳；然而，你可以任意在你應用程式任何適當的場合使用 `Collection` 類別。

<a name="available-methods"></a>
## 可用的方法

在這份文件剩餘的部份，我們將會探討每一個 `Collection` 類別上可用的方法。要記得的是，所有方法都能被鏈結以流暢地操控底層的陣列。此外，幾乎所有的方法都會回傳新的 `Collection` 實例，讓你保留原版的集合以備不時之需。

你可以從這張表格中選擇任一方法看使用範例：

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

這個方法在有用到網格系統如 [Bootstrap](http://getbootstrap.com/css/#grid) 的[視圖](/docs/{{version}}/views)內特別有用。想像你有一個 [Eloquent](/docs/{{version}}/eloquent) 模型的集合要顯示在一個網格內：

    @foreach ($products->chunk(3) as $chunk)
        <div class="row">
            @foreach ($chunk as $product)
                <div class="col-xs-4">{{ $product->name }}</div>
            @endforeach
        </div>
    @endforeach

<a name="method-collapse"></a>
#### `collapse()` {#collection-method}

`collapse` 方法將多個陣列組成的集合折成單一陣列集合：

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

你可以將一對鍵/值傳入 `contains` 方法，用來判斷該組合是否存在於集合內：

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

<a name="method-every"></a>
#### `every()` {#collection-method}

The `every` method creates a new collection consisting of every n-th element:

    $collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

    $collection->every(4);

    // ['a', 'e']

You may optionally pass offset as the second argument:

    $collection->every(4, 1);

    // ['b', 'f']

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

`flip` 方法將集合中的鍵和對應的數值進行互換：

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $flipped = $collection->flip();

    $flipped->all();

    // ['taylor' => 'name', 'laravel' => 'framework']

<a name="method-forget"></a>
#### `forget()` {#collection-method}

`forget` 方法以鍵自集合移除掉一個項目：

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

`get` 方法回傳給定鍵的項目。如果該鍵不存在，則回傳 `null`：

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $value = $collection->get('name');

    // taylor

你可以選擇性地傳入一個預設值為第二個參數：

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $value = $collection->get('foo', 'default-value');

    // default-value

你甚至可以傳入回呼函式當預設值。如果指定的鍵不存在，就會回傳回呼函式的執行結果：

    $collection->get('email', function () {
        return 'default-value';
    });

    // default-value

<a name="method-groupby"></a>
#### `groupBy()` {#collection-method}

`groupBy` 方法根據給定的鍵替集合內的項目分組：

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

除了傳入字串的`鍵`之外，你也可以傳入回呼函式。該函式應該回傳你希望用來分組的鍵的值。

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

`has` 方法用來確認集合中是否含有給定的鍵：

    $collection = collect(['account_id' => 1, 'product' => 'Desk']);

    $collection->has('email');

    // false

<a name="method-implode"></a>
#### `implode()` {#collection-method}

`implode` 方法連接集合中的項目。它的參數依集合中的項目類型而定。

假如集合含有陣列或物件，你應該傳入你希望連接的屬性的鍵，以及你希望放在數值之間的「黏著」字串：

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

如你所見，最後出來的集合將會保留原始集合的鍵。

<a name="method-isempty"></a>
#### `isEmpty()` {#collection-method}

假如集合是空的，`isEmpty` 方法會回傳 `true`：否則回傳 `false`：

    collect([])->isEmpty();

    // true

<a name="method-keyby"></a>
#### `keyBy()` {#collection-method}

以給定鍵的值作為集合項目的鍵：

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

如果多個項目有同樣的鍵，只有最後一個會出現在新的集合內。

你也可以傳入自己的回呼函式，該函式應該回傳集合的鍵的值：

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

`keys` 方法回傳該集合所有的鍵：

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

`merge` 方法將給定的陣列合併進集合。陣列字串鍵與集合字串鍵相同的將會覆蓋掉集合的數值：

    $collection = collect(['product_id' => 1, 'name' => 'Desk']);

    $merged = $collection->merge(['price' => 100, 'discount' => false]);

    $merged->all();

    // ['product_id' => 1, 'name' => 'Desk', 'price' => 100, 'discount' => false]

如果給定陣列的鍵為數字，則數值將會附加在集合的後面：

    $collection = collect(['Desk', 'Chair']);

    $merged = $collection->merge(['Bookcase', 'Door']);

    $merged->all();

    // ['Desk', 'Chair', 'Bookcase', 'Door']

<a name="method-pluck"></a>
#### `pluck()` {#collection-method}

`pluck` 方法取得所有集合中給定鍵的值：

    $collection = collect([
        ['product_id' => 'prod-100', 'name' => 'Desk'],
        ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]);

    $plucked = $collection->pluck('name');

    $plucked->all();

    // ['Desk', 'Chair']

你也可以指定要怎麼給最後出來的集合分配鍵：

    $plucked = $collection->pluck('name', 'product_id');

    $plucked->all();

    // ['prod-100' => 'Desk', 'prod-200' => 'Chair']

<a name="method-pop"></a>
#### `pop()` {#collection-method}

`pop` 方法移除並回傳集合最後一個項目：

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->pop();

    // 5

    $collection->all();

    // [1, 2, 3, 4]

<a name="method-prepend"></a>
#### `prepend()` {#collection-method}

`prepend` 方法在集合前面增加一個項目：

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->prepend(0);

    $collection->all();

    // [0, 1, 2, 3, 4, 5]

<a name="method-pull"></a>
#### `pull()` {#collection-method}

`pull` 方法以鍵從集合中移除並回傳一個項目：

    $collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

    $collection->pull('name');

    // 'Desk'

    $collection->all();

    // ['product_id' => 'prod-100']

<a name="method-push"></a>
#### `push()` {#collection-method}

`push` 方法附加一個項目到集合後面：

    $collection = collect([1, 2, 3, 4]);

    $collection->push(5);

    $collection->all();

    // [1, 2, 3, 4, 5]

<a name="method-put"></a>
#### `put()` {#collection-method}

`put` 在集合內設定一個給定鍵和數值：

    $collection = collect(['product_id' => 1, 'name' => 'Desk']);

    $collection->put('price', 100);

    $collection->all();

    // ['product_id' => 1, 'name' => 'Desk', 'price' => 100]

<a name="method-random"></a>
#### `random()` {#collection-method}

`random` 方法從集合中隨機回傳一個項目：

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->random();

    // 4 - (retrieved randomly)

你可以選擇性地傳入一個整數到 `random`。如果該整數大於 `1`，則會回傳一個集合：

    $random = $collection->random(3);

    $random->all();

    // [2, 4, 5] - (retrieved randomly)

<a name="method-reduce"></a>
#### `reduce()` {#collection-method}

`reduce` 方法將集合縮減到單一數值，該方法會將每次迭代的結果傳入到下一次迭代：

    $collection = collect([1, 2, 3]);

    $total = $collection->reduce(function ($carry, $item) {
        return $carry + $item;
    });

    // 6

第一次迭代時 `$carry` 的數值為 `null`；然而你也可以傳入第二個參數進 `reduce` 以指定它的初始值：

    $collection->reduce(function ($carry, $item) {
        return $carry + $item;
    }, 4);

    // 10

<a name="method-reject"></a>
#### `reject()` {#collection-method}

`reject` 方法以給定的回呼函式篩選集合。該回呼函式應該對希望從最終集合移除掉的項目回傳 `true`：

    $collection = collect([1, 2, 3, 4]);

    $filtered = $collection->reject(function ($item) {
        return $item > 2;
    });

    $filtered->all();

    // [1, 2]

與 `reject` 相對的方法可以檢視 [`filter`](#method-filter) 方法。

<a name="method-reverse"></a>
#### `reverse()` {#collection-method}

`reverse` 方法倒轉集合內項目的順序：

    $collection = collect([1, 2, 3, 4, 5]);

    $reversed = $collection->reverse();

    $reversed->all();

    // [5, 4, 3, 2, 1]

<a name="method-search"></a>
#### `search()` {#collection-method}

`search` 方法在集合內搜尋給定的數值並回傳找到的鍵。假如找不到項目，則回傳 `false`：

    $collection = collect([2, 4, 6, 8]);

    $collection->search(4);

    // 1

搜尋是用「寬鬆」比對來進行。要使用嚴格比對，就傳入 `true` 為該方法的第二個參數：

    $collection->search('4', true);

    // false

另外，你可以傳入你自己的回呼函式來搜尋第一個通過你判斷測試的項目：

    $collection->search(function ($item, $key) {
        return $item > 5;
    });

    // 2

<a name="method-shift"></a>
#### `shift()` {#collection-method}

`shift` 方法移除並回傳集合的第一個項目：

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->shift();

    // 1

    $collection->all();

    // [2, 3, 4, 5]

<a name="method-shuffle"></a>
#### `shuffle()` {#collection-method}

`shuffle` 方法隨機排序集合的項目：

    $collection = collect([1, 2, 3, 4, 5]);

    $shuffled = $collection->shuffle();

    $shuffled->all();

    // [3, 2, 5, 1, 4] // (generated randomly)

<a name="method-slice"></a>
#### `slice()` {#collection-method}

`slice` 方法回傳集合從給定索引開始的一部分切片：

    $collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

    $slice = $collection->slice(4);

    $slice->all();

    // [5, 6, 7, 8, 9, 10]

如果你想限制回傳切片的大小，就傳入想要的大小為方法的第二個參數：

    $slice = $collection->slice(4, 2);

    $slice->all();

    // [5, 6]

回傳的切片將會有以數字索引的新鍵。假如你希望保留原始的鍵，傳入 `true` 為方法的第三個參數。

<a name="method-sort"></a>
#### `sort()` {#collection-method}

`sort` 方法對集合排序：

    $collection = collect([5, 3, 1, 2, 4]);

    $sorted = $collection->sort();

    $sorted->values()->all();

    // [1, 2, 3, 4, 5]

排序過的集合保有原來的陣列鍵。在這個例子中我們用了 [`values`](#method-values) 方法重設鍵為連續的數字索引。

要排序內含陣列或物件的集合，見 [`sortBy`](#method-sortby) 和 [`sortByDesc`](#method-sortbydesc) 方法。

假如你需要更進階的排序，你可以傳入回呼函式以你自己的演算法進行`排序`。參考 PHP 文件的 [`usort`](http://php.net/manual/en/function.usort.php#refsect1-function.usort-parameters)，這是集合的 `sort` 方法在背後所呼叫的函式。

<a name="method-sortby"></a>
#### `sortBy()` {#collection-method}

`sortBy` 方法以給定的鍵排序集合：

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

排序過的集合保有原來的陣列鍵。在這個例子中我們用了 [`values`](#method-values) 方法重設鍵為連續的數字索引。

你也可以傳入自己的回呼函式以決定如何排序集合數值：

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

這個方法與 [`sortBy`](#method-sortby) 有著一樣的形式，但是會以相反的順序來排序集合：

<a name="method-splice"></a>
#### `splice()` {#collection-method}

`splice` 方法移除並回傳從指定的索引開始的一小切片項目：

    $collection = collect([1, 2, 3, 4, 5]);

    $chunk = $collection->splice(2);

    $chunk->all();

    // [3, 4, 5]

    $collection->all();

    // [1, 2]

你可以傳入第二個參數以限制大小：

    $collection = collect([1, 2, 3, 4, 5]);

    $chunk = $collection->splice(2, 1);

    $chunk->all();

    // [3]

    $collection->all();

    // [1, 2, 4, 5]

此外，你可以傳入含有新項目的第三個參數以取代集合中被移除的項目：

    $collection = collect([1, 2, 3, 4, 5]);

    $chunk = $collection->splice(2, 1, [10, 11]);

    $chunk->all();

    // [3]

    $collection->all();

    // [1, 2, 10, 11, 4, 5]

<a name="method-sum"></a>
#### `sum()` {#collection-method}

`sum` 方法回傳集合內所有項目的總和：

    collect([1, 2, 3, 4, 5])->sum();

    // 15

如果集合包含陣列或物件，你應該傳入一個鍵來確認要用哪些數值來計算總合：

    $collection = collect([
        ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
        ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
    ]);

    $collection->sum('pages');

    // 1272

此外，你可以傳入自己的回呼函式來決定要用哪些數值來計算總合：

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

`take` 方法回傳有著指定數量項目的集合：

    $collection = collect([0, 1, 2, 3, 4, 5]);

    $chunk = $collection->take(3);

    $chunk->all();

    // [0, 1, 2]

你也可以傳入負整數以取得從集合後面來算指定數量的項目：

    $collection = collect([0, 1, 2, 3, 4, 5]);

    $chunk = $collection->take(-2);

    $chunk->all();

    // [4, 5]

<a name="method-toarray"></a>
#### `toArray()` {#collection-method}

`toArray` 方法將集合轉換成純 PHP `陣列`。假如集合的數值是 [Eloquent](/docs/{{version}}/eloquent) 模型，也會被轉換成陣列：

    $collection = collect(['name' => 'Desk', 'price' => 200]);

    $collection->toArray();

    /*
        [
            ['name' => 'Desk', 'price' => 200],
        ]
    */

> **注意：**`toArray` 也會轉換所有內嵌的物件為陣列。假如你希望取得原本的底層陣列，改用 [`all`](#method-all) 方法。

<a name="method-tojson"></a>
#### `toJson()` {#collection-method}

`toJson` 方法將集合轉換成 JSON：

    $collection = collect(['name' => 'Desk', 'price' => 200]);

    $collection->toJson();

    // '{"name":"Desk","price":200}'

<a name="method-transform"></a>
#### `transform()` {#collection-method}

`transform` 方法遍歷集合並對集合內每一個項目呼叫給定的回呼函式。集合的項目將會被回呼函式回傳的數值取代掉：

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->transform(function ($item, $key) {
        return $item * 2;
    });

    $collection->all();

    // [2, 4, 6, 8, 10]

> **注意：**與大多數其他集合的方法不同，`transform` 會修改集合本身。如果你希望建立新集合，就改用 [`map`](#method-map) 方法。

<a name="method-unique"></a>
#### `unique()` {#collection-method}

`unique` 方法回傳集合中所有獨特的項目：

    $collection = collect([1, 1, 2, 2, 3, 4, 2]);

    $unique = $collection->unique();

    $unique->values()->all();

    // [1, 2, 3, 4]

排序過的集合保有原來的陣列鍵。在這個例子中我們用了 [`values`](#method-values) 方法重設鍵為連續的數字索引。

當處理內嵌的陣列或物件，你可以指定用來決定獨特性的鍵：

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

你可以傳入自己的回呼函式來決定項目的獨特性：

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

`values` 方法回傳鍵重設為連續整數的的新集合：

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

`where` 方法以一對給定的鍵／數值篩選集合：

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

`where` 方法以嚴格比對檢查數值。使用 [`whereLoose`](#where-loose) 方法以寬鬆比對進行篩選。

<a name="method-whereloose"></a>
#### `whereLoose()` {#collection-method}

這個方法與 [`where`](#method-where) 方法有著一樣的形式；但是會以寬鬆比對來比對數值：

<a name="method-zip"></a>
#### `zip()` {#collection-method}

`zip` 方法將集合與給定陣列同樣索引的值合併在一起：

    $collection = collect(['Chair', 'Desk']);

    $zipped = $collection->zip([100, 200]);

    $zipped->all();

    // [['Chair', 100], ['Desk', 200]]
