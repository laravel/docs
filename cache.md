# Cache

<<<<<<< HEAD
- [Configuration](#configuration)
- [Cache Usage](#cache-usage)
- [Increments & Decrements](#increments-and-decrements)
- [Cache Tags](#cache-tags)
- [Cache Events](#cache-events)
- [Database Cache](#database-cache)
- [Memcached Cache](#memcached-cache)
- [Redis Cache](#redis-cache)
=======
- [Configuração](#configuration)
- [Uso do Cache](#cache-usage)
- [Incrementação & Decrementação](#increments-and-decrements)
- [Marcações de Cache](#cache-tags)
- [Cache no banco de dados](#database-cache)
>>>>>>> 5.0

<a name="configuration"></a>
## Configuração

O Laravel fornece uma API unificada para vários sistemas de cache. A configuração do cache do laravel fica em `config/cache.php`. Neste arquivo você pode especificar o driver que você gostaria de usar por padrão em toda a sua aplicação. O Laravel suporta ferramentas como [Memcached](http://memcached.org) e [Redis](http://redis.io).

O arquivo de configuração do cache também contém várias outras opções, que são documentadas dentro do arquivo. Sendo assim, certifique-se de ler estas opções. Por padrão, o Laravel é configurado para usar o drive `file`, que armazena objetos serializados no sistema de arquivos. Para grandes aplicações, recomenda-se que você utilize uma cache de in-memory(Verificar esse termo) como Memcached ou APC. Você pode ter várias configurações de cache para o mesmo driver.

Antes de usar o Redis com o Laravel, vc precisará instalar o pacote `predis/predis` (~1.0) via Composer.

<a name="cache-usage"></a>
## Uso do Cache

#### Gravando um item no Cache

	Cache::put('key', 'value', $minutes);

#### Usando objetos do Carbon para a expiração

	$expiresAt = Carbon::now()->addMinutes(10);

	Cache::put('key', 'value', $expiresAt);

#### Gravando um item no Cache caso ele não exista

	Cache::add('key', 'value', $minutes);
O método `add` retornará `true` se o item foi realmente **adicionado** para o cache. Caso contrário, retornará `false`.

#### Verificando se um Cache existe

	if (Cache::has('key'))
	{
		//
	}

#### Recuperando um item do Cache

	$value = Cache::get('key');

#### Recuperando um item ou retornando um valor default

	$value = Cache::get('key', 'default');

	$value = Cache::get('key', function() { return 'default'; });

#### Gravando um item no Cache permanentemente

	Cache::forever('key', 'value');

Algumas vezes você pode querer recuperar um item do cache, mas também armazenar um valor default se o item requisitado não existir. Você pode fazer isto utilizando o método `Cache::remember`:

	$value = Cache::remember('users', $minutes, function()
	{
		return DB::table('users')->get();
	});

Você também pode combinar os métodos `remember` e `forever`:

	$value = Cache::rememberForever('users', function()
	{
		return DB::table('users')->get();
	});

Note que todos os itens gravados no cache são serializados, neste caso, você fica livre para armazenar qualquer tipo de dado.

#### Puxando um item do Cache

Se você precisar recuperar um item do cache e, em seguida, deletá-lo, você pode usar o método `pull`:

	$value = Cache::pull('key');

#### Removendo um item do Cache

	Cache::forget('key');

#### Access Specific Cache Stores

When using multiple cache stores, you may access them via the `store` method:

	$value = Cache::store('foo')->get('key');

<a name="increments-and-decrements"></a>
## Incrementando & Desincrementando

Todos os drivers, exceto `file` e `database`, suportam as operações `increment` e `decrement`:

#### Incrementando um valor

	Cache::increment('key');

	Cache::increment('key', $amount);

#### Desincrementando um valor

	Cache::decrement('key');

	Cache::decrement('key', $amount);

<a name="cache-tags"></a>
## Marcações de Cache

> **Nota:** As marcações de cache, não são suportadas quando se usam os drivers `file` ou `database`. Além disso, quando usamos várias marcações em caches que são armazenados "para sempre", o desempenho será melhor com um driver como `memcached`, que limpa automaticamente registros obsoletos.

#### Acessando um Cache com uma marcação

As marcações, permitem que você marque os items relacionados ao cache, em seguida, limpe todos os caches marcados com um nome dado. Para acessar um cache marcado, use o método `tags`.

Você pode armazenar um cache passando um array dos nomes das marcações como argumentos ou como um array com os nomes das marcações:

	Cache::tags('people', 'authors')->put('John', $john, $minutes);

	Cache::tags(['people', 'artists'])->put('Anne', $anne, $minutes);

Você pode usar qualquer método de armazenamento de cache em combinação com as marcações, incluindo `remember`, `forever` e `rememberForever`. Você também pode acessar itens que estão no cache oriundos das marcações de cache, também pode usar outros métodos de cache como `increment` e `decrement`. 

#### Acessando items em um Cache marcado

Para acessar um cache marcado, passe o array das tags usadas anteriormente para armazenar.

	$anne = Cache::tags('people', 'artists')->get('Anne');

	$john = Cache::tags(['people', 'authors'])->get('John');

Você pode limpar todos os itens marcados com um nome ou array de nomes. Por exemplo, nesta declaração removeremos todas as marcações de cache com  `people`, `author` ou ambos. Então, "Anne" e "John" seriam removidos do cache:

	Cache::tags('people', 'authors')->flush();

Sendo assim, este outro código removerá somente caches marcados com `authors`. Então "John" será removido, mas "Anne", não.

	Cache::tags('authors')->flush();

<a name="cache-events"></a>
## Cache Events

To execute code on every cache operation, you may listen for the events fired by the cache:

	Event::listen('cache.hit', function($key, $value) {
		//
	});

	Event::listen('cache.missed', function($key) {
		//
	});

	Event::listen('cache.write', function($key, $value, $minutes) {
		//
	});

	Event::listen('cache.delete', function($key) {
		//
	});

<a name="database-cache"></a>
## Cache do banco de dados

Quando usar o drive de cache `database` , você precisará configurar uma tabela no que contém os itens do cache. Veja um exemplo `Schema` abaixo:

	Schema::create('cache', function($table)
	{
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});

<a name="memcached-cache"></a>
#### Memcached Cache

Using the Memcached cache requires the [Memcached PECL package](http://pecl.php.net/package/memcached) to be installed.

The default [configuration](#configuration) uses TCP/IP based on [Memcached::addServer](http://php.net/manual/en/memcached.addserver.php):

	'memcached' => array(
		array('host' => '127.0.0.1', 'port' => 11211, 'weight' => 100),
	),

You may also set the `host` option to a UNIX socket path. If you do this, the `port` option should be set to `0`:

	'memcached' => array(
		array('host' => '/var/run/memcached/memcached.sock', 'port' => 0, 'weight' => 100),
	),

<a name="redis-cache"></a>
#### Redis Cache

See [Redis Configuration](/docs/redis#configuration)
