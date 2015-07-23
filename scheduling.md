# Scheduling dei Task

- [Introduzione](#introduzione)
- [Definire i Task](#definire-task)
	- [Opzioni di Frequenza per lo Scheduler](#opzioni-frequenza-scheduler)
	- [Evitare l'Overlap dei Task](#evitare-overlap-task)
- [Output dei Task](#output-task)
- [Eventi dopo un Task](#eventi-dopo-task)

<a name="introduzione"></a>
## Introduzione

Nel passato, gli sviluppatori dovevano generare un cron job per ogni task da eseguire in modo programmato. Un bel giramento di testa, ogni volta! Considerando anche che i task in questione non venivano certo salvati nella codebase. Il command scheduler di Laravel ti permette di creare in modo espressivo e semplice una serie di comandi in base alle tue necessità, impostando solamente un singolo cronjob sul tuo server.

La programmazione dei vari task è definita in `app/Console/Kernel.php`, nel metodo `schedule`. Per aiutarti ad iniziare, è stato già inserito un semplice task di esempio.

### Avviare lo Scheduler

Come già detto, devi comunque creare un singolo job di partenza sul tuo server.

	* * * * * php /path/to/artisan schedule:run 1>> /dev/null 2>&1

Tale cron richiamerà il Laravel command scheduler ogni singolo minuto. A quel punto, il framework stesso valuterà i vari task da avviare e quali tralasciare.

<a name="definire-task"></a>
## Definire i Task

Puoi definire tutti i tuoi task programmati in _schedule_ della classe `App\Console\Kernel`. Iniziamo subito con un esempio, per capire meglio. Vedremo una chiamata ad una closure da eseguire ogni giorno a mezzanotte. Tale closure si occuperà di pulire il database con una query.

	<?php namespace App\Console;

	use DB;
	use Illuminate\Console\Scheduling\Schedule;
	use Illuminate\Foundation\Console\Kernel as ConsoleKernel;

	class Kernel extends ConsoleKernel
	{
	    /**
	     * The Artisan commands provided by your application.
	     *
	     * @var array
	     */
	    protected $commands = [
	        'App\Console\Commands\Inspire',
	    ];

	    /**
	     * Define the application's command schedule.
	     *
	     * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
	     * @return void
	     */
	    protected function schedule(Schedule $schedule)
	    {
	        $schedule->call(function () {
	        	DB::table('recent_users')->delete();
	        })->daily();
	    }
	}

In aggiunta alla chiamata, puoi anche schedulare specifici [comandi Artisan](/docs/5.1/artisan) tramite _command_.

    $schedule->command('emails:send --force')->daily();

Inoltre, tramite _exec_ puoi addirittura eseguire delle istruzioni sul server stesso.

    $schedule->exec('node /home/forge/script.js')->daily();

<a name="opzioni-frequenza-scheduler"></a>
### Opzioni di Frequenza per lo Scheduler

Per pesonalizzare il momento specifico in cui eseguire i tuoi task, lo scheduler ti mette a disposizione svariati metodi.


* `->cron('* * * * *');`  |  Avvia il task in base alla personalizzazione inserita;
* `->everyMinute();`  |  Avvia il task ogni minuto;
* `->everyFiveMinutes();`  |  Avvia il task ogni cinque minuti;
* `->everyTenMinutes();`  |  Avvia il task ogni dieci minuti;
* `->everyThirtyMinutes();`  |  Avvia il task ogni mezz'ora;
* `->hourly();`  |  Avvia il task una volta ogni ora;
* `->daily();`  |  Avvia il task ogni giorno, a mezzanotte;
* `->dailyAt('13:00');`  |  Avvia il task ogni giorno, alle 13:00
* `->twiceDaily();`  |  Avvia il task ogni giorno, alle 1:00 e alle 13:00
* `->weekly();`  |  Avvia il task una volta a settimana;
* `->monthly();`  |  Avvia il task una volta al mese;

Questi metodi possono inoltre essere combinati con altre condizioni, in modo tale da rendere massima la personalizzazione. Ad esempio, per avviare un certo comando ogni settimana, di lunedì, basterà usare...

	$schedule->call(function () {
		// Comando avviato una volta a settimana, di lunedì, alle 13:00...
	})->weekly()->mondays()->at('13:00');

Ecco una lista di condizioni disponibili:

* `->weekdays();`  |  Il task viene eseguito tutti i giorni;
* `->sundays();`  |  Il task viene eseguito solo di Domenica;
* `->mondays();`  |  Il task viene eseguito solo di Lunedì
* `->tuesdays();`  |  Il task viene eseguito solo di Martedì
* `->wednesdays();`  |  Il task viene eseguito solo di Mercoledì;
* `->thursdays();`  |  Il task viene eseguito solo di Giovedì;
* `->fridays();`  |  Il task viene eseguito solo di Venerdì;
* `->saturdays();`  |  Il task viene eseguito solo di Sabato;
* `->when(Closure);`  |  Il task viene limitato secondo una certa condizione;

#### Condizione di Test

Usando il metodo _when_ puoi limitare l'esecuzione di un task in base ad un test di verità su una certa condizione. Fin quando tale test tornerà true, il task verrà eseguito.

	$schedule->command('emails:send')->daily()->when(function () {
		return true;
	});

<a name="evitare-overlap-task"></a>
### Evitare l'Overlap dei Task

Di default, un task schedulato verrà esegutio anche nel caso in cui una precedente istanza dello stesso task sia ancora in esecuzione. Per prevenire una cosa del genere, usa il metodo _withoutOverlapping_.

	$schedule->command('emails:send')->withoutOverlapping();

Tale metodo è particolarmente utile quando i task da eseguire richiedono molto tempo.

<a name="output-task"></a>
## Output dei Task

Lo scheduler di Laravel fornisce svariati metodi di comodo per lavorare con l'output generato dai task programmati. Ad esempio, puoi usare il metodo _sendOutputTo_ per inviare l'output ottenuto ad un file.

	$schedule->command('emails:send')
			 ->daily()
			 ->sendOutputTo($filePath);

Usando invece _emailOutputTo_ puoi inviare una mail ad in indirizzo a tua scelta. In questo caso l'output però deve essere prima inviato ad un file, quindi via mail tramite una chiamata a catena. Come questa nell'esempio:

	$schedule->command('foo')
			 ->daily()
			 ->sendOutputTo($filePath)
			 ->emailOutputTo('foo@example.com');

> **Nota:** ricorda di configurare il servizio di invio di email adeguatamente.

<a name="eventi-dopo-task"></a>
## Eventi dopo un Task

Usando il metodo _then_ è possibile specificare del codice da eseguire dopo l'esecuzione di un task.

	$schedule->command('emails:send')
			 ->daily()
			 ->then(function () {
			 	// Task completato!
			 });

#### Ping

Usando il metodo _thenPing_, lo scheduler può effettuare un ping verso uno specifico URL dopo l'esecuzione di un task. Tale metodo può essere particolarmente utile per inviare una notifica ad un servizio esterno, come [Laravel Envoyer](https://envoyer.io), ad esempio.

	$schedule->command('emails:send')
			 ->daily()
			 ->thenPing($url);

Se decidi di usare _thenPing($url)_ ricorda che hai bisogno di installare il package Guzzle HTTP. Aggiungi la seguente dipendenza al file _composer.json_ del tuo progetto:

	"guzzlehttp/guzzle": "~5.3|~6.0"

... ed avvia il comando _composer update_ per installarlo!
