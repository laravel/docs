# Validazione

- [Uso Base](#uso-base)
- [Validazione Controller](#validazione-controller)
- [Validazione Form Request](#validazione-form-request)
- [Lavorare Con I Messaggi Di Errore](#lavorare-con-messaggi-di-errore)
- [Messaggi Di Errore & View](#messaggi-di-errore-e-view)
- [Regole Di Validazione Disponibili](#regole-validazione-disponibili)
- [Aggiungere Regole Condizionali](#aggiungere-regole-condizionali)
- [Messaggi Di Errore Personalizzati](#messaggi-errore-personalizzati)
- [Regole Di Validazione Personalizzate](#regole-validazione-personalizzate)

<a name="uso-base"></a>
## Uso Base

Laravel mette a disposizione un semplice e conveniente meccanismo per validare i dati e ritrovare i messaggi di errore tramite la classe `Validation`.

#### Esempio Base Di Validazione

	$validator = Validator::make(
		array('name' => 'Dayle'),
		array('name' => 'required|min:5')
	);

Il primo parametro passato al metodo `make` è il dato da validare. Il secondo parametro è la regola di validazione che deve essere applicata al dato.

#### Uso Di Array Per Specificare Le Regole

Regole multiple possono essere delimitate usando il carattere “pipe”, oppure da un array di elementi.

	$validator = Validator::make(
		array('name' => 'Dayle'),
		array('name' => array('required', 'min:5'))
	);

#### Validazione Di Più Campi

    $validator = Validator::make(
        array(
            'name' => 'Dayle',
            'password' => 'lamepassword',
            'email' => 'email@example.com'
        ),
        array(
            'name' => 'required',
            'password' => 'required|min:8',
            'email' => 'required|email|unique:users'
        )
    );
Una volta che l'istanza `Validator` è stata creata, il metodo `fails` (o `passes`)  può essere usato per eseguire la validazione.

	if ($validator->fails())
	{
		// I dati non hanno passato la validaqzione
	}

Se la validazione fallisce, puoi ritrovare i messaggi di errore da validatore.

	$messages = $validator->messages();

Puoi anche accedere ad un array di regole di validazione non andate a buon fine, senza messaggi. Per fare questo, usa il metodo `failed`:

	$failed = $validator->failed();

#### Validare I File

La classe `Validator` offre diverse regole per la validazione dei file, come `size`, `mimes`, ed altre.
Quando esegui la validazione di file, puoi passarle all'interno del validatore con gli altri tuoi dati.

### After Validation Hook

Il validatore ti permette anche di usare una funzione di callback da eseguire a validazione completata. Questo ti permette di eseguire facilmente un ulteriore validazione, e di aggiungere ulteriori messaggi di errore. Per iniziare, usa il metodo `after` sull'istanza validator:

	$validator = Validator::make(...);

	$validator->after(function($validator)
	{
		if ($this->somethingElseIsInvalid())
		{
			$validator->errors()->add('field', 'Something is wrong with this field!');
		}
	});

	if ($validator->fails())
	{
		//
	}

Puoi aggiungere quante chiamate `after` al validatore, se necessario.

<a name="validazione-controller"></a>
## Validazione Controller

Naturalmente, la creazione manuale e il controllo di una istanza `Validator` ogni volta che si esegue la convalida, può essere una perdita di tempo. Non preoccuparti, hai altre opzioni! La classe controller base  `App\Http\Controllers\Controller` utilizza il trait, incluso in Laravel, `ValidatesRequests`. Questo trait offre un singolo e conveniente metodo per validare una richiesta HTTP.  Ecco come si presenta:

	/**
	 * Store the incoming blog post.
	 *
	 * @param  Request  $request
	 * @return Response
	 */
	public function store(Request $request)
	{
		$this->validate($request, [
			'title' => 'required|unique|max:255',
			'body' => 'required',
		]);

		//
	}

Se la validazione va a buon fine, il codice verrà eseguito normalmente. Mentre, se la validazione fallisce, verrà lanciata un eccezione `Illuminate\Contracts\Validation\ValidationException`. Questa eccezione viene intercettata automaticamente e genera un redirect per l'utente alla pagina precedente. Gli errori della validazione sono automaticamente salvati all'interno della sessione!

Se la richiesta è stata una richiesta AJAX, non sarà generato nessun redirect. Invece, verrà ritornata una risposta HTTP con un codice di stato 422 al browser contenente una rappresentazione JSON degli errori di validazione.

Per esempio, qui il codice equivalente scritto a mano:

	/**
	 * Store the incoming blog post.
	 *
	 * @param  Request  $request
	 * @return Response
	 */
	public function store(Request $request)
	{
		$v = Validator::make($request->all(), [
			'title' => 'required|unique|max:255',
			'body' => 'required',
		]);

		if ($v->fails())
		{
			return redirect()->back()->withErrors($v->errors());
		}

		//
	}

### Personalizzazione del Formato Degli Errori Di Validazione

Se desideri personalizzare il formato degli errori memorizzati nella sessione quando la validazione fallisce, sovrascrivi `formatValidationErrors` sul controller base. Non dimenticarti di includere la classe `Illuminate\Validation\Validator` all'inizio del file:

	/**
	 * {@inheritdoc}
	 */
	protected function formatValidationErrors(Validator $validator)
	{
		return $validator->errors()->all();
	}

<a name="validazione-form-request"></a>
## Validazione Form Request

Per scenari di validazione più complessi, potresti creare un "form request". I Form request sono delle classi request personalizzate che contengono la logica della validazione. Per creare una classe form request, usa il comando Artisan CLI `make:request`:

	php artisan make:request StoreBlogPostRequest

La classe generata verrà memorizzata nella directory `app/Http/Requests`. Andiamo ad aggiungere delle regole di validazione al metodo `rules`:

	/**
	 * Get the validation rules that apply to the request.
	 *
	 * @return array
	 */
	public function rules()
	{
		return [
			'title' => 'required|unique|max:255',
			'body' => 'required',
		];
	}

Ora, come eseguire queste regole di validazione? E' sufficiente passare al metodo del tuo controller la classe appena creata, in questo modo:

	/**
	 * Store the incoming blog post.
	 *
	 * @param  StoreBlogPostRequest  $request
	 * @return Response
	 */
	public function store(StoreBlogPostRequest $request)
	{
		// The incoming request is valid...
	}

La form request è validata prima della chiamata al metodo del controller, questo significa che non hai bisogno di inserire ulteriore logica di validazione nel tuo controller. È già stata eseguita la validazione!

Se la validazione fallisce, verrà generato un redirect che riporta l'utente alla pagina precedente. Gli errori verranno memorizzati nella sessione in modo da renderli disponibili per la visualizzazione. Se la richiesta è stata una richiesta AJAX, verrà ritornata all'utente una risposta HTTP con codice di stato 422, inclusa una rappresentazione JSON degli errori della validazione.

### Autorizzazione Form Request

La classe form request contiene anche un metodo `authorize`. All'interno di questo metodo, puoi controllare se l'utente autenticato ha l'autorizzazione ad aggiornare una data risorsa. Per esempio, se un utente sta tentando di aggiornare un commento di un post, è autorizzato ad effettuare l'aggiornamento? Per esempio:

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

Nota la chiamata al metodo `route` nell'esempio sopra illustrato. Questo metodo ti garantisce l'accesso ai parametri dell'URL definiti  per quella route durante una sua chiamata, come in questo esempio sotto viene fatto per il parametro `{comment}`:

	Route::post('comment/{comment}');

Se il metodo `authorize` ritorna `false`, verrà ritornata automaticamente una risposta HTTP con un codice di stato 403 è il metodo del tuo controller non verrà eseguito.

Se decidi di spostare la logica di autorizzazione in un altra parte della tua applicazione, ritorna semplicemente `true` dal metodo `authorize`:

	/**
	 * Determine if the user is authorized to make this request.
	 *
	 * @return bool
	 */
	public function authorize()
	{
		return true;
	}

### Personalizzazione Formato Degli Errori

Se desideri personalizzare il formato degli errori di validazione memorizzati nella sessione in caso di validazione fallita, sosvrascrivi `formatValidationErrors` nella classe request di base (`App\Http\Requests\Request`). Non dimenticare di importare la classe `Illuminate\Validation\Validator`:

	/**
	 * {@inheritdoc}
	 */
	protected function formatErrors(Validator $validator)
	{
		return $validator->errors()->all();
	}

<a name="lavorare-con-messaggi-di-errore"></a>
## Lavorare Con I Messaggi Di Errore

Dopo la chiamata al metodo `messages` su un istanza `Validator`, verrà ritornata un'istanza `MessageBag`, che contiene una serie di metodi per manipolare i messaggi di errore.

#### Ritrovare Il Primo Messaggio Di Errore Per Un Campo

	echo $messages->first('email');

#### Ritrovare Tutti I Messaggi Di Errore Per Un Campo

	foreach ($messages->get('email') as $message)
	{
		//
	}

#### Ritrovare Tutti I Messaggi Di Errore Per Tutti I Campi

	foreach ($messages->all() as $message)
	{
		//
	}

#### Determinare L'Esistenza Di Un Messaggio Per Un Campo

	if ($messages->has('email'))
	{
		//
	}

#### Ritrovare Un Messaggio Di Errore Con Un Formato

	echo $messages->first('email', '<p>:message</p>');

> **Nota:** Di default, i messaggi sono formattati usando la sintassi Bootstrap.

#### Ritrovare Tutti I Messaggi Di Errore Con Un Formato

	foreach ($messages->all('<li>:message</li>') as $message)
	{
		//
	}

<a name="messaggi-di-errore-e-view"></a>
## Messaggi Di Errore E View

Una volta eseguita la validazione, avrai bisogno di un modo semplice per visualizzare i messaggi di errore nelle tue view. Questo comportamento è gestito da Laravel in modo adeguato. Prendi in considerazione le seguenti route come esempio:

	Route::get('register', function()
	{
		return View::make('user.register');
	});

	Route::post('register', function()
	{
		$rules = array(...);

		$validator = Validator::make(Input::all(), $rules);

		if ($validator->fails())
		{
			return redirect('register')->withErrors($validator);
		}
	});

Nota che quando la validazione fallisce, passiamo l'istanza `Validator` al Redirect usando il metodo `withErrors`. Questo metodo inserisce i messaggi di errore nella sessione in modo da renderli disponibili alla prossima richiesta.

Tuttavia, nota che non è necessario bindare esplicitamente i messaggi di errore con la view nella route GET. Questo perché Laravel effettua sempre un check degli errori in sessione e, qualora fossero disponibili, fa il bind automaticamente. **E’ importante notare quindi, che la variabile `$errors` è sempre disponibile in tutte le tue view, in ogni richiesta**, puoi considerarla quindi sempre definita e utilizzabile in modo sicuro. La variabile `$errors` sarà un’istanza di MessageBag.

Quindi, dopo il redirect, puoi effettuare il bind di `$errors` nella tua view come da esempio:

	<?php echo $errors->first('email'); ?>

### Error Bag Nominato

Se hai molti form in una singola pagina, potresti voler dare un nome agli errori `MessageBag`.
Questo ti permetterà di ritrovare i messaggi di errore per uno specifico form. Semplicemente passando un nome come secondo argomento del metodo `withErrors`:

	return redirect('register')->withErrors($validator, 'login');

Puoi anche accedere all'istanza nominata di `MessageBag` dalla variabile `$errors`:

	<?php echo $errors->login->first('email'); ?>

<a name="regole-validazione-disponibili"></a>
## Regole Di Validazione Disponibili

Di seguito la lista delle regole di validazione disponibili e la loro descrizione:

- [Accepted](#rule-accepted)
- [Active URL](#rule-active-url)
- [After (Date)](#rule-after)
- [Alpha](#rule-alpha)
- [Alpha Dash](#rule-alpha-dash)
- [Alpha Numeric](#rule-alpha-num)
- [Array](#rule-array)
- [Before (Date)](#rule-before)
- [Between](#rule-between)
- [Boolean](#rule-boolean)
- [Confirmed](#rule-confirmed)
- [Date](#rule-date)
- [Date Format](#rule-date-format)
- [Different](#rule-different)
- [Digits](#rule-digits)
- [Digits Between](#rule-digits-between)
- [E-Mail](#rule-email)
- [Exists (Database)](#rule-exists)
- [Image (File)](#rule-image)
- [In](#rule-in)
- [Integer](#rule-integer)
- [IP Address](#rule-ip)
- [Max](#rule-max)
- [MIME Types](#rule-mimes)
- [Min](#rule-min)
- [Not In](#rule-not-in)
- [Numeric](#rule-numeric)
- [Regular Expression](#rule-regex)
- [Required](#rule-required)
- [Required If](#rule-required-if)
- [Required With](#rule-required-with)
- [Required With All](#rule-required-with-all)
- [Required Without](#rule-required-without)
- [Required Without All](#rule-required-without-all)
- [Same](#rule-same)
- [Size](#rule-size)
- [String](#rule-string)
- [Timezone](#rule-timezone)
- [Unique (Database)](#rule-unique)
- [URL](#rule-url)

<a name="rule-accepted"></a>
#### accepted

Il campo da validare deve avere un valore pari a _yes_, _on_, or _1_. Questo è utile per esempio, per validare l'accettazione dei “Termini del Servizio”

<a name="rule-active-url"></a>
#### active_url

Il campo da validare deve essere un URL valido secondo la funzione PHP `checkdnsrr`.

<a name="rule-after"></a>
#### after:_date_

Il campo deve essere una data successiva a quella fornita. La data è processata con la funzione PHP strtotime.

<a name="rule-alpha"></a>
#### alpha

Il campo deve essere composto da caratteri alfabetici.

<a name="rule-alpha-dash"></a>
#### alpha_dash

Il campo deve essere composto da caratteri alfanumerici, da trattini e da underscore.

<a name="rule-alpha-num"></a>
#### alpha_num

Il campo deve essere composto solo da caratteri alfanumerici.

<a name="rule-array"></a>
#### array

Il campo sottoposto a validazione deve essere un array.

<a name="rule-before"></a>
#### before:_date_

Il campo deve essere una data precedente a quella fornita. La data è processata con la funzione PHP strtotime.

<a name="rule-between"></a>
#### between:_min_,_max_

Il campo deve avere un valore all’interno dell’intervallo definito da min e max. Stringhe, numeri e file verranno validati allo stesso modo in base alla regola di size.

<a name="rule-boolean"></a>
#### boolean

Il campo da validare deve essere compatibile al tipo booleano. Gli input validi sono `true`, `false`, `1`, `0`, `"1"` e `"0"`.

<a name="rule-confirmed"></a>
#### confirmed

Il campo in validazione deve avere un campo corrispondente nomecampoconfirmation per la comferma. Ad esempio, se il campo sotto convalida è password il suo campo di conferma deve essere passwordconfirmation.

<a name="rule-date"></a>
#### date

Il campo deve essere una data valida. Viene utilizzato lo stesso criterio della funzione PHP strtotime.

<a name="rule-date-format"></a>
#### date_format:_format_

Il campo deve combaciare con il formato specificato come definito nella funzione PHP dateparsefrom_format.

<a name="rule-different"></a>
#### different:_field_

Il valore dato deve essere diverso da quello del campo di validazione.

<a name="rule-digits"></a>
#### digits:_value_

Il campo sottoposto a validazione deve essere numerico e deve avere una specifica lunghezza (value).

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

Il campo sottoposto a validazione deve avere una lunghezza compresa tra min e max.

<a name="rule-email"></a>
#### email

Il campo sottoposto a validazione deve essere un e-mail valida.

<a name="rule-exists"></a>
#### exists:_table_,_column_

Il campo sottoposto a validazione deve esistere nella tabella del database specificata.

#### Uso Base Di Una Regola Esistente

	'state' => 'exists:states'

#### Specificare Un Nome Di Colonna Custom

	'state' => 'exists:states,abbreviation'

Puoi anche specificare più condizione che verranno aggiunte come clausula "where" alla query:

	'email' => 'exists:staff,email,account_id,1'

Passando `NULL` come clausula "where" aggiungerà un check per un valore NULL nel database:

	'email' => 'exists:staff,email,deleted_at,NULL'

<a name="rule-image"></a>
#### image

Il file in validazione deve essere un’immagine (jpeg, png, bmp, gif o svg)

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

Il campo in validazione deve essere incluso nella lista di valori specificata.

<a name="rule-integer"></a>
#### integer

Il campo da validare deve essere un intero.

<a name="rule-ip"></a>
#### ip

Il campo da validare deve essere un indirizzo IP nel formato corretto.

<a name="rule-max"></a>
#### max:_value_

Il campo da validare deve essere minore di un valore massimo specificato. Stringhe, numeri e file verranno validati allo stesso modo in base alla regola di [`size`](#rule-size).

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

Il file da validare deve avere un MIME type corrispondente alla lista delle estensioni listate.

#### Uso Base Della Regola MIME

	'photo' => 'mimes:jpeg,bmp,png'

<a name="rule-min"></a>
#### min:_value_

Il campo da validare deve essere maggiore di un valore minimo specificato. Stringhe, numeri e file verranno validati allo stesso modo in base alla regola di [`size`](#rule-size).

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

Il campo in validazione non deve essere incluso nella lista di valori specificata.

<a name="rule-numeric"></a>
#### numeric

Il campo deve essere numerico.

<a name="rule-regex"></a>
#### regex:_pattern_

Il campo deve fare match con l’espressione regolare data.

**Nota:** Quando usi il pattern `regex`, potrebbe essere necessario specificare le regole in un array invece di usare il carattere di pipe come delimitatore, specialmente se la regula expression contiene il carattere di pipe.

<a name="rule-required"></a>
#### required

Il campo da validare deve essere inserito obbligatoriamente.

<a name="rule-required-if"></a>
#### required_if:_field_,_value_,...

Il campo da validare è obbligatorio se il campo field è uguale a value.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

Il campo da validare deve essere presente solo se uno qualsiasi degli altri campi specificati è presente.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

Il campo da validare deve essere presente solo se tutti gli altri campi specificati sono presenti.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

Il campo da validare deve essere presente solo quando uno qualsiasi degli altri campi specificati non è presente.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

Il campo da validare deve essere presente soltanto quando tutti gli altri campi specificati non sono presenti.

<a name="rule-same"></a>
#### same:_field_

Il valore di field deve corrispondere con il campo in validazione.

<a name="rule-size"></a>
#### size:_value_

Il campo da validare deve avere una dimensione corrispondente al valore dato. Per i dati di stringa, il valore corrisponde al numero dei caratteri. Per i dati numerici, il valore corrisponde a un valore dato. Per i file, la dimensione corrisponde alla dimensione del file in kilobyte.

<a name="rule-string"></a>
#### string:_value_

Il campo da validare deve essere di tipo string.

<a name="rule-timezone"></a>
#### timezone

Il campo da validare deve essere un identificatore timezone valido secondo la funzione PHP `timezone_identifiers_list`.

<a name="rule-unique"></a>
#### unique:_table_,_column_,_except_,_idColumn_

Il campo da validare deve essere univoco su una determinata tabella di database. Se l’opzione colonna non è specificata, verrà utilizzato il nome del campo.

#### Uso Base Della Regola Unique

	'email' => 'unique:users'

#### Specificare Un Nome Colonna Custom

	'email' => 'unique:users,email_address'

#### Forzare La Regola Unique Ad Ignorare Una Data ID

	'email' => 'unique:users,email_address,10'

#### Aggiungere Clausule Where Addizionali

Puoi inoltre specificare ulteriori condizioni che saranno aggiunte come clausola “where” alla query:

	'email' => 'unique:users,email_address,NULL,id,account_id,1'

Nella regola di sopra solo le righe con account_id uguale a 1 dovrebbero essere incluse nel check unique.

<a name="rule-url"></a>
#### url

Il campo da validare deve essere correttamente formattato con un URL.

> **Nota:** Questa funzione utilizza il metodo PHP `filter_var`.

<a name="aggiungere-regole-condizionali"></a>
## Aggiungere Regole Condizionali

In alcune situazioni potresti voler validare un campo **solo** se questo è presente nell’array di input. Per farlo in modo facile, aggiungi la regola sometimes alla tua lista:

	$v = Validator::make($data, array(
		'email' => 'sometimes|required|email',
	));

Nell’esempio sopra, il campo `email` sarà validato solo se presente nell’array `$data`.

#### Validazioni Condizionali Complesse

A volte potresti voler richiedere un determinato campo solo se un altro campo ha un valore maggiore di 100. O potresti aver bisogno che due campi abbiano un dato valore solo se un altro campo è presente. L’aggiunta di questo tipo di regole di convalida non è una onerosa. Per prima cosa crea un’istanza `Validator` con le regole statiche che non cambieranno mai:

	$v = Validator::make($data, array(
		'email' => 'required|email',
		'games' => 'required|numeric',
	));

Supponiamo di avere un’ applicazione web per collezionisti di giochi. Se un utente si registra nella nostra applicazione e possiede più di 100 giochi, vogliamo che spieghi perché possiede tanti giochi. Ad esempio potrebbe essere perché ha un negozio re-sell di giochi, oppure perché semplicemente vuole collezionare giochi. Per aggiungere condizionalmente questo requisito, possiamo usare il metodo `sometimes` sull’istanza `Validator`.

	$v->sometimes('reason', 'required|max:500', function($input)
	{
		return $input->games >= 100;
	});

Il primo argomento passato al metodo `sometimes` è il nome del campo che vogliamo validare condizionalmente. Il secondo parametro è la regola che vogliamo aggiungere. Se la Closure passata come terzo argomento restituisce `true`, la regola verrà aggiunta. Questo metodo rende facile la costruzione di convalide condizionali complesse. Si possono anche aggiungere validazioni condizionali per più campi contemporaneamente:

	$v->sometimes(array('reason', 'cost'), 'required', function($input)
	{
		return $input->games >= 100;
	});

> **Nota:** Il parametro `$input` passato alla tua Closure sarà un’istanza di  `Illuminate\Support\Fluent` e può essere usata come oggetto per accedere ai tuoi input e file.

<a name="messaggi-errore-personalizzati"></a>
## Messaggi Di Errore Personalizzati

Se ne hai la necessità, puoi usare messaggi di errori personalizzati alternativamente a quelli di default. Ci sono diversi modi per specificare messaggi personalizzati.

#### Passare Messaggi Personalizzati Nel Validatore

	$messages = array(
		'required' => 'The :attribute field is required.',
	);

	$validator = Validator::make($input, $rules, $messages);

> *Nota:* Il place-holder `:attribute` verrà sostituito dal nome attuale del campo da validare. Puoi anche usare altri place-holder nei messaggi di validazione.

#### Altri Place-Holder

	$messages = array(
		'same'    => 'The :attribute and :other must match.',
		'size'    => 'The :attribute must be exactly :size.',
		'between' => 'The :attribute must be between :min - :max.',
		'in'      => 'The :attribute must be one of the following types: :values',
	);

#### Specificare Un Messaggio Personalizzato Per Un Dato Attributo

Certe vole portesti voler specificare un messaggio di errore personalizzato per uno specifico campo:

	$messages = array(
		'email.required' => 'We need to know your e-mail address!',
	);

<a name="localizzazione"></a>
#### Specificare Messaggi Personalizzati All'Interno Di Un File Lingua

In alcuni casi, puoi aver bisogno di specificare i tuoi messaggi personalizzati per un file lingua invece che passarli direttamente ad una istanza `Validator`. Per farlo, aggiungi i tuoi messaggi all'interno dell'array `custom` del file lingua `resources/lang/xx/validation.php`.

	'custom' => array(
		'email' => array(
			'required' => 'We need to know your e-mail address!',
		),
	),

<a name="regole-validazione-personalizzate"></a>
## Regole Di Validazione Personalizzate

#### Registrare Una Regola Di Validazione Personalizzata

Laravel ha le sue proprie regole di validazione ma nulla toglie che tu possa specificarne di personali. Un metodo per la registrazione di regole di convalida personalizzate è `Validator::extend`:

	Validator::extend('foo', function($attribute, $value, $parameters)
	{
		return $value == 'foo';
	});

La Closure per la customizzazione delle regole di validazione riceve tre parametri: il nome `$attribute` da validare, il valore `$value` e l’array `$parameters`.

Puoi anche passare una classe e un metodo invece di una closure. Usa il metodo `extend`.

	Validator::extend('foo', 'FooValidator@validate');

Per le tue regole puoi definire messaggi di errore personalizzati. Puoi farlo utilizzando un array di messaggi custom inline oppure aggiungendo una entry nel file di lingua.

#### Estendere La Classe Validator

Invece di utilizzare la Closure callback, potresti estendere direttamente la classe Validator. Per farlo basta scrivere una classe Validator che estende `Illuminate\Validation\Validator`. Puoi aggiungere dei metodi alla classe semplicemente aggiungendo il prefisso validate: 

	<?php

	class CustomValidator extends Illuminate\Validation\Validator {

		public function validateFoo($attribute, $value, $parameters)
		{
			return $value == 'foo';
		}

	}

#### Registrare Un Validator Resolver Personalizzato

Next, you need to register your custom Validator extension:

	Validator::resolver(function($translator, $data, $rules, $messages)
	{
		return new CustomValidator($translator, $data, $rules, $messages);
	});

Quando si crea una regola di validazione personalizzata, talvolta può essere necessario definire un place-holder personalizzato per i messaggi di errore. Puoi farlo creando un Validator come descritto sopra, aggiungendo una funzione `replaceXXX`.

	protected function replaceFoo($message, $attribute, $rule, $parameters)
	{
		return str_replace(':foo', $parameters[0], $message);
	}

Se vuoi aggiungere un messaggio custom “replacer” senza estendere la classe `Validator`, puoi usare il metodo `Validator::replacer`:

	Validator::replacer('rule', function($message, $attribute, $rule, $parameters)
	{
		//
	});
