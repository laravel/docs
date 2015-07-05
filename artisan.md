# Console Artisan

- [Introduzione](#introduzione)
- [Scrivere Comandi](#scrivere-comandi)
    - [Struttura Comandi](#struttura-comandi)
- [Comandi I/O](#comandi-io)
    - [Definire Gli Input](#definire-input)
    - [Recuperare L'Input](#recuperare-input)
    - [Richiesta  Di Input](#richiesta-input)
    - [Scrittura Dell'Output](#scrittura-output)
- [Registrare Comandi](#registrare-comandi)
- [Chiamata Comandi Tramite Codice](#chiamata-comandi-tramite-codice)

<a name="introduzione"></a>
## Introduzione

Artisan è il nome dell'interfaccia command-line di Laravel. Offre un numero di utili comandi da usare mentre si sviluppa la propria applicazione. E' basato sul componente Symfony Console.Per visualizzare la lista di tutti i comandi Artisan disponibili, puoi usare il comand  `list`:

    php artisan list

Ogni comando include anche una schermata di “aiuto” che visualizza e descrive i parametri e le opzioni disponibili per il comando. Per visualizzare la schermata di aiuto, basta precedere il nome del comando dal flag `help`:

    php artisan help migrate

<a name="scrivere-comandi"></a>
## Scrivere Comandi

In aggiunta ai comandi offerti da Artisan, puoi anche cotruire i tuoi comandi personalizzati da usare con la tua applicazione. Puoi salvare i tuoi comandi nella directory `app/Console/Commands`; comunque, libero di scegliere la tua directory in cui salvarli, impostando il tuo file `composer.json` in modo tale da includerli nel caricamento.

Per creare un nuovo comando, puoi usare il comando Artisan `make:console`, che genererà i file necessari per aiutarti ad iniziare:

    php artisan make:console SendEmails

Il comando sopra dovrà generare una classe in `app/Console/Commands/SendEmails.php`. Quando crei un comando, l'opzione `--command` può essere usata per assegnare il nome del comando da usare nel terminale:

    php artisan make:console SendEmails --command=emails:send

<a name="struttura-comandi"></a>
### Struttura Comandi

Una volta che il tuo comando è stato generato, dovresti impostare le proprietà `signature` e `description` della classe, che saranno usate nella visualizzazione dei tuoi comandi sulla lista che comparirà sul tuo schermo.

Il metodo `handle` sarà chiamato quando il tuo comando sarà eseguito. Puoi inserire qualsiasi logica del comando in questo metodo. Diamo un occhiata ad un esempio di comando.

Nota che puoi iniettare qualsiasi dipendenza di cui hai bisogno nel costruttore del comando. Il [service container](/docs/{{version}}/container) di Laravel inietterà automaticamente tutte le dipendenze inserite nel costruttore. Per una maggiore ri-usabilità del codice, è una buona pratica mantenere i tuoi comandi “puliti” e fare in modo di rimandare ai servizi dell'applicazione il compito di completare i loro compiti.

    <?php namespace App\Console\Commands;

    use App\User;
    use App\DripEmailer;
    use Illuminate\Console\Command;
    use Illuminate\Foundation\Inspiring;

    class Inspire extends Command
    {
        /**
         * The name and signature of the console command.
         *
         * @var string
         */
        protected $signature = 'email:send {user}';

        /**
         * The console command description.
         *
         * @var string
         */
        protected $description = 'Send drip e-mails to a user';

        /**
         * The drip e-mail service.
         *
         * @var DripEmailer
         */
        protected $drip;

        /**
         * Create a new command instance.
         *
         * @param  DripEmailer  $drip
         * @return void
         */
        public function __construct(DripEmailer $drip)
        {
            parent::__construct();

            $this->drip = $drip;
        }

        /**
         * Execute the console command.
         *
         * @return mixed
         */
        public function handle()
        {
            $this->drip->send(User::find($this->argument('user')));
        }
    }

<a name="comandi-io"></a>
## Comandi I/O

<a name="definire-input"></a>
### Definire Gli Input

Quando scrivi un comando per la console, è prassi comune raccogliere gli input dell'utente tramite parametri o opzioni. Laravel permette facilmente di definire gli input che ci si aspetta dall'utente usando la proprietà `signature` nel tuo comando. La proprietà `signature` ti permette di definire il nome, parametri, e opzioni per il comando in una singola, espressiva, sintassi simile alla sintassi delle route.

Tutti i parametri e le opzioni fornite dall'utente sono racchiuse tra parentesi graffe, ad esempio

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'email:send {user}';

In questo esempio, il comando definisce un parametro **obbligatorio**: `user`. Puoi anche impostare dei parametri opzionali e definire dei valori di default per i parametri opzionali:

    // Optional argument...
    email:send {user?}

    // Optional argument with default value...
    email:send {user=foo}

Anche le opzioni, come i parametri, provengono dall'input dell'utente. Tuttavia, sono preceduti da un (`--`) quando vengono specificati da line di comando. Puoi definire le opzioni nella signature in questo modo:

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'email:send {user} {--queue}';

In questo esempio, lo switch `--queue` può essere specificato quando si richiama un comando Artisan. Se viene passato lo switch`--queue`, il valore dell'opzione sarà `true`. Altrimenti, il valore sarà `false`:

    php artisan email:send 1 --queue

Puoi anche specificare che all'opzione possa essere assegnato un valore dall'utente usando il simbolo `=` dopo il nome dell'opzione, indicando che il valore dovrebbe essere specificato:

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'email:send {user} {--queue=}';

In questo esempio, l'utente può passare un avlore per l'opzione, come in questo esempio:

    php artisan email:send 1 --queue=default

Puoi anche assegnare un valore di default alle opzioni:

    email:send {user} {--queue=default}

#### Descrizione Degli Input

Puoi anche assegnare una descrizione ai parametri e alle opzioni separandoli con il simobo ':' seguito dalla descrzione:

    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'email:send
                            {user : The ID of the user}
                            {--queue= : Whether the job should be queued}';

<a name="recuperare-input"></a>
### Recuperare L'Input

Mentre si sta eseguendo un comando, 
While your command is executing, avrai ovviamente bisogno di accedere ai valori per i parametri e le opzioni accettate dal comando. Per falro, puoi usare i metodi `argument` e `option`:

Per recuperare il valore di un parametro, usa il metodo `argument`:

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $userId = $this->argument('user');

        //
    }

Se hai bisogno di recuperare tutti i parametri come un `array`, richiama il metodo `argument` senza nessun parametro:

    $arguments = $this->argument();

Le opzioni possono essere recuperare facilmente come i parametri usando il metodo `option`. Come il metodo `argument`, puoi richiamare `option` senza nessun parametro in modo da ritrovare tutte le opzioni come un `array`:

    // Retrieve a specific option...
    $queueName = $this->option('queue');

    // Retrieve all options...
    $options = $this->option();

<a name="richiesta-input"></a>
### Richiesta  Di Input

In aggiunta alla visualizzazione dell'output, puoi anche richiedere all'utente di inserire degli input durante l'esecuzione di un comando. Il metodo `ask` chiederà all'utente con una data domanda, accetterà i suoi input, ed infine l'utente verrà riportato indietro al comando:

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $name = $this->ask('What is your name?');
    }

Il metodo `secret` è simile ad `ask`, ma gli input dell'utente non saranno visibili mentre si inseriscono da console. Questo metodo è utile quando si richiedono informazioni sensibili come ad esempio una password:

    $password = $this->secret('What is the password?');

#### Chiedere Conferme

Se hai bisogno di chiedere all'utente una semplice conferma, puoi usare il metodo `confirm`. Di default, questo metodo ritornerà `false`. Tuttavia, se l'utente inserisce `y` in risposta alla richiesta, il metodo ritornerà `true`.

    if ($this->confirm('Do you wish to continue? [y|N]')) {
        //
    }

#### Date Una Scelta All'Utente

Il metodo `anticipate` può essere usato per fornire un autocompletamento per una possibile scelta. L'utente può ancora scegliere qualsiasi rispostaThe user can still choose any answer, indipendentemente dalle scelte offerte.

    $name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);

Se hai bisogno di dare all'utente un insieme predefinito di scelte, puoi usare il metodo `choice`. L'utente sceglie l'indice della risposta, mati sarà restituito il valore della risposta. Puoi anche impostare un valore di default da ritornare se non è stato scelto nulla:

    $name = $this->choice('What is your name?', ['Taylor', 'Dayle'], false);

<a name="Scrittura-output"></a>
### Scrittura Dell'Output

Per inviare dell'output alla console, usa i metodi `info`, `comment`, `question` ed `error`. Ognuno di questi metodi userà l'appropriato colore nello standard ANSI a seconda del loro scopo.

Per visualizzare un messaggio di informazione all'utente, usa il metodo `info`. Solitamente, verrà visualizzato in console come un testo verde:

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $this->info('Display this on the screen');
    }

Per visualizzare un messaggio di errore, usa il metodo `error`. Un messaggio di errore è solitamente visualizzato in rosso:

    $this->error('Something went wrong!');

#### Table Layout

Il metodo `table` ti permette di formattare correttamente i dati nella forma riga / colonna. Basta passare al metodo le intestazioni e le righe. La larghezza e l'altezza saranno calcolate dinamicamente in base ai dati inseriti:

    $headers = ['Name', 'Email'];

    $users = App\User::all(['name', 'email'])->toArray();

    $this->table($headers, $users);

#### Barre Di Avanzamento

Per operazioni lunghe, potrebbe essere utile mostrare un indicatore dei progessi. Usando l'oggetto output, puoi inizizare, avanzare e fermare la barra di avanzamento. Devi definire un numero di step quando si inizia l'avanzamento, e quindi fai avanzare la barra dopo ogni step:

    $users = App\User::all();

    $this->output->progressStart(count($users));

    foreach ($users as $user) {
        $this->performTask($user);

        $this->output->progressAdvance();
    }

    $this->output->progressFinish();

Per maggiori informazioni, controlla la [documentazione Symfony Progress Bar](http://symfony.com/doc/2.7/components/console/helpers/progressbar.html).

<a name="registrare-comandi"></a>
## Registrare Comandi

Una volta completato il comando, hai bisogno di registrarlo con Artisan e quindi renderlo diposnibile all'utilizzo. Questo viene fatto all'interno del file `app/Console/Kernel.php`.

All'interno di questo file, troverai una lista di comandi nella proprietà `commands`. Per registrare un comando, semplicemente aggiungi il nome della classe alla lista. Quando Artisan si avvia, tutti i comandi nella lista in questa proprietà verrano risolti dal [service container](/docs/{{version}}/container) e registrati con Artisan:

    protected $commands = [
        'App\Console\Commands\SendEmails'
    ];

<a name="chiamata-comandi-tramide-codice"></a>
## Chiamata Comandi Tramite Codice

In alcune situazioni puoi desiderare di eseguire un comando Artisan al di fuori della console. Per esempio, puoi eseguire un comando da una route o da un controller. Puoi usare il metodo `call` dalla facade `Artisan`. Il metodo `call` accetta il nome del comando come primo parametro, ed un array di parametri come secondo parametro. Sarà ritornato il codice di uscita:

    Route::get('/foo', function () {
        $exitCode = Artisan::call('email:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    });

Usando il metodo `queue` della facade `Artisan`, puoi mettere sempre in coda i comandi Artisan in modo da essere eseguiti in background dalla tua [queue workers](/docs/{{version}}/queues):

    Route::get('/foo', function () {
        Artisan::queue('email:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    });

### Richiamare Comandi Da Altri Comandi

Qualche volta puoi voler chiamare altri comandi da un comando Artisan esistente. Per farlo, puoi usare il metodo `call`. Questo metodo `call` accetta il nome del comando ad un array di parametri di comando:

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $this->call('email:send', [
            'user' => 1, '--queue' => 'default'
        ]);

        //
    }

Se preferisci chiamare un altro comando e sopprimere tutti i suoi input, usa il metodo `callSilent`. Il metodo `callSilent` ha la stessa signature del metodo `call`:

    $this->callSilent('email:send', [
        'user' => 1, '--queue' => 'default'
    ]);
