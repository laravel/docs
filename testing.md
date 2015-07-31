# Testing

- [Introduzione](#introduzione)
- [Testing Dell'Applicazione](#testing-applicazione)
	- [Interagire Con La Tua Applicazione](#interagire-con-la-tua-applicazione)
	- [Testing API JSON](#testing-apis-json)
	- [Sessioni / Autenticazione](#sessioni-e-autenticazione)
	- [Disabilitare I Middleware](#disabilitare-i-middleware)
	- [Richieste HTTP Personalizzate](#richieste-http-personalizzate)
- [Lavorare Con I Database](#lavorare-con-database)
	- [Resettare Il Database Dopo Ogni Test](#resettare-database-dopo-ogni-test)
	- [Model Factory](#model-factory)
- [Mocking](#mocking)
	- [Mocking Degli Eventi](#mocking-eventi)
	- [Mocking Dei Job](#mocking-job)
	- [Mocking Delle Facade](#mocking-facade)

<a name="introduzione"></a>
## Introduzione

Laravel è nato con in mente lo unit testing. Il supporto per il testing con PHPUnit, infatti, è incluso nell’installazione base, e un file `phpunit.xml` è già pronto da usare per la tua applicazione. 
Il framweork inoltre lavora con dei metodi helper convenienti che ti permettono di testare la tua applicazione in modo “espressivo”.

Un esempio di file test è fornito nella directory `tests`. Dopo l'installazione di una nuova applicazione Laravel, basta eseguire semplicemente da terminale `phpunit` per eseguire i tuoi test.

### Ambiente Di Test

Quando esegui gli unit test, Laravel imposterà automaticamente la configurazione d'ambiente su `testing`. Laravel configurerà autoamticamente la sessione la cache nell'`array` dei driver durante il test, questo significa che nessun dato di sessione o di cache verrà mantenuto durante il test.

Sei libero di creare tutte le configurazioni per i test di cui hai bisogno. Le variabili d'ambiente di `test` possono essere configurate nel file `phpunit.xml`.

### Definire & Eseguire I Test

Per creare un nuovo test case, crea semplicemente un nuovo file nella directory `tests`. La classe test dovrebbe estendere `TestCase`. Puoi quindi definire dei metodi di test come normalmente faresti usando PHPUnit. Per eseguire i tuoi test, esegui semplicemente il comando `phpunit` dal tuo terminale:

	<?php

	class FooTest extends TestCase
	{
		public function testSomethingIsTrue()
		{
			$this->assertTrue(true);
		}
	}

> **Nota:** Se definisci il tuo metodo `setUp`, assicurati di effettuare la chiamata a `parent::setUp`.

<a name="testing-applicazione"></a>
## Testing Dell'Applicazione

Laravel ti offre un sistema fluente di API per effettuare richieste HTTP alla tua applicazione, esaminare l'output, e anche la compilazione di form. Per esempio, dai uno sguardo al file `ExampleTest.php` incluso nella directory `tests`:

	<?php

	use Illuminate\Foundation\Testing\WithoutMiddleware;
	use Illuminate\Foundation\Testing\DatabaseTransactions;

	class ExampleTest extends TestCase
	{
	    /**
	     * A basic functional test example.
	     *
	     * @return void
	     */
	    public function testBasicExample()
	    {
	        $this->visit('/')
	             ->see('Laravel 5');
	    }
	}

Il metodo `visit` effettua una richiesta `GET` nella tua applicazione. Il metodo `see` asserisce che quello che dovremmo vedere sia il testo dato nella risposta ritornata dalla tua applicazione. Questo è il test più comune disponibile in Laravel.

<a name="interagire-con-la-tua-applicazione"></a>
### Interagire Con La Tua Applicazione

Ovviamente, puoi fare molto di più rispetto ad un semplice assert di un testo che appare in una data risposta. Dai uno sguardo ad alcuni esempi di click di link e di completamento di form:

#### Click Di Link

In questo test, effettueremo una richiesta all'applicazione, "cliccare" un link nella risposta ritornata, e quindi asserire di essere riportati su un dato URI. Per esempio, assumiamo di avere un link nella nostra risposta con un testo che ha il valore di "Chi Siamo":

	<a href="/chi-siamo">Chi Siamo</a>

Ora, scriviamo un test che clicchi sul link ed asserisce che l'utente venga riportato sulla pagina corretta:

    public function testBasicExample()
    {
        $this->visit('/')
             ->click('About Us')
             ->seePageIs('/about-us');
    }

#### Lavorare Con I Form

Laravel offre anche una serie di metodi per testare i form. I metodi `type`, `select`, `check`, `attach`, e `press` ti permettono di interagire con tutti gli input dei form. Per esempio, immaginiamo di avere un form nella pagina di registrazione della nostra applicazione:

	<form action="/register" method="POST">
		{!! csrf_field() !!}

		<div>
			Name: <input type="text" name="name">
		</div>

		<div>
			<input type="checkbox" value="yes" name="terms"> Accept Terms
		</div>

		<div>
			<input type="submit" value="Register">
		</div>
	</form>

Possiamo scrivere un test per completare questo form e controllarne il risultato:

    public function testNewUserRegistration()
    {
        $this->visit('/register')
             ->type('Taylor', 'name')
             ->check('terms')
             ->press('Register')
             ->seePageIs('/dashboard');
    }

Ovviamente, se il tuo form contiene altri input come pulsanti radio o box drop-down, puoi facilmente compilarli. Qui una lista dei metodi di manipolazione per i form:

Method  | Description
------------- | -------------
`$this->type($text, $elementName)`  |  "Type" text into a given field.
`$this->select($value, $elementName)`  |  "Select" a radio button or drop-down field.
`$this->check($elementName)`  |  "Check" a checkbox field.
`$this->attach($pathToFile, $elementName)`  |  "Attach" a file to the form.
`$this->press($buttonTextOrElementName)`  |  "Press" a button with the given text or name.

#### Lavorare Con Gli Allegati
Se il tuo form contiene input di tipo `file`, puoi allegare i file al form usando il metodo `attach`:

    public function testPhotoCanBeUploaded()
    {
        $this->visit('/upload')
             ->name('File Name', 'name')
             ->attach($absolutePathToFile, 'photo')
             ->press('Upload')
             ->see('Upload Successful!');
    }

<a name="testing-apis-json"></a>
### Testing API JSON

Laravel offre anche una serie di helper per il testing di API JSON e le loro risposte. Per esempio, i metodi `get`, `post`, `put`, `patch`, e `delete` possono essere usati per inviare richieste con vari verbi HTTP. Puoi anche facilmente passare dei dati e header a questi metodi. Per iniziare, scriviamo un test per effettuare una richiesta `POST` a `/user` e asseriamo che un dato array sia ritornato in formato JSON:

	<?php

	class ExampleTest extends TestCase
	{
	    /**
	     * A basic functional test example.
	     *
	     * @return void
	     */
	    public function testBasicExample()
	    {
	    	$this->post('/user', ['name' => 'Sally'])
	    	     ->seeJson([
	    	     	'created' => true,
	    	     ]);
	    }
	}

Il metodo `seeJson` converte l'array dato in JSON, e quindi verifica che quel segmento JSON coincida **dovunque** con l'intera risposta JSON ritornata dall'applicazione. Così, se ci sono altre proprietà nella risposta JSON, questo test sarà ancora valido finchè il segmento dato è presente.

#### Verificare L'Esatta Corrispondenza JSON

Se vuoi verificare che un dato array sia un **esatta** corrispondenza per il JSON ritornato dall'applicazione, dovresti usare il metodo `seeJsonEquals`:

	<?php

	class ExampleTest extends TestCase
	{
	    /**
	     * A basic functional test example.
	     *
	     * @return void
	     */
	    public function testBasicExample()
	    {
	    	$this->post('/user', ['name' => 'Sally'])
	    	     ->seeJsonEquals([
	    	     	'created' => true,
	    	     ]);
	    }
	}

<a name="sessioni-e-autenticazione"></a>
### Sessioni / Autenticazione

Laravel offre una serie di helper per lavorare con le sessioni durante i test. Per prima cosa, puoi impostare i dati di sessione in un array usando il metodo `withSession`. Questo è utile per caricare la sessione con dei dati prima di testare la richiesta della tua applicazione:

	<?php

	class ExampleTest extends TestCase
	{
	    public function testApplication()
	    {
			$this->withSession(['foo' => 'bar'])
			     ->visit('/');
	    }
	}

Ovviamente, un uso comune della sessione e per mantenere lo stato utente, come ad esempio l'utente autenticato. L'helper `actingAs` offre un modo semplice di autenticare un dato utente come utente corrente. Per esempio, possiamo usare la [model factory](#model-factory) per generare ed autenticare un utente:

	<?php

	class ExampleTest extends TestCase
	{
	    public function testApplication()
	    {
	    	$user = factory('App\User')->create();

			$this->actingAs($user)
				 ->withSession(['foo' => 'bar'])
			     ->visit('/')
			     ->see('Hello, '.$user->name);
	    }
	}

<a name="disabilitare-i-middleware"></a>
### Disabilitare I Middleware

Quando testi la tua applicazione, puoi trovare conveniente disabilitare i [middleware](/documentazione/5.1/middleware) per alcuni dei tuoi test. Questo ti permetterà di testare le tue route e controller in completo isolamento dai controlli dei middleware. Laravel include un semplice trait `WithoutMiddleware` che puoi usare per disabiltiare automaticamente tutti i middleware per la classe di test:

	<?php

	use Illuminate\Foundation\Testing\WithoutMiddleware;
	use Illuminate\Foundation\Testing\DatabaseTransactions;

	class ExampleTest extends TestCase
	{
		use WithoutMiddleware;

	    //
	}

Se preferisci solo disabilitare i middleware per alcuni metodi di test, puoi chiamare il metodo `withoutMiddleware` dall'interno di tali metodi:

	<?php

	class ExampleTest extends TestCase
	{
	    /**
	     * A basic functional test example.
	     *
	     * @return void
	     */
	    public function testBasicExample()
	    {
	    	$this->withoutMiddleware();

	        $this->visit('/')
	             ->see('Laravel 5');
	    }
	}

<a name="richieste-http-personalizzate"></a>
### Richieste HTTP Personalizzate

Se vuoi effettuare una richiesta HTTP personalizzata nella tua applicazione e prelevare l'intero oggetto `Illuminate\Http\Response`, puoi usare il metodo `call`:

    public function testApplication()
    {
    	$response = $this->call('GET', '/');

    	$this->assertEquals(200, $response->status());
    }

Se stai effettuando delle richieste `POST`, `PUT`, o `PATCH` puoi passare un array di dati di input con la richiesta. Ovviamente, questi dati saranno disponibili nelle tue route e controller tramite l' [istanza Request](/documentazione/5.1/richieste):

   	$response = $this->call('POST', '/user', ['name' => 'Taylor']);

<a name="lavorare-con-database"></a>
## Lavorare Con I Database

Laravel offre anche una serie di utili strumenti per rendere più facili i test su applicazioni basate su database. Per prima cosa, puoi usare l'helper `seeInDatabase` per asserire che quel dato esiste nel database in base ad un dato criterio. Per esempio, se vuoi verificare l'esistenza di un record nella tabella `users` con il campo `email` uguale a `sally@example.com`, possiamo fare come segue:

    public function testDatabase()
    {
    	// Make call to application...

    	$this->seeInDatabase('users', ['email' => 'sally@foo.com']);
    }

Ovviamente, il metodo `seeInDatabase` e gli altri helper piacciono per la loro convenienza. Sei libero di usare qualsiasi metodo di asserzione built-in di PHPUnit per completare i tuoi test.

<a name="resettare-database-dopo-ogni-test"></a>
### Resettare Il Database Dopo Ogni Test

Spesso è utile resettare il database dopo ogni test così che i dati precedenti di un precedente test non interferiranno con i test successivi.

#### Usare Le Migration

Un'opzione è di eseguire un rollback del database dopo ogni test ed eseguire le migration prima del prossimo test. Laravel offre un semplice trait `DatabaseMigrations` che gestirà questo per te automaticamente. Usa semplicemente il trait nella tua classe test:

	<?php

	use Illuminate\Foundation\Testing\WithoutMiddleware;
	use Illuminate\Foundation\Testing\DatabaseMigrations;
	use Illuminate\Foundation\Testing\DatabaseTransactions;

	class ExampleTest extends TestCase
	{
		use DatabaseMigrations;

	    /**
	     * A basic functional test example.
	     *
	     * @return void
	     */
	    public function testBasicExample()
	    {
	        $this->visit('/')
	             ->see('Laravel 5');
	    }
	}

#### Usare Le Transazioni

Un altra opzione è di racchiudere ogni test case in una transazione database. Ancora una volta, Laravel offre un conveniente trait `DatabaseTransactions` che gestirà questo automaticamente:

	<?php

	use Illuminate\Foundation\Testing\WithoutMiddleware;
	use Illuminate\Foundation\Testing\DatabaseMigrations;
	use Illuminate\Foundation\Testing\DatabaseTransactions;

	class ExampleTest extends TestCase
	{
		use DatabaseTransactions;

	    /**
	     * A basic functional test example.
	     *
	     * @return void
	     */
	    public function testBasicExample()
	    {
	        $this->visit('/')
	             ->see('Laravel 5');
	    }
	}

<a name="model-factory"></a>
### Model Factory

Quando testi, è comune di aver bisogno di inserire alcuni record nel tuo database prima di eseguire il tuo test. Invece di specificare manualmente il valore di ogni colonna quando crei dei dati di test, Laravel di permette di definire un insieme di attributi di default per ogni [model Eloquent](/documentazione/5.1/eloquent) usando le "factories". Per iniziare, dai uno sguardo al file `database/factories/ModelFactory.php` nella tua applicazione. Questo file contiene la definizione di una factory:

	$factory->define('App\User', function ($faker) {
	    return [
	        'name' => $faker->name,
	        'email' => $faker->email,
	        'password' => str_random(10),
	        'remember_token' => str_random(10),
	    ];
	});

All'interno della Closure, che serve come definizione della factory, puoi ritornare i valori di test di default di tutti gli attributi del model. La Closure riceverà un istanza della libreria PHP [Faker](https://github.com/fzaninotto/Faker), che ti permette in modo conveniente di generare vari tipi di dati in modo casuale per i tuoi test.

Ovviamente, sei libero di aggiungere le tue factory aggiuntive nel file `ModelFactory.php`.

#### Multipli Tipi Di Factory

Qualche volta puoi desiderare di avere factory multiple per la stessa classe di un model Eloquent. Per esempio, forse vorresti avere una factory per gli utenti "Administrator" in aggiunta ai normali utenti. Puoi definire queste factory usando il metodo `defineAs`:

	$factory->defineAs('App\User', 'admin', function ($faker) {
	    return [
	        'name' => $faker->name,
	        'email' => $faker->email,
	        'password' => str_random(10),
	        'remember_token' => str_random(10),
	        'admin' => true,
	    ];
	});

Invece di duplicare tutti gli attributi dalla tua factory user di base, puoi usare il metodo `raw` per recuperare gli attributi base. Una volta che hai ottenuto gli attributiOnce you have the attributes, integrali facilmente con qualsiasi altro valore aggiuntivo tu abbia bisogno:

	$factory->defineAs('App\User', 'admin', function ($faker) use ($factory) {
		$user = $factory->raw('App\User');

		return array_merge($user, ['admin' => true]);
	});

#### Usare Le Factory Nei Test

Una volta che hai definito le tue factory, puoi usarle nei tuoi test o nei file di seed per il database per generare istanze del model usando la funzione globale `factory`. Ora, diamo un occhiata ad alcuni esempi di creazione di model. Per prima cosa, useremo il metodo `make`, che crea i model ma non li salva nel database:

    public function testDatabase()
    {
    	$user = factory('App\User')->make();

    	// Use model in tests...
    }

Se vuoi sovrascrivere qualche valore di default dei tuoi model, puoi passare un array di valori al metodo `make`. Verranno sovrascritti soltanto i valori specificati mentre i valori restanti saranno settati con i loro valori specificati dalla factory:

    $user = factory('App\User')->make([
    	'name' => 'Abigail',
   	]);

Puoi anche creare una Collection di model oppure creare model di un dato tipo:

	// Create three App\User instances...
	$users = factory('App\User', 3)->make();

	// Create an App\User "admin" instance...
	$user = factory('App\User', 'admin')->make();

	// Create three App\User "admin" instances...
	$users = factory('App\User', 'admin', 3)->make();

#### Model Factory Persistenti

Il metodo `create` non solo crea le istanze dei model, ma li salva anche  nel database usando il metodo `save` di Eloquent:

    public function testDatabase()
    {
    	$user = factory('App\User')->create();

    	// Use model in tests...
    }

Ancora una volta, puoi sovrascrivere gli attributi nel model passando un array al metodo `create`:

    $user = factory('App\User')->create([
    	'name' => 'Abigail',
   	]);

#### Aggiungere Relazioni Ai Models

Puoi avere anche multipli model persistenti nel database. In questo esempio, collegheremo una relazione ai model creati. Quando usi il metodo `create` per creare multipli model, viene ritornata una [istanza collection](/documentazione/5.1/eloquent-collection) di Eloquent, che ti permette di usare qualsiasi delle funzioni offerte dalle collection, come ad esempio `each`:

    $users = factory('App\User', 3)
               ->create()
               ->each(function($u) {
					$u->posts()->save(factory('App\Post')->make());
				});

<a name="mocking"></a>
## Mocking

<a name="mocking-eventi"></a>
### Mocking Degli Eventi
Se stai facendo un uso intensivo del sistema di Eventi di Laravel, potresti desiderare di “silenziare” oppure eseguire finte chiamate ad alcuni eventi durante i test. Per esempio, se stai testando la registrazione degli utenti, probabilmente non vorrai che vengano eseguiti tutti gli handler relativi a `UserRegistered`, dal momento che potrebbero inviare delle email di “benvenuto”, etc.

Laravel offre un conveniente metodo `expectsEvents` che verifica che gli eventi attesi siano eseguiti, ma previene l'esecuzioni di qualsiasi handler associato a questi eventi:

	<?php

	class ExampleTest extends TestCase
	{
	    public function testUserRegistration()
	    {
	    	$this->expectsEvents('App\Events\UserRegistered');

	    	// Test user registration code...
	    }
	}

Se preferisci  prevenire l'esecuzione di tutti gli handler, puoi usare il metodo `withoutEvents`:

	<?php

	class ExampleTest extends TestCase
	{
	    public function testUserRegistration()
	    {
	    	$this->withoutEvents();

	    	// Test user registration code...
	    }
	}

<a name="mocking-job"></a>
### Mocking Dei Job

Qualche volta, potresti voler testare che uno specifico job venga eseguito dai tuoi controller quando eseguono una richiesta alla tua applicazione. Questo ti permette di testare le tue route / controller in modo separato dalla logica del tuo job. Ovviamente, puoi quindi testare il job in una classe seprata.

Laravel fornisce un metodo conveniente `expectsJobs` che verificherò che i job attesi siano eseguiti, ma lo job stesso non verrà eseguito:

	<?php

	class ExampleTest extends TestCase
	{
	    public function testPurchasePodcast()
	    {
	    	$this->expectsJobs('App\Jobs\PurchasePodcast');

	    	// Test purchase podcast code...
	    }
	}

> **Nota:** Questo metodo controlla solo i job che vengono inviati tramite i metodi di invio del trait `DispatchesCommands`. Non rileva i job che sono inviati direttamente a `Queue::push`.

<a name="mocking-facades"></a>
### Mocking Facades

In fase di testing, potresti spesso voler eseguire una finta chiamata alle [facade](/documentazione/5.1/facade) di Laravel. Per esempio, considera il la seguente action del controller:

	<?php namespace App\Http\Controllers;

	use Cache;
	use Illuminate\Routing\Controller;

	class UserController extends Controller
	{
		/**
		 * Show a list of all users of the application.
		 *
		 * @return Response
		 */
		public function index()
		{
			$value = Cache::get('key');

			//
		}
	}

Possiamo fingere la chiamata alla facade `Cache` usando il metodo `shouldReceive`, che ritornerà un istanza mock di [Mockery](https://github.com/padraic/mockery). Dal momento che le facade sono risolte e gestite dal [service container](/documentazione/5.1/container) di Laravel, sono molto più testabili rispetto ad una tipica classe statica. Per esempio, eseguiamo una finta chiamata alla facade `Cache`:

	<?php

	class FooTest extends TestCase
	{
		public function testGetIndex()
		{
			Cache::shouldReceive('get')
						->once()
						->with('key')
						->andReturn('value');

			$this->visit('/users')->see('value');
		}
	}

> **Nota:** Non dovresti eseguire il mock sulla facade `Request`. Invece, passa l'input all'interno del metodo `call` e `post` quando esegui il tuo test.
