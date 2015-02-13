# 服务提供者

- [简介](#introduction)
- [基本提供者范例](#basic-provider-example)
- [注册提供者](#registering-providers)
- [缓载提供者](#deferred-providers)

<a name="introduction"></a>
## 简介

服务提供者是所有 Laravel 应用程序的启动中心。你的应用程序，以及所有 Laravel 的核心服务，都是透过服务提供者启动。

但我们所说的「启动」指的是什么？一般而言，我们指**注册**事物，包括注册服务容器绑定、事件监听器、过滤器，甚至路由。服务提供者是你的应用程序设置中心所在。

如果你开启包含于 Laravel 中 `config/app.php` 此一文件，你会看到 `providers` 数组。这些是所有将加载至你的应用程序里的服务提供者类别。当然，它们之中有很多属于「缓载」提供者，意思是除非真正需要它们所提供的服务，否则它们并不会在每一个请求中都被加载。

在这份概述中，你会学到如何编写你自己的服务提供者，并将它们注册于你的 Laravel 应用程序。

<a name="basic-provider-example"></a>
## 基本提供者范例

所有的服务提供者都应继承 `Illuminate\Support\ServiceProvider` 此一类别。在这个抽象类别中，至少必须定义一个方法： `register` 。在 `register` 方法中，应该**只绑定服务到[服务容器](/docs/5.0/container)之中**。你永远不该试图在 `register` 方法中注册任何事件监听器、路由或任何其他功能。

Artisan 命令行接口可以很容易地透过 `make:provider` 产生新的提供者：

	php artisan make:provider RiakServiceProvider

### 注册者方法

现在，让我们来看看基本的服务提供者：

	<?php namespace App\Providers;

	use Riak\Connection;
	use Illuminate\Support\ServiceProvider;

	class RiakServiceProvider extends ServiceProvider {

		/**
		 * 在容器中注册绑定。
		 *
		 * @return void
		 */
		public function register()
		{
			$this->app->singleton('Riak\Contracts\Connection', function($app)
			{
				return new Connection($app['config']['riak']);
			});
		}

	}

这个服务提供者只定义了一个 `register` 方法，并在服务容器中使用此方法定义了一份 `Riak\Contracts\Connection` 的实作。若你还不了解服务容器是如何运作的，不用担心，[我们很快会提到它](/docs/5.0/container)。

此类别位于 `App\Providers` 命名空间之下，因为这是 Laravel 中默认服务提供者所在的位置。然而，你可以随自己的需要改变它。你的服务提供者可被置于任何 Composer 能自动加载的位置。

### 启动方法

所以，若我们需要在服务提供者中注册一个事件监听器，该怎么做？它应该在 `boot` 方法中完成。**这个方法会在所有的服务提供者注册后才被调用**，这让你能取用框架中所有其他已注册过的服务。

	<?php namespace App\Providers;

	use Event;
	use Illuminate\Support\ServiceProvider;

	class EventServiceProvider extends ServiceProvider {

		/**
		 * 执行注册后的启动服务。
		 *
		 * @return void
		 */
		public function boot()
		{
			Event::listen('SomeEvent', 'SomeEventHandler');
		}

		/**
		 * 在容器中注册绑定。
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}

	}

我们可以对 `boot` 方法中的相依作型别暗示。服务容器会自动注入任何你所需要的相依：

	use Illuminate\Contracts\Events\Dispatcher;

	public function boot(Dispatcher $events)
	{
		$events->listen('SomeEvent', 'SomeEventHandler');
	}

<a name="registering-providers"></a>
## 注册提供者

所有的服务提供者都在 `config/app.php` 此一设置档中被注册。此档包含了一个 `providers` 数组，你可以在其中列出你所有服务提供者的名称。此数组默认会列出一组 Laravel 的核心服务提供者。这些提供者启动了 Laravel 的核心组件，例如邮件寄送者、队列、缓存及其他等等。

要注册你的提供者，只要把它加入此数组：

	'providers' => [
		// 其他的服务提供者

		'App\Providers\AppServiceProvider',
	],

<a name="deferred-providers"></a>
## 缓载提供者

若你的提供者**仅仅**用于绑定注册到[服务容器](/docs/5.0/container)，你可以选择延缓其注册，直到真正需要其中注册的绑定才加载。延缓像这样的提供者加载可增进应用程序的性能，因为这样就不用每个请求都从文件系统中将其加载。

要延缓提供者加载，将 `defer` 性质设为 `true`，并定义一个 `provides` 方法。 `provides` 方法应回传提供者所注册的服务容器绑定。

	<?php namespace App\Providers;

	use Riak\Connection;
	use Illuminate\Support\ServiceProvider;

	class RiakServiceProvider extends ServiceProvider {

		/**
		 * 指定是否延缓提供者加载。
		 *
		 * @var bool
		 */
		protected $defer = true;

		/**
		 * 注册服务提供者。
		 *
		 * @return void
		 */
		public function register()
		{
			$this->app->singleton('Riak\Contracts\Connection', function($app)
			{
				return new Connection($app['config']['riak']);
			});
		}

		/**
		 * 取得提供者所提供的服务。
		 *
		 * @return array
		 */
		public function provides()
		{
			return ['Riak\Contracts\Connection'];
		}

	}

Laravel 编译并保存所有由延缓服务提供者所提供的服务清单，以及其服务提供者的类别名称。只有在当你企图解析其中的服务时， Laravel 才会加载服务提供者。
