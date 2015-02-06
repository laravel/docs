# Aggiornamento

- [Aggiornamento alla versione 5.0 dalla 4.2](#aggiornamento-5.0)

<a name="aggiornamento-5.0"></a>
## Aggiornamento alla versione 5.0 dalla 4.2

### Nuova Installazione (e Successiva Migrazione)

Il modo migliore di migrare un'applicazione creata con Laravel 4.2 è, innanzitutto, installare una nuova copia di un progetto vuoto con la 5.0. Quindi, in un secondo step, copiare i file dell'applicazione 4.2. Precisamente, i controller, le routes, model di Eloquent, comandi Artisan, asset e tutto ciò che è specifico dell'applicazione.

Per iniziare, quindi [crea una nuova applicazione con Laravel 5](/installazione) in una nuova directory. Adesso, un po' alla volta, vedremo quali sono tutti gli step necessari per completare l'operazione senza intoppi.

### Dipendenze & Package

Non scordarti, innanzitutto, di copiare ogni dipendenza nella tua nuova applicazione. Tali dipendenze includono ovviamente anche i vari SDK e codici di terze parti.

Alcuni package specifici potrebbero non essere compatibili con Laravel 5, soprattutto se stai leggendo queste righe in un momento in cui Laravel 5 è uscito da poco. Ad ogni modo, una volta copiate le dipendenze, esegui il comando _composer update_.

### Namespacing

Di default, Laravel 4 non usa i namespace nell'application code. Per intenderci, in un'applicazione 4.2 tutti i model Eloquent "vivono" in un namespace globale. Nulla ti vieta, se vuoi velocizzare le cose, di lasciare in un namespace globale queste classi.

### Configurazione

#### Migrare le Variabili di Ambiente

Copia il nuovo file _.env.example_ in _.env_, che è appunto l'equivalente del vecchio _.env.php_. Imposta i vari valori più appropriati, come _APP_ENV_ e _APP_KEY_, le credenziali del database ed i driver di sessione e caching.

Inoltre, copia tutti i valori personalizzati che ti eri creato in _.env.php_, mettendoli in _.env_ (che userai per davvero) ed in _.env.example_ (un sample che userai con gli altri membri del tuo team).

Per altre informazioni sulla configurazione degli ambienti, dai uno sguardo alla [sezione dedicata sulla documentazione](/configurazione#configurazione-ambiente).

> **Nota:** Avrai bisogno di sistemare adeguatamente il file _.env_ sul tuo server prima di effettuare il deploy!

#### File di Configurazione

Laravel 5.0 non usa più le directory _app/config/{nome_ambiente}_ per fornire file di configurazione specifici in base all'ambiente di lavoro usato. Al loro posto, sposta i valori che in base all'ambiente possono cambiare in _.env_, quindi accedici usando la funzione _env('key', 'default value')_.

Vedrai alcuni esempi di questo meccanismo in _config/database.php_.

In questo modo potrai usare i file in _config/_ per gestire i valori consistenti indipendentemente dall'ambiente di sviluppo, con l'aggiunta di _env()_ per quelli variabili.

Ricorda, se aggiungi più valori al file _.env_ fallo anche per _.env.example_, se lavori in team.

### Route

Copia il vecchio file _routes.php_ in _app/routes.php_.

### Controller

Muovi quindi tutti i controller della tua applicazione in _app/Http/Controllers_. Visto che in questa "guida" non effettueremo una migrazione completa che include anche i namespace, _app/Http/Controllers_ alla direttiva _classmap_ del file _composer.json_. Rimuovi quindi il namespace dalla classe astratta _app/Http/Controllers/Controller.php_. Verifica infine che i controller che usi estendano tale classe base.

In _app/Providers/RouteServiceProvider.php_, quindi, imposta _namespace_ come _null_.

### Filtri delle Route

Copia i binding dei tuoi filtri dal file _app/filters.php_ mettendoli in _boot()_ della classe _app/Providers/RouteServiceProvider.php_. Aggiungi _use Illuminate\Support\Facades\Route;_ in _app/Providers/RouteServiceProvider.php_ per continuare ad usare la Facade _Route_.

Non avrai bisogno di spostare i vari filtri di default, come _auth_ e _csrf_, dato che esistono già come middleware. Dovrai invece modificare le route o i controller che li richiedono, trasformando ad esempio il _['before' => 'auth']_ in _['middleware' => 'auth']_.

In ogni caso, i filtri non sono stati rimossi in Laravel 5. Puoi comunque usarli tramite _before_ ed _after_.

### CSRF Globale

Di default, la [protezione CSRF](/routing#protezione-csrf) è abilitata di default su tutte le route. Se vuoi disabilitarla (magari per abilitarla solo su alcune route), rimuovi questa linea dall'array _middleware_ in _App\Http\Kernel_:

	'App\Http\Middleware\VerifyCsrfToken',

Per usarlo altrove, quindi, aggiungi all'array _$routeMiddleware_.

	'csrf' => 'App\Http\Middleware\VerifyCsrfToken',

Da questo momento puoi aggiungere il middleware alle singole route usando _['middleware' => 'csrf']_.

### Model Eloquent

Se necessario, crea pure una nuova cartella _app/Models_ per ospitare i tuoi model Eloquent. Come prima, però, ricorda di aggiungere la cartella alla direttiva _classmap_ del tuo file _composer.json_.

Aggiorna i vari model che usano _SoftDeletingTrait_ in modo tale che usino _Illuminate\Database\Eloquent\SoftDeletes_..

#### Eloquent Caching

Eloquent non permette più l'uso del metodo _remember_ per effettuare il caching delle query. Sei ora "responsabile" di tale operazione che dovrai effettuare manualmente usando la funzione _Cache::remember_.

### Model per l'Autenticazione dell'Utente

Per aggiornare il tuo model _User_ segui i seguenti passi:

**Cancella ciò che segue dal blocco _use_.**

_._.hp
use Illuminate\Auth\UserInterface;
use Illuminate\Auth\Reminders\RemindableInterface;
_.`

**Aggiungici ciò che segue:**

_._.hp
use Illuminate\Auth\Authenticatable;
use Illuminate\Auth\Passwords\CanResetPassword;
use Illuminate\Contracts\Auth\Authenticatable as AuthenticatableContract;
use Illuminate\Contracts\Auth\CanResetPassword as CanResetPasswordContract;
_.`

**Rimuovi UserInterface e RemindableInterface.**

**Implementa la seguenti interfacce:**

_._.hp
implements AuthenticatableContract, CanResetPasswordContract
_.`

**Includi i seguenti trait nella dichiarazione della classe:**

_._.hp
use Authenticatable, CanResetPassword;
_.`

### Comandi Artisan

Sposta tutti i tuoi comandi dalla vecchia cartella _app/commands_ alla nuova _app/Console/Commands_. Dopodiché, aggiungi _app/Console/Commands_ alla direttiva _classmap_ del file _composer.json_.

Infine, copia la tua lista di comandi Artisan da _start/artisan.php_ in _command_ del file _app/Console/Kernel.php_.

### Migration e Seeding

Cancella le due migration incluse con Laravel 5.0, dato che dovresti già avere le tue ed il tuo database.

Muovi tutte le classi da _app/database/migrations_ a _database/migrations_. Tutti i tuoi seed, inoltre, dovrebbero essere spostati da _app/database/seeds_ a _database/seeds_.

### Binding IoC Globali

Se hai dei binding IoC in _start/global.php_, occorre muoverli nel metodo _register_ di _app/Providers/AppServiceProvider.php_. Potresti avere bisogno inoltre di importare la Facade _App_.

Se preferisci, puoi inoltre separare questi binding in più service provider in base alla categoria.

### View

Sposta le tue view da _app/views_ a _resources/views_

### Cambiamenti ai Tag Blade

Di default, Laravel 5.0 effettua di default l'esacape di tutti i caratteri sia in _{{ }}_ che in _{{{ }}}_ È stata creata infatti una nuova direttiva _{!! !!}_ che permette di visualizzare dei dati "grezzi". Usa quindi questa nuova opzione se devi visualizzare dei dati in modo non totalmente sicuro.

Ad ogni modo, se sei costretto ad usare la vecchia sintassi di blade, aggiungi le seguenti linee di codice in _AppServiceProvider@register_.

	\Blade::setRawTags('{{', '}}');
	\Blade::setContentTags('{{{', '}}}');
	\Blade::setEscapedContentTags('{{{', '}}}');

Se possibile, comunque, evita questo approccio.

### File delle Traduzioni

Sposta i tuoi file di lingua da _app/lang_ a _resources/lang_.

### Directory Pubblica

Copia i tuoi asset dalla directory _public_ della tua app _4.2_ a quella nuova. Ricorda comunque di mantenere il file _index.php_ della **5.0**.

### Test

Sposta i tuoi test da _app/tests_ in _tests_.

### File Vari

Sposta quindi i tuoi altri file vari presenti nel tuo progetto: _.scrutinizer.yml_. _bower.json_ ed altri simili.

### Helper per Form ed HTML

Se stai usando gli helper per creare form e codice html, otterrai molto probabilmente un errore di classe non trovata. Includi quindi la dipendenza _"illuminate/html": "~5.0"_ nel tuo file _composer.json_.

Dovrai comunque includere anche le Facade e Service Provider necessari: modifica adeguatamente il file _config/app.php_ aggiungendo in _providers_:

    'Illuminate\Html\HtmlServiceProvider',

Quindi, aggiungi agli alias:

    'Form'      => 'Illuminate\Html\FormFacade',
    'Html'      => 'Illuminate\Html\HtmlFacade',

### CacheManager

Se la tua applicazione usava _Illuminate\Cache\CacheManager_ usa _Illuminate\Cache\Repository_ al suo posto.

### Paginazione

Cambia ogni chiamata al metodo _$paginator->links()_ con _$paginator->render()_.

### Beanstalk

Laravel 5.0 adesso richiede _"pda/pheanstalk": "~3.0"_ al posto di _"pda/pheanstalk": "~2.1"_.

### Remote

Il component Remote ora risulta _deprecato_.

### Workbench

Il componente Workbench ora risulta _deprecato_.
