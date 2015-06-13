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


O Laravel fornece uma API unificada para vários sistemas de cache. A configuração do cache do Laravel fica em `config/cache.php`. Neste arquivo você pode especificar o driver que você gostaria de usar por padrão em toda a sua aplicação. O Laravel suporta ferramentas como [Memcached](http://memcached.org) e [Redis](http://redis.io) de uma maneira massa.

O arquivo de configuração do cache também contém várias outras opções que são documentadas dentro do arquivo, sendo assim, certifique-se de ler estas opções. Por padrão, o Laravel é configurado para usar o drive `file`, que armazena objetos serializados no sistema de arquivos. Para grandes aplicações, recomenda-se que você utilize um in-memory cache como Memcached ou APC. Você pode ter várias configurações de cache para o mesmo driver.

### Pré-requisitos do Cache

#### Banco de dados

Quando estiver usando o driver `database`, você precisará criar uma tabela para os itens do cachê. Aqui temos um exemplo de `Schema` para a tabela:

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

Você pode também setar a opção `host` para um caminho de socket UNIX. Se você fizer isto, a opção `port` deverá ser setada como `0`:

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

As [Contracts](/docs/{{version}}/contracts) `Illuminate\Contracts\Cache\Factory` e `Illuminate\Contracts\Cache\Repository` fornecem acesso para os serviços de cache do Laravel. A contract `Factory` fornecem acesso para todos os drivers de cache definidos por sua aplicação. A contract `Repository` é tipicamente uma implementação do drive de cache padrão para sua aplicação especificado pelo seu arquivo de configuração de `cache`.

Por outro lado, você também pode usar a facade `Cache`, que é o que vamos utilizar em toda esta documentação. A facade `Cache` fornece convenientemente acesso elegante para as implementações subjacentes dos contratos de cache Laravel

Por exemplo, vamos importar a facade `Cache` dentro de um controller:

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

#### Acessando Múltiplos Caches Armazenados

Usando a facade `Cache`, você pode acessar vários caches armazenados através do método `store`. A variável passada para o método `store` deve corresponder a um dos itens do array de configuração `store` que fica no seu arquivo de configuração do `cache`:

	$value = Cache::store('file')->get('foo');

	Cache::store('redis')->put('bar', 'baz', 10);

<a name="retrieving-items-from-the-cache"></a>
### Recuperando Itens do Cache

O método `get` da facade `Cache` é usado para recuperar itens do cache. Se o item não existir no cache, `null` será retornado. Se você preferir, você pode passar um segundo argumento para o método `get`, especificando o valor padrão que você quiser que seja retornado caso o item não exista:

	$value = Cache::get('key');

	$value = Cache::get('key', 'default');

Você pode passar uma `Closure` como um valor padrão também. O resultado da `Closure` será retornado se o item especificado não existir no cache. Passando uma Closure você pode diferenciar a recuperação de valores padrão de um banco de dados ou outro serviço externo:

	$value = Cache::get('key', function() {
		return DB::table(...)->get();
	});

#### Verificando a Existência de um Item

O método `has` pode ser usado para determinar se um item existe no cache:

	if (Cache::has('key')) {
		//
	}

#### Incremetando / Desincrementando Valores

Os métodos `increment` e `decrement` podem ser usados para ajustar o valor dos itens numéricos inteiros do cache. Ambos os métodos opcionalmente aceitam um segundo argumento indicando o número que você deve incrementar ou desincrementar.

	Cache::increment('key');

	Cache::increment('key', $amount);

	Cache::decrement('key');

	Cache::decrement('key', $amount);

#### Recuperar ou Atualizar

Algumas vezes você pode querer recuperar um item do cache, mas também gravar um valor padrão se o item pedido não existir. Por exemplo, você quer recuperar todos os usuários do cache ou, se se eles não existirem, recuperar do banco de dados e adicionar no cache. Você pode fazer isto usando o método `Cache::remember`:

	$value = Cache::remember('users', $minutes, function() {
		return DB::table('users')->get();
	});

Se o item não existir no cache, a `Closure` passada para o método `remember` será executada e seu resultado serar colocado no cache.

Você pode também combinar os métodos `remembeŕ` e `forever`:

	$value = Cache::rememberForever('users', function() {
		return DB::table('users')->get();
	});

#### Recuperando e Deletando

Se você precisar recuperar um item do cache e posteriormente deletá-lo, você pode usar o método `pull`. Assim como o método `get`, `null` será retornado se o item não existir no cache:

	$value = Cache::pull('key');

<a name="storing-items-in-the-cache"></a>
### Gravando Itens no Cache

Você pode usar o método `set` na facade `Cache` para armazenar itens no cache. Quando você coloca um item no cache, você precisa especificar o número de minutos que o valor ficará cacheado:

	Cache::put('key', 'value', $minutes);

Em vez de passar o número de minutos de expiração do item, você também pode passar uma instancia da classe `DateTime` do PHP representando o tempo de expiração do item cacheado:

	$expiresAt = Carbon::now()->addMinutes(10);

	Cache::put('key', 'value', $expiresAt);

O método `add` somente adicionará o item para o cache se ele ainda não existir no cache. O método retornará `true` se o item for armazenado com sucesso. Do contrário, o método retornará `false`:

	Cache::add('key', 'value', $minutes);

O método `forever` pode ser usado para armazenar um item no cache permanentemente. Estes valores deve ser manualmente removidos do cache utilizando o método `forget`:

	Cache::forever('key', 'value');

<a name="removing-items-from-the-cache"></a>
### Removendo Items do Cache

Você pode remover itens do cache usando o método `forget` na facade `Cache`

	Cache::forget('key');

<a name="adding-custom-cache-drivers"></a>
## Adicionando um Driver de Cache Customizado

Para extender o cache do Laravel com um driver customizado, nós usaremos o método `extend` da facade `Cache`, que é usado para vincular um driver customizado para o gerenciador. Normalmente, isto é feito com um [service provider](/docs/{{version}}/providers).

Por exemplo, para registrar um novo driver de cache com o nome "mongo":

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

O primeiro argumento passado para o método `extend` é o nome do driver. Isto corresponderá à sua opção escolhida para `driver` no arquivo de configuração `config/cache.php`. O segundo argumento é a Closure que deve retornar uma instância de `Illuminate\Cache\Repository`. Na Closure será passada a variável `$app`, que é a instancia de [service container](/docs/{{version}}/container).

A chamada para `Cache::extend` poderia ser feita no método `boot` do `App\Providers\AppServiceProvider` que é fornecido com a aplicação Laravel, ou você pode criar seu próprio service provider para abrigar a extensão - Não se esqueça de registrar o serviço no array de service providers em `config/app.php`

Para criar seu cache de driver customizado, antes você precisa implementar a [contract](/docs/{{version}}/contracts) `Illuminate\Contracts\Cache\Store`. Então, sua implementação de cache MongoDB seria algo como isto:

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

Nós precisamos implementar cada um desses métodos usando uma conexão MongoDB. Uma vez que sua implementação é completa, nós podemos finalizar o registro de seu driver customizado:

	Cache::extend('mongo', function($app) {
		return Cache::repository(new MongoStore);
	});

Uma vez que sua extensão for completada, simplesmente mude a opção `driver` no seu arquivo de configuração `config/cache.php` para o nome de sua extensão.

Se você estiver querendo saber onde colocar o código do seu driver de cache customizado, considere deixar isto disponível no Packagist! Ou, você pode criar um namespace `Extensions` dentro do seu diretório `app`. Contudo, tenha em mente que Laravel não tem uma estrutura de aplicação rígida e você é livre para organizar sua aplicação de acordo com suas preferências.
