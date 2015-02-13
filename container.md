# Service Container

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

让我们来看一个简单的例子：

	<?php namespace App\Handlers\Commands;

	use App\User;
	use App\Commands\PurchasePodcast;
	use Illuminate\Contracts\Mail\Mailer;

	class PurchasePodcastHandler {

		/**
		 * 一个发信功能的实现
		 */
		protected $mailer;

		/**
		 * 创建一个新的实例
		 *
		 * @param  Mailer  $mailer
		 * @return void
		 */
		public function __construct(Mailer $mailer)
		{
			$this->mailer = $mailer;
		}

		/**
		 * 购买一个播客节目
		 *
		 * @param  PurchasePodcastCommand  $command
		 * @return void
		 */
		public function handle(PurchasePodcastCommand $command)
		{
			//
		}

	}

在这个例子中，当播客被购买时， `PurchasePodcast` 命令处理器需要发送一封电子邮件。所以，我们将**注入**一个服务来提供这个能力。当这个服务被注入以后，我们就可以轻易地切换到不同的实现。当测试我们的应用程序时，我们同样也可以轻易地“模拟”，或者创建一个虚拟的发信服务实现，来帮助我们进行测试。

如果要创建一个强大并且大型的应用，或者对Laravel的内核做贡献，首先必须对Laravel的服务容器进行深入了解。

<a name="basic-usage"></a>
## 基本用法

### 绑定

几乎你所有服务容器将与已注册的[服务提供者](/doc/5.0/providers)绑定，这些例子都在情境(context)使用容器做说明，如果应用程序其它地方需要容器实例，像是工厂(factory)，能以型别提示 `Illuminate\Contracts\Container\Container` 注入一个容器实例。另外，你可以使用 `App` facade 访问容器。

#### 注册基本解析器

在一个服务提供者内部，你总是可以通过 `$this->app` 实例变量来访问到容器。

在服务提供者里，总是透过 `$this->app` 实例变量使用容器。

服务容器注册依赖有几种方式，包括闭包回调和绑定实例的接口。首先，探讨闭包回调方式，具有键值(通常是类别名称)和返值闭包的闭包解析器，被注册至容器:

	$this->app->bind('FooBar', function($app)
	{
		return new FooBar($app['SomethingElse']);
	});

#### 注册一个单例

有时候，你可能希望绑定到容器的对象只会被解析一次，之后的调用都返回相同的实例：

	$this->app->singleton('FooBar', function($app)
	{
		return new FooBar($app['SomethingElse']);
	});

#### 绑定一个已经存在的实例

你也可以使用 `instance` 方法，绑定一个已经存在的实例到容器，接下来将总是返回该实例：

	$fooBar = new FooBar(new SomethingElse);

	$this->app->instance('FooBar', $fooBar);

### 解析

从容器解析有几种方式。
一、可以使用 `make` 方法：

	$fooBar = $this->app->make('FooBar');

二、你可以像“访问数组”一样对容器进行访问，因为它实现了PHP的 `ArrayAccess` 接口：

	$fooBar = $this->app['FooBar'];

最后，也是最重要的一点，你可以在构造函数中简单地“类型指定（type-hint）”你所需要的依赖，包括在控制器、事件监听器、队列任务，过滤器等等之中。容器将自动注入你所需的所有依赖：

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
## 将接口绑定到实现

### 注入具体依赖

