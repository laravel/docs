# Middleware

- [Introduzione](#introduzione)
- [Definire un Middleware](#definire-middleware)
- [Registrare un Middleware](#registrare-middleware)

<a name="introduzione"></a>
## Introduzione

I middleware HTTP forniscono un meccanismo molto conveniente di filtraggio delle richieste HTTP in entrata. Per farti un esempio, Laravel possiede un middleware che verifica se l'utente della tua applicazione ha effettuato l'accesso correttamente. Nel caso in cui questo controllo dia un esito negativo, il middleware effettua un redirect verso la schermata di login. In caso contrario, invece, tutto prosegue normalmente.

Ovviamente, un middleware può essere scritto per una marea di motivi più disparati che vanno ben oltre l'autenticazione. Ad esempio, un middleware CORS potrebbe occuprasi di aggiungere gli header appropriati a tutte le risposte delle tua applicazione. Un logging middleware potrebbe occuparsi di loggare, appunto, le richieste verso la tua applicazione.

Laravel possiede out of the box svariati middleware già pronti, tra cui uno per la modalità di manutenzione, per l'autenticazione, protezione da CSRF e così via. Tutti questi middleware si trovano nella cartella `app/Http/Middleware`.

<a name="definire-middleware"></a>
## Definire un Middleware

Per creare un nuovo middleware, usa il comando `make:middleware` di Artisan:

	php artisan make:middleware OldMiddleware

Questo comando, nello specifico, creerà un nuovo file `OldMiddleware` nella directory `app/Http/Middleware`. Per fare un esempio pratico, faremo in modo che questo middleware garantisca l'accesso solo se l'età specificata è maggiore di 200. In caso contrario, l'utente verrà reindirizzato verso la home page.

	<?php namespace App\Http\Middleware;

	class OldMiddleware {

		/**
		 * Run the request filter.
		 *
		 * @param  \Illuminate\Http\Request  $request
		 * @param  \Closure  $next
		 * @return mixed
		 */
		public function handle($request, Closure $next)
		{
			if ($request->input('age') < 200)
			{
				return redirect('home');
			}

			return $next($request);
		}

	}

Come puoi vedere, se l'età fornita è minore di 200 il middleware ritorna un semplice redirect HTTP. In caso contrario, la richiesta verrà passata all'applicazione vera e propria. L'istruzione da usare per "procedere" nell'applicazione consiste nel chiamare la route _$next_.

	return $next($request);

Il modo migliore per inquadrare il concetto di middleware è quello di una serie di "livelli" che devono essere superati prima di poter lavorare con l'applicazione vera e propria. Ogni livello può infatti prendere e rifiutare una richiesta, se necessario.

<a name="registrare-middleware"></a>
## Registrare un Middleware

### Middleware Globali

Se vuoi fare in modo che un middleware venga eseguito ad ogni richiesta HTTP, inseriscilo nell'array _$middleware_, proprietà della classe `app/Http/Kernel.php`.

### Assegnare un Middleware solo ad alcune Route

Potresti voler usare un middleware solo per alcune route specifiche: molto spesso è il caso di _auth_ il middleware che si occupa di controllare se l'utente ha effettuato l'accesso. Comunque, se è questo il tuo caso, aggiungi il middleware all'array associativo `$routeMiddleware` della classe `app/Http/Kernel.php`. Come chiave scegli un nome che userai successivamente come identificatore in fase di chiamata da una route.

Definito tutto il necessario puoi usare da subito il middleware usando il nome scelto:

	Route::get('admin/profile', ['middleware' => 'auth', function()
	{
		//
	}]);
