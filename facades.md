# Facades

- [介紹](#introduction)
- [解釋](#explanation)
- [實際用法](#practical-usage)
- [建立 Facades](#creating-facades)
- [模擬 Facades](#mocking-facades)
- [Facade 類別參考](#facade-class-reference)

<a name="introduction"></a>
## 介紹

Facades 提供一個靜態介面給在應用程式的 [IoC 容器](/docs/5.0/container) 中可以取用的類別。Laravel 附帶許多 facades，甚至你可能已經在不知情的狀況下使用過它們！Laravel 的「facades」作為在 IoC 容器裡面的基底類別的靜態代理，提供的語法有簡潔、易表達的優點，同時維持比傳統的靜態方法更高的可測試性和彈性。

有時，你或許會希望為應用程式和套件建立自己的 facades，所以讓我們來探索這些類別的概念、開發和用法。

> **注意：** 在深入了解 facades 之前，強烈建議你先熟悉 Laravel [IoC 容器](/docs/5.0/container).

<a name="explanation"></a>
## 解釋

在 Laravel 應用程式的環境中，facade 是個提供從容器存取物件的類別。`Facade` 類別是讓這個機制可以運作的原因。Laravel 的 facades 和你建立的任何客製化 facades，將會繼承基本的 `Facade` 類別。

你的 facade 類別只需要去實作一個方法：`getFacadeAccessor`。`getFacadeAccessor` 方法的工作是定義要從容器解析什麼。基本的 `Facade` 類別利用 `__callStatic()` 魔術方法來從你的 facade 呼叫到解析出來的物件。

所以當你對 facade 呼叫，例如 `Cache::get`，Laravel 從 IoC 容器解析快取管理類別出來，並對該類別呼叫 `get` 方法。用科技術語來說，Laravel Facades 是使用 Laravel IoC 容器作為服務定位器的便捷語法。

<a name="practical-usage"></a>
## 實際用法

在下面的例子，對 Laravel 快取系統進行呼叫。簡單看過去這程式碼，有人可能會以為靜態方法 `get` 是對 `Cache` 類別呼叫。

	$value = Cache::get('key');

然而，如果我們去看 `Illuminate\Support\Facades\Cache` 類別，你將會看到它沒有靜態方法 `get`：

	class Cache extends Facade {

		/**
		 * 取得元件的註冊名稱
		 *
		 * @return string
		 */
		protected static function getFacadeAccessor() { return 'cache'; }

	}

Cache 類別繼承基本的 `Facade` 類別並定義一個 `getFacadeAccessor()` 方法。記住，這個方法的工作是回傳 IoC 綁定的名稱。

當使用者在 `Cache` 的 facade 上參考任何的靜態方法，Laravel 會從 IoC 容器解析被綁定的 `cache` ，並對該物件執行被請求的方法 (在這個例子中， `get`)。

所以我們的 `Cache::get` 呼叫可以被重寫成像這樣：

	$value = $app->make('cache')->get('key');

#### 匯入 Facades

記住，如果你在控制器有使用命名空間的狀況使用 facade，你會需要匯入 facade 類別進入命名空間。所有的 facades 存在於全域命名空間：

	<?php namespace App\Http\Controllers;

	use Cache;

	class PhotosController extends Controller {

		/**
		 * 取得所有的應用程式相片。
		 *
		 * @return Response
		 */
		public function index()
		{
			$photos = Cache::get('photos');

			//
		}

	}

<a name="creating-facades"></a>
## 建立 Facades

為你自己的應用程式或套件建立 facade 是很簡單的。你只需要 3 個東西：

- 一個 IoC 綁定。
- 一個 facade 類別。
- 一個 facade 別名設定。

讓我們來看個例子。這裡有一個定義為 `PaymentGateway\Payment` 的類別。

	namespace PaymentGateway;

	class Payment {

		public function process()
		{
			//
		}

	}

我們需要可以從 IoC 容器解析出這個類別。所以，讓我們來加上一個綁定到服務提供者：

	App::bind('payment', function()
	{
		return new \PaymentGateway\Payment;
	});

註冊這個綁定的好方式是建立新的 [服務提供者](/docs/5.0/container#service-providers) 命名為 `PaymentServiceProvider`，並把這個綁定加到 `register` 方法。再來你可以設定 Laravel 從 `config/app.php` 設定檔載入你的服務提供者。

接下來，我們可以建立我們自己的 facade 類別：

	use Illuminate\Support\Facades\Facade;

	class Payment extends Facade {

		protected static function getFacadeAccessor() { return 'payment'; }

	}

最後，如果我們希望，可以在 `config/app.php` 設定檔為 facade 加個別名到 `aliases` 陣列。現在我們可以在 `Payment` 類別的實例上呼叫 `process` 方法。

	Payment::process();

### 自動載入別名的附註

在 `aliases` 陣列中的類別在某些實例中不能使用，因為 [PHP 將不會嘗試去自動載入未定義的類型暗示類別](https://bugs.php.net/bug.php?id=39003)。如果 `\ServiceWrapper\ApiTimeoutException` 命別名為 `ApiTimeoutException`，即便有例外被拋出，在 `\ServiceWrapper` 命名空間外面的 `catch(ApiTimeoutException $e)` 將永遠捕捉不到例外。類似的問題在有類型暗示的別名類別一樣會發生。唯一的替代方案就是放棄別名並用 `use` 在每一個檔案的最上面引入你希望暗示類型的類別。

<a name="mocking-facades"></a>
## 模擬 Facades

單元測試是為什麼現在 facades 採用這樣的工作方式的重要面向。事實上，可測試性甚至是 facades 存在的主要理由。想要獲得更多資訊，請查看文件的 [模擬 facades](/docs/testing#mocking-facades) 章節。

<a name="facade-class-reference"></a>
## Facade 類別參考

你將會在下面找到每一個 facade 和它的基底類別。這是個可以從一個給定的 facade 根源快速地深入 API 文件的有用工具。可應用的 [IoC 綁定](/docs/5.0/container) 關鍵字也包含在裡面。

Facade  |  Class  |  IoC Binding
------------- | ------------- | -------------
App  |  [Illuminate\Foundation\Application](http://laravel.com/api/5.0/Illuminate/Foundation/Application.html)  | `app`
Artisan  |  [Illuminate\Console\Application](http://laravel.com/api/5.0/Illuminate/Console/Application.html)  |  `artisan`
Auth  |  [Illuminate\Auth\AuthManager](http://laravel.com/api/5.0/Illuminate/Auth/AuthManager.html)  |  `auth`
Auth (實例)  |  [Illuminate\Auth\Guard](http://laravel.com/api/5.0/Illuminate/Auth/Guard.html)  |
Blade  |  [Illuminate\View\Compilers\BladeCompiler](http://laravel.com/api/5.0/Illuminate/View/Compilers/BladeCompiler.html)  |  `blade.compiler`
Cache  |  [Illuminate\Cache\Repository](http://laravel.com/api/5.0/Illuminate/Cache/Repository.html)  |  `cache`
Config  |  [Illuminate\Config\Repository](http://laravel.com/api/5.0/Illuminate/Config/Repository.html)  |  `config`
Cookie  |  [Illuminate\Cookie\CookieJar](http://laravel.com/api/5.0/Illuminate/Cookie/CookieJar.html)  |  `cookie`
Crypt  |  [Illuminate\Encryption\Encrypter](http://laravel.com/api/5.0/Illuminate/Encryption/Encrypter.html)  |  `encrypter`
DB  |  [Illuminate\Database\DatabaseManager](http://laravel.com/api/5.0/Illuminate/Database/DatabaseManager.html)  |  `db`
DB (實例)  |  [Illuminate\Database\Connection](http://laravel.com/api/5.0/Illuminate/Database/Connection.html)  |
Event  |  [Illuminate\Events\Dispatcher](http://laravel.com/api/5.0/Illuminate/Events/Dispatcher.html)  |  `events`
File  |  [Illuminate\Filesystem\Filesystem](http://laravel.com/api/5.0/Illuminate/Filesystem/Filesystem.html)  |  `files`
Form  |  [Illuminate\Html\FormBuilder](http://laravel.com/api/5.0/Illuminate/Html/FormBuilder.html)  |  `form`
Hash  |  [Illuminate\Hashing\HasherInterface](http://laravel.com/api/5.0/Illuminate/Hashing/HasherInterface.html)  |  `hash`
HTML  |  [Illuminate\Html\HtmlBuilder](http://laravel.com/api/5.0/Illuminate/Html/HtmlBuilder.html)  |  `html`
Input  |  [Illuminate\Http\Request](http://laravel.com/api/5.0/Illuminate/Http/Request.html)  |  `request`
Lang  |  [Illuminate\Translation\Translator](http://laravel.com/api/5.0/Illuminate/Translation/Translator.html)  |  `translator`
Log  |  [Illuminate\Log\Writer](http://laravel.com/api/5.0/Illuminate/Log/Writer.html)  |  `log`
Mail  |  [Illuminate\Mail\Mailer](http://laravel.com/api/5.0/Illuminate/Mail/Mailer.html)  |  `mailer`
Paginator  |  [Illuminate\Pagination\Factory](http://laravel.com/api/5.0/Illuminate/Pagination/Factory.html)  |  `paginator`
Paginator (實例)  |  [Illuminate\Pagination\Paginator](http://laravel.com/api/5.0/Illuminate/Pagination/Paginator.html)  |
Password  |  [Illuminate\Auth\Passwords\PasswordBroker](http://laravel.com/api/5.0/Illuminate/Auth/Passwords/PasswordBroker.html)  |  `auth.reminder`
Queue  |  [Illuminate\Queue\QueueManager](http://laravel.com/api/5.0/Illuminate/Queue/QueueManager.html)  |  `queue`
Queue (實例) |  [Illuminate\Queue\QueueInterface](http://laravel.com/api/5.0/Illuminate/Queue/QueueInterface.html)  |
Queue (基底類別) |  [Illuminate\Queue\Queue](http://laravel.com/api/5.0/Illuminate/Queue/Queue.html)  |
Redirect  |  [Illuminate\Routing\Redirector](http://laravel.com/api/5.0/Illuminate/Routing/Redirector.html)  |  `redirect`
Redis  |  [Illuminate\Redis\Database](http://laravel.com/api/5.0/Illuminate/Redis/Database.html)  |  `redis`
Request  |  [Illuminate\Http\Request](http://laravel.com/api/5.0/Illuminate/Http/Request.html)  |  `request`
Response  |  [Illuminate\Support\Facades\Response](http://laravel.com/api/5.0/Illuminate/Support/Facades/Response.html)  |
Route  |  [Illuminate\Routing\Router](http://laravel.com/api/5.0/Illuminate/Routing/Router.html)  |  `router`
Schema  |  [Illuminate\Database\Schema\Blueprint](http://laravel.com/api/5.0/Illuminate/Database/Schema/Blueprint.html)  |
Session  |  [Illuminate\Session\SessionManager](http://laravel.com/api/5.0/Illuminate/Session/SessionManager.html)  |  `session`
Session (實例)  |  [Illuminate\Session\Store](http://laravel.com/api/5.0/Illuminate/Session/Store.html)  |
SSH  |  [Illuminate\Remote\RemoteManager](http://laravel.com/api/5.0/Illuminate/Remote/RemoteManager.html)  |  `remote`
SSH (實例)  |  [Illuminate\Remote\Connection](http://laravel.com/api/5.0/Illuminate/Remote/Connection.html)  |
URL  |  [Illuminate\Routing\UrlGenerator](http://laravel.com/api/5.0/Illuminate/Routing/UrlGenerator.html)  |  `url`
Validator  |  [Illuminate\Validation\Factory](http://laravel.com/api/5.0/Illuminate/Validation/Factory.html)  |  `validator`
Validator (實例)  |  [Illuminate\Validation\Validator](http://laravel.com/api/5.0/Illuminate/Validation/Validator.html) |
View  |  [Illuminate\View\Factory](http://laravel.com/api/5.0/Illuminate/View/Factory.html)  |  `view`
View (實例)  |  [Illuminate\View\View](http://laravel.com/api/5.0/Illuminate/View/View.html)  |
