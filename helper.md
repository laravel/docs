# Funzioni Helper

- [Array](#arraya)
- [Percorsi](#percorsi)
- [Stringhe](#stringhe)
- [URL](#url)
- [Varie](#varie)

<a name="array"></a>
## Array

### array_add

La funzione `array_add` aggiunge una coppia chiave / valore se la chiave data non esiste già nell'array.

	$array = array('foo' => 'bar');

	$array = array_add($array, 'key', 'value');

### array_divide

La funzione array_divide restituisce due array: il primo contiene le chiavi, l’altro i valori dell’array originale.

	$array = array('foo' => 'bar');

	list($keys, $values) = array_divide($array);

### array_dot

La funzione array_dot semplifica un array multi dimensionale restituendone uno singolo con la notazione "dot" per indicarne il livello di profondità.

	$array = array('foo' => array('bar' => 'baz'));

	$array = array_dot($array);

	// array('foo.bar' => 'baz');

### array_except

La funzione array_except rimuove la coppia chiave/valore dall’array.

	$array = array_except($array, array('keys', 'to', 'remove'));

### array_fetch

La funzione array_fetch restituisce un array semplificato che contiene gli elementi selezionati annidati.

	$array = array(
		array('developer' => array('name' => 'Taylor')),
		array('developer' => array('name' => 'Dayle')),
	);

	$array = array_fetch($array, 'developer.name');

	// array('Taylor', 'Dayle');

### array_first

La funzione `array_first` ritorna il primo elemento di un array se quest'ultimo passa un test.

	$array = array(100, 200, 300);

	$value = array_first($array, function($key, $value)
	{
		return $value >= 150;
	});

Un valore di default può essere passato come terzo parametro:

	$value = array_first($array, $callback, $default);

### array_last

Il metodo `array_last` ritorna l'ultimo elemento di un array se quest'ultimo passa un test.

	$array = array(350, 400, 500, 300, 200, 100);

	$value = array_last($array, function($key, $value)
	{
		return $value > 350;
	});

	// 500

Un valore di default può essere passato come terzo parametro:

	$value = array_last($array, $callback, $default);

### array_flatten

Il metodo `array_flatten` ridurrà un array multi dimensionale ad un singolo livello.

	$array = array('name' => 'Joe', 'languages' => array('PHP', 'Ruby'));

	$array = array_flatten($array);

	// array('Joe', 'PHP', 'Ruby');

### array_forget


Il metodo `array_forget` eliminerà una coppia chiave/valore da un array complesso utilizzando la notazione "dot".

	$array = array('names' => array('joe' => array('programmer')));

	array_forget($array, 'names.joe');

### array_get

Il metodo `array_get` recupererà una valore da un array complesso utilizzando la notazione "dot".

	$array = array('names' => array('joe' => array('programmer')));

	$value = array_get($array, 'names.joe');

	$value = array_get($array, 'names.john', 'default');

> **Nota:** Vuoi utilizzare `array_get` sugli oggetti ? Usa `object_get`.

### array_only

Il metodo `array_only` recupererà solo le specifiche coppie chiave/valore dall'array.

	$array = array('name' => 'Joe', 'age' => 27, 'votes' => 1);

	$array = array_only($array, array('name', 'votes'));

### array_pluck
 
La funzione array_pluck recupererà una lista delle specificate coppie chiave/valore dell’array.

	$array = array(array('name' => 'Taylor'), array('name' => 'Dayle'));

	$array = array_pluck($array, 'name');

	// array('Taylor', 'Dayle');

### array_pull

La funzione array_pull restituirà una specifica coppia chiave/valore dell’array, quindi la rimuoverà.

	$array = array('name' => 'Taylor', 'age' => 27);

	$name = array_pull($array, 'name');

### array_set

La funzione array_set imposterà un valore dentro un array annidato utilizzando la notazione “dot”.

	$array = array('names' => array('programmer' => 'Joe'));

	array_set($array, 'names.editor', 'Taylor');

### array_sort

La funzione array_sort ordina l’array restituito da una Closure.

	$array = array(
		array('name' => 'Jill'),
		array('name' => 'Barry'),
	);

	$array = array_values(array_sort($array, function($value)
	{
		return $value['name'];
	}));

### array_where

Filtra l'array usando una Closure.

	$array = array(100, '200', 300, '400', 500);

	$array = array_where($array, function($key, $value)
	{
		return is_string($value);
	});

	// Array ( [1] => 200 [3] => 400 )

### head

Restituisce il primo elemento dell'array. Utile per il metodo di concatenamento presente in PHP 5.3.x.

	$first = head($this->returnsArray('foo'));

### last

Restituisce l'ultimo elemento dell'array. Utile per il metodo di concatenamento.

	$last = last($this->returnsArray('foo'));

<a name="percorsi"></a>
## Percorsi

### app_path

Restituisce il percorso completo della directory `app`.

	$path = app_path();

### base_path

Restituisce il percorso completo alla root della tua applicazione.

### public_path

Restituisce il percorso completo della directory `public`.

### storage_path

Restituisce il percorso completo della directory `app/storage`.

<a name="stringhe"></a>
## Stringhe

### camel_case

Converte una data stringa nel formato `camelCase`.

	$camel = camel_case('foo_bar');

	// fooBar

### class_basename

Restituisce il nome della classe, senza namespace.

	$class = class_basename('Foo\Bar\Baz');

	// Baz

### e

Utilizza htmlentities su una stringa, con il supporto UTF-8.

	$entities = e('<html>foo</html>');

### ends_with

Determina se un valore è presente in un insieme.

	$value = ends_with('This is my name', 'name');

### snake_case

Converte una stringa nel formato `snake_case`.

	$snake = snake_case('fooBar');

	// foo_bar

### str_limit

Limita il numero di caratteri in una stringa.

	str_limit($value, $limit = 100, $end = '…')

Esempio:

	$value = str_limit('The PHP framework for web artisans.', 7);

	// The PHP...

### starts_with

Determina se un insieme inizia con un valore dato.

	$value = starts_with('This is my name', 'This');

### str_contains

Determina se un insieme contiene un valore.

	$value = str_contains('This is my name', 'my');

### str_finish

Aggiunge una singola istanza di un valore ad un insieme. Rimuove, inoltre qualsiasi istanza ulteriore.

	$string = str_finish('this/string', '/');

	// this/string/

### str_is

Determina se una stringa è associabile ad un pattern. Gli asterischi possono essere usati per indicare le wildcards.

	$value = str_is('foo*', 'foobar');

### str_plural

Converte una stringa nella sua forma plurale (Solo per l'Inglese).

	$plural = str_plural('car');

### str_random

Genera una stringa casuale con lunghezza determinata dal valore dato.

	$string = str_random(40);

### str_singular

Converte una stringa nella sua forma al singolare (Solo per l'Inglese).

	$singular = str_singular('cars');

### studly_case

Converte una stringa nel formato `StudlyCase`.

	$value = studly_case('foo_bar');

	// FooBar

### trans

Traduce un test. Alias di `Lang::get`.

	$value = trans('validation.required'):

### trans_choice

Traduce un testo con la sua inflessione. Alias di `Lang::choice`.

	$value = trans_choice('foo.bar', $count);

<a name="url"></a>
## URL

### action

Genera un URL da un'azione del Controller.

	$url = action('HomeController@getIndex', $params);

### route

Genera un URL dal nome di una route.

	$url = route('routeName', $params);

### asset

Genera un URL da un asset.

	$url = asset('img/photo.jpg');

### link_to

Genera un link HTML per l'URL specificato.

	echo link_to('foo/bar', $title, $attributes = array(), $secure = null);

### link_to_asset

Genera un link HTML per un asset specificato.

	echo link_to_asset('foo/bar.zip', $title, $attributes = array(), $secure = null);

### link_to_route

Genera un link HTML per una route specificata.

	echo link_to_route('route.name', $title, $parameters = array(), $attributes = array());

### link_to_action

Genera un link HTML per un'azione di un controller.

	echo link_to_action('HomeController@getIndex', $title, $parameters = array(), $attributes = array());

### secure_asset

Genera un link HTML per un asset usando il protocollo HTTPS.

	echo secure_asset('foo/bar.zip', $title, $attributes = array());

### secure_url

Genera un URL completo per un path specificato usando il protocollo HTTPS.

	echo secure_url('foo/bar', $parameters = array());

### url

Genera un URL completo per un path specificato.

	echo url('foo/bar', $parameters = array(), $secure = null);

<a name="varie"></a>
## Varie

### csrf_token

Restituisce il valore corrente del token CSRF.

	$token = csrf_token();

### dd

Effettua il dump della variabile data e termina l'esecuzione dello script.

	dd($value);

### value

Se il valore dato è una `Closure`, restituisce il valore ritornato dalla `Closure`. Altrimenti, restituisce il valore.

	$value = value(function() { return 'bar'; });

### with

Restituisce l’oggetto specificato. Utile per i costruttori che concatenano i metodi in PHP 5.3.x.

	$value = with(new Foo)->doWork();
