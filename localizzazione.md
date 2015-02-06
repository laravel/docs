# Localizzazione

- [Introduzione](#introduzione)
- [Language File](#language-File)
- [Uso Base](#uso-base)
- [Pluralizzazione](#pluralizzazione)
- [Validazione](#validazione)
- [Sovrascrivere I Language File Di Un Package](#sovrascrivere-language-file-package)

<a name="introduzione"></a>
## Introduzione

La facade `Lang` di Laravel offre un modo conveniente per recuperare stringhe di testo neri vari linguaggi, offrendoti un facile supporto per le applicazioni multi-language.

<a name="language-file"></a>
## Language File

Le stringhe di testo nei vari linguaggi sono memorizzate nella directory `resources/lang`. All'interno di questa directory troverai delle sub-directory per ogni lingua supportata dalla tua applicazione.

	/resources
		/lang
			/en
				messages.php
			/es
				messages.php

#### Esempio Di Language File

I language file ritornano semplicemente un array associativo di stringhe. Per esempio:

	<?php

	return array(
		'welcome' => 'Welcome to our application'
	);

#### Cambiare Il Linguaggio Di Default In Fase di Esecuzione

Il linguaggio di default della tua applicazione è memorizzato nel file di configurazione `config/app.php`. Puoi rendere attivo qualsiasi linguaggio usando il metodo `App::setLocale`:

	App::setLocale('es');

#### Impostare Il Linguaggio Fallback

Puoi configurare anche il "fallback language, il quale verrà usato quando il linguaggio attivo non dovesse contenere una data stringa. Come il linguaggio di default, il fallback language è configurabile dal file di configurazione `config/app.php`:

	'fallback_locale' => 'en',

<a name="uso-base"></a>
## Uso Base

#### Ritrovare Una Linea Da Un Language File

	echo Lang::get('messages.welcome');

Il primo segmento della stringa passato al metodo `get` è il nome del language file, ed il secondo è il nome della linea che dovrà essere recuperata.

> **Nota:** Se una linea non dovesse esistere, verrà ritornato il nome della chiave tramite il metodo `get`.

Puoi anche usare la funzione helper `trans`, come alias per il metodo `Lang::get`.

	echo trans('messages.welcome');

#### Attivare Una Sostituzione Nella Linea

Puoi definire anche dei place-holder nella linea:

	'welcome' => 'Welcome, :name',

A quel punto, basta passare un secondo argomento al metodo `Lang::get`:

	echo Lang::get('messages.welcome', array('name' => 'Dayle'));

#### Determinare Se Un Language File Contiene Una Linea

	if (Lang::has('messages.welcome'))
	{
		//
	}

<a name="pluralizzazione"></a>
## Pluralizzazione

La pluralizzazione è un problema complesso, differenti linguaggi hanno una varietà di regole complesse per la pluralizzazione. Puoi gestire facilmente questo aspetto nel tuo language file. Usando il carattere "pipe" puoi separare la forma singolare da quella plurale di una stringa:

	'apples' => 'There is one apple|There are many apples',

Quindi usando il metodo `Lang::choice` puoi recuperare la linea adatta:

	echo Lang::choice('messages.apples', 10);

Puoi anche fornire al metodo un parametro supplementare per specificare la lingua. Per esempio, se vuoi usare il Russo (ru):

	echo Lang::choice('товар|товара|товаров', $count, array(), 'ru');

Dato che Laravel utilizza il componente Translation di Symfony, inoltre, puoi anche creare più regole di pluralizzazione: 

	'apples' => '{0} There are none|[1,19] There are some|[20,Inf] There are many',


<a name="validazione"></a>
## Validazione

Per la localizzazione dei messaggi di errore e di validazione dai uno sguardo alla [documentazione sulla Validazione](/validazione).

<a name="sovrascrivere-language-file-package"></a>
## Sosvrascrivere I Language File Di Un Package

Puoi sovrascrivere quello che non ti serve, infatti, piazzando dei file di lingua ad hoc nella cartella `resources/lang/packages/{locale}/{package}`. Così, per esempio, se hai bisogno di sovrascrivere le linee del file in Inglese nel file `messages.php` per un package chiamato `skyrim/hearthfire`, devi semplicemente aggiungere una linea in: `resources/lang/packages/en/hearthfire/messages.php`. In questo file potrai definire solo le linee che desideri sovrascrivere. Qualsiasi linea che non desideri sovrascrivere sarà caricata direttamente dal file di lingua del package.
