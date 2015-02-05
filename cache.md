# Cache

- [Configurazione](#configurazione)
- [Utilizzo Cache](#utilizzo-cache)
- [Incrementi & Decrementi](#incrementi-e-decrementi)
- [Cache Tag](#cache-tag)
- [Database Cache](#database-cache)

<a name="configurazione"></a>
## Configurazione

Laravel fornisce un API per vari sistemi di caching. Il file di configurazione della cache si trova in `config/cache.php`. In questo file puoi specificare il driver che preferisci usare di default per la tua applicazione. Laravel supporta le più conosciute tecnologie di caching come [Memcached](http://memcached.org) e [Redis](http://redis.io).

Il file di configurazione della cache contiene inoltre molte altre opzioni, documentate al suo interno, quindi assicurati di leggerle. Di default, Laravel è configurato in modo che usi il driver `file`, che memorizza gli oggetti sul filesystem, serializzandoli. Per applicazioni più grandi, è consigliato usare una cache in-memory come Memcached o APC. Puoi sempre configurare configurazioni multiple di cache per uno stesso driver.

Prima di usare Redis con Laravel, è necessario installare il package `predis/predis` (~1.0) via Composer.

<a name="utilizzo-cache"></a>
## Utilizzo Cache

#### Memorizzare Un Elemento Nella Cache

	Cache::put('key', 'value', $minutes);

#### Usare Un Oggetto Carbon Per Impostare Un Tempo Di Scadenza

	$expiresAt = Carbon::now()->addMinutes(10);

	Cache::put('key', 'value', $expiresAt);

#### Memorizzare Un Elemento Nella Cache Se Non Esiste

	Cache::add('key', 'value', $minutes);

Il metodo `add` ritornerà `true` se l'elemento è stato realmente aggiunto alla cache. Altrimenti, il metodo ritornerà `false`.

#### Verificare L'Esistenza Di Un Elemento Nella Cache

	if (Cache::has('key'))
	{
		//
	}

#### Recuperare Un Elemento Dalla Cache

	$value = Cache::get('key');

#### Recuperare Un Elemento Oppure Ritornare Un Valore Di Default

	$value = Cache::get('key', 'default');

	$value = Cache::get('key', function() { return 'default'; });

#### Memorizzare Un Elemento Nella Cache Permanentemente

	Cache::forever('key', 'value');

A volte ti capiterà di dover recuperare un elemento dalla cache, ma anche di memorizzare un valore di default se l’elemento richiesto non è stato trovato. Potresti usare il metodo `Cache::remember`:

	$value = Cache::remember('users', $minutes, function()
	{
		return DB::table('users')->get();
	});

Potrai combinare, inoltre i metodi `remember` e `forever`:

	$value = Cache::rememberForever('users', function()
	{
		return DB::table('users')->get();
	});

Nota che tutti gli elementi salvati sono serializzati, quindi sei libero di memorizzare qualsiasi tipo di dato.

#### Pulling An Item From The Cache

If you need to retrieve an item from the cache and then delete it, you may use the `pull` method:

	$value = Cache::pull('key');

#### Rimuovere Un Elemento Dalla Cache

	Cache::forget('key');

<a name="incrementi-e-decrementi"></a>
## Incrementi & Decrementi

Tutti i driver, tranne `file` e `database`, supportano le operazioni di `incremento` e `decremento`:

#### Incrementare Un Valore

	Cache::increment('key');

	Cache::increment('key', $amount);

#### Decrementare Un Valore

	Cache::decrement('key');

	Cache::decrement('key', $amount);

<a name="cache-tags"></a>
## Cache Tag

> **Note:** I tag nella cache non sono supportati quando si usano i driver `file` o `database`. Di conseguenza, quando usi tag multipli con cache memorizzate per sempre, le performance saranno migliori usando un driver come `memcached` che elimina automaticamente i record non aggiornati.

#### Accedere Ad Una Cache Taggata

I tag ti permettono di “taggare” elementi correlati nella cache, per poi fare il flash di tutte le cache con un determinato nome. Per accederci, usa il metodo `tags`.

Puoi salvare una cache “taggata” passandole una lista di tag come parametri, oppure un array ordinato di tag:

	Cache::tags('people', 'authors')->put('John', $john, $minutes);

	Cache::tags(array('people', 'artists'))->put('Anne', $anne, $minutes);

Puoi usare qualsiasi metodo di memorizzazione della cache assieme, compresi `remember`, `forever`, e `rememberForever`. Puoi, inoltre, recuperare elementi, già presenti, dalla cache “taggata”, così come puoi usare i metodi `increment` e `decrement`.

#### Accedere Agli Elementi In Una Cache Taggata

Per accedere ad una cache “taggata”, passale la stessa lista ordinata di tag che hai usato quando l’hai salvata.

	$anne = Cache::tags('people', 'artists')->get('Anne');

	$john = Cache::tags(array('people', 'authors'))->get('John');

Puoi eliminare tutti gli elementi taggati con un nome o lista di nomi. Ad esempio, questo codice rimuove tutti gli elementi presenti taggati con `people`, `authors`, od entrambi. Quindi, entrambi “Anne” e John” saranno rimossi:

	Cache::tags('people', 'authors')->flush();

Viceversa, questo codice rimuove solo gli elementi taggati con `authors`, quindi “John” sarà rimosso, mentre “Anne” no.

	Cache::tags('authors')->flush();

<a name="database-cache"></a>
## Database Cache

Quando si usa il driver `database`, devi impostare una tabella che contenga gli elementi. Troverai, di seguito, una tabella di esempio, creata usando la classe `Schema`:

	Schema::create('cache', function($table)
	{
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});
