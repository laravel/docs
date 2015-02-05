# Risposte HTTP

- [Risposte Base](#risposte-base)
- [Redirect](#redirect)
- [Altre Risposte](#altre-risposte)
- [Macro Risposte](#macro-risposte)

<a name="risposte-base"></a>
## Risposte Base

#### Ritornare Una Stringa Da Una Route

La risposta più semplice proveniente da una route è una stringa:

	Route::get('/', function()
	{
		return 'Hello World';
	});

#### Creare Una Risposta Personalizzata

Tuttavia, per la maggior parte delle route e delle azioni dei controller, ritornerà un'istanza
However, for most routes and controller actions, you will be returning a full `Illuminate\Http\Response` oppure una [view](/docs/master/views). Il ritorno di una istanza completa di `Response` ti permette di personalizzare il codice di stato e gli header di una risposta HTTP. Un'istanza `Response` eredita la classe `Symfony\Component\HttpFoundation\Response`, che offre una serie di metodi per costruire le richieste HTTP:

	use Illuminate\Http\Response;

	return (new Response($content, $status))
	              ->header('Content-Type', $value);

Per convenienza, puoi usare anche l'helper `response`:

	return response($content, $status)
	              ->header('Content-Type', $value);

> **Nota:** Per una lista completa dei metodi disponibili di `Response`, dai un oacchiata alla [documentazione delle API](http://laravel.com/api/master/Illuminate/Http/Response.html) ed alla [documentazione Symfony API](http://api.symfony.com/2.5/Symfony/Component/HttpFoundation/Response.html).

#### Inviare Una View In Una Risposta

Se hai bisogno di accedere ai metodi della classe `Response`, ma vuoi ritornare una view il contenuto della risposta, puoi usare il metodo `view` come segue:

	return response()->view('hello')->header('Content-Type', $type);

#### Allegare Un Cookie Alla Risposta

	return response($content)->withCookie(cookie('name', 'value'));

<a name="redirect"></a>
## Redirect

Le risposte redirect sono tipicamente delle istanze della classe `Illuminate\Http\RedirectResponse`, contenenti gli header necessari per reindirizzare l'utente ad un altro URL.

#### Ritornare Un Redirect

Ci sono vari metodi per generare un'istanza di `RedirectResponse`. Il metodo più semplice è quello di usare il metodo helper `redirect`. In fase di testing, non è solito fare il mock della creazione della risposta redirect, quindi è sempre accettabile usare il metodo helper:

	return redirect('user/login');

#### Ritornare Un Redirect Con Il Flash Dei Dati

Il re-indirizzamento ad un nuovo URL e il [flashing dei dati nella sessione](/docs/master/session) normalmente fanno la stessa cosa. Quindi, per convenienza, puoi crare un'istanza `RedirectResponse` **e** fare il flash dei dati nella sessione concatendando l'operazione con un singolo metodo:

	return redirect('user/login')->with('message', 'Login Failed');

#### Ritornare Un Redirect Di Una Route Nomiata

Quando effettui una chiamata al metodo helper `redirect` senza parametri, viene ritornata un'istanza  `Illuminate\Routing\Redirector`, che ti permette di richiamare qualsiasi metodo sull'istanza  `Redirector`. Per esempio, per generare un `RedirectResponse` ad una route nominata, puoi usare il metodo `route`:

	return redirect()->route('login');

#### Ritornare Un Redirect Di Una Route Nominata Con Parametri

Se la tua route ha dei parametri, puoi passarli come secondo parametro del metodo `route`.

	// For a route with the following URI: profile/{id}

	return redirect()->route('profile', [1]);

Se stai per essere reindirizzato ad una route con un parametro "ID" che verrà popolato ad un modello Eloquent, puoi passare semplicemente il modello stesso al metodo. L'ID verrà estratta automaticamente:

	return redirect()->route('profile', [$user]);

#### Ritornare Un Redirect Di Una Route Nominata Usando I Parametri Nominati

	// For a route with the following URI: profile/{user}

	return redirect()->route('profile', ['user' => 1]);

#### Ritornare Un Redirect Ad Un'Azione Di Un Controller

In maniera simile all'istanza  `RedirectResponse` ad una route nominata, puoi anche generare dei redirect alle [azioni del controller](/docs/master/controllers):

	return redirect()->action('App\Http\Controllers\HomeController@index');

> **Nota:** Non hai bisogno di specificare il namespace completo ad un altro controller se hai registrato il namespace root tramite `URL::setRootControllerNamespace`.

#### Ritornare Un Redirect Di Un'Azione Di Un Controller Con Parametri

	return redirect()->action('App\Http\Controllers\UserController@profile', [1]);

#### Ritornare Un Redirect Di Un'Azione Di Un Controller Usando I Parametri Nominati

	return redirect()->action('App\Http\Controllers\UserController@profile', ['user' => 1]);

<a name="altre-risposte"></a>
## Altre Risposte

L'helper `response` può essere usato per comodità per generare altri tipi di istanze di risposte. Quando l'helper `response` viene chiamato senza parametri, viene ritornata un'implementazione del contract `Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/master/contracts). Questo contract offre dei metodi utili per generare delle risposte.

#### Creazione Di Una Risposta JSON

Il metodo `json` imposterà automaticamente l'header `Content-Type` a `application/json`:

	return response()->json(['name' => 'Steve', 'state' => 'CA']);

#### Creazione Di Una Risposta JSONP

	return response()->json(['name' => 'Steve', 'state' => 'CA'])
	                 ->setCallback($request->input('callback'));

#### Creazione Di Una Risposta Di Download File

	return response()->download($pathToFile);

	return response()->download($pathToFile, $name, $headers);

> **Nota:** Symfony HttpFoundation, che gestisce il download dei file, richiede che il file che sta per essere scaricato abbia un nome file nel formato ASCII.

<a name="macro-risposte"></a>
## Macro Risposte

Se preferisci definire una risposta personalizzata da ri-utilizzare nelle tue route o nei tuoi controller, puoi usare il metodo `macro` su un'implementazione del contract `Illuminate\Contracts\Routing\ResponseFactory`.

Per esempio, dal metodo `boot` di un [service provider](/docs/master/providers):

	<?php namespace App\Providers;

	use Response;
	use Illuminate\Support\ServiceProvider;

	class ResponseMacroServiceProvider extends ServiceProvider {

		/**
		 * Perform post-registration booting of services.
		 *
		 * @return void
		 */
		public function boot()
		{
			Response::macro('caps', function($value)
			{
				return Response::make(strtoupper($value));
			});
		}

	}

La funzione `macro` accetta un nome come primo parametro, e come secondo una Closure. La Closure della macro sarà eseguita quando verrà effettuata una chiamata al nome della macro da un'implementazione di `ResponseFactory` o dall'helper `response`:

	return response()->caps('foo');
