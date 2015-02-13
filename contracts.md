# Contracts

- [简介](#introduction)
- [为什么用 Contracts？](#why-contracts)
- [Contract 参考](#contract-reference)
- [如何使用 Contracts](#how-to-use-contracts)

<a name="introduction"></a>
## 简介

Laravel 的 Contracts 是一组定义了框架核心服务的接口（ interfaces ）。例如，`Queue` contract 定义了队列任务所需要的方法，而 `Mailer` contract 定义了寄送 e-mail 需要的方法。

在 Laravel 框架里，每个 contract 都提供了一个对应的实作。例如， Laravel 提供了有多种驱动的 `Queue` 的实作，而根据 [SwiftMailer](http://swiftmailer.org/) 实作了 `Mailer`。

Laravel 所有的 contracts 都放在[各自的 Github repository](https://github.com/illuminate/contracts)。除了提供了所有可用的 contracts 一个快速的参考，也可以单独作为一个低耦合的套件让其他套件开发者使用。

<a name="why-contracts"></a>
## 为什么用 Contracts？

你可能有很多关于 contracts 的问题。像是为什么要使用接口？使用接口会不会变的更复杂？

让我们用下面的标题来解释为什么要使用接口：低耦合和简单性。

### 低耦合

首先，看一些强耦合的缓存实作代码。如下：

	<?php namespace App\Orders;

	class Repository {

		/**
		 * The cache.
		 */
		protected $cache;

		/**
		 * Create a new repository instance.
		 *
		 * @param  \Package\Cache\Memcached  $cache
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
			if ($this->cache->has($id))
			{
				//
			}
		}

	}

在上面的类别里，代码跟缓存实作之间是强耦合。理由是它会依赖于套件库（ package vendor ）的特定缓存类别。一旦这个套件的 API 更改了，我们的代码也要跟着改变。

同样的，如果想要将底层的缓存技术（比如 Memcached ）抽换成另一种（像 Redis ），又一次的我们必须修改这个 repository 类别。我们的 repository 不应该知道这么多关于谁提供了数据，或是如何提供等等细节。

**比起上面的做法，我们可以改用一个简单、和套件无关的接口来改进程式码：**

	<?php namespace App\Orders;

	use Illuminate\Contracts\Cache\Repository as Cache;

	class Repository {

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

现在上面的代码没有跟任何套件耦合，甚至是 Laravel。既然 contracts 套件没有包含实作和任何依赖，你可以很简单的对任何 contract 进行实作，你可以很简单的写一个替换的实作，甚至是替换 contracts，让你可以替换缓存实作而不用修改任何用到缓存的代码。

### 简单性

当所有的 Laravel 服务都简洁的使用简单的接口定义，就能够很简单的决定一个服务需要提供的功能。** 可以将 contracts 视为说明框架特色的简洁文档。**

除此之外，当你依赖简洁的接口，你的代码能够很简单的被了解和维护。比起搜索一个大型复杂的类别里有哪些可用的方法，你有一个简单，干净的接口可以参考。

<a name="contract-reference"></a>
## Contract 参考

以下是大部分 Laravel Contracts 的参考，以及相对应的 "facade"

Contract  |  Laravel 4.x Facade
------------- | -------------
[Illuminate\Contracts\Auth\Guard](https://github.com/illuminate/contracts/blob/master/Auth/Guard.php)  |  Auth
[Illuminate\Contracts\Auth\PasswordBroker](https://github.com/illuminate/contracts/blob/master/Auth/PasswordBroker.php)  |  Password
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
## 如何使用 Contracts

所以，要如何实作一个 contract？实际上非常的简单。很多 Laravel 的类别都是经由 [service container](/docs/5.0/container) 解析，包含控制器，事件监听，过滤器，队列任务，甚至是闭包。所以，要实作一个 contract，你可以在类别的建构子使用「型别提示」解析类别。例如，看下面的事件处理程序：

	<?php namespace App\Handlers\Events;

	use App\User;
	use App\Events\NewUserRegistered;
	use Illuminate\Contracts\Redis\Database;

	class CacheUserInformation {

		/**
		 * Redis 数据库实作
		 */
		protected $redis;

		/**
		 * 建立新的事件处理实例
		 *
		 * @param  Database  $redis
		 * @return void
		 */
		public function __construct(Database $redis)
		{
			$this->redis = $redis;
		}

		/**
		 * 处理事件
		 *
		 * @param  NewUserRegistered  $event
		 * @return void
		 */
		public function handle(NewUserRegistered $event)
		{
			//
		}

	}

当事件监听被解析时，服务容器会经由类别建构子参数的型别提示，注入适当的值。要知道怎么注册更多服务容器，参考[这个文档](/docs/5.0/container)。
