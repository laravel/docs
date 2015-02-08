# 服務提供者

- [簡介](#introduction)
- [基本提供者範例](#basic-provider-example)
- [註冊提供者](#registering-providers)
- [緩載提供者](#deferred-providers)

<a name="introduction"></a>
## 簡介

服務提供者是所有 Laravel 應用程式的啟動中心。你的應用程式，以及所有 Laravel 的核心服務，都是透過服務提供者啟動。

但我們所說的「啟動」指的是什麼？一般而言，我們指**註冊**事物，包括註冊服務容器綁定、事件監聽器、過濾器，甚至路由。服務提供者是你的應用程式設定中心所在。

如果你開啟包含於 Laravel 中 `config/app.php` 此一檔案，你會看到 `providers` 陣列。這些是所有將載入至你的應用程式裡的服務提供者類別。當然，它們之中有很多屬於「緩載」提供者，意思是除非真正需要它們所提供的服務，否則它們並不會在每一個請求中都被載入。

在這份概述中，你會學到如何編寫你自己的服務提供者，並將它們註冊於你的 Laravel 應用程式。

<a name="basic-provider-example"></a>
## 基本提供者範例

所有的服務提供者都應繼承 `Illuminate\Support\ServiceProvider` 此一類別。在這個抽象類別中，至少必須定義一個方法： `register` 。在 `register` 方法中，應該**只綁定服務到[服務容器](/docs/5.0/container)之中**。你永遠不該試圖在 `register` 方法中註冊任何事件監聽器、路由或任何其他功能。

Artisan 命令行介面可以很容易地透過 `make:provider` 產生新的提供者：

	php artisan make:provider RiakServiceProvider

### 註冊者方法

現在，讓我們來看看基本的服務提供者：

	<?php namespace App\Providers;

	use Riak\Connection;
	use Illuminate\Support\ServiceProvider;

	class RiakServiceProvider extends ServiceProvider {

		/**
		 * 在容器中註冊綁定。
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

這個服務提供者只定義了一個 `register` 方法，並在服務容器中使用此方法定義了一份 `Riak\Contracts\Connection` 的實作。若你還不瞭解服務容器是如何運作的，不用擔心，[我們很快會提到它](/docs/5.0/container)。

此類別位於 `App\Providers` 命名空間之下，因為這是 Laravel 中預設服務提供者所在的位置。然而，你可以隨自己的需要改變它。你的服務提供者可被置於任何 Composer 能自動載入的位置。

### 啟動方法

所以，若我們需要在服務提供者中註冊一個事件監聽器，該怎麼做？它應該在 `boot` 方法中完成。**這個方法會在所有的服務提供者註冊後才被呼叫**，這讓你能取用框架中所有其他已註冊過的服務。

	<?php namespace App\Providers;

	use Event;
	use Illuminate\Support\ServiceProvider;

	class EventServiceProvider extends ServiceProvider {

		/**
		 * 執行註冊後的啟動服務。
		 *
		 * @return void
		 */
		public function boot()
		{
			Event::listen('SomeEvent', 'SomeEventHandler');
		}

		/**
		 * 在容器中註冊綁定。
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}

	}

我們可以對 `boot` 方法中的相依作型別暗示。服務容器會自動注入任何你所需要的相依：

	use Illuminate\Contracts\Events\Dispatcher;

	public function boot(Dispatcher $events)
	{
		$events->listen('SomeEvent', 'SomeEventHandler');
	}

<a name="registering-providers"></a>
## 註冊提供者

所有的服務提供者都在 `config/app.php` 此一設定檔中被註冊。此檔包含了一個 `providers` 陣列，你可以在其中列出你所有服務提供者的名稱。此陣列預設會列出一組 Laravel 的核心服務提供者。這些提供者啟動了 Laravel 的核心元件，例如郵件寄送者、隊列、快取及其他等等。

要註冊你的提供者，只要把它加入此陣列：

	'providers' => [
		// 其他的服務提供者

		'App\Providers\AppServiceProvider',
	],

<a name="deferred-providers"></a>
## 緩載提供者

若你的提供者**僅僅**用於綁定註冊到[服務容器](/docs/5.0/container)，你可以選擇延緩其註冊，直到真正需要其中註冊的綁定才載入。延緩像這樣的提供者載入可增進應用程式的效能，因為這樣就不用每個請求都從檔案系統中將其載入。

要延緩提供者載入，將 `defer` 性質設為 `true`，並定義一個 `provides` 方法。 `provides` 方法應回傳提供者所註冊的服務容器綁定。

	<?php namespace App\Providers;

	use Riak\Connection;
	use Illuminate\Support\ServiceProvider;

	class RiakServiceProvider extends ServiceProvider {

		/**
		 * 指定是否延緩提供者載入。
		 *
		 * @var bool
		 */
		protected $defer = true;

		/**
		 * 註冊服務提供者。
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
		 * 取得提供者所提供的服務。
		 *
		 * @return array
		 */
		public function provides()
		{
			return ['Riak\Contracts\Connection'];
		}

	}

Laravel 編譯並儲存所有由延緩服務提供者所提供的服務清單，以及其服務提供者的類別名稱。只有在當你企圖解析其中的服務時， Laravel 才會載入服務提供者。
