# 服务容器

- [介绍](#introduction)
- [基本用法](#basic-usage)
- [绑定实例的接口](#binding-interfaces-to-implementations)
- [情境绑定](#contextual-binding)
- [标签](#tagging)
- [实际应用](#practical-applications)
- [容器事件](#container-events)

<a name="introduction"></a>
## 介绍

Laravel 服务容器是管理类别依赖的强力工具。依赖注入是个异想天开的词，真正意思是类别依赖透过建构子或 "setter" 方法注入。

来看个简单范例:

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

在这范例里， 当播客被购买时， `PurchasePodcast` 命令处理器需要寄封 e-mails，因此，我们将 **注入** 能寄送 e-mails 的服务，由于服务被注入，我们能容易地切换成其它实例，当测试应用程序时，一样能轻易地 "mock" 或建立假的发信者(mailer)实例。

在建置强大应用程序，以及为 Lavael 核心贡献，须深入理解 Lavavel 服务容器，。

<a name="basic-usage"></a>
## 基本用法

### 绑定

几乎你所有服务容器将与已注册的[服务提供者](/doc/5.0/providers)绑定，这些例子都在情境(context)使用容器做说明，如果应用程序其它地方需要容器实例，像是工厂(factory)，能以型别提示 `Illuminate\Contracts\Container\Container` 注入一个容器实例。另外，你可以使用 `App` facade 访问容器。

#### 注册基本解析器

在服务提供者里，总是透过 `$this->app` 实例变量使用容器。

服务容器注册依赖有几种方式，包括闭包函式和绑定实例的接口。首先，探讨闭包函式，具有键值(通常是类别名称)和返值闭包的闭包解析器，被注册至容器:

	$this->app->bind('FooBar', function($app)
	{
		return new FooBar($app['SomethingElse']);
	});

#### 注册共享

有时候，你可能希望绑定到容器的型别只会被解析一次，之后的调用都返回相同的实例：

	$this->app->singleton('FooBar', function($app)
	{
		return new FooBar($app['SomethingElse']);
	});

#### 绑定已存在的实例到容器

你也可以使用 `instance` 方法，绑定一个已经存在的实例到容器，将总是返回特定的实例：

	$fooBar = new FooBar(new SomethingElse);

	$this->app->instance('FooBar', $fooBar);

### 解析

从容器解析有几种方式。一、可以使用 `make` 方法：

	$fooBar = $this->app->make('FooBar');

二、可以对实作 PHP `ArrayAccess` 接口的容器，使用 "数组访问"：

	$fooBar = $this->app['FooBar'];

最后，重点是你可以简单地在类别建构子注入"型别提示"依赖，包含控制器、事件监听者、工作队列、筛选器等，容器将会自动注入依赖：

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
## 绑定实例的接口

### 注入具体依赖

服务容器有个非常强大特色，能够绑定特定实例的接口。举例，假设我们应用程序要集成 [Pusher](https://pusher.com) 服务去收发即时事件，如果使用 Pusher 的 PHP SDK，可以在类别注入一个 Pusher 客户端实例：

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

在这范例中，注入类别依赖是件好事，不过，与 Pusher SDK 产生紧密耦合，如果 Pusher SDK 方法异动，或是决定彻底改变成新的事件服务时，需要改写 `CreateOrderHandler` 代码。

### 设计成接口

为了"隔离" `createOrderHander` 倚靠于事件推送变化，可以定义 `EventPusher` 接口和 `PusherEventPusher` 实例：

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

一旦 `PusherEventPusher` 实作这接口，就可以在服务容器像这样注册它：

	$this->app->bind('App\Contracts\EventPusher', 'App\Services\PusherEventPusher');

当有类别需要 `EventPusher` 实作时，会告诉容器应该注入 `PusherEventPusher`，现在可以在建构子做型别提示 `EventPusher` 接口：

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
## 情境绑定

有时候，你可能有两个类别使用到相同接口，但你希望每个类别能注入不同实例，例如当系统收到新订单时，想透过 [PubNub](http://www.pubnub.com/) 来发送事件，而不是 Pusher。 Laravel 提供一个简单又流利接口来定义这行为：

	$this->app->when('App\Handlers\Commands\CreateOrderHandler')
			  ->needs('App\Contracts\EventPusher')
			  ->give('App\Services\PubNubEventPusher');

<a name="tagging"></a>
## 标签

你偶尔可能需要解析某一个分类下的所有绑定，例如你正在建置一个能接收各种 `Report` 接口实例之数组的报表聚合器(report aggregator)，注册完 `Report` 实例后，可以使用 `tag` 方法将它们指派成一个标签：

	$this->app->bind('SpeedReport', function()
	{
		//
	});

	$this->app->bind('MemoryReport', function()
	{
		//
	});

	$this->app->tag(['SpeedReport', 'MemoryReport'], 'reports');

一旦服务完成标签，可以透过 `tagged` 方法轻易地解析它们：

	$this->app->bind('ReportAggregator', function($app)
	{
		return new ReportAggregator($app->tagged('reports'));
	});

<a name="practical-applications"></a>
## 实际应用

Laravel 提供几个使用服务容器，提高应用程序弹性和可测试性的机会，主要例子是解析控制器时，所有控制器都是透过服务容器解析，意思是你可在控制器建构子做型别提示依赖，它们将会自动注入。

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

在这范例中，`OrderRespository` 类别会自动被注入至控制器，这意味着，在[单元测试](/docs/5.0/testing)时，"mock" `OrderRepository` 可以绑定至容器，给予数据库层交互无痛的 stub 。

#### 其他容器使用范例

当然，如上面所述，控制器不是唯一透过服务容器 Laravel 类别解析，你也可以在路由闭包、筛选器、工作队列、事件聆听等，做型别提示依赖，对于在这些情境使用服务容器的例子，请参考相关文档。

<a name="container-events"></a>
## 容器事件

#### 注册解析事件的监听

每当容器解析一个对象时就会触发事件，你可以使用 `resolving` 方法监听这个事件：

	$this->app->resolving(function($object, $app)
	{
		// Called when container resolves object of any type...
	});

	$this->app->resolving(function(FooBar $fooBar, $app)
	{
		// Called when container resolves objects of type "FooBar"...
	});

被解析的对象会被传到闭合函式。
