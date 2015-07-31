# Routing

- [Routing di Base](#routing-di-base)
- [Parametri delle Route](#parametri-route)
	- [Parametri Obbligatori](#parametri-obbligatori)
	- [Parametri Opzionali](#parametri-opzionali)
	- [Uso di Espressioni Regolari](#uso-espressioni-regolari)
	- [Regole "Globali"](#regole-globali)
- [Route "Rinominate"](#route-rinominate)
- [Gruppi di Route](#gruppi-route)
	- [Condivisione di Middleware](#condivisione-middleware)
	- [Condivisione di Namespace](#condivisione-namespace)
	- [Routing del Sottodominio](#routing-sottodominio)
	- [Prefissi dei Gruppi](#prefissi-gruppi)
- [Protezione CSRF](#protezione-csrf)
	- [Introduzione](#introduzione)
	- [Escludere degli URL dalla Protezione CSRF](#escludere-url-protezione-csrf)
	- [X-CSRF-TOKEN](#x-csrf-token)
	- [X-XSRF-TOKEN](#x-xsrf-token)
- [Method Spoofing per i Form](#method-spoofing-form)
- [Errori 404](#errori-404)

<a name="routing-di-base"></a>
## Basic Routing

Le route della tua applicazione verranno definite, di default, in `app/Http/routes.php` caricato automaticamente dalla class `App\Providers\RouteServiceProvider`. Ecco alcuni esmepi di definizione base: tutto quello che bisogna fare è definire l'url ed una closure corrispondente. Il nome del metodo corrisponde al verb HTTP da usare.

	Route::get('/', function () {
		return 'Hello World';
	});

	Route::post('foo/bar', function () {
		return 'Hello World';
	});

	Route::put('foo/bar', function () {
		//
	});

	Route::delete('foo/bar', function () {
		//
	});

#### Registrare una Route per più Verb

A volte potresti voler registrare una route che risponda, contemporaneamente, a più verb HTTP. Puoi farlo tramite _match()_:

	Route::match(['get', 'post'], '/', function () {
		return 'Hello World';
	});

Oppure, potresti anche voler registrare una route per tutti i verb HTTP. In questo caso usa `any`:

	Route::any('foo', function () {
		return 'Hello World';
	});

#### Generare gli URL corrispondenti alle Route

Per generare gli URL relativi alle route, usa l'helper `url`:

	$url = url('foo');

<a name="parametri-route"></a>
## Parametri delle Route

<a name="parametri-obbligatori"></a>
### Parametri Obbligatori

Ovviamente, molto spesso avrai la necessità di "intercettare" i segmenti dell'URI della tua route. Ad esempio, potresti voler prelevare l'id di un utente dall'URL. In questo caso, basta usare i parametri in questo modo:

	Route::get('user/{id}', function ($id) {
		return 'User '.$id;
	});

Puoi definirne, ovviamente, quanti ne vuoi:

	Route::get('posts/{post}/comments/{comment}', function ($postId, $commentId) {
		//
	});

Vengono sempre usate le parentesi graffe. I parametri verranno passati alla closure nell'ordine in cui sono scritti.

> **Nota:** il nome di un parametro non può contenere il carattere `-`. Puoi usare però un underscore (`_`).

<a name="parametri-opzionali"></a>
### Parametri Opzionali

Occasionalmente, potresti avere la necessità di specificare dei parametri non obbligatori. In tal caso, aggiungi un `?` subito dopo il nome del parametro.

	Route::get('user/{name?}', function ($name = null) {
		return $name;
	});

	Route::get('user/{name?}', function ($name = 'John') {
		return $name;
	});

<a name="uso-espressioni-regolari"></a>
### Uso di Espressioni Regolari

Tramite il metodo _where()_ puoi decidere di dare delle "regole" per l'ammissibilità di alcuni parametri. Tali regole possono essere specificate tramite l'uso di espressioni regolari, come nell'esempio di seguito:

	Route::get('user/{name}', function ($name) {
		//
	})
	->where('name', '[A-Za-z]+');

	Route::get('user/{id}', function ($id) {
		//
	})
	->where('id', '[0-9]+');

	Route::get('user/{id}/{name}', function ($id, $name) {
		//
	})
	->where(['id' => '[0-9]+', 'name' => '[a-z]+']);

<a name="regole-globali"></a>
#### Regole "Globali"

Se preferisci, puoi assegnare delle regole globali a tutti i parametri (di tutte le route) che hanno un certo nome. Immagina, ad esempio, di aver deciso che un qualsiasi parametro "id" sarà sempre un numero intero. Apri la classe _RouteServiceProvider_ in _app/Providers_ e aggiungi al metodo _boot_:

    /**
     * Define your route model bindings, pattern filters, etc.
     *
     * @param  \Illuminate\Routing\Router  $router
     * @return void
     */
    public function boot(Router $router)
    {
		$router->pattern('id', '[0-9]+');

        parent::boot($router);
    }

Una volta definito, il pattern viene applicato a tutti i parametri con quello specifico nome.

	Route::get('user/{id}', function ($id) {
		// Viene eseguito solo se {id} è numerico
	});

<a name="route-rinominate"></a>
## Route "Rinominate"

Tramite le route "rinominate" (Named Routes) puoi generare più agevolmente dei redirect verso una route specifica. Tutto quello che devi fare è usare la chiave "as" nell'array associativo usato per definire una route.

	Route::get('user/profile', ['as' => 'profile', function () {
		//
	}]);

La stessa cosa può essere fatta per le action di un controller:

	Route::get('user/profile', [
		'as' => 'profile', 'uses' => 'UserController@showProfile'
	]);

#### Route "Rinominate" e Gruppi

Se stai usando i [gruppi di route](#gruppi-route), puoi specificare l'elemento "as" anche come attributo di un gruppo, in modo tale da dare un prefisso comune in fase di ridenominazione di una route.

	Route::group(['as' => 'admin::'], function () {
		Route::get('dashboard', ['as' => 'dashboard', function () {
			// "admin::dashboard"
		}]);
	});

In questo esempio, la route sarà "raggiungibile" con un link generato da

	url('admin::dashboard');

#### Generare gli URL per le Route "Rinominate"

Una volta che hai assegnato un nome ad una certa route, puoi usare il suo nome in fase di generazione tramite il metodo _route_:

	$url = route('profile');

	$redirect = redirect()->route('profile');

Se per tale route sono stati definiti dei parametri, puoi passare tali parametri come secondo argomento del metodo _route_. Questi parametri verranno automaticamente aggiunti all'URL finale.

	Route::get('user/{id}/profile', ['as' => 'profile', function ($id) {
		//
	}]);

	$url = route('profile', ['id' => 1]);

<a name="gruppi-route"></a>
## Gruppi di Route

I gruppi di route ti permettono di far condividere a più route attributi, middleware, namespace e così via, senza dover definire la stessa cosa più volte. Tali attributi condivisi sono specificati in un array in corrispondenza della definizione del gruppo stesso.

Vediamo alcuni esempi.

<a name="condivisione-middleware"></a>
### Condivisione di Middleware

Per far condividere a più route lo stesso middleware, usa la chiave _middleware_ come segue.

	Route::group(['middleware' => 'auth'], function () {
		Route::get('/', function ()	{
			// Viene usato il middleware auth
		});

		Route::get('user/profile', function () {
			// Viene usato il middleware auth
		});
	});

<a name="condivisione-namespace"></a>
### Condivisione di Namespace

Un altro caso d'uso comune è la condivisione di namespace PHP per un determinato gruppi di controller. Questo tramite l'elemento _namespace_ nell'array degli attributi.

	Route::group(['namespace' => 'Admin'], function()
	{
		// controller nel namespace "App\Http\Controllers\Admin"

		Route::group(['namespace' => 'User'], function()
		{
			// controller nel namespace "App\Http\Controllers\Admin\User"
		});
	});

Ricorda che di default il `RouteServiceProvider` include tutte le tue route in `routes.php` in un gruppo di default, che ti permette di registrare i tuoi controller senza dover specificare, ogni volta, `App\Http\Controllers`.

<a name="routing-sottodominio"></a>
### Routing del Sottodominio

I gruppi di route possono essere usati anche per specificare il routing relativo ai sottodomini. Tali sottodomini possono essere assegnati esattamente come qualsiasi altra route. Stavolta l'elemento da usare è _domain_:

	Route::group(['domain' => '{account}.myapp.com'], function () {
		Route::get('user/{id}', function ($account, $id) {
			//
		});
	});

<a name="prefissi-gruppi"></a>
### Prefissi dei Gruppi

L'elemento _prefix_ dell'array degli attributi può essere usato per specificare un prefisso per ogni route inclusa nel gruppo stesso. Ecco un esempio:

	Route::group(['prefix' => 'admin'], function () {
		Route::get('users', function ()	{
			// Risponderà a "/admin/users"
		});
	});

Puoi anche specificare dei parametri nel prefisso, se preferisci.

	Route::group(['prefix' => 'accounts/{account_id}'], function () {
		Route::get('detail', function ($account_id)	{
			// Risponderà a accounts/{account_id}/detail URL
		});
	});

<a name="protezione-csrf"></a>
## Protezione CSRF

<a name="introduzione"></a>
### Introduction

Laravel permette, in modo molto facile, di proteggere la tua applicazione da attacchi di tipo [cross-site request forgery](https://it.wikipedia.org/wiki/Cross-site_request_forgery). Tali attacchi consistono in exploit con lo scopo di portare all'esecuzione di comandi da parte utenti non autorizzati.

Tramite l'helper *csrf_field* è possibile generare un "token" di verifica per la messa in sicurezza dell'applicazione.

	<?php echo csrf_field(); ?>

L'HTML risultante generato è il seguente:

	<input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">

Ovviamente puoi anche usare il [sistema di template Blade](/documentazione/5.1/blade), se vuoi:

	{!! csrf_field() !!}

Non devi assolutamente fare nulla per verificare il token creato: tramite il middleware `VerifyCsrfToken`, infatti, l'operazione è svolta automaticamente. In caso di problemi viene mostrato un errore che blocca i tentativi di attacco.

<a name="escludere-url-protezione-csrf"></a>
### Escludere degli URL dalla Protezione CSRF

A volte potresti aver bisogno di escludere un certo set di URI dalla protezione da CSRF. Ad esempio, se dovessi usare [Stripe](https://stripe.com) per processare i pagamenti ne avrai sicuramente bisogno.

Puoi sistemare la cosa velocemente aggiungendo tali URI alla proprietà _$except_ del middleware `VerifyCsrfToken`

	<?php namespace App\Http\Middleware;

	use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as BaseVerifier;

	class VerifyCsrfToken extends BaseVerifier
	{
	    /**
	     * The URIs that should be excluded from CSRF verification.
	     *
	     * @var array
	     */
	    protected $except = [
	        'stripe/*',
	    ];
	}

<a name="x-csrf-token"></a>
### X-CSRF-TOKEN

In aggiunta al controllo del token CSRF appena citato come parametro POST, il middleware `VerifyCsrfToken` controlla anche l'eventuale presenza di un header `X-CSRF-TOKEN` nella richiesta. Se preferisci puoi anche usare un meta tag come il seguente.

	<meta name="csrf-token" content="{{ csrf_token() }}">

Tale soluzione può essere ottima se stai effettuando delle chiamate asincrone tramite librerie e framework come jQuery, o AngularJS.

	$.ajaxSetup({
			headers: {
				'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
			}
	});

<a name="x-xsrf-token"></a>
### X-XSRF-TOKEN

Laravel, inoltre, memorizza il token in un cookie chiamato `XSRF-TOKEN` cookie. Puoi usare tale cookie per impostare il valore dell'header `X-XSRF-TOKEN`. Ad ogni modo, alcuni framework come Angular effettuano questa operazione automaticamente.

<a name="method-spoofing-form"></a>
## Method Spoofing per i Form

I form HTML non supportano i verb `PUT`, `PATCH` e `DELETE`. Se tuttavia dovessi averne bisogno, tutto quello che devi fare è specificare un campo hidden chiamato `_method`:

	<form action="/foo/bar" method="POST">
		<input type="hidden" name="_method" value="PUT">
		<input type="hidden" name="_token" value="{{ csrf_token() }}">
	</form>

<a name="errori-404"></a>
## Errori 404

Ci sono due diversi modi di lanciare un errore 404 da una route. Il primo, più semplice, è tramite l'uso dell'helper _abort()_.

	abort(404);

Altrimenti, se preferisci le cose più complesse, ti basta lanciare un'istanza di `Symfony\Component\HttpKernel\Exception\NotFoundHttpException`.

Se vuoi avere più informazioni su come gestire le eccezioni di questo genere e, eventualmente, come personalizzare l'output relativo, dai uno sguardo alla [pagina dedicata su questa documentazione](/documentazione/5.1/errori#eccezioni-http).
