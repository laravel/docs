# Validazione

- [Introduzione](#introduzione)
- [Primi Passi](#primi-passi)
- [Altre Modalità di Validazione](#altre-modalita-validazione)
	- [Creare Manualmente il Validator](#creare-manualmente-validator)
	- [Validazione con una Form Request](#validazione-form-request)
- [Lavorare con i Messaggi di Errore](#lavorare-messaggi-errore)
	- [Messaggi di Errore Personalizzati](#messaggi-errore-personalizzati)
- [Regole di Validazione Disponibili](#regole-validazione-disponibili)
- [Aggiungere delle Regole in Base a Condizioni](#aggiungere-regole-base-condizioni)
- [Regole di Validazione Personalizzate](#regole-validazione-personalizzate)

<a name="introduzione"></a>
## Introduzione

Laravel fornisce svariate possibilità per quanto riguarda la validazione dei dati della tua applicazione. Di default, ogni controller fa uso di un trait _ValidatesRequest_, che permette, tramite un metodo di comodo, di validare le richieste in arrivo con molte tipologie di regole diverse.

<a name="primi-passi"></a>
## Primi Passi

Per capire meglio il sistema di validazione di Laravel, faremo un esempio completo di un caso d'uso pratico. Mostreremo al nostro utente un form in cui inserire dei dati, che verranno poi inviati all'applicazione. In caso di problemi in fase di validazione il sistema si occuperà di rimandare l'utente al punto di partenza, con le dovute informazioni aggiuntive su cosa è andato storto.

#### Definire le Route

Innanzitutto, supponiamo di avere le seguenti route definite nel file `app/Http/routes.php`:

	// Qui mostro un form...
	Route::get('post/create', 'PostController@create');

	// Qui memorizzo il post...
	Route::post('post', 'PostController@store');

Ovviamente, il metodo in _GET_ mostrerà un form dedicato alla creazione di un nuovo post. Il metodo in _POST_, invece, si occuperà di salvarlo sul database.

#### Creare il Controller

Bene. Adesso, diamo uno sguardo a questo semplice controller, i cui metodi saranno "raggiunti" dalle due route appena viste.

	<?php namespace App\Http\Controllers;

	use Illuminate\Http\Request;
	use App\Http\Controllers\Controller;

	class PostController extends Controller
	{
		/**
		 * Mostra il form con il quale creare un post.
		 *
		 * @return Response
		 */
		public function create()
		{
			return view('post.create');
		}

		/**
		 * Memorizza il post.
		 *
		 * @param  Request  $request
		 * @return Response
		 */
		public function store(Request $request)
		{
			// Valida i dati in arrivo e poi memorizza il post...
		}
	}

#### Scrivere la Logica di Validazione

Ora siamo pronti ad implementare il metodo _store_ in modo adeguato. Se esamini attentamente il controller di base, quello da cui derivano tutti gli altri della tua applicazione (parlo di `App\Http\Controllers\Controller`), puoi notare che viene usato il trait _ValidatesRequest_. Il suo scopo è fornire un metodo di comodo per la validazione, che puoi usare in ogni controller.

Tale metodo _validate_ accetta come parametro, una richiesta HTTP (la classe Request) ed un set di regole di validazione. Se i dati passati nella richiesta "passano" questo test di validazione, il resto del codice viene eseguito normalmente. In caso contrario, invece, l'utente viene reindirizzato alla pagina dove si trovava precedentemente, con l'aggiunta di un set di dati (informazioni relative agli errori) da poter mostrare.

Per capirci meglio, torniamo al nostro esempio:

	/**
	 * Store a new blog post.
	 *
	 * @param  Request  $request
	 * @return Response
	 */
	public function store(Request $request)
	{
		$this->validate($request, [
			'title' => 'required|unique:posts|max:255',
			'body' => 'required',
		]);

		// Se il post è valido, posso eseguire le istruzioni di memorizzazione del post...
	}

Come puoi vedere, tutto quello che devi fare è passare l'oggetto _$request_ al metodo _validate_, seguito dalle regole di validazione come array associativo. Nel caso in cui la validazione non dovesse andare a buon fine ci penserebbe direttamente Laravel a rimandarti alla pagina di partenza.

A questo punto ti starai chiedendo... "ok, ma come mostro gli errori?"

#### Mostrare gli Errori di Validazione

Supponiamo che la procedura di validazione sia andata male. L'utente ha inserito qualcosa di sbagliato ed il validatore ci ha preso e rimandati alla pagina precedente. Quello che non vedi, però, è che i dati relativi agli errori sono stati presi e ["flashati" in sessione](/documentazione/5.1/sessioni#dati-flash).

Probabilmente ti starai chiedendo perché non leggi da nessuna parte qualcosa che ricordi, anche vagamente, un bind esplicito degli errori con la view. Ecco svelata la soluzione: **Laravel, quando trova dei dati su errori flashati in sessione, li "aggancia" direttamente alla view**. Comodo, no? E saranno sempre utilizzabili come _$errors_. Più precisamente, _$errors_ sarà di tipo `Illuminate\Support\MessageBag` e potrà essere usata in questo modo:

	<!-- /resources/views/post/create.blade.php -->

	<h1>Create Post</h1>

	@if (count($errors) > 0)
		<div class="alert alert-danger">
			<ul>
				@foreach ($errors->all() as $error)
					<li>{{ $error }}</li>
				@endforeach
			</ul>
		</div>
	@endif

	<!-- Create Post Form -->

Se vuoi saperne di più, guarda [questa parte della documentazione](#lavorare-messaggi-errore)

#### Personalizzare il Formato degli Errori

Se vuoi, puoi personalizzare come meglio credi gli errori di validazione nella loro formattazione, in modo tale da poter essere "sparati" al meglio della forma quando necessario. Se ne hai bisogno, effettua l'override del metodo _formatValidationErrors_ del tuo controller di base.

Ricorda inoltre di importare `Illuminate\Contracts\Validation\Validator` all'inizio del tuo file.

	<?php namespace App\Http\Controllers;

	use Illuminate\Foundation\Bus\DispatchesJobs;
	use Illuminate\Contracts\Validation\Validator;
	use Illuminate\Routing\Controller as BaseController;
	use Illuminate\Foundation\Validation\ValidatesRequests;

	abstract class Controller extends BaseController
	{
	    use DispatchesJobs, ValidatesRequests;

		/**
		 * {@inheritdoc}
		 */
		protected function formatValidationErrors(Validator $validator)
		{
			return $validator->errors()->all();
		}
	}

### Validazione e Richieste AJAX

In questo esempio abbiamo usato un form classico per inviare dei dati all'applicazione. Tuttavia, molte applicazioni moderne fanno largo uso di richieste AJAX. Chiaramente, per una richiesta AJAX non si può generare una semplice risposta di redirect, ma restituire un output di tipo totalmente diverso. Magari JSON, con uno status code HTTP 422.

Beh... è esattamente quello che fa Laravel, senza che tu faccia altro. Il controllo della richiesta (se "normale" oppure AJAX) viene fatto direttamente dal framework. Comodo vero?

<a name="altre-modalita-validazione"></a>
## Altre Modalità di Validazione

<a name="creare-manualmente-validator"></a>
### Creare Manualmente il Validator

Se non vuoi usare il metodo _validate_ visto poco fa, o hai bisogno di più libertà d'azione, puoi sempre creare una nuova istanza di validatore, usando la facade _Validator_. Precisamente, devi usare il metodo _make_.

	<?php namespace App\Http\Controllers;

	use Validator;
	use Illuminate\Http\Request;
	use App\Http\Controllers\Controller;

	class PostController extends Controller
	{
		/**
		 * Store a new blog post.
		 *
		 * @param  Request  $request
		 * @return Response
		 */
		public function store(Request $request)
		{
			$validator = Validator::make($request->all(), [
				'title' => 'required|unique:posts|max:255',
				'body' => 'required',
			]);

			if ($validator->fails()) {
				return redirect('post/create')
							->withErrors($validator)
							->withInput();
			}

			// Memorizzo il post...
		}
	}

Il primo parametro passato al metodo è l'array di dati da validare. Il secondo, invece, è l'insieme di regole validazione, sotto la forma di array associativo.

Dopo aver controllato se la validazione è andata a buon fine o meno, puoi decidere di mandare in sessione i dati degli errori usando il metodo _withErrors_, concatenandone la chiamata al metodo _redirect_. Ricorda che il metodo _withErrors_ accetta come parametro un validator (quello che hai appena usato), un'istanza _MessageBag_ oppure un semplice array PHP.

#### Dare un Nome ad una Error Bag

A volte puoi ritrovarti con più form su una singola pagina. Perfettamente nomrmale! In questo caso, avere una semplice _MessageBag_ potrebbe risultare ambiguo: per quale form dovresti usarla? Puoi tranquillamente ovviare al problema dandole un nome. Tale nome non è altro che una stringa, passata come secondo parametro a _withErrors_.

	return redirect('register')
				->withErrors($validator, 'login');

Dopodiché, per accedervi, non devi fare altro che specificare il nome scelto come proprietà di _$errors_ per richiamare questa o quella _MessageBag_, così:

	{{ $errors->login->first('email') }}

#### Hook Post-Validazione

Il validator ti permette, con estrema semplicità, di "agganciare" una callback subito dopo il completamento della procedura di validazione. Tutto quello che devi fare è usare il metodo _after_, in questo modo:

	$validator = Validator::make(...);

	$validator->after(function($validator) {
		if ($this->somethingElseIsInvalid()) {
			$validator->errors()->add('field', 'Something is wrong with this field!');
		}
	});

	if ($validator->fails()) {
		//
	}

<a name="validazione-form-request"></a>
### Validazione con una Form Request

Le possibilità a disposizione non finiscono qui. In casi più complessi, infatti, potresti ritrovarti a voler implementare una "form request". Tipicamente, le form request sono delle classi che implementano una richiesta "personalizzata", contenenti anche la logica di validazione.

Per crearne una, usa il comando `make:request` di Artisan:

	php artisan make:request StoreBlogPostRequest

La classe generata verrà messa in `app/Http/Requests`. Vediamo ora come aggiungerci le regole di validazione correlate.

	/**
	 * Get the validation rules that apply to the request.
	 *
	 * @return array
	 */
	public function rules()
	{
		return [
			'title' => 'required|unique:posts|max:255',
			'body' => 'required',
		];
	}

Esatto: ti basta fare in modo che il metodo _rules_ ritorni un array associativo con le regole di validazione. Il formato è quello che hai già visto in precedenza. A quel punto non devi fare altro che sostituire la _$request_ base con quella appena creata...

	/**
	 * Store the incoming blog post.
	 *
	 * @param  StoreBlogPostRequest  $request
	 * @return Response
	 */
	public function store(StoreBlogPostRequest $request)
	{
		// Il codice qui viene eseguito solo se i dati sono validati correttamente...
	}

Se la procedura di validazione fallisce, l'utente viene reindirizzato verso la sua posizione precedente. Esattamente come visto prima, inoltre, eventuali errori vengono messi in sessione e sono quindi pronti ad essere visualizzati. Infine, in caso di richiesta AJAX, la _MessageBag_ viene restituita in JSON con un codice 422.

#### Autorizzare una Form Request

Una form request, inoltre, può implementare anche un metodo _authorize_. Come il nome suggerisce, questo metodo può essere usato per controllare se un certo utente ha il "permesso" per aggiornare una certa risorsa. Ad esempio, immagina di voler implementare la modifica di un commento da parte dell'utente. Come fare per capire se, effettivamente, quel commento è suo?

Così:

	/**
	 * Determine if the user is authorized to make this request.
	 *
	 * @return bool
	 */
	public function authorize()
	{
		$commentId = $this->route('comment');

		return Comment::where('id', $commentId)
                      ->where('user_id', Auth::id())->exists();
	}

Fai caso alla chiamata di _route_ questo metodo ti da l'accesso ai parametri passati tramite URI definiti sulla route chiamata, come ad esempio, in questo caso, _{comment}_.

	Route::post('comment/{comment}');

Il metodo authorize può ritornare _true_ o _false_. Se ritorna _true_ tutto bene, non bisogna fare altro e la richiesta viene processata. In caso contrario, invece, viene ritornata una risposta HTTP con status code 403. Il codice nel controller non verrà eseguito.

Se prevedi di implementare altrove la logica di autorizzazione, fai in modo che il metodo ritorni semplicemente _true_.

	/**
	 * Determine if the user is authorized to make this request.
	 *
	 * @return bool
	 */
	public function authorize()
	{
		return true;
	}

#### Personalizzare il Formato dei Messaggi di Errore

Se vuoi personalizzare il formato degli errori di validazione che vengono flashati in sessione, effettua l'override del metodo _formatErrors_ sulla classe _Request_ base (`App\Http\Requests\Request`). Non scordarti di importare `Illuminate\Contracts\Validation\Validator` all'inizio del file.

	/**
	 * {@inheritdoc}
	 */
	protected function formatErrors(Validator $validator)
	{
		return $validator->errors()->all();
	}

<a name="lavorare-messaggi-errore"></a>
## Lavorare con i Messaggi di Errore

Dopo aver chiamato il metodo _errors_ sull'istanza di _Validator_ riceverai come risultato un'istanza di `Illuminate\Support\MessageBag`, which has a variety of convenient methods for working with error messages.

#### Recuperare il Primo Messaggio di Errore

Per recuperare il primo messaggio di errore della box, usa _first_.

	$messages = $validator->errors();

	echo $messages->first('email');

#### Recuperare Tutti i Messaggi per un Campo

Se vuoi recuperare tutti i messaggi di errore per un certo campo, usa _get_.

	foreach ($messages->get('email') as $message) {
		//
	}

#### Recuperare Tutti i Messaggi di Errore

To retrieve an array of all messages for all fields, use the `all` method:

	foreach ($messages->all() as $message) {
		//
	}

#### Verificare se ci sono Errori per un Campo

	if ($messages->has('email')) {
		//
	}

#### Formattare uno Specifico Messaggio di Errore

	echo $messages->first('email', '<p>:message</p>');

#### Formattare Tutti i Messaggi di Errore

	foreach ($messages->all('<li>:message</li>') as $message) {
		//
	}

<a name="messaggi-errore-personalizzati"></a>
### Messaggi di Errore Personalizzati

Se necessario, puoi personalizzare come meglio credi i messaggi di errore, per definirne di tuoi al posto di quelli predefiniti. Ci sono svariati modi di definire dei messaggi custom.

Per cominciare, puoi passare al metodo _validate_ o a _Validator::make_, come terzo parametro, un array di questo tipo:

	$messages = [
		'required' => 'The :attribute field is required.',
	];

	$validator = Validator::make($input, $rules, $messages);

Nell'esempio, `:attribute` è un segnaposto per il valore effettivo. Ci sono svariati segnaposti a disposizione: eccone alcuni.

	$messages = [
		'same'    => 'The :attribute and :other must match.',
		'size'    => 'The :attribute must be exactly :size.',
		'between' => 'The :attribute must be between :min - :max.',
		'in'      => 'The :attribute must be one of the following types: :values',
	];

#### Specificare un Messaggio Personalizzato per un Campo

Se dovessi averne bisogno, sappi che puoi arrivare a personalizzare il messaggio di errore per il singolo campo. Così:

	$messages = [
		'email.required' => 'We need to know your e-mail address!',
	];

#### Specificare i Messaggi nei File di Lingua

In molti casi, i tuoi messaggi di errore cambieranno in base alla lingua scelta. In questo caso, basta modificare il file `resources/lang/xx/validation.php`, dove _xx_ è la lingua che ti interessa.

	'custom' => [
		'email' => [
			'required' => 'We need to know your e-mail address!',
		],
	],

<a name="regole-validazione-disponibili"></a>
## Regole di Validazione Disponibili

Di seguito, una lista di tutte le regole di validazione disponibili.

Below is a list of all available validation rules and their function:

- [Accepted](#regola-accepted)
- [Active URL](#regola-active-url)
- [After (Date)](#regola-after)
- [Alpha](#regola-alpha)
- [Alpha Dash](#regola-alpha-dash)
- [Alpha Numeric](#regola-alpha-num)
- [Array](#regola-array)
- [Before (Date)](#regola-before)
- [Between](#regola-between)
- [Boolean](#regola-boolean)
- [Confirmed](#regola-confirmed)
- [Date](#regola-date)
- [Date Format](#regola-date-format)
- [Different](#regola-different)
- [Digits](#regola-digits)
- [Digits Between](#regola-digits-between)
- [E-Mail](#regola-email)
- [Exists (Database)](#regola-exists)
- [Image (File)](#regola-image)
- [In](#regola-in)
- [Integer](#regola-integer)
- [IP Address](#regola-ip)
- [Max](#regola-max)
- [MIME Types (File)](#regola-mimes)
- [Min](#regola-min)
- [Not In](#regola-not-in)
- [Numeric](#regola-numeric)
- [Regular Expression](#regola-regex)
- [Required](#regola-required)
- [Required If](#regola-required-if)
- [Required With](#regola-required-with)
- [Required With All](#regola-required-with-all)
- [Required Without](#regola-required-without)
- [Required Without All](#regola-required-without-all)
- [Same](#regola-same)
- [Size](#regola-size)
- [String](#regola-string)
- [Timezone](#regola-timezone)
- [Unique (Database)](#regola-unique)
- [URL](#regola-url)

<a name="regola-accepted"></a>
#### accepted

Il campo deve avere un valore pari a _yes_, _on_, _1_, o _true_. Può essere utile quando un utente deve accettare i termini di servizio di un prodotto.

<a name="regola-active-url"></a>
#### active_url

Il campo deve essere un URL valido, verificabile con `checkdnsrr` di PHP.

<a name="regola-after"></a>
#### after:_date_

Il campo deve avere un valore successivo alla data _date_ fornita. Le date verranno parsate con _strtotime_.

<a name="regola-alpha"></a>
#### alpha

Il campo deve essere una stringa di caratteri alfabetici.

<a name="regola-alpha-dash"></a>
#### alpha_dash

Il campo deve essere una stringa alfanumerica, ma può contenere anche underscore (_) e dash (-).

<a name="regola-alpha-num"></a>
#### alpha_num

Il campo deve essere una stringa di caratteri alfanumerici.

<a name="regola-array"></a>
#### array

Il campo deve essere un array valido.

<a name="regola-before"></a>
#### before:_date_

Il campo deve avere un valore precedente alla data _date_ fornita. La data verrà parsata usando `strtotime`.

<a name="regola-between"></a>
#### between:_min_,_max_

Il campo deve avere una dimensione compresa tra _min_ e _max_. Stringhe, numeri e file vengono "valutati" con gli stessi criteri di [`size`](#regola-size).

<a name="regola-boolean"></a>
#### boolean

Il campo deve avere un valore booleano valido (anche con cast). Ovvero: `true`, `false`, `1`, `0`, `"1"`, o `"0"`.

<a name="regola-confirmed"></a>
#### confirmed

Il campo deve avere lo stesso valore di un altro campo, che porta lo stesso nome con l'aggiunta di *_confirmation*. Ad esempio, per il campo *password* dovrà esistere un campo *password_confirmation*.

<a name="regola-date"></a>
#### date

Il campo deve avere come valore una data valida riconoscibile da `strtotime`.

<a name="regola-date-format"></a>
#### date_format:_format_

Il campo deve avere un valore con un formato verificabile tramite `date_parse_from_format`.

<a name="regola-different"></a>
#### different:_field_

Il campo deve avere un valore differente dal campo _field_.

<a name="regola-digits"></a>
#### digits:_value_

Il campo deve essere numerico ed avere una lunghezza esatta di _value_.

<a name="regola-digits-between"></a>
#### digits_between:_min_,_max_

Il campo deve avere un numero di cifre compreso tra _min_ e _max_.

<a name="regola-email"></a>
#### email

Il campo deve avere come valore un indirizzo email valido.

<a name="regola-exists"></a>
#### exists:_table_,_column_

Il campo deve avere un valore unico rispetto a quelli già presenti su una certa tabella del database.

#### Uso Base

	'state' => 'exists:states'

#### Specificare il Nome della Colonna

	'state' => 'exists:states,abbreviation'

Se vuoi, puoi anche specificare alcune condizioni.

	'email' => 'exists:staff,email,account_id,1'

Puoi anche passare _NULL_ come valore per un controllo.

	'email' => 'exists:staff,email,deleted_at,NULL'

<a name="regola-image"></a>
#### image

Il campo (file) deve essere un'immagine (jpeg, png, bmp, gif, or svg).

<a name="regola-in"></a>
#### in:_foo_,_bar_,...

Il valore del campo deve essere presente in una lista di valori possibili.

<a name="regola-integer"></a>
#### integer

Il valore del campo deve essere un intero.

<a name="regola-ip"></a>
#### ip

Il valore del campo deve essere un indirizzo IP valido.

<a name="regola-max"></a>
#### max:_value_

Il valore del campo deve essere minore o uguale a _value_. Stringhe, numeri e file vengono valutati così come succede con [`size`](#regola-size).

<a name="regola-mimes"></a>
#### mimes:_foo_,_bar_,...

Il file sotto validazione deve avere un MIME type corrispondente ad uno presente nella lista specificata.

#### Uso Base

	'photo' => 'mimes:jpeg,bmp,png'

<a name="regola-min"></a>
#### min:_value_

Il valore del campo deve essere maggiore o uguale a _value_. Stringhe, numeri e file vengono valutati così come succede con [`size`](#regola-size).

<a name="regola-not-in"></a>
#### not_in:_foo_,_bar_,...

Il valore del campo non deve essere presente nella data lista.

<a name="regola-numeric"></a>
#### numeric

Il valore del campo deve essere numerico.

<a name="regola-regex"></a>
#### regex:_pattern_

Il valore del campo deve corrispondere ad una certa espressione regolare.

**Nota:** usando il pattern _regex_ potrebbe essere necessario specificare le regole all'interno di un array, e non in una semplice stringa con i pipe | come delimitatori.

<a name="regola-required"></a>
#### required

Il campo deve essere presente nei dati di input.

<a name="regola-required-if"></a>
#### required_if:_field_,_value_,...

Il campo deve essere presente se il campo _field_ è uguale a _value_.

<a name="regola-required-with"></a>
#### required_with:_foo_,_bar_,...

Il campo deve essere presente solo se uno degli altri specificati lo è.

<a name="regola-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

Il campo deve essere presente solo se tutti gli altri campi elencati lo sono.

<a name="regola-required-without"></a>
#### required_without:_foo_,_bar_,...

Il campo deve essere presente solo se uno dei campi elencati non lo è.

<a name="regola-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

Il campo deve essere presente solo se tutti i campi elencati non lo sono.

<a name="regola-same"></a>
#### same:_field_

Il campo _field_ deve corrispondere a quello preso in esame.

<a name="regola-size"></a>
#### size:_value_

Il campo da validare deve avere una dimensione pari a _value_. Per le stringhe, per dimensione si intende il conteggio dei caratteri. Per i numeri corrisponde ad un valore specifico, mentre per i file corrisponde alla grandezza in kilobyte.

<a name="regola-string"></a>
#### string

Il valore inserito deve essere una stringa.

<a name="regola-timezone"></a>
#### timezone

Il valore inserito deve essere un identificatore valido di timezone, riconosciuto dalla funzione PHP `timezone_identifiers_list`.

<a name="regola-unique"></a>
#### unique:_table_,_column_,_except_,_idColumn_

Il campo sotto validazione deve essere unico in una certa tabella. Se il nome della tabella _column_ non è specificato, verrà usato il nome del campo.

**Specificare un Nome Personalizzato per una Colonna:**

	'email' => 'unique:users,email_address'

**Connessione al Database Personalizzata**

A volte potresti avere la necessità di impostare una connessione specifica per quanto riguarda le query del Validator. Come puoi facilmente immaginare, `unique:users` userà la connessione al database di default. Puoi personalizzare questo comportamento tramite una sintassi di tipo *nome_connessione.tabella*.

	'email' => 'unique:connection.users,email_address'

**Forzare la Regola Unique ad Ignorare un ID**

In caso di aggiornamento di un dato specifico, potresti avere la necessità di ignorare la regola _unique_. Immagina, infatti, di implementare una funzionalità di "aggiornamento del profilo" di un utente. Certo, l'email deve essere sempre unica, ma che succede se l'utente non cambia il suo indirizzo, tenendo sempre lo stesso? Teoricamente riceveresti un errore, perché il valore immesso esiste già nel database. In realtà, però, puoi ignorare uno specifico ID con questa sintassi:

	'email' => 'unique:users,email_address,'.$user->id

**Aggiungere Ulteriori Clausole Where:**

Puoi aggiungere altre clausole e condizioni alla tua query in modo abbastanza semplice:

	'email' => 'unique:users,email_address,NULL,id,account_id,1'

Secondo questa regola, in un eventuale controllo verrebbero prese in considerazione solo i record con `account_id` pari ad `1`.

<a name="regola-url"></a>
#### url

Il campo sotto validazione deve essere un URL valido, verificabile tramite la funzione `filter_var`.

<a name="aggiungere-regole-base-condizioni"></a>
## Aggiungere delle Regole in Base a Condizioni

In alcune situazioni potresti avere la necessità di eseguire una procedura di validazione solo se alcuni campi sono presenti. In casi come questi puoi usare _sometimes_:

	$v = Validator::make($data, [
		'email' => 'sometimes|required|email',
	]);

Nell'esempio appena visto, _email_ verrà validato solo se presente nell'array _$data_.

#### Validazione Condizionale più Complessa

Un'altra necessità potrebbe essere l'inclusione di alcune regole di validazione in base a logiche più complesse. Ad esempio, potresti voler richiedere obbligatoriamente un campo se un altro campo ha un valore maggiore di 100. Oppure, potresti richiedere obbligatoriamente due campi solo se un altro campo è già presente. Vediamo come fare.

Innanzitutto crea una nuova istanza della classe `Validator` con le regole di cui sei sicuro al 100%:

	$v = Validator::make($data, [
		'email' => 'required|email',
		'games' => 'required|numeric',
	]);

Supponiamo che questa applicazione serva a dei collezionisti di giochi. Se il collezionista registra più di 100 giochi, vogliamo che spieghi perché ha tutti questi giochi. Ad esempio, perché ha un negozio e li rivende, o magari semplicemente apprezza collezionarne. Dobbiamo quindi introdurre una regola in modo condizionale.

Possiamo usare il metodo _sometimes_ come segue sul campo _reason_.

	$v->sometimes('reason', 'required|max:500', function($input) {
		return $input->games >= 100;
	});

Il primo argomento passato sarà il nome del campo, _reason_ appunto. Il secondo, invece, sarà una Closure alla quale passeremo come parametro l'array dei dati in input chiamato, in questo caso, _$input_. Tale metodo dovrà ritornare _true_ per validare la condizione.

	$v->sometimes(['reason', 'cost'], 'required', function($input) {
		return $input->games >= 100;
	});

<a name="regole-validazione-personalizzate"></a>
## Regole di Validazione Personalizzate

Laravel fornisce, come hai potuto vedere, tantissime regole di validazione di ogni genere. Le vie del signore, però, sono infinite. Potresti facilmente ritrovarti a dovertene creare una tua. Per fortuna, puoi ovviare al problema molto facilmente tramite il metodo _extend_ della facade _Validator_.

Una buona norma sarebbe quella di richiamare il metodo in un [service provider](/documentazione/5.1/provider).

	<?php namespace App\Providers;

	use Validator;
	use Illuminate\Support\ServiceProvider;

	class AppServiceProvider extends ServiceProvider
	{
	    /**
	     * Bootstrap any application services.
	     *
	     * @return void
	     */
		public function boot()
		{
			Validator::extend('foo', function($attribute, $value, $parameters) {
				return $value == 'foo';
			});
		}

		/**
		 * Register the service provider.
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}
	}

La _Closure_ specificata riceve tre parametri: il nome dell'attributo _$attribute_ da validare, il _$valore_ presente ed un array di parametri _$parameters_ da passare alla regole.

Puoi anche decidere di passare una specifica classe ed un relativo metodo al posto di una _Closure_, con questa sintassi:

	Validator::extend('foo', 'FooValidator@validate');

#### Definire il Messaggio di Errore

Per la tua regola avrai bisogno di registrare anche un messaggio di errore di default. Niente di più semplice: basta aggiungere l'opportuno elemento al file di lingua relativo alla validazione. Ad esempio _resources/lang/en/validation.php_, per capirci. Il messaggio dovrebbe essere inserito nel primo livello dell'array, in ogni caso non nell'elemento _custom_ usato per messaggi specifici per gli attributi.

	"foo" => "Your input was invalid!",

    "accepted" => "The :attribute must be accepted.",

    // The rest of the validation error messages...

Quando crei una regola di validazione personalizzata, potresti voler definire un segnaposto di default per i messaggi di errore. Se è il tuo caso, tutto quello che devi fare è richiamare il metodo _replacer_ della facade _Validator_. Puoi farlo sempre all'interno del metodo _boot_ di un [service provider](/documentazione/5.1/provider):

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
	public function boot()
	{
		Validator::extend(...);

		Validator::replacer('foo', function($message, $attribute, $rule, $parameters) {
			return str_replace(...);
		});
	}
