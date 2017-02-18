# Banco de dados: Introdução

- [Introdução](#introduction)
- [Rodando SQL puro](#running-queries)
	- [Escutando eventos de consulta (Query Events)](#listening-for-query-events)
- [Transações](#database-transactions)
- [Usando conexões múltiplas](#accessing-connections)

<a name="introduction"></a>
## Introdução

Laravel faz com que a consulta e a conexão com banco de dados sejam tarefas extremamente simples
e com uma variedade de banco dados utilizando SQL puro, o [fluent query builder](/docs/{{version}}/queries), e o [Eloquent ORM](/docs/{{version}}/eloquent).
Atualmente, Laravel contém suporte a quatro sistema de banco de dados:

- MySQL
- Postgres
- SQLite
- SQL Server

<a name="configuration"></a>
### Configuração

A configuração do banco de dados para sua aplicação está localizada em `config/database.php`. 
Neste arquivo você define todas as suas conexões de banco de dados e especificar qual a sua conexão padrão. Exemplos para todos os bancos de dados suportados estão nesse arquivo.

Por padrão, um exemplo [environment configuration](/docs/{{version}}/installation#environment-configuration) vem pronto para uso com [Laravel Homestead](/docs/{{version}}/homestead), que é uma máquina virtual para desenvolvimento local com laravel. É claro, que você é livre para modificar a configuração para atender suas necessidades.

<a name="read-write-connections"></a>
#### Conexões para Leitura / Escrita

As vezes você pode querer usar um conexão para instruções SELECT, outra para insert, update e delete.
Laravel torna isso suave, as conexões apropriadas são chamadas quando você utiliza SQL puro, query builder ou o Eloquent ORM.

Para entender como são configuradas as conexões de leitura / escrita, vamos a um exemplo:

	'mysql' => [
		'read' => [
			'host' => '192.168.1.1',
		],
		'write' => [
			'host' => '196.168.1.2'
		],
		'driver'    => 'mysql',
		'database'  => 'database',
		'username'  => 'root',
		'password'  => '',
		'charset'   => 'utf8',
		'collation' => 'utf8_unicode_ci',
		'prefix'    => '',
	],

Veja que temos duas chaves adicionadas ao nosso array: `read` e `write`. Ambas contém uma chave com o nome: `host`. Os demais dados para a conexão serão mesclados com array principal `mysql`.

Então, só precisamos adicionar as chaves, `read` e `write` se queremos substituir os dados da matriz (array) principal. Dessa forma, neste caso, `192.168.1.1` é usado para conexões de leitura (read), enquanto `192.168.1.2` é usado para conexões de escrita (write). As credenciais do banco de dados, prefixo, character set, e todas as outras opções da matriz (array) `mysql` serão compartilhadas entre as duas conexões.

<a name="running-queries"></a>
## Rodando instruções puras

Depois da sua conexão estiver configurada, você pode executar consultas usando a fachada `DB`. A fachada `DB` fornece métodos para cada tipo de consulta: `select`, `update`, `insert` e `statement`.

#### Rodando uma consulta SQL

Para rodar uma consulta básica, nós podemos usar o método `select` na fachada `DB`:

	<?php namespace App\Http\Controllers;

	use DB;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Exibir uma lista de todos os usuários da aplicação.
		 *
		 * @return Response
		 */
		public function index()
		{
			$users = DB::select('select * from users where active = ?', [1]);

			return view('user.index', ['users' => $users]);
		}
	}

O primeiro argumento passado para o método `select` é a consulta pura, enquanto o segundo argumento é uma matriz de valores a serem ligados com o SQL. Normalmente esses valores são restrições da cláusula `where`. Parâmetros linkados com a query são protegidos contra `SQL Injection`.

O método `select` sempre retorna uma matriz (array) de resultados. Cada resultado dentro da matriz (array) será um objeto da classe PHP `StdClass`, permitindo que você acesse o resultado dos valores:

	foreach ($users as $user) {
		echo $user->name;
	}

#### Usando nomes de link

Ao invés de utilizar `?` para representar sua ligação de parâmetros, você pode executar a consulta usando uma ligação por nome.

	$results = DB::select('select * from users where id = :id', ['id' => 1]);

#### Inserindo dados

Para executar um `insert`, você pode usar o método `insert` existente na fachada `DB`. Assim como o `select`, este método pega o SQL puro como seu primeiro parâmetro e ligações como segundo parâmetro. 

	DB::insert('insert into users (id, name) values (?, ?)', [1, 'Dayle']);

#### Atualizando dados

O método `update` deve ser utilizado para atualizar registros existentes no banco de dados. O número de linhas afetadas pela `query` será retornado pelo método:

	$affected = DB::update('update users set votes = 100 where name = ?', ['John']);

#### Removendo dados

O método `delete` deve ser usado para remover registros do banco de dados. Assim com o `update`, o número de linhas deletadas será retornado pelo método:

	$deleted = DB::delete('delete from users');

#### Executando instruções genéricas

Algumas instruções no banco de dados não devem retornar nenhum valor. Para esse tipo de operação, você pode utilizar o método `statement` na fachada `DB`:

	DB::statement('drop table users');

<a name="listening-for-query-events"></a>
### Escutando eventos de consulta (Query Events)

Se você gostaria de receber cada consulta SQL executada pela sua aplicação, você pode usar o método `listen`. Este método é útil para logar as consultas ou debuga-las. Você pode registrar sua escuta de eventos em um [service provider](/docs/{{version}}/providers):

	<?php namespace App\Providers;

	use DB;
	use Illuminate\Support\ServiceProvider;

	class AppServiceProvider extends ServiceProvider
	{
		/**
		 * Bootstrap any application services.
		 *
		 * @return void
		 */
		public function boot()
		{
			DB::listen(function($sql, $bindings, $time) {
				//
			});
		}

		/**
		 * Register the service provider.
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}
	}

<a name="database-transactions"></a>
## Transações 

Para executar um conjunto de operações dentro de uma transação com o banco de dados, você pode utilizar o método `transaction` na fachada `DB`. Se uma `exception` for gerada dentro de uma transação `Closure`, a transação será automaticamente revertida. Você não precisa se preocupar em fazer a reversão (rollback) ou a confirmação (commit) manualmente enquanto estiver usando o método `transaction`.

	DB::transaction(function () {
		DB::table('users')->update(['votes' => 1]);

		DB::table('posts')->delete();
	});

#### Usando Transações Manualmente

Se você gostaria de começar uma transação manualmente e ter controle completo sobre as reversões (rollbacks) e confirmações (commits), você pode utilizar o método `beginTransaction` na fachada `DB`:

	DB::beginTransaction();

Você pode reverter a transação pelo método de `rollBack`:

	DB::rollBack();

Por último, você pode confirmar a transação pelo método de `commit`:

	DB::commit();

> **Observação:** Os métodos de transação da fachada `DB` também controlam as transações do [query builder](/docs/{{version}}/queries) e do [Eloquent ORM](/docs/{{version}}/eloquent).

<a name="accessing-connections"></a>
## Usando Múltiplas conexões

Quando estiver utilizando múltiplas conexões, você poderá acessar cada conexão pelo método `connection` na fachada `DB`. O `name` passado para a o método `connection` deve ser correspondente a um que esteja listado em seu arquivo de configurações `config/database.php`:

	$users = DB::connection('foo')->select(...);

Você pode também acessar a instância subjacente crua do PDO utilizando o método `getPdo` na sua instância de conexão:

	$pdo = DB::connection()->getPdo();
