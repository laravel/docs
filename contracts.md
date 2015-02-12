# Contracts

- [簡介](#introduction)
- [為什麼用 Contracts？](#why-contracts)
- [Contract 參考](#contract-reference)
- [如何使用 Contracts](#how-to-use-contracts)

<a name="introduction"></a>
## 簡介

Laravel 的 Contracts 是一組定義了框架核心服務的介面（ interfaces ）。例如，`Queue` contract 定義了隊列任務所需要的方法，而 `Mailer` contract 定義了寄送 e-mail 需要的方法。

在 Laravel 框架裡，每個 contract 都提供了一個對應的實作。例如， Laravel 提供了有多種驅動的 `Queue` 的實作，而根據 [SwiftMailer](http://swiftmailer.org/) 實作了 `Mailer`。

Laravel 所有的 contracts 都放在[各自的 Github repository](https://github.com/illuminate/contracts)。除了提供了所有可用的 contracts 一個快速的參考，也可以單獨作為一個低耦合的套件讓其他套件開發者使用。

<a name="why-contracts"></a>
## 為什麼用 Contracts？

你可能有很多關於 contracts 的問題。像是為什麼要使用介面？使用介面會不會變的更複雜？

讓我們用下面的標題來解釋為什麼要使用介面：低耦合和簡單性。

### 低耦合

首先，看一些強耦合的快取實作程式碼。如下：

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

在上面的類別裡，程式碼跟快取實作之間是強耦合。理由是它會依賴於套件庫（ package vendor ）的特定快取類別。一旦這個套件的 API 更改了，我們的程式碼也要跟著改變。

同樣的，如果想要將底層的快取技術（比如 Memcached ）抽換成另一種（像 Redis ），又一次的我們必須修改這個 repository 類別。我們的 repository 不應該知道這麼多關於誰提供了資料，或是如何提供等等細節。

**比起上面的做法，我們可以改用一個簡單、和套件無關的介面來改進程式碼：**

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

現在上面的程式碼沒有跟任何套件耦合，甚至是 Laravel。既然 contracts 套件沒有包含實作和任何依賴，你可以很簡單的對任何 contract 進行實作，你可以很簡單的寫一個替換的實作，甚至是替換 contracts，讓你可以替換快取實作而不用修改任何用到快取的程式碼。

### 簡單性

當所有的 Laravel 服務都簡潔的使用簡單的介面定義，就能夠很簡單的決定一個服務需要提供的功能。** 可以將 contracts 視為說明框架特色的簡潔文件。**

除此之外，當你依賴簡潔的介面，你的程式碼能夠很簡單的被瞭解和維護。比起搜尋一個大型複雜的類別裡有哪些可用的方法，你有一個簡單，乾淨的介面可以參考。

<a name="contract-reference"></a>
## Contract 參考

以下是大部分 Laravel Contracts 的參考，以及相對應的 "facade"

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

所以，要如何實作一個 contract？實際上非常的簡單。很多 Laravel 的類別都是經由 [service container](/docs/5.0/container) 解析，包含控制器，事件監聽，過濾器，隊列任務，甚至是閉包。所以，要實作一個 contract，你可以在類別的建構子使用「型別提示」解析類別。例如，看下面的事件處理程式：

	<?php namespace App\Handlers\Events;

	use App\User;
	use App\Events\NewUserRegistered;
	use Illuminate\Contracts\Redis\Database;

	class CacheUserInformation {

		/**
		 * Redis 資料庫實作
		 */
		protected $redis;

		/**
		 * 建立新的事件處理實例
		 *
		 * @param  Database  $redis
		 * @return void
		 */
		public function __construct(Database $redis)
		{
			$this->redis = $redis;
		}

		/**
		 * 處理事件
		 *
		 * @param  NewUserRegistered  $event
		 * @return void
		 */
		public function handle(NewUserRegistered $event)
		{
			//
		}

	}

當事件監聽被解析時，服務容器會經由類別建構子參數的型別提示，注入適當的值。要知道怎麼註冊更多服務容器，參考[這個文件](/docs/5.0/container)。
