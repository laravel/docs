# Lista de Tarefas - Básico

- [Introdução](#introduction)
- [Instalação](#installation)
- [Preparando o Banco de Dados](#prepping-the-database)
	- [Banco de Dados: Migrations](#database-migrations)
	- [Modelos Eloquent](#eloquent-models)
- [Roteamento](#routing)
	- [Rotas](#stubbing-the-routes)
	- [Exibindo uma Visão](#displaying-a-view)
- [Construindo Layouts & Views](#building-layouts-and-views)
	- [Definindo o Layout](#defining-the-layout)
	- [Definindo uma Visão Filha](#defining-the-child-view)
- [Criando um Tarefa](#adding-tasks)
	- [Validação](#validation)
	- [Criando um Tarefa](#creating-the-task)
	- [Exibindo Tarefas Existentes](#displaying-existing-tasks)
- [Apagando Tarefas](#deleting-tasks)
	- [Adicionando o botão de Apagar](#adding-the-delete-button)
	- [Apagando a Tarefa](#deleting-the-task)

<a name="introduction"></a>
## Introdução

Este guia fornece uma introdução básica ao framework Laravel e abrange: migração de banco de dados, Eloquent (ORM), roteamento, validação, visões e templates utilizando o Blade. Este guia é um ótimo ponto de partida se você é iniciante no uso do framework Laravel ou de frameworks PHP em geral.  Se você já utiliza o Laravel ou outros frameworks PHP, talvez queira consultar um guia mais avançado.

Para exemplificar um uso básico das funcionalidades do Laravel, construiremos uma simples aplicação de lista de tarefas onde poderemos manter todas as tarefas que desejamos realizar (uma típica aplicação "to-do"). O código fonte completo do projeto está [disponível no GitHub](http://github.com/laravel/quickstart-basic).

<a name="installation"></a>
## Instalação

Primeiro você precisará de uma nova instalação do Laravel. Você pode utilizar a [virtual machine Homestead](/docs/{{version}}/homestead) ou o ambiente PHP de sua preferência para executar o framework. Uma vez que seu ambiente esteja pronto, você pode instalar o framework Laravel utilizando o Composer:

	composer create-project laravel/laravel quickstart --prefer-dist

Você pode continuar apenas lendo este guia; entretanto, se desejar realizar o download do código fonte utilizado neste guia e executá-lo em seu ambiente local, você pode clonar seu repositório Git e instalar suas dependências:

	git clone https://github.com/laravel/quickstart-basic quickstart
	cd quickstart
	composer install
	php artisan migrate

Para uma documentação mais completa de como executar um ambiente local para desenvolvimento utilizando Laravel, confira a documentação completa do [Homestead](/docs/{{version}}/homestead) e da [instalação](/docs/{{version}}/installation) do framework.

<a name="prepping-the-database"></a>
## Preparando o Banco de Dados

<a name="database-migrations"></a>
### Banco de Dados: Migrations

Primeiro, vamos utilizar uma migration para definir uma tabela para armazenar todas as nossas tarefas. O Laravel fornece uma maneira fácil, utilizando código PHP, para definir a estrutura e realizar modificações no banco de dados. Ao invés de informar aos membros do seu time para adicionar manualmente colunas na cópia local do banco de dados, seus colegas podem simplesmente executar as migrations que você enviou ao servidor de controle de versões.

Então, vamos construir uma tabela para armazenar todas as nossas tarefas. O [Artisan](/docs/{{version}}/artisan) pode ser usado para gerar uma variedade de classes e fará você economizar muita digitação conforme seu projeto Laravel é construído. Neste caso, usaremos o comando `make:migration` para gerar uma nova migration para nossa tabela `tasks`:

	php artisan make:migration create_tasks_table --create=tasks

A migration será armazenada no diretório `database/migrations` do seu projeto. Como você pode ter notado, o comando `make:migration` adiciona automaticamente um ID auto-incremental e timestamps ao migration. Vamos editar este arquivo e adicionar uma coluna do tipo `string` para o nome das nossas tarefas:

	<?php

	use Illuminate\Database\Schema\Blueprint;
	use Illuminate\Database\Migrations\Migration;

	class CreateTasksTable extends Migration
	{
	    /**
	     * Run the migrations.
	     *
	     * @return void
	     */
	    public function up()
	    {
	        Schema::create('tasks', function (Blueprint $table) {
	            $table->increments('id');
	            $table->string('name');
	            $table->timestamps();
	        });
	    }

	    /**
	     * Reverse the migrations.
	     *
	     * @return void
	     */
	    public function down()
	    {
	        Schema::drop('tasks');
	    }
	}

Para executar nossa migration, usaremos o comando Artisan `migrate`. Se você está usando o Homestead, você deve executar este comando dentro da virtual machine, uma vez que sua maquina local não terá acesso direta ao banco de dados:

	php artisan migrate

Este comando criará todas as tabelas do banco de dados. Se você inspecionar o banco de dados utilizando um cliente de sua escolha, você verá uma nova tabela `tasks` contendo as colunas definidas em nosso migration. A seguir, estamos prontos para definir um modelo Eloquent para nossas tarefas.

<a name="eloquent-models"></a>
### Modelos Eloquent

[Eloquent](/docs/{{version}}/eloquent) é o ORM (object-relational mapper|mapeamento objeto-relacional) padrão do Laravel. O Eloquent torna fácil obter e gravar dados no banco de dados usando "modelos" bem definidos. Normalmente, cada modelo Eloquent corresponde diretamente a uma única tabela no banco de dados.

Então, vamos definir um modelo `Task` que corresponde a tabela `tasks` que acabamos de criar. Novamente, podemos utilizar um comando Artisan para gerar este modelo. Neste caso, usaremos o comando `make:model`:

	php artisan make:model Task

O modelo será armazenado no diretório `app` da sua aplicação. Por padrão, a classe está vazia. Não precisamos informar explicitamente ao modelo Eloquent qual tabela este modelo corresponde, por que a classe modelo assumirá que o nome da tabela é a forma no plural do seu próprio nome. Neste caso, o modelo `Task` irá assumir que corresponde a tabela `tasks`. Aqui está o que nosso modelo vazio deve parecer:

	<?php

	namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Task extends Model
	{
		//
	}

Iremos aprender mais sobre como utilizar os modelos Eloquent à medida que criamos rotas para nossa aplicação. Para mais informações, fique à vontade para consultar a [documentação completa do Eloquent] (/docs/{{version}}/eloquent).

<a name="routing"></a>
## Roteamento

<a name="stubbing-the-routes"></a>
### Rotas

Estamos prontos para adicionar algumas rotas a nossa aplicação. Rotas são usadas para associar URLs à controladores ou funções anônimas que devem ser executadas quando um usuário acessar a referida página. Por padrão, todas as rotas são definidas no arquivo `app/Http/routes.php`. Este arquivo esta presente em todo novo projeto.

Para esta aplicação, nós sabemos que iremos precisar de ao menos três rotas: um rota para exibir uma lista de todas as nossas tarefas, uma rota para criar uma nova tarefa e uma rota para excluir uma tarefa existente. Vamos criar estas três rotas no arquivo `app/Http/routes.php`:

	<?php

	use App\Task;
	use Illuminate\Http\Request;

	/**
	 * Display All Tasks
	 */
	Route::get('/', function () {
		//
	});

	/**
	 * Add A New Task
	 */
	Route::post('/task', function (Request $request) {
		//
	});

	/**
	 * Delete An Existing Task
	 */
	Route::delete('/task/{id}', function ($id) {
		//
	});
	
<a name="displaying-a-view"></a>
### Exibindo uma Visão

A seguir iremos implementar nossa rota `/`. A partir desta rota, queremos renderizar um template HTML que contenha um formulário para adicionar novas tarefas, e também exibir uma lista de todas as tarefas existentes.

No Laravel, todos o templates HTML são armazenados no diretório `resources/views`, e podemos utilizar o helper `view` para retornar um destes templates a partir da nossa rota.

    Route::get('/', function () {
        return view('tasks');
    });

Claro, devemos definir esta view, então vamos fazer isto!

<a name="building-layouts-and-views"></a>
## Construindo Layouts & Views

Esta aplicação possuí apenas uma visão que contém um formulário para adicionar novas tarefas e também exibir um listagem de todas as tarefas. Para ajudar você a visualizar esta view (visão), aqui está um screenshot da aplicação finalizada, sendo aplicado um estilo básico do Bootstrap CSS.

![Application Image](http://laravel.com/assets/img/quickstart/basic-overview.png)

<a name="defining-the-layout"></a>
### Definindo o Layout
 
Quase todas as aplicações web compartilham o mesmo layout através de suas paginas. Por exemplo, esta aplicação tem uma barra de navegação no topo do layout que estará presente em todas as páginas (se tivermos mais de uma). O Laravel facilita o compartilhamento destas funcionalidades comuns a todas as páginas usando os **layouts** do Blade.

Como discutimos antes, todas as visões do Laravel são armazenadas em `resources/views`. Então, vamos definir um novo layout em `resources/views/layouts/app.blade.php`. A extensão `.blade.php` instrui o framework a usar o [Blade templating engine](/docs/{{version}}/blade) para renderizar a visão. Claro, você pode utilizar templates escritos em PHP puro. Porém, o Blade fornece atalhos para escrever templates mais limpos e concisos.

Nossa visão `app.blade.php` deve ser semelhante com código abaixo:

    // resources/views/layouts/app.blade.php

	<!DOCTYPE html>
	<html lang="en">
		<head>
			<title>Laravel Quickstart - Basic</title>

			<!-- CSS And JavaScript -->
		</head>

		<body>
			<div class="container">
				<nav class="navbar navbar-default">
					<!-- Navbar Contents -->
				</nav>
			</div>

			@yield('content')
		</body>
	</html>

Observe a porção `@yield('content')` do layout. Está é uma diretiva especial do Blade que especifica onde todos as páginas que estenderem o layout  podem injetar seus conteúdos. A seguir, iremos definir um visão que irá utilizar este layout e fornecer seu conteúdo.

<a name="defining-the-child-view"></a>
### Definindo uma Visão Filha

Ótimo, o layout da nossa aplicação está finalizado. Agora devemos definir uma visão que contenha um formulário para criar uma nova tarefa, bem como uma tabela para listar todas as tarefas existentes. Vamos criar esta visão em `resources/views/tasks.blade.php`.

Vamos ignorar o uso do Bootstrap CSS e focar apenas nas coisas que interessam. Lembre-se, você pode baixar o projeto completo para esta aplicação no [GitHub](https://github.com/laravel/quickstart-basic):

    // resources/views/tasks.blade.php

	@extends('layouts.app')

	@section('content')

        <!-- Bootstrap Boilerplate... -->

		<div class="panel-body">
            <!-- Display Validation Errors -->
			@include('common.errors')

			<!-- New Task Form -->
			<form action="/task" method="POST" class="form-horizontal">
				{{ csrf_field() }}

                <!-- Task Name -->
				<div class="form-group">
					<label for="task" class="col-sm-3 control-label">Task</label>

					<div class="col-sm-6">
						<input type="text" name="name" id="task-name" class="form-control">
					</div>
				</div>

                <!-- Add Task Button -->
				<div class="form-group">
					<div class="col-sm-offset-3 col-sm-6">
						<button type="submit" class="btn btn-default">
							<i class="fa fa-plus"></i> Add Task
						</button>
					</div>
				</div>
			</form>
		</div>

		<!-- TODO: Current Tasks -->
	@endsection

#### Algumas Explicações

Antes de continuarmos, vamos falar um pouco mais sobre este template. Primeiro, a diretiva `@extends` informa ao Blade que queremos utilizar o layout definido em `resources/views/layouts/app.blade.php`. Todo o conteúdo entre `@section('content')` e `@endsection` será injetado na localização da diretiva `@yield('contents')` dentro do layout `app.blade.php`.

Agora temos um layout e uma visão básicos para nossa aplicação. Lembre-se, nós estamos retornando esta visão a partir da rota `/`:

	Route::get('/', function () {
		return view('tasks');
	});

Estamos prontos para adicionar algum código em nossa rota `POST /task`, que irá manipular o formulário de entrada de dados e adicionar uma nova tarefa ao banco de dados.

> **Nota:** A diretiva `@include('common.errors')` irá carregar o template localizado em `resources/views/common/errors.blade.php`. Não definimos este template, mas iremos fazê-lo logo!

<a name="adding-tasks"></a>
## Criando um Tarefa

<a name="validation"></a>
### Validação

Agora que temos um formulário em nossa visão, precisamos adicionar código em nossa rota `POST /task` para validar o formulário de entrada e criar uma nova tarefa. Primeiro, vamos validar o formulário de entrada.

Para este formulário, vamos fazer o campo `name` obrigatório e declarar que tal campo precisa ter manos que `255` caracteres. Se a validação falhar, iremos redirecionar o usuário para a URL `/`, e armazenar temporariamente na [sessão](/docs/{{version}}/session) os dados inseridos no input e os erros:

	Route::post('/task', function (Request $request) {
		$validator = Validator::make($request->all(), [
			'name' => 'required|max:255',
		]);

		if ($validator->fails()) {
			return redirect('/')
				->withInput()
				->withErrors($validator);
		}

		// Create The Task...
	});


#### A variável `$errors`

Vamos parar por um momento e conversar sobre a porção `->withErrors($validator)` deste exemplo. A chamada do método `->withErrors($validator)` irá armazenar temporariamente na sessão os erros da instância do validator, assim eles poderão ser acessados pela variável `$errors` em nossa visão.

Lembre-se que usamos a diretiva `@include('common.errors')` dentro da nossa visão para renderizar os erros de validação do formulário. O `common.errors` permitirá exibir facilmente os erros de validação utilizando o mesmo formato em toda as páginas. Vamos definir o conteúdo desta visão agora:

    // resources/views/common/errors.blade.php

    @if (count($errors) > 0)
        <!-- Form Error List -->
        <div class="alert alert-danger">
            <strong>Whoops! Something went wrong!</strong>

            <br><br>

            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

> **Nota:** A variável `$errors` está disponível em **todas** as visões do Laravel. Será apenas uma instância vazia de `ViewErrorBag` se nenhum erro de validação estiver presente.

<a name="creating-the-task"></a>
### Criando um Tarefa

Agora que cuidamos da validação, vamos criar uma nova tarefa continuando a preencher nossa rota. Uma vez que a nova tarefa esteja criada, redirecionaremos o usuários para a URL `/`. Para criar a tarefa, podemos usar o método `save` após criar e definir as propriedades no novo modelo Eloquent.

	Route::post('/task', function (Request $request) {
		$validator = Validator::make($request->all(), [
			'name' => 'required|max:255',
		]);

		if ($validator->fails()) {
			return redirect('/')
				->withInput()
				->withErrors($validator);
		}

		$task = new Task;
		$task->name = $request->name;
		$task->save();

		return redirect('/');
	});

Ótimo! Agora podemos criar tarefas. Vamos continuar melhorando nossa visão através da construção da listagem de todas as tarefas existentes.

<a name="displaying-existing-tasks"></a>
### Exibindo Tarefas Existentes

Primeiro, precisamos editar nossa rota `/` para passar todas as tarefas existentes para a visão. A função `view` aceita um array de dados como segundo argumento. Este array está disponível para a visão, onde cada chave do array se tornará uma variável dentro da visão:

	Route::get('/', function () {
		$tasks = Task::orderBy('created_at', 'asc')->get();

		return view('tasks', [
			'tasks' => $tasks
		]);
	});

Uma vez passado os dados, podemos iterar sobre o array de tarefas na visão `tasks.blade.php` e exibi-las em uma tabela. A diretiva `@foreach` do Blade nos permite escrever loops de forma concisa. Estes loops serão transformados para código PHP puro e rápido:

	@extends('layouts.app')

	@section('content')
        <!-- Create Task Form... -->

        <!-- Current Tasks -->
        @if (count($tasks) > 0)
            <div class="panel panel-default">
                <div class="panel-heading">
                    Current Tasks
                </div>

                <div class="panel-body">
                    <table class="table table-striped task-table">

                        <!-- Table Headings -->
                        <thead>
                            <th>Task</th>
                            <th>&nbsp;</th>
                        </thead>

                        <!-- Table Body -->
                        <tbody>
                            @foreach ($tasks as $task)
                                <tr>
                                    <!-- Task Name -->
                                    <td class="table-text">
                                        <div>{{ $task->name }}</div>
                                    </td>

                                    <td>
                                        <!-- TODO: Delete Button -->
                                    </td>
                                </tr>
                            @endforeach
                        </tbody>
                    </table>
                </div>
            </div>
        @endif
	@endsection

Nossa aplicação está quase completa. Ainda não temos como apagar um tarefa existente. Vamos criar isto!

<a name="deleting-tasks"></a>
## Apagando Tarefas

<a name="adding-the-delete-button"></a>
### Adicionando o botão de Apagar

Deixamos uma nota de "TODO" em nosso código onde nosso botão de apagar deverá estar. Vamos adicionar um botão de apagar para cada linha da nossa lista de tarefa na visão `tasks.blade.php`. Criaremos um pequeno formulário contendo apenas um botão para cada tarefa da lista. Quando clicado, uma requisição `DELETE /task` será enviada para a aplicação:

    <tr>
        <!-- Task Name -->
        <td class="table-text">
            <div>{{ $task->name }}</div>
        </td>

        <!-- Delete Button -->
        <td>
            <form action="/task/{{ $task->id }}" method="POST">
                {{ csrf_field() }}
                {{ method_field('DELETE') }}

                <button>Delete Task</button>
            </form>
        </td>
    </tr>

<a name="a-note-on-method-spoofing"></a>
#### Nota sobre Falsificação de Métodos

Note que o método do formulário para apagar uma tarefa aparece como `POST`, ainda assim estamos respondendo esta requisição utilizando a rota `Route::delete`. Formulário HTML permitem apenas os verbos HTTP `GET` e `POST`, então precisamos uma maneira de falsificar uma requisição `DELETE` a partir do formulário.

Podemos falsificar a requisição `DELETE` inserindo o resultado da função `method_field('DELETE')` dentro do formulário. Esta função gera um campo hidden que o Laravel reconhece e usará para sobreescrever o método da requisição atual. O campo hidden gerado pelo método será algo como:

	<input type="hidden" name="_method" value="DELETE">

<a name="deleting-the-task"></a>
### Apagando a Tarefa

Finalmente, vamos adicionar a lógica à nossa rota para realmente apagar a tarefa. Podemo utilizar o método `findOrFail` do Eloquent para obter um modelo pelo seu ID ou lançar um exceção caso o modelo não exista. Uma vez que o modelo foi obtido, usaremos o método `delete` para apagar o registro. Quando o registro for apagado, redirecionaremos o usuário para a URL `/`:

	Route::delete('/task/{id}', function ($id) {
		Task::findOrFail($id)->delete();

		return redirect('/');
	});
    
