# Sessioni

- [Introduzione](#introduzione)
- [Uso Base](#uso-base)
	- [Dati Flash](#dati-flash)
- [Creare un Driver Personalizzato](#creare-driver-personalizzato)

<a name="introduzione"></a>
## Introduzione

Dato che le applicazioni basate su HTTP sono stateless, cioè senza stasto, le sessioni permettono di memorizzare alcune informazioni passando da una richiesta e l'altra. Laravel, di default, ha svariati driver per offrire questa funzionalità. Il tutto attraverso un'API unificata. Ad essere supportato è, ad esempio, [Memcached](http://memcached.org), o [Redis](http://redis.io).

### Configurazione

Il file di configurazione per il sistema di sessioni è `config/session.php`. Prima di lavorarci, quindi, assicurati di dare uno sguardo e controllare tutte le opzioni presenti nel file. Il file è ben documentato: non avrai particolari problemi a lavorarci. Di default Laravel è configurato con il driver _file_, che lavora con il filesystem. Dovrebbe andar bene per una buona parte di applicazioni. In produzione considera l'uso di _memcached_ o _redis_ per una maggiore velocità.

Il _driver_ definisce quindi dove questi dati verranno memorizzati. Allo stato attuale Laravel offre, out of the box, i seguenti driver:

* `file` - le sessioni vengono memorizzate in `storage/framework/sessions`;
* `cookie` - i dati di sessione vengono memorizzate in cookie criptati;
* `database` - le sessioni vengono memorizzate su database, su una tabella apposita;
* `memcached` / `redis` - i dati di sessione vengono memorizzati su questi due sistemi molto performanti;
* `array` - le sessioni vengono salvate su un semplice array PHP, ma il loro ciclo di vita si esaurisce nel contesto della richiesta corrente;

> **Nota:** come forse hai già immaginato, il driver _array_ è molto utile in fase di [testing](/docs/5.1/testing).

### Prerequisiti dei Driver

#### Database

Se usi il driver _database_ avrai bisogno di una tabella apposita dove salvare i vari elementi. Ecco un esempio di definizione di schema che potresti usare:

	Schema::create('sessions', function ($table) {
		$table->string('id')->unique();
		$table->text('payload');
		$table->integer('last_activity');
	});

Ovviamente, Artisan ha già un comando che puoi usare per generare la migration al posto tuo!

	php artisan session:table
	composer dump-autoload
	php artisan migrate

#### Redis

Prima di usare Redis con Laravel per quanto riguarda le sessioni, ricorda di installare il package `predis/predis`(~1.0) tramite Composer.

### Altra Considerazioni

Laravel usa la session key _flash_ internamente, quindi ricorda di non usarla nella tua applicazione, in quanto riservata.

Se hai bisogno di criptare tutti i dati di sessione, imposta l'opzione _encrypt_ su _true_.

<a name="uso-base"></a>
## Uso Base

#### Accedere ai Dati di Sessione

Vediamo innanzitutto come accedere ad un dato di sessione. Puoi accedere all'istanza del servizio di sessioni tramite la richiesta HTTP, che può essere iniettata direttamente nel metodo. Ecco un esempio:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Show the profile for the given user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function showProfile(Request $request, $id)
		{
			$value = $request->session()->get('key');

			//
		}
	}

Ad essere usato è il metodo _session()_, quindi il _get()_. Quando recuperi un valore di sessione, inoltre, puoi scegliere di passare un secondo parametro che funga da valore di "default" in caso l'elemento per la data chiave non dovesse esistere. Puoi inoltre passare anche una closure come valore di default.

	$value = $request->session()->get('key', 'default');

	$value = $request->session()->get('key', function() {
		return 'default';
	});

Se vuoi recuperare tutti i dati di sessione, usa _all_.

	$data = $request->session()->all();

Puoi anche usare la shortcut _session_, passandogli una chiave per recuperare un elemento oppure un array associativo per passargli i vari elementi da memorizzare.

	Route::get('home', function () {
		// Recupera un dato...
		$value = session('key');

		// Memorizza un dato...
		session(['key' => 'value']);
	});

#### Determinare se un Elemento Esiste

Puoi usare _has_ per sapere se un certo elemento esiste o meno in sessione. Tale metodo ritornerà _true_ se l'elemento è presente.

	if ($request->session()->has('users')) {
		//
	}

#### Memorizzare i Dati di Sessione

Una volta ottenuto l'accesso all'istanza, puoi chiamare una serie di metodi per interagire con i dati. Ad esempio, il metodo _put_ ti permette di memorizzare un nuovo dato in sessione.

	$request->session()->put('key', 'value');

#### Il metodo _push_

Il metodo _push_ può essere usato per inserire un nuovo elemento in un altro elemento in sessione che è un array. Ad esempio, se _user.teams_ contiene un array, puoi "spingerci" un nuovo valore in questo modo:

	$request->session()->push('user.teams', 'developers');

#### Recuperare e Cancellare un Elemento

Tramite il metodo _pull_ puoi recuperare e cancellare un elemento dalla sessione.

	$value = $request->session()->pull('key', 'default');

#### Cancellare degli Elementi dalla Sessione

Il metodo _forget_ cancellerà un certo elemento dalla sessione. Se vuoi rimuovere invece tutti i dati presenti, usa il metodo _flush_.

	$request->session()->forget('key');

	$request->session()->flush();

#### Rigenerare l'ID della Sessione

Per rigenerare l'id della sessione, usa _regenerate_.

	$request->session()->regenerate();

<a name="dati-flash"></a>
### Dati Flash

A volte, potresti voler memorizzare degli elementi in sessione in modo tale da poterli riusare nella richiesta successiva. Il metodo da usare a tale scopo, in caso, è _flash_.

	$request->session()->flash('status', 'Task was successful!');

Da questo momento in poi, _status_ sarà disponibile solo fino alla richiesta successiva. Nulla ti vieta chiaramente di ripetere l'operazione, per passare il dato stesso alla nuova richiesta successiva. In tal caso puoi usare _reflash_ oppure _keep_ se vuoi tenere solo uno specifico subset di elementi.

	$request->session()->reflash();

	$request->session()->keep(['username', 'email']);

<a name="creare-driver-personalizzato"></a>
## Creare un Driver Personalizzato

In aggiunta a quelli già presenti, puoi creare un tuo driver per il sistema di sessioni in modo molto semplice. Tutto quello che devi fare, infatti, è usare il metodo _extend_ sulla facade _Session_. Il posto migliore per effettuare tale operazione è in un [service provider](/docs/5.1/provider), nel metodo _boot_:

    <?php namespace App\Providers;

    use Session;
    use App\Extensions\MongoSessionStore;
    use Illuminate\Support\ServiceProvider;

    class SessionServiceProvider extends ServiceProvider
    {
        /**
         * Perform post-registration booting of services.
         *
         * @return void
         */
        public function boot()
        {
			Session::extend('mongo', function($app) {
				// Ritorna un'implementazione di SessionHandlerInterface...
				return new MongoSessionStore;
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

Nota bene che il driver personalizzato deve obbligatoriamente implementare alcuni metodi, rispettando la `SessionHandlerInterface`. Ecco i metodi previsti di cui c'è bisogno.

	<?php namespace App\Extensions;

	class MongoHandler implements SessionHandlerInterface
	{
		public function open($savePath, $sessionName) {}
		public function close() {}
		public function read($sessionId) {}
		public function write($sessionId, $data) {}
		public function destroy($sessionId) {}
		public function gc($lifetime) {}
	}

Vediamo a cosa servono:

* il metodo _open_ viene usato in un sistema tipicamente basasto su file. Raramente avrai bisogno di metterci mano, quindi lascialo come lo trovi, come un semplice stub;
* il metodo _close_ esattamente come _open_ viene generalmente lasciato stare. Non serve per molti driver;
* il metodo _read_ dovrebbe ritornare la stringa equivalente ad un elemento identificato da un certo _sessionId_. Ricorda che non c'è bisogno di serializare o deserializzare i dati in questa fase ed in quella di scrittura. Laravel fa tutto al posto tuo;
* il metodo _write_ scrive determinati dati sul sistema scelto, prendendo come riferimento un _sessionId_;
* il metodo _destroy_ rimuove i dati associati ad un certo _sessionId_;
* il metodo _gc_ distrugge tutti i dati di sessione più vecchi di un dato _lifetime_, un timestamp. Se usi un sistema self-expiring, come _Memcached_ e _Redis_, questo metodo va lasciato vuoto;

Una volta registrato il driver di sessione non devi fare altro, se non specificare _mongo_ (in questo esempio) come driver in `config/session.php`.
