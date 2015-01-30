# Artisan CLI

- [Introduzione](#introduzione)
- [Utilizzo](#utilizzo)
- [Chiamata Comandi Esterni alla CLI](#chiamata-comandi-esterni-alla-cli)
- [Scheduling Comandi Artisan](#scheduling-comandi-artisan)

<a name="introduzione"></a>
## Introduzione

Artisan è il nome dell'interfaccia command-line di Laravel. Offre una serie di utili comandi da usare mentre si sviluppa la propria applicazione. Inoltre, è basato sul componente Console di Symfony.

<a name="utilizzo"></a>
## Utilizzo

#### Lista Di Tutti i Comandi Disponibili

Per visualizzare la lista di tutti i comandi Artisan disponibili, puoi usare il comando `list`:

	php artisan list

#### Visualizzare La Schermata Di Aiuto Per un Comando

Ogni comando include anche una schermata di "aiuto" che visualizza e descrive i parametri e le opzioni del comando. Per visualizzare la schermata di aiuto, basta precedere il nome del comando dal flag `help`:

	php artisan help migrate

#### Specificare La Configurazione D'Ambiente

E' possibile specificare la configurazione d'ambiente da usare durante l'esecuzione di un comando utilizzando il flag  `--env`:

	php artisan migrate --env=local

#### Displaying Your Current Laravel Version

E' inoltre possibile visualizzare la versione corrente di Laravel che si sta utilizzando con l'opzione `--version`:

	php artisan --version

<a name="chiamata-comandi-esterni-alla-cli"></a>
## Chiamata Comandi Esterni alla CLI

A volte potresti avere il bisogno di eseguire un comando Artisan al di fuori della CLI. Per esempio, eseguire un comando Artisan all'interno di una route. Basta utilizzare la facade `Artisan`:

	Route::get('/foo', function()
	{
		$exitCode = Artisan::call('command:name', ['--option' => 'foo']);

		//
	});

Puoi anche mettere in coda i tuoi comandi Artisan in modo da essere eseguiti in background dal proprio [queue workers](/docs/master/queues):

	Route::get('/foo', function()
	{
		Artisan::queue('command:name', ['--option' => 'foo']);

		//
	});

<a name="scheduling-comandi-artisan"></a>
## Scheduling Comandi Artisan

In passato, gli sviluppatori generavano una Cron entry per ogni comando che volevano schedulare. Tuttavia, ciò procurava un forte mal di testa. Your console schedule is no longer in source control, and you must SSH into your server to add the Cron entries. Rendiamoci la vita più facile. The Laravel command scheduler allows you to fluently and expressively define your command schedule within Laravel itself, and only a single Cron entry is needed on your server.

Your command schedule is stored in the `app/Console/Kernel.php` file. Within this class you will see a `schedule` method. To help you get started, a simple example is included with the method. You are free to add as many scheduled jobs as you wish to the `Schedule` object. The only Cron entry you need to add to your server is this:

	* * * * * php /path/to/artisan schedule:run 1>> /dev/null 2>&1

Questo Cron richiamerà il comando scheduler di Laravel ogni minuto. Then, Laravel evalutes your scheduled jobs and runs the jobs that are due. Non potrebbe essere più facile!

### Altri Esempi di Scheduling

Diamo un'occhiata ad alcuni esempi di scheduling:

#### Scheduling Closure

	$schedule->call(function()
	{
		// Do some task...

	})->hourly();

#### Scheduling Comandi da Terminale

	$schedule->exec('composer self-update')->daily();

#### Espressione Cron Manuale

	$schedule->command('foo')->cron('* * * * *');

#### Job Frequenti

	$schedule->command('foo')->everyFiveMinutes();

	$schedule->command('foo')->everyTenMinutes();

	$schedule->command('foo')->everyThirtyMinutes();

#### Job Giornalieri

	$schedule->command('foo')->daily();

#### Job Giornalieri Ad Uno Specifico Orario (formato 24 Ore)

	$schedule->command('foo')->dailyAt('15:00');

#### Job Due Volte al Giorno

	$schedule->command('foo')->twiceDaily();

#### Job Eseguiti Ogni Giorno Feriale

	$schedule->command('foo')->weekdays();

#### Job Settimanali

	$schedule->command('foo')->weekly();

	// Scheduling job settimanali per uno giorno (0-6) ed ora specifici...
	$schedule->command('foo')->weeklyOn(1, '8:00');

#### Job Mensili

	$schedule->command('foo')->monthly();

#### Limitare L'Environment nel quale i Job dovrebbero essere eseguiti

	$schedule->command('foo')->monthly()->environments('production');

#### Indicare Ai Job Di Non Essere Mai Eseguiti Quando L'Applicazione E' In Maintenance Mode

	$schedule->command('foo')->monthly()->evenInMaintenanceMode();

#### Permettere Ai Job Di Essere Eseguiti Soltanto Quando Una Funzione Callback E' True

	$schedule->command('foo')->monthly()->when(function()
	{
		return true;
	});
