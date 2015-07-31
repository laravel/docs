# Blade Templates

- [Introduzione](#introduzione)
- [Template ed Ereditarietà](#template-ereditarieta)
	- [Definire un Layout](#definire-layout)
	- [Estendere un Layout](#estendere-layout)
- [Mostrare dei Dati](#mostrare-dati)
- [Strutture di Controllo](#strutture-controllo)
- [Service Injection](#service-injection)
- [Estendere Blade](#estendere-blade)

<a name="introduzione"></a>
## Introduzione

Blade è un template engine molto semplice ma allo stesso tempo molto potente che viene incluso in ogni installazione di Laravel. Nonostante le sue svariate funzionalità, Blade non ti impedisce comunque, se vuoi, di usare il PHP vero e proprio nel tuo codice. Tutte le view vengono compilate e messe in cache per poi essere ri-compilate in caso di modifiche. Il che vuol dire che l'overhead di Blade è praticamente prossimo allo zero. I file riconosciuti da Blade terminano con l'estensione _.blade.php_.

Normalmente, puoi trovare le view nella cartella _resources/views_.

<a name="template-ereditarieta"></a>
## Template ed Ereditarietà

<a name="definire-layout"></a>
### Definire un Layout

I benefici principali nell'uso di Blade sono la possibilità di creare dei template che ne estendono altri, insieme alla possibilità di creare delle sezioni, strutture che vedremo a breve.

In molte applicazioni viene usato un template di base, generalmente chiamato _master page_. Da questa pagina, quindi, vengono create tutte le altre. La _master page_ quindi funge da minimo comun denominatore. La stessa cosa si può fare con Blade.

Partiamo da una view base:

	<!-- File: resources/views/layouts/master.blade.php -->

	<html>
		<head>
			<title>App Name - @yield('title')</title>
		</head>
		<body>
			@section('sidebar')
				This is the master sidebar.
			@show

			<div class="container">
				@yield('content')
			</div>
		</body>
	</html>

Come puoi vedere, questo file contiene del semplice codice HTML. Con qualche eccezione: avrai sicuramente visto le istruzioni _@section_ e _@yield_. La direttiva _@section_ definisce una sezione con dei contenuti specific. La direttiva _@yield_, invece, funge da segnaposto per contenuti che verranno aggiunti successivamente (da pagine derivanti da questa "base").

Ora che abbiamo definito la master page, vediamo come estenderla.

<a name="estendere-layout"></a>
### Estendere un Layout

Quando definisci una pagina a partire da un'altra "madre", devi usare la direttiva _@extends_ di Blade per specificare quale pagina bisogna estendere. A quel punto puoi specificare le varie sezioni nell'ordine che preferisci, in modo tale da iniettare il codice necessario durante l'uso.

	<!-- File: resources/views/layouts/child.blade.php -->

	@extends('layouts.master')

	@section('title', 'Page Title')

	@section('sidebar')
		@@parent

		<p>This is appended to the master sidebar.</p>
	@endsection

	@section('content')
		<p>This is my body content.</p>
	@endsection

Nell'esempio che hai appena visto, inoltre, la sezione _sidebar_ usa la direttiva `@@parent` per aggiungere (e non sovrascrivere) il contenuto della sidebar.

Esattamente come per delle semplicissime view PHP, puoi usare l'istruzione _return view()_ per mandarle in output.

	Route::get('blade', function () {
		return view('child');
	});

<a name="mostrare-dati"></a>
## Mostrare dei Dati

Puoi mostrare dei dati in una view passandoglieli, quindi usando le doppie parentesi graffe. Per farti un esempio, guarda questa route:

	Route::get('greeting', function () {
		return view('welcome', ['name' => 'Samantha']);
	});

Per mostrare la variabile in _name_ nella view _welcome_ dovrai usare la seguente istruzione:

	Hello, {{ $name }}.

Non sei chiaramente limitato ad una cosa così semplice. Puoi anche usare una qualsiasi funzione PHP, per iniziare!

	The current UNIX timestamp is {{ time() }}.

> **Nota:** per evitare gli attacchi XSS, tutto quello che passa per le parantesi graffe di blade è sistemato con `htmlentities`.

#### Blade ed I Framework JavaScript

Visto che molti framework JavaScript usano le parentesi graffe, come Blade, puoi precederle con il simbolo _@_ se vuoi spiegare a Blade che quelle parentesi, stavolta, non sono per lui.

	<h1>Laravel</h1>

	Hello, @{{ name }}.

Nell'esempio appena visto il _@_ verrà rimosso da Blade. L'espressione `{{ name }}`, invece, rimarrà intatta così com'è.

#### Echo di Dati se Esistono

A volte potresti voler stampare il valore di una variabile, ma non sei sicuro della sua esistenza. Puoi usare PHP in questo modo:

	{{ isset($name) ? $name : 'Default' }}

oppure...

	{{ $name or 'Default' }}

Più comodo, vero? La stringa _'Default'_ indica un valore di default che viene mostrato se _$name_ non esiste.

#### Mostrare dei Dati non "Puliti"

Come già accennato prima, di default Blade effettua l'escape dell'output tramite _htmlentities_, in modo tale da prevenire attacchi XSS. Tuttavia, nel caso in cui volessi evitare una cosa del genere, sentiti libero di usare

	Hello, {!! $name !!}.

> **Nota:** ovviamente, massima attenzione nei confronti di quello che mandi in output, se usi questa istruzione.

<a name="strutture-controllo"></a>
## Strutture di Controllo

In aggiunta all'ereditarietà dei template e alla possibilità di mostrare dei dati, Blade fornisce svariate direttive equivalenti (a volte sono vere e proprie aggiunte) alle strutture di controllo PHP. In questo modo sarà più semplice avere un codice più pulito.

#### If

Puoi usare le direttive `@if`, `@elseif`, `@else`, ed `@endif` per costruire un blocco _If_:

	@if (count($records) === 1)
		I have one record!
	@elseif (count($records) > 1)
		I have multiple records!
	@else
		I don't have any records!
	@endif

Per convenienza, inoltre, Blade fornisce anche la controparte `@unless`:

	@unless (Auth::check())
		You are not signed in.
	@endunless

#### Loop

In aggiunta alle strutture condizionali, _Blade_ fornisce anche le direttive per lavorare con le strutture di loop PHP. Le direttive sono identiche alle loro controparti PHP.

	@for ($i = 0; $i < 10; $i++)
		Il valore attuale è {{ $i }}
	@endfor

	@foreach ($users as $user)
		<p>Questo è l'utente {{ $user->id }}</p>
	@endforeach

	@forelse ($users as $user)
		<li>{{ $user->name }}</li>
	@empty
		<p>Nessun utente presente.</p>
	@endforelse

	@while (true)
		<p>Loop Eterno!</p>
	@endwhile

#### Includere altre View

Tramite la direttiva `@include` puoi includere una view dentro un'altra. Le variabili assegnate alla view che include sono automaticamente disponibili anche all'inclusa.

	<div>
		@include('shared.errors')

		<form>
			<!-- Form Contents -->
		</form>
	</div>

Nulla ti vieta comunque di passare altri dati aggiuntivi tramite la seguente sintassi.

	@include('view.name', ['some' => 'data'])

#### Commenti

Blade ti consente di scrivere dei commenti all'interno delle tue view. Tuttavia, a differenza di come avviene nell'HTML, i commenti di Blade NON vengono inclusi nell'applicazione.

	{{-- Questo commento non sarà presente nell'HTML --}}

<a name="service-injection"></a>
## Service Injection

Tramite la direttiva _@inject_ puoi usare un qualsiasi servizio tramite [service container](/documentazione/5.1/container). Il primo parametro passato è il nome della variabile a cui verrà assegnata l'istanza, mentre il secondo è il nome della classe/interfaccia da risolvere.

	@inject('metrics', 'App\Services\MetricsService')

	<div>
		Entrate Mensili: {{ $metrics->monthlyRevenue() }}.
	</div>

<a name="estendere-blade"></a>
## Estendere Blade

Blade ti permette di definire le tue direttive in modo personalizzato. Puoi usare il metodo _directive_ per registrare una nuova direttiva e quindi ampliare le possibilità offerte da Blade. 

L'esempio seguente crea una direttiva di tipo _@datetime($var)_ che da un formato ad un parametro _$var_.

	<?php namespace App\Providers;

	use Blade;
	use Illuminate\Support\ServiceProvider;

	class AppServiceProvider extends ServiceProvider
	{
		/**
		 * Perform post-registration booting of services.
		 *
		 * @return void
		 */
		public function boot()
		{
			Blade::directive('datetime', function($expression) {
				return "<?php echo with{$expression}->format('m/d/Y H:i'); ?>";
			});
		}

		/**
		 * Register bindings in the container.
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}
	}

Come puoi vedere, viene usato l'helper _with_ di Laravel. Molto prezioso, questo _helper_ ritorna l'oggetto che gli viene passato, in modo tale da consentire, quando non possibile, la concatenazione di più chiamate a svariati metodi di un certo oggetto.

Il codice generato da questa direttiva sarà, alla fine:

	<?php echo with($var)->format('m/d/Y H:i'); ?>
