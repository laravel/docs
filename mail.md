# Mail

- [Configurazione](#configurazione)
- [Uso Base](#uso-base)
- [Incorporare Gli Allegati](#incorporare-allegati)
- [Code Di Posta](#code-di-posta)
- [Mail & Ambiente Di Sviluppo](#mail-e-ambiente-sviluppo)

<a name="configurazione"></a>
## Configurazione

Laravel fornisce una chiara e semplice API della popolare libreria [SwiftMailer](http://swiftmailer.org). Il file di configurazione della mail è `config/mail.php`, al suo interno troverai una serie di opzioni che ti permetteranno di cambiare il tuo host SMTP, la porta, le credenziali, ma anche l’indirizzo del mittente per tutti i messaggi inviati con questa libreria. Puoi, inoltre, usare tutti gli host SMTP che preferisci. Se preferisci usare la funzione `mail` di PHP per inviare mail, puoi cambaire il `driver` da usare nel file di configurazione. E' disponibile anche il driver `sendmail`.

### Driver API

Laravel include i driver per le api Mailgun e Mandrill HTTP. Queste API sono spesso più semplici e veloci rispetto ad un server SMTP. Entrambi i driver richiedono la libreria Guzzle 4 HTTP, che dovrai installare nella tua applicazione. Per aggiungere Guzzle 4 al tuo progetto inserisci la seguente linea nel tuo file `composer.json`:

	"guzzlehttp/guzzle": "~4.0"

#### Mailgun Driver

Per usare il driver Mailgun, imposta l'opzione `driver` con `mailgun` nel tuo file di configurazione mail `config/mail.php`. Successivamente, crea un file di configurazione `config/services.php`, se non ne esiste già uno per il tuo progetto. Infine, verifica che contenga le seguenti opzioni:

	'mailgun' => array(
		'domain' => 'your-mailgun-domain',
		'secret' => 'your-mailgun-key',
	),

#### Mandrill Driver

Per usare il driver Mandrill, imposta l'opzione `driver` con `mandrill` nel tuo file di configurazione mail `config/mail.php`. Successivamente, crea un file di configurazione `config/services.php`, se non ne esiste già uno per il tuo progetto. Infine, verifica che contenga le seguenti opzioni:

	'mandrill' => array(
		'secret' => 'your-mandrill-key',
	),

### Log Driver

Se l'opzione `driver` del tuo file di configurazione mail `config/mail.php` è impostata su `log`, tutte le tue mail saranno scritte sul file di log, e non verranno inviate a nessun destinatario. Questo è estremamente utile, nella fase di debugging e verifica dei contenuti della tua applicazione.

<a name="uso-base"></a>
## Uso Base

Il metodo `Mail::send` può essere usato per inviare un messaggio email:

	Mail::send('emails.welcome', array('key' => 'value'), function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

Il primo parametro passato al metodo `send` è il nome della view che viene usata come corpo della mail. Il secondo parametro sono i dati passati alla view, spesso si tratta di un array associativo ai quali dati si accede tramite una chiave `$key`. Il terzo parametro è una Closure che ti permette di specificare una serie di opzioni per il messaggio della mail.

> **Nota:** Una variabile `$message` è sempre passata alla view, che ti permette di incorporare allegati. Per questo motivo, quindi, è consigliabile evitare di utilizzare una variabile `message` nella view che non sia quella passata attraverso la Closure.

Puoi specificare una view per il solo testo in aggiunta ad una view HTML:

	Mail::send(array('html.view', 'text.view'), $data, $callback);

Oppure, specificare solo un tipo di view usando le chiavi `html` o `text`:

	Mail::send(array('text' => 'view'), $data, $callback);

Puoi specificare altre opzioni per l'invio della mail come la copia carbone o gli allegati:

	Mail::send('emails.welcome', $data, function($message)
	{
		$message->from('us@example.com', 'Laravel');

		$message->to('foo@example.com')->cc('bar@example.com');

		$message->attach($pathToFile);
	});

Quando alleghi dei file alla mail, devi specificare il MIME type e/o visualizzare il nome indicativo del file:

	$message->attach($pathToFile, array('as' => $display, 'mime' => $mime));

Se hai solo bisogno di inviare una semplice stringa invece di un intera view, puoi usare il metodo `raw`:

	Mail::raw('Text to e-mail', function($message)
	{
		$message->from('us@example.com', 'Laravel');

		$message->to('foo@example.com')->cc('bar@example.com');
	});

> **Nota:** L'istanza message passata alla Closure di `Mail::send` estende la classe SwiftMailer message, che ti permette di usare qualsiasi altro metodo presente in quella classe per costruire i tuoi messaggi email.

<a name="incorporare-gli-allegati"></a>
## Incorporare Gli Allegati

La gestione delle immagini nelle email è una classica attività piuttosto ingombrante. Ad ogni modo, Laravel fornisce un semplice metodo per allegare immagini alle tue email e recuperare quindi il relativo CID.

#### Incorporare Una Immagine Nella View Per L’Email

	<body>
		Here is an image:

		<img src="<?php echo $message->embed($pathToFile); ?>">
	</body>

#### Incorporare Dati Grezzi Nella View Per L’Email

	<body>
		Here is an image from raw data:

		<img src="<?php echo $message->embedData($data, $name); ?>">
	</body>

Nota che la variabile `$message` è sempre passata alla view usando la facade `Mail`.

<a name="code-di-posta"></a>
## Code Di Posta

#### Mettere In Coda Un Messaggio

Nel momento in cui spedire email può drasticamente allungare i tempi di risposta della tua applicazione, molti sviluppatori scelgono di mettere in coda i messaggi attraverso un invio in background. Laravel rende questa operazione semplice attraverso un’[API apposita](/code). Per mettere in coda una mail, usa il metodo `queue` della facade `Mail`:

	Mail::queue('emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

Puoi specificare il numero di secondi per ritardare l'invio del messaggio usando il metodo `later`:

	Mail::later(5, 'emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

Se preferisci specificare una particolare coda sulla quale spingere il messaggio, puoi farlo usando i metodi `queueOn` e `laterOn`:

	Mail::queueOn('queue-name', 'emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

<a name="mail-e-ambiente-sviluppo"></a>
## Mail & Ambiente Di Sviluppo

Quando stai sviluppando un'applicazione che invia email, è consigliabile disattivare l’invio email nell’ambiente locale o di sviluppo. Per farlo, puoi usare il metodo `Mail::pretend` oppure impostare l'opzione `pretend` su `true` nel file di configurazione `config/mail.php`. Quando il mailer è in modalità `pretend`, i messaggi saranno scritti sul file di log della tua applicazione invece di essere spediti.

Se desideri testare l'invio delle email, è possibile usare anche un servizio come [MailTrap](https://mailtrap.io).
