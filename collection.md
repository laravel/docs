# Collection

- [Introduzione](#introduzione)
- [Creare una Collection](#creare-collection)
- [Metodi Disponibili](#metodi-disponibili)

<a name="introduzione"></a>
## Introduzione

La classe `Illuminate\Support\Collection` è un ottimo wrapper, pieno zeppo di funzionalità, per lavorare con array di dati ed oggetti. Ad esempio, guarda il codice di seguito. L'helper _collect_ viene chiamato per creare una nuova istanza di Collection partendo da un semplice array. Dopodiché, viene richiamato _strtoupper_ su ogni elemento, per poi eliminare tutti quelli vuoti.

Abbastanza semplice, vero?


	$collection = collect(['taylor', 'abigail', null])->map(function ($name) {
		return strtoupper($name);
	})
	->reject(function ($name) {
		return empty($name);
	});

Usando un'istanza della classe `Collection`, come vedi, ti permette di concatenare più metodi per permetterti di lavorare con una sintassi fluida ed espressiva. Più in generale, ogni metodo della classe _Collection_ ritorna fondamentalmente una _Collection_.

<a name="creare-collection"></a>
## Creare una Collection

Come visto poco fa, creare una collection è molto semplice: _collect_ ritorna un oggetto di tipo `Illuminate\Support\Collection` partendo da un semplice array. Così:

	$collection = collect([1, 2, 3]);

Di default, quando lavori con [Eloquent](/documentazione/5.1/eloquent) ogni risultato è una _Collection_. Ad ogni modo, sentiti libero di usare una collection ogni volta che la tua applicazione lo richiede.

<a name="metodi-disponibili"></a>
## Metodi Disponibili

Vediamo, adesso, tutti i metodi attualmente disponibili ed utilizzabili di una qualsiasi _Collection_. Ricorda, ognuno di questi metodi ritorna a sua volta una _Collection_, quindi sentiti libero di concatenarli per manipolare i tuoi array in modo veloce e conveniente.

Scegli un metodo per scoprire cosa fa:

* [all](#metodo-all)
* [chunk](#metodo-chunk)
* [collapse](#metodo-collapse)
* [contains](#metodo-contains)
* [count](#metodo-count)
* [diff](#metodo-diff)
* [each](#metodo-each)
* [filter](#metodo-filter)
* [first](#metodo-first)
* [flatten](#metodo-flatten)
* [flip](#metodo-flip)
* [forget](#metodo-forget)
* [forPage](#metodo-forpage)
* [get](#metodo-get)
* [groupBy](#metodo-groupby)
* [has](#metodo-has)
* [implode](#metodo-implode)
* [intersect](#metodo-intersect)
* [isEmpty](#metodo-isempty)
* [keyBy](#metodo-keyby)
* [keys](#metodo-keys)
* [last](#metodo-last)
* [map](#metodo-map)
* [merge](#metodo-merge)
* [pluck](#metodo-pluck)
* [pop](#metodo-pop)
* [prepend](#metodo-prepend)
* [pull](#metodo-pull)
* [push](#metodo-push)
* [put](#metodo-put)
* [random](#metodo-random)
* [reduce](#metodo-reduce)
* [reject](#metodo-reject)
* [reverse](#metodo-reverse)
* [search](#metodo-search)
* [shift](#metodo-shift)
* [shuffle](#metodo-shuffle)
* [slice](#metodo-slice)
* [sort](#metodo-sort)
* [sortBy](#metodo-sortby)
* [sortByDesc](#metodo-sortbydesc)
* [splice](#metodo-splice)
* [sum](#metodo-sum)
* [take](#metodo-take)
* [toArray](#metodo-toarray)
* [toJson](#metodo-tojson)
* [transform](#metodo-transform)
* [unique](#metodo-unique)
* [values](#metodo-values)
* [where](#metodo-where)
* [whereLoose](#metodo-whereloose)
* [zip](#metodo-zip)

<a name="metodo-all"></a>
#### `all()`

Il metodo _all_, semplicemente, ritorna tutti gli elementi presenti nella collection come array.

	collect([1, 2, 3])->all();

	// [1, 2, 3]

<a name="metodo-chunk"></a>
#### `chunk()`

Il metodo _chunk_ permette di "spezzare" una collection in altre collection più piccole, di una certa dimensione.

	$collection = collect([1, 2, 3, 4, 5, 6, 7]);

	$chunks = $collection->chunk(4);

	$chunks->toArray();

	// [[1, 2, 3, 4], [5, 6, 7]]

Questo metodo può risultare particolarmente utile nelle [view](/documentazione/5.1/view), lavorando con [Bootstrap](http://getbootstrap.com/css/#grid). Immagina di avere una collection di model da mostrare in una grid.

	@foreach ($products->chunk(3) as $chunk)
		<div class="row">
			@foreach ($chunk as $product)
				<div class="col-xs-4">{{ $product->name }}</div>
			@endforeach
		</div>
	@endforeach

Comodo, vero?

<a name="metodo-collapse"></a>
#### `collapse()`

Il metodo _collapse_ prende una serie di array, convertendola in una singola collection.

	$collection = collect([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

	$collapsed = $collection->collapse();

	$collapsed->all();

	// [1, 2, 3, 4, 5, 6, 7, 8, 9]

<a name="metodo-contains"></a>
#### `contains()`

Il metodo _contains_ determina se una collection contiene o meno un certo valore.

	$collection = collect(['name' => 'Desk', 'price' => 100]);

	$collection->contains('Desk');

	// true

	$collection->contains('New York');

	// false

Volendo, puoi anche passare come parametri una coppia chiave/valore, per un controllo più accurato.

	$collection = collect([
		['product' => 'Desk', 'price' => 200],
		['product' => 'Chair', 'price' => 100],
	]);

	$collection->contains('product', 'Bookcase');

	// false

Per una maggiore personalizzazione, inoltre, puoi passare come parametro una _callback_ da usare come meglio credi.

	$collection = collect([1, 2, 3, 4, 5]);

	$collection->contains(function ($key, $value) {
		return $value > 5;
	});

	// false

<a name="metodo-count"></a>
#### `count()`

Il metodo _count_ ritorna il conteggio del numero di elementi presenti nella collection.

	$collection = collect([1, 2, 3, 4]);

	$collection->count();

	// 4

<a name="metodo-diff"></a>
#### `diff()`

Il metodo _diff_ confronta la collection con un'altra, oppure con un semplice array PHP.

	$collection = collect([1, 2, 3, 4, 5]);

	$diff = $collection->diff([2, 4, 6, 8]);

	$diff->all();

	// [1, 3, 5]

<a name="metodo-each"></a>
#### `each()`

Il metodo _each_ itera gli elementi nella collection, ed ognuno di questi elementi viene passato ad una callback.

	$collection = $collection->each(function ($item, $key) {
		//
	});

Per "rompere" il loop prima della fine, fai in modo che la callback ritorni _false_.

	$collection = $collection->each(function ($item, $key) {
		if (/* some condition */) {
			return false;
		}
	});

<a name="metodo-filter"></a>
#### `filter()`

Il metodo _filter_ filtra la collection partendo da una certa callback, mantenendo "dentro" solo gli elementi che passano un test specificato dallo sviluppatore:

	$collection = collect([1, 2, 3, 4]);

	$filtered = $collection->filter(function ($item) {
		return $item > 2;
	});

	$filtered->all();

	// [3, 4]

Se hai bisogno dell'esatto contrario di _filter_, guarda _[reject](#metodo-reject)_.

<a name="metodo-first"></a>
#### `first()`

Il metodo _first_ ritorna il primo elemento in una collection che passa un test definito dallo sviluppatore.

	collect([1, 2, 3, 4])->first(function ($key, $value) {
		return $value > 2;
	});

	// 3

Puoi anche chiamare _first_ senza parametri per fare in modo che ritorni, semplicemente, il primo elemento.

	collect([1, 2, 3, 4])->first();

	// 1

<a name="metodo-flatten"></a>
#### `flatten()`

Il metodo _flatten_ prende un array multi-dimensionale e lo "appiattisce" in un array semplice.

	$collection = collect(['name' => 'taylor', 'languages' => ['php', 'javascript']]);

	$flattened = $collection->flatten();

	$flattened->all();

	// ['taylor', 'php', 'javascript'];

<a name="metodo-flip"></a>
#### `flip()`

Il metodo _flip_ scambia le chiavi di una collection con il loro valore.

	$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

	$flipped = $collection->flip();

	$flipped->all();

	// ['taylor' => 'name', 'laravel' => 'framework']

<a name="metodo-forget"></a>
#### `forget()`

Il metodo _forget_ rimuove un elemento da una collection partendo dalla sua chiave.

	$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

	$collection->forget('name');

	$collection->all();

	// [framework' => 'laravel']

> **Note:** a differenza di molti metodi che vedi in questa pagina, _forget_ non ritorna un'altra collection, ma lavora su quella su cui è chiamato.

<a name="metodo-forpage"></a>
#### `forPage()`

Il metodo _forPage_ ritorna una nuova collection contenente tutti gli elementi che sarebbero presenti su una singola "pagina". I parametri da passare sono due: la pagina in cui ci si trova ed il numero di elementi per pagina.

	$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9])->forPage(2, 3);

	$collection->all();

	// [4, 5, 6]

<a name="metodo-get"></a>
#### `get()`

Il metodo _get_ ritorna un elemento specifico partendo dalla chiave. Se la chiave non esiste viene ritornato _null_.


	$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

	$value = $collection->get('name');

	// taylor

Puoi passare un valore di default opzionale da far ritornare, qualora l'elemento non esistesse.

	$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

	$value = $collection->get('foo', 'default-value');

	// default-value

Puoi inoltre passare anche una callback come valore di default, calcolando di volta in volta tale valore.

	$collection->get('email', function () {
		return 'default-value';
	});

	// default-value

<a name="metodo-groupby"></a>
#### `groupBy()`

Il metodo _groupBy_ raggruppa gli elementi di una collection partendo da una chiave specifica.

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

Al posto di una stringa puoi specificare anche una callback, che ritorni l'elemento da usare come riferimento.

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

<a name="metodo-has"></a>
#### `has()`

Il metodo _has_ determina se una data chiave esiste in una collection.

	$collection = collect(['account_id' => 1, 'product' => 'Desk']);

	$collection->has('email');

	// false

<a name="metodo-implode"></a>
#### `implode()`

Il metodo _implode_ unisce tutti gli elementi di una collection. I parametri da passare dipendono anche dalla tipologia di elementi nella collection stessa.

Se la collection contiene array oppure oggetti, allora dovresti passare come parametro la chiave dell'attributo da unire, ad una stringa "collante" da mettere tra un elemento e l'altro.

	$collection = collect([
		['account_id' => 1, 'product' => 'Desk'],
		['account_id' => 2, 'product' => 'Chair'],
	]);

	$collection->implode('product', ', ');

	// Desk, Chair

Se la collection contiene valori semplici, come stringhe oppure numeri, basta la stringa "collante".

	collect([1, 2, 3, 4, 5])->implode('-');

	// '1-2-3-4-5'

<a name="metodo-intersect"></a>
#### `intersect()`

Il metodo _intersect_ rimuove tutti i valori che non sono presenti partendo dalla collection su cui è richiamato il metodo ed un'altra passata come parametro. Tale controllo si può fare anche passando un semplice array.

	$collection = collect(['Desk', 'Sofa', 'Chair']);

	$intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

	$intersect->all();

	// [0 => 'Desk', 2 => 'Chair']

La collection risultante, come vedi, preserverà comunque le chiavi per i singoli elementi.

<a name="metodo-isempty"></a>
#### `isEmpty()`

Il metodo _isEmpty_ ritorna _true_ se la collection è vuota. In caso contrario, _false_.

	collect([])->isEmpty();

	// true

<a name="metodo-keyby"></a>
#### `keyBy()`

Esegue un raggruppamento prendendo come parametro un attributo da rendere, poi, chiave.

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

Se ci sono più elementi con la stessa chiave, verrà preso in considerazione solo l'ultimo.

Puoi anche passare un callback come parametro, che ritorni il valore da usare come chiave.

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

<a name="metodo-keys"></a>
#### `keys()`

Il metodo _keys_ ritorna tutte le chiavi della collection.

	$collection = collect([
		'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
		'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
	]);

	$keys = $collection->keys();

	$keys->all();

	// ['prod-100', 'prod-200']

<a name="metodo-last"></a>
#### `last()`

Il metodo _last_ ritorna l'ultimo elemento in una collection che soddisfa determinate condizioni:

	collect([1, 2, 3, 4])->last(function ($key, $value) {
		return $value < 3;
	});

	// 2

In questo caso, viene ritornato l'ultimo elemento il cui valore è minore di tre. Se il metodo viene chiamato senza parametri, invece, ad essere ritornato è l'ultimo elemento in assoluto della collection.

	collect([1, 2, 3, 4])->last();

	// 4

<a name="metodo-map"></a>
#### `map()`

Il metodo _map_ itera attraverso la collection e passa ogni singolo valore ad un certa callback. Tramite questa, l'elemento può essere modificato, cancellato ed eventualmente ritornato per creare una nuova collection a parte.

	$collection = collect([1, 2, 3, 4, 5]);

	$multiplied = $collection->map(function ($item, $key) {
		return $item * 2;
	});

	$multiplied->all();

	// [2, 4, 6, 8, 10]

> **Nota:** come molti metodi di collection, _map_ ritornat una nuova istanza. Non trasforma la collection "attuale". Se il tuo obiettivo è lavorare sull'originale, considera l'uso di [`transform`](#metodo-transform).

<a name="metodo-merge"></a>
#### `merge()`

Il metodo _merge_ "fonde" un certo array in una collection. Ogni chiave nell'array già presente nella collection sovrascriverà quella già esistente.

	$collection = collect(['product_id' => 1, 'name' => 'Desk']);

	$merged = $collection->merge(['price' => 100, 'discount' => false]);

	$merged->all();

	// ['product_id' => 1, 'name' => 'Desk', 'price' => 100, 'discount' => false]

Nel caso in cui le chiavi siano semplici numeriche, gli elementi verranno aggiunti alla fine della collection data.

	$collection = collect(['Desk', 'Chair']);

	$merged = $collection->merge(['Bookcase', 'Door']);

	$merged->all();

	// ['Desk', 'Chair', 'Bookcase', 'Door']

<a name="metodo-pluck"></a>
#### `pluck()`

Il metodo _pluck_ recupera tutti i valori di una collection per una certa chiave.

	$collection = collect([
		['product_id' => 'prod-100', 'name' => 'Desk'],
		['product_id' => 'prod-200', 'name' => 'Chair'],
	]);

	$plucked = $collection->pluck('name');

	$plucked->all();

	// ['Desk', 'Chair']

Puoi anche specificare, eventualmente, una chiave da usare per la collection risultante.

	$plucked = $collection->pluck('name', 'product_id');

	$plucked->all();

	// ['prod-100' => 'Desk', 'prod-200' => 'Chair']

<a name="metodo-pop"></a>
#### `pop()`

Il metodo _pop_ rimuove e ritorna l'ultimo elemento di una collection.

	$collection = collect([1, 2, 3, 4, 5]);

	$collection->pop();

	// 5

	$collection->all();

	// [1, 2, 3, 4]

<a name="metodo-prepend"></a>
#### `prepend()`

Il metodo `prepend` aggiunge un elemento all'inizio di una collection.

	$collection = collect([1, 2, 3, 4, 5]);

	$collection->prepend(0);

	$collection->all();

	// [0, 1, 2, 3, 4, 5]

<a name="metodo-pull"></a>
#### `pull()`

Il metodo _pull_ rimuove e ritorna un certo elemento da una collection partendo dalla sua chiave.

	$collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

	$collection->pull('name');

	// 'Desk'

	$collection->all();

	// ['product_id' => 'prod-100']

<a name="metodo-push"></a>
#### `push()`

Il metodo _push_ aggiunge un elemento alla fine della collection.

	$collection = collect([1, 2, 3, 4]);

	$collection->push(5);

	$collection->all();

	// [1, 2, 3, 4, 5]

<a name="metodo-put"></a>
#### `put()`

Il metodo _put_ imposta un dato valore per una data chiave nella collection.

	$collection = collect(['product_id' => 1, 'name' => 'Desk']);

	$collection->put('price', 100);

	$collection->all();

	// ['product_id' => 1, 'name' => 'Desk', 'price' => 100]

<a name="metodo-random"></a>
#### `random()`

Il metodo _random_ ritorna un elemento casuale dalla collection.

	$collection = collect([1, 2, 3, 4, 5]);

	$collection->random();

	// 4 - (retrieved randomly)

Puoi anche passare, opzionalmente, un intero N come parametro. In tal caso, verranno ritornati N elementi casuali al posto di un singolo.

	$random = $collection->random(3);

	$random->all();

	// [2, 4, 5] - (retrieved randomly)

<a name="metodo-reduce"></a>
#### `reduce()`

Il metodo _reduce_ riduce la collection ad un singolo valore, passando il risultato di ogni iterazione a quella successiva.

	$collection = collect([1, 2, 3]);

	$total = $collection->reduce(function ($carry, $item) {
		return $carry + $item;
	});

	// 6

Il valore di _$carry_ alla prima iterazione è _null_. Tuttavia, puoi specificare un valore iniziale passandolo come secondo parametro opzionale:

	$collection->reduce(function ($carry, $item) {
		return $carry + $item;
	}, 4);

	// 10

<a name="metodo-reject"></a>
#### `reject()`

Il metodo _reject_ filtra la collezione usando una specifica callback. Tale callback deve ritornare _true_ per ogni elemento che deve essere rimosso dalla collezione stessa.

	$collection = collect([1, 2, 3, 4]);

	$filtered = $collection->reject(function ($item) {
		return $item > 2;
	});

	$filtered->all();

	// [1, 2]

Per l'inverso di _reject_, cerca il metodo [`filter`](#metodo-filter).

<a name="metodo-reverse"></a>
#### `reverse()`

Il metodo _reverse_ inverte la data collection.

	$collection = collect([1, 2, 3, 4, 5]);

	$reversed = $collection->reverse();

	$reversed->all();

	// [5, 4, 3, 2, 1]

<a name="metodo-search"></a>
#### `search()`

Il metodo _search_ cerca un determinato (e dato) valore nella collection e ne ritorna la chiave, se tale elemento esiste. In caso contrario, invece, viene ritornato _false_.

	$collection = collect([2, 4, 6, 8]);

	$collection->search(4);

	// 1

La ricerca viene effettuata tramite loose comparison. Per avere più "rigore", imposta il secondo argomento opzionale su _true_.

	$collection->search('4', true);

	// false

Se preferisci, puoi sempre specificare una tua callback:

	$collection->search(function ($item, $key) {
		return $item > 5;
	});

	// 2

<a name="metodo-shift"></a>
#### `shift()`

Il metodo _shift_ rimuove e ritorna il primo elemento di una collection:

	$collection = collect([1, 2, 3, 4, 5]);

	$collection->shift();

	// 1

	$collection->all();

	// [2, 3, 4, 5]

<a name="metodo-shuffle"></a>
#### `shuffle()`

Il metodo _shuffle_ mescola a caso gli elementi della collection.

	$collection = collect([1, 2, 3, 4, 5]);

	$shuffled = $collection->shuffle();

	$shuffled->all();

	// [3, 2, 5, 1, 4] // (generated randomly)

<a name="metodo-slice"></a>
#### `slice()`

Il metodo _slice_ ritorna una porzione di una certa collection, a partire da un dato indice.

	$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

	$slice = $collection->slice(4);

	$slice->all();

	// [5, 6, 7, 8, 9, 10]

Se vuoi limitare le dimensioni della parte ritornata, specifica un secondo parametro (opzionale):

	$slice = $collection->slice(4, 2);

	$slice->all();

	// [5, 6]

La "porzione" ritornata avrà delle nuove chiavi. Se preferisci tenere quelle originali, specifica _true_ come terzo parametro.

<a name="metodo-sort"></a>
#### `sort()`

Il metodo _sort_ ordina la collection.

	$collection = collect([5, 3, 1, 2, 4]);

	$sorted = $collection->sort();

	$sorted->values()->all();

	// [1, 2, 3, 4, 5]

La collezione ordinata mantiene l'array di chiavi originali. Per vederne i valori abbiamo usato il metodo [`values`](#metodo-values).

Se hai bisogno di ordinare un array nidificato o degli oggetti, dai uno sguardo a [`sortBy`](#metodo-sortby) e [`sortByDesc`](#metodo-sortbydesc).

Se preferisci, puoi anche specificare una callback particolare per ordinare i tuoi elementi con il tuo algoritmo. A tal proposito, dai uno sguardo alla documentazione PHP relativa alla funzione [`usort`](http://php.net/manual/en/function.usort.php#refsect1-function.usort-parameters) per capire come organizzare la callback.

<a name="metodo-sortby"></a>
#### `sortBy()`

Il metodo _sortBy_ ordina la collection a partire da una certa chiave.

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

La collection ordinata mantiene l'array originale delle chiavi. Puoi anch specificare la tua callback personalizzata.

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

<a name="metodo-sortbydesc"></a>
#### `sortByDesc()`

Questo metodo ha la stessa segnatura di [`sortBy`](#metodo-sortby) visto poco fa. Con la sola eccezione di ordinare la collection in modo inverso.

<a name="metodo-splice"></a>
#### `splice()`

Il metodo _splice_ rimuove e ritorna una parte di collection partendo da un indice specifico.

	$collection = collect([1, 2, 3, 4, 5]);

	$chunk = $collection->splice(2);

	$chunk->all();

	// [3, 4, 5]

	$collection->all();

	// [1, 2]

Se vuoi limitare la dimensione della porzione rimossa, specifica un secondo parametro.

	$collection = collect([1, 2, 3, 4, 5]);

	$chunk = $collection->splice(2, 1);

	$chunk->all();

	// [3]

	$collection->all();

	// [1, 2, 4, 5]

In aggiunta, puoi anche definire un terzo argomento contenente i nuovi elementi che andranno a rimpiazzare quelli rimossi.

	$collection = collect([1, 2, 3, 4, 5]);

	$chunk = $collection->splice(2, 1, [10, 11]);

	$chunk->all();

	// [3]

	$collection->all();

	// [1, 2, 10, 11, 4, 5]

<a name="metodo-sum"></a>
#### `sum()`

Il metodo _sum_ ritorna la somma di tutti gli elementi nella collection.

	collect([1, 2, 3, 4, 5])->sum();

	// 15

Se la collection ha oggetti più complessi, come array nidificati o oggetti, puoi specificare la chiave da usare...

	$collection = collect([
		['name' => 'JavaScript: The Good Parts', 'pages' => 176],
		['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
	]);

	$collection->sum('pages');

	// 1272

... oppure puoi sempre specificare una callback di riferimento. Il valore da ritornare è quello da "contare".

	$collection = collect([
		['name' => 'Chair', 'colors' => ['Black']],
		['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
		['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
	]);

	$collection->sum(function ($product) {
		return count($product['colors']);
	});

	// 6

<a name="metodo-take"></a>
#### `take()`

Il metodo _take_ ritorna una nuova collection con un certo numero, specificato, di elementi.

	$collection = collect([0, 1, 2, 3, 4, 5]);

	$chunk = $collection->take(3);

	$chunk->all();

	// [0, 1, 2]

Puoi anche passare come parametro un numero negativo: in tal caso il conto verrà fatto "all'inverso" partendo dalla fine della collection.

	$collection = collect([0, 1, 2, 3, 4, 5]);

	$chunk = $collection->take(-2);

	$chunk->all();

	// [4, 5]

<a name="metodo-toarray"></a>
#### `toArray()`

Il metodo _toArray_ converte una collection in un semplice array PHP. Se la collection data è di model [Eloquent](/documentazione/5.1/eloquent), anche questi verranno automaticamente convertiti.

	$collection = collect(['name' => 'Desk', 'price' => 200]);

	$collection->toArray();

	/*
		[
			['name' => 'Desk', 'price' => 200],
		]
	*/

> **Nota:** `toArray` converte tutti gli oggetti nidificati in array. Se vuoi accedere all'array sottostante così com'è, allora usa [`all`](#metodo-all).

<a name="metodo-tojson"></a>
#### `toJson()`

Il metodo _toJson_ converte una collection in JSON.

	$collection = collect(['name' => 'Desk', 'price' => 200]);

	$collection->toJson();

	// '{"name":"Desk","price":200}'

<a name="metodo-transform"></a>
#### `transform()`

Il metodo _transform_ itera all'interno di una collection e chiama la data callback per ogni elemento al suo interno. Gli elementi presenti veranno "rimpiazzati" da quelli ritornati dalla callback.

	$collection = collect([1, 2, 3, 4, 5]);

	$collection->transform(function ($item, $key) {
		return $item * 2;
	});

	$collection->all();

	// [2, 4, 6, 8, 10]

> **Nota:** a differenza di molti di questi metodi, _transform_ agisce sull'oggetto originale. Se vuoi ottenere una copia della collection "lavorata", usa [`map`](#metodo-map).

<a name="metodo-unique"></a>
#### `unique()`

Il metodo _unique_ ritorna tutti i valori unici della collection.

	$collection = collect([1, 1, 2, 2, 3, 4, 2]);

	$unique = $collection->unique();

	$unique->values()->all();

	// [1, 2, 3, 4]

Se lavori con oggetti più complessi come array nidificati ed oggetti, potresti voler specificare la chiave da usare.

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

Puoi anche specificare, come al solito, una callback dedicata.

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

<a name="metodo-values"></a>
#### `values()`

Il metodo _values_ ritorna una nuova collection con le chiavi "resettate" in interi consecutivi.

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

<a name="metodo-where"></a>
#### `where()`

Il metodo _where_ filtra la collezione basandosi su una coppia _chiave/valore_.

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

Il metodo _where_ fa uso di una comparazione rigorosa. Usa [`whereLoose`](#metodo-whereloose) per una maggiore flessibilità.

<a name="metodo-whereloose"></a>
#### `whereLoose()`

Questo metodo ha la stessa segnatura di [`where`](#metodo-where). La differenza sta nel tipo di comparazione: qui è meno rigida e più flessibile.

<a name="metodo-zip"></a>
#### `zip()`

Il metodo _zip_ fonde insieme due collection, prendendo come punto di riferimento l'indice di ogni elemento.

	$collection = collect(['Chair', 'Desk']);

	$zipped = $collection->zip([100, 200]);

	$zipped->all();

	// [['Chair', 100], ['Desk', 200]]

In questo esempio, _Chair_ ha lo stesso indice di _100_, quindi andranno a formare un unico elemento... e così via.
