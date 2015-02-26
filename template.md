# Template

- [Template Con Blade](#template-con-blade)
- [Altre Strutture Di Controllo Con Blade](#altre-strutture-di-controllo-con-blade)
- [Estendere Blade](#estendere-blade)

<a name="template-con-blade"></a>
## Template Con Blade

Blade è un template engine molto semplice ma allo stesso tempo molto potente che viene incluso in ogni installazione di Laravel. A differenza dei controller layout, Blade è guidato da _template inheritance_ e _sections_. Tutti i template Blade devono avere `.blade.php` come estensione.

#### Definire Un Layout Blade

	<!-- Salvato in resources/views/layouts/master.blade.php -->

	<html>
		<body>
			@section('sidebar')
				Questa è la Sidebar principale.
			@stop

			<div class="container">
				@yield('content')
			</div>
		</body>
	</html>

#### Utilizzare Un Layout Blade

	@extends('layouts.master')

	@section('sidebar')
		@parent

		<p>Questo verrà aggiunto alla sidebar principale.</p>
	@stop

	@section('content')
		<p>Questo è il contenuto.</p>
	@stop

Nota che le view che estendono il layout Blade tramite la parola chiave `extend` non fanno altro che sovrascrivere le sezioni. Il contenuto del layout può essere incluso nel layout figlio usando la direttiva `@parent` nella sezione, permettendo così di aggiungere contenuti.

Qualche volta, come ad esempio quando non sai se una particolare sezione è stata definita, puoi passare un valore di default alla direttiva `@yield`. Puoi farlo passando il valore di default come secondo argomento:

	@yield('section', 'Default Content')

<a name="altre-strutture-di-controllo-con-blade"></a>
## Altre Strutture Di Controllo Con Blade

#### Stampare I Dati

	Ciao, {{ $name }}.

	Lo UNIX timestamp corrente è {{ time() }}.

#### Stampare Dati Dopo Aver Controllato La Loro Esistenza

Qualche volta potresti aver bisogno di stamapre una variabile ma non sei sicuro che quella variabile sia stata impostata, in pratica hai bisogno di una cosa del genere:

	{{ isset($name) ? $name : 'Default' }}

Tuttavia, invece di scrivere la forma contratta di controllo, Blade ti permette di utilizzare questo trucchetto che ti velocizza la scrittura:

	{{ $name or 'Default' }}

#### Mostrare Puro Testo Dentro Parentesi Graffe

Se hai bisogno di stamapre a video del testo all'interno di parentesi graffe è necessario informare Balde evitando che effettui il parsing del testo. Per farlo è sufficiente anteporre il simbolo `@`:

	@{{ Questo testo non verrà processato da Blade }}

Se non vuoi che sul contenuto di una variabile vengano eseguite funzioni di escape, puoi usare questa sintassi:

	Ciao, {!! $name !!}.

> **Nota:** Fai molta attenzione quando stampi a video contenuto che arriva da un utente che utilizza la tua applicazione. Sempre meglio usare la tripla parentesi graffa per eseguire l'escape di qualsiasi codice HTML inserito nelle variabili.

#### Costrutto If

	@if (count($records) === 1)
		Ho un valore!
	@elseif (count($records) > 1)
		Ho più di un valore!
	@else
		Non ho nessun valore!
	@endif

	@unless (Auth::check())
		Non hai eseguito il login.
	@endunless

#### Cicli

	@for ($i = 0; $i < 10; $i++)
		Il valore corrente è: {{ $i }}
	@endfor

	@foreach ($users as $user)
		<p>Questo è l'utente: {{ $user->id }}</p>
	@endforeach

	@forelse($users as $user)
	  	<li>{{ $user->name }}</li>
	@empty
	  	<p>Non ci sono utenti</p>
	@endforelse

	@while (true)
		<p>Questo ciclo non finirà mai.</p>
	@endwhile

#### Includere Sotto-View

	@include('view.name')

Puoi anche passare un array di dati alla view che vuoi includere:

	@include('view.name', ['some' => 'data'])

#### Sovrascrivere Le Sezioni

Per sovrascrivere completamente una sezione puoi usare la direttiva `overwrite`:

	@extends('list.item.container')

	@section('list.item.content')
		<p>Questo è un elemento di tipo {{ $item->type }}</p>
	@overwrite

#### Mostrare Le Linee Di Una Lingua

	@lang('language.line')

	@choice('language.line', 1)

#### Commenti

	{{-- Questo commento non sarà mostrato nell'HTML della pagina --}}

<a name="estendere-blade"></a>
## Estendere Blade

Blade ti permette anche di definire le tue strutture di controllo. Quando un file Blade è compilato, ogni estensione viene chiamata con il contenuto della view, permettendoti così di fare quello che vuoi come ad esempio usare un semplice `str_replace` o una complessa espressione regolare.

Il compilatore Blade ha alcuni metodi molto utili come `createMatcher` e `createPlainMatcher`, che generano tutte le espressioni che ti servono per creare le tue direttive.

Il metodo `createPlainMatcher` è utilizzato per le direttive che non hanno nessun argomento come ad esempio `@endif` e `@stop`, mentre il metodo `createMatcher` viene usato per quelle direttive che richiedono almeno un argomento.

Il seguente esempio crea la direttiva `@datetime($var)` che semplicemente chiama `->format()` su `$var`:

	Blade::extend(function($view, $compiler)
	{
		$pattern = $compiler->createMatcher('datetime');

		return preg_replace($pattern, '$1<?php echo $2->format(\'m/d/Y H:i\'); ?>', $view);
	});
