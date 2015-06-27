# Risposte HTTP

- [Risposte Base](#risposte-base)
	- [Allegare Header Alla Risposta](#allegare-header-alla-risposta)
	- [Allegare Cookie Alla Risposta](#allegare-cookie-alla-risposta)
- [Altri Tipi di Risposte](#altri-tipi-di-risposte)
	- [View In Una Risposta](#view-in-una-risposta)
	- [Risposte JSON](#risposte-json)
	- [Download di File](#file-downloads)
- [Redirect](#redirect)
	- [Redirect Di Una Route Nomiata](#redirect-route-nominata)
	- [Redirect Ad Un'Azione di un Controller](#redirect-azione-controller)
	- [Redirect Con Dati Memorizzati nella Sessione](#redirect-con-dati-memorizzati-sessione)
- [Macro Response](#macro-risposte)

<a name="risposte-base"></a>
## Risposte Base

Ovviamente, tutte le route e tutti i controller dovrebbero ritornare qualche tipo di risposta da ri inviare al browser dell'utente. Laravel offre diversi modi per ritornare una risposta. La più semplice risposta base è quella di ritornare una stringa da una route o dal controller:

	Route::get('/', function () {
		return 'Hello World';
	});

La stringa sarà automaticamente convertita dal framwork in una risposta HTTP.

Tuttavia, per molte routes e per la azione di un controller, ti sarà restituita una istanza di `Illuminate\Http\Response` oppure una [view](/docs/{{version}}/views). Il ritorno di una istanza completa di `Response` ti permette di personalizzare il codice di stato e gli header di una risposta HTTP. Un'istanza `Response`eredita la classe `Symfony\Component\HttpFoundation\Response`, che offre una serie di metodi per costruire le richieste HTTP:

	use Illuminate\Http\Response;

	Route::get('home', function () {
		return (new Response($content, $status))
		              ->header('Content-Type', $value);
	});

Per convenienza, puoi usare l'helper `response`:

	Route::get('home', function () {
		return response($content, $status)
		              ->header('Content-Type', $value);
	});

> **Nota:** Per una lista completa dei metodi disponibili di `Response`, dai un oacchiata alla documentazione delle [API documentation](http://laravel.com/api/master/Illuminate/Http/Response.html) ed alla documentazione [delle API Symfony](http://api.symfony.com/2.7/Symfony/Component/HttpFoundation/Response.html).
<a name="allegare-header-alla-risposta"></a>
#### Allegare Header Alla Risposta

Tieni bene in mente, che la maggior parte dei metodi della risposta sono concatenabili, offrendoti la creazione fluente di risposte. Per esempio, puoi usare il metodo `header` per aggiunere una serie di header alla risposta perima di inviarla all'utente:

	return response($content)
				->header('Content-Type', $type)
				->header('X-Header-One', 'Header Value')
				->header('X-Header-Two', 'Header Value');


<a name="allegare-cookie-alla-risposta"></a>
#### Allegare Cookie Alla Risposta

Il metodo helper `withCookie` sull'istanza Response ti permette facilmente di allegare un cookie alla risposta. Per esempio, puoi usare il metodo `withCookie` per generare un cookie ed allegarlo all'istanza della risposta:

	return response($content)->header('Content-Type', $type)
                     ->withCookie('name', 'value');

Il metodo `withCookie` accetta degli argomenti come facoltativi che ti permettono di modificare le proprietà del cookie:

	->withCookie($name, $value, $minutes, $path, $domain, $secure, $httpOnly)

Di default, tutti i cookie generati da Laravel sono criptati e segnati così non possono essere modificati o letti dal client. Se vuoi disabilitare la criptazione per un certo insieme di cookie generati dalla tua applicazione, puoi usare la proprietà `$except` del middleware `App\Http\Middleware\EncryptCookies`:

    /**
     * The names of the cookies that should not be encrypted.
     *
     * @var array
     */
    protected $except = [
        'cookie_name',
    ];

<a name="altri-tipi-di-risposte"></a>
## Altri Tipi di Risposte

L'helper `response` può essere usato per comodità, per generare altri tipi di istanza di risposte. Quando l'helper `response` è chiamato senza parametris, viene ritornata un implementazione del  [contract](/docs/{{version}}/contracts) `Illuminate\Contracts\Routing\ResponseFactory`. Questo contract offre una serie di utili metodi per generare risposte.

<a name="view-in-una-risposta"></a>
#### View In Una Risposta

Se hai bisogno di controllare lo stato e gli header della risposta, ma anche di ritornare una [view](/docs/{{version}}/views) come contenuto di una risposta, puoi usare il metodo `view`:

	return response()->view('hello', $data)->header('Content-Type', $type);

Ovviamente, se non hai bisogno di passare un codice di stato HTTP personalizzato o degli header personalizzati, puoi usare semplicemente la funzione di helper globale `view`.

<a name="risposte-json"></a>
#### Risposte JSON

Il metodo `json` imposterà automaticamente l'header `Content-Type` su `application/json`, convertendo l'array in JSON usando la funzione `json_encode` di PHP:

	return response()->json(['name' => 'Abigail', 'state' => 'CA']);

Se vuoi creare una risposta JSONP, puoi usare il metodo `json` aggiunendo il metodo`setCallback`, in questo modo:

	return response()->json(['name' => 'Abigail', 'state' => 'CA'])
	                 ->setCallback($request->input('callback'));

<a name="download-di-file"></a>
#### Download di File

Il metodo `download` può essere usato per generare una risposta the forza il browser dell'utente a scaricare un file da un dato percorso. Il metodo `download` accetta un nome di un file come suo secondo parametro, che determinerà con quale nome verrà scaricato il file dall'utente. In fine, puoi passare un array di header HTTP come terzo parametro:

	return response()->download($pathToFile);

	return response()->download($pathToFile, $name, $headers);

> **Nota:** Symfony HttpFoundation, che gestisce il download dei file, richiede che il file che sta per essere scaricato abbia un nome file nel formato ASCII. 

<a name="redirect"></a>
## Redirect

I redirect sono istanze della classe `Illuminate\Http\RedirectResponse`, e contengono gli header necessari per reindirizzare l'utente ad un altro URL. Ci sono diversi modi per generare un istanza `RedirectResponse`. Il più semplice metodo è di usare il metodo helper globale `redirect`:

	Route::get('dashboard', function () {
		return redirect('home/dashboard');
	});

Alcune volte, puoi voler reindirizzare l'utente alla sua precedente posizione, per esempio dopo l'invio di un form che non è andato a buon fine. Per farlo puoi usare la funzione di helper globale `back`:

	Route::post('user/profile', function () {
		// Validate the request...

		return back()->withInput();
	});

<a name="redirect-route-nominata"></a>
#### Redirect Di Una Route Nomiata

Quando richiami l'helper `redirect` senza nessun parametro, viene ritornata un istanza di `Illuminate\Routing\Redirector`, che ti permette di chiamare qualsiasi metodo dell'istanza `Redirector`. Per esempio, per generare una `RedirectResponse` ad una route nominata, puoi usare il metodo `route`:

	return redirect()->route('login');

Se la tua route ha dei parametri, puoi passarli come secondo parametro del metodo `route`:

	// For a route with the following URI: profile/{id}

	return redirect()->route('profile', [1]);

Se stai reindirizzando ad una route con un parametro "ID" che viene popolato da un model Eloquent, passa semplicmente il model stesso come parametro. L'ID sarà così estratta automaticamente:

	return redirect()->route('profile', [$user]);

<a name="redirect-azione-controller"></a>
#### Redirect Ad Un'Azione di un Controller

Puoi anche generare redirect alle [azioni di un controller](/docs/{{version}}/controllers). Per farlo, passa semplicemente il controller e il nome dell'azione al metodo `action`. Ricordati, non devi specificare il namespace completoo al controller dato che il provider `RouteServiceProvider` imposterà automaticamente il namespace di default del controller:

	return redirect()->action('HomeController@index');

Ovviamente, se la route del tuo controller richiede paramaetri, puoi passarli come secondo parametro del metodo `action`:

	return redirect()->action('UserController@profile', [1]);

<a name="redirect-con-dati-memorizzati-sessione"></a>
#### Redirect Con Dati Memorizzati nella Sessione

Il redirect ad un nuovo URL e la [memorizzazione di dati nella sessione](/docs/{{version}}/session) sono tipicamente eseguite nello stesso tempo. Cosi, per comodità, puoi creare un istanza `RedirectResponse` **e** memorizzare dati nella sessione in un singolo metodo concatenato. Questo è particolarmente utile per memorizzare messaggi di stato dopo un'azione:

	Route::post('user/profile', function () {
		// Update the user's profile...

		return redirect('dashboard')->with('status', 'Profile updated!');
	});

Ovviamente, dopo che l'utente è reindirizzato alla nuova pagina, puoi ritrovare e visualizzare il messaggio memorizzato nella [sessione](/docs/{{version}}/session). Per esempio, usando la [sintassi Blade](/docs/{{version}}/views):

	@if (session('status'))
		<div class="alert alert-success">
			{{ session('status') }}
		</div>
	@endif

<a name="macro-risposte"></a>
## Macro Risposte

Se preferisci definire una risposta personalizzata da ri-utilizzare nelle tue route o nei tuoi controller, puoi usare il metodo macro su un'implementazione del contract `Illuminate\Contracts\Routing\ResponseFactory`. 

Per esempio, dal metodo `boot` di un [service provider](/docs/{{version}}/providers):

	<?php namespace App\Providers;

	use Illuminate\Support\ServiceProvider;
	use Illuminate\Contracts\Routing\ResponseFactory;

	class ResponseMacroServiceProvider extends ServiceProvider
	{
		/**
		 * Perform post-registration booting of services.
		 *
		 * @param  ResponseFactory  $factory
		 * @return void
		 */
		public function boot(ResponseFactory $factory)
		{
			$factory->macro('caps', function ($value) use ($factory) {
				return $factory->make(strtoupper($value));
			});
		}
	}

La funzione `macro` accetta un nome come primo parametro, ad una Closure come secondo. La Closure della macro sarà eseguita quando verrà effettuata una chiamata al nome della macro da un'implementazione di `ResponseFactory` dell'helper `response`:

	return response()->caps('foo');
