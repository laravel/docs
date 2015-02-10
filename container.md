# 服務容器

- [介紹](#introduction)
- [基本用法](#basic-usage)
- [綁定實例的介面](#binding-interfaces-to-implementations)
- [情境綁定](#contextual-binding)
- [標籤](#tagging)
- [實際應用](#practical-applications)
- [容器事件](#container-events)

<a name="introduction"></a>
## 介紹

Laravel 服務容器是管理類別依賴的強力工具。依賴注入是個異想天開的詞，真正意思是類別依賴透過建構子或 "setter" 方法注入。

來看個簡單範例:

	<?php namespace App\Handlers\Commands;

	use App\User;
	use App\Commands\PurchasePodcast;
	use Illuminate\Contracts\Mail\Mailer;

	class PurchasePodcastHandler {

		/**
		 * The mailer implementation.
		 */
		protected $mailer;

		/**
		 * Create a new instance.
		 *
		 * @param  Mailer  $mailer
		 * @return void
		 */
		public function __construct(Mailer $mailer)
		{
			$this->mailer = $mailer;
		}

		/**
		 * Purchase a podcast.
		 *
		 * @param  PurchasePodcastCommand  $command
		 * @return void
		 */
		public function handle(PurchasePodcastCommand $command)
		{
			//
		}

	}

在這範例裡， 當播客被購買時， `PurchasePodcast` 命令處理器需要寄封 e-mails，因此，我們將 **注入** 能寄送 e-mails 的服務，由於服務被注入，我們能容易地切換成其它實例，當測試應用程式時，一樣能輕易地 "mock" 或建立假的發信者(mailer)實例。

在建置強大應用程式，以及為 Lavael 核心貢獻，須深入理解 Lavavel 服務容器，。

<a name="basic-usage"></a>
## 基本用法

### 綁定

幾乎你所有服務容器將與已註冊的[服務提供者](/doc/5.0/providers)綁定，這些例子都在情境(context)使用容器做說明，如果應用程式其它地方需要容器實例，像是工廠(factory)，能以型別提示 `Illuminate\Contracts\Container\Container` 注入一個容器實例。另外，你可以使用 `App` facade 存取容器。

#### 註冊基本解析器

在服務提供者裡，總是透過 `$this->app` 實例變數使用容器。

服務容器注冊依賴有幾種方式，包括閉包函式和綁定實例的介面。首先，探討閉包函式，具有鍵值(通常是類別名稱)和返值閉包的閉包解析器，被註冊至容器:

	$this->app->bind('FooBar', function($app)
	{
		return new FooBar($app['SomethingElse']);
	});

#### 註冊共享

有時候，你可能希望綁定到容器的型別只會被解析一次，之後的呼叫都返回相同的實例：

	$this->app->singleton('FooBar', function($app)
	{
		return new FooBar($app['SomethingElse']);
	});

#### 綁定已存在的實例到容器

你也可以使用 `instance` 方法，綁定一個已經存在的實例到容器，將總是返回特定的實例：

	$fooBar = new FooBar(new SomethingElse);

	$this->app->instance('FooBar', $fooBar);

### 解析

從容器解析有幾種方式。一、可以使用 `make` 方法：

	$fooBar = $this->app->make('FooBar');

二、可以對實作 PHP `ArrayAccess` 介面的容器，使用 "陣列存取"：

	$fooBar = $this->app['FooBar'];

最後，重點是你可以簡單地在類別建構子注入"型別提示"依賴，包含控制器、事件監聽者、工作隊列、篩選器等，容器將會自動注入依賴：

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use App\Users\Repository as UserRepository;

	class UserController extends Controller {

		/**
		 * The user repository instance.
		 */
		protected $users;

		/**
		 * Create a new controller instance.
		 *
		 * @param  UserRepository  $users
		 * @return void
		 */
		public function __construct(UserRepository $users)
		{
			$this->users = $users;
		}

		/**
		 * Show the user with the given ID.
		 *
		 * @param  int  $id
		 * @return Response
		 */
		public function show($id)
		{
			//
		}

	}

<a name="binding-interfaces-to-implementations"></a>
## 綁定實例的介面

### 注入具體依賴

服務容器有個非常強大特色，能夠綁定特定實例的介面。舉例，假設我們應用程式要整合 [Pusher](https://pusher.com) 服務去收發即時事件，如果使用 Pusher 的 PHP SDK，可以在類別注入一個 Pusher 客戶端實例：

	<?php namespace App\Handlers\Commands;

	use App\Commands\CreateOrder;
	use Pusher\Client as PusherClient;

	class CreateOrderHandler {

		/**
		 * The Pusher SDK client instance.
		 */
		protected $pusher;

		/**
		 * Create a new order handler instance.
		 *
		 * @param  PusherClient  $pusher
		 * @return void
		 */
		public function __construct(PusherClient $pusher)
		{
			$this->pusher = $pusher;
		}

		/**
		 * Execute the given command.
		 *
		 * @param  CreateOrder  $command
		 * @return void
		 */
		public function execute(CreateOrder $command)
		{
			//
		}

	}

在這範例中，注入類別依賴是件好事，不過，與 Pusher SDK 產生緊密耦合，如果 Pusher SDK 方法異動，或是決定徹底改變成新的事件服務時，需要改寫 `CreateOrderHandler` 程式碼。

### 設計成介面

為了"隔離" `createOrderHander` 倚靠於事件推送變化，可以定義 `EventPusher` 介面和 `PusherEventPusher` 實例：

	<?php namespace App\Contracts;

	interface EventPusher {

		/**
		 * Push a new event to all clients.
		 *
		 * @param  string  $event
		 * @param  array  $data
		 * @return void
		 */
		public function push($event, array $data);

	}

一旦 `PusherEventPusher` 實作這介面，就可以在服務容器像這樣註冊它：

	$this->app->bind('App\Contracts\EventPusher', 'App\Services\PusherEventPusher');

當有類別需要 `EventPusher` 實作時，會告訴容器應該注入 `PusherEventPusher`，現在可以在建構子做型別提示 `EventPusher` 介面：

		/**
		 * Create a new order handler instance.
		 *
		 * @param  EventPusher  $pusher
		 * @return void
		 */
		public function __construct(EventPusher $pusher)
		{
			$this->pusher = $pusher;
		}

<a name="contextual-binding"></a>
## 情境綁定

有時候，你可能有兩個類別使用到相同介面，但你希望每個類別能注入不同實例，例如當系統收到新訂單時，想透過 [PubNub](http://www.pubnub.com/) 來發送事件，而不是 Pusher。 Laravel 提供一個簡單又流利介面來定義這行為：

	$this->app->when('App\Handlers\Commands\CreateOrderHandler')
			  ->needs('App\Contracts\EventPusher')
			  ->give('App\Services\PubNubEventPusher');

<a name="tagging"></a>
## 標籤

你偶爾可能需要解析某一個分類下的所有綁定，例如你正在建置一個能接收各種 `Report` 介面實例之陣列的報表聚合器(report aggregator)，註冊完 `Report` 實例後，可以使用 `tag` 方法將它們指派成一個標籤：

	$this->app->bind('SpeedReport', function()
	{
		//
	});

	$this->app->bind('MemoryReport', function()
	{
		//
	});

	$this->app->tag(['SpeedReport', 'MemoryReport'], 'reports');

一旦服務完成標籤，可以透過 `tagged` 方法輕易地解析它們：

	$this->app->bind('ReportAggregator', function($app)
	{
		return new ReportAggregator($app->tagged('reports'));
	});

<a name="practical-applications"></a>
## 實際應用

Laravel 提供幾個使用服務容器，提高應用程式彈性和可測試性的機會，主要例子是解析控制器時，所有控制器都是透過服務容器解析，意思是你可在控制器建構子做型別提示依賴，它們將會自動注入。

	<?php namespace App\Http\Controllers;

	use Illuminate\Routing\Controller;
	use App\Repositories\OrderRepository;

	class OrdersController extends Controller {

		/**
		 * The order repository instance.
		 */
		protected $orders;

		/**
		 * Create a controller instance.
		 *
		 * @param  OrderRepository  $orders
		 * @return void
		 */
		public function __construct(OrderRepository $orders)
		{
			$this->orders = $orders;
		}

		/**
		 * Show all of the orders.
		 *
		 * @return Response
		 */
		public function index()
		{
			$all = $this->orders->all();

			return view('orders', ['all' => $all]);
		}

	}

在這範例中，`OrderRespository` 類別會自動被注入至控制器，這意味著，在[單元測試](/docs/5.0/testing)時，"mock" `OrderRepository` 可以綁定至容器，給予資料庫層互動無痛的 stub 。

#### 其他容器使用範例

當然，如上面所述，控制器不是唯一透過服務容器 Laravel 類別解析，你也可以在路由閉包、篩選器、工作隊列、事件聆聽等，做型別提示依賴，對於在這些情境使用服務容器的例子，請參考相關文件。

<a name="container-events"></a>
## 容器事件

#### 註冊解析事件的監聽

每當容器解析一個物件時就會觸發事件，你可以使用 `resolving` 方法監聽這個事件：

	$this->app->resolving(function($object, $app)
	{
		// Called when container resolves object of any type...
	});

	$this->app->resolving(function(FooBar $fooBar, $app)
	{
		// Called when container resolves objects of type "FooBar"...
	});

被解析的物件會被傳到閉合函式。
