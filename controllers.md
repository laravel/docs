# HTTP Controllers

- [Introduzione](#introduzione)
- [Controller Base](#controller-base)
- [Middleware nei Controller](#middleware-controller)
- [Controller RESTful](#controller-restful)
	- [Definire una Parte delle Route](#definire-parte-route)
	- [Dare dei Nomi alle Route](#dare-nomi-route)
	- [Risorse Annidate](#risorse-annidate)
	- [Aggiungere Metodi ad un Controller Risorsa](#aggiungere-metodi-controller-risorsa)
- [Controller Impliciti](#controller-impliciti)
- [Dependency Injection e Controller](#dependency-injection-controller)
- [Route Caching](#route-caching)

<a name="introduzione"></a>
## Introduzione

Anzichè definire tutte le tue logiche all'interno di un singolo file _routes.php_, una buona mossa potrebbe essere l'organizzare tutto usando dei controller. I controller possono infatti occuparsi di "raggruppare" adeguatamente determinate logiche all'interno di una classe. Normalmente, puoi trovarli all'interno della cartella _app/Http/Controllers_.

<a name="controller-base"></a>
## Controller Base

Ecco un esempio di controller. Tutti i controller, di default, dovrebbero estendere quello base incluso nell'installazione di Laravel.

	<?php namespace App\Http\Controllers;

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
			return view('user.profile', ['user' => User::findOrFail($id)]);
		}
	}

Possiamo quindi "instradare" la richiesta ad un metodo specifico del controller così:

	Route::get('user/{id}', 'UserController@showProfile');

La notazione è semplice: quando viene riconosciuta la sintassi specificata in _Route::get()_, viene richiamato il metodo _showProfile_ del controller _UserController_, indicato come secondo argomento. Eventuali parametri verranno automaticamente riconosciuti e passati.

#### Controller e Namespace

Molto importante è notare che non abbiamo specificato il nome del controller nella sua "interezza", cioè considerando anche il suo namespace, durante la definizione della route. Abbiamo solamente definito il nome del controller, tralasciando `App\Http\Controllers`. Perché? Di default, _RouteServiceProvider_ carica le route in _routes.php_ di default tenendo conto del namespace dei controller. Questo per una maggiore comodità.

Nulla ti vieta di organizzare i tuoi controller in modo più complesso. Supponendo che tu abbia deciso di inserire un controller _AdminController_ in _Photos_, la registrazione avverrebbe come segue:

	Route::get('foo', 'Photos\AdminController@method');

#### Dare dei Nomi alle Route dei Controller

Come vale anche per le semplici route, puoi dare un nome ad una route che collega un percorso ad un metodo di un controller tramite _as_.

	Route::get('foo', ['uses' => 'FooController@method', 'as' => 'name']);

Una volta assegnato il nome alla route, puoi generare con estrema semplicità l'url rispettivo. Uno dei modi di farlo è il metodo helper _action_.

	$url = action('FooController@method');

<a name="middleware-controller"></a>
## Middleware nei Controller

Se hai bisogno di assegnare un [Middleware](/docs/{{5.1}}/middleware) ad una route di un controller puoi fare così:

	Route::get('profile', [
		'middleware' => 'auth',
		'uses' => 'UserController@showProfile'
	]);

Tuttavia, può essere molto più conveniente specificare il middleware nel costruttore del controller stesso. Il metodo da usare è _middleware_, come segue:

	class UserController extends Controller
	{
		/**
		 * Instantiate a new UserController instance.
		 *
		 * @return void
		 */
		public function __construct()
		{
			$this->middleware('auth');

			$this->middleware('log', ['only' => ['fooAction', 'barAction']]);

			$this->middleware('subscribed', ['except' => ['fooAction', 'barAction']]);
		}
	}

Tramite _except_ e _only_ puoi assegnare uno specifico middleware solo ad alcuni metodi.

<a name="controller-restful"></a>
## Controller RESTful

I _resource_ controller sono ottimi per costruire senza troppi problemi delle strutture RESTful intorno ad una risorsa. Ad esempio, potresti voler creare un controller che gestice le richieste inerenti le foto memorizzate dalla tua applicazione. Tramite il comando _make:controller_ di Artisan puoi creare velocemente la classe di cui hai bisogno.

	php artisan make:controller PhotoController

Il comando genererà il file `app/Http/Controllers/PhotoController.php`. Tale controller inoltre conterrà un metodo per ognuna delle operazioni da effettuare.

Per concludere, non bisogna fare altro che assegnare il controller alle sue specifiche route tramite:

	Route::resource('photo', 'PhotoController');

Interessante notare che nella dichiarazione appena vista vengono automaticamente create svariate route corrispondenti alle varie operazioni da effettuare. Nella seguente tabella puoi trovare più informazioni sui metodi creati e sulle action contemplate.

#### Action gestite da un Resource Controller

Verb      | Path                  | Action       | Route Name
----------|-----------------------|--------------|---------------------
GET       | `/photo`              | index        | photo.index
GET       | `/photo/create`       | create       | photo.create
POST      | `/photo`              | store        | photo.store
GET       | `/photo/{photo}`      | show         | photo.show
GET       | `/photo/{photo}/edit` | edit         | photo.edit
PUT/PATCH | `/photo/{photo}`      | update       | photo.update
DELETE    | `/photo/{photo}`      | destroy      | photo.destroy

<a name="definire-parte-route"></a>
#### Definire una Parte delle Route

Quando dichiari una route ad un controller risorsa, puoi decidere anche di definire un subset specifico di azioni.

	Route::resource('photo', 'PhotoController',
					['only' => ['index', 'show']]);

	Route::resource('photo', 'PhotoController',
					['except' => ['create', 'store', 'update', 'destroy']]);

<a name="dare-nomi-route"></a>
#### Dare dei Nomi alle Route

Di default, tutte le action di un controller risorsa hanno una route predefinita. Tuttavia, se preferisci, puoi sovrascrivere le impostazioni di default con altre più adeguate alla situazione.

	Route::resource('photo', 'PhotoController',
					['names' => ['create' => 'photo.build']]);

<a name="risorse-annidate"></a>
#### Risorse Annidate

A volte potresti avere la necessità di definire delle route ad una risorsa "annidata". Ad esempio, una risorsa foto potrebbe averne un'altra "commento" correlata. Per effettuare un'operazione di annidamento, basta usarel la dot notation come segue.

	Route::resource('photos.comments', 'PhotoCommentController');

Tale route registrerà una risorsa annidata che potrà essere raggiunta tramite un url simile a : `photos/{photos}/comments/{comments}`.

	<?php namespace App\Http\Controllers;

	use App\Http\Controllers\Controller;

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

<a name="aggiungere-metodi-controller-risorsa"></a>
#### Aggiungere Metodi ad un Controller Risorsa

Nel caso in cui volessi aggiungere delle funzionalità aggiuntive ad un controller risorsa, dovrai definire le relative route separatamente. In ogni caso, ricordati di metterle **prima** della chiamata al metodo _Route::resource_.

	Route::get('photos/popular', 'PhotoController@method');
	Route::resource('photos', 'PhotoController');

<a name="controller-impliciti"></a>
## Controller Impliciti

Laravel ti permette, inoltre, di definire le route relative a tutte le action presenti in una classe con una sola chiamata. Nello specifico, il metodo ad essere chiamato è _Route::controller_. I parametri accettati sono due: l'URI base che sarà collegata ai metodi ed il controller desiderato.

	Route::controller('users', 'UserController');

A quel punto non devi fare altro che aggiungere i metodi di cui hai bisogno, il cui nome comincerà sempre con il verbo HTTP di riferimento e quindi il titolo, in questo modo:

 	<?php namespace App\Http\Controllers;

	class UserController extends Controller
	{
		/**
		 * Responds to requests to GET /users
		 */
		public function getIndex()
		{
			//
		}

		/**
		 * Responds to requests to GET /users/show/1
		 */
		public function getShow($id)
		{
			//
		}

		/**
		 * Responds to requests to GET /users/admin-profile
		 */
		public function getAdminProfile()
		{
			//
		}

		/**
		 * Responds to requests to POST /users/profile
		 */
		public function postProfile()
		{
			//
		}
	}

Come puoi inoltre notare dall'esempio qui in alto, il metodo _index_ risponde alla root URI del controller. In questo caso, semplicemente, _users_.

#### Assegnare i Nomi alle Route

Nel caso in cui tu voglia [assegnare dei nomi](/docs/5.1/routing#route-rinominate) ad alcune delle route assegnate ad un controller implicito, puoi passare un array di nomi come terzo parametro del metodo _controller_.

	Route::controller('users', 'UserController', [
		'getShow' => 'user.show',
	]);

<a name="dependency-injection-controller"></a>
## Dependency Injection e Controller

#### Constructor Injection

Il [service container](/docs/5.1/container) di Laravel viene usato per risolvere tutti i controller della tua applicazione. Di conseguenza, volendo puoi specificare delle dipendenze tramite type-hint come argomenti del costruttore. Le dipendenze verranno automaticamente risolte ed iniettate nell'istanza risultante:

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use App\Repositories\UserRepository;

	class UserController extends Controller
	{
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

Ovviamente, puoi anche effettuare il type-hint di un [Laravel contract](/docs/5.1/contracts). Basta che il container sia capace di risolverlo.

#### Method Injection

In aggiunta alla constructor injection, in un controller puoi anche specificare le dipendenze nelle varie action, dove necessario. Nell'esempio di seguito puoi vedere un type-hint di un'istanza della classe `Illuminate\Http\Request` direttamente in un metodo:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller
	{
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

Nel caso in cui il metodo preveda dei parametri, specificali dopo le dipendenze.

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller
	{
		/**
		 * Update the specified user.
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

<a name="route-caching"></a>
## Route Caching

Se la tua applicazione usa le controller route in modo piuttosto estensivo, potresti trovare un bel vantaggio nell'uso della route cache. In questo modo, usando questo "tramite", abbatterai i tempi di registrazione delle varie route per ogni chiamata. In alcuni casi, la registrazione delle route può arrivare ad essere cento volte più veloce!

Tutto quello che devi fare è usare il comando Artisan _route:cache_.

	php artisan route:cache

Niente di più. Al posto di _app/Http/routes.php_ verrà usato, adesso, un file compilato intermedio. Ricorda però di eseguire nuovamente il comando se aggiungi altre route al tuo file. Una buona norma può essere quella di eseguirlo solo quando stai per effettuare il deploy.

Per rimuovere il file cache senza generarne uno nuovo, usa _route:clear_:

	php artisan route:clear
