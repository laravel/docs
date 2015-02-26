# Testing

- [Introduzione](#introduzione)
- [Definire & Eseguire I Test](#definire-ed-eseguire-test)
- [Ambiente di Test](#ambiente-di-test)
- [Chiamare Una Route Da Un Test](#chiamare-route-da-test)
- [Mocking Delle Facade](#mocking-facade)
- [Asserzioni Framework](#asserzioni-framework)
- [Metodi Di Helper](#metodi-helper)
- [Refreshing Dell'Applicazione](#refreshing-applicazione)

<a name="introduzione"></a>
## Introduzione

Laravel è nato con in mente lo unit testing. Il supporto per il testing con PHPUnit, infatti, è incluso nell’installazione base, e un file phpunit.xml è già pronto da usare per la tua applicazione.

Un esempio di file test è fornito nella directory `tests`. Dopo l'installazione di una nuova applicazione Laravel, basta eseguire semplicemente da terminale `phpunit` per eseguire i tuoi test.

<a name="definire-ed-eseguire-test"></a>
## Definire & Eseguire I Test

Puoi creare un nuovo test case semplicemente aggiungendo un file di test nella directory `tests`. La classe test deve estendere la classe `TestCase`. Puoi definire i metodi della classe test con le stesse modalità di PHPUnit.

#### Un Esempio Di Classe Di Test

	class FooTest extends TestCase {

		public function testSomethingIsTrue()
		{
			$this->assertTrue(true);
		}

	}

Puoi eseguire tutti i tuoi test per la tua applicazione eseguendo il comando `phpunit` dal terminale.

> **Nota:** Se definisci il tuo metodo `setUp`, assicurati di effettuare la chiamata a parent::setUp`.

<a name="ambiente-di-test"></a>
## Ambiente di Test

Quando esegui gli unit test, Laravel imposterà automaticamente la configurazione d'ambiente su `testing`. Laravel, include anche, file di configurazione per `session` e `cache` nell'ambiente di test. Entrambi questi driver sono impostati come array nell'ambiente di test, questo significa che nessun dato di sessione o di cache verrà mantenuto durante il test. Sei libero di creare tutte le configurazioni per i test di cui hai bisogno.

<a name="chiamare-route-da-test"></a>
## Chiamare Una Route Da Un Test

#### Chimare Una Route Da Un Test

Puoi facilmente chiamare una delle tue route da un test usando il metodo `call`:

	$response = $this->call('GET', 'user/profile');

	$response = $this->call($method, $uri, $parameters, $files, $server, $content);

Puoi dare una sbirciata all’oggetto `Illuminate\Http\Response`:

	$this->assertEquals('Hello World', $response->getContent());

#### Chiamare Un Controller Da Un Test

Puoi anche chiamare un controller da un test:

	$response = $this->action('GET', 'HomeController@index');

	$response = $this->action('GET', 'UserController@profile', array('user' => 1));

> **Nota:** Non hai bisogno di specificare il namespace completo del controller durante la chiamata al metodo `action`. Basta specificare soltanto la porzione data dal nome della classe seguito dal namespace `App\Http\Controllers`.

Il metodo `getContent` ritornerà una stringa valorizzata che contiene la risposta. Se la tua route ritorna una `View`, puoi accedervi usando la proprietà `original`:

	$view = $response->original;

	$this->assertEquals('John', $view['name']);

Per chiamare una route HTTPS, puoi usare il metodo `callSecure`:

	$response = $this->callSecure('GET', 'foo/bar');

<a name="mocking-facade"></a>
## Mocking Delle Facades

In fase di testing potresti aver bisogno di effettuare una finta chiamata alle static facade di Laravel. Per esempio, dai un’occhiata al seguente metodo di un controller:

	public function getIndex()
	{
		Event::fire('foo', ['name' => 'Dayle']);

		return 'All done!';
	}

Possiamo fingere la chiamate alla classe `Event` usando il metodo `shouldReceive` sulla facade, che restituirà un’istanza del mock [Mockery](https://github.com/padraic/mockery).

#### Mocking A Facade

	public function testGetIndex()
	{
		Event::shouldReceive('fire')->once()->with('foo', ['name' => 'Dayle']);

		$this->call('GET', '/');
	}

> **Nota:** Non dovresti eseguire il mock sulla facade `Request`. Invece, passa l'input all'interno del metodo `call` in fase di chiamata al test.

<a name="asserzioni-framework"></a>
## Asserzioni del Framework

Laravel include una serie di metodi assert per aiutarci a testare senza difficoltà:

#### Controllare Se La Risposta E' OK

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertResponseOk();
	}

#### Controllare Lo Stato Della Risposta

	$this->assertResponseStatus(403);

#### Controllare Che Le Risposte Sono Dei Redirect

	$this->assertRedirectedTo('foo');

	$this->assertRedirectedToRoute('route.name');

	$this->assertRedirectedToAction('Controller@method');

#### Controllare Che Una View Ha Qualche Dato

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertViewHas('name');
		$this->assertViewHas('age', $value);
	}

#### Controllare Che La Sessione Ha Qualche Dato

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertSessionHas('name');
		$this->assertSessionHas('age', $value);
	}

#### Controllare Che La Sessione Ha Dei Messaggi Di Errore

    public function testMethod()
    {
        $this->call('GET', '/');

        $this->assertSessionHasErrors();

        // Asserting the session has errors for a given key...
        $this->assertSessionHasErrors('name');

        // Asserting the session has errors for several keys...
        $this->assertSessionHasErrors(array('name', 'age'));
    }

#### Controllare Che Un Old Input Abbia Qualche Dato

	public function testMethod()
	{
		$this->call('GET', '/');

		$this->assertHasOldInput();
	}

<a name="metodi-helper"></a>
## Metodi Di Helper

La classe `TestCase` contiene vari metodi helper per rendere il testing della tua applicazione il semplice possibile.

#### Impostare E Svuotare Una Sessione Da Un Test

	$this->session(['foo' => 'bar']);

	$this->flushSession();

#### Impostare L'Utente Autenticato Attuale

Puoi impostare l'utente autenticato attuale usando il metodo `be`:

	$user = new User(array('name' => 'John'));

	$this->be($user);

Puoi inserire nel db dei dati con il metodo `seed`:

#### Re-Seeding Database Dai Test

	$this->seed();

	$this->seed($connection);

Maggiori informazioni su come creare un seed le puoi trovare nella sezione [migrazioni e seeding](/migration#database-seeding) della documentazione.

<a name="refreshing-applicazione"></a>
## Refreshing Dell'Applicazione

Come già sai, puoi accedere al tuo `Application` / IoC Container via `$this->app` da qualsiasi metodo per il test. Questa istanza dell'applicazione è resettata per ogni classe test.Se desideri forzare il refresh dell’Application per un determinato metodo, puoi usare il metodo `refreshApplication` dal tuo metodo test. Questa resetterà qualsiasi binding extra, come i mock, che sono stati sostituiti nel IoC container nel momento in cui è partito il test.
