# Contracts

- [簡介](#introduction)
- [為何要用 Contracts?](#why-contracts)
- [Contract 參考](#contract-reference)
- [如何使用 Contracts](#how-to-use-contracts)

<a name="introduction"></a>
## 簡介

Laravel 的 Contracts 是一組定義了框架核心服務的介面（ interfaces ）。例如，`Illuminate\Contracts\Queue\Queue` contract 定義了隊列任務所需要的方法，而 `Illuminate\Contracts\Mail\Mailer` contract 定義了寄送 e-mail 需要的方法。

框架對於每個 contract 都有提供對應的實作，例如，Laravel 提供各種驅動程式的隊列實作，以及由 [SwiftMailer](http://swiftmailer.org/) 提供的 mailer 實作。

Laravel 所有的 contracts 都放在 [各自的 GitHub 儲存庫](https://github.com/illuminate/contracts)。除了提供所有可用的 contracts 一個快速的參考，也可以單獨作為一個低耦合的套件讓其他套件開發者使用。

### Contracts Vs. Facades

Laravel 的 [facades](/docs/{{version}}/facades) 提供一個簡單的方法來使用服務，而不需要使用型別提示和在服務容器之外拆解 contracts。然而，使用 contracts 可以明顯地定義出類別的依賴，對大部分應用程序而言，使用 facade 就很足夠了，然而，若您實在需要特別的低耦合，使用 contracts 可以做到這一點，就讓我們繼續看下去！

<a name="why-contracts"></a>
## 為何要用 Contracts?

你可能有很多關於 contracts 的問題。像是為什麼要使用介面？使用介面會不會變的更複雜？

讓我們用下面的標題來解釋為什麼要使用介面：低耦合和簡單性。

### 低耦合

首先，讓我們來檢視這一段和快取功能有高耦合的程式碼，如下：

	<?php

	namespace App\Orders;

	class Repository
	{
		/**
		 * 快取功能.
		 */
		protected $cache;

		/**
		 * 建立一個新的倉庫實體
		 *
		 * @param  \SomePackage\Cache\Memcached  $cache
		 * @return void
		 */
		public function __construct(\SomePackage\Cache\Memcached $cache)
		{
			$this->cache = $cache;
		}

		/**
		 * 藉由 ID 取得訂單資訊
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

在此類別中，程式和快取實作之間是高耦合。因為它是依賴於套件庫的特定快取類別。一旦這個套件的 API 更改了，我們的程式碼也要跟著改變。

同樣的，如果想要將底層的快取技術（比如 Memcached ）抽換成另一種（像 Redis ），又一次的我們必須修改這個 repository 類別。我們的 儲存庫不應該知道這麼多關於誰提供了資料，或是如何提供等等細節。

**比起上面的做法，我們可以改用一個簡單、和套件無關的介面來改進程式碼：**

	<?php

	namespace App\Orders;

	use Illuminate\Contracts\Cache\Repository as Cache;

	class Repository
	{
		/**
		 * 建立一個新的倉庫實體
		 *
		 * @param  Cache  $cache
		 * @return void
		 */
		public function __construct(Cache $cache)
		{
			$this->cache = $cache;
		}
	}

現在上面的程式碼沒有跟任何套件耦合，甚至是 Laravel。既然 contracts 套件沒有包含實作和任何依賴，你可以很簡單的對任何 contract 進行實作，你可以很簡單的寫一個替換的實作，甚至是替換 contracts，讓你可以替換快取實作而不用修改任何用到快取的程式碼。

### 簡單性

當所有的 Laravel 服務都簡潔的使用簡單的介面定義，就能夠很簡單的決定一個服務需要提供的功能。 **可以將 contracts 視為說明框架特色的簡潔文件。**

除此之外，當你依賴簡潔的介面，你的程式碼能夠很簡單的被瞭解和維護。比起搜尋一個大型複雜的類別裡有哪些可用的方法，你有一個簡單，乾淨的介面可以參考。

<a name="contract-reference"></a>
## Contract 參考

This is a reference to most Laravel Contracts, as well as their Laravel "facade" counterparts:

Contract  |  References Facade
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
## 如何使用 Contracts

So, how do you get an implementation of a contract? It's actually quite simple.

Many types of classes in Laravel are resolved through the [service container](/docs/{{version}}/container), including controllers, event listeners, middleware, queued jobs, and even route Closures. So, to get an implementation of a contract, you can just "type-hint" the interface in the constructor of the class being resolved.

For example, take a look at this event listener:

	<?php

	namespace App\Listeners;

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

When the event listener is resolved, the service container will read the type-hints on the constructor of the class, and inject the appropriate value. To learn more about registering things in the service container, check out [its documentation](/docs/{{version}}/container).
