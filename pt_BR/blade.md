# Blade Templates

- [Introdução](#introduction)
- [Herança de Templates](#template-inheritance)
	- [Definindo um layout](#defining-a-layout)
	- [Herdando um layout](#extending-a-layout)
- [Exibindo Dados](#displaying-data)
- [Estruturas de Controle](#control-structures)
- [Serviço de Injeção](#service-injection)
- [Extendendo o Blade](#extending-blade)

<a name="introduction"></a>
## Introdução

Blade é um simples e poderoso mecanismo de templates fornecido com o Laravel. Diferentemente de outros mecanismos de templates PHP, o Blade não lhe restringe de usar puro PHP em suas views. Todas as views Blade são compiladas em PHP puro e armazenadas em cache até serem modificadas, e isso significa que usar templates Blade essenciamente não "pesam" sua aplicação. Todos os arquivos Blade usam a extensão `.blade.php` e tipicamente estão armazenados no diretório `resources/views`.

<a name="template-inheritance"></a>
## Herança de Templates

<a name="defining-a-layout"></a>
### Definindo um layout

Dois benefícios básicos de usar o Blade são _template inheritance_ e _sections_. Para iniciarmos, vamos dar uma olhada em um exemplo simples. Primeiro, nós vamos examinar um layout de uma "master page". Como a maioria das aplicações web mantém um layout em comum na maioria de suas páginas, é conveniente definir esse layout como uma view Blade:

	<!-- Stored in resources/views/layouts/master.blade.php -->

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

Como você pode ver, esse arquivo contém um típico código HTML. Entretanto, note as diretivas `@section` e `@yield`. A diretiva `@section`, como seu nome implica, define uma parte/seção do conteúdo, enquanto a diretiva  `@yield` é utilizada para exibir os conteúdos de uma seção.

Agora que nós definimos um layout para nossa aplicação, vamos definir uma página filha que herda esse layout.

<a name="extending-a-layout"></a>
### Herdando um layout

Ao definir uma página filha, você deve utilizar a diretiva `@extends` para especificar qual layout a página filha deve "herdar". Views que  `@extend` um layout Blade podem injetar conteúdo no layout mestre usando a diretiva `@section`. Lembre-se, como visto no exemplo acima, os conteúdos dessas seções serão exibidos no layout mestre usando a diretiva `@yield`:

	<!-- Stored in resources/views/layouts/child.blade.php -->

	@extends('layouts.master')

	@section('title', 'Page Title')

	@section('sidebar')
		@@parent

		<p>This is appended to the master sidebar.</p>
	@endsection

	@section('content')
		<p>This is my body content.</p>
	@endsection

Nesse exemplo, a seção `sidebar` está utilizando a diretiva `@@parent` para incluir (ao invés de sobrescrever) o conteúdo do layout para a sidebar (menu lateral). A diretiva `@@parent` será substituída pelo conteúdo do layout mestre quando a view for renderizada.

E claro, assim como views com PHP puro, as views Blade podem ser retornadas diretamente das suas rotas usando a função helper global `view`:

	Route::get('blade', function () {
		return view('child');
	});

<a name="displaying-data"></a>
## Exibindo Dados

Você pode exibir dados passados para suas views Blade ao inserir a variável entre chaves. Por exemplo, dado a seguinte rota:

	Route::get('greeting', function () {
		return view('welcome', ['name' => 'Samantha']);
	});

Você pode exibir os conteúdos da variável `name` da seguinte maneira:

	Hello, {{ $name }}.

Claro, você não está limitado a exibir somente os conteúdos de suas variáveis em uma view Blade. Você também pode imprimir o resultado de uma função PHP. Na verdade, você pode colocar qualquer código PHP que você desejar dentro de uma declaração echo do Blade:

	The current UNIX timestamp is {{ time() }}.

> **Nota:** Todas as declarações Blade `{{ }}` são automaticamente enviadas por meio da função `htmlentities` para previnir ataques XSS.

#### Blade & Frameworks JavaScrip

Como muitos frameworks JavaScript também utilizam chaves para indicar uma expressão que deve ser exibida no navegador, você deve utilizar o símbolo `@` para informar ao Blade que aquele pedaço de código não deve ser renderizado. Por exemplo:

	<h1>Laravel</h1>

	Hello, @{{ name }}.

Nesse exemplo, o símbolo `@` será removido pelo Blade; Entretanto, a expressão `{{ name }}` continuará intocada pelo mecanismo do Blade, permitindo assim que essa parte de seu código seja renderizada pelo framework JavaScript que você estiver utilizando.

#### Exibindo os dados caso eles existam

Algumas vezes você quer exibir uma variável, mas não tem certeza se ela foi atribuída. Podemos fazer essa verificação via PHP da seguinte maneira:

	{{ isset($name) ? $name : 'Default' }}

Entretando, ao invés de utilizar um if ternário, o Blade lhe fornece o seguinte atalho:

	{{ $name or 'Default' }}

Nesse exemplo, se a variável `$name` existir, seu valor será exibido. Entretando, se não existir, a palavra `Default` será exibida.

#### Exibindo dados "não tradados/não escapados"

Por padrão, com a sintaxe `{{ }}` todas as declarações realizadas pelo Blade são automaticamente enviadas através da função PHP `htmlentities` para prevenir ataques XSS. Se você quiser que os dados não sejam tradados/escapados, utilize a seguinte sintaxe:

	Hello, {!! $name !!}.

> **Nota:** Seja muito cuidadoso quando exibir os dados que são fornecidos pelos usuários da sua aplicação. Sempre utilize chaves duplas para exibir qualquer elemento HTML no conteúdo.

<a name="control-structures"></a>
## Estruturas de Controle

Em adição à herança e a exibição de dados, o Blade também fornece atalhos convenientes para as mais comuns estruturas de controle do PHP, como declarações condicionais e loops. Esses atalhos fornecem uma maneira muito concisa e limpa de trabalhar com essas estruturas, além de continuar parecidos com as expressões originais do PHP puro.

#### Declarações If

Você pode utilizar declarações `if` com as diretivas `@if`, `@elseif`, `@else`, e `@endif`. A funcionalidade dessas diretivas são idênticas às expressões originais do PHP:

	@if (count($records) === 1)
		I have one record!
	@elseif (count($records) > 1)
		I have multiple records!
	@else
		I don't have any records!
	@endif

Para conveniência, o Blade também fornece uma diretiva `@unless`:

	@unless (Auth::check())
		You are not signed in.
	@endunless

#### Repetições

Além das estruturas condicionais, o Blade fornece diretivas simples para trabalhar com as estruturas de repetições suportadas pelo PHP. Novamente, a funcionalidade dessas diretivas são idênticas às expressões originais do PHP:

	@for ($i = 0; $i < 10; $i++)
		The current value is {{ $i }}
	@endfor

	@foreach ($users as $user)
		<p>This is user {{ $user->id }}</p>
	@endforeach

	@forelse ($users as $user)
		<li>{{ $user->name }}</li>
	@empty
		<p>No users</p>
	@endforelse

	@while (true)
		<p>I'm looping forever.</p>
	@endwhile

#### Incluindo Sub-Views

Com a diretiva `@include` do Blade, você pode facilmente incluir outra view Blade em uma view existente. Todas as variáveis da view "mãe" estarão disponíveis na view "filha":

	<div>
		@include('shared.errors')

		<form>
			<!-- Form Contents -->
		</form>
	</div>

Apesar disso, você pode também passar um array com dados extras para a view que está sendo incluída:

	@include('view.name', ['some' => 'data'])

#### Comentários

O Blade também lhe permite adicionar comentários em suas views. Entretanto, diferentemente dos comentários HTML, os comentários Blade não estarão dispoíveis no HTML renderizado por sua aplicação:

	{{-- This comment will not be present in the rendered HTML --}}

<a name="service-injection"></a>
## Serviço de Injeção

A diretiva `@inject` deve ser utilizada para recuperar um serviço diretamente do [service container](/docs/{{version}}/container) do Laravel. O primeiro parâmetro passado para a diretiva `@inject` é o nome da variável em que o serviço será injetado, enquanto o segundo parâmetro é a classe / interface do serviço está incluindo:

	@inject('metrics', 'App\Services\MetricsService')

	<div>
		Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
	</div>

<a name="extending-blade"></a>
## Extendendo o Blade

O Blade lhe permite até adicionar diretivas customizadas. Você pode usar o método `directive` para registrar uma diretiva. Quando o blade for compilado e encontrar a diretiva, ele chamará a função de retorno fornecida com seus parâmetros.

O exemplo a seguir cria uma diretiva `@datetime($var)` que formata a variável `$var` que é fornecida:

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

Como você pode ver, o função helper `with` do Laravel foi utilizada nessa diretiva. O helper `with` simplesmente retorna o objeto/ valor que é atribuído, permitindo um conveniente encadeamento de métodos. O PHP gerado por essa diretiva é:

	<?php echo with($var)->format('m/d/Y H:i'); ?>


