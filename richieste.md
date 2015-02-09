# Richieste HTTP

- [Ottenere Una Istanza Request](#ottenere-istanza-request)
- [Recuperare L'Input](#recuperare-input)
- [Input Precedente](#input-precedente)
- [Cookie](#cookie)
- [File](#file)
- [Altre Informazioni Sulla Classe Request](#altre-informazioni-classe-request)

<a name="ottenere-istanza-request"></a>
## Ottenere Una Istanza Request

### Via Facade

La facade `Request` ti garantirà l'accesso alla richiesta corrente contenuta nel container. Per esempio:

	$name = Request::input('name');

Ricorda, se sei in un namespace, dovrai importare la facade `Request` usando lo statement `use Request;` in cima al file della tua classe.

### Via Dependency Injection

Per ottenere un istanza della richiesta HTTP corrente via dependency injection, puoi importare la classe nel costruttore del tuo controller oppure in un suo metodo. L'istanza della richiesta corrente sarà automaticamente iniettata dal [service container](/container):

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller {

		/**
		 * Store a new user.
		 *
		 * @param  Request  $request
		 * @return Response
		 */
		public function store(Request $request)
		{
			$name = $request->input('name');

			//
		}

	}

Se il metodo del controller riceve un input dal parametro di una route, inserisci gli eventuali parametri dopo  le altre dipendenze:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller {

		/**
		 * Store a new user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function update(Request $request, $id)
		{
			//
		}

	}

<a name="recuperare-input"></a>
## Recuperare L'Input

#### Recupero Di Un Valore Di Un Input

Usando pochi semplici metodi, puoi accedere a tutti gli input utenti dall' istanza `Illuminate\Http\Request`. Non ti devi preoccupare del verbo HTTP usato per la richiesta, perchè l'accesso agli input avviene allo stesso modo per tutti i verbi HTTP.

	$name = Request::input('name');

#### Recupero Di Un Valore Di Default Se Il Valore Di Un Input Non E' Presente

	$name = Request::input('name', 'Sally');

#### Determinare Se Il Valore Di Un Input E' Presente

	if (Request::has('name'))
	{
		//
	}

#### Recuperare Tutti Gli Input Di Una Richiesta

	$input = Request::all();

#### Recuperare Solo Alcuni Input Dalla Richiesta

	$input = Request::only('username', 'password');

	$input = Request::except('credit_card');

Quando si lavora sui form con input “array”, puoi usare la notazione dot per accedere agli elementi:

	$input = Request::input('products.0.name');

<a name="input-precedente"></a>
## Input Precedente

Laravel ti offre la possibilità di mantenere l'input di una richiesta durante una successiva richiesta. Per esempio, puoi ripopolare un form dopo aver controllato l'input per errori di validazione.

#### Flashing Dell'Input Nella Sessione

Il metodo `flash` memorizzerà gli input correnti nella [sessione](/sessioni) in modo da renderli disponibili, durante la richiesta successiva dell'utente, all'applicazione:

	Request::flash();

#### Flashing Di Alcuni Input Nella Sessione

	Request::flashOnly('username', 'email');

	Request::flashExcept('password');

#### Flash & Redirect

Dal momento che spesso si vuole fare il flash dell’input in associazione con un redirect alla pagina precedente, si può mettere facilmente a catena il flash su un redirect.

	return redirect('form')->withInput();

	return redirect('form')->withInput(Request::except('password'));

#### Recupero Dati Precedenti

Per recuperare i dati memorizzati nella richiesta precedente, usa il metodo `old` dell'istanza  `Request`.

	$username = Request::old('username');

Se vuoi visualizzare l'input precedente all'interno di un template Blade, è molto conveniente usare la funzione helper `old`:

	{{ old('username') }}

<a name="cookie"></a>
## Cookie

Tutti i cookie creati del framework Laravel vengono crittografati e firmati con un codice di autenticazione. Ciò vuol dire che saranno considerati validi se sono stati cambiati dal client. 

#### Recuperare Un Valore Di Un Cookie

	$value = Request::cookie('name');

#### Allegare Un Nuovo Cookie Ad Una Risposta

L'helper `cookie` fornice un modo semplice di generare una nuova istanza di `Symfony\Component\HttpFoundation\Cookie`. Il cookie può essere allegato ad una istanza `Response` usando il metodo `withCookie`:

	$response = new Illuminate\Http\Response('Hello World');

	$response->withCookie(cookie('name', 'value', $minutes));

#### Creare Un Cookie Che Duri Per Sempre*

_Durare "per sempre", significa veramente cinque anni._

	$response->withCookie(cookie()->forever('name', 'value'));

<a name="file"></a>
## File

#### Recuperare Un File Caricato

	$file = Request::file('photo');

#### Determinare Se Un File E' Stato Caricato

	if (Request::hasFile('photo'))
	{
		//
	}

L'oggetto ritornato dal metodo `file` è un'istanza della classe `Symfony\Component\HttpFoundation\File\UploadedFile`, che estende la classe PHP `SplFileInfo` e fornisce vari metodi per interagire con il file.

#### Determinare La Validità Di Un File Caricato

	if (Request::file('photo')->isValid())
	{
		//
	}

#### Spostare Un File Caricato

	Request::file('photo')->move($destinationPath);

	Request::file('photo')->move($destinationPath, $fileName);

### Altri Metodi Sui File

Ci sono una serie di metodi disponibili sull'istanza `UploadedFile` instances. Controlla la [documentazione delle API per questa classe] http://api.symfony.com/2.5/Symfony/Component/HttpFoundation/File/UploadedFile.html) per ulteruiori informazioni riguardo questi metodi.

<a name="altre-informazioni-classe-request"></a>
## Altre Informazioni Sulla Classe Request

La classe `Request` fornisce molti metodi per esaminare una richiesta HTTP per la tua applicazione, ed estende la classe  `Symfony\Component\HttpFoundation\Request` class.Qui di seguito un focus su alcuni metodi.

#### Recuperare Un URL Dalla Richiesta

	$uri = Request::path();

#### Recupero Di Un Metodo

	$method = Request::method();

	if (Request::isMethod('post'))
	{
		//
	}

#### Determinare Se Il Percorso Della Richiesta Coincide Con Un Pattern

	if (Request::is('admin/*'))
	{
		//
	}

#### Recupero Dell'URL Corrente Della Richiesta

	$url = Request::url();
