# Cache

- [Configuração](#configuration)
- [Uso do Cache](#cache-usage)
	- [Obtendo uma Instância do Cache](#obtaining-a-cache-instance)
	- [Recuperando Itens do Cache](#retrieving-items-from-the-cache)
	- [Armazenando Itens no Cache](#storing-items-in-the-cache)
	- [Removendo Itens do Cache](#removing-items-from-the-cache)
- [Adicionando Drivers Customizados](#adding-custom-cache-drivers)

<a name="configuration"></a>
## Configuração


O Laravel fornece uma API unificada para vários sistemas de cache. A configuração do cache do laravel fica em `config/cache.php`. Neste arquivo você pode especificar o driver que você gostaria de usar por padrão em toda a sua aplicação. O Laravel suporta ferramentas como [Memcached](http://memcached.org) e [Redis](http://redis.io) de uma maneira massa.

O arquivo de configuração do cache também contém várias outras opções que são documentadas dentro do arquivo, sendo assim, certifique-se de ler estas opções. Por padrão, o Laravel é configurado para usar o drive `file`, que armazena objetos serializados no sistema de arquivos. Para grandes aplicações, recomenda-se que você utilize um in-memory cache como Memcached ou APC. Você pode ter várias configurações de cache para o mesmo driver.

### Pré-requisitos do Cache

#### Banco de dados

Quando estiver usando o drive `database`, você precisará criar uma tabela para os itens do cachê. Aqui temos um exemplo de `Schema` para a tabela:

	Schema::create('cache', function($table) {
		$table->string('key')->unique();
		$table->text('value');
		$table->integer('expiration');
	});

#### Memcached

Usar o cache do Memcached requer a instalação do [pacote Memcached PECL](http://pecl.php.net/package/memcached)

A [configuração](#configuration) padrão usa [Memcached::addServer](http://php.net/manual/en/memcached.addserver.php) baseado em TCP/IP:

	'memcached' => [
		[
			'host' => '127.0.0.1',
			'port' => 11211,
			'weight' => 100
		],
	],

Você pode também setar a opção `host` para um caminho de socket UNIX. Se você fizer isto, a opção `port` deveria ser setada como `0`:

	'memcached' => [
		[
			'host' => '/var/run/memcached/memcached.sock',
			'port' => 0,
			'weight' => 100
		],
	],

#### Redis

Para usar um cache de Redis no Laravel, você precisa instalar o pacote `predis/predis` (~1.0) via Composer.

Para mais informações sobre como configurar o Redis, consulte esta [Página da Documentação do Laravel](/docs/{{version}}/redis#configuration).

<a name="cache-usage"></a>
## Uso do Cache

<a name="obtaining-a-cache-instance"></a>
### Obtendo uma instância do Cache

O `Illuminate\Contracts\Cache\Factory` and `Illuminate\Contracts\Cache\Repository` [contracts](/docs/{{version}}/contracts) provide access to Laravel's cache services. The `Factory` contract provides access to all cache drivers defined for your application. The `Repository` contract is typically an implementation of the default cache driver for your application as specified by your `cache` configuration file.

However, you may also use the `Cache` facade, which is what we will use throughout this documentation. The `Cache` facade provides convenient, terse access to the underlying implementations of the Laravel cache contracts.

For example, let's import the `Cache` facade into a controller:

	<?php namespace App\Http\Controllers;

	use Cache;
	use Illuminate\Routing\Controller;

	class UserController extends Controller
	{
		/**
		 * Show a list of all users of the application.
		 *
		 * @return Response
		 */
		public function index()
		{
			$value = Cache::get('key');

			//
		}
	}

#### Accessing Multiple Cache Stores

Using the `Cache` facade, you may access various cache stores via the `store` method. The key passed to the `store` method should correspond to one of the stores listed in the `stores` configuration array in your `cache` configuration file:

	$value = Cache::store('file')->get('foo');

	Cache::store('redis')->put('bar', 'baz', 10);

<a name="retrieving-items-from-the-cache"></a>
### Retrieving Items From The Cache

The `get` method on the `Cache` facade is used to retrieve items from the cache. If the item does not exist in the cache, `null` will be returned. If you wish, you may pass a second argument to the `get` method specifying the custom default value you wish to be returned if the item doesn't exist:

	$value = Cache::get('key');

	$value = Cache::get('key', 'default');


You may even pass a `Closure` as the default value. The result of the `Closure` will be returned if the specified item does not exist in the cache. Passing a Closure allows you to defer the retrieval of default values from a database or other external service:

	$value = Cache::get('key', function() {
		return DB::table(...)->get();
	});

#### Checking For Item Existence

The `has` method may be used to determine if an item exists in the cache:

	if (Cache::has('key')) {
		//
	}

#### Incrementing / Decrementing Values

The `increment` and `decrement` methods may be used to adjust the value of integer items in the cache. Both of these methods optionally accept a second argument indicating the amount by which to increment or decrement the item's value:

	Cache::increment('key');

	Cache::increment('key', $amount);

	Cache::decrement('key');

	Cache::decrement('key', $amount);

#### Retrieve Or Update

Sometimes you may wish to retrieve an item from the cache, but also store a default value if the requested item doesn't exist. For example, you may wish to retrieve all users from the cache or, if they don't exist, retrieve them from the database and add them to the cache. You may do this using the `Cache::remember` method:

	$value = Cache::remember('users', $minutes, function() {
		return DB::table('users')->get();
	});

If the item does not exist in the cache, the `Closure` passed to the `remember` method will be executed and its result will be placed in the cache.

You may also combine the `remember` and `forever` methods:

	$value = Cache::rememberForever('users', function() {
		return DB::table('users')->get();
	});

#### Retrieve And Delete

If you need to retrieve an item from the cache and then delete it, you may use the `pull` method. Like the `get` method, `null` will be returned if the item does not exist in the cache:

	$value = Cache::pull('key');

<a name="storing-items-in-the-cache"></a>
### Storing Items In The Cache

You may use the `set` method on the `Cache` facade to store items in the cache. When you place an item in the cache, you will need to specify the number of minutes for which the value should be cached:

	Cache::put('key', 'value', $minutes);

Instead of passing the number of minutes until the item expires, you may also pass a PHP `DateTime` instance representing the expiration time of the cached item:

	$expiresAt = Carbon::now()->addMinutes(10);

	Cache::put('key', 'value', $expiresAt);

The `add` method will only add the item to the cache if it does not already exist in the cache store. The method will return `true` if the item is actually added to the cache. Otherwise, the method will return `false`:

	Cache::add('key', 'value', $minutes);

The `forever` method may be used to store an item in the cache permanently. These values must be manually removed from the cache using the `forget` method:

	Cache::forever('key', 'value');

<a name="removing-items-from-the-cache"></a>
### Removing Items From The Cache

You may remove items from the cache using the `forget` method on the `Cache` facade:

	Cache::forget('key');

<a name="adding-custom-cache-drivers"></a>
## Adding Custom Cache Drivers

To extend the Laravel cache with a custom driver, we will use the `extend` method on the `Cache` facade, which is used to bind a custom driver resolver to the manager. Typically, this is done within a [service provider](/docs/{{version}}/providers).

For example, to register a new cache driver named "mongo":

	<?php namespace App\Providers;

	use Cache;
	use App\Extensions\MongoStore;
	use Illuminate\Support\ServiceProvider;

	class CacheServiceProvider extends ServiceProvider
	{
		/**
		 * Perform post-registration booting of services.
		 *
		 * @return void
		 */
		public function boot()
		{
			Cache::extend('mongo', function($app) {
				return Cache::repository(new MongoStore);
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

The first argument passed to the `extend` method is the name of the driver. This will correspond to your `driver` option in the `config/cache.php` configuration file. The second argument is a Closure that should return an `Illuminate\Cache\Repository` instance. The Closure will be passed an `$app` instance, which is an instance of the [service container](/docs/{{version}}/container).

The call to `Cache::extend` could be done in the `boot` method of the default `App\Providers\AppServiceProvider` that ships with fresh Laravel applications, or you may create your own service provider to house the extension - just don't forget to register the provider in the `config/app.php` provider array.

To create our custom cache driver, we first need to implement the `Illuminate\Contracts\Cache\Store` [contract](/docs/{{version}}/contracts) contract. So, our MongoDB cache implementation would look something like this:

	<?php namespace App\Extensions;

	class MongoStore implements \Illuminate\Contracts\Cache\Store
	{
		public function get($key) {}
		public function put($key, $value, $minutes) {}
		public function increment($key, $value = 1) {}
		public function decrement($key, $value = 1) {}
		public function forever($key, $value) {}
		public function forget($key) {}
		public function flush() {}
	}

We just need to implement each of these methods using a MongoDB connection. Once our implementation is complete, we can finish our custom driver registration:

	Cache::extend('mongo', function($app) {
		return Cache::repository(new MongoStore);
	});

Once your extension is complete, simply update your `config/cache.php` configuration file's `driver` option to the name of your extension.

If you're wondering where to put your custom cache driver code, consider making it available on Packagist! Or, you could create an `Extensions` namespace within your `app` directory. However, keep in mind that Laravel does not have a rigid application structure and you are free to organize your application according to your preferences.

