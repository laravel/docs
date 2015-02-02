# Autenticazione

- [Introduzione](#introduzione)
- [Autenticare Utenti](#autenticare-utenti)
- [Ritrovare Un Utente Autenticato](#recupero-utenti-autenticati)
- [Route Protette](#route-protette)
- [Autenticazione HTTP Basic](#autenticazione-http-basic)
- [Recupero Password & Reset](#recupero-password-e-reset)
- [Autenticazione Social](#autenticazione-social)

<a name="introduzione"></a>
## Introduzione

Laravel implementa un semplice meccanismo di autenticazione. Infatti, quasi tutto è già configurato “out of the box”. Il file di configurazione si trova in `config/auth.php`, che contiene una serie di opzioni, ben documentate, che userai per ottimizzare il comportamento del tuo servizio di autenticazione.

Di default, Laravel include il model `App\User` della tua directory `app`. Questo model può essere usato di default dal driver Eloquent per gestire l'autenticazione.

Ricorda: quando costruisci lo Schema per questo modello, crea un campo password di almeno 60 caratteri. E ancora, prima di iniziare, assicurati che la tua tabella `users` (o equivalente) contenga una colonna di tipo string e nulla  `remember_token` di 100 caratteri. Questa colonna verrà usata per memorizzare un token per l'opzione di sessione “ricordami” mantenuta dalla tua applicazione. Questo può essere fatto usando il metodo `$table->rememberToken();` nella migration.

Se la tua applicazione non usa Eloquent, puoi sempre usare il driver di autenticazione `database` che usa il query builder di Laravel.

<a name="autenticare-utenti"></a>
## Autenticare Utenti

Laravel utilizza due controller legati all'autenticazione. `AuthController` gestisce le registrazioni di nuovi utenti e i loro accessi, mentre `PasswordController` contiene la logica per aiutare gli utenti per il reset delle loro credenziali di accesso.

Ognuno di questi controller usa un trait che include i loro metodi necessari. Per molte applicazioni, non avrai bisogno di modificare questi controller. Le view che utilizzano questi controller si trovano nella directory `resources/views/auth`. Sei libero di personalizzarle come meglio credi.

### User Registrar

Per modificare i campi del form necessari quando un nuovo utente si registra con la tua applicazione, è possibile farlo modificando la classe `App\Services\Registrar`. Questa classe è responsabile per la creazione e validazione dei nuovi utenti.

Il metodo `validator` di `Registrar` contiene le regole di validazione per i nuovi utenti, mentre il metodo `create` di `Registrar` è responsabile della creazione di un nuovo record `User` nel database. Sei libero di modificare ognuno di questi metodi come desideri. `Registrar` è chiamato da `AuthController` tramite dei metodi contenuti nel trait `AuthenticatesAndRegistersUsers`.

#### Autenticazione Manuale

Se scegli di non usare l'implementazione offerta da `AuthController`, avrai bisogno di gestire l'autenticazione dei tuoi utenti direttamente con la classe di autenticazione di Laravel. Non preoccuparti, è un gioco da ragazzi! Per prima cosa, analizza il metodo `attempt`:

	<?php namespace App\Http\Controllers;

	use Auth;
	use Illuminate\Routing\Controller;

	class AuthController extends Controller {

		/**
		 * Handle an authentication attempt.
		 *
		 * @return Response
		 */
		public function authenticate()
		{
			if (Auth::attempt(['email' => $email, 'password' => $password]))
			{
				return redirect()->intended('dashboard');
			}
		}

	}

Il metodo `attempt` accetta un array di coppie chiave / valore come suo primo parametro. Il valore di `password` sarà [codificato](/docs/master/hashing). Gli altri valori nell'array saranno usati per cercare l'utente nella tabella user del database. Quindi, in questo esempio sopra, l'utente verrà ricercato dal valore della colonna `email`. Se l'utente è presente, la password codificata nel database verrà confrontata con il valore di `password` passato al metodo tramite array. Se le due password coincidono, verrà iniziata una nuova sessione di autenticazione per l'utente.

Il metodo `attempt` restituirà `true` se l'autenticazione ha avuto successo. Altrimenti, verrà restituito `false`.

> **Nota:** In questo esempio, l'`email` non è un'opzione obbligatoria, In this example, `email` is not a required option, è usato unicamente come esempio. Potresti usare qualsiasi nome di colonna che corrisponda alla "username" nel tuo database.

Il metodo `intended` reindirizzerà l’utente all’URL a cui stava tentando di accedere prima di essere intercettato dal filtro di autenticazione. Nel caso in cui la destinazione di redirect non sarà disponibile puoi specificare un fallback URI, ovvero un indirizzo alternativo, passandolo come parametro al metodo.

#### Autenticare Un Utente Con Condizioni

Pupo aggiungere anche delle condizioni extra alla query di autenticazione:

    if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1]))
    {
        // The user is active, not suspended, and exists.
    }

#### Determinare Se Un Utente E' Autenticato

Per determinare se un utente è già loggato nella tua applicazione, puoi usare il metodo `check`:

	if (Auth::check())
	{
		// The user is logged in...
	}

#### Autenticare Un Utente E "Ricordalo"

Se vuoi offrire la funzionalità "ricordami" nella tua applicazione, puoi passare un valore booleano come secondo parametro del metodo `attempt`, che manterrà loggato l'utente indefinitamente, o fino a ché l'utente non effettui un logout. Ovviamente, la tabella `users` deve includere il campo string `remember_token`, il quale verrà usato per salvare il token "ricordami".

	if (Auth::attempt(['email' => $email, 'password' => $password], $remember))
	{
		// The user is being remembered...
	}

Se sei un utente "ricordato", puoi usare il metodo `viaRemember` per determinare se l'utente autenticato sta usando il cookie "ricordami":

	if (Auth::viaRemember())
	{
		//
	}

#### Autenticare Utenti Tramite ID

Per loggare un uente nell'applicazione tramite le loro ID, usa il metodo `loginUsingId`:

	Auth::loginUsingId(1);

#### Validare Le Credenziali Utente Senza Login

Il metodo `validate`  ti permette di validare le credenziali utente senza che quest'ultimo venga loggato nella tua applicazione:

	if (Auth::validate($credentials))
	{
		//
	}

#### Loggare Un Utente Per Un Singola Richiesta

Puoi anche usare il metodo `once` per loggare un utente nell'applicazione per una singola richiesta. Non saranno usati sessioni o cookie:

	if (Auth::once($credentials))
	{
		//
	}

#### Loggare Manualmente Un Utente

Se hai bisogno di loggare un istanza utente nella tua applicazione, puoi usare il metodo `login` con una istanza utente:

	Auth::login($user);

Questo è equivalente a loggare un utente tramite credenziali usando il metodo `attempt`.

#### Logout Dell'Utente

	Auth::logout();

Ovviamente, se stai usando i controller built-in, per la gestione dell'autenticazione, di Laravel, viene fornito un metodo per gestire il logout degli utenti dalla tua applicazione.

#### Eventi Di Autenticazione

Quando viene eseguito il metodo `attempt`, viene lanciato l'[evento](/docs/master/events) `auth.attempt`. Se l'autenticazione ha avuto successo e l'utente è loggato, verrà lanciato l'evento `auth.login`. 

<a name="recupero-utenti-autenticati"></a>
## Recupero Utenti Autenticati

Una autenticato l'utente, ci sono una serie di modi per ottenere un istanza User.

In primo luogo, puoi accedere all'utente usando la facade `Auth`:

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;

	class ProfileController extends Controller {

		/**
		 * Update the user's profile.
		 *
		 * @return Response
		 */
		public function updateProfile()
		{
			if (Auth::user())
			{
				// $request->user() returns an instance of the authenticated user...
			}
		}

	}

In secondo luogo, puoi avere accesso all'utente autenticato tramite un istanza di `Illuminate\Http\Request`:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class ProfileController extends Controller {

		/**
		 * Update the user's profile.
		 *
		 * @return Response
		 */
		public function updateProfile(Request $request)
		{
			if ($request->user())
			{
				// $request->user() returns an instance of the authenticated user...
			}
		}

	}

In terzo luogo, puoi passare il contract `Illuminate\Contracts\Auth\User`. Puoi aggiungerlo o al costruttore del controller, o al metodo, oppure in qualsiasi altra classe risolta dal [service container](/docs/master/container):

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use Illuminate\Contracts\Auth\User;

	class ProfileController extends Controller {

		/**
		 * Update the user's profile.
		 *
		 * @return Response
		 */
		public function updateProfile(User $user)
		{
			// $user is an instance of the authenticated user...
		}

	}

<a name="route-protette"></a>
## Route Protette

I [Route middleware](/docs/master/middleware) possono essere usati per permettere ai soli utenti autenticati di accedere ad una particolare route. Laravel offre di default il middleware `auth`, definito nel file `app\Http\Middleware\Authenticate.php`. Tutto ciò di cui hai bisogno è appendere questo filtro nella definizione della route:

	// Tramite Route Closure...

	Route::get('profile', ['middleware' => 'auth', function()
	{
		// Only authenticated users may enter...
	}]);

	// Tramite Controller...

	Route::get('profile', ['middleware' => 'auth', 'uses' => 'ProfileController@show']);

<a name="autenticazione-http-basic"></a>
## Autenticazione HTTP Basic

L'autenticazione HTTP Basic offre un modo veloce di autenticare gli utenti nella tua applicazione senza impostare una pagina dedicata di "login". Per inizare, appendi il middleware `auth.basic` alla tua route:

#### Proteggere Una Route Con HTTP Basic

	Route::get('profile', ['middleware' => 'auth.basic', function()
	{
		// Only authenticated users may enter...
	}]);

Di default, il middleware `basic` userà la colonna `email` del record utente come "username".

#### Impostare Un Filtro HTTP Basic Stateless

Puoi inoltre usare l'autenticazione HTTP Basic senza impostare un cookie nella sessione, particolarmente utile per un API di autenticazione. Per fare ciò [definisci un middleware](/docs/master/middleware) che richiami il metodo `onceBasic`:

	public function handle($request, Closure $next)
	{
		return Auth::onceBasic() ?: $next($request);
	}

Se stai usando FastCGI di PHP, l'autenticazione HTTP potrebbe non funzionare correttamente. Per questo, la seguente linea dovrebbe esssere aggiunta al tuo file `.htaccess`:

	RewriteCond %{HTTP:Authorization} ^(.+)$
	RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

<a name="recupero-password-e-reset"></a>
## Recupero Password & Reset

### Modello & Tabella

Molte applicazioni forniscono dei metodi per gestire la password dell’utente e Laravel non è da meno: con Laravel hai a disposizione metodi per inviare la password dimenticata e per resettarla.

Per iniziare, verifica che il model `User` implementi il contract `Illuminate\Contracts\Auth\Remindable`. Ovviamente, il model `User` incluso nel framework implementa già questa interfaccia, ed usa il trait `Illuminate\Auth\Reminders\Remindable` per includere i metodi necessari ad implementare quest'interfaccia.

#### Generare La Migration Reminder Password

Il passo successivo, è quello di creare una tabella per memorizzare il token di reset password. La migration per questa tabella è inclusa tra le funzionalità di Laravel, e si trova nella directory `database/migrations`. In questo modo tutto quello che hai bisogno di fare è eseguire la migration:

	php artisan migrate

### Controller Per Il Remind Della Password

Laravel include anche un controller `Auth\PasswordController` che contiene la logica necessaria ad eseguire il rest della password utente. 
Laravel also includes an `Auth\PasswordController` that contains the logic necessary to reset user passwords. Ti forniamo già le view per facilitarti le cose! Le view si trovano nella directory `resources/views/auth`. Sei libero di modificarle come meglio credi, seguendo il design della tua applicazione.

I tuoi utenti riceveranno una email con un link che punta al metodo `getReset` di `PasswordController`. Questo metodo visualizzerà il form per il reset permettendo agli utenti di modificare la loro password. Dopo che la password è resettata, l'utente verrà automaticamente loggato nell'applicazione e reindirizzato a `/home`. Puoi personalizzare il redirect post-reset impostando la proprietà `redirectTo` in `PasswordController`:

	protected $redirectTo = '/dashboard';

> **Nota:** Di default, il token di reset password scade dopo un'ora. Puoi cambiare questa opzione modificando la voce `reminder.expire` nel file `config/auth.php`.

<a name="autenticazione-social"></a>
## Auutenticazione Social

In aggiunta ai tipici form di autenticazione, Laravel offre anche un modo semplice di autenticazione con i provider Oauth usando il package Laravel Socialite. **Socialite supporta correntemente autenticazioni con Facebook, Twitter, Google, e GitHub.**

Per iniziare ad usare Socialite, includi il package nel tuo file `composer.json`:

	"laravel/socialite": "~2.0"

Successivamente, registra `Laravel/Socialite/SocialiteServiceProvider` nel tuo file di configurazione
`config/app.php`. Puoi anche registrarlo come una [facade](/docs/master/facades):

	'Socialize' => 'Laravel\Socialite\Facades\Socialite',

Avrai bisogno di aggiungere le credenziali per i servizi OAuth  che la tua applicazione usa. Queste credenziali dovrebbero essere inserite nel file di configurazione `config/services.php`, e dovrebbero essere usate le chiavi `facebook`, `twitter`, `google`, o `github`, a seconda del provider che la tua applicazione necessita.
Per esempio:

	'github' => [
		'client_id' => 'la-tua-app-id-github',
		'client_secret' => 'la-tua-app-secret-github',
		'redirect' => 'http://il-tuo-url-callback',
	],

Ora, sei pronto per autenticare gli utenti! Avrai bisogno di due route: una per il redirect utente al provider OAuth, un altra per ricevere il callback dal provider dopo l'autenticazione.
Qui c'è un esempio usando la facade `Socialize`:

	public function redirectToProvider()
	{
		return Socialize::with('github')->redirect();
	}

	public function handleProviderCallback()
	{
		$user = Socialize::with('github')->user();

		// $user->token;
	}

Il metodo redirect si prende cura di inviare l'utente al provider OAuth, mentre il metodo `user` leggerà la richiesta in arrivo e ritroverà le informazioni utente dal provider. Prima di reindirizzare l'utente, puoi anche impostare degli "scopes" sulla richiesta:

	return Socialize::with('twitter')->scopes(['scope1', 'scope2'])->redirect();

Una volta avuta l'istanza utente, puoi ritrovare alcuni dettagli aggiunti sull'utente:

#### Recupero Dettagli Utente

	$user = Socialize::with('github')->user();

	// OAuth Provider Due
	$token = $user->token;

	// OAuth Provider Uno
	$token = $user->token;
	$tokenSecret = $user->tokenSecret;

	// Tutti i Provider
	$user->getNickname();
	$user->getName();
	$user->getEmail();
	$user->getAvatar();
