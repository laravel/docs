# Richieste HTTP

- [Accedere alla Richiesta](#accedere-alla-richiesta)
	- [Informazioni Base della Richiesta](#informazioni-base-richiesta)
	- [Richieste PSR-7](#richieste-psr7)
- [Recupeare L'Input](#recuperare-input)
	- [Input Precedente](#input-precedente)
	- [Cookie](#cookie)
	- [File](#file)

<a name="accedere-alla-richiesta"></a>
## Accedere alla Richiesta

Per ottenere un istanza di una richiesta HTTP tramite dependency injection, devi importare la classe `Illuminate\Http\Request` nel construttore o nel metodo del controller. L'istanza corrente sarà automaticamente iniettata dal [service container](/docs/{{version}}/container):

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller
	{
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

Se il metodo del controller si aspetta di ricevere dai parametri da una route, inserisci i parametri dopo le altre dipendeze. Per esempio, se la tua route è definita in questo modo:

	Route::put('user/{id}', 'UserController@update');

Puoi importare la classe `Illuminate\Http\Request` ed accedere al parametro id della route, modificando il tuo metodo in quesot modo:

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use Illuminate\Routing\Controller;

	class UserController extends Controller
	{
		/**
		 * Update the specified user.
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

<a name="informazioni-base-richiesta"></a>
### Informazioni Base della Richiesta

L'istanza `Illuminate\Http\Request` offre vari metodi per esaminare le richieste HTTP per la tua applicazione. La classe `Illuminate\Http\Request` estende la classe `Symfony\Component\HttpFoundation\Request`. Qui di seguito un focus su alcuni metodi:

#### Recuperare Un URL Dalla Richiesta

Il metodo `path` ritorna l'URL dalla richiesta. In questo modo, se la richiesta corrente proviene da `http://domain.com/foo/bar`, il metodo `path` ritonerà `foo/bar`:

	$uri = $request->path();

Il metodo `is` ti permette di verificare che la richiesta corrente coincida con un dato pattern. Puoi usare il carattere `*` come una wildcard quando usi questo metodo, in questo modo:

	if ($request->is('admin/*')) {
		//
	}

Per recuperare l'URL completo, non solo il path, puoi usare il metodo `url` sull'instanza della richiesta:

	$url = $request->url();

#### Recupero Di Un Metodo

Il metodo `method` recupererà il verbo HTTP per la richiesta. Puoi usare anche il metodo`isMethod` per verificare che il verbo HTTP coincida con una stringa data, in questo modo:

	$method = $request->method();

	if ($request->isMethod('post')) {
		//
	}

<a name="richieste-psr7"></a>
### Richieste PSR-7

Lo standard PSR-7 specifica le interefface per i messagi HTTP, incluse le richieste e le risposte. Se vuoi ottenere un istanza di una richiesta PSR-7, dovrai installare alcune librerie aggiuntive. Laravel usa il componente di Symphony HTTP Message Bridge per convertir le tipiche richieste e risposte Laravel in un implementazione compatibile di richiesta PSR-7:

	composer require symfony/psr-http-message-bridge

	composer require zendframework/zend-diactoros

Una volta installate queste librerie, puoi ottenere una richiesta PSR-7 importando semplicemente il tipo di richiesta nella route o nel controller:

	use Psr\Http\Message\ServerRequestInterface;

	Route::get('/', function (ServerRequestInterface $request) {
		//
	});

Se ritorni un istanza di risposta PSR-7 dalla route o dal controller, verrà automaticamente convertita ina un istanza di risposta Laravel e sarà visualizzata dal framework.

<a name="recuperare-input"></a>
## Recupeare L'Input

#### Retrieving An Input Value

Usando pochi semplici metodi, puoi accedere a tutti gli input utenti dall'istanza `Illuminate\Http\Request`. Non ti devi preoccupare del verbo HTTP usato per la richiesta, perchè l'accesso agli input avviene allo stesso modo per tutti i verbi HTTP.

	$name = $request->input('name');

Puoi passare un valore di default come secondo parametro al metodo `input`. Questo valore sarà ritornato se il valore richiesto non è presnete nella richiesta:

	$name = $request->input('name', 'Sally');

Quando stai lavorando sui form con array di input, puoi usare la notazione "dot" per accedere all'array:

	$input = $request->input('products.0.name');

#### Determinare Se Il Valore Di Un Input E' Presente

Per determinare se un valore è presente nella richiesta, puoi usare il metodo `has`. Il metodo `has` ritorna `true` se il valore è presente **e** se non presente una stringa vuota:

	if ($request->has('name')) {
		//
	}

#### Recuperare Tutti Gli Input Di Una Richiesta

Puoi anche recuperare tutti i dati di input come un `array` usando il metodo `all`:

	$input = $request->all();

#### Recuperare Solo Alcuni Input Dalla Richiesta

Se hai bisogno di recuperare un sotto-insieme degli input della richiesta, puoi usare i metodi `only` e `except`. Entrambi questi metodi accettano un singolo `array` come unico argomento:

	$input = $request->only('username', 'password');

	$input = $request->except('credit_card');

<a name="input-precedente"></a>
### Input Precedente

Laravel ti offre la possibilità di mantenere l'input di una richiesta durante una successiva richiesta. Per esempio, puoi ripopolare un form dopo aver controllato l'input per errori di validazione. Tuttavia, se stai usando la validazione inclusa di Laravel [validation services](/docs/{{version}}/validation), non sarà necessario usare manualmente questi metodi, perchè sarà il meccanismo built-in di Laravel a richiamarli automaticamente.

#### Flashing Dell'Input Nella Sessione

Il metodo `flash` sull'istanza `Illuminate\Http\Request`  memorizzerà gli input correnti nella
[sessione](/docs/{{version}}/session) in modo da renderli disponibili, durante la richiesta successiva dell'utente, all'applicazione:

	$request->flash();

Puoi usare anche i metodi `flashOnly` e `flashExcept` per memorizzare solo alcuni input della richiesta:

	$request->flashOnly('username', 'email');

	$request->flashExcept('password');

#### Flashing Dell'Input Nella Session E Redirect

Dal momento che spesso si vuole memorizzare gli input in associazione con un redirect alla pagina precedente, si può facilmente agganciarli su un redirect utilizzando il metodo `withInput`:

	return redirect('form')->withInput();

	return redirect('form')->withInput($request->except('password'));

#### Recuperare I Dati Precedenti

Per recuperare gli input memorizzati dalla precedente richiesta, usa il metodo `old` dell'istanza `Request`. Il metodo `old` offre un conveniente helper per recupare gli input fuori dalla [sessione](/docs/{{version}}/session):

	$username = $request->old('username');

Laravel offre anche una funzione hepler `old` globale. Se stai visualizzando l'input precedente all'interno di un [template Blade](/docs/{{version}}/views), è più conveniente usare l'helper `old`:

	{{ old('username') }}

<a name="cookie"></a>
### Cookie

#### Recupeare I Cookie Da Una Richiesta

Tutti i cookie creati da Laravel sono criptati e segnati da un codice di autenticazione, ciò vuol dire che saranno considerati validi se sono stati cambiati dal client. Per recupeare il valore di un cookie dalla richiesta, puoi usare il metodo `cookie` dell'istanza `Illuminate\Http\Request`:

	$value = $request->cookie('name');

#### Allegare Un Nuovo Cookie Ad Una Risposta

Laravel offre una funzione helper globale `cookie` fornice un modo semplice di generare una nuova istanza di `Symfony\Component\HttpFoundation\Cookie`Il cookie può essere allegato ad una istanza `Illuminate\Http\Response` usando il metodo `withCookie`:

	$response = new Illuminate\Http\Response('Hello World');

	$response->withCookie(cookie('name', 'value', $minutes));

	return $response;

Per crare un cookie che duri per sempre, per i prossimi cinque anni, puoi richiamare il metodo `forever` dopo la chiamata all'helper `cookie`:

	$response->withCookie(cookie()->forever('name', 'value'));

<a name="file"></a>
### File

#### Recuperare I File Caricati

Puoi accedere ai file caricati che sono inclusi con `Illuminate\Http\Request` usando il metodo `file`. L'oggeto ritornato dal metodo `file` è un istanza della classe `Symfony\Component\HttpFoundation\File\UploadedFile`, che estende la classe PHP `SplFileInfo` e fornisce una serie di metodi per interagire con i file:

	$file = $request->file('photo');

#### Verificare la Presenza di un File

Puoi anche determinare se un file è presente nella richiesta usando il meteodo `hasFile`:

	if ($request->hasFile('photo')) {
		//
	}

#### Determinare La Validità Di Un File Caricato

In aggiunta a verificare la presenza di un file, puoi anche verificare che non ci siano stati problemi durante l'upload del file, tramite il metodo:

	if ($request->file('photo')->isValid())
	{
		//
	}

#### Spostare Un File Caricato

Per spostare un file caricato in una nuova destinazione, puoi usare il metodo `move`. Questo metodo sposterà il file dalla directory di upload temporanea (determinata dalla configurazione di PHP) ad una nuova destinazione da te scelta:

	$request->file('photo')->move($destinationPath);

	$request->file('photo')->move($destinationPath, $fileName);

#### Altri Metodi sui File

Ci sono molti altri metodi disponibili per l'istanza `UploadedFile`. Controlla la [documentazione delle API per questa classe] http://api.symfony.com/2.7/Symfony/Component/HttpFoundation/File/UploadedFile.html) per ulteruiori informazioni riguardo questi metodi.
