# Funzioni Helper

- [Introduzione](#introduzione)
- [Metodi Disponibili](#metodi-disponibili)

<a name="introduzione"></a>
## Introduzione

Laravel include una serie di funzioni di "helper" PHP. Molte di queste funzioni sono usate dal framework stesso; tuttavia, sei libero di usarle nella tua applicazione se le trovi convenienti.

<a name="metodi-disponibili"></a>
## Metodi Disponibili

<style>
	.collection-metodo-list > p {
		column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
		column-gap: 2em; -moz-column-gap: 2em; -webkit-column-gap: 2em;
	}

	.collection-metodo-list a {
		display: block;
	}
</style>

### Array

<div class="collection-metodo-list" markdown="1">
[array_add](#metodo-array-add)
[array_divide](#metodo-array-divide)
[array_dot](#metodo-array-dot)
[array_except](#metodo-array-except)
[array_first](#metodo-array-first)
[array_flatten](#metodo-array-flatten)
[array_forget](#metodo-array-forget)
[array_get](#metodo-array-get)
[array_only](#metodo-array-only)
[array_pluck](#metodo-array-pluck)
[array_pull](#metodo-array-pull)
[array_set](#metodo-array-set)
[array_sort](#metodo-array-sort)
[array_where](#metodo-array-where)
[head](#metodo-head)
[last](#metodo-last)
</div>

### Percorsi

<div class="collection-metodo-list" markdown="1">
[app_path](#metodo-app-path)
[base_path](#metodo-base-path)
[config_path](#metodo-config-path)
[database_path](#metodo-database-path)
[public_path](#metodo-public-path)
[storage_path](#metodo-storage-path)
</div>

### Stringhe

<div class="collection-metodo-list" markdown="1">
[camel_case](#metodo-camel-case)
[class_basename](#metodo-class-basename)
[e](#metodo-e)
[ends_with](#metodo-ends-with)
[snake_case](#metodo-snake-case)
[str_limit](#metodo-str-limit)
[starts_with](#metodo-starts-with)
[str_contains](#metodo-str-contains)
[str_finish](#metodo-str-finish)
[str_is](#metodo-str-is)
[str_plural](#metodo-str-plural)
[str_random](#metodo-str-random)
[str_singular](#metodo-str-singular)
[str_slug](#metodo-str-slug)
[studly_case](#metodo-studly-case)
[trans](#metodo-trans)
[trans_choice](#metodo-trans-choice)
</div>

### URL

<div class="collection-metodo-list" markdown="1">
[action](#metodo-action)
[route](#metodo-route)
[url](#metodo-url)
</div>

### Varie

<div class="collection-metodo-list" markdown="1">
[csrf_token](#metodo-csrf-token)
[dd](#metodo-dd)
[elixir](#metodo-elixir)
[env](#metodo-env)
[event](#metodo-event)
[response](#metodo-response)
[value](#metodo-value)
[view](#metodo-view)
[with](#metodo-with)
</div>

<a name="lista-metodi"></a>
## Lista Metodi

<style>
	#collection-metodo code {
		font-size: 14px;
	}

	#collection-metodo:not(.first-collection-metodo) {
		margin-top: 50px;
	}
</style>

<a name="metodo-array-add"></a>
#### `array_add()` {#collection-metodo .first-collection-metodo}

La funzione `array_add` aggiunge una coppia chiave / valore all'array se la chiave data non esiste già nell'array:

	$array = array_add(['name' => 'Desk'], 'price', 100);

	// ['name' => 'Desk', 'price' => 100]

<a name="metodo-array-divide"></a>
#### `array_divide()` {#collection-metodo}

La funzione `array_divide` ritorna due array, uno contenente le chiavi, e l'altro contentente i valori dell'array originale:

	list($keys, $values) = array_divide(['name' => 'Desk']);

	// $keys: ['name']

	// $values: ['Desk']

<a name="metodo-array-dot"></a>
#### `array_dot()` {#collection-metodo}

La funzione `array_dot` semplifica un array multi dimensionale restituendone uno singolo con la notazione "dot" per indicarne il livello di profondità:

	$array = array_dot(['foo' => ['bar' => 'baz']]);

	// ['foo.bar' => 'baz'];

<a name="metodo-array-except"></a>
#### `array_except()` {#collection-metodo}

Il metodo `array_except` rimuove una coppia chiave / valore dall'array:

	$array = ['name' => 'Desk', 'price' => 100];

	$array = array_except($array, ['price']);

	// ['name' => 'Desk']
<a name="metodo-array-first"></a>
#### `array_first()` {#collection-metodo}

Il metodo `array_first` ritorna il primo elemento di un array se quest'ultimo passa un test:

	$array = [100, 200, 300];

	$value = array_first($array, function ($key, $value) {
		return $value >= 150;
	});

	// 200

Al metodo può anche essere passato come terzo parametro un valore di default. Questo valore sarà ritornato se nessun valore passa il test:

	$value = array_first($array, $callback, $default);

<a name="metodo-array-flatten"></a>
#### `array_flatten()` {#collection-metodo}

Il metodo `array_flatten` ridurrà un array multi dimensionale ad un singolo livello.

	$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

	$array = array_flatten($array);

	// ['Joe', 'PHP', 'Ruby'];

<a name="metodo-array-forget"></a>
#### `array_forget()` {#collection-metodo}

Il metodo`array_forget` rimuove una coppia chiave / valore da un array complesso utilizzando la notazione "dot":

	$array = ['products' => ['desk' => ['price' => 100]]];

	array_forget($array, 'products.desk');

	// ['products' => []]

<a name="metodo-array-get"></a>
#### `array_get()` {#collection-metodo}

Il metodo `array_get` recupererà una valore da un array complesso utilizzando la notazione "dot":

	$array = ['products' => ['desk' => ['price' => 100]]];

	$value = array_get($array, 'products.desk');

	// ['price' => 100]

La funzione `array_get` accetta anche un valore di default, che sarà ritornato se la chiave specificata non viene trovata:

	$value = array_get($array, 'names.john', 'default');

<a name="metodo-array-only"></a>
#### `array_only()` {#collection-metodo}

Il metodo `array_only`recupererà solo le specifiche coppie chiave/valore dall'array:

	$array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

	$array = array_only($array, ['name', 'price']);

	// ['name' => 'Desk', 'price' => 100]

<a name="metodo-array-pluck"></a>
#### `array_pluck()` {#collection-metodo}

Il metodo`array_pluck` recupererà una lista delle specificate coppie chiave/valore dell’array:

	$array = [
		['developer' => ['name' => 'Taylor']],
		['developer' => ['name' => 'Abigail']]
	];

	$array = array_pluck($array, 'developer.name');

	// ['Taylor', 'Abigail'];

<a name="metodo-array-pull"></a>
#### `array_pull()` {#collection-metodo}

Il metodo `array_pull` restituirà una specifica coppia chiave/valore dell’array, quindi la rimuoverà:

	$array = ['name' => 'Desk', 'price' => 100];

	$name = array_pull($array, 'name');

	// $name: Desk

	// $array: ['price' => 100]

<a name="metodo-array-set"></a>
#### `array_set()` {#collection-metodo}

Il metodo `array_set` imposterà un valore dentro un array annidato utilizzando la notazione “dot”:

	$array = ['products' => ['desk' => ['price' => 100]]];

	array_set($array, 'products.desk.price', 200);

	// ['products' => ['desk' => ['price' => 200]]]

<a name="metodo-array-sort"></a>
#### `array_sort()` {#collection-metodo}

Il metodo `array_sort` ordina l'array in base al risultato di una Closure:

	$array = [
		['name' => 'Desk'],
		['name' => 'Chair'],
	];

	$array = array_values(array_sort($array, function ($value) {
		return $value['name'];
	}));

	/*
		[
			['name' => 'Chair'],
			['name' => 'Desk'],
		]
	*/

<a name="metodo-array-where"></a>
#### `array_where()` {#collection-metodo}

La funzione `array_where` filtra l'array usando una Closure:

	$array = [100, '200', 300, '400', 500];

	$array = array_where($array, function ($key, $value) {
		return is_string($value);
	});

	// [1 => 200, 3 => 400]

<a name="metodo-head"></a>
#### `head()` {#collection-metodo}

La funzione `head` ritorna semplicemente il primo elemento dell'array:

	$array = [100, 200, 300];

	$first = head($array);

	// 100

<a name="metodo-last"></a>
#### `last()` {#collection-metodo}

La funzione `last` ritorna l'ultimo elemento dell'array:

	$array = [100, 200, 300];

	$last = last($array);

	// 300

<a name="percorsi"></a>
## Percorsi

<a name="metodo-app-path"></a>
#### `app_path()` {#collection-metodo}

La funzione `app_path` Restituisce il percorso completo della directory `app`:

	$path = app_path();

Puoi anche usare la funzione `app_path` per generare un percorso completo ad un file relativo alla directory dell'applicazione:

	$path = app_path('Http/Controllers/Controller.php');

<a name="metodo-base-path"></a>
#### `base_path()` {#collection-metodo}

La funzione `base_path` restituisce il percorso completo alla root della tua applicazione:

	$path = base_path();

Puoi usare la funzione `base_path` anche per generare un percorso completo ad una data directory relativa all'applicazione:

	$path = base_path('vendor/bin');

<a name="metodo-config-path"></a>
#### `config_path()` {#collection-metodo}

La funzione `config_path` ritorna il percorso completo alla directory di configurazione dell'applicazione:

	$path = config_path();

<a name="metodo-database-path"></a>
#### `database_path()` {#collection-metodo}

La funzione `database_path` ritorna il percorso completo alla directory database dell'applicazione:

	$path = database_path();

<a name="metodo-public-path"></a>
#### `public_path()` {#collection-metodo}

La funzione `public_path` ritorna il percorso completo alla directory `public`:

	$path = public_path();

<a name="metodo-storage-path"></a>
#### `storage_path()` {#collection-metodo}

La funzione `storage_path` ritorna il percorso completo alla directory `storage`:

	$path = storage_path();

Puoi anche usare la funzione `storage_path` per generare un percorso completo ad un dato file relativo alla directory storage:

	$path = storage_path('app/file.txt');

<a name="stringhe"></a>
## Stringhe

<a name="metodo-camel-case"></a>
#### `camel_case()` {#collection-metodo}

La funzione `camel_case` converte una stringa nel formato `camelCase`:

	$camel = camel_case('foo_bar');

	// fooBar

<a name="metodo-class-basename"></a>
#### `class_basename()` {#collection-metodo}

La funzione `class_basename` ritorna il nome della classe senza namespace:

	$class = class_basename('Foo\Bar\Baz');

	// Baz

<a name="metodo-e"></a>
#### `e()` {#collection-metodo}

La funzione `e` esegue `htmlentities` sulla stringa:

	echo e('<html>foo</html>');

<a name="metodo-ends-with"></a>
#### `ends_with()` {#collection-metodo}

La funzione `ends_with` determina se una stringa termina con un dato valore:

	$value = ends_with('This is my name', 'name');

	// true

<a name="metodo-snake-case"></a>
#### `snake_case()` {#collection-metodo}

La funzione `snake_case` converte una stringa nel formato `snake_case`:

	$snake = snake_case('fooBar');

	// foo_bar

<a name="metodo-str-limit"></a>
#### `str_limit()` {#collection-metodo}

La funzione `str_limit` limita il numero di caratteri di una stringa. La funzione accetta una stringa come primo parametro e il massimo numero di caratteri risultanti come secondo parametro:

	$value = str_limit('The PHP framework for web artisans.', 7);

	// The PHP...

<a name="metodo-starts-with"></a>
#### `starts_with()` {#collection-metodo}

La funzione `starts_with` determina se una stringa inizia con un dato valore:

	$value = starts_with('This is my name', 'This');

	// true

<a name="metodo-str-contains"></a>
#### `str_contains()` {#collection-metodo}

La funzione `str_contains` determina se la stringa contiene un dato valore:

	$value = str_contains('This is my name', 'my');

	// true

<a name="metodo-str-finish"></a>
#### `str_finish()` {#collection-metodo}

La funzione `str_finish` aggiunge una singola istanza di un dato valore ad una stringa:

	$string = str_finish('this/string', '/');

	// this/string/

<a name="metodo-str-is"></a>
#### `str_is()` {#collection-metodo}

La funzione `str_is` determina se una stringa è associabile ad un pattern. Può essere usato un asterisco per indicare una wildcard:

	$value = str_is('foo*', 'foobar');

	// true

	$value = str_is('baz*', 'foobar');

	// false

<a name="metodo-str-plural"></a>
#### `str_plural()` {#collection-metodo}

La funzione `str_plural` converte una stringa nella sua forma plurale. Questa funzione supporta solo la lingua Inglese:

	$plural = str_plural('car');

	// cars

	$plural = str_plural('child');

	// children

<a name="metodo-str-random"></a>
#### `str_random()` {#collection-metodo}

La funzione `str_random` Genera una stringa casuale con lunghezza determinata dal valore dato:

	$string = str_random(40);

<a name="metodo-str-singular"></a>
#### `str_singular()` {#collection-metodo}

La funzione `str_singular` converte una stringa nella sua forma singolare. Questa funzione supporta solo la lingua Inglese:

	$singular = str_singular('cars');

	// car

<a name="metodo-str-slug"></a>
#### `str_slug()` {#collection-metodo}

La funzione `str_slug` genera un URL "slug" dalla stinga data:

	$title = str_slug("Laravel 5 Framework", "-");

	// laravel-5-framework

<a name="metodo-studly-case"></a>
#### `studly_case()` {#collection-metodo}

La funzione `studly_case` converte la stringa nel formato `StudlyCase`:

	$value = studly_case('foo_bar');

	// FooBar

<a name="metodo-trans"></a>
#### `trans()` {#collection-metodo}

La funzione `trans` traduce la linea di linguaggio data usando i [File di localizzazione](/docs/{{version}}/localization):

	echo trans('validation.required'):

<a name="metodo-trans-choice"></a>
#### `trans_choice()` {#collection-metodo}

La funzione `trans_choice` traduce un testo con la sua inflessione:

	$value = trans_choice('foo.bar', $count);

<a name="url"></a>
## URL

<a name="metodo-action"></a>
#### `action()` {#collection-metodo}

La funzione `action` genera un URL per una data azione di un controller. Non hai bisogno di passare il namespace completo del controller. Invece, passa il nome della classe del controller relativo al namespace `App\Http\Controllers`:

	$url = action('HomeController@getIndex');

Se il metodo accetta dei parametri dalla route, puoi passarli come secondo parametro del metodo:

	$url = action('UserController@profile', ['id' => 1]);

<a name="metodo-route"></a>
#### `route()` {#collection-metodo}

La funzione `route` genera un URL per una data route nominata:

	$url = route('routeName');

Se la route riceve dei parametri, puoi passarli come secondo parametro del metodo:

	$url = route('routeName', ['id' => 1]);

<a name="metodo-url"></a>
#### `url()` {#collection-metodo}

La funzione `url` genera un URL completo ad un dato percorso:

	echo url('user/profile');

	echo url('user/profile', [1]);

<a name="varie"></a>
## Varie

<a name="metodo-csrf-token"></a>
#### `csrf_token()` {#collection-metodo}

La funzione `csrf_token` recupera il valore corrente del token CSRF:

	$token = csrf_token();

<a name="metodo-dd"></a>
#### `dd()` {#collection-metodo}

La funzione `dd` Effettua il dump della variabile data e termina l'esecuzione dello script:

	dd($value);

<a name="metodo-elixir"></a>
#### `elixir()` {#collection-metodo}

La funzione `elixir` ritorna il percorso al file [Elixir](/docs/{{version}}/elixir):

	elixir($file);

<a name="metodo-env"></a>
#### `env()` {#collection-metodo}

La funzione `env` recupera il valore di una variabile d'ambiente o ritorna un valore di default:

	$env = env('APP_ENV');

	// Return a default value if the variable doesn't exist...
	$env = env('APP_ENV', 'production');

<a name="metodo-event"></a>
#### `event()` {#collection-metodo}

La funzione `event` invia un dato [evento](/docs/{{version}}/events) ai suoi listener:

	event(new UserRegistered($user));

<a name="metodo-response"></a>
#### `response()` {#collection-metodo}

La funzione `response` crea un istanza di [risposta](/docs/{{version}}/responses) oppure ottiene un istanza della response factory:

	return response('Hello World', 200, $headers);

	return response()->json(['foo' => 'bar'], 200, $headers);

<a name="metodo-value"></a>
#### `value()` {#collection-metodo}

La funzione `value` ritornerà semplicemente il valore dato. Tuttavia, se passi una `Closure` alla funzione, la `Closure` sarà eseguita e sarà ritornato il suo valore:

	$value = value(function() { return 'bar'; });

<a name="metodo-view"></a>
#### `view()` {#collection-metodo}

La funzione `view` recupera un istanza di [view](/docs/{{version}}/views):

	return view('auth.login');

<a name="metodo-with"></a>
#### `with()` {#collection-metodo}

La funzione `with` ritorna il valore dato. Questa funzione è particolaremente utile per il concatenamento di metoti dove altrimenti sarebbe impossibile :

	$value = with(new Foo)->work();
