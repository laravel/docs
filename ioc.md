# IoC 容器

- [介紹](#introduction)
- [基本用法](#basic-usage)
- [何處註冊綁定](#where-to-register)
- [自動解析](#automatic-resolution)
- [應用](#practical-usage)
- [Service Providers](#service-providers)
- [容器事件](#container-events)

<a name="introduction"></a>
## Introduction

Laravel 的依賴反轉 ( IoC, inversion of control ) 容器是管理類別依賴的強力工具。 依賴注入 ( Dependency injection ) 是一種移除 hard-coded 類別依賴的方式。相較之下，在執行的時候才注入依賴，
可以擁有更好的彈性，在替換依賴實體時相當容易。

理解 Laravel IoC 容器對於建立強力且大型的應用程式，以及改進 Laravel 核心是很重要的。

<a name="basic-usage"></a>
## 基本用法

#### 綁定型別到容器

IoC 容器有兩種解析依賴的方式：經由閉合函數或自動解析。我們將先探索閉合函數的用法。首先，綁定一個「型別」到容器：

	App::bind('foo', function($app)
	{
		return new FooBar;
	});

#### 從容器解析型別

	$value = App::make('foo');

當 `App::make` 方法被呼叫，綁定的閉合函數會被呼叫並返回結果。

#### 綁定「共享」的型別到容器 

有時候，你可能希望綁定到容器的型別只會被解析一次，之後的呼叫都返回相同的實體：

	App::singleton('foo', function()
	{
		return new FooBar;
	});

#### 綁定已存在的實體到容器

你也可以使用 `instance` 方法，綁定一個已經存在的實體到容器：

	$foo = new Foo;

	App::instance('foo', $foo);

<a name="where-to-register"></a>
## 何處註冊綁定

IoC 綁定跟「註冊事件處理」或是「註冊 router 」一樣，通常稱為「起始碼」。換句話說，IoC 綁定後等待請求，在 router 或 controller 呼叫時才實際執行。像其他的「起始碼」一樣，`start` 檔案總是註冊 IoC 綁定的一個選擇。或者，你可以建立一個 `app/ioc.php` 檔案（檔名不重要），並且從 `start` 檔案引入。

如果你的應用程式有很多 IoC 綁定，或是想要分門別類，在不同檔案組織綁定，你可以註冊綁定在 [service provider](#service-providers)。

<a name="automatic-resolution"></a>
## 自動解析

在很多情境下，IoC 容器不需要額外設定就有能力自動解析類別。例如：

	class FooBar {

		public function __construct(Baz $baz)
		{
			$this->baz = $baz;
		}

	}

	$fooBar = App::make('FooBar');

雖然我們沒有註冊 FooBar 類別綁定到容器，它還是可以解析類別，甚至自動注入 `Baz` ！

如果容器裡沒有找到對應的型別綁定，容器會利用 PHP 的 Reflection 檢查類別，並且解讀傳入建構子的型別提示。利用這些資訊，讓容器可以自動建立類別實體。

#### 綁定實體的介面

然而，有些時候，一個類別可能需要依賴介面，而不是一個「具體的型別」。這些情況下，`App::bind` 方法用來通知容器要注入哪個介面實體：

	App::bind('UserRepositoryInterface', 'DbUserRepository');

考慮以下的 controller：

	class UserController extends BaseController {

		public function __construct(UserRepositoryInterface $users)
		{
			$this->users = $users;
		}

	}

既然我們已經綁定 `UserRepositoryInterface` 到一個具體型別，`DbUserRepository` 會在 controller 建立時自動注入。

<a name="practical-usage"></a>
## 應用

在 Laravel 裡，很多時候使用 IoC 容器，可以增加應用程式的彈性與可測試性。一個基本的範例是用在解析 controller。所有的 controller 都會經由 IoC 容器解析，意味著你可以在 controller 建構子注入型別提示依賴，然後依賴就會自動被注入。

#### 注入型別提示 ( Type-Hinting ) 依賴到 Controller

	class OrderController extends BaseController {

		public function __construct(OrderRepository $orders)
		{
			$this->orders = $orders;
		}

		public function getIndex()
		{
			$all = $this->orders->all();

			return View::make('orders', compact('all'));
		}

	}

在這個範例裡， `OrderRepository` 類別會自動被注入到 controller。意味著在[單元測試](/docs/testing)時，可以綁定一個 "mock" 的 `OrderRepository` 到容器裡，之後被注入到  controller，讓你不用在測試時一定要和資料庫層互動。

#### 其他 Ioc 應用範例

[Filters](/docs/routing#route-filters)，[composers](/docs/responses#view-composers)，和[事件處理](/docs/events#using-classes-as-listeners)也可以使用 IoC 容器解析。只要在註冊的時候設定要使用的類別名稱：

	Route::filter('foo', 'FooFilter');

	View::composer('foo', 'FooComposer');

	Event::listen('foo', 'FooHandler');

<a name="service-providers"></a>
## Service Providers

Service providers 是一個很好的方式，可以把相關的 IoC 註冊放到到一個地方。可以將 service provider 想像成是一個在應用程式裡啟動元件的方式。你可以在裡面註冊自定的會員認證，綁定應用程式的 repository 類別到 IoC 容器，或甚至設定自定的 Artisan 指令。

事實上，大部份的 Laravel 核心元件都有 service provider，所有被註冊的 service providers 都列在 `app/config/app.php` 設定檔的 `providers` 陣列裡。

#### 定義一個 Service Provider

要建立一個 service provider，只要繼承 `Illuminate\Support\ServiceProvider` 類別，然後在裡面定義一個 `register` 方法：

	use Illuminate\Support\ServiceProvider;

	class FooServiceProvider extends ServiceProvider {

		public function register()
		{
			$this->app->bind('foo', function()
			{
				return new Foo;
			});
		}

	}

注意，在 `register` 方法裡，經由 `$this->app` 使用 IoC 容器。當你建立了一個 provider 而且準備要註冊到你的應用程式裡時，只要把它加到你的 `app` 設定檔的 `providers` 陣列裡即可。

#### 在執行期間註冊 Service Provider

你也可以使用 `App::register` 在執行期間註冊 service provider ：

	App::register('FooServiceProvider');

<a name="container-events"></a>
## 容器事件

#### 註冊解析事件的監聽

每當容器解析一個物件時就會觸發事件，你可以使用 `resolving` 方法監聽這個事件：

	App::resolvingAny(function($object)
	{
		//
	});

	App::resolving('foo', function($foo)
	{
		//
	});

注意，被解析的物件會被傳到閉合函式。
