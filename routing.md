# Routing

- [Routing di Base](#routing-base)
- [Protezione CSRF](#protezione-csrf)
- [Method Spoofing](#method-spoofing)
- [Route e Parametri](#route-parametri)
- [Named Route](#named-route)
- [Gruppi di Route](#gruppi-route)
- [Binding di una Route con un Model](#binding-route-model)
- [Errori 404](#errori-404)

<a name="routing-base"></a>
## Routing di Base

Potrai definire la maggior parte delle route della tua applicazione nel file _app/Http/routes._, che viene caricato dalla classe `App\Providers\RouteServiceProvider`. Nella sua forma più semplice, una route è essenzialmente composta da un URL ed una _Closure_ corrispondente.

#### Route GET Base

	Route::get('/', function()
	{
		return 'Hello World';
	});

#### Route POST, PUT e DELETE di Base

	Route::post('foo/bar', function()
	{
		return 'Hello World';
	});

	Route::put('foo/bar', function()
	{
		//
	});

	Route::delete('foo/bar', function()
	{
		//
	});

#### Registrare una Route per più di un HTTP Verb Contemporaneamente

	Route::match(['get', 'post'], '/', function()
	{
		return 'Hello World';
	});

#### Registrare una Route che Corrisponda ad ogni HTTP Verb

	Route::any('foo', function()
	{
		return 'Hello World';
	});

Spesso ti ritroverai a dover generare l'URL di una certa route. Usa l'helper _url_:

	$url = url('foo');

<a name="protezione-csrf"></a>
## Protezione CSRF

Laravel fornisce, out of the box, un metodo molto semplice per proteggere la tua applicazione da attacchi di tipo [cross-site request forgery](http://en.wikipedia.org/wiki/Cross-site_request_forgery). Si tratta di un tipo di exploit particolarmente usato per eseguire operazioni normalmente non autorizzate su un'applicazione.

Di default, Laravel genera automaticamente un token per ogni sessione gestita dall'applicazione. Tale token può essere usato per verificare che effettivamente l'utente autenticato sia quello che sta effettuando la richiesta in questione.

#### Inserire un Token CSRF dentro un Form

    <input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">

Non dovrai mai verificare manualmente un token: di default, infatti, il middleware _VerifyCsrfToken_ farà tutto al posto tuo, senza lasciarti nessun disturbo.

In aggiunta, il middleware cercherà anche un eventuale _X-XSRF-TOKEN_.

<a name="method-spoofing"></a>
## Method Spoofing

I form HTML non supportano gli HTTP Verb _PUT_ e _DELETE_. Potresti però avere la necessità di effettuare una richiesta specifica usando proprio questi Verb... come fare? Laravel riconosce automaticamente che HTTP Verb usare se viene specificato un campo *_method* in un form. Ad esempio:

	<form action="/foo/bar" method="POST">
		<input type="hidden" name="_method" value="PUT">
    	<input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">
    </form>

<a name="route-parametri"></a>
## Route e Parametri

Ovviamente, puoi "catturare" i segmenti dei tuoi URI come fossero dei parametri. Anzi, Laravel li tratta esattamente come tali!

#### Passaggio Base di Parametri in una Route

	Route::get('user/{id}', function($id)
	{
		return 'User '.$id;
	});

#### Parametri Opzionali

	Route::get('user/{name?}', function($name = null)
	{
		return $name;
	});

#### Parametri Opzionali con un Valore di Default

	Route::get('user/{name?}', function($name = 'John')
	{
		return $name;
	});

#### Parametri che Rispettano una certa Regex

	Route::get('user/{name}', function($name)
	{
		//
	})
	->where('name', '[A-Za-z]+');

	Route::get('user/{id}', function($id)
	{
		//
	})
	->where('id', '[0-9]+');

#### Array di Condizioni (Regex) per Parametri

	Route::get('user/{id}/{name}', function($id, $name)
	{
		//
	})
	->where(['id' => '[0-9]+', 'name' => '[a-z]+'])

#### Definire Pattern Globali

Se preferisci, puoi specificare dei pattern globali per il riconoscimento di un certo tipo di parametro. Puoi definire questi pattern nel metodo _before_ del _RouteServiceProvider_.

	$router->pattern('id', '[0-9]+');

Una volta definito il pattern, questo viene applicato a tutte le route che usano tale parametro.

	Route::get('user/{id}', function($id)
	{
		// Viene chiamata solo se {id} è numerico come da Regex.
	});

#### Accedere ad un Valore di un Parametro

Se hai bisogno di accedere ad un valore di un parametro al di fuori di una route, puoi usare il metodo _input_:

	if ($route->input('id') == 1)
	{
		//
	}

Puoi anche accedere a questi valori tramite un'istanza della classe _Illuminate\Http\Request_. Tale istanza viene gestita tramite la Facade _Request_, o tramite il type-hinting di _Illuminate\Http\Request_ in caso di iniezione di dipendenza.

	use Illuminate\Http\Request;

	Route::get('user/{id}', function(Request $request, $id)
	{
		if ($request->route('id'))
		{
			//
		}
	});

<a name="named-route"></a>
## Named Route

Una named route ti permette di generare URL e redirect in modo molto più comodo. In poche parole, puoi specificare un "alias" per una route, tramite la chiave associativa _as_ in fase di definizione della route stessa.

Ecco un esempio:

	Route::get('user/profile', ['as' => 'profile', function()
	{
		//
	}]);

Lo stesso vale per le action di un controller:

	Route::get('user/profile', ['as' => 'profile', 'uses' => 'UserController@showProfile']);

A questo punto, puoi usare l'alias in caso di redirect o generazione di URL.

	$url = route('profile');

	$redirect = redirect()->route('profile');

Infine, il metodo _currentRouteName()_ ritorna il nome della route attuale.

	$name = Route::currentRouteName();

<a name="gruppi-route"></a>
## Gruppi di Route

A volte potresti avere bisogno di usare lo stesso filtro per tutta una serie di route che condividono "qualcosa". In tal caso, potresti usare un gruppo di route in questo modo:

	Route::group(['before' => 'auth'], function()
	{
		Route::get('/', function()
		{
			// Has Auth Filter
		});

		Route::get('user/profile', function()
		{
			// Has Auth Filter
		});
	});

Puoi anche usare il parametro _namespace_ per specificare il namespace di tutti i controller all'interno del gruppo in questione.

	Route::group(['namespace' => 'Admin'], function()
	{
		//
	});

> **Nota:** di default, il _RouteServiceProvider_ include il tuo file _routes.php_ senza un namespace, permettendoti quindi di registrare le route ai controller senza specificare di volta in volta il namespace completo. Tienilo a mente.

### Routing di Sotto-Dominio

Laravel gestisce tranquillamente anche un sistema di wildcard per i sottodomini.

#### Registrare una Route di Sotto-Dominio

	Route::group(['domain' => '{account}.myapp.com'], function()
	{

		Route::get('user/{id}', function($account, $id)
		{
			//
		});

	});

### Prefissi per le Route

Un gruppo di route può essere inoltre fornito di un prefisso comune tramite l'attributo _prefix_:

	Route::group(['prefix' => 'admin'], function()
	{

		Route::get('user', function()
		{
			//
		});

	});

<a name="binding-route-model"></a>
## Binding di una Route con un Model

I model di Laravel possono essere velocemente usati con una route. Ad esempio, al posto di "iniettare" l'id di un utente, puoi inserire un'intera istanza della classe _User_ per un dato ID.

Innanzitutto, si usa il metodo _model_ per specificare la classe da usare per un certo parametro. Questi binding vengono definiti nel metodo _boot_ di _RouteServiceProvider_.

#### Bind di un Parametro ad un Model

	public function boot(Router $router)
	{
		parent::boot($router);

		$router->model('user', 'App\User');
	}

Definiamo quindi una route che contiene un parametro _user_.

	Route::get('profile/{user}', function(App\User $user)
	{
		//
	});

Dal momento che abbiamo "legato" il parametro _user_ al model _App\User_, l'istanza di questo verrà automaticamente iniettata senza altre operazioni. Piuttosto comodo, considerando che una richiesta come _profile\1_ inietterà automaticamente un'istanza del model _User_ corrispondente a quella con l'ID pari ad 1.

> **Nota:** Se l'istanza cercata non viene trovata, viene lanciato un errore 404.

Nel caso in cui tu voglia inoltre specificare un comportamento particolare per un certo model in caso di istanza non trovata, puoi includere una _Closure_ come terzo parametro del metodo _model_ appena visto.

	Route::model('user', 'User', function()
	{
		throw new NotFoundHttpException;
	});

Se invece vuoi specificare tu stesso la logica di risoluzione devi usare il metodo _Router::bind_. La closure passata gestirà il valore ricevuto lasciando a te il comando completo. Chiaramente, il valore di ritorno deve essere un'istanza della classe specificata.

	Route::bind('user', function($value)
	{
		return User::where('name', $value)->first();
	});

<a name="errori-404"></a>
## Errori 404

Ci sono due modi di lanciare manualmente un errore 404 da una route. Il primo è tramite l'helper _abort_:

	abort(404);

Tutto quello che viene fatto da questo helper è lanciare un'eccezione di tipo `Symfony\Component\HttpFoundation\Exception\HttpException` con lo specifico status code.

Un'alternativa è lanciare tu stesso un'istanza di `Symfony\Component\HttpKernel\Exception\NotFoundHttpException`.

Puoi trovare altre informazioni sulle eccezioni nella sezione dedicata alla gestione degli errori in questa documentazione.
