# Envoy Task Runner

- [Introduzione](#introduzione)
	- [Installazione](#installazione)
- [Scrivere un Task](#scrivere-task)
	- [Variabili di un Task](#variabili-task)
	- [Server Multipli](#server-multipli)
	- [Task Macro](#task-macro)
- [Eseguire un Task](#eseguire-task)
- [Notifiche](#notifiche)
	- [HipChat](#notifiche-hipchat)
	- [Slack](#notifiche-slack)

<a name="introduzione"></a>
## Introduzione

[Laravel Envoy](https://github.com/laravel/envoy) fornisce una sintassi semplice, pulita e minimal per definire tutti quei task che esegui con una certa frequenza sul tuo server. La sintassi, nello specifico, è molto simile a quella che usi normalmente con Blade. Ci puoi fare un po' di tutto: dal deploy ai comandi Artisan, ed oltre. Allo stato attuale Envoy supporta solo Mac e Linux.

<a name="installazione"></a>
### Installazione

Innanzitutto, installa Envoy usando il comando _global_ di Composer:

	composer global require "laravel/envoy=~1.0"

Assicurati di aver messo il percorso `~/.composer/vendor/bin` nella variabile di sistema PATH in modo tale da poter eseguire sempre il comando _envoy_.

#### Aggiornare Envoy

Puoi usare Composer anche per aggiornare Envoy. Basta un update.

	composer global update

<a name="scrivere-task"></a>
## Scrivere un Task

Tutti i task Envoy devono essere definiti in un file _Envoy.blade.php_ nella root del tuo progetto. Ecco un esempio, per iniziare.

	@servers(['web' => '192.168.1.1'])

	@task('foo', ['on' => 'web'])
		ls -la
	@endtask

Come puoi vedere, un array _@servers_ viene definito all'inizio del file, permettendoti poi di riusare questi server per definire i vari task da eseguire nello specifico. All'interno delle varie dichiarazioni di _@task_, invece, devi piazzare il codice Bash vero e proprio.

#### Bootstrapping

A volte potresti voler eseguire del codice prima di eseguire i task Envoy. Puoi usare la direttiva _@setup_ a tale scopo.

	@setup
		$now = new DateTime();

		$environment = isset($env) ? $env : "testing";
	@endsetup

Puoi usare anche _@include_ per includere degli script esterni.

	@include('vendor/autoload.php');

#### Conferma di un Task

Se vuoi fare in modo che prima dell'esecuzione di un task ti venga chiesta la conferma, aggiungi l'elemento _confirm_ nella dichiarazione di un task.

	@task('deploy', ['on' => 'web', 'confirm' => true])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

<a name="variabili-task"></a>
### Variabili di un Task

Se necessario, puoi passare una o più variabili ad un file Envoy usando gli switch da linea di comando.

Ecco un esempio:

	envoy run deploy --branch=master

Puoi quindi "riprendere" queste opzioni passate sempre usando la stessa sintassi vista per Blade.

	@servers(['web' => '192.168.1.1'])

	@task('deploy', ['on' => 'web'])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

Comodo, vero?

<a name="server-multipli"></a>
### Server Multipli

Puoi eseguire facilmente un task su più server contemproraneamente. Innanzitutto, aggiungi tutti i server interessati all'interno della dichiarazione di _@servers_. Una volta definiti rimane solo da usare l'elemento _on_ nell'array di configurazione del singolo task.

	@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

	@task('deploy', ['on' => ['web-1', 'web-2']])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

Di default, il task verrà eseguito su ogni server in modo sequenziale. Il che vuol dire che una volta eseguito il task sul primo server si passerà al secondo, e così via.

#### Esecuzione Parallela

Vuoi eseguire un certo task in modo parallelo su tutti i server? Nessun problema. Aggiungi l'opzione _parallel_ nella dichiarazione.

	@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

	@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

<a name="task-macro"></a>
### Task Macro

Le macro ti permettono di definire un set di task da eseguire in sequenza usando un singolo comando. Ad esempio, la macro _deploy_ potrebbe occuparsi di avviare insieme _git_ e _composer_.

	@servers(['web' => '192.168.1.1'])

	@macro('deploy')
		git
		composer
	@endmacro

	@task('git')
		git pull origin master
	@endtask

	@task('composer')
		composer install
	@endtask

Una volta definita la macro potresti avviare tutta la procedura, semplicemente, con

	envoy run deploy

<a name="eseguire-task"></a>
## Eseguire un Task

Per eseguire un task dal tuo file _Envoy.blade.php_ esegui il comando _run_ passando come argomento il nome del task o della macro creata che vuoi eseguire. Envoy penserà al resto:

	envoy run task

<a name="notifiche"></a>
## Notifiche

<a name="notifiche-hipchat"></a>
### HipChat

Dopo aver avviato un task, potrebbe essere comodo inviare una notifica al tuo team tramite HipChat! Nessun problema: esiste la direttiva apposita _@hipchat_. Tutto quello che devi fare è specificare l'API token, la room ed il messaggio da inviare. 

	@servers(['web' => '192.168.1.1'])

	@task('foo', ['on' => 'web'])
		ls -la
	@endtask

	@after
		@hipchat('token', 'room', 'Envoy')
	@endafter

Se lo preferisci, puoi anche specificare un messaggio personalizzato da inviare alla room HipChat. Tutte le variabili disponibili in Envoy, inoltre, diventano disponibili anche nella creazione del messaggio. Guarda qui:

	@after
		@hipchat('token', 'room', 'Envoy', "{$task} ran in the {$env} environment.")
	@endafter

<a name="notifiche-slack"></a>
### Slack

In aggiunta ad HipChat, puoi usare anche [Slack](https://slack.com). In tal caso la direttiva da usare (si, è proprio quella che immagini) è `@slack`.

Tale direttiva accetta uno Slack Hook URL, il nome del canale ed il messaggio che vuoi inviare al canale specificato.

	@after
		@slack('hook', 'channel', 'message')
	@endafter

Puoi anche recuperare l'URL del webhook creando un'integrazione _Incoming WebHooks_ su Slack. L'argomento _hook_ dovrebbe essere il webhook per intero fornito dall'integrazione. Ad esempio:

	https://hooks.slack.com/services/ZZZZZZZZZ/YYYYYYYYY/XXXXXXXXXXXXXXX

Puoi inoltre fornire, come parametro per il canale, una delle seguenti alternative:

- per inviare una notifica ad un canale: `#channel`
- per inviare una notifica ad un utente: `@user`
