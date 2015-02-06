# Facade

- [Introduzione](#introduzione)
- [Spiegazione](#spiegazione)
- [Uso Pratico](#uso-pratico)
- [Creare Facade](#creare-facade)
- [Mocking delle Facades](#mocking-facades)
- [Le Classi Facade Reference](#classi-facade-reference)

<a name="introduzione"></a>
## Introduzione

Il sistema di Facade offre un interfaccia "statica" a tutte le classi disponibili attraverso l'[IoC container](/container). Laravel conta già diverse facade pronte all'uso, e probabilmente le hai usate senza neanche saperlo. Le Facade di Laravel fanno da proxy per le classi "sottostanti" presenti nell'IoC Container, dando allo sviluppatore la possibilità di usare una sintassi espressiva ma mantenendo, allo stesso tempo, la flessibilità e la testabilità che con un metodo statico non si può ottenere. 

Occasionalmente, portesti voler creare la tua propria facade per la tua applicazione o per i tuoi package, andiamo ad esaminare lo sviluppo, contetto ed uso di queste classi.

> **Nota:** prima di buttarti nel mondo della Facades, è consigliabile avere ben presente in mente il concetto di [IoC Container](/container).

<a name="spiegazione"></a>
## Spiegazione

Nel contesto di un’applicazione Laravel, una Facade è una classe che permette l’accesso ad un oggetto tramite uno specifico “contenitore”. Questo “passaggio” trova la sua concretizzazione, appunto, nella classe Facade. Di conseguenza, quando dovrai creare le tue Facade in futuro sarà proprio questo il punto di partenza.  Le facade di Laravel, è qualsiasi facade personalizzata che crei, dovranno estendere la classe di base `Facade`.

Una classe `Facade` ha bisogno solo di implementare un singolo metodo: `getFacadeAccessor`. Proprio questo metodo, infatti, definisce quello che viene poi “risolto” all’interno del container. 
La classe di base `Facade`, infatti, fa largamente uso del metodo magico `__callStatic()` per la gestione delle varie chiamate.

Quindi, nel momento in cui effettui una chiamata ad una facade come `Cache::get`, Laravel “risolve” la classe che gestisce la Cache al di fuori dell' IoC container ed effettua la chiamata al metodo `get` della classe. In termini tecnici, le facade di Laravel rappresentano una sintassi conventiente per usare l'IoC container come service locator.

<a name="uso-pratico"></a>
## Uso Pratico

Nell'esempio qui di seguito, si effettua una chiamata al sistema cache di Laravel. Guardando questo codice, si potrebbe assumere che il metodo statico `get` venga chiamato dalla classe `Cache`.

	$value = Cache::get('key');

Tuttavia, se diamo un occhiata alla classe `Illuminate\Support\Facades\Cache`, vedrai che non esiste nessun metodo `get` al suo interno:

	class Cache extends Facade {

		/**
		 * Get the registered name of the component.
		 *
		 * @return string
		 */
		protected static function getFacadeAccessor() { return 'cache'; }

	}

La classe Cache estende la classe di base `Facade` e definisce un metodo `getFacadeAccessor()`. Ricorda, il lavoro di questo metodo è di restituire il nome del Binding del IoC.

In poche parole, quando qualcuno richiama un metodo statico della facade `Cache`, Laravel “risolve” il binding `cache` dall'IoC container, ed esegue il metodo richiesto (in questo caso, `get`) di questo specifico oggetto.

Quindi, la nostra chiamata `Cache::get` potrebbe essere riscritta come segue:

	$value = $app->make('cache')->get('key');

#### Importare Facade

Ricorda, se stai usando una facade in un controller sotto uno specifico namespace, hai bisogno di importare la classe facade all'interno di questo namespace. Tutte le facade si trovano in un global namespace:

	<?php namespace App\Http\Controllers;

	use Cache;

	class PhotosController extends Controller {

		/**
		 * Get all of the application photos.
		 *
		 * @return Response
		 */
		public function index()
		{
			$photos = Cache::get('photos');

			//
		}

	}

<a name="creare-facade"></a>
## Creare Facade

Creare una facade per la tua applicazione o package è semplice. Hai bisogno soltanto di 3 cose in tutto:

- Un Binding IoC.
- Una classe facade.
- Un alias per la tua facade.

Guardiamo un esmepio. Qui, abbiamo definito una classe `PaymentGateway\Payment`.

	namespace PaymentGateway;

	class Payment {

		public function process()
		{
			//
		}

	}

Abbiamo bisogno che questa classe venga risolta dall'IoC container. Quindi, aggiungiamo un binding al service provider:

	App::bind('payment', function()
	{
		return new \PaymentGateway\Payment;
	});

Un buon modo per registrare questo binding sarebbe quello di creare un nuovo [service provider](/provider) chiamato `PaymentServiceProvider`,  e aggiungere questo binding al metodo `register`. Puoi quindi configurare Laravel in modo che carichi il tuo service provider dal file di configurazione `config/app.php`.

Successivamente, possiamo creare la nostra classe facade:

	use Illuminate\Support\Facades\Facade;

	class Payment extends Facade {

		protected static function getFacadeAccessor() { return 'payment'; }

	}

Finalmente, puoi aggiungere, se lo desideri, un alias per la nostra facade nell'array `aliases` nel file di configurazione `config/app.php`. Ora, possiamo effettuare chiamate al metodo `process` sull'istanza della classe `Payment`.

	Payment::process();

### Note Sul Caricamento Automatico Degli Alias
 
Le classi definite nell'array `aliases` non sono sempre disponibili in alcuni casi perchè il [PHP  non proverà a caricare delle classi non definite](https://bugs.php.net/bug.php?id=39003). Se `\ServiceWrapper\ApiTimeoutException` è un alias di `ApiTimeoutException`, un metodo `catch(ApiTimeoutException $e)` al di fuori del namespace `\ServiceWrapper`, non riuscirà mai ad intercettare questa eccezione se si verificherà. L'unica soluzione è quella di usare sempre l’istruzione use con le classi desiderate all’inizio del file sul quale si sta lavorando.

<a name="mocking-facade"></a>
## Mocking delle Facade

Gli unit test sono un aspetto importante del perchè le facade lavorano nel modo in cui lo fanno. Infatti, la testabilità è una ragione primaria della loro esistenza. Per maggiori informazioni, dai un'occhiata alla documentazione [mocking facades](/docs/testing#mocking-facades).

<a name="classi-facade-reference"></a>
## Le Classi Facade Reference

Qui di seguito trovi le varie Facades e le classi sottostanti collegate. Può essere una buona reference in caso di problemi e, quindi, per poter sapere quale classe andare ad analizzare.

Facade  |  Class  |  IoC Binding
------------- | ------------- | -------------
App  |  [Illuminate\Foundation\Application](http://laravel.com/api/5.0/Illuminate/Foundation/Application.html)  | `app`
Artisan  |  [Illuminate\Console\Application](http://laravel.com/api/5.0/Illuminate/Console/Application.html)  |  `artisan`
Auth  |  [Illuminate\Auth\AuthManager](http://laravel.com/api/5.0/Illuminate/Auth/AuthManager.html)  |  `auth`
Auth (Instance)  |  [Illuminate\Auth\Guard](http://laravel.com/api/5.0/Illuminate/Auth/Guard.html)  |
Blade  |  [Illuminate\View\Compilers\BladeCompiler](http://laravel.com/api/5.0/Illuminate/View/Compilers/BladeCompiler.html)  |  `blade.compiler`
Cache  |  [Illuminate\Cache\Repository](http://laravel.com/api/5.0/Illuminate/Cache/Repository.html)  |  `cache`
Config  |  [Illuminate\Config\Repository](http://laravel.com/api/5.0/Illuminate/Config/Repository.html)  |  `config`
Cookie  |  [Illuminate\Cookie\CookieJar](http://laravel.com/api/5.0/Illuminate/Cookie/CookieJar.html)  |  `cookie`
Crypt  |  [Illuminate\Encryption\Encrypter](http://laravel.com/api/5.0/Illuminate/Encryption/Encrypter.html)  |  `encrypter`
DB  |  [Illuminate\Database\DatabaseManager](http://laravel.com/api/5.0/Illuminate/Database/DatabaseManager.html)  |  `db`
DB (Instance)  |  [Illuminate\Database\Connection](http://laravel.com/api/5.0/Illuminate/Database/Connection.html)  |
Event  |  [Illuminate\Events\Dispatcher](http://laravel.com/api/5.0/Illuminate/Events/Dispatcher.html)  |  `events`
File  |  [Illuminate\Filesystem\Filesystem](http://laravel.com/api/5.0/Illuminate/Filesystem/Filesystem.html)  |  `files`
Form  |  [Illuminate\Html\FormBuilder](http://laravel.com/api/5.0/Illuminate/Html/FormBuilder.html)  |  `form`
Hash  |  [Illuminate\Hashing\HasherInterface](http://laravel.com/api/5.0/Illuminate/Hashing/HasherInterface.html)  |  `hash`
HTML  |  [Illuminate\Html\HtmlBuilder](http://laravel.com/api/5.0/Illuminate/Html/HtmlBuilder.html)  |  `html`
Input  |  [Illuminate\Http\Request](http://laravel.com/api/5.0/Illuminate/Http/Request.html)  |  `request`
Lang  |  [Illuminate\Translation\Translator](http://laravel.com/api/5.0/Illuminate/Translation/Translator.html)  |  `translator`
Log  |  [Illuminate\Log\Writer](http://laravel.com/api/5.0/Illuminate/Log/Writer.html)  |  `log`
Mail  |  [Illuminate\Mail\Mailer](http://laravel.com/api/5.0/Illuminate/Mail/Mailer.html)  |  `mailer`
Paginator  |  [Illuminate\Pagination\Factory](http://laravel.com/api/5.0/Illuminate/Pagination/Factory.html)  |  `paginator`
Paginator (Instance)  |  [Illuminate\Pagination\Paginator](http://laravel.com/api/5.0/Illuminate/Pagination/Paginator.html)  |
Password  |  [Illuminate\Auth\Reminders\PasswordBroker](http://laravel.com/api/5.0/Illuminate/Auth/Reminders/PasswordBroker.html)  |  `auth.reminder`
Queue  |  [Illuminate\Queue\QueueManager](http://laravel.com/api/5.0/Illuminate/Queue/QueueManager.html)  |  `queue`
Queue (Instance) |  [Illuminate\Queue\QueueInterface](http://laravel.com/api/5.0/Illuminate/Queue/QueueInterface.html)  |
Queue (Base Class) |  [Illuminate\Queue\Queue](http://laravel.com/api/5.0/Illuminate/Queue/Queue.html)  |
Redirect  |  [Illuminate\Routing\Redirector](http://laravel.com/api/5.0/Illuminate/Routing/Redirector.html)  |  `redirect`
Redis  |  [Illuminate\Redis\Database](http://laravel.com/api/5.0/Illuminate/Redis/Database.html)  |  `redis`
Request  |  [Illuminate\Http\Request](http://laravel.com/api/5.0/Illuminate/Http/Request.html)  |  `request`
Response  |  [Illuminate\Support\Facades\Response](http://laravel.com/api/5.0/Illuminate/Support/Facades/Response.html)  |
Route  |  [Illuminate\Routing\Router](http://laravel.com/api/5.0/Illuminate/Routing/Router.html)  |  `router`
Schema  |  [Illuminate\Database\Schema\Blueprint](http://laravel.com/api/5.0/Illuminate/Database/Schema/Blueprint.html)  |
Session  |  [Illuminate\Session\SessionManager](http://laravel.com/api/5.0/Illuminate/Session/SessionManager.html)
  |  `session`
Session (Instance)  |  [Illuminate\Session\Store](http://laravel.com/api/5.0/Illuminate/Session/Store.html)  |
SSH  |  [Illuminate\Remote\RemoteManager](http://laravel.com/api/5.0/Illuminate/Remote/RemoteManager.html)  |  `remote`
SSH (Instance)  |  [Illuminate\Remote\Connection](http://laravel.com/api/5.0/Illuminate/Remote/Connection.html)  |
URL  |  [Illuminate\Routing\UrlGenerator](http://laravel.com/api/5.0/Illuminate/Routing/UrlGenerator.html)  |  `url`
Validator  |  [Illuminate\Validation\Factory](http://laravel.com/api/5.0/Illuminate/Validation/Factory.html)  |  `validator`
Validator (Instance)  |  [Illuminate\Validation\Validator](http://laravel.com/api/5.0/Illuminate/Validation/Validator.html) |
View  |  [Illuminate\View\Factory](http://laravel.com/api/5.0/Illuminate/View/Factory.html)  |  `view`
View (Instance)  |  [Illuminate\View\View](http://laravel.com/api/5.0/Illuminate/View/View.html)  |
