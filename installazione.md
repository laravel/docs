# Installazione

- [Installare Composer](#installare-composer)
- [Installare Laravel](#installare-laravel)
- [Requisiti](#requisiti)
- [Configurazione](#configurazione)
- [Riscrittura degli URL](#riscrittura-url)

<a name="installare-composer"></a>
## Installare Composer

Laravel usa [Composer](http://getcomposer.org) per la gestione delle dipendenze. Ragion per cui, prima di usare Laravel, dovrai assicurarti di aver installato Composer sulla tua macchina.

<a name="installare-laravel"></a>
## Installare Laravel

### Tramite Laravel Installer

Innanzitutto, scarica il Laravel Installer usando Composer.

	composer global require "laravel/installer=~1.1"

Assicurati di aver messo la directory `~/.composer/vendor/bin` nella variabile d'ambiente PATH, in modo tale da poter usare `laravel` da qualsiasi directory.

Una volta installato, puoi usare il semplice comando _laravel new_ che si occuperà di creare un nuovo progetto Laravel nella directory da te specificata. Quindi, per fare un esempio, _laravel new blog_ creerà una nuova applicazione Laravel nella cartella _blog_.

	laravel new blog

### Tramite Composer Create-Project

Puoi anche installare Laravel tramite il comando `create-project` di Composer nel tuo terminale.

	composer create-project laravel/laravel --prefer-dist

<a name="requisiti"></a>
## Requisiti

Laravel ha alcuni requisiti. Pochi, ma comunque ci sono:

- PHP >= 5.4
- Estensione PHP Mcrypt
- Estensione PHP OpenSSL
- Estensione PHP Mbstring

Usando PHP 5.5 alcune distribuzioni potrebbero richiedere l'installazione manuale dell'estensione PHP JSON. Usando Ubuntu il problema si può facilmente risolvere usando

	`apt-get install php5-json`

<a name="configurazione"></a>
## Configurazione

La prima cosa che devi fare, dopo aver installato Laravel, è impostare la tua application key. Se hai effettuato l'installazione via Composer molto probabilmente questa operazione è stata già effettuata, tramite il comando `key:generate` di Artisan.

Una buona norma vuole questa stringa lunga 32 caratteri. Può essere impostata nel file _app.php_ di configurazione.

> Nota: nel caso in cui la chiave non venga impostata, l'applicazione non sarà totalmente al sicuro!

Di default, Laravel non ha bisogno di altre configurazioni particolari per funzionare, per cui arrivato a questo punto puoi già sentirti libero di fare qualche prima prova! Continuando a dare un'occhiata al file _config/app.php_, inoltre, potresti trovare altre cose interessanti. Un esempio su tutti: la scelta della timezone.

Una volta sistemata questa prima configurazione, comunque, ti conviene dare uno sguardo anche alle [impostazioni dell'ambiente locale](/configurazione#configurazione-ambiente).

> **Nota:** Ricorda di non impostare mai su _true_ la variabile _app.debug_ se sei in produzione.

<a name="permessi"></a>
### Permessi

Potresti aver bisogno di impostare alcuni permessi: nello specifico, ricorda che la cartella _public_ è quella esposta ed accessibile dall'esterno, e _storage_ richiede l'accesso per la scrittura da parte del server.

<a name="riscrittura-url"></a>
## Riscrittura degli URL

### Apache

Di default, il framework ha già un file _public/.htaccess_ copiato in ogni nuovo progetto. Permette di inserire gli URL della tua applicazione senza dover specificare il _index.php_ molto fastidioso. Se usi Apache per eseguire la tua applicazione, assicurati di abilitare il modulo _mod_rewrite_.

Nel caso in cui il file di default non dovesse funzionare, prova con questo:

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]

### Nginx

Su Nginx, invece, puoi usare le seguenti direttive nel tuo file di configurazione per ottenere lo stesso risultato.

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

Ovviamente, usando [Homestead](/homestead), tutte queste impostazioni sono sistemate automaticamente.
