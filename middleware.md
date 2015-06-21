# HTTP Middleware

- [Introduzione](#introduzione)
- [Definire un Middleware](#definire-middleware)
- [Registrare un Middleware](#registrare-middleware)
- [Parametri di un Middleware](#parametri-middleware)
- [Middleware Terminabili](#middleware-terminabili)

<a name="introduzione"></a>
## Introduzione

I middleware HTTP sono un meccanismo molto utile quando c'è bisogno di filtrare una richiesta HTTP verso la tua applicazione. 

Giusto per fare un esempio, Laravel include di default un middleware che verifica se l'utente è autenticato oppure no. Tale middleware, inoltre, reindirizza l'utente verso una pagina di login qualora non abbia effettuato l'accesso. Se l'utente invece è effettivamente entrato, allora prosegue senza problemi. Una sorta di posto di blocco, insomma.

Ovviamente, puoi costruire tu stesso altri middleware in base alle tue necessità. Ad esempio, un middleware CORS potrebbe avere il compito di aggiungere qualcosa all'header, o magari un altro middleware potrebbe essere dedicato al logging delle operazioni.

Ci sono svariati middleware inclusi in Laravel. Inclusi alcuni per la manutenzione, autenticazione, protezione da CSRF ed altro ancora. Tutti questi middleware possono essere trovati nella cartella _app/Http/Middleware_.

<a name="definire-middleware"></a>
## Definire un Middleware

Per creare un nuovo middleware puoi usare il comando Artisan _make:middleware_:

	php artisan make:middleware OldMiddleware

L'esecuzione di questo comando creerà un nuovo file chiamato _OldMiddleware.php_ contenente la rispettiva classe in `app/Http/Middleware`. Vogliamo che questo middleware si occupi di permettere l'accesso solo se un certo parametro _age_ (fornito nella richiesta) sia maggiore di 200. In caso contrario, reindirizzerà l'utente in home page.

	<?php namespace App\Http\Middleware;

	use Closure;

	class OldMiddleware
	{
		/**
		 * Run the request filter.
		 *
		 * @param  \Illuminate\Http\Request  $request
		 * @param  \Closure  $next
		 * @return mixed
		 */
		public function handle($request, Closure $next)
		{
			if ($request->input('age') < 200) {
				return redirect('home');
			}

			return $next($request);
		}

	}

Come puoi vedere, se il parametro _age_ è minore di 200 il middleware ritorna un redirect HTTP al client. In caso contrario, invece, la richiesta viene passata al "livello successivo", permettendone la continuazione senza problemi tramite il richiamo di _$next_.

Per intendere meglio il meccanismo, immagina i middleware come una serie di "livelli" che la richiesta HTTP deve superare prima di arrivare al suo obiettivo. Ogni livello può effettuare delle operazioni, e a volte presentare dei requisiti affinché la richiesta possa "continuare indisturbata".

### Middleware *Before* ed *After*

Il "quando" un middleware viene eseguito, se prima o dopo una richiesta, dipende fondamentalmente dal middleware stesso. Nell'esempio seguente puoi osservare un middleware le cui istruzioni vengono eseguite prima che la richiesta vera e propria venga gestita.

	<?php namespace App\Http\Middleware;

	use Closure;

	class BeforeMiddleware
	{
		public function handle($request, Closure $next)
		{
			// Eseguo le operazioni desiderate...

			return $next($request);
		}
	}

Questo altro middleware, invece, esegue prima quello che viene richiesto, poi effettua una determinata azione.

	<?php namespace App\Http\Middleware;

	use Closure;

	class AfterMiddleware
	{
		public function handle($request, Closure $next)
		{
			$response = $next($request);

			// Eseguo le operazioni desiderate...

			return $response;
		}
	}

<a name="registrare-middleware"></a>
## Registrare un Middleware

### Middleware Globali

A volte può essere utile definire dei middleware "globali", cioè eseguiti per ogni singola richiesta HTTP. Se è questa la tua necessità, non devi fare altro che aggiungere la classe del middleware che ti interessa all'array _$middleware_ in _app/Http/Kernel.php_.

### Assegnare un Middleware ad una Route

Se vuoi assegnare un middleware ad una route specifica, devi prima assegnare al tuo middleware un "nome", andando ad aggiungere un nuovo elemento alla proprietà _$routeMiddleware_ in _app/Http/Kernel.php_. Ecco come appare:

	// Siamo nella classe App\Http\Kernel...

    protected $routeMiddleware = [
        'auth' => 'App\Http\Middleware\Authenticate',
        'auth.basic' => 'Illuminate\Auth\Middleware\AuthenticateWithBasicAuth',
        'guest' => 'App\Http\Middleware\RedirectIfAuthenticated',
    ];

Una volta che il middleware è stato registrato e definito (esatto, _$routeMiddleware è un array associativo), puoi usare la chiave _middleware_ durante la definizione di una route.

	Route::get('admin/profile', ['middleware' => 'auth', function () {
		//
	}]);

<a name="parametri-middleware"></a>
## Parametri di un Middleware

A volte potresti aver bisogno di cose più complesse di un middleware basilare. Potresti necessitare, ad esempio, di usare un middleware ma con parametri specifici. Uno degli esempi più comuni è il controllo di un certo "ruolo" associato all'utente che sta effettuando una richiesta. Un _RoleMiddleware_ potrebbe essere la soluzione più adatta.

Puoi passare dei parametri aggiuntivi ad un middleware subito dopo _$next_. Così:

	<?php namespace App\Http\Middleware;

	use Closure;

	class RoleMiddleware
	{
		/**
		 * Run the request filter.
		 *
		 * @param  \Illuminate\Http\Request  $request
		 * @param  \Closure  $next
		 * @param  string  $role
		 * @return mixed
		 */
		public function handle($request, Closure $next, $role)
		{
			if (! $request->user()->hasRole($role)) {
				// Redirect...
			}

			return $next($request);
		}

	}

A quel punto, definire un parametro in fase di definizione di una route è semplicissimo: basta separare il nome del middleware e i parametri con un _:_. 

	Route::put('post/{id}', ['middleware' => 'role:editor', function ($id) {
		//
	}]);

<a name="middleware-terminabili"></a>
## Middleware Terminabili

Un'altra eventualità che potrebbe presentarsi è l'esecuzione di alcune operazioni **dopo** l'invio della risposta ad una richiesta. Ad esempio, il middleware _session_ incluso con Laravel scrive dei dati di sessione nello storage _dopo_ l'invio della risposta al browser. Niente di complicato: basta aggiungere un metodo _terminate_ al middleware desiderato.

	<?php namespace Illuminate\Session\Middleware;

	use Closure;

	class StartSession
	{
		public function handle($request, Closure $next)
		{
			return $next($request);
		}

		public function terminate($request, $response)
		{
			// Store the session data...
		}
	}

Il metodo _terminate_ riceve sia la richiesta che la risposta.
