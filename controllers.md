# Controller HTTP

- [Introduzione](#introduzione)
- [Controller Basilari](#controller-basilari)
- [Controller Middleware](#controller-middleware)
- [Controllers Resource RESTful](#controller-resource-restful)
- [Dependency Injection & Controller](#dependency-injection-e-controller)
- [Route Caching](#route-caching)

<a name="introduzione"></a>
## Introduzione

Invece di definire tutta la logica con le routes, in un unico file `routes.php`, potresti voler organizzare il comportamento della tua applicazione usando i Controller. I Controller possono raggruppare tutta la logica a livello di percorso in una classe sola. I Controller sono in genere salvati all'interno della directory `app/Http/Controllers`.

<a name="controller-basilari"></a>
## Controller Basilari

Ecco un esempio di una classe controller di base:

	<?php namespace App\Http\Controllers;

	use App\Http\Controllers\Controller;

	class UserController extends Controller {

		/**
		 * Show the profile for the given user.
		 *
		 * @param  int  $id
		 * @return Response
		 */
		public function showProfile($id)
		{
			return view('user.profile', ['user' => User::findOrFail($id)]);
		}

	}

Possiamo creare un percorso per un'action di un controller in questo modo:

	Route::get('user/{id}', 'UserController@showProfile');

> **Nota:** Tutti i controller dovrebbero ereditare la classe controller di base.

#### Controller & Namespace

E' molto importante notare che non abbiamo bisogno di specificare il namespace completo del controller, ma solo la porzione del nome della classe che viene dopo il namespace “route” `App\Http\Controllers`. Di default, `RouteServiceProvider` caricherà il file `routes.php` con un gruppo di route contenente il namespace principale.

Se scegli di nidificare oppure organizzare i tuoi controller usando i namespace PHP all'interno della directory App\Http\Controllers`, è sufficiente specificare il nome della classe rispetto al namespace principale `App\Http\Controllers`. Quindi, se il namespace completo del tuo controller è `App\Http\Controllers\Photos\AdminController`, dovrai registrare la route in questo modo:

	Route::get('foo', 'Photos\AdminController@method');

#### Controller Route Nominate

Come le route Clousure, puoi specificare un nome alle route dei controller:

	Route::get('foo', ['uses' => 'FooController@method', 'as' => 'name']);

#### URL Da Azioni del Controller

Per generare un URL da un'azione di un controller, usa il metodo helper `action`:

	$url = action('App\Http\Controllers\FooController@method');

Se preferisci generare un URL da un'azione del controller usando solo la porzione del nome della classe rispetto al namespace del tuo controller, registra il namespace principale del controller con il generatore URL:

	URL::setRootControllerNamespace('App\Http\Controllers');

	$url = action('FooController@method');

Puoi accedere al nome dell’azione del controller in fase di esecuzione utilizzando il metodo `currentRouteAction`:

	$action = Route::currentRouteAction();

<a name="controller-middleware"></a>
## Controller Middleware

I [Middleware](/docs/master/middleware) possono essere specificati nella route del controller in questo modo:

	Route::get('profile', [
		'middleware' => 'auth',
		'uses' => 'UserController@showProfile'
	]);

Inoltre, puoi specificare il middleware all'interno del costruttore del controller:

	class UserController extends Controller {

		/**
		 * Instantiate a new UserController instance.
		 */
		public function __construct()
		{
			$this->middleware('auth');

			$this->middleware('log', ['only' => ['fooAction', 'barAction']]);

			$this->middleware('subscribed', ['except' => ['fooAction', 'barAction']]);
		}

	}

<a name="controller-resource-restful"></a>
## Controller Resource RESTful

I controller resource permettono senza difficoltà la creazione di controller RESTful delle risorse. Per esempio, potresti aver bisogno di creare un controller che gestisca le “Foto” memorizzate dall’applicazione. Usando il comando Artisan `make:controller` puoi rapidamente creare un tale controller:

	php artisan make:controller PhotoController

Ora puoi creare un percorso al controller:

	Route::resource('photo', 'PhotoController');

Questa unica dichiarazione crea percorsi multipli per gestire una serie di azioni RESTful sulla risorsa “Foto”. Allo stesso modo, il controller generato avrà già un metodo per ognuna di queste azioni con delle note che informano che URI e che verbi trattano.

#### Azioni Gestite Dal Controller Delle Risorse

Verb      | Path                        | Action       | Route Name
----------|-----------------------------|--------------|---------------------
GET       | /resource                   | index        | resource.index
GET       | /resource/create            | create       | resource.create
POST      | /resource                   | store        | resource.store
GET       | /resource/{resource}        | show         | resource.show
GET       | /resource/{resource}/edit   | edit         | resource.edit
PUT/PATCH | /resource/{resource}        | update       | resource.update
DELETE    | /resource/{resource}        | destroy      | resource.destroy

#### Personalizzare Resource Routes

Puoi inoltre specificare un insieme di azioni per gestire il percorso:

	Route::resource('photo', 'PhotoController',
					['only' => ['index', 'show']]);

	Route::resource('photo', 'PhotoController',
					['except' => ['create', 'store', 'update', 'destroy']]);

Di default, tutti i controller resource hanno una route nominata; comunque, puoi sovrascrivere questi nomi passando all'array `names` le tue opzioni:

	Route::resource('photo', 'PhotoController',
					['names' => ['create' => 'photo.build']]);

#### Gestione Controller Resource Nidificati

Per “nidificare” controller resource, usa la notazione “punto” nella dichiarazione della tua route:

	Route::resource('photos.comments', 'PhotoCommentController');

Questa route registrerà una risorsa “nidificata” alla quale si può accedere tramite un URL come il seguente:
`photos/{photos}/comments/{comments}`.

	class PhotoCommentController extends Controller {

		/**
		 * Show the specified photo comment.
		 *
		 * @param  int  $photoId
		 * @param  int  $commentId
		 * @return Response
		 */
		public function show($photoId, $commentId)
		{
			//
		}

	}

#### Aggiungere Una Route Aggiuntiva Al Controller Resource

Se fosse necessario aggiungere una route aggiuntiva al controller resource oltre alle risorse di default, potresti definire questi percorsi prima della chiamata a `Route::resource`:

	Route::get('photos/popular');

	Route::resource('photos', 'PhotoController');

<a name="dependency-injection-e-controller"></a>
## Dependency Injection & Controller

#### Constructor Injection

Il [service container](/docs/master/container) di Laravel è usato per risolvere tutti i controller di Laravel. Come risultato, sei in grado di inserire qualsiasi dipendenza che il tuo controller abbia bisogno nel suo construct:

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use App\Repositories\UserRepository;

	class UserController extends Controller {

		/**
		 * The user repository instance.
		 */
		protected $users;

		/**
		 * Create a new controller instance.
		 *
		 * @param  UserRepository  $users
		 * @return void
		 */
		public function __construct(UserRepository $users)
		{
			$this->users = $users;
		}

	}

Ovviamente, puoi anche inserire qualsiasi [Laravel contract](/docs/master/contracts). Se il container può risolverla, puoi aggiungerla.

#### Metodi Di Injection

Oltre all'injection nel costruttore, puoi anche inserire le dipendenze nei metodi del tuo controller. Per esempio, inseriamo l'istanza `Request` in uno dei nostri metodi:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller {

		/**
		 * Store a new user.
		 *
		 * @param  Request  $request
		 * @return Response
		 */
		public function store(Request $request)
		{
			$name = $request->input('name');

			//
		}

	}

Se il metodo del tuo controller deve ricevere degli input da un parametro di una route, inserisci semplicemente i tuoi parametri dopo le altre dipendenze:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller {

		/**
		 * Store a new user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function update(Request $request, $id)
		{
			//
		}

	}

> **Nota:** Il metodo di injection è completamente compatibile con il [model  binding](/docs/master/routing#route-model-binding). Il container determinerà in maniera opportuna quali parametri sono vincolati al model e quali invece devono essere iniettati.

<a name="route-caching"></a>
## Route Caching

Se la tua applicazione usa esclusivamente route controller, puoi trarne vantaggio dalla cache route di Laravel. Usando la cache route verrà drasticamento diminuito il tempo per la registrazione di tutte le route dell'applicazione. In alcuni casi, la registrazione può anche essere 100 volte più veloce! Per generare una cache route, basta eseguire il comando Artisan `route:cache`

	php artisan route:cache

Questo è tutto quello che c'è da fare! Il tuo file di cache route verrà usato al posto del file `app/Http/routes.php`. Ricorda, se vuoi aggiungere qualsiasi altra route hai bisogno di rigenerare una nuova cache route. Per questo, hai bisogno di usare solo il comando `route:cache` durante lo sviluppo del tuo progetto.

Per rimuovere il file con le cache route senza generare una nuova cache, usa il comando `route:clear`:

	php artisan route:clear
