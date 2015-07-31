# Facade

- [Introduzione](#introduzione)
- [Uso di Facade](#uso-facade)
- [Reference Classi Facade](#reference-classi-facade)

<a name="introduzione"></a>
## Introduzione

Il sistema di Facade offre un interfaccia "statica" a tutte le classi disponibili attraverso il [service container](/docs/5.1/container). Laravel conta già diverse facade pronte all'uso, e probabilmente le hai usate senza neanche saperlo. Le Facade di Laravel fanno da proxy per le classi "sottostanti" presenti nell'IoC Container, dando allo sviluppatore la possibilità di usare una sintassi espressiva ma mantenendo, allo stesso tempo, la flessibilità e la testabilità che con un metodo statico non si può ottenere. 

<a name="uso-facade"></a>
## Uso di Facade

Nel contesto di applicazioni Laravel, una facade è una classe che offre l'accesso ad un oggeto tramite uno specifico “contenitore”. Questo “passaggio” trova la sua concretizzazione, appunto, nella classe Facade. Le facade di Laravel, e qualsiai altra facade personalizzata che crei, dovranno estendere la classe base `Illuminate\Support\Facades\Facade`.

Una classe facade ha solo bisogno di implementare un singolo metodo: `getFacadeAccessor`. E' compito del metodo `getFacadeAccessor` infatti, definisce quello che viene poi “risolto” all’interno del container. La classe di base `Facade` fa largamente uso del metodo magico `__callStatic()` per la gestione delle varie chiamate.

Nell'esempio sotto, viene eseguita una chiamata al sistema di cache di Laravel. Guardando il codice, si potrebbe pensare che il metodo statico `get` venga chiamato dalla classe `Cache`:

	<?php namespace App\Http\Controllers;

	use Cache;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Show the profile for the given user.
		 *
		 * @param  int  $id
		 * @return Response
		 */
		public function showProfile($id)
		{
			$user = Cache::get('user:'.$id');

			return view('profile', ['user' => $user]);
		}
	}
Nota come all'inizio del file abbiamo "importato" la facade `Cache`. Questa facade funge da proxy per accedere all'implementazione dell'interfaccia`Illuminate\Contracts\Cache\Factory`. Qualsiasi chiamata esegui usando la facade sarà passata all'istanza della cache di Laravel.

Se diamo uno sguardo alla classe `Illuminate\Support\Facades\Cache`, vedrai che non è presente nessun metodo statico `get`:

	class Cache extends Facade {

		/**
		 * Get the registered name of the component.
		 *
		 * @return string
		 */
		protected static function getFacadeAccessor() { return 'cache'; }

	}

Invece, la facade `Cache` estende la classe base `Facade` e viene definito il metodo `getFacadeAccessor()`. Ricorda, la funzione di questo metodo è quella di ritornare il nome del binding dal service container. Quando un utente referenzia qualsiasi metodo statico sulla facade `Cache`, Laravel risolte il binding `cache` dal  [service container](/docs/5.1/container) ed esegue il metodo richiesto (in questo caso, `get`) di questo specifico oggetto.

<a name="reference-classi-facade"></a>
## Reference Classi Facade

Qui di seguito trovi le varie Facades e le classi sottostanti collegate. Può essere una buona reference in caso di problemi e, quindi, per poter sapere quale classe andare ad analizzare. E' inclusa anche la chiave del [binding del service container](/docs/5.1/container) dove applicabile.

La leggenda per leggere queste informazioni è, in sequenza:

* Facade;
* Classe;
* Binding del Service Container;

* App  |  [Illuminate\Foundation\Application](http://laravel.com/api/{{version}}/Illuminate/Foundation/Application.html)  | `app`
* Artisan  |  [Illuminate\Console\Application](http://laravel.com/api/{{version}}/Illuminate/Console/Application.html)  |  `artisan`
* Auth  |  [Illuminate\Auth\AuthManager](http://laravel.com/api/{{version}}/Illuminate/Auth/AuthManager.html)  |  `auth`
* Auth (Instance)  |  [Illuminate\Auth\Guard](http://laravel.com/api/{{version}}/Illuminate/Auth/Guard.html)  |
* Blade  |  [Illuminate\View\Compilers\BladeCompiler](http://laravel.com/api/{{version}}/Illuminate/View/Compilers/BladeCompiler.html)  |  `blade.compiler`
* Bus  |  [Illuminate\Contracts\Bus\Dispatcher](http://laravel.com/api/{{version}}/Illuminate/Contracts/Bus/Dispatcher.html)  |
* Cache  |  [Illuminate\Cache\Repository](http://laravel.com/api/{{version}}/Illuminate/Cache/Repository.html)  |  `cache`
* Config  |  [Illuminate\Config\Repository](http://laravel.com/api/{{version}}/Illuminate/Config/Repository.html)  |  `config`
* Cookie  |  [Illuminate\Cookie\CookieJar](http://laravel.com/api/{{version}}/Illuminate/Cookie/CookieJar.html)  |  `cookie`
* Crypt  |  [Illuminate\Encryption\Encrypter](http://laravel.com/api/{{version}}/Illuminate/Encryption/Encrypter.html)  |  `encrypter`
* DB  |  [Illuminate\Database\DatabaseManager](http://laravel.com/api/{{version}}/Illuminate/Database/DatabaseManager.html)  |  `db`
* DB (Instance)  |  [Illuminate\Database\Connection](http://laravel.com/api/{{version}}/Illuminate/Database/Connection.html)  |
* Event  |  [Illuminate\Events\Dispatcher](http://laravel.com/api/{{version}}/Illuminate/Events/Dispatcher.html)  |  `events`
* File  |  [Illuminate\Filesystem\Filesystem](http://laravel.com/api/{{version}}/Illuminate/Filesystem/Filesystem.html)  |  `files`
* Hash  |  [Illuminate\Contracts\Hashing\Hasher](http://laravel.com/api/{{version}}/Illuminate/Contracts/Hashing/Hasher.html)  |  `hash`
* Input  |  [Illuminate\Http\Request](http://laravel.com/api/{{version}}/Illuminate/Http/Request.html)  |  `request`
* Lang  |  [Illuminate\Translation\Translator](http://laravel.com/api/{{version}}/Illuminate/Translation/Translator.html)  |  `translator`
* Log  |  [Illuminate\Log\Writer](http://laravel.com/api/{{version}}/Illuminate/Log/Writer.html)  |  `log`
* Mail  |  [Illuminate\Mail\Mailer](http://laravel.com/api/{{version}}/Illuminate/Mail/Mailer.html)  |  `mailer`
* Password  |  [Illuminate\Auth\Passwords\PasswordBroker](http://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBroker.html)  |  `auth.password`
* Queue  |  [Illuminate\Queue\QueueManager](http://laravel.com/api/{{version}}/Illuminate/Queue/QueueManager.html)  |  `queue`
* Queue (Instance) |  [Illuminate\Queue\QueueInterface](http://laravel.com/api/{{version}}/Illuminate/Queue/QueueInterface.html)  |
* Queue (Base Class) |  [Illuminate\Queue\Queue](http://laravel.com/api/{{version}}/Illuminate/Queue/Queue.html)  |
* Redirect  |  [Illuminate\Routing\Redirector](http://laravel.com/api/{{version}}/Illuminate/Routing/Redirector.html)  |  `redirect`
* Redis  |  [Illuminate\Redis\Database](http://laravel.com/api/{{version}}/Illuminate/Redis/Database.html)  |  `redis`
* Request  |  [Illuminate\Http\Request](http://laravel.com/api/{{version}}/Illuminate/Http/Request.html)  |  `request`
* Response  |  [Illuminate\Contracts\Routing\ResponseFactory](http://laravel.com/api/{{version}}/Illuminate/Contracts/Routing/ResponseFactory.html)  |
* Route  |  [Illuminate\Routing\Router](http://laravel.com/api/{{version}}/Illuminate/Routing/Router.html)  |  `router`
* Schema  |  [Illuminate\Database\Schema\Blueprint](http://laravel.com/api/{{version}}/Illuminate/Database/Schema/Blueprint.html)  |
* Session  |  [Illuminate\Session\SessionManager](http://laravel.com/api/{{version}}/Illuminate/Session/SessionManager.html)  |  `session`
* Session (Instance)  |  [Illuminate\Session\Store](http://laravel.com/api/{{version}}/Illuminate/Session/Store.html)  |
* Storage  |  [Illuminate\Contracts\Filesystem\Factory](http://laravel.com/api/{{version}}/Illuminate/Contracts/Filesystem/Factory.html)  |  `filesystem`
* URL  |  [Illuminate\Routing\UrlGenerator](http://laravel.com/api/{{version}}/Illuminate/Routing/UrlGenerator.html)  |  `url`
* Validator  |  [Illuminate\Validation\Factory](http://laravel.com/api/{{version}}/Illuminate/Validation/Factory.html)  |  `validator`
* Validator (Instance)  |  [Illuminate\Validation\Validator](http://laravel.com/api/{{version}}/Illuminate/Validation/Validator.html) |
* View  |  [Illuminate\View\Factory](http://laravel.com/api/{{version}}/Illuminate/View/Factory.html)  |  `view`
* View (Instance)  |  [Illuminate\View\View](http://laravel.com/api/{{version}}/Illuminate/View/View.html)  |
