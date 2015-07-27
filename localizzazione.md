# Localizzazione

- [Introduzione](#introduzione)
- [Uso Base](#uso-base)
	- [Pluralizzazione](#pluralizzazione)
- [Sovrascrivere I Language File Di Un Package](#sovrascrivere-language-file)

<a name="introduzione"></a>
## Introduzione

La funzionalità di localizzazione di Laravel offre un modo conveniente per recuperare stringhe di testo in varie lingue, dandoti la possibilità di gestire facilmente più lingue con la tua applicazione.

Le stringhe di testo sono memorizzate in file all'interno della directory `resources/lang`. All'interno di questa directory dovrebbero essere create delle sotto-cartelle per ogni linguaggio supportato dalla tua applicazione:

	/resources
		/lang
			/en
				messages.php
			/es
				messages.php

Tutti i file di lingua ritornano semplicemente un array associativo di stringhe. Per esempio:

	<?php

	return [
		'welcome' => 'Welcome to our application'
	];

#### Configurare Il Locale

Il linguaggio di default della tua applicazione è memorizzato nel file `config/app.php`. Ovviamente, puoi modirficare questo valore a seconda delle esigenze della tua applicazione. Puoi anche cambiare la lingua in runtime usando il metodo `setLocale` della facade `App`:

	Route::get('welcome/{locale}', function ($locale) {
		App::setLocale($locale);

		//
	});

Puoi anche configurare un "fallback language", che sarà usato quando la lingua corrente non contiene una data stringa di testo. Come la lingua di default, il fallback language è configurato all'interno del file `config/app.php`:

	'fallback_locale' => 'en',

<a name="uso-base"></a>
## Uso Base
Puoi recuperare una linea da un file di lingua usando la funzione helper `trans`. Il metodo `trans`accetta il nome del file e la chiave della linea come suo primo parametro. Per esempio, recuperiamo la linea `welcome` nel file `resources/lang/messages.php`:

	echo trans('messages.welcome');

Ovviamente se stai usando [Blade](/docs/{{version}}/views#blade-templating), puoi usare la sintassi `{{ }}` per stampare la stringa:

	{{ trans('messages.welcome') }}

Se la linea di lingua non esiste, la funzione `trans` ritornerà il nome della chiave. In questo modo, seguendo l'esempio sopra, la funzione `trans` dovrebbe ritornare `messages.welcome` se la linea di lingua non esiste.

#### Attivare Una Sostituzione Nella Linea

Se lo desideri, puoi definire dei place-holders nelle tue linee. Tutti i place-holder sono precedeuti da un `:`. Per esempio, puoi definire un messaggio di benvenuto con un place-holder per il nome dell'utente:

	'welcome' => 'Welcome, :name',

Per sostituire il place-holders quando si recupera una lina, passa un array come secondo parametro della funzione `trans`:

	echo trans('messages.welcome', ['name' => 'Dayle']);

<a name="pluralizzazione"></a>
### Pluralizzazione

La pluralizzazione è un problema complesso, differenti linguaggi hanno una varietà di regole complesse per la pluralizzazione. Puoi gestire facilmente questo aspetto nel tuo language file. Usando il carattere "pipe" puoi separare la forma singolare da quella plurale di una stringa:

	'apples' => 'There is one apple|There are many apples',

Quindi, puoi usare la funzione `trans_choice` per recuperare la linea per un dato "count". In questo esempio, dato che il valore è maggiore di uno, sarà ritornata la forma plurale della linea:

	echo trans_choice('messages.apples', 10);

Visto che il traduttore di Laravel è basato sul componente Translation di Symfony, puoi creare delle regole di pluralizzazione ancora più complesse:

	'apples' => '{0} There are none|[1,19] There are some|[20,Inf] There are many',

<a name="sovrascrivere-language-file"></a>
## Sovrascrivere I Language File Di Un Package

Alcuni package possono lavorare con dei propri file di lingua. Invece di hackerare il core di questi file per modificare queste linee, puoi sovrascriverle inserendo i tuoi file nella directory `resources/lang/vendor/{package}/{locale}`.

Così, per esempio, se hai bisogno di sovrascrivere le linee della lingua Inglese in `messages.php` per un certo package chiamato `skyrim/hearthfire`, potresti memorizzare un file di lingua in: `resources/lang/vendor/hearthfire/en/messages.php`. In questo file dovresti definire soltanto le linee che desideri sovrascrivere. Qualsiasi linea non sovrascritta sarà caricata dai file di lingua originali del package.
