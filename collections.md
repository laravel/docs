# Collections

- [Introdução](#introduction)
- [Criando Coleções](#creating-collections)
- [Métodos Disponíveis](#available-methods)

<a name="introduction"></a>
## Introdução

A classe `Illuminate\Support\Collection` provê um container conveniente e flexivel para trabalhar com coleções (arrays). Por exemplo, confira o código abaixo. Nós usamos o helper `collect` para criar uma nova instância da classe Collection passando como parâmetro um array, então usamos a função `strtoupper` em cada elemento do array, e depois removemos todos os elementos vazios:

    $collection = collect(['taylor', 'abigail', null])->map(function ($name) {
        return strtoupper($name);
    })
    ->reject(function ($name) {
        return empty($name);
    });


Como você pode ver, a classe `Collection` permite que você realize ações em cadeia com a coleção de dados. Em geral, cada método da `Collection` retorna uma nova instância da classe `Collection`.

<a name="creating-collections"></a>
## Criando Collections

Como mencionado anteriormente, o helper `collect` retorna uma instância da classe `Illuminate\Support\Collection` para o array dado. Então, criar uma collection é simples como:

    $collection = collect([1, 2, 3]);

Por padrão, coleções de models do [Eloquent](/docs/{{version}}/eloquent) serão sempre retornadas como instância da classe `Collection`; Entretanto, sinta-se livre para usar a classe `Collection` em sua aplicação sempre que lhe for conveniente.

<a name="available-methods"></a>
## Métodos disponíveis

Para o restante desta documentação, vamos discutir cada método disponível na classe `Collection`. Lembre-se, todos estes métodos podem ser encadeados para manipular facilmente a coleção de dados. Além disso, quase todos os métodos retornam uma nova instância da classe `Collection`, permitindo-lhe preservar a coleção de dados original quando necessário.

Você pode escolher qualquer método a partir desta tabela para ver um exemplo de seu uso:

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
[avg](#method-avg)
[chunk](#method-chunk)
[collapse](#method-collapse)
[contains](#method-contains)
[count](#method-count)
[diff](#method-diff)
[each](#method-each)
[every](#method-every)
[except](#method-except)
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
[max](#method-max)
[merge](#method-merge)
[min](#method-min)
[only](#method-only)
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
## Listando Métodos

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

O método `all` simplesmente retorna coleção completa:

    collect([1, 2, 3])->all();

    // [1, 2, 3]

<a name="method-avg"></a>
#### `avg()` {#collection-method}

O método `avg` retorna a média de todos os itens na coleção:

    collect([1, 2, 3, 4, 5])->avg();

    // 3

Se a coleção contém arrays aninhados ou objetos, você deve passar uma chave para determinar quais valores serão usados para calcular a média:

    $collection = collect([
        ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
        ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
    ]);

    $collection->avg('pages');

    // 636

<a name="method-chunk"></a>
#### `chunk()` {#collection-method}

O método `chunk` quebra a coleção em múltiplas coleções menores de acordo com um determinado tamanho:

    $collection = collect([1, 2, 3, 4, 5, 6, 7]);

    $chunks = $collection->chunk(4);

    $chunks->toArray();

    // [[1, 2, 3, 4], [5, 6, 7]]

Este método é especialmente útil nas [views](/docs/{{version}}/views) quando se trabalha com um sistema de grids como [Bootstrap](http://getbootstrap.com/css/#grid). Imagine que você tenha uma coleção do [Eloquent](/docs/{{version}}/eloquent) e deseje exibir em grids:

    @foreach ($products->chunk(3) as $chunk)
        <div class="row">
            @foreach ($chunk as $product)
                <div class="col-xs-4">{{ $product->name }}</div>
            @endforeach
        </div>
    @endforeach

<a name="method-collapse"></a>
#### `collapse()` {#collection-method}

O método `collapse` une várias coleções em apenas uma:

    $collection = collect([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

    $collapsed = $collection->collapse();

    $collapsed->all();

    // [1, 2, 3, 4, 5, 6, 7, 8, 9]

<a name="method-contains"></a>
#### `contains()` {#collection-method}

O método `contains` determina se a coleção contém um determinado item e retorna um boleano:

    $collection = collect(['name' => 'Desk', 'price' => 100]);

    $collection->contains('Desk');

    // true

    $collection->contains('New York');

    // false

Você também pode passar um array de chaves para o método `contains`, que ele irá determinar se os dados do array passado existem na coleção:

    $collection = collect([
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Chair', 'price' => 100],
    ]);

    $collection->contains('product', 'Bookcase');

    // false

Finalmente, você também pode passar uma chamada de retorno para o método `contains` para realizar seu próprio teste:

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->contains(function ($key, $value) {
        return $value > 5;
    });

    // false

<a name="method-count"></a>
#### `count()` {#collection-method}

O método `count` retorna o número total de itens na coleção:

    $collection = collect([1, 2, 3, 4]);

    $collection->count();

    // 4

<a name="method-diff"></a>
#### `diff()` {#collection-method}

O método `diff` compara a uma coleção com outra coleção ou um `array` simples:

    $collection = collect([1, 2, 3, 4, 5]);

    $diff = $collection->diff([2, 4, 6, 8]);

    $diff->all();

    // [1, 3, 5]

<a name="method-each"></a>
#### `each()` {#collection-method}

Os método `each` itera sobre os itens da coleção e passa para cada item da coleção uma chamada de retorno:

    $collection = $collection->each(function ($item, $key) {
        //
    });

Retorne `false` pra sair de uma chamada de retorno ou um loop:

    $collection = $collection->each(function ($item, $key) {
        if (/* some condition */) {
            return false;
        }
    });

<a name="method-every"></a>
#### `every()` {#collection-method}

<!--The `every` method creates a new collection consisting of every n-th element:-->
O método `every` cria uma nova coleção que consiste a cada elemento n-th:

    $collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

    $collection->every(4);

    // ['a', 'e']

Você pode opcionalmente passar como o segundo argumento, um deslocamento:

    $collection->every(4, 1);

    // ['b', 'f']

<a name="method-except"></a>
#### `except()` {#collection-method}

O método `except` retorna todos os itens na coleção, exceto aqueles que tiveram as chaves especificadas:

    $collection = collect(['product_id' => 1, 'name' => 'Desk', 'price' => 100, 'discount' => false]);

    $filtered = $collection->except(['price', 'discount']);

    $filtered->all();

    // ['product_id' => 1, 'name' => 'Desk']

Para o inverso do `except`, veja o método [only](#method-only).

<a name="method-filter"></a>
#### `filter()` {#collection-method}

O método `filter` filtra a coleção por um determinado retorno de chamada, mantendo apenas os itens que passam na condição:

    $collection = collect([1, 2, 3, 4]);

    $filtered = $collection->filter(function ($item) {
        return $item > 2;
    });

    $filtered->all();

    // [3, 4]

Para o inverso de `filter`, veja o método [reject](#method-reject).

<a name="method-first"></a>
#### `first()` {#collection-method}

O método `first` retorna o primeiro elemento na coleção que atende a condição dada:

    collect([1, 2, 3, 4])->first(function ($key, $value) {
        return $value > 2;
    });

    // 3

Você também pode chamar o método `first` sem argumentos para obter o primeiro elemento da coleção. Se a coleção estiver vazia, é retornado `null`:

    collect([1, 2, 3, 4])->first();

    // 1

<a name="method-flatten"></a>
#### `flatten()` {#collection-method}

O método `flatten` alinhará uma coleção multidimensional em uma única dimensão:

    $collection = collect(['name' => 'taylor', 'languages' => ['php', 'javascript']]);

    $flattened = $collection->flatten();

    $flattened->all();

    // ['taylor', 'php', 'javascript'];

<a name="method-flip"></a>
#### `flip()` {#collection-method}

O método `flip` troca chaves da coleção por seus valores correspondentes:

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $flipped = $collection->flip();

    $flipped->all();

    // ['taylor' => 'name', 'laravel' => 'framework']

<a name="method-forget"></a>
#### `forget()` {#collection-method}

O método `forget` remove um item da coleção que tenha a chave passada:

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $collection->forget('name');

    $collection->all();

    // [framework' => 'laravel']

> **Note:** Diferentemente dos outros métodos da classe, `forget` não retorna uma nova coleção modificada; ela modifica a coleção e chama a si mesma.

<a name="method-forpage"></a>
#### `forPage()` {#collection-method}

O método `forPage` retorna uma nova coleção que contém os itens que estariam presentes em um determinado número de páginas da coleção:

    $collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9]);

    $chunk = $collection->forPage(2, 3);

    $chunk->all();

    // [4, 5, 6]

O método requer o número de páginas e o número de itens a serem exibidos por página, respectivamente.

<a name="method-get"></a>
#### `get()` {#collection-method}

O método `get` retorna o item em uma determinada chave. Se a chave não existir, é retornado `null`:

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $value = $collection->get('name');

    // taylor

Você pode, opcionalmente, passar um valor padrão como o segundo argumento:

    $collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

    $value = $collection->get('foo', 'default-value');

    // default-value

Você pode até passar um retorno de chamada como valor padrão. O resultado da chamada de retorno será devolvido se a chave especificada não existir:

    $collection->get('email', function () {
        return 'default-value';
    });

    // default-value

<a name="method-groupby"></a>
#### `groupBy()` {#collection-method}

O método `groupBy` agrupa itens da coleção pela chave passada:

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

Além de passar uma string `key`, você também pode passar uma chamada de retorno. O retorno de chamada deve retornar o valor que deseja introduzir no grupo:

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

O método `has` determina se existe uma determinada chave na coleção:

    $collection = collect(['account_id' => 1, 'product' => 'Desk']);

    $collection->has('email');

    // false

<a name="method-implode"></a>
#### `implode()` {#collection-method}

O método `implode` junta os itens da coleção. Os seus argumentos dependem do tipo de itens na coleção..

Se a coleção contém arrays ou objetos, você deve passar a chave dos atributos que você deseja unir, e o caractere que deseja que seja usado para unir os valores:

    $collection = collect([
        ['account_id' => 1, 'product' => 'Desk'],
        ['account_id' => 2, 'product' => 'Chair'],
    ]);

    $collection->implode('product', ', ');

    // Desk, Chair

Se a coleção contém cadeias simples ou valores numéricos, simplesmente passar o caractere que deseja que usado para unir os valores como o único argumento para o método:

    collect([1, 2, 3, 4, 5])->implode('-');

    // '1-2-3-4-5'

<a name="method-intersect"></a>
#### `intersect()` {#collection-method}

O método `intersect` remove quaisquer valores que não estão presentes `array` dado ou coleção:

    $collection = collect(['Desk', 'Sofa', 'Chair']);

    $intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

    $intersect->all();

    // [0 => 'Desk', 2 => 'Chair']

Como você pode ver, a coleção resultante irá preservar as chaves da coleção original.

<a name="method-isempty"></a>
#### `isEmpty()` {#collection-method}

O método `isEmpty` retorna `true` se a coleção estiver vazia; Caso não esteja vazia, retorna `false`:

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

Se vários itens têm a mesma chave, apenas o último será exibido na nova coleção.

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

O método `keys` retorna todas as chaves da coleção:

    $collection = collect([
        'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
        'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]);

    $keys = $collection->keys();

    $keys->all();

    // ['prod-100', 'prod-200']

<a name="method-last"></a>
#### `last()` {#collection-method}

O método `last` retorna o último elemento na coleção que for verdadeiro para a condição dada:

    collect([1, 2, 3, 4])->last(function ($key, $value) {
        return $value < 3;
    });

    // 2

Você também pode chamar o método `last` sem argumentos para obter o último elemento na coleção. Se a coleção está vazia, é retornado `null`:

    collect([1, 2, 3, 4])->last();

    // 4

<a name="method-map"></a>
#### `map()` {#collection-method}

O método `map` itera através de toda a coleção passando cada valor para a chamada de retorno dada. O retorno de chamada é livre para modificar o item e devolvê-lo, formando assim uma nova coleção de itens modificados:

    $collection = collect([1, 2, 3, 4, 5]);

    $multiplied = $collection->map(function ($item, $key) {
        return $item * 2;
    });

    $multiplied->all();

    // [2, 4, 6, 8, 10]

> **Note:** Como a maioria dos outros métodos da classe, `map` retorna uma nova instância da classe; Ele não modifica a coleção original. Se você quer transformar a coleção original, use o método [`transform`](#method-transform).

<a name="method-max"></a>
#### `max()` {#collection-method}

O método `max` retorna o valor máximo para uma determinada chave fornecida:

    $max = collect([['foo' => 10], ['foo' => 20]])->max('foo');

    // 20

    $max = collect([1, 2, 3, 4, 5])->max();

    // 5

<a name="method-merge"></a>
#### `merge()` {#collection-method}

O método `merge` mescla uma matriz dada com a coleção original. Qualquer chave da matriz dada que for igual a coleção original irá substituir o valor na coleção original:

    $collection = collect(['product_id' => 1, 'name' => 'Desk']);

    $merged = $collection->merge(['price' => 100, 'discount' => false]);

    $merged->all();

    // ['product_id' => 1, 'name' => 'Desk', 'price' => 100, 'discount' => false]

Se a chave da matriz dada for númerica, os valores serão acrescentados ao final da coleção:

    $collection = collect(['Desk', 'Chair']);

    $merged = $collection->merge(['Bookcase', 'Door']);

    $merged->all();

    // ['Desk', 'Chair', 'Bookcase', 'Door']

<a name="method-min"></a>
#### `min()` {#collection-method}

O método `main` retorna o valor mínimo de uma determinada chave:

    $min = collect([['foo' => 10], ['foo' => 20]])->min('foo');

    // 10

    $min = collect([1, 2, 3, 4, 5])->min();

    // 1

<a name="method-only"></a>
#### `only()` {#collection-method}

O método `only` retorna os itens da coleção que conincidem com a chave passada:

    $collection = collect(['product_id' => 1, 'name' => 'Desk', 'price' => 100, 'discount' => false]);

    $filtered = $collection->only(['product_id', 'name']);

    $filtered->all();

    // ['product_id' => 1, 'name' => 'Desk']

Para o inverso do método `only`, veja o método [except](#method-except).

<a name="method-pluck"></a>
#### `pluck()` {#collection-method}

O método `pluck` todos os valores de uma coleção que contenham a chave fornecida:

    $collection = collect([
        ['product_id' => 'prod-100', 'name' => 'Desk'],
        ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]);

    $plucked = $collection->pluck('name');

    $plucked->all();

    // ['Desk', 'Chair']

// You may also specify how you wish the resulting collection to be keyed:
Você também pode especificar como você deseja que a coleção seja chaveada:

    $plucked = $collection->pluck('name', 'product_id');

    $plucked->all();

    // ['prod-100' => 'Desk', 'prod-200' => 'Chair']

<a name="method-pop"></a>
#### `pop()` {#collection-method}

O método `pop` remove e retorna o último item da coleção:

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->pop();

    // 5

    $collection->all();

    // [1, 2, 3, 4]

<a name="method-prepend"></a>
#### `prepend()` {#collection-method}

O método `prepend` adiciona um item ao início da coleção:

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->prepend(0);

    $collection->all();

    // [0, 1, 2, 3, 4, 5]

Você também pode passar um segundo parâmetro para definir a chave que o item adicionado terá:

    $collection = collect(['one' => 1, 'two', => 2]);

    $collection->prepend(0, 'zero');

    $collection->all();

    // ['zero' => 0, 'one' => 1, 'two', => 2]

<a name="method-pull"></a>
#### `pull()` {#collection-method}

O método `pull` remove e retorna itens da coleção de acordo com a chave fornecida:

    $collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

    $collection->pull('name');

    // 'Desk'

    $collection->all();

    // ['product_id' => 'prod-100']

<a name="method-push"></a>
#### `push()` {#collection-method}

O método `push` adiciona um item ao final da coleção:

    $collection = collect([1, 2, 3, 4]);

    $collection->push(5);

    $collection->all();

    // [1, 2, 3, 4, 5]

<a name="method-put"></a>
#### `put()` {#collection-method}

O método `put` insere na coleção um valor e uma chave fornecida:

    $collection = collect(['product_id' => 1, 'name' => 'Desk']);

    $collection->put('price', 100);

    $collection->all();

    // ['product_id' => 1, 'name' => 'Desk', 'price' => 100]

<a name="method-random"></a>
#### `random()` {#collection-method}

O método `random` retorna um item aleatório da coleção:

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->random();

    // 4 - (retrieved randomly)

Você pode opcionalmente passar um inteiro para `random`. Se o inteiro for maior que `1`, um coleção com o valor passado será retornada:

    $random = $collection->random(3);

    $random->all();

    // [2, 4, 5] - (retrieved randomly)

<a name="method-reduce"></a>
#### `reduce()` {#collection-method}

O método `reduce` reduz a coleção para um único valor, passando o resultado de cada iteração para iteração seguinte:

    $collection = collect([1, 2, 3]);

    $total = $collection->reduce(function ($carry, $item) {
        return $carry + $item;
    });

    // 6

O valor para `$carry` na primeira iteração é `null`; entretanto, você pode especificar seu valor inicial, passando um segundo argumento para `reduce`:

    $collection->reduce(function ($carry, $item) {
        return $carry + $item;
    }, 4);

    // 10

<a name="method-reject"></a>
#### `reject()` {#collection-method}

O método `reject` filtra a coleção usando o callback dado. O callback deve retornar `true` para todos os itens que deseja remover da coleção resultante:

    $collection = collect([1, 2, 3, 4]);

    $filtered = $collection->reject(function ($item) {
        return $item > 2;
    });

    $filtered->all();

    // [1, 2]

Para o inverso do método `reject`, veja o método [`filter`](#method-filter).

<a name="method-reverse"></a>
#### `reverse()` {#collection-method}

O método `reverse` inverte a ordem dos itens da coleção:

    $collection = collect([1, 2, 3, 4, 5]);

    $reversed = $collection->reverse();

    $reversed->all();

    // [5, 4, 3, 2, 1]

<a name="method-search"></a>
#### `search()` {#collection-method}

O método `search` procura na coleção para o valor dado e retorna sua chave se for encontrado. Se o item não for encontrado, retorna `false`.

    $collection = collect([2, 4, 6, 8]);

    $collection->search(4);

    // 1

A pesquisa é feita usando uma comparação de "loose". Para usar a comparação "strict", passe `true` como segundo argumento:

    $collection->search('4', true);

    // false

Alternativamente, você pode passar em seu próprio callback para procurar o primeiro item que passe numa condição dada:

    $collection->search(function ($item, $key) {
        return $item > 5;
    });

    // 2

<a name="method-shift"></a>
#### `shift()` {#collection-method}

O método `shift` remove e retorna o primeiro item da coleção:

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->shift();

    // 1

    $collection->all();

    // [2, 3, 4, 5]

<a name="method-shuffle"></a>
#### `shuffle()` {#collection-method}

O método `shuffle` embaralha aleatoriamente os itens na coleção:

    $collection = collect([1, 2, 3, 4, 5]);

    $shuffled = $collection->shuffle();

    $shuffled->all();

    // [3, 2, 5, 1, 4] // (generated randomly)

<a name="method-slice"></a>
#### `slice()` {#collection-method}

O método `slice` retorna uma parte da coleção:

    $collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

    $slice = $collection->slice(4);

    $slice->all();

    // [5, 6, 7, 8, 9, 10]

Se você gostaria de limitar o tamanho da parte retornada, passe o tamanho desejado como segundo argumento para o método:

    $slice = $collection->slice(4, 2);

    $slice->all();

    // [5, 6]

A parte retornada terá chaves novas, numericamente indexadas. Se você deseja preservar as chaves originais, passe `true` como terceiro parâmetro.

<a name="method-sort"></a>
#### `sort()` {#collection-method}

O método `sort` ordena a coleção:

    $collection = collect([5, 3, 1, 2, 4]);

    $sorted = $collection->sort();

    $sorted->values()->all();

    // [1, 2, 3, 4, 5]

A coleção ordenada mantém as chaves da coleção original. Neste exemplo foi usado o método [`values`](#method-values) para repor as chaves de índices numeradas de forma ordenada.

Para classificar uma coleção de matrizes aninhadas ou objetos, veja os métodos [`sortBy`](#method-sortby) e [`sortByDesc`](#method-sortbydesc).

Se as suas necessidades de ordenação são mais avançadas, você talvez deseje passar um callback para o método `sort` com o seu algoritimo. Consulte a documentação do php sobre [`usort`](http://php.net/manual/en/function.usort.php#refsect1-function.usort-parameters), que é o que é feito por debaixo dos panos pelo método `sort`.

<a name="method-sortby"></a>
#### `sortBy()` {#collection-method}

O método `sortBy` ordena a coleção pela chave passada:

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

A coleção ordenada mantém as chaves de matriz original. Neste exemplo foi usado o método [`values`](#method-values)  para repor as chaves de índices numeradas de forma ordenada.

Você também pode passar o seu próprio callback para determinar como classificar a coleção retornada:

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

Este método tem a mesma assinatura que o método [`sortBy`](#method-sortby), mas irá classificar na ordem inversa.

<a name="method-splice"></a>
#### `splice()` {#collection-method}

O método `splice` remove e retorna um pedaço da coleção:

    $collection = collect([1, 2, 3, 4, 5]);

    $chunk = $collection->splice(2);

    $chunk->all();

    // [3, 4, 5]

    $collection->all();

    // [1, 2]

Você pode passar um segundo argumento para limitar o tamanho do pedaço da coleção retornada:

    $collection = collect([1, 2, 3, 4, 5]);

    $chunk = $collection->splice(2, 1);

    $chunk->all();

    // [3]

    $collection->all();

    // [1, 2, 4, 5]

Além disso, você pode passar um terceiro argumento que contém os novos itens que irão substituir os itens removidos da coleção:

    $collection = collect([1, 2, 3, 4, 5]);

    $chunk = $collection->splice(2, 1, [10, 11]);

    $chunk->all();

    // [3]

    $collection->all();

    // [1, 2, 10, 11, 4, 5]

<a name="method-sum"></a>
#### `sum()` {#collection-method}

O método `sum` retorna a soma de todos os itens da coleção:

    collect([1, 2, 3, 4, 5])->sum();

    // 15

Se a coleção contém arrays aninhados ou objetos, você deve passar uma chave para determinar quais os valores serão inclusos na soma:

    $collection = collect([
        ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
        ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
    ]);

    $collection->sum('pages');

    // 1272

Além disso, você pode passar o seu próprio callback para determinar quais valores da coleção serão somados:

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

O método `take` retorna uma nova coleção com o número específico de itens informado:

    $collection = collect([0, 1, 2, 3, 4, 5]);

    $chunk = $collection->take(3);

    $chunk->all();

    // [0, 1, 2]

Você também pode passar um número negativo para para que os itens retornados sejam contados a partir do final da coleção:

    $collection = collect([0, 1, 2, 3, 4, 5]);

    $chunk = $collection->take(-2);

    $chunk->all();

    // [4, 5]

<a name="method-toarray"></a>
#### `toArray()` {#collection-method}

O método `toArray` converte a coleção para um `array` PHP. Se a coleção for um model do [Eloquent](/docs/{{version}}/eloquent), o modelo também será convertido para array:

    $collection = collect(['name' => 'Desk', 'price' => 200]);

    $collection->toArray();

    /*
        [
            ['name' => 'Desk', 'price' => 200],
        ]
    */

> **Note:** `toArray` também converte todos os seus objetos aninhados para um array. Se você quiser obter os arrays aninhados, tal como são, use o método [`all`](#method-all).

<a name="method-tojson"></a>
#### `toJson()` {#collection-method}

O método `toJson` converte a coleção em um JSON:

    $collection = collect(['name' => 'Desk', 'price' => 200]);

    $collection->toJson();

    // '{"name":"Desk","price":200}'

<a name="method-transform"></a>
#### `transform()` {#collection-method}

O método `transform` itera sobre a coleção e chama o callback dado para cada item na coleção. Os itens na coleção serão substituídos pelos valores retornados no callback:

    $collection = collect([1, 2, 3, 4, 5]);

    $collection->transform(function ($item, $key) {
        return $item * 2;
    });

    $collection->all();

    // [2, 4, 6, 8, 10]

> **Note:** Diferentemente da maioria dos outros métodos, `transform` modifica a coleção original. Se você deseja criar uma nova coleção, use o método [`map`](#method-map).

<a name="method-unique"></a>
#### `unique()` {#collection-method}

O método `unique` retorna todos os itens únicos da coleção:

    $collection = collect([1, 1, 2, 2, 3, 4, 2]);

    $unique = $collection->unique();

    $unique->values()->all();

    // [1, 2, 3, 4]

A coleção retornada mantém as chaves de matriz original. Neste exemplo foi o usado o método [`values`](#method-values) para repor as chaves de índices ordenadas numericamente.

Ao lidar com arrays aninhados ou objetos, você pode especificar a chave usada para determinar exclusividade:

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

Você também pode passar o seu próprio callback:

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

O método `values` retorna uma nova coleção com as chaves ordenadas numericamente:

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

O método `where` filtra a coleção por um valor passado:

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

O método `where` método usa comparação 'strict' ao verificar os valores dos itens. Use o método [`whereLoose`](#where-loose) para filtrar usando comparação do tipo "loose".

<a name="method-whereloose"></a>
#### `whereLoose()` {#collection-method}

Este método tem a mesma assinatura do método [`where`](#method-where); Entretanto, todos os valores são comparados usando comparação do tipo "loose".

<a name="method-zip"></a>
#### `zip()` {#collection-method}

O método `zip` une os valores do array dado com os valores da coleção no índice correspondente:

    $collection = collect(['Chair', 'Desk']);

    $zipped = $collection->zip([100, 200]);

    $zipped->all();

    // [['Chair', 100], ['Desk', 200]]