服务容器有个非常强大特色，能够绑定特定实例的接口。举例，假设我们应用程序要集成 [Pusher](https://pusher.com) 服务去收发即时事件，如果使用 Pusher 的 PHP SDK，可以在类别注入一个 Pusher 客户端实例：

	<?php namespace App\Handlers\Commands;

	use App\Commands\CreateOrder;
	use Pusher\Client as PusherClient;

	class CreateOrderHandler {

		/**
		 * Pusher SDK 客户端实例
		 */
		protected $pusher;

		/**
		 * 创建一个实例
		 *
		 * @param  PusherClient  $pusher
		 * @return void
		 */
		public function __construct(PusherClient $pusher)
		{
			$this->pusher = $pusher;
		}

		/**
		 * 执行命令
		 *
		 * @param  CreateOrder  $command
		 * @return void
		 */
		public function execute(CreateOrder $command)
		{
			//
		}

	}

在上面这个例子中，注入类的依赖到类中已经能够满足需求；但同时，我们也紧密耦合于 Pusher 的 SDK 。如果 Pusher 的 SDK 方法发生改变，或者我们要切换到别的事件服务，那我们也需要同时修改 `CreateOrderHandler` 的代码。

### 为接口编程

为了将 `CreateOrderHandler` 和事件推送的修改“隔离”，我们可以定义一个 `EventPusher` 接口和一个 `PusherEventPusher` 实现：

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

一旦 `PusherEventPusher` 实现这接口，就可以在服务容器像这样注册它：

	$this->app->bind('App\Contracts\EventPusher', 'App\Services\PusherEventPusher');

当有类别需要 `EventPusher` 接口时，会告诉容器应该注入 `PusherEventPusher`，现在就可以在构造器中“类型指定”一个 `EventPusher` 接口：

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
## 上下文绑定

有时候，你可能会有两个类需要用到同一个接口，但是你希望为每个类注入不同的接口实现。例如当我们的系统收到一个新的订单时，我们需要使用 [PubNub](http://www.pubnub.com/) 来代替 Pusher 发送消息。Laravel 提供了一个简单便利的接口来定义以上的行为：

	$this->app->when('App\Handlers\Commands\CreateOrderHandler')
	          ->needs('App\Contracts\EventPusher')
	          ->give('App\Services\PubNubEventPusher');

<a name="tagging"></a>
## 标签

偶尔你可能需要解析绑定中的某个“类别”。例如你正在建设一个汇总报表，它需要接收实现了 `Report` 接口的不同实现的数组。在注册了 `Report` 的这些实现之后，你可以用 `tag` 方法来给他们赋予一个标签：

	$this->app->bind('SpeedReport', function()
	{
		//
	});

	$this->app->bind('MemoryReport', function()
	{
		//
	});

	$this->app->tag(['SpeedReport', 'MemoryReport'], 'reports');

一旦服务打上标签，可以通过 `tagged` 方法轻易地解析它们：

	$this->app->bind('ReportAggregator', function($app)
	{
		return new ReportAggregator($app->tagged('reports'));
	});

<a name="practical-applications"></a>
## 实际应用

Laravel 提供了几个机会来使用服务容器以提高应用程序的灵活性和可测试性。解析控制器是一个最主要的案例。所有的控制器都通过服务容器来进行解析，意味着你可以在控制器的构造函数中”类型指定“所需依赖，而且它们将被自动注入。

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

在这个例子中，`OrderRepository` 类将被自动注入到控制器中。这意味着在进行 [单元测试](/docs/5.0/testing) 时，我们可以绑定一个假的 `OrderRepository` 到容器中来代替我们对数据库的真实操作，避免对真实数据库的影响。

#### 使用容器的其他几个例子

当然，在上面提到过的，控制器并不是 Laravel 通过服务容器进行解析的唯一类。你也可以在路由的闭包中、过滤器中、队列任务中、事件监听器中来“类型指定”你所需要的依赖。对于在这些情境中如何使用服务容器，请参考相关文档。

<a name="container-events"></a>
## 容器事件

#### 注册一个解析事件监听器

容器在解析每一个对象时就会触发一个事件。你可以用 `resolving` 方法来监听此事件：

	$this->app->resolving(function($object, $app)
	{
		// 当容器解析任意类型的依赖时被调用
	});

	$this->app->resolving(function(FooBar $fooBar, $app)
	{
		// 当容器解析 `FooBar` 类型的依赖时被调用
	});

被解析的对象将被传入到闭包方法中。