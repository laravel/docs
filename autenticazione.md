# Autenticazione

- [Introduzione](#introduzione)
- [Autenticazione Rapida](#autenticazione-rapida)
    - [Routing](#routing-incluso)
    - [View](#view-incluse)
    - [Autenticazione](#autenticazione-inclusa)
    - [Recuperare Gli Utenti Autenticati](#recuperare-utenti-autenticati)
    - [Proteggere Le Route](#proteggere-route)
- [Autenticazione Manuale Degli Utenti](#autenticare-utenti)
    - [Ricordarsi Degli Utenti](#ricordarsi-degli-utenti)
    - [Altri Metodi di Autenticazione](#altri-metodi-di-autenticazione)
- [Autenticazione HTTP Basic](#autenticazione-http-basic)
     - [Autenticazione Stateless HTTP Basic](#autenticazione-stateless-http-basic)
- [Resettare Le Password](#resettare-password)
    - [Considerazioni Sul Database](#resettare-database)
    - [Routing](#resettare-routing)
    - [View](#resettare-view)
    - [Dopo Il Reset Password](#dopo-reset-password)
- [Autenticazione Social](#social-authentication)
- [Aggiungere Driver Personalizzati di Autenticazione](#aggiungere-driver-personalizzati-di-autenticazione)

<a name="introduzione"></a>
## Introduzione

Laravel implementa un semplice meccanismo di autenticazione. Infatti, quasi tutto è già configurato “out of the box”. Il file di configurazione si trova in `config/auth.php`, che contiene una serie di opzioni, ben documentate, che userai per ottimizzare il comportamento del tuo servizio di autenticazione. 

### Considerazioni Database

Di default, Laravel include un [model Eloquent](/docs/{{version}}/eloquent) `App\User` nella directory `app`. Questo model può essere usato per il driver Eloquent di autenticazione. Se la tua applicazione non usa Eloquent, puoi usare il driver di autenticazione `database` che fa uso del query builder di Laravel.

Quando costruisci lo schema database per il model `App\User`, assicurati che la colonna password sia lunga almeno 60 caratteri.

Dovresti anche verificare che la tabella `users` (o equivalente) contenga una colonna `remember_token`, stringa nulla, di 100 caratteri. Questa colonna sarà usata per memorizzare un token per le sessioni “remember me” che verranno mantenute dalla tua applicazione. Questo può essere fatto usanto  `$table->rememberToken();` nella migration.

<a name="autenticazione-rapida"></a>
## Autenticazione Rapida

Laravel utilizza due controller legati all'autenticazione, presenti nel namespace `App\Http\Controllers\Auth`. `AuthController` gestisce la registrazione di nuovi utenti e l'autenticazione, mentre `PasswordController` contiene la logica per facilitare il reset della password degli utenti. Ognuno di questi controller usa un trait per includere i metodi necessari. Per molte applicazioni, non avrai bisogno di modificare questi controller.

<a name="routing-incluso"></a>
### Routing

Di default, non sono incluse [route](/docs/{{version}}/routing) per far puntare le richieste ai controller per l'autenticazione. Puoi aggiungerli manualmente nel file `app/Http/routes.php`:

    // Authentication routes...
    Route::get('auth/login', 'Auth\AuthController@getLogin');
    Route::post('auth/login', 'Auth\AuthController@postLogin');
    Route::get('auth/logout', 'Auth\AuthController@getLogout');

    // Registration routes...
    Route::get('auth/register', 'Auth\AuthController@getRegister');
    Route::post('auth/register', 'Auth\AuthController@postRegister');

<a name="view-incluse"></a>
### View

Anche se i controller sono inclusi con il framework, avrai bisogno di fornire delle [view](/docs/{{version}}/views) che verrano mostrate da questi controller. Le view dovrebbero essere memorizzate nella directory `resources/views/auth`. Sentiti libero di personalizzare queste view come meglio desideri. La view per il login dovrebbe essere memorizzata in `resources/views/auth/login.blade.php`, e la view della registrazione in `resources/views/auth/register.blade.php`.

#### Form Di Autenticazione Di Esempio

    <!-- resources/views/auth/login.blade.php -->

    <form method="POST" action="/auth/login">
        {!! csrf_field() !!}

        <div>
            Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            Password
            <input type="password" name="password" id="password">
        </div>

        <div>
            <input type="checkbox" name="remember"> Remember Me
        </div>

        <div>
            <button type="submit">Login</button>
        </div>
    </form>

#### Form Di Registrazione Di Esempio

    <!-- resources/views/auth/register.blade.php -->

    <form method="POST" action="/auth/register">
        {!! csrf_field() !!}

        <div class="col-md-6">
            Name
            <input type="text" name="name" value="{{ old('name') }}">
        </div>

        <div>
            Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            Password
            <input type="password" name="password">
        </div>

        <div class="col-md-6">
            Confirm Password
            <input type="password" name="password_confirmation">
        </div>

        <div>
            <button type="submit">Register</button>
        </div>
    </form>

<a name="autenticazione-inclusa"></a>
### Autenticare

Ora che hai impostato le route e le view per i controller di autenticazione, sei pronto a registrare ed autenticare nuovi utenti per la tua applicazione. Puoi accedere alle route con il browser. I controller di autenticazione contengono già la logica (tramite i loro trait) per autenticare utenti esistenti e salvarne di nuovi nel database.

Quando un utente viene autenticato correttamente, saranno reindirizzati all'URI `/home`, che è necessario impostare una route per gestire questa richiesta. Puoi personalizzare il redirect post-autenticazione definendo la proprietà `redirectTo` in `AuthController`:

    protected $redirectTo = '/dashboard';

#### Personalizzazioni

Per modificare i campi del form che sono richiesti quando si registra un nuovo utente alla tua applicazione, o per personalizzare la modalità di inserimento dei record utenti nel database, puoi modificare la classe `AuthController`. Questa classe è responsabile della validazione e della creazione di nuovi utenti per la tua applicazione.

Il metodo `validator` di `AuthController` contiene le regole di validazione per i nuovi utenti dell'applicazione. Sei libero di modificare questo metodo come meglio desideri.

Il metodo `create` di `AuthController` è responsabile della creazione di nuovi record `App\User` nel database usando [Eloquent ORM](/docs/{{version}}/eloquent). Sei libero di modificare questo metodo a seconda dei bisogni del tuo database.

<a name="recuperare-utenti-autenticati"></a>
### Recupeare L'Utente Autenticato

Puoi accedere all'utente autenticato tramite la facade `Auth`:

    $user = Auth::user();

In alternativa, una volta autenticato, puoi accedere all'utente tramite una istanza di `Illuminate\Http\Request`:

    <?php namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use Illuminate\Routing\Controller;

    class ProfileController extends Controller
    {
        /**
         * Update the user's profile.
         *
         * @param  Request  $request
         * @return Response
         */
        public function updateProfile(Request $request)
        {
            if ($request->user()) {
                // $request->user() returns an instance of the authenticated user...
            }
        }
    }

#### Determinare Se L'Utente Corrente E' Autenticato

Per determinare se un utente è già loggato nella tua applicazione, puoi usare il metodo `check` sulla facade `Auth`, che ritornerà `true` se l'utente è autenticato:

    if (Auth::check()) {
        // The user is logged in...
    }

Tuttavia, puoi usare un middleware per verificare che l'utnete sia autenticato prima di permettergli l'accesso a certe route / controller. Per saperne di più riguardo, dai uno sguardo alla documentazione  su come [proteggere le route](/docs/{{version}}/authentication#protecting-routes).

<a name="proteggere-le-route"></a>
### Proteggere Le Route

[I middleware delle route](/docs/{{version}}/middleware) possono essere usato per permettere solo agli utenti autenticati di accedere a certe route. Per farlo Laravel usa il middleware `auth`, definito in `app\Http\Middleware\Authenticate.php`. Tutto quello che hai bisogno di fare è agganciare il middleware nella definizione della route:

    // Using A Route Closure...

    Route::get('profile', ['middleware' => 'auth', function() {
        // Only authenticated users may enter...
    }]);

    // Using A Controller...

    Route::get('profile', [
        'middleware' => 'auth',
        'uses' => 'ProfileController@show'
    ]);

Ovviamente, se stai usando i [controller](/docs/{{version}}/controllers), puoi usare il metodo `middleware` dal costruttore del controller invece di agganciarlo nella definizione di una route:

    public function __construct()
    {
        $this->middleware('auth');
    }

<a name="utenti-autenticati"></a>
## Utenti Autenticati Manualmente

Ovviamente, non sei obbligato ad usare i controller per l'autenticazione inclusi con Larave. Se scegli di rimuovere questi controller, avrai bisogno di gestire l'autenticazione degli utenti direttamente con le classi di autenticazione di Laravel. Non preoccuparti, è un gioco da ragazzi!

Puoi accedere ai servizi di autenticazione di Laravrel tramite la [facade](/docs/{{version}}/facades) `Auth`, quindi assicurati di importare la facade `Auth` in cima al file della classe. Successivamente, controlla il metodo `attempt`:

    <?php namespace App\Http\Controllers;

    use Auth;
    use Illuminate\Routing\Controller;

    class AuthController extends Controller
    {
        /**
         * Handle an authentication attempt.
         *
         * @return Response
         */
        public function authenticate()
        {
            if (Auth::attempt(['email' => $email, 'password' => $password])) {
                // Authentication passed...
                return
 redirect()->intended('dashboard');
            }
        }
    }

Il metodo `attempt` accetta un array di coppie chiave / valore come primo parametro. I valori nell'array saranno usato per ritrovare l'utente nella tabella del database. Quindi, nell'esempio sopra, l'utente sarà ricercato dal valore della colonna `email`. Se l'utente viene trovato, la password criptata nel database sarà confrontata con il valore `password` passato al metodo tramite array. Se le due password coincidono sarà inizializzata una sessione di autenticazione per l'utente.

Il metodo `attempt` ritornerà `true` se l'autenticazione avrà successo. Altrimenti verrà ritornato `false`.

Il metodo `intended` reindirizzerà l'utente all'URL al quale aveva tentato di accedere prima di pssare sotto al controllo del filtro di autenticazione. A questo metodo può essere assegnato un URI fallback,in caso la destinazione richiesta non sia disponibile.

Se lo derisderi, puoi anche aggiunere delle condizioni extra alla query di autenticazione in aggiunta ad email e password. Per esempio, potresti verificare che l'utente sia marchiato come “attivo”:

    if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
        // The user is active, not suspended, and exists.
    }

Per disconnettere gli utenti dalla tua applicazione, puoi usare il metodo `logout` sulla facade `Auth`. Questo cancellerà le informazioni di autenticazione presenti nella sessione utente:

    Auth::logout();

> **Nota:** In questi esempi, l' `email` non è un opzione obbligatoria,is not a required option, viene semplicemente usata come esempio. Dovresti usare qualsiasi colonna corrisponda allo "username" nel tuo database.

<a name="ricordare-utenti"></a>
## Ricodarsi Degli Utenti

Se vuoi fornire la funzionalità di “ricordati di me” nella tua applicazione, puoi passare un valore booleano come secondo parametro del metodo `attempt`, che manterrà attiva l'autenticazione utente indefinitamente, o fino al logout manuale dell'utente. Ovviamente, la tabella `users` deve includere la colonna `remember_token`, che verrà usata per memorizzare il token “ricordati di me”.

    if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
        // The user is being remembered...
    }

Se stai “ricordando” gli utenti, puoi usare il metodo `viaRemember` per determinare se un utente è stato autenticato usando il cookie "remember me":

    if (Auth::viaRemember()) {
        //
    }

<a name="altri-metodi-di-autenticazione"></a>
### Altri Metodi Di Autenticazione

#### Autenticare Una Istanza Utente

Se hai bisogno di autenticare un utente esistente nella tua applicazione, puoi richiamare il metodo `login` con l'istanza utente. L'oggetto deve essere un implementazione del [contract](/docs/{{version}}/contracts) `Illuminate\Contracts\Auth\Authenticatable`. Ovviamente, il model `App\User` include già l'implementazione a questa interfaccia:

    Auth::login($user);

#### Autenticare Un Utente Tramite ID

Per autenticare un utente nell'applicazione tramite il suo id, puoi usare il metodo `loginUsingId`. Questo metodo accetta semplicemente la chiave primaria dell'utente che vuoi autenticare:

    Auth::loginUsingId(1);

#### Autenticare Un Utente Una Sola Volta

Puoi usare il metodo `once` per autenticare un utente nell'applicazione per una singola richiesta. Nessuna sesisone o nessun cookie saranno utilizzati, che può essere utile quando si realizza un sistema di API. Il metodo `once` ha la stessa signature del metodo `attempt`:

    if (Auth::once($credentials)) {
        //
    }

<a name="autenticazione-http-basic"></a>
## Autenticazione HTTP Basic

[L'autenticazione HTTP Basic](http://en.wikipedia.org/wiki/Basic_access_authentication) offre un modo veloce per autenticare gli utenti della tua applicazione senza impostare una pagina dedicata di “login”. Per iniziare, aggancia il [middleware](/docs/{{version}}/middleware) `auth.basic` alla tua route. Il middleware `auth.basic` è incluso con Laravel, in questo modo non hai bisogno di definirlo:

    Route::get('profile', ['middleware' => 'auth.basic', function() {
        // Only authenticated users may enter...
    }]);

Una volta agganciato il middleware alla route, ti sarà richiesto automaticamente di inserire le credenziali quando si tenterà di accedere alla route dal tuo browser. Di default, il middleware `auth.basic` userà la colonna `email` column sul record utente come "username".

#### Una Nota Su FastCGI

Se stai usando PHP FastCGI, l'autenticazione HTTP Basic potrebbe non funzionare correttamente. Le seguenti linee dovrebbero essere aggiunte al tuo file`.htaccess`:

    RewriteCond %{HTTP:Authorization} ^(.+)$
    RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

<a name="autenticazione-stateless-http-basic"></a>
### Autenticazione Stateless HTTP Basic

Puoi anche usare l'autenticazione HTTP Basic Authentication senza impostare un cookie di identificazione nella sessione, che è particolarmente utile in caso di autenticazione tramite API. Per farlo, [definisci un middleware](/docs/{{version}}/middleware) che richiami il metodo `onceBasic`. Se non vinee ritornata nessuna risposta dal metodo `onceBasic`, la richiesta può essere passata all'interno dell'applicazione:

    <?php namespace Illuminate\Auth\Middleware;

    use Auth;
    use Closure;
    use Illuminate\Contracts\Routing\Middleware;

    class AuthenticateOnceWithBasicAuth implements Middleware
    {
        /**
         * Handle an incoming request.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @return mixed
         */
        public function handle($request, Closure $next)
        {
            return Auth::onceBasic() ?: $next($request);
        }

    }

Il passo successivo, è di [registrare il middleware](/docs/{{version}}/middleware#registering-middleware) ed agganciarlo alla route:

    Route::get('api/user', ['middleware' => 'auth.basic.once', function() {
        // Only authenticated users may enter...
    }]);

<a name="reset-password"></a>
## Reset Password

<a name="reset-database"></a>
### Considerazioni Sul Database

La maggior parte delle applicazioni web fornisce un modo, ai propri utenti, di resettare le proprie password. Piuttosto che forzare l'implementazione per ogni applicazione di questa funzionalità, Laravel ti offre dei metodi convenienti per l'invio di password reminder e per eseguire reset delle password.

Per cominciare, verifica che il tuo model `App\User` implementi il contract `Illuminate\Contracts\Auth\CanResetPassword`. Ovviamente, il model `App\User` incluso con il framework implementa già questa interfaccia, ed usa il trait `Illuminate\Auth\Passwords\CanResetPassword` per includere i metodi necessari ad implementare l'interfaccia.

#### Generare Il Reset Token

Successivamente, deve essere creata una tabella per memorizzare i reset token. La migration per questa tabella è inclusa con Laravel, e risiede nella directory `database/migrations`. Così, tutto quello di cui hai bisogno è di eseguire le migration in questo modo:

    php artisan migrate

<a name="routing-di-reset"></a>
### Routing

Laravel include un controller `Auth\PasswordController` che contiene la logica necessaria per resettare la password degli utenti. Tuttavia, avrai bisogno di definire delle route per far puntare le richieste di questo controller:

    // Password reset link request routes...
    Route::get('password/email', 'Auth\PasswordController@getEmail');
    Route::post('password/email', 'Auth\PasswordController@postEmail');

    // Password reset routes...
    Route::get('password/reset/{token}', 'Auth\PasswordController@getReset');
    Route::post('password/reset', 'Auth\PasswordController@postReset');

<a name="view-di-reset"></a>
### Views

In aggiunta alla definizione delle route per `PasswordController`, avrai bisogno di fornire delle view che saranno ritornate da questo controller. Non preoccuparti, ti verranno fornite delle view di esempio per iniziare. Ovviamente, sei libero di stilizzare i tuoi form come meglio desideri.

#### Form Di Richiesta Link Reset Password  Di Esempio

Avrai bisogno di fornire una view HTML per il form di richiesta di reset password. Questa view dovrebbe essere salvata in `resources/views/auth/password.blade.php`. Questo form contiene un singolo campo per l'email dell'utnete, permettendogli la richiesta di link per il reset della password:

    <!-- resources/views/auth/password.blade.php -->

    <form method="POST" action="/password/email">
        {!! csrf_field() !!}

        <div>
        	Email
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            <button type="submit">
                Send Password Reset Link
            </button>
        </div>
    </form>

Quando un utente invia una richiesta di reset della password, riceverà un'email con un link che punta al metodo `getReset` (normalmente indirizzato a `/password/reset`) di `PasswordController`. Avrai bisogno di creare una view per questa email in `resources/views/emails/password.blade.php`. La view riceverà una variabile `$token` che contiene il token di reset password per confrontare la richiesta di reset dell'utente. Qui un esempio di view per l'email per iniziare:

    <!-- resources/views/emails/password.blade.php -->

    Click here to reset your password: {{ url('password/reset/'.$token) }}

#### Form Di Reset Password Di Esempio

Quando un utente clicca sul link contenuto nella email per resettare la password, sarà visualizzato un form per il reset della password. Questa view dovrebbe essere salvata in `resources/views/auth/reset.blade.php`.

Qui un esempio di form di reset password per iniziare:

    <!-- resources/views/auth/reset.blade.php -->

    <form method="POST" action="/password/reset">
        {!! csrf_field() !!}
        <input type="hidden" name="token" value="{{ $token }}">

        <div>
            <input type="email" name="email" value="{{ old('email') }}">
        </div>

        <div>
            <input type="password" name="password">
        </div>

        <div>
            <input type="password" name="password_confirmation">
        </div>

        <div>
            <button type="submit">
                Reset Password
            </button>
        </div>
    </form>

<a name="dopo-il-reset-password"></a>
### Dopo Il Reset Password

Una volta che hai definito le route e le view per il reset della password dei tuoi utenti, puoi accedere alle route dal tuo browser. Il `PasswordController` incluso con il framweork include già la logica per inviare il link di reset password così come l'update della password nel database.

Dopo che la password è stata resettata, l'utente sarà automaticamente loggato all'interno dell'applicazione e reindirizzato in `/home`. Puoi personalizzare il redirect post reset password definendo la proprietà `redirectTo` all'interno di `PasswordController`:

    protected $redirectTo = '/dashboard';

> **Nota:** Di default, il token di reset password perde validità dopo un ore. Puoi cambiare il tempo di validità tramite l'opzione `reminder.expire` del file `config/auth.php`.

<a name="autenticazione-social"></a>
## Autenticazione Social

In aggiunta ai tipici form di autenticazione, Laravel offre anche un semplice e conveniente modo per autenticare tramite provider OAuth usando [Laravel Socialite](https://github.com/laravel/socialite). Socialite attualmente supporta autenticazioni con Facebook, Twitter, Google, GitHub e Bitbucket.

Per iniziare ad usare Socialite, aggiungilo come dipendenza nel tuo file `composer.json`:

    composer require laravel/socialite

### Configurazione

Dopo aver installato le librerie Socialite, registra `Laravel\Socialite\SocialiteServiceProvider` nel file di configurazione `config/app.php`:

    'providers' => [
        // Other service providers...

        'Laravel\Socialite\SocialiteServiceProvider',
    ],

Aggiungi anche, la facade `Socialite` all'array `aliases` nel file di configurazione `app`:

    'Socialite' => 'Laravel\Socialite\Facades\Socialite',

Avrai bisogno anche di aggiungere le credenziali per i servizi OAuth utilizzati dalla tua applicazione. Queste credenziali dovranno essere memorizzate nel file `config/services.php`, e dovreti usare la chiave `facebook`, `twitter`, `google`, o `github`, a seconda del provider richiesto dalla tua applicazione. Per esempio:

    'github' => [
        'client_id' => 'your-github-app-id',
        'client_secret' => 'your-github-app-secret',
        'redirect' => 'http://your-callback-url',
    ],

### Uso Base

Ora, sei pronto ad autenticare gli utenti! Avrai bisogno di due route: una per il redirect degli utenti al provider OAuth, ed un altra per ricevere il callback dal providere dopo l'autenticazione. Accederemo a Socialite usando la [facade](/docs/{{version}}/facades) `Socialite`:

    <?php namespace App\Http\Controllers;

    use Illuminate\Routing\Controller;

    class AuthController extends Controller
    {
        /**
         * Redirect the user to the GitHub authentication page.
         *
         * @return Response
         */
        public function redirectToProvider()
        {
            return Socialite::driver('github')->redirect();
        }

        /**
         * Obtain the user information from GitHub.
         *
         * @return Response
         */
        public function handleProviderCallback()
        {
            $user = Socialite::driver('github')->user();

            // $user->token;
        }
    }

Il metodo `redirect` si prende cura di inviare l'utente al provider OAuth, mentre il metodo `user` leggerà la richiesta in arrivo e ritroverà le informazioni dell'utente dal provider. Prima di reindirizzare l'utente, puoi anche impostare degli "scopes" sulla richiesta con il metodo
 `scope`. Questo metodo sovrascriverà tutti gli “scopes” esistenti:

    return Socialite::driver('github')
                ->scopes(['scope1', 'scope2'])->redirect();

#### Recuperare I Dettagli Utente

Una volta ritornata un istanza uente, puoi accedere ad alcuni dettagli sull'utente:

    $user = Socialite::driver('github')->user();

    // OAuth Two Providers
    $token = $user->token;

    // OAuth One Providers
    $token = $user->token;
    $tokenSecret = $user->tokenSecret;

    // All Providers
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();

<a name="aggiungere-driver-personalizzati-di-autenticazione"></a>
## Aggiungere Driver Personalizzati Di Autenticazione

Se non stai usando un tradizionale database relazionale per memorizzare i tuoi utenti, avrai bisogno di estendere Laravel con il tuo driver di autenticazione. Useremo il metodo `extend` sulla facade `Auth` per definire un driver personalizzato. Dovresti inserire questa chiamata ad `extend` all'interno del [service provider](/docs/{{version}}/providers):

    <?php namespace App\Providers;

    use Auth;
    use App\Extensions\RiakUserProvider;
    use Illuminate\Support\ServiceProvider;

    class AuthServiceProvider extends ServiceProvider
    {
        /**
         * Perform post-registration booting of services.
         *
         * @return void
         */
        public function boot()
        {
            Auth::extend('riak', function($app) {
                // Return an instance of Illuminate\Contracts\Auth\UserProvider...
                return new RiakUserProvider($app['riak.connection']);
            });
        }

        /**
         * Register bindings in the container.
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

Dopo aver registrato il driver con il metodo `extend`, puoi passare al nuovo driver impostandolo nel file di configurazione `config/auth.php`.

### Il Contract User Provider

Le implementazioni di `Illuminate\Contracts\Auth\UserProvider` sono responsabili soltanto per il recupero di un implementazione di `Illuminate\Contracts\Auth\Authenticatable` da un sistema persistente di memorizzazione, come MySQL, Riak, ecc. Queste due interfacce permettono al meccanismo di autenticazione di Laravel di continuare a funzionare indipendentemente da come gli utenti vengono memorizzati o dal tipo di classe usata per rappresentarli.

Dai un'occhiata al contract `Illuminate\Contracts\Auth\UserProvider`:

    <?php namespace Illuminate\Contracts\Auth;

    interface UserProvider {

        public function retrieveById($identifier);
        public function retrieveByToken($identifier, $token);
        public function updateRememberToken(Authenticatable $user, $token);
        public function retrieveByCredentials(array $credentials);
        public function validateCredentials(Authenticatable $user, array $credentials);

    }

La funzione `retrieveById` tipicamente riceve una chiave rappresentante l'utente, come ad esempio un id auto-incrementante da un database MySQL. L'implementazione `Authenticatable` controlla l'ID e dovrebbe ritornarlo al metodo.

La funzione `retrieveByToken` recupera un utente tramite un identificatore unito `$identifier` e il `$token` "remember me", memorizzato nel campo `remember_token`. Come col metodo precedente, verrà ritornata un implementazione di `Authenticatable`.

Il metodo `updateRememberToken` aggiorna il campo `remember_token` dell'utente `$user` con un nuovo `$token`. Il nuovo token può essere un nuovo token, assegnato con un login “ricordati di me”, oppure null se l'utente effettua il logout.

Il metodo `retrieveByCredentials` riceve un array di credenziali passate al metodo `Auth::attempt` quando si tenta di loggarsi nell'applicazione. Il metodo dovrebbe quindi eseguire una query nel sistema persistente di memorizzazione per l'utente corrispondete a quelle credenziali. Normalmente, questo metodo esegue una query con una condizione "where" su `$credentials['username']`. Il metodo dovrebbe quindi ritornare un implementazione di `UserInterface`. **Questo metodo non dovrebbe eseguire nessuna validazione della password o dell'autenticazione.**

Il metodo `validateCredentials` confronta l'utente `$user` con `$credentials` per autenticarlo. Per esempio, questo metodo potrebbe confrontare la stringa `$user->getAuthPassword()` con un `Hash::make` di`$credentials['password']`. Questo metodo dovrebbe validare soltanto le credenziali dell'utente e ritornare un booleano.

### Il Contract Authenticatable

Ora che abbiamo analizzato ogni metodo di `UserProvider`, dai un'occhiata ad `Authenticatable`. Ricorda, il provider dovrebbe ritornare un implementazione di questa interfaccia dai metodi `retrieveById` e `retrieveByCredentials`:

    <?php namespace Illuminate\Contracts\Auth;

    interface Authenticatable {

        public function getAuthIdentifier();
        public function getAuthPassword();
        public function getRememberToken();
        public function setRememberToken($value);
        public function getRememberTokenName();

    }

Quest'interfaccia è semplice. Il metodo `getAuthIdentifier` dovrebbe ritornare la "primary key" di un utente. In un database MySQL, ancora una volta, questo valore dovrebbe corrispondere ad una primary key auto-incrementante. `getAuthPassword` dovrebbe ritornare la password criptata dell'utente. Questa interfaccia permette al sistema di autenticazione di lavorare con qualsiasi classe User, indipendentemente da quale ORM o sistema di memorizzazione astratto tu stia usando. Di default, Laravel include una classe `User` nella directory `app` che implementa queste interfacce, così puoi consultare questa classe per un implementazione di esempio.
