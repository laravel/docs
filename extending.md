# Estendere Il Framework

- [Manager & Factory](#manager-e-factory)
- [Cache](#cache)
- [Sessioni](#sessioni)
- [Autenticazione](#autenticazione)
- [Estensione basata Su IoC](#estensione-basata-ioc)

<a name="manager-e-factory"></a>
## Manager & Factory

Laravel offre, letteralmente, una marea di classi `Manager` per quanto riguarda la personalizzazione del comportamento e dei suoi componenti. Queste includono la cache, le sessioni, l'autenticazione e le code. La classe Manager, come puoi immaginare, ha proprio la responsabilità di fornire le funzionalità base necessarie alla creazione di un componente basato su driver legato, a sua volta, con il sistema di configurazione dell’applicazione. Per esempio, la classe `CacheManager` può crare APC, Memcached, File, è altri tipi di implementazione di driver cache.

Ognuno di questi manager include un metodo `extend` il quale può essere usato facilmente per iniettare le funzionalità di risoluzione di un nuovo driver all'interno del manager. Esamineramo tutti questi manager sotto, con esempi di come iniettare il supporto dei driver personalizzati per ciascuno di essi.

> **Nota:** Prenditi del tempo per sfogliare i vari tipi di classe `Manager` usati da Laravel, come `CacheManager` e `SessionManager`. Leggendo il codice di queste classi avrai più coscienza di come Laravel lavora “dietro le quinte”. Tutte le classi manager estendo la classe base `Illuminate\Support\Manager`, la quale offre alcune utili funzionalità per ogni manager.

<a name="cache"></a>
## Cache

Per estendere la struttura delegata alla Cache di Laravel useremo il metodo `extend` nel `CacheManager`, che permette l’aggancio ad un nuovo driver da usare. Ecco, per esempio, il codice da scrivere per creare un nuovo driver “mongo”. 

	Cache::extend('mongo', function($app)
	{
		return Cache::repository(new MongoStore);
	});

Il primo parametro passato al metodo `extend` è il nome del driver. Dovrà essere un valore corrispondente a quello che, successivamente, verrà inserito in `config/cache.php`. Il secondo parametro è una Closure che ritorna un'istanza di `Illuminate\Cache\Repository. La Closure sarà passata ad un'istanza `$app`, che a sua volta è un istanza della classe `Illuminate\Foundation\Application`.

La chiamata a `Cache::extend` potrebbe essere fatta nel metodo di default `boot` di `App\Providers\AppServiceProvider` che lavora con Laravel, oppure puoi creare un tuo service provider per creare questa estensione – non dimenticarti però di registrare il provider nell'array providce in `config/app.php`.

Per crare il nostro driver cache personalizzato, abbiamo bisogno di implementare ilò contract `Illuminate\Contracts\Cache\Store`. Quindi, la nostra implementazione del driver cache MongoDB dovrebbe essere qualcosa come:

	class MongoStore implements Illuminate\Contracts\Cache\Store {

		public function get($key) {}
		public function put($key, $value, $minutes) {}
		public function increment($key, $value = 1) {}
		public function decrement($key, $value = 1) {}
		public function forever($key, $value) {}
		public function forget($key) {}
		public function flush() {}

	}

Abbiamo bisogno di implementare tutti questi metodi usando una connessione a MongoDB. Una volta completata l'implementazione, possiamo terminare la nostra registrazione del driver personalizzato:

	Cache::extend('mongo', function($app)
	{
		return Cache::repository(new MongoStore);
	});

Nel caso ti stessi chiedendo dove mettere il codice creato, puoi tranquillamente creare un namespace Extensions, oppure, perchè no, renderlo disponibile su Packagist! Oppure, potresti creare un namespace `Extensions` nella tua directory `app`. Tuttavia, tieni a mente che Laravel non ha una struttura rigida e sei libero di organizzare la tua applicazione secondo le tue preferenze.

<a name="sessioni"></a>
## Sessioni

Estendere Laravel con un driver di sessione personalizzato e facile come estendere il sistema cache. Ancora una volta, useremo il metodo `extend` per la registrazione del nostro codice personalizzato:

	Session::extend('mongo', function($app)
	{
		// Return implementation of SessionHandlerInterface
	});

### Dove Estendere La Sessione

Potresti inserire il tuo codice di estensione sessione nel metodo `boot` del tuo `AppServiceProvider`.

### Scrivere L'Estensione Della Sessione

Nota che il nostro driver di sessione personalizzato deve implementare `SessionHandlerInterface`. Questa interfaccia contiene alcuni semplici metodi che hanno bisogno di essere implementati. Un'implementazione MongoDB sarebbe simile a qualcosa del tipo:

	class MongoHandler implements SessionHandlerInterface {

		public function open($savePath, $sessionName) {}
		public function close() {}
		public function read($sessionId) {}
		public function write($sessionId, $data) {}
		public function destroy($sessionId) {}
		public function gc($lifetime) {}

	}

Dal momento che questi metodi non sono di facile comprensione come per l'interfaccia cache `StoreInterface`, spieghiamo velocemente cosa fanno:

- Il metodo `open` viene usato tipicamente usato nei sistemi di sessioni basati su files. Dato che Laravel ha, di default, un driver di questo tipo, non avrai quasi mai bisogno di scrivere niente in corrispondenza di questo metodo. Tutto quello che dovrai fare sarà lasciarlo come un semplice stub, vuoto. E' semplicemente una questione di design di interfacce “povere” (di cui parleremo più avanti) che PHP ci richiede per implementare questo metodo.
- Il metodo `close`, come il metodo `open`, lascialo pure questo metodo così com’è. Per molti driver, non è necessario avere un implementazione.
- Il metodo `read` ha il compito di ritornare una stringa contenente i dati della sessione associati ad un determinato `$sessionId`. Non c’è bisogno di effettuare nessuna serializzazione o encoding in fase di recupero del dato, dato che Laravel se ne occupa automaticamente.
- Il metodo `write` si occupa di scrivere la stringa passata come parametro in `$data` in corrispondenza di un preciso id `$sessionId` per qualche sistema di memorizzazione, come MongoDB, Dynamo, etc.
- Il metodo `destroy` snon fa altro che rimuovere tutti i dati associati ad una specifica sessione, indicata univocamente dall’id `$sessionId`.
- Il metodo `gc` dato un certo parametro $lifetime, si occupa di rimuovere tutti i dati precedenti a questo. Per i vari sistemi dotati di auto-expiring invece, come Redis o Memcached, questo metodo dovrebbe essere lasciato vuoto.

Una volta che `SessionHandlerInterface` è stata implementata, siamo pronti per registrarla con il manager di Sessione:

	Session::extend('mongo', function($app)
	{
		return new MongoHandler;
	});

Una volta registrato il driver di sessione, possiamo usare il driver `mongo` nel nostro file di configurazione `config/session.php`.

> **Nota:** Ricorda, se scrivi un handler di sessione personalizzato, condividilo su Packagist!

<a name="autenticazione"></a>
## Autenticazione

Proprio come per il sistema di cache o di sessioni, anche l’autenticazione può facilmente essere presa, estesa e migliorata come meglio si crede, in modo tale da venire incontro a tutte le esigenze. Ancora una volta, useremo il metodo `extend` di cui abbiamo già preso familiarità:

	Auth::extend('riak', function($app)
	{
		// Return implementation of Illuminate\Contracts\Auth\UserProvider
	});

Le implementazioni di `UserProvider` sono responsabili di effettuare il fetching di un implementazione di `Illuminate\Contracts\Auth\Authenticatable` da un sistema di storage persistente, come un database, Riak e così via. Questi due tipi di interfaccia permetto al meccanismo di autenticazione di Laravel, di continuare a funzionare, senza stare a guardare come i dati dell’utente sono memorizzati e qual è la classe usata.

Diamo un'occhiata al contract `UserProvider`:

	interface UserProvider {

		public function retrieveById($identifier);
		public function retrieveByToken($identifier, $token);
		public function updateRememberToken(Authenticatable $user, $token);
		public function retrieveByCredentials(array $credentials);
		public function validateCredentials(Authenticatable $user, array $credentials);

	}

Il metodo `retrieveById` si occupa tipicamente di ricevere una chiave numerica rappresentante il singolo utente. Un po’ come l’id autoincrementante, per intenderci. L’implementazione di `Authenticatable` corrispondente a quel determinato ID è quindi prelevata e restituita al sistema da questo metodo. 

Il metodo `retrieveByToken` recuperà un utente da un `$identifier` unico e dal `$token` “ricordati di me”, memorizzato nel campo `remember_token`. Come il metodo precedente, verrà prelevata e restituita un implementazione di `Authenticatable`.

Il metodo `updateRememberToken` aggionra il campo `$user` `remember_token` con un nuovo `$token`. Il nuovo token può essere un token, assegnato da un tentativo di login andato a buon fine con l'opzione “ricordati di me”, oppure null quando l'utente esegue un logout.

Il metodo `retrieveByCredentials` riceve un array di credenziali passato la metodo `Auth::attempt` quando si tenta di loggarsi nell'applicazione. Questo metodo effettua una query per ritrovare l'utente con queste credenziali. Normalmente, questo metodo eseguirà una query con una condizione “where” su `$credentials['username']`. **Questo metodo non deve tentare di eseguire nessuna operazione di convalida password o di autenticazione.**

Il metodo `validateCredentials` confronta l'utente `$user` dato con `$credentials` con l'utente autenticato. Per esempio, questo metodo potrebbe confrontare la stringa `$user->getAuthPassword()` su un `Hash::make` di `$credentials['password']`.

Ora che abbiamo esaminato ogni metodo di `UserProvider`, diamo uno sguardo a `Authenticatable`. Ricorda, il provider deve ritornare un implementazione di questa interfaccia dai metodi `retrieveById` e `retrieveByCredentials`:

	interface Authenticatable {

		public function getAuthIdentifier();
		public function getAuthPassword();
		public function getRememberToken();
		public function setRememberToken($value);
		public function getRememberTokenName();

	}

Questa interfaccia è semplice. Il metodo `getAuthIdentifier` ritorna una "primary key" dell'utente. Nel database, questa chiave dovrebbe essere una chiave auto-incrementante. Il metodo `getAuthPassword` ritorna l'hash della password dell'utente. Questa interfaccia permette al sistema di autenticazione di lavorare con qualsiasi classe User, a seconda di quale ORM, o livello di astrazione dello storage, tu stia usando. Di default, Laravel offre una classe `User` nella directory `app` che implementa questa interfaccia, quindi puoi consultare questa classe per un esempio di implementazione.

Finalmente, una volta implementato `UserProvider`, siamo pronti a registrare la nostra estensione con la facade `Auth`:

	Auth::extend('riak',
 function($app)
	{
		return new RiakUserProvider($app['riak.connection']);
	});

Dopo aver registrato il driver col metodo `extend`, passa al nuovo driver nel file di configurazione `config/auth.php`.

<a name="estensione-basata-ioc"></a>
## Estensione basata Su IoC

Praticamente, quasi tutti i service provider inclusi in Laravel “agganciano” le varie istanze tramite l’IoC Container. Se vuoi avere un’idea precisa di tutti i vari service provider, dai uno sguardo. Con un po’ di tempo, l’ideale sarebbe guardarti nel dettaglio un po’ tutto il codice sorgente dei vari provider, per capire meglio il loro funzionamento. Facendolo, otterrai una maggiore consapevolezza di come ogni provider si aggiunge al framework, così come quali chiavi sono usate per eseguire il bind di vari servizi nell'IoC container.

Per esempio, il provider `HashServiceProvider` usa il bind di una chiave `hash` nell'IoC container, che viene risolto in un istanza di `Illuminate\Hashing\BcryptHasher`. Puoi estendere e sovrascrivere facilmente questa classe con la tua applicazione e usare i tuoi binding. Per esempio:

	<?php namespace App\Providers;

	class SnappyHashProvider extends \Illuminate\Hashing\HashServiceProvider {

		public function boot()
		{
			$this->app->bindShared('hash', function()
			{
				return new \Snappy\Hashing\ScryptHasher;
			});

			parent::boot();
		}

	}

Nota che questa classe estende `HashServiceProvider`, non la classe base di default `ServiceProvider`. Una volta esteso il service provider, cambia l'`HashServiceProvider` nel tuo file di configurazione `config/app.php` con il nome del tuo nuovo provider.

Questo è il metodo generare di estendere qualsiasi classe del core del framework è vincolata al container. Essenzialmente ogni classe è vincolata nel container in questo modo, e può essere sovrascritta. Ancora una volta, analizza ogni service provider incluso nel framework per prendere familiarità con tutte le classi vincolate al container, è quali chiavi sono associate ad essi. Questo è il modo migliore per imparare di più su come Laravel le unisce tra loro.
