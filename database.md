# Utilização básica do banco de dados

- [Configuração](#configuration)
- [Conexões de Leitura / Escrita](#read-write-connections)
- [Executando consultas](#running-queries)
- [Transações de banco de dados](#database-transactions)
- [Acessando conexões](#accessing-connections)
- [Log de consultas](#query-logging)

<a name="configuration"></a>
## Configuração

O Laravel se conecta com banco de dados e executa consultas de forma extremamente simples. O arquivo de configuração é o `config/database.php`. Neste arquivo, você pode definir todas as suas conexões com os bancos de dados, e também especificar a conexão padrão. Neste arquivo, você encontra exemplos para se conectar com todos os bancos suportados.

Atualmente, o Laravel suporta quatro sistemas de bancos de dados: MySQL, Postgres, SQLite, e SQL Server.

<a name="read-write-connections"></a>
## Conexões de Leitura / Escrita

As vezes, você deseja usar uma conexão do banco de dados para comandos SELECT, e uma para comandos INSERT, UPDATE, e DELETE. O Laravel torna isso possível, e as devidas conexões serão sempre usadas, esteja você usando "raw queries", o "query builder", ou o ORM Eloquent.

Para ver como conexões de leitura / escrita devem ser configuradas, dê uma olhada neste exemplo:

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

Observe que duas chaves foram adicionadas ao array de configuração: `read` e `write` (leitura e escrita). Essas duas chaves possuem valores de array contendo uma única chave: `host`. O resto das opções do banco de dados para conexões de`read` e `write` serão mescladas como array principal `mysql`. Então, nós so precisamos colocar itens nos arrays `read` e `write` se quisermos sobrescrever os valores do array principal. Então, neste casi, `192.168.1.1` será usado para a coneXão "read", enquanto `192.168.1.2` será usado para a conexão "write". As credeciais do banco de dados, o prefixo, conjunto de caracteres, e todas as outras opções do array proincipal `mysql`serão compartilhadas entre as duas conexões.

<a name="running-queries"></a>
## Executando consultas

Uma vez configurada sua conexão com o banco de dados, você pode executar consultas com a facade `DB`.

#### Execuntando uma consultas Select

	$results = DB::select('select * from users where id = ?', [1]);

O métodos `select` sempre retornará um `array` de resultados.

You may also execute a query using named bindings:

	$results = DB::select('select * from users where id = :id', ['id' => 1]);

#### Executando uma consulta Insert

	DB::insert('insert into users (id, name) values (?, ?)', [1, 'Dayle']);

#### Executando uma consulta Update

	DB::update('update users set votes = 100 where name = ?', ['John']);

#### Executando uma consulta Delete

	DB::delete('delete from users');

> **Observação:** Os comandos `update` e `delete` retornam o número de linhas afetadas pela operação.

#### Executando um comando geral

	DB::statement('drop table users');

#### "Escutando" eventos de consulta

Você pode escutar eventos de consultas usando o método `DB::listen`:

	DB::listen(function($sql, $bindings, $time)
	{
		//
	});

<a name="database-transactions"></a>
## Transações no banco de dados

Para executar uma série de operação com uma transação de banco de dados, você pode usar o método `transaction`:

	DB::transaction(function()
	{
		DB::table('users')->update(['votes' => 1]);

		DB::table('posts')->delete();
	});

> **Obsevação:** Qualquer exceção lançada na closure `transaction` irá provocar um rollback na transação automaticamente.

As vezes, você mesmo pode precisar iniciar a transação:

	DB::beginTransaction();

Você pode fazer um rollback na transação usando o método `rollback`:

	DB::rollback();

Finalmente, você pode fazer um commit na transação transaction com o método `commit`:

	DB::commit();

<a name="accessing-connections"></a>
## Acessando conexões

Quando usar múltiplas conexões, você pode acessá-las com o método `DB::connection`:

	$users = DB::connection('foo')->select(...);

Você pode acessar diretamente a instância PDO da conexão:

	$pdo = DB::connection()->getPdo();

Às vezes você pode precisar se reconectar a um banco de dados:

	DB::reconnect('foo');

Se você precisar se desconectar de um banco de dados por ter excedido o limite de instâncias PDO (`max_connections`), use o métoddo `disconnect`:

	DB::disconnect('foo');

<a name="query-logging"></a>
## Logando consultas

Laravel can optionally log in memory all queries that have been run for the current request. Be aware that in some cases, such as when inserting a large number of rows, this can cause the application to use excess memory. To enable the log, you may use the `enableQueryLog` method:

	DB::connection()->enableQueryLog();

por padrão, o Laravel mantém um log na memória de todas as counsultas que foram executadas na requisição atual. No entanto, em alguns casos, como por exemplo quando inserindo uma grande quantidade de registros, isso pode fazer com que a aplicação use memória em excesso. Para desabilitar o log, você pode usar o método `disableQueryLog`:

Para obter um array de consultas já executadas, você pode usa ro método `getQueryLog`:

	$queries = DB::getQueryLog();
