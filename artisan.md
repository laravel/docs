# Artisan CLI

- [Introduzione](#introduzione)
- [Utilizzo](#utilizzo)
- [Chiamata Comandi Esterni alla CLI](#chiamata-comandi-esterni-alla-cli)
- [Scheduling dei Comandi Artisan](#scheduling-comandi-artisan)

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

#### Mostrare la Versione di Laravel

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

Puoi anche mettere in coda i tuoi comandi Artisan in modo da essere eseguiti in background dal proprio [queue workers](/code):

	Route::get('/foo', function()
	{
		Artisan::queue('command:name', ['--option' => 'foo']);

		//
	});

<a name="scheduling-comandi-artisan"></a>
## Scheduling dei Comandi Artisan

In passato, gli sviluppatori generavano una Cron entry per ogni comando che volevano pianificare. Tuttavia, ciò procurava un forte mal di testa. La tua schedule console non è più in controllo del codice, e bisogna essere connessi via SSH al server per aggiungere delle Cron entry. Rendiamoci la vita più facile. Il comando scheduler di Laravel ti permette facilmente di definire un comando schedule con Laravel stesso, ed è necessaria solo una singola Cron entry sul tuo server.

I tuoi comandi schedule sono salvati nel file `app/Console/Kernel.php`. All'interno di questa classe potrai notare un metodo `schedule`. Per aiutarti ad iniziare, assieme al metodo è incluso un semplice esempio. Sei libero di aggiungere quanti scheduled job desideri all'oggetto `Schedule`. La sola Cron entry necessaria da aggiungere al tuo server è questa:

	* * * * * php /path/to/artisan schedule:run 1>> /dev/null 2>&1

Questo Cron richiamerà il comando scheduler di Laravel ogni minuto. Quindi, Laravel valuterà i tuoi job pianificati ed eseguirà quelli opportuni. Non potrebbe essere più facile!

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
