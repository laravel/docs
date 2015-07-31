# Cache

- [Configurazione](#configurazione)
- [Uso della Cache](#uso-cache)
	- [Ottenere un'Istanza della Cache](#ottenere-istanza-cache)
	- [Recuperare degli Elementi dalla Cache](#recuperare-elementi-cache)
	- [Memorizzare Elementi nella Cache](#memorizzare-elementi-cache)
	- [Rimuovere Elementi dalla Cache](#rimuovere-elementi-cache)
- [Aggiungere Nuovi Driver](#aggiungere-nuovi-driver)

<a name="configurazione"></a>
## Configurazione

Laravel offre un'API unificata per svariati sistema di caching. Puoi trovarne le impostazioni nel file _config/cache.php_. In tale file dovrai specificare quale driver usare nella tua applicazione. Laravel supporta svariati sistemi dedicati allo scopo, come [Memcached](http://memcached.org) e [Redis](http://redis.io) out of the box.

Il file di configurazine per la cache, inoltre, contiene svariate altre operazioni, documentate nel file stesso, quindi assicurati di guardare tutto per bene. Di default, Laravel lavora con il driver _file_, che memorizza i dati serializzati nel filesystem. Per altre applicazioni più grandi, la cosa migliore è usare un sistema di cache in memoria come Memcached o APC. Nulla ti vieta, inoltre, di avere più configurazioni per lo stesso driver.

### Prerequisiti

#### Database

Se usi il driver _database_ per la cache, dovrai creare una tabella dedicata allo scopo. Ecco lo schema da usare in una migration.

	Schema::create('cache', function($table) {
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});

#### Memcached

Se dovessi decidere di usare Memcached, sappi che richiede il [Memcached PECL package](http://pecl.php.net/package/memcached). Quindi, installalo.

Di default, la [configurazione](#configurazione) usa TCP/IP su [Memcached::addServer](http://php.net/manual/en/memcached.addserver.php):

	'memcached' => [
		[
			'host' => '127.0.0.1',
			'port' => 11211,
			'weight' => 100
		],
	],

Potresti inoltre voler settare l'host da usare come UNIX Socket path. Puoi farlo in questo modo, impostando inoltre la porta da usare su 0.

	'memcached' => [
		[
			'host' => '/var/run/memcached/memcached.sock',
			'port' => 0,
			'weight' => 100
		],
	],

#### Redis

Prima di usare Redis con Laravel, assicurati di aver installato il package `predis/predis` tramite Composer.

Per maggiori informazioni sulla configurazione, dai uno sguardo alla [pagina ad esso dedicata](/documentazione/5.1/redis#configurazione).

<a name="uso-cache"></a>
## Uso della Cache

<a name="ottenere-istanza-cache"></a>
### Ottenere un'Istanza della Cache

I due [contract](/documentazione/5.1/contracts) `Illuminate\Contracts\Cache\Factory` ed `Illuminate\Contracts\Cache\Repository` ti forniscono l'accesso ai servizi di Cache presenti in Laravel. Nello specifico, `Factory` ti da l'accesso a tutti i driver definiti per la tua applicazione. `Repository`, invece, è tipicamente l'implementazione del driver che hai specificato nel file di configurazione `cache`.

Per comodità potresti voler usare la Facade `Cache`, che è quella che poi useremo in questa documentazione. La Facade in oggetto fonisce a sua volta una sintassi semplice ed espressiva per l'accesso alle funzionalità sottostanti del sistema di cache.

Iniziamo dalla semplice importazione in un controller.

	<?php namespace App\Http\Controllers;

	use Cache;
	use Illuminate\Routing\Controller;

	class UserController extends Controller
	{
		/**
		 * Show a list of all users of the application.
		 *
		 * @return Response
		 */
		public function index()
		{
			$value = Cache::get('key');

			//
		}
	}

Nulla di più. Importiamo _Cache_, che viene poi usata.

#### Accedere a Diversi Sistemi di Cache

Potresti decidere, per la tua applicazione, di memorizzare in diversi sistemi di cache diverse entità o strutture. Tramite il metodo _store_ puoi decidere quale _store_ richiamare, tra quelli presenti nel file di configurazione _cache_ apposito.

	$value = Cache::store('file')->get('foo');

	Cache::store('redis')->put('bar', 'baz', 10);

<a name="recuperare-elementi-cache"></a>
### Recuperare degli Elementi dalla Cache

Il metodo _get_ viene usato per recuperare i vari elementi dal sistema di cache scelto. Nel momento in cui l'elemento richiesto non esiste viene restituito _null_, anche se è possibile specificare, come secondo argomento, un eventuale valore di default.

	$value = Cache::get('key');

	$value = Cache::get('key', 'default');

Puoi anche scegliere di usare una _Closure_ per ritornare un ipotetico valore di default. 

	$value = Cache::get('key', function() {
		return DB::table(...)->get();
	});

#### Controllare l'Esistenza di un Elemento

Il metodo _has_ viene usato per controllare l'eventuale esistenza di un elemento.

	if (Cache::has('key')) {
		//
	}

#### Incrementare / Decrementare dei Valori

I metodi _increment_ e _decrement_ possono essere usati per "sistemare" adeguatamente il valore di un integer nella cache. Entrambi i metodi accettano inoltre un secondo parametro (facoltativo) che specifichi l'ammontare dell'operazione. Di default, il valore di questo secondo parametro è ovviamente 1.

	Cache::increment('key');

	Cache::increment('key', $amount);

	Cache::decrement('key');

	Cache::decrement('key', $amount);

#### Preleva o Aggiorna

A volte potresti voler recuperare un elemento dalla cache, ma anche memorizzare per un certo indice uno specifico valore qualora questo non esistesse. Ad esempio, immagina di mettere l'elenco degli utenti nella cache e dare, a questa lista, l'indice "users". In cache però questi valori non ci sono ancora, e alla prima chiamata di questo metodo voglio che tale lista venga presa dal database. Una volta presa dal database, quindi, deve essere anche automaticamente salvata per l'indice "users" in cache.

Ecco come fare tutto questo con un solo metodo: _remember_.

	$value = Cache::remember('users', $minutes, function() {
		return DB::table('users')->get();
	});

Il primo parametro è la chiave da usare, il secondo è il numero di minuti di "vita" del record all'interno della cache, il terzo parametro (la closure) ritorna un valore di default (in questo caso legge dal database l'elenco degli utenti).

Se vuoi memorizzare "per sempre" un certo valore, allora non devi fare altro che usare _rememberForever_.

	$value = Cache::rememberForever('users', function() {
		return DB::table('users')->get();
	});

#### Preleva e Cancella

Se hai bisogno di prelevare un elemento dalla cache per poi cancellarlo, usa il metodo _pull_. Esattamente come _get_ ritorna il valore, con la differenza però, poi, di cancellarlo.

	$value = Cache::pull('key');

<a name="memorizzare-elementi-cache"></a>
### Memorizzare Elementi nella Cache

Il metodo da usare per memorizzare dei valori è _put_. La sintassi è la seguente:

	Cache::put('key', 'value', $minutes);

Il primo parametro è la chiave da usare, quindi il valore e infine, in minuti, la durata di permanenza dell'elemento. Una cosa davvero interessante è la possibilità di passare, come durata, un'istanza di _DateTime_ (o come vedrai nel prossimo esempio, _Carbon_).

	$expiresAt = Carbon::now()->addMinutes(10);

	Cache::put('key', 'value', $expiresAt);

Il metodo _add_, invece, si occuperà di aggiungere un elemento solo se non già presente nella cache. Ritornerà _true_ se l'elemento è stato aggiunto, _false_ in caso esista già.

	Cache::add('key', 'value', $minutes);

Il metodo _forever_, infine, inserisce in cache un valore in modo permanente.

	Cache::forever('key', 'value');

<a name="rimuovere-elementi-cache"></a>
### Rimuovere Elementi dalla Cache

Per rimuovere un elemento dalla cache, usa il metodo _forget_.

	Cache::forget('key');

<a name="aggiungere-nuovi-driver"></a>
## Aggiungere Nuovi Driver

Se preferisci, puoi estendere tu stesso le funzionalità di Laravel con altri sistemi di cache. Come? Semplicemente, creando dei nuovi driver compatibili e registrandoli tramite il resolver specifico. Normalmente una cosa del genere viene fatta con un [service provider](/documentazione/5.1/provider) apposito.

Nell'esempio di seguito è stato creato un nuovo provider incaricato della registrazione di un nuovo driver per la Cache.

	<?php namespace App\Providers;

	use Cache;
	use App\Extensions\MongoStore;
	use Illuminate\Support\ServiceProvider;

	class CacheServiceProvider extends ServiceProvider
	{
		/**
		 * Perform post-registration booting of services.
		 *
		 * @return void
		 */
		public function boot()
		{
			Cache::extend('mongo', function($app) {
				return Cache::repository(new MongoStore);
			});
		}

		/**
		 * Register bindings in the container.
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}
	}

Il primo argomento passato al metodo _extend_ è il nome del driver. Tale nome corrisponderà all'opzione _driver_ in `config/cache.php`. 

Il secondo argomento è invece una Closure, che dovrà ritornare un'istanza di `Illuminate\Cache\Repository`. A tale closure verrà passata un'istanza _$app_ del [service container](/documentazione/5.1/container).

Il posto migliore per chiamare `Cache::extend` potrebbe essere il metodo `boot` della classe `App\Providers\AppServiceProvider` già presente in Laravel. Nulla ti vieta, ovviamente, di crearti un provider appositamente per lo scopo. A te la scelta!

Passiamo adesso alla realizzazione. La prima cosa da fare è creare un'implementazione del [contract](/documentazione/5.1/contract) `Illuminate\Contracts\Cache\Store`. Qualcosa del genere:

	<?php namespace App\Extensions;

	class MongoStore implements \Illuminate\Contracts\Cache\Store
	{
		public function get($key) {}
		public function put($key, $value, $minutes) {}
		public function increment($key, $value = 1) {}
		public function decrement($key, $value = 1) {}
		public function forever($key, $value) {}
		public function forget($key) {}
		public function flush() {}
	}

Chiaramente dovremo implementare ogni singolo metodo usando la connessione MongoDB specifica. A quel punto, una volta creata la classe, possiamo registrare il driver adeguatamente.

	Cache::extend('mongo', function($app) {
		return Cache::repository(new MongoStore);
	});

Una volta completata l'estensione puoi tranquillamente aggiornare il file di configurazione `config/cache.php`, impostando il nuovo driver sotto la voce, appunto, `driver`.

> Un consiglio: se hai creato un nuovo driver che prima non esisteva, mettilo su Packagist! Potrebbe essere utile anche ad altri!
