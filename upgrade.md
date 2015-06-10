# Upgrade Guide

- [Aggiornamento Alla 5.1.0](#aggiornamento-5.1.0)
- [Aggiornamento Alla 5.0.16](#aggiornamento-5.0.16)
- [Aggiornamento Alla 5.0 Dalla 4.2](#aggiornamento-5.0)
- [Aggiornamento Alla 4.2 Dalla 4.1](#aggiornamento-4.2)
- [Aggiornamento Alla 4.1.29 Dalla <= 4.1.x](#aggiornamento-4.1.29)
- [Aggiornamento Alla 4.1.26 Dalla <= 4.1.25](#aggiornamento-4.1.26)
- [Aggiornamento Alla 4.1 Dalla 4.0](#aggiornamento-4.1)

<a name="aggiornamento-5.1.0"></a>
## Aggiornamento Alla 5.1.0

#### Tempo stimato per l'aggiornamento: Meno di 1 ora

### Aggiornare `bootstrap/autoload.php`

Aggiorna la variabile `$compiledPath` in `bootstrap/autoload.php` come di seguito:

	$compiledPath = __DIR__.'/cache/compiled.php';

### Crea la Directory `bootstrap/cache`

All'interno della tua directory `bootstrap`, crea una directory `cache` (`bootstrap/cache`). Inserisci, all'interno di questa directory, un file `.gitignore` con il seguente contenuto:

	*
	!.gitignore

Questa directory dovrebbe essere scrivibile, e sarà usata dal framework per memorizzare file temporanei di ottimizzazione come `compiled.php`, `routes.php`, `config.php`, e `services.json`.

### Autenticazione

Se stai usando `AuthController` che utilizza il trait `AuthenticatesAndRegistersUsers`, avrai bisogno di apportare alcune modifiche di come i nuovi utenti sono convalidati e creati.

Per prima cosa, non hai più bisogno di passare le istanze `Guard` e `Registrar` al costruttore base. Puoi rimuovere completamente queste dipendenze dal costruttore del tuo controller.

In secondo luoigo, la classe `App\Services\Registrar` usata in Laravel 5.0 non è più necessaria. Puoi semplicemente copiare ed incolare i metodi `validator` e `create` da questa classe direttamente in `AuthController`. Non sono necessari altri cambiamenti per questi metodi; comunque, devi essere sicuro di importare la facade `Validator` e il model `User` all'interno di `AuthController`.

#### Password Controller

Il controller per la gestione del recupero password `PasswordController` non richiede nessuna dipendenza nel suo costruttore. Puoi rimuovere entrambe le dipendenze che erano richieste sotto la versione 5.0.

### Validazione

Se stai sovrascrivendo il metodo `formatValidationErrors` nella tua classe controller di base, dovrai richiamare il contract `Illuminate\Contracts\Validation\Validator` invece dell'istanza concreta `Illuminate\Validation\Validator`.

Allo stesso modo, se stai sovrascrivendo il metodo `formatErrors` nella classe form request di base, dovrai richiamare il contract `Illuminate\Contracts\Validation\Validator`invece dell'istanza concreta `Illuminate\Validation\Validator`.

### Eloquent

#### Il Metodo `create`

Il metodo create di Eloquent può ora essere chiamato senza nessun parametro. Se stai sovrascrivendo il metodo `create` nei tuoi model, imposta il valore di default del parametro `$attributes` ad un array:

	public static function create(array $attributes = [])
	{
		// Your custom implementation
	}

#### Il Metodo `find`

Se stai sovrascrivendo il metodo `find` nei tuoi model e richiamando `parent::find()` all'interno del tuo metodo personalizzato, dovrai ora cambiarlo per richiamare il metodo `find` dal query builder di Eloquent:

	public static function find($id, $columns = ['*'])
	{
		$model = static::query()->find($id, $columns);

		// ...

		return $model;
	}

#### Formattazione Date

Precedentemente, il formato di memorizzazione per i campi data di Eloquent poteva essere modificando sosvrascivendo il metodo `getDateFormat` nel tuo model. Questo è ancora possibile; tuttavia, per convenienza puoi semplicemente specificare una proprietà `$dateFormat` nel tuo model anzichè sovrascrivere il metodo.

Il formato delle date è anche ora applicabile durante la serializzazione di un model in un `array` o in JSON. Questo potrebbe cambiare il formato dei campi data JSON serializzati durante la migrazione da Laravel 5.0-5.1. Per impostare uno specifico formato date per i model serializzati, puoi sovrascrivere il metodo `serializeDate(DateTime $date)` nel tuo model. Questo metodo ti permette di avere un controllo dettagliato sulla formattazione dei campi date di Eloquent serializzati senza cambiare il formato di memorizzazione. 

### La Classe Collection

#### Il Metodo `sortBy`

Il metodo `sortBy` ora ritorna una nuova istanza di una collection invece di modificare quella esistente:

	$collection = $collection->sortBy('name');

#### Il Metodo `groupBy`

Il metodo `groupBy` ora ritorna una istanza `Collection` per ogni elemento nella `Collection` genitore. Se vuoi convertire di nuovo tutti gli elementi in un array, puoi usare il metodo `map`:

	$collection->groupBy('type')->map(function($item)
	{
		return $item->all();
	});

#### Il Metodo `lists`

Il metodo `lists` ora ritorna una istanza di una `Collection`. Se vuoi convertire la `Collection` in un array, usa il metodo `all`:

	$collection->lists('id')->all();

### Comandi & Handler

La directory `app/Commands` è stata rinominata in `app/Jobs`. Comunque, non sei obbligato a spostare tutti i tuoi comandi nella nuova posizione, e puoi continuare ad usare i comandi Artisan `make:command` e `handler:command` per generare le tue classi.

Allo stesso modo, la directory `app/Handlers` è stata rinominata in `app/Listeners` ed ora contiene solo i listener degli eventi. Comunque, non sei obbligato a spostare o rinominare i tuoi comandi ed handler esistenti, e puoi continuare ad usare il comando `handler:event` per generare gli handler delgi eventi.

Per offrire una retro compatibilità con la struttura di cartella di Laravel 5.0, puoi aggiornare la tua applicazione a Laravel 5.1 e lentamente aggiornare i tuoi eventi e comandi nelle loro nuove posizioni quando è più conveniente per te o per il tuo team.

### Amazon Web Services SDK

Se stai usando il driver per la coda AWS SQS o il driver per l'email AWS SES, ricortdati di installare la versione di AWS PHP SDK 3.0.

### Deprecati

Le seguenti funzionalità di Laravel sono state deprecate e verranno rimosse completamente con la release di Laravel 5.2 a Dicembre 2015.

<div class="content-list" markdown="1">
- I filtri delle route sono stati deprecati in favore dei [middleware](/docs/{{version}}/middleware).
- Il contract `Illuminate\Contracts\Routing\Middleware` è deprecato. Non è necessario nessun contract nei tuoi middleware. In aggiunta, anche il contract `TerminableMiddleware` è deprecato. Invece di implementare l'interfaccia, semplicemente definisci un metodo `terminate` nel tuo middleware.
- Il contract `Illuminate\Contracts\Queue\ShouldBeQueued` è deprecato in favore di `Illuminate\Contracts\Queue\ShouldQueue`.
- Iron.io “code push” è deprecato in favore del tipico Iron.io code e [queue listeners](/docs/{{version}}/queues#running-the-queue-listener).
- Il trait `Illuminate\Foundation\Bus\DispatchesCommands` è deprecato e rinominato in `Illuminate\Foundation\Bus\DispatchesJobs`.
- `Illuminate\Container\BindingResolutionException` è stato spostato in `Illuminate\Contracts\Container\BindingResolutionException`.
- Il metodo del service container `bindShared` è deprecato in favore del metodo `singleton`.
- Il metodo `pluck` di Eloquent e del query builder è deprecato e rinominato in `value`.
- Il metodo `fetch` delle collection è deprecato method has been deprecated in favor of the `pluck` method.
- L'helper `array_fetch` è deprecato in favore del metodo `array_pluck`.
</div>

<a name="aggiornamento-5.0.16"></a>
## Aggiornamento alla 5.0.16

Nel tuo file `bootstrap/autoload.php` file, aggiorna la variabile `$compiledPath` in questo modo:

	$compiledPath = __DIR__.'/../vendor/compiled.php';

<a name="aggiornamento-5.0"></a>
## Aggiornamento Alla 5.0 Dalla 4.2

### Nuova Installazione, Successiva Migrazione

Il modo migliore di migrare un'applicazione creata con Laravel 4.2 è, innanzitutto, installare una nuova copia di un progetto vuoto con la 5.0. Quindi, in un secondo step, copiare i file dell'applicazione 4.2. Precisamente, i controller, le routes, model di Eloquent, comandi Artisan, asset e tutto ciò che è specifico dell'applicazione.

Per iniziare, quindi, [installa una nuova applicazione con Laravel 5](/docs/{{version}}/installation) in una nuova directory. Discuteremo nel dettaglio di ogni step necessario del processo di migrazione di seguito.

### Dipendenze Composer & Package

Non scordarti, innanzitutto, di copiare ogni dipendenza nella tua nuova applicazione. Tali dipendenze includono ovviamente anche i vari SDK e codici di terze parti.

Alcuni package specifici per Laravel possono non essere compatibili con l'iniziale release di Laravel 5. Controlla quindi il maintainer del package per determinare la versione appropriata per Laravel 5. Ad ogni modo, una volta copiate le dipendenze, esegui il comando composer update.


### Namespacing

Di default, Laravel 4 non usa i namespace nell'application code. Quindi, per esempio, tutti i model Eloquent ed i controller "vivono" in un namespace globale. Nulla ti vieta, se vuoi velocizzare le cose, di lasciare in un namespace globale queste classi.

### Configurazione

#### Migrare le Variabili di Ambiente

Copia il nuovo file .env.example in .env, che è appunto l'equivalente '5.0' del vecchio file `.env.php`. Imposta i vari valori più appropriati, come APPENV_ e APPKEY_, le credenziali del database ed i driver di sessione e caching.

In aggiunta, copia qualsiasi valore personalizzato tu abbia nel vecchio file `.env.php` e ricopiali in `.env` (che userai per davvero) ed `.env.example` (un sample che userai con gli altri membri del tuo team).

Per altre informazioni sulla configurazione degli ambienti, dai uno sguardo [alla documentazione](/docs/{{version}}/installation#environment-configuration).

> **Nota:** Avrai bisogno di sistemare adeguatamente il file .env sul tuo server prima di effettuare il deploy!

#### File di Configurazione

Laravel 5.0 non usa più le directory `app/config/{nomeambiente}` per fornire file di configurazione specifici in base all'ambiente di lavoro usato.
Al loro posto, sposta i valori che in base all'ambiente possono cambiare in .env, quindi accedici usando la funzione env('key', 'default value'). Vedari esempi su questo meccanismo nel file di configurazione `config/database.php`.

Imposta i files di configurazione nella directory `config/` per rappresentare i valori associati al tuo ambiente, oppure usa `env()` per impostarli e caricare i valori a seconda dell'ambiente di configurazione scelto.

Ricorda, se aggiungi più valori al file .env fallo anche per .env.example, se lavori in team.

### Route

Copia ed incolla il tuo vecchio file `routes.php` in `app/Http/routes.php`.

### Controller

Successivamente, sposta tutti i tuoi controller nella directory `app/Http/Controllers`. Visto che in questa "guida" non effettueremo una migrazione completa che include anche i namespace, aggiungi la directory `app/Http/Controllers` alla direttiva `classmap` del tuo file `composer.json`. Rimuovi quindi il namespace dalla classe astratta `app/Http/Controllers/Controller.php`. Verifica che i tuoi controller estendano questa classe base.

Nel tuo file `app/Providers/RouteServiceProvider.php`, imposta la proprietà `namespace` a `null`.

### Filtri delle Route

Copia i binding dei tuoi filtri da `app/filters.php` ed aggiungili al metodo `boot()` di `app/Providers/RouteServiceProvider.php`. Aggiungi `use Illuminate\Support\Facades\Route;` in `app/Providers/RouteServiceProvider.php` per continuare ad usare la Facadce `Route`.

Non hai bisogno di spostare qualsisi filtro di default di Laravel 4.0 come `auth` e `csrf`; sono entrambi presenti, ma come middleware. Dovrai invece modificare le route o i controller che li richiedono, trasformando ad esempio il filtro `['before' => 'auth']`in `['middleware' => 'auth']`.

I filtri non sono stati rimossi in Laravel 5. Puoi comunque usarli tramite `before` ed `after`.

### CSRF Globale

Di default, la [protezione CSRF](/docs/{{version}}/routing#csrf-protection) è abilitata su tutte le route. Se preferisci disabiltarla, o attivarla manualmente solo per alcune route, rimuovi questa linea dall'array del file `App\Http\Kernel`:

	'App\Http\Middleware\VerifyCsrfToken',

Se vuoi usarlo altrove, aggiungi questa linea a `$routeMiddleware`:

	'csrf' => 'App\Http\Middleware\VerifyCsrfToken',

Ora puoi aggiungere il middleware ad una singola route / controller usando `['middleware' => 'csrf']` sulla route. Per maggiori infomrazioni sui middleware, consulta la [documentazione ufficiale](/docs/{{version}}/middleware).

### Model Eloquent

Sentiti libero di creare una nuova directory `app/Models` per ospitare i tuoi model Eloquent. Ancora una volta, aggiungi questa eventuale directory alla direttiva `classmap` del tuo file `composer.json`.

Aggiorna i vari model che usano il trait `SoftDeletingTrait` in modo tale che usino `Illuminate\Database\Eloquent\SoftDeletes`.

#### Eloquent Caching

Eloquent non offre più il metodo `remember` per il caching delle query. Sei ora "responsabile" di tale operazione che dovrai effettuare manualmente usando la funzione `Cache::remember`. Per maggiori informazioni sul caching, consulta la [documentazione ufficiale](/docs/{{version}}/cache).

### Model Per L'Autenticazione dell'Utente

Per aggiornare il tuo model `User` per il sistema di autenticazione di Laravel 5, segui le seguenti isrtuzioni:

**Elimina le seguenti linee dal blocco `use`:**

```php
use Illuminate\Auth\UserInterface;
use Illuminate\Auth\Reminders\RemindableInterface;
```

**Aggiungi le seguenti linee al blocco `use`:**

```php
use Illuminate\Auth\Authenticatable;
use Illuminate\Auth\Passwords\CanResetPassword;
use Illuminate\Contracts\Auth\Authenticatable as AuthenticatableContract;
use Illuminate\Contracts\Auth\CanResetPassword as CanResetPasswordContract;
```

**Rimuovi le interfacce UserInterface e RemindableInterface.**

**Segna la classe come implementazione delle seguenti interfacce:**

```php
implements AuthenticatableContract, CanResetPasswordContract
```

**Includi i seguenti trait all'interno della dichiarazione della classe:**

```php
use Authenticatable, CanResetPassword;
```

**Se le usi, rimuovi `Illuminate\Auth\Reminders\RemindableTrait` e `Illuminate\Auth\UserTrait` dal blocco use e dalla dichiarazione della classe.**

### Cambiamenti a User Cashier

Il nome dei trait e delle interfacce usate da [Laravel Cashier](/docs/{{version}}/billing) è cambiato. Anzichè usare `BillableTrait`, usa il trait `Laravel\Cashier\Billable`. E, al posto di `Laravel\Cashier\BillableInterface` implementa l'interfaccia `Laravel\Cashier\Contracts\Billable`. Non è richiesto nessuna altra modifica ai metodi.

### Comandi Artisan

Sposta tutte le tue classi command dalla vecchia directory `app/commands` alla nuova `app/Console/Commands`. Successivamente, aggiungi la directory `app/Console/Commands` alla direttiva `classmap` del tuo file `composer.json`.

Quindi, copia la tua lista di comandi Artisan da `start/artisan.php` nell'array `command` del file `app/Console/Kernel.php`.

### Migration & Seed

Cancella le due migration incluse con Laravel 5.0, dato che dovresti già avere le tue ed il tuo database

Muovi tutte le classi da `app/database/migrations` a `database/migrations`. Tutti i tuoi seed, inoltre, dovrebbero essere spostati da `app/database/seeds` a `database/seeds`.

### Binding IoC Globali
Se hai dei binding [service container](/docs/{{version}}/container) in `start/global.php`, occorre muoverli nel metodo `register` del file `app/Providers/AppServiceProvider.php`. Potresti avere bisogno inoltre di importare la Facade `App`.

Se preferisci, puoi inoltre separare questi binding in più service provider in base alla categoria.

### View

Sposta le tue view da `app/views` a `resources/views`.

### Cambiamenti ai Tag Blade

Per maggiore sicurezza, di default, Laravel 5.0 effettua di default l'esacape di tutti i caratteri sia in `{{ }}` che in `{{{ }}}`. È stata creata infatti una nuova direttiva `{!! !!}` che permette di visualizzare dei dati "grezzi". L'opzione più sicura quando si aggiorna l'applicazione è quella di utilizzare solo la nuova direttiva `{!! !!} ` quando si è **certi** che sia sicuro far visualizzare l'output in modo "grezzo".

Ad ogni modo, se sei **costretto** ad usare la vecchia sintassi di blade, aggiungi le seguenti linee di codice in `AppServiceProvider@register`:

```php
\Blade::setRawTags('{{', '}}');
\Blade::setContentTags('{{{', '}}}');
\Blade::setEscapedContentTags('{{{', '}}}');
```

Se possibile, comunque, evita questo approccio, perchè rende la tua applicazione più vulnerabile agli exploit XSS. Anche i commenti con la direttiva `{{--` sono stati rimossi.

### File delle Traduzioni

Sposta o file di lingua da `app/lang` a `resources/lang`.

### Directory Pubblica

Copia i tuoi asset dalla directory public della tua applicazione `4.2` nella nuova directory `public. Assicurati di mantenere il file `index.php` della versione `5.0`.

### Test

Sposta i tuoi testa da `app/tests` a `tests`.

### File Vari

Sposta quindi i tuoi altri file vari presenti nel tuo progetto. Per esempio, `.scrutinizer.yml`, `bower.json` ed altri simili.

Puoi spostare i tuoi file Sass, Less, o CoffeeScript in qualsiasi posizione tu desideri. La directory `resources/assets` potrebbe essere un ottima posizione.

### Helper per Form ed HTML

Se stai usando gli helper per creare Form o HTML, vedrai un messaggio di errore `class 'Form' non trovata` oppure `class 'Html' non trovata`. Gli helper per Form e HTML sono deprecati in Laravel 5.0; tuttativa, ci sono community per il mantenimento di questi driver come ad esempio [Laravel Collective](http://laravelcollective.com/docs/{{version}}/html), per maggiori informazioni.

Per esempio, puoi aggiungere `"laravelcollective/html": "~5.0"` nella sezione require del tuo file `composer.json`.

Dovrai anche aggiungere le facade Form e HTML al service provider. Modifica `config/app.php` ed aggiungi queste linee di codice nell'array 'providers':

	'Collective\Html\HtmlServiceProvider',

Infine, aggiungi queste linee di codice all'array 'aliases':

	'Form' => 'Collective\Html\FormFacade',
	'Html' => 'Collective\Html\HtmlFacade',

### CacheManager

Se la tua applicazione usava `Illuminate\Cache\CacheManager` per usare la versione non Facade della cache di Laravel, usa `Illuminate\Contracts\Cache\Repository`.

### Paginazione

Sostituisci tutte le chiamate a `$paginator->links()` con `$paginator->render()`.

Sostituisci tutte le chiamate a `$paginator->getFrom()` e `$paginator->getTo()` rispettivamente con `$paginator->firstItem()` e `$paginator->lastItem()`.

Rimuovi il prefisso "get" dalla chiamata a `$paginator->getPerPage()`, `$paginator->getCurrentPage()`, `$paginator->getLastPage()` e `$paginator->getTotal()` (es. `$paginator->perPage()`).

### Beanstalk

Laravel 5.0 adesso richiede `"pda/pheanstalk": "~3.0"` invece di `"pda/pheanstalk": "~2.1"`.

### Remote

Il componente Remote è deprecato.

### Workbench

Il componente Workbench è deprecato.

<a name="aggiornamento-4.2"></a>
## Aggiornamento Alla 4.2 Dalla 4.1

### PHP 5.4+

Laravel 4.2 richiede PHP 5.4.0 o superiore.

### Crittografia

Aggiungi una nuova opzione `cipher` nel tuo file di configurazione `app/config/app.php`. Il valore di questa opzione dovrebbe essere `MCRYPT_RIJNDAEL_256`.

	'cipher' => MCRYPT_RIJNDAEL_256

> **Nota:** In Laravel 4.2, la cifratuda di default è `MCRYPT_RIJNDAEL_128` (AES), la quale viene considerata più sicura. Cambiando la cifratura riportandola a `MCRYPT_RIJNDAEL_256` è obbligatorio per derciptare cookies/valori che venivano crittografati in versioni di Laravel <= 4.1.

### Il Soft Deleting dei Model Adesso Usa I Trait

Se stai usando il soft deleteing dei model, la proprietà `softDeletes` è stata rimossa. Adesso devi usare `SoftDeletingTrait` in questo modo:

	use Illuminate\Database\Eloquent\SoftDeletingTrait;

	class User extends Eloquent {
		use SoftDeletingTrait;
	}

Puoi anche aggiungere manualmente la colonna `deleted_at` alla proprietà `dates`:

	class User extends Eloquent {
		use SoftDeletingTrait;

		protected $dates = ['deleted_at'];
	}

Le API per le operazioni di soft delete rimangono le stesse.

> **Nota:** Il trait `SoftDeletingTrait` non può essere usato sul model base. Deve essere inveve usato sulla classe attuale del model.

### View / Pagination Environment Rinominate

Se stai referenziando direttamente le classi `Illuminate\View\Environment` oppure `Illuminate\Pagination\Environment`, aggiorna il tuo codice con `Illuminate\View\Factory` e `Illuminate\Pagination\Factory`. Queste due classi sono state rinominate per meglio riflettere le loro funzionalità.

### Parametri Aggiuntivi Per Pagination Presenter

Se stai estendendo la classe `Illuminate\Pagination\Presenter`, la firma del metodo astratto `getPageLinkWrapper` è cambiata aggingendo l'argomento `rel` come segue:

	abstract public function getPageLinkWrapper($url, $page, $rel = null);

### Crittografia Code Iron.Io

Se stai usando i driver per le code Iron.io, avrai bisogno di aggiungere l'opzione `encrypt` al file di configurazione delle code:

	'encrypt' => true

<a name="aggiornamento-4.1.29"></a>
## Aggiornamento Alla 4.1.29 Dalla <= 4.1.x

Laravel 4.1.29 migliora improves the column quoting per tutti i driver database. Questo protegge la tua applicazione dalla vulnerabilità dell'assegnamento di massa quando **non** viene usata la proprietà `fillable` nei model. Se stai usando la proprietà `fillable`, l'applicazione non è più vulnerabile. Tuttavia, se stai usando `guarded` e stai passando un array di dati controllato dall'utente ad una delle funzioni "update" o "save, dovresti aggiornare immediatamente la tua applicazione alla `4.1.29`.

Per aggiornare a Laravel 4.1.29, utilizza il comando `composer update`.

<a name="aggiornamento-4.1.26"></a>
## Aggiornamento Alla 4.1.26 Dalla <= 4.1.25

Laravel 4.1.26 introduce alcuni miglioramenti sulla sicurezza per i cookie "ricordami". Prima di questo aggiornamento, se un cookie "ricordami" è stato manipolato da un altro utente malintenzionato, il cookie rimarrebbe valido per un lungo periodo di tempo, anche dopo che il vero uente reimposta la propria password, effettua il logout, ecc.

Questo cambiamento richiede l'aggiunta di una nuova colonna alla tabella users (o equivalente). Dopo questo cambiamento, verrà assegnato un nuovo token all'utente ogni volta che effettua il login alla tua applicazione. Il token, verrà aggiornato anche quando l'utente effettuerà il logout dall'applicazione. Le implicazioni di questo cambio sono: se un cookie "ricordami" viene manipolato malignamente, semplicemente accedendo dall'applicazione invaliderà il cookie.

### Upgrade Path

Per prima cosa, aggiungi, un nuovo campo nullo `remember_token` del tipo VARCHAR(100), TEXT, o equivalente nella tabella `users`.

Successivamente, se stai usando i driver di autenticazione di Eloquent, aggiorna la classe `User` aggiungendo i seguenti metodi:

	public function getRememberToken()
	{
		return $this->remember_token;
	}

	public function setRememberToken($value)
	{
		$this->remember_token = $value;
	}

	public function getRememberTokenName()
	{
		return 'remember_token';
	}

> **Nota:** Tutti i "ricordati di me" di sessione saranno invalidati da questo cambiamento, in modo che tutti gli utenti saranno costretti a ri-autenticarsi con l'applicazione.

### Package Maintainer

Due nuovi metodi sono stati aggiunti all'interfaccia `Illuminate\Auth\UserProviderInterface`. Le implementazioni di esempio possono essere trovate nei driver di default:

	public function retrieveByToken($identifier, $token);

	public function updateRememberToken(UserInterface $user, $token);

L'interfaccia `Illuminate\Auth\UserInterface` ha ricevuto tre nuovi metodi descritti in "Upgrade Path".

<a name="aggiornamento-4.1"></a>
## Aggiornamento Alla 4.1 Dalla 4.0

### Aggiornamento Delle Tue Dipendenze Composer

Per aggiornare la tua applicazione a Laravel 4.1, cambia la versione di `laravel/framework` alla `4.1.*` nel file `composer.json`.

### Sostituire I File

Sostituisci il tuo file `public/index.php`con [questa nuova copia dal repository](https://github.com/laravel/laravel/blob/v4.1.0/public/index.php).

Sostituisci il tuo file `artisan` con [questa nuova copia dal repository](https://github.com/laravel/laravel/blob/v4.1.0/artisan).

### Aggiungere File di Configurazione & Opzioni

Aggiorna gli array `aliases` e `providers` nel file di configurazione `app/config/app.php`. I valori aggiornati per questi array possono essere trovati [in questo file](https://github.com/laravel/laravel/blob/v4.1.0/app/config/app.php). Assicurati di ri-aggiungere i tuoi package e service provider personalizzati negli array.

Aggiungi un nuovo file `app/config/remote.php` [dal repository](https://github.com/laravel/laravel/blob/v4.1.0/app/config/remote.php).

Aggiungi una nuova opzione di configurazione `expire_on_close` in `app/config/session.php`. Il valore di default dovrebbe essere `false`.

Aggiungi una nuova sezione `failed` in `app/config/queue.php`. Qui ci sono i valori di default per questa sezione:

	'failed' => [
		'database' => 'mysql', 'table' => 'failed_jobs',
	],

**(Facoltativo)** Aggiorna l'opzione `pagination` in `app/config/view.php` con `pagination::slider-3`.

### Aggiornamento Controller

Se `app/controllers/BaseController.php` ha uno statement`use` all'inizio del file, cambia `use Illuminate\Routing\Controllers\Controller;` con `use Illuminate\Routing\Controller;`.

### Aggiornamento Recupero Password

Il recupero password 
Password reminders è stato revisionato per avere una maggiore flessibilità nell'utilizzo. Puoi controllare il nuovo stub di controller usando il comando Artisan `php artisan auth:reminders-controller`. Puoi anche visionare la [documentazione aggiornata](/docs/security#password-reminders-and-reset) ed aggiornare in modo opportuno la tua applicazione.

Aggiorna i file di lingua `app/lang/en/reminders.php` in modo che sia corrispondente a [questo file aggiornato](https://github.com/laravel/laravel/blob/v4.1.0/app/lang/en/reminders.php).

### Aggiornamento Rilevamento Ambiente

Per ragioni di sicurezza, l'URL di dominio non viene più usato per determinare l'ambiente di lavoro della tua apoplicazione. Questi valori sono facilmente modificabili e permettono ai male intezionati di modificare l'ambiente per una richiesta. Devi convertire il rilevamento dell'ambiente usando il nome dell'host della tua macchina (comando `hostname` per Mac, Linux, e Windows).

### Semplice File Di Log

Larave adesso genera un singolo file di log: `app/storage/logs/laravel.log`. Tuttavia, puoi ancora configurare questa funzionalità da `app/start/global.php`.

### Rimozione Redirect Trailing Slash

Nel file `bootstrap/start.php`, rimuovi la chiamata a `$app->redirectIfTrailingSlash()`. Questo metodo non è più usato, e questa funzionalità può essere gestita da file `.htaccess` incluso col framework.

Successivamente, sostituisci il tuo file `.htaccess` con [questo nuovo] file (https://github.com/laravel/laravel/blob/v4.1.0/public/.htaccess) that handles trailing slashes.

### Accesso Alla Route Corrente

Per accedere alla route corrente usa `Route::current()` invece di `Route::getCurrentRoute()`.

### Composer Update

Una volta completato i cambiamenti descritti sopra, puoi eseguire il comando `composer update` per aggiornare i file del core del framework! Se ricevi messaggi di errore per il caricamento delle classei, prova ad eseguire il comando `update` con l'opzione `--no-scripts` in questo modo: `composer update --no-scripts`.

### Event Listener Wildcard 

The wildcard event listeners no longer append the event to your handler functions parameters. Se hai bisogno di trovare l'evento che è stato richiamto usa  `Event::firing()`.
