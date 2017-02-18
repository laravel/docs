# Contracts

- [Introdução](#introduction)
- [Por que Contracts?](#why-contracts)
- [Referência das Contracts](#contract-reference)
- [Como Utilizar Contracts](#how-to-use-contracts)

<a name="introduction"></a>
## Introdução

As Contracts do Laravel são uma série de *interfaces* que definem os serviços essenciais fornecidos pelo framework. Por exemplo, a contract `Illuminate\Contracts\Queue\Queue` define os metodos para trabalhar com filas, enquanto a contract `Illuminate\Contracts\Mail\Mailer` define os métodos necessários para o envio de emails.

Cada contract possui uma implementação correspondente disponibilizada pelo framework. Por exemplo, o Laravel disponibiliza uma implementação de *queue* para inúmeros *drivers*, e uma implementação do *mailer* fornecida pelo [SwiftMailer](http://swiftmailer.org/).

Todas as contracts do Laravel estão em um [repositório no GitHub](https://github.com/illuminate/contracts). Isto fornece um ponto de referência rápida para todas as contracts disponíveis, assim como um pacote único, dissociado dos demais, que pode ser utilizado por desenvolvedores de pacotes.

### Contracts Vs. Facades

As [facades](/docs/{{version}}/facades) do Laravel fornecem um modo simples de utilizar os serviços do framework, sem a necessidade de explicitar e resolver as contracts através do *service container*. Entretanto, utilizar contracts permite que você defina explicitamente as dependências de sua classe. Para a maioria das aplicações as *Facades* são o sufuciente. Porém, caso seja necessário o baixo acoplamente fornecido pelos contracts, continue lendo!

<a name="why-contracts"></a>
## Por que Contracts?

Você pode ter muitas perguntas a respeito de contracts. Por que utilizar interfaces? Utilizar interfaces não é mais complicado? Vamos exemplificar as razões para o uso de *interfaces* para os seguintes tópicos: Simplicidade e Baixo Acoplamento.

### Baixo Acoplamento

Primeiro, vamos revisar um código que está fortemente vinculado a uma implementação de *cache*. Considere o seguinte:


	<?php namespace App\Orders;

	class Repository
	{
		/**
		 * The cache.
		 */
		protected $cache;

		/**
		 * Create a new repository instance.
		 *
		 * @param  \SomePackage\Cache\Memcached  $cache
		 * @return void
		 */
		public function __construct(\SomePackage\Cache\Memcached $cache)
		{
			$this->cache = $cache;
		}

		/**
		 * Retrieve an Order by ID.
		 *
		 * @param  int  $id
		 * @return Order
		 */
		public function find($id)
		{
			if ($this->cache->has($id))	{
				//
			}
		}
	}

Nesta classe, o código está fortemente vinculado a uma implementação de *cache*. Isto se deve ao fato de que estamos dependendo de uma classe concreta de *Cache*. Se a API desta classe for alterada, termos que alterar nosso código também.

Do mesmo modo, se for necessário alterar a atual tecnologia de *cache* (Memcached) por outra (Redis), teremos que modificar nosso repositório novamente. O repositório não dever ter tanto conhecimento a respeito de quem irá provê-lo de dados ou mesmo como eles estão sendo providos.

**Ao invés desta abordagem, podemos melhorar nosso código dependendo de uma *interface* simples e *vendor agnostic*:**

	<?php namespace App\Orders;

	use Illuminate\Contracts\Cache\Repository as Cache;

	class Repository
	{
		/**
		 * Create a new repository instance.
		 *
		 * @param  Cache  $cache
		 * @return void
		 */
		public function __construct(Cache $cache)
		{
			$this->cache = $cache;
		}
	}

Agora o código não está vinculado a um *vendor* específico, nem mesmo ao Laravel. Já que o pacote de contracts não contém implementações e dependências, você pode facilmente escrever uma implementação alternativa para qualquer uma das contracts, possibilitando que você troque a implementação do *cache* sem que seja necessário alterações em seu código.

### Simplicidade

Quando todos os serviços do Laravel estão nitidamente definidos em *interfaces* simples, é muito fácil determinar a funcionalidade oferecida pelo serviço. **As contracts servem como uma documentação sucinta dos recursos do framework.**

Além disso, quando você depende de *interfaces* simples, o entendimento e a manutenção do seu código são mais fáceis. Ao invés de rastrear quais métodos estão disponíveis dentro de uma extensa e complexa classe, você pode consultar uma *interface* simples e limpa.

<a name="contract-reference"></a>
## Referência das Contracts

Esta é uma referência para a maiorias das Contracts do Laravel, assim como suas respectivas *Facades*:


Contract  |  Facade
------------- | -------------
[Illuminate\Contracts\Auth\Guard](https://github.com/illuminate/contracts/blob/master/Auth/Guard.php)  |  Auth
[Illuminate\Contracts\Auth\PasswordBroker](https://github.com/illuminate/contracts/blob/master/Auth/PasswordBroker.php)  |  Password
[Illuminate\Contracts\Bus\Dispatcher](https://github.com/illuminate/contracts/blob/master/Bus/Dispatcher.php)  |  Bus
[Illuminate\Contracts\Broadcasting\Broadcaster](https://github.com/illuminate/contracts/blob/master/Broadcasting/Broadcaster.php)  | &nbsp;
[Illuminate\Contracts\Cache\Repository](https://github.com/illuminate/contracts/blob/master/Cache/Repository.php) | Cache
[Illuminate\Contracts\Cache\Factory](https://github.com/illuminate/contracts/blob/master/Cache/Factory.php) | Cache::driver()
[Illuminate\Contracts\Config\Repository](https://github.com/illuminate/contracts/blob/master/Config/Repository.php) | Config
[Illuminate\Contracts\Container\Container](https://github.com/illuminate/contracts/blob/master/Container/Container.php) | App
[Illuminate\Contracts\Cookie\Factory](https://github.com/illuminate/contracts/blob/master/Cookie/Factory.php) | Cookie
[Illuminate\Contracts\Cookie\QueueingFactory](https://github.com/illuminate/contracts/blob/master/Cookie/QueueingFactory.php) | Cookie::queue()
[Illuminate\Contracts\Encryption\Encrypter](https://github.com/illuminate/contracts/blob/master/Encryption/Encrypter.php) | Crypt
[Illuminate\Contracts\Events\Dispatcher](https://github.com/illuminate/contracts/blob/master/Events/Dispatcher.php) | Event
[Illuminate\Contracts\Filesystem\Cloud](https://github.com/illuminate/contracts/blob/master/Filesystem/Cloud.php) | &nbsp;
[Illuminate\Contracts\Filesystem\Factory](https://github.com/illuminate/contracts/blob/master/Filesystem/Factory.php) | File
[Illuminate\Contracts\Filesystem\Filesystem](https://github.com/illuminate/contracts/blob/master/Filesystem/Filesystem.php) | File
[Illuminate\Contracts\Foundation\Application](https://github.com/illuminate/contracts/blob/master/Foundation/Application.php) | App
[Illuminate\Contracts\Hashing\Hasher](https://github.com/illuminate/contracts/blob/master/Hashing/Hasher.php) | Hash
[Illuminate\Contracts\Logging\Log](https://github.com/illuminate/contracts/blob/master/Logging/Log.php) | Log
[Illuminate\Contracts\Mail\MailQueue](https://github.com/illuminate/contracts/blob/master/Mail/MailQueue.php) | Mail::queue()
[Illuminate\Contracts\Mail\Mailer](https://github.com/illuminate/contracts/blob/master/Mail/Mailer.php) | Mail
[Illuminate\Contracts\Queue\Factory](https://github.com/illuminate/contracts/blob/master/Queue/Factory.php) | Queue::driver()
[Illuminate\Contracts\Queue\Queue](https://github.com/illuminate/contracts/blob/master/Queue/Queue.php) | Queue
[Illuminate\Contracts\Redis\Database](https://github.com/illuminate/contracts/blob/master/Redis/Database.php) | Redis
[Illuminate\Contracts\Routing\Registrar](https://github.com/illuminate/contracts/blob/master/Routing/Registrar.php) | Route
[Illuminate\Contracts\Routing\ResponseFactory](https://github.com/illuminate/contracts/blob/master/Routing/ResponseFactory.php) | Response
[Illuminate\Contracts\Routing\UrlGenerator](https://github.com/illuminate/contracts/blob/master/Routing/UrlGenerator.php) | URL
[Illuminate\Contracts\Support\Arrayable](https://github.com/illuminate/contracts/blob/master/Support/Arrayable.php) | &nbsp;
[Illuminate\Contracts\Support\Jsonable](https://github.com/illuminate/contracts/blob/master/Support/Jsonable.php) | &nbsp;
[Illuminate\Contracts\Support\Renderable](https://github.com/illuminate/contracts/blob/master/Support/Renderable.php) | &nbsp;
[Illuminate\Contracts\Validation\Factory](https://github.com/illuminate/contracts/blob/master/Validation/Factory.php) | Validator::make()
[Illuminate\Contracts\Validation\Validator](https://github.com/illuminate/contracts/blob/master/Validation/Validator.php) | &nbsp;
[Illuminate\Contracts\View\Factory](https://github.com/illuminate/contracts/blob/master/View/Factory.php) | View::make()
[Illuminate\Contracts\View\View](https://github.com/illuminate/contracts/blob/master/View/View.php) | &nbsp;

<a name="how-to-use-contracts"></a>
## Como Utilizar Contracts

Então, como você consegue uma implementação de uma contract? Na verdade é bastante simples.

Muitos tipos de classes no Laravel são resolvidos através do [service container](/docs/{{version}}/container), incluindos os *controllers*, *event listeners*, *middlewares*, *queue jobs*, e até *route Closures*. Logo, para obter a implementação de uma contract, basta você "informar" a interface desejada no construtor da classe que está sendo resolvida.

Por exemplo, considere o seguinte *event listener*:

	<?php namespace App\Listeners;

	use App\User;
	use App\Events\NewUserRegistered;
	use Illuminate\Contracts\Redis\Database;

	class CacheUserInformation
	{
		/**
		 * The Redis database implementation.
		 */
		protected $redis;

		/**
		 * Create a new event handler instance.
		 *
		 * @param  Database  $redis
		 * @return void
		 */
		public function __construct(Database $redis)
		{
			$this->redis = $redis;
		}

		/**
		 * Handle the event.
		 *
		 * @param  NewUserRegistered  $event
		 * @return void
		 */
		public function handle(NewUserRegistered $event)
		{
			//
		}
	}

Quando o *event listener* é resolvido, o *service container* lerá o construtor da classe e injetará as dependências apropriadas. Para aprender mais sobre como registrar coisas no *service container* dê uma olhada [na documentação](/docs/{{version}}/container).
