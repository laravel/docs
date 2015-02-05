# SSH

- [Configurazione](#configurazione)
- [Utilizzo Base](#utilizzo-base)
- [Task](#task)
- [Download SFTP](#download-sftp)
- [Upload SFTP](#upload-sftp)
- [Mostrare le ultime righe di log remoti](#mostrare-le-ultime-righe-di-log-remoti)
- [Envoy Task Runner](#envoy-task-runner)

<a name="configurazione"></a>
## Configurazione

Laravel include un semplice modo per eseguire comandi SSH su server remoti, permettendoti così di creare facilmente task Artisan che lavorano sul server. La facade `SSH` ti fornisce un punto di accesso per collegarti a server remoti ed eseguire dei comandi.

Il file di configurazione è salvato in `config/remote.php`, e contiene tutte le opzioni che ti servono per configurare connessioni remote. L'array `connections` contiene una lista dei tuoi server ordinati in base al nome. Non devi far altro che inserire le credenziali nell'array `connections` e sarai pronto per eseguire task su server remoti. Nota che `SSH` può eseguire l'autenticazione sia utilizzando la password che una chiave SSH.

> **Nota:** Hai bisogno di un metodo semplice per eseguire diversi task sul tuo server remoto? Dai una occhiata a [Envoy task runner](#envoy-task-runner)!

<a name="utilizzo-base"></a>
## Utilizzo Base

#### Eseguire Comandi Sul Server Di Default

Per eseguire comandi sul tuo server `default`, puoi usare il metodo `SSH::run`:

	SSH::run(array(
		'cd /var/www',
		'git pull origin master',
	));

#### Eseguire Comandi Su Una Specifica Connessione

In alternativa, puoi eseguire comandi su una connessione specifica utilizzando il metodo `into`:

	SSH::into('staging')->run(array(
		'cd /var/www',
		'git pull origin master',
	));

#### Intercettare L'Output Dei Comandi

Puoi intercettare le risposte dei comandi eseguite semplicemente passando una Closure all'interno del metodo `run`:

	SSH::run($commands, function($line)
	{
		echo $line.PHP_EOL;
	});

## Task
<a name="task"></a>

Se hai un gruppo di comandi che devono essere eseguiti sempre assieme, puoi utilizzare il metodo `define` per raggrupparli in un unico `task`:

	SSH::into('staging')->define('deploy', array(
		'cd /var/www',
		'git pull origin master',
		'php artisan migrate',
	));

Una volta che il task è stato definito puoi utilizzare il metodo `task` per eseguirlo:

	SSH::into('staging')->task('deploy', function($line)
	{
		echo $line.PHP_EOL;
	});

<a name="download-sftp"></a>
## Download SFTP

La classe `SSH` include un modo facile per eseguire il download dei file utilizzando i metodi `get` e `getString`:

	SSH::into('staging')->get($remotePath, $localPath);

	$contents = SSH::into('staging')->getString($remotePath);

<a name="upload-sftp"></a>
## Upload SFTP

La classe `SSH` include anche un modo facile per eseguire l'upload di file, oppure di stringhe, utilizzando i metodi `put` e `putString`:

	SSH::into('staging')->put($localFile, $remotePath);

	SSH::into('staging')->putString($remotePath, 'Foo');

<a name="mostrare-le-ultime-righe-di-log-remoti"></a>
## Mostrare le ultime righe di log remoti

Laravel include un utile comando che ti permette di vedere le ultime righe del file `laravel.log` di ogni tua connessione remota. Utilizza semplicemente il comando Artisan `tail` e specifica il nome della connessione remota per la quale vuoi visualizzare le ultime righe dei log:

	php artisan tail staging

	php artisan tail staging --path=/path/to/log.file

<a name="envoy-task-runner"></a>
## Envoy Task Runner

- [Installazione](#envoy-installation)
- [Eseguire Task](#envoy-running-tasks)
- [Server Multipli](#envoy-multiple-servers)
- [Esecuzione Parallela](#envoy-parallel-execution)
- [Task Macro](#envoy-task-macros)
- [Notifiche](#envoy-notifications)
- [Aggiornamento Envoy](#envoy-updating-envoy)

Laravel Envoy fornisce una sintassi minima e pulita che ti permette di definire task da eseguire sui tuoi server remoti. Utilizza una sintassi simile a quella di [Blade](/docs/templates#blade-templating), e puoi facilmente impostare task per il deployment, comandi di Artisan, e molto altro.

> **Nota:** Envoy richiede una versione di PHP maggiore o uguale alla 5.4, e può essere eseguita solo su sistemi operativi Mac / Linux.

<a name="envoy-installation"></a>
### Installazione

Per prima cosa devi installare Envoy utilizzando Composer e il comando `global`:

	composer global require "laravel/envoy=~1.0"

Assicurati di inserire la cartella `~/.composer/vendor/bin` all'interno del tuo PATH in modo che l'eseguibile `envoy` venga riconosciuto quando esegui il comando `envoy` all'interno del tuo terminale.

Fatto questo crea il file `Envoy.blade.php` nella root del tuo progetto. Ecco un esempio che ti aiuterà a iniziare:

	@servers(['web' => '192.168.1.1'])

	@task('foo', ['on' => 'web'])
		ls -la
	@endtask

Come puoi vedere all'inizio del file è stato definito un array di `@servers`. In questo modo puoi riferirti a questi server utilizzando l'opzione `on` quando dichiari un task. All'interno della dichiarazione `@task` devi inserire il codice Bash che deve essere eseguito quando il task viene lanciato.

Puoi usare il comando `init` per creare un file di esempio per Envoy:

	envoy init user@192.168.1.1

<a name="envoy-running-tasks"></a>
### Eseguire Task

Per avviare dei Task, utilizza il comando `run` della tua installazione di Envoy:

	envoy run foo

Se necessario puoi passare delle variabili all'interno del file Envoy usando:

	envoy run deploy --branch=master

Puoi usare le opzioni sfruttando la sintassi di Balde:

	@servers(['web' => '192.168.1.1'])

	@task('deploy', ['on' => 'web'])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

#### Avvio

Puoi utilizzare la direttiva ```@setup``` per dichiarare variabili ed eseguire codice PHP all'interno del file Envoy:

	@setup
		$now = new DateTime();

		$environment = isset($env) ? $env : "testing";
	@endsetup

Puoi anche utilizzare ```@include``` per includere file PHP:

	@include('vendor/autoload.php');

<a name="envoy-multiple-servers"></a>
### Server Multipli

Puoi eseguire facilmente task su più server. Non devi far altro che inserire il server nella lista in cima al file e richiamarlo nel task:

	@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

	@task('deploy', ['on' => ['web-1', 'web-2']])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

Il task verrà eseguito in modo seriale su ogni server messo nella lista. Questo vuol dire che il task verrà eseguito sul server successivo solo quando finirà la sua esecuzione sul precedente.

<a name="envoy-parallel-execution"></a>
### Esecuzione Parallela

Se vuoi eseguire un task su più server in modo parallelo devi semplicemente aggiungere l'opzione `parallel` nella dichiarazione del task:

	@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

	@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

<a name="envoy-task-macros"></a>
### Task Macro

Le Macro ti permettono di definire una serie di task che devono essere eseguiti in sequenza utilizzando un solo comando. Per esempio:

	@servers(['web' => '192.168.1.1'])

	@macro('deploy')
		foo
		bar
	@endmacro

	@task('foo')
		echo "HELLO"
	@endtask

	@task('bar')
		echo "WORLD"
	@endtask

La Macro `deploy` può ora essere eseguita con un solo comando:

	envoy run deploy

<a name="envoy-notifications"></a>
<a name="envoy-hipchat-notifications"></a>
### Notifiche

#### HipChat

Dopo l'esecuzione di un task, puoi inviare una notifica nella chatroom HipChat del tuo team semplicemente aggiungendo la direttiva `@hipchat`:

	@servers(['web' => '192.168.1.1'])

	@task('foo', ['on' => 'web'])
		ls -la
	@endtask

	@after
		@hipchat('token', 'room', 'Envoy')
	@endafter

Puoi anche specificare un messaggio per la hipchat room. Ogni variabile dichiarata in ```@setup``` o inclusa con ```@include``` sarà disponibile per essere usata nel messaggio:

	@after
		@hipchat('token', 'room', 'Envoy', "$task ran on [$environment]")
	@endafter

Questo è un modo fantastico e molto semplice per tenere informati i tuoi colleghi sui task che sono eseguiti sul server.

#### Slack

La seguente sintassi può essere utilizzata per inviare notifiche utilizzando [Slack](https://slack.com):

	@after
		@slack('team', 'token', 'channel')
	@endafter

<a name="envoy-updating-envoy"></a>
### Aggiornare Envoy

Per aggiornare Envoy puoi usare semplicemente il comando `self-update`:

	envoy self-update

Se la tua installazione di Envoy si trova in `/usr/local/bin`, allora potrebbe essere necessario usare `sudo`:

	composer global update
