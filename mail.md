# Mail

- [Introduzione](#introduzione)
- [Inviare una Mail](#inviare-mail)
	- [Allegati](#allegati)
	- [Allegati Inline](#allegati-inline)
	- [Mail e Code](#mail-code)
- [Mail e Sviluppo in Locale](#mail-sviluppo-locale)

<a name="introduzione"></a>
## Introduzione

Laravel offre una semplice e pulita API che fa da tramite con il popolarissimo package [SwiftMailer](http://swiftmailer.org). Non solo: di default, vengono offerti dei driver per SMTP, Mailgun, Mandrill ed Amazon SES, oltre ovviamente alla classica funzione _mail_ di PHP e _sendmail_. Scegliere il servizio giusto per la tua applicazione, insomma, non è mai stato così semplice.

### Prerequisiti dei Driver

I driver basati su API, come Mailgun e Mandrill, sono molto spesso più semplici dei classici server SMTP. Come prerequisito, tuttavia, c'è il package Guzzle HTTP che si occupa di effettuare le giuste chiamate. Installarlo è semplicissimo: non devi fare altro che aggiungere la seguente dipendenza al tuo file _composer.json_.

	"guzzlehttp/guzzle": "~5.3|~6.0"

#### Driver per Mailgun

Per usare il driver Mailgun, innanzitutto devi installare Guzzle. Dopodiché, imposta l'opzione _driver_ in `config/mail.php` come `mailgun`. Infine, verifica le credenziali inserite in `config/services.php`:

	'mailgun' => [
		'domain' => 'your-mailgun-domain',
		'secret' => 'your-mailgun-key',
	],

Niente di più! Pronto a lavorare!

#### Driver per Mandrill

Per usare il driver per Mandrill installa Guzzle. Dopodiché imposta l'opzione _driver_ in `config/mail.php` come `mandrill`. Infine verifica le credenziali nell'elemento _mandrill_ in `config/services.php`.

	'mandrill' => [
		'secret' => 'your-mandrill-key',
	],

#### Driver per SES

Per usare Amazon SES, installa l'Amazon SDK per PHP. Anche in questo caso basta una semplice inclusione del package nel file _composer.json_.

	"aws/aws-sdk-php": "~3.0"

Subito dopo l'installazione imposta il `driver` in `config/mail.php` come `ses` e controlla le credenziali relative in `config/services.php`.

	'ses' => [
		'key' => 'your-ses-key',
		'secret' => 'your-ses-secret',
		'region' => 'ses-region',  // e.g. us-east-1
	],

<a name="inviare-mail"></a>
## Inviare una Mail

Laravel ti permette di memorizzare un messaggio e-mail in una [view](/documentazione/5.1/view) per maggiore praticità. Anche per una migliore organizzazione, infatti, date le circostanze potresti crearti una cartella _emails_ in `resources/views`.

Per inviare un messaggio devi usare il metodo _send_ della [facade](/documentazione/5.1/facade) _Mail_. Tale metodo accetta tre parametri.

Il primo definisce il nome della view da usare. Il secondo, invece, un array di dati da passare a tale view. Il terzo, infine, una _Closure_ che riceve un'istanza del messaggio e permette di modificarne l'oggetto, i destinatari e così via.

	<?php namespace App\Http\Controllers;

	use Mail;
	use App\User;
	use Illuminate\Http\Request;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Send an e-mail reminder to the user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function sendEmailReminder(Request $request, $id)
		{
			$user = User::findOrFail($id);

			Mail::send('emails.reminder', ['user' => $user], function ($m) use ($user) {
				$m->to($user->email, $user->name)->subject('Your Reminder!');
			});
		}
	}

In questo esempio stiamo passando un array contenente l'elemento _user_. Il che vuol dire che possiamo mostrare i vari dettagli dell'utente usando un semplice:

	<?php echo $user->name; ?>

> **Nota:** la variabile _$message_ è sempre passata alla view, il che permette anche [l'inclusione di allegati inline](#allegati-inline). Evita quindi di passare l'oggetto _$message_ un'ulteriore volta.

#### Costruire il Messaggio

Come detto in precedenza, il terzo parametro del metodo _send_ è una callback che ti permette di specificare varie opzioni relative al messaggio stesso. Carbon copy, blind carbon copy, oggetto e così via.

	Mail::send('emails.welcome', $data, function ($message) {
		$message->from('us@example.com', 'Laravel');

		$message->to('foo@example.com')->cc('bar@example.com');
	});

Ecco una lista di tutti i metodi che puoi richiamare su _$message_.

	$message->from($address, $name = null);
	$message->sender($address, $name = null);
	$message->to($address, $name = null);
	$message->cc($address, $name = null);
	$message->bcc($address, $name = null);
	$message->replyTo($address, $name = null);
	$message->subject($subject);
	$message->priority($level);
	$message->attach($pathToFile, array $options = []);

	// Allegare un file "grezzo" partendo da una stringa $data...
	$message->attachData($data, $name, array $options = []);

	// Accedere all'istanza Swift sottostante...
	$message->getSwiftMessage();

> **Nota:** l'istanza _$message_ passata a _Mail::send_ estende la classe _SwiftMailer_, il che vuol dire che puoi comunque richiamare su di esso TUTTI i metodi già definiti per tale classe.

#### Messaggio di Testo Semplice

Di default, Laravel assume che la view passata al metodo _send_ sia in HTML. Tuttavia, passando un array come primo argomento del metodo _send_, puoi specificare anche una versione testuale semplificata del messaggio.

	Mail::send(['html.view', 'text.view'], $data, $callback);

Inoltre, se vuoi inviare un messaggio **solo** testuale, nell'array inseriscici un solo nome di view come elemento, che faccia capo alla chiave _text_.

	Mail::send(['text' => 'view'], $data, $callback);

#### Inviare Stringhe Grezze

Puoi, infine, inviare una stringa grezza usando il metodo _raw_ come segue. 

	Mail::raw('Testo da inviare!', function ($message) {
		//
	});

<a name="allegati"></a>
### Allegati

Per aggiungere un allegato ad un messaggio, usa il metodo _attach_ sull'oggetto _$message_ passato alla _Closure_. Tale metodo accetta una stringa che rappresenta il path completo del file.

	Mail::send('emails.welcome', $data, function ($message) {
		
		// ... altre operazioni ...

		$message->attach($pathToFile);
	});

Quando alleghi un file ad un messaggio puoi decidere il nome da mostrare ed il MIME type relativo, passando come secondo argomento un _array_ associativo come nell'esempio di seguito.

	$message->attach($pathToFile, ['as' => $display, 'mime' => $mime]);

<a name="allegati-inline"></a>
### Allegati Inline

#### Allegare un'Immagine nella View

Inserire nel messaggio un'immagine inline è una cosa piuttosto noiosa, molto spesso. Tuttavia, Laravel fornisce un modo molto semplice di risolvere il problema. Tutto quello che devi fare, infatti, è usare il metodo _embed_ dell'oggetto _Message_.

> Nota: ricordi cosa abbiamo detto poco fa? Laravel passa di default l'oggetto _$message_ alla view scelta per l'email.

	<body>
		Here is an image:

		<img src="<?php echo $message->embed($pathToFile); ?>">
	</body>

#### Inclusione di Dati Grezzi nel Messaggio

Se hai già una stringa "grezza" che vuoi includere nel tuo messaggio, usa _embedData_ come segue:

	<body>
		Here is an image from raw data:

		<img src="<?php echo $message->embedData($data, $name); ?>">
	</body>

<a name="mail-code"></a>
### Mail e Code

#### Mettere in Coda un Messaggio

Inviare messaggi di posta può rallentare, a volte anche di molto, la tua richiesta. Molti sviluppatori, per questo motivo, predispongono delle code per l'invio di messaggi in modo tale da svolgere tutto il più velocemente possibile. Laravel ha già un [API unificata per le Code](/documentazione/5.1/code) ed è disponibile, nella facade _Mail_, il metodo _queue_:

	Mail::queue('emails.welcome', $data, function ($message) {
		//
	});

Questo metodo si occuperà di tutto automaticamente, creando il relativo job per il messaggio. Per usare un simile servizio dovrai, ovviamente, [configurare tutto in modo adeguato](/documentazione/5.1/code) prima di poter usare una feature del genere.

#### Invio di Messaggi in Coda Dilazionati

Se vuoi dilazionare l'invio di un messaggio di posta, puoi usare il metodo _later_. Tutto quello che devi fare, in tal caso, è passare come primo parametro il numero di secondi per il delay. Per tutto il resto non devi fare altro, se non inserire nuovamente gli stessi parametri che già conosci.

	Mail::later(5, 'emails.welcome', $data, function ($message) {
		//
	});

#### Push Verso una Coda Specifica

Se vuoi inserire il job dell'invio di un messaggio in una coda specifica, usa _queueOn_ o _laterOn_.

	Mail::queueOn('queue-name', 'emails.welcome', $data, function ($message) {
		//
	});

	Mail::laterOn('queue-name', 5, 'emails.welcome', $data, function ($message) {
		//
	});

<a name="mail-sviluppo-locale"></a>
## Mail e Sviluppo in Locale

Durante la fase di sviluppo di un'applicazione che fa uso delle funzionalità viste in questa parte della guida, probabilmente vuoi fare anche in modo che non partano invii non desiderati. Laravel, fortunatamente, ha vari meccanismi che puoi usare per disattivare l'invio senza incappare in errori.

La prima soluzione è usare il driver _log_ per il sistema di mail. In questo modo, al posto di processare l'invio vero e proprio, tutti i dettagli relativi all'email verranno scritti sul file di log e nulla di più. A tal proposito dai uno sguardo al sistema di [configurazione per gli ambienti](/documentazione/5.1/installazione#configurazione-ambiente).

Un altro modo per risolvere il problema è usare servizi come [Mailtrap](https://mailtrap.io) insieme al driver `smtp`, mandando il messaggio ad una casella di posta dummy. Un simile approccio ha il beneficio di permetterti di vedere come effettivamente "arriva" il messaggio.
