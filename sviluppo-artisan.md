# Svilluppo Artisan

- [Introduzione](#introduzione)
- [Costruire Un Comando](#costruire-un-comando)
- [Registrazione Comandi](#registrazione-comandi)

<a name="introduzione"></a>
## Introduzione

In aggiunta ai comandi offerti da Artisan, puoi anche cotruire i tuoi comandi personalizzati da usare con la tua applicazione. Puoi salvare i tuoi comandi personalizzati nella directory `app/Console/Commands`; ma sei libero di scegliere la tua directory in cui salvarli, impostando il tuo file `composer.json` in modo tale da includerli nel caricamento.

<a name="costruire-un-comando"></a>
## Costruire Un Comando

### Generare La Classe

Per creare un nuovo comando, puoi usare il comando Artisan `make:console`, che genererà i file necessari per aiutarti ad iniziare:

#### Generare Una Nuova Classe Command

	php artisan make:console FooCommand

Il comando sopra genera una classe in `app/Console/FooCommand.php`.

Quando crei il comando, l'opzione `--command` può essere usato per assegnare il nome del comando da usare nel terminale:

	php artisan make:console AssignUsers --command=users:assign

### Scrivere Il Comando

Una volta che il tuo comando è stato generato, dovresti impostare le proprietà `name` e `description` della classe, che saranno usate nella visualizzazione dei tuoi comandi sulla lista che comparirà sul tuo schermo.

Il metodo `fire` sarà chiamato quando il tuo comando verrà eseguito. Puoi anche metterci la logica del comando in questo metodo.

### Parametri & Opzioni

I metodi `getArguments` e `getOptions` vengono usati nel momento in cui definisci dei parametri o delle opzioni che il comando riceve. Entrambi questi metodi ritornano un array di comandi, rappresentati da una lista di array di opzioni.

Quando si definiscono i `parametri`, l'array delle definizioni dei valori viene rappresentato come segue:

	array($name, $mode, $description, $defaultValue)

Il parametro `mode` può  assumere i seguenti valori: `InputArgument::REQUIRED` o `InputArgument::OPTIONAL`.

Quando si definisco le `options`, l'array delle definizioni dei valori viene rappresentato come segue:

	array($name, $shortcut, $mode, $description, $defaultValue)

Per le opzioni, il parametro `mode` può assumere i seguenti valori: `InputOption::VALUE_REQUIRED`, `InputOption::VALUE_OPTIONAL`, `InputOption::VALUE_IS_ARRAY`, `InputOption::VALUE_NONE`.

La modalità `VALUE_IS_ARRAY` indica che l'uso di quel flag può essere ripetuto più volte quando viene chiamato un comando:

	php artisan foo --option=bar --option=baz

L'opzione `VALUE_NONE` indica che quel flag è usato come un semplice "switch":

	php artisan foo --option

### Recuperare L'Input

Mentre si sta eseguendo il comando, sarà ovviamente necessario accedere ai valori dei parametri o delle opzioni accettati dalla tua applicazione. Per farlo, puoi usare i metodi `argument` e `option`:

#### Recuperare Il Valore Di Un Parametro Di Un Comando

	$value = $this->argument('name');

#### Recupero Di Tutti I Parametri

	$arguments = $this->argument();

#### Recupero Del Valore Di Un'Opzione Del Comando

	$value = $this->option('name');

#### Recupero Di Tutte Le Opzioni

	$options = $this->option();

### Scrittura Dell'Output

Per inviare dell'output alla console, puoi usare i metodi `info`, `comment`, `question` e `error`. Ognuno di questi metodi userà in maniera appropriata il codice ANSI del colore per il loro scopo.

#### Inviare Informazioni Alla Console

	$this->info('Display this on the screen');

#### Inviare Un Messaggio Di Errore Alla Console

	$this->error('Something went wrong!');

### Chiedere Domande

Puoi anche usare i metodi `ask` e `confirm` per far confermare all'utente le operazioni:

#### Richiedere Input All'Utente

	$name = $this->ask('What is your name?');

#### Richiedere All'Utente Input Segreto

	$password = $this->secret('What is the password?');

#### Riehicedere All'Utente Una Conferma

	if ($this->confirm('Do you wish to continue? [yes|no]'))
	{
		//
	}

Puoi anche specificare un valore di default al metodo `confirm`, che può essere `true` o `false`:

	$this->confirm($question, true);

### Chiamata Di Altri Comandi

In alcuni casi, potresti voler eseguire la chiamata di altri comandi dal tuo comando. Per farlo usa il metodo `call`:

	$this->call('command:name', ['argument' => 'foo', '--option' => 'bar']);

<a name="registrazione-comandi"></a>
## Registrazione Comandi

#### Registrare Un Comando Artisan

Una volta completato il tuo comando, hai bisogno di registrarlo con Artisan, in modo da renderlo disponibile all'uso. Solitamente questo viene fatto nel file `app/Console/Kernel.php`. All'interno di questo file, potrai trovare una lista di comandi nella proprietà `commands`. Per registrare il tuo comando, aggiungilo semplicemente a questa lista. Quando Artisan si avvia, tutti i comandi inseriti in questa proprietà saranno risolti dall'[IoC container](/container) e registrati con Artisan.
