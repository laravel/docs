# Banco de dados: Introdução

- [Introdução](#introduction)
- [Rodando SQL puro](#running-queries)
	- [Listening For Query Events](#listening-for-query-events)
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
Neste arquivo você define todas as suas conexões de banco de dados e especificar qual a sua conexão padrão. Exemplos para todos os banco de dados suportados estão nesse arquivo.

Por padrão, Laravel's sample [environment configuration](/docs/{{version}}/installation#environment-configuration) vem pronto para uso com [Laravel Homestead](/docs/{{version}}/homestead), que é uma máquina virtual para desenvolvimento local com laravel. É claro, que você é livre para modificar a configuração para atender suas necessidades.

<a name="read-write-connections"></a>
#### Conexões para Leitura / Escrita

As vezes você pode querer usar um conexão para instruções SELECT, outra para insert, update e delete.
Laravel torna isso suave, as conexões apropriadas são chamadas quando você utiliza SQL puro, query builder ou o Eloquent ORM.

Para entender como são configuradas as  conexões  read / write, vamos a um exemplo:

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

Veja que temos duas chave adicionada ao nosso array: `read` e `write`. Ambas contém uma chave com o nome: `host`. Os demais dados para a conexão serão mesclados com array principal `mysql`.

Então, só precisamos adicionar as chaves, `read` e `write` se queremos substituir os dados da matriz(array) principal. Dessa forma, neste caso, `192.168.1.1` é usado para conexçoes de leitura(read), enquanto `192.168.1.2` é usado para conexões de escrita(write). As credenciais do banco de dados, prefixo, character set, e todas as outras opções da matriz(array) `mysql` serão compartilhadas entre as duas conexões.

<a name="running-queries"></a>
## Rodando SQL puras

Depois da sua conexão estiver configurada, você pode executar consultas usando facade `DB`. O `DB` facade fornece métodos para cada tipo de consulta: `select`, `update`, `insert` e `statement`.

#### Rodando uma query SQL

Para rodar uma query básica, nós podemos usar o método `select` do facade `DB`:

	<?php namespace App\Http\Controllers;

	use DB;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Show a list of all of the application's users.
		 *
		 * @return Response
		 */
		public function index()
		{
			$users = DB::select('select * from users where active = ?', [1]);

			return view('user.index', ['users' => $users]);
		}
	}

O primeiro argumento passado para o método `select` é o sql puro, enquanto o segundo argumento é uma matriz de valores a serem ligados com o SQL. Normalmente esses valores são restrições da cláusula `where`. Parâmetros linkados com a query são protegidos contra SQL Injection.

O método `select` sempre retorna uma matriz(array) de resultados. Cada resultado dentro da matriz(array) será um objeto da classe PHP `StdClass`, permitindo que você acesse o resultado dos valores:

	foreach ($users as $user) {
		echo $user->name;
	}

#### Usando nomes de link

Instead of using `?` to represent your parameter bindings, you may execute a query using named bindings:

	$results = DB::select('select * from users where id = :id', ['id' => 1]);

#### Running An Insert Statement

To execute an `insert` statement, you may use the `insert` method on the `DB` facade. Like `select`, this method takes the raw SQL query as its first argument, and bindings as the second argument:

	DB::insert('insert into users (id, name) values (?, ?)', [1, 'Dayle']);

#### Running An Update Statement

The `update` method should be used to update existing records in the database. The number of rows affected by the statement will be returned by the method:

	$affected = DB::update('update users set votes = 100 where name = ?', ['John']);

#### Running A Delete Statement

The `delete` method should be used to delete records from the database. Like `update`, the number of rows deleted will be returned:

	$deleted = DB::delete('delete from users');

#### Running A General Statement

Some database statements should not return any value. For these types of operations, you may use the `statement` method on the `DB` facade:

	DB::statement('drop table users');

<a name="listening-for-query-events"></a>
### Listening For Query Events

If you would like to receive each SQL query executed by your application, you may use the `listen` method. This method is useful for logging queries or debugging. You may register your query listener in a [service provider](/docs/{{version}}/providers):

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

To run a set of operations within a database transaction, you may use the `transaction` method on the `DB` facade. If an exception is thrown within the transaction `Closure`, the transaction will automatically be rolled back. If the `Closure` executes successfully, the transaction will automatically be committed. You don't need to worry about manually rolling back or committing while using the `transaction` method:

	DB::transaction(function () {
		DB::table('users')->update(['votes' => 1]);

		DB::table('posts')->delete();
	});

#### Manually Using Transactions

If you would like to begin a transaction manually and have complete control over rollbacks and commits, you may use the `beginTransaction` method on the `DB` facade:

	DB::beginTransaction();

You can rollback the transaction via the `rollBack` method:

	DB::rollBack();

Lastly, you can commit a transaction via the `commit` method:

	DB::commit();

> **Note:** Using the `DB` facade's transaction methods also controls transactions for the [query builder](/docs/{{version}}/queries) and [Eloquent ORM](/docs/{{version}}/eloquent).

<a name="accessing-connections"></a>
## Usando Multiplas conexões

When using multiple connections, you may access each connection via the `connection` method on the `DB` facade. The `name` passed to the `connection` method should correspond to one of the connections listed in your `config/database.php` configuration file:

	$users = DB::connection('foo')->select(...);

You may also access the raw, underlying PDO instance using the `getPdo` method on a connection instance:

	$pdo = DB::connection()->getPdo();
