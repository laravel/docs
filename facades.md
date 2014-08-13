# Facades

- [介紹](#introduction)
- [解釋](#explanation)
- [實際用法](#practical-usage)
- [建立 Facades](#creating-facades)
- [模擬 Facades](#mocking-facades)
- [Facade 類別參考](#facade-class-reference)

<a name="introduction"></a>
## 介紹

Facades 提供一個靜態介面讓類別可以在應用程式的 [IoC 容器](/docs/ioc) 裡運用。 Laravel 附帶許多 facades，甚至你可能已經在使用它們即使你並不知道! Laravel 的 "facades" 在 IoC 容器裡面作為的基底類別的靜態代理，提供有簡潔、易表達優點的語法，同時維持比傳統的靜態方法更高的可測試性和彈性。

你偶爾或許會希望為你的應用程式和套件建立自己的 facades，所以讓我們來探索這些類別的概念、開發和用法。

> **備註:** 在深入 facades 之前，強烈建議你先熟悉 Laravel [IoC 容器](/docs/ioc)。

<a name="explanation"></a>
## 解釋

在 Laravel 應用程式的環境中， facade 是個提供從容器存取物件的類別。 使這個機制可以運作的原因在 `Facade` 類別中。 Laravel 的 facades 和任何你建立的客製化 facades，將會繼承基本的 `Facade` 類別。

你的 facade 類別只需要去實作一個方法： `getFacadeAccessor`。 `getFacadeAccessor` 方法的工作是定義要從容器解析什麼。 基本的 `Facade` 類別利用 `__callStatic()` 魔術方法去從你的 facade 呼叫到解析物件。

所以當你對 facade 呼叫，例如 `Cache::get`， Laravel 從 IoC 容器解析快取管理類別出來，並對類別呼叫 `get` 方法。 用科技術語來說， Laravel Facades 是使用 Laravel IoC 容器作為服務定位器的便捷語法。

<a name="practical-usage"></a>
## 實際用法

在下面的例子，對 Laravel 快取系統進行呼叫。 簡單看過這程式碼，有人可能會以為靜態方法 `get` 是被 `Cache` 類別呼叫。

	$value = Cache::get('key');

然而，如果我們去看 `Illuminate\Support\Facades\Cache` 類別， 你將會看到他沒有靜態方法 `get`:

	class Cache extends Facade {

		/**
		 * Get the registered name of the component.
		 *
		 * @return string
		 */
		protected static function getFacadeAccessor() { return 'cache'; }

	}

Cache 類別繼承基本的 `Facade` 類別並定義方法 `getFacadeAccessor()`。 記住，這個方法的工作是回傳 IoC 綁定的名稱。

當使用者參考 `Cache` facade 的任何靜態方法， Laravel 會從 IoC 容器解析被綁定 `cache` ，並對該物件執行被請求的方法 (在這個例子， `get`)。

所以我們的 `Cache::get` 呼叫可以被重寫成這樣：

	$value = $app->make('cache')->get('key');

<a name="creating-facades"></a>
## 建立 Facades

為你的應用程式或套件建立 facade 是很簡單的。 你只需要 3 個東西：

- 一個 IoC 綁定。
- 一個 facade 類別。
- 一個 facade 別名設定。

讓我們來看個例子。 這裡我們有一個定義為 `PaymentGateway\Payment` 的類別。

	namespace PaymentGateway;

	class Payment {

		public function process()
		{
			//
		}

	}

這個類別可以存在在你的 `app/models` 資料夾，或者任何其他 Composer 知道如何自動載入的資料夾。

我們需要可以從 IoC 容器解析出這個類別。 所以，讓我們來加個綁定：

	App::bind('payment', function()
	{
		return new \PaymentGateway\Payment;
	});

註冊這個綁定的好方式是建立新的 [服務提供者](/docs/ioc#service-providers) 命名為 `PaymentServiceProvider`，並把這個綁定加到 `register` 方法。 再來你可以從 `app/config/app.php` 檔案設定讓 Laravel 載入你的服務提供者。

接下來，我們可以建立我們自己的 facade 類別：

	use Illuminate\Support\Facades\Facade;

	class Payment extends Facade {

		protected static function getFacadeAccessor() { return 'payment'; }

	}

最後，如果我們希望，我們可以在 `app/config/app.php` 設定檔案為我們的 facade 加個別名到 `aliases` 陣列。 現在我們可以對 `Payment` 類別的實體呼叫 `process` 方法。

	Payment::process();

### 自動載入別名的附註

在 `aliases` 陣列中的類別在某些實體中不能使用，因為 [PHP 將不會嘗試去自動載入未定義的類型暗示類別](https://bugs.php.net/bug.php?id=39003)。 如果 `\ServiceWrapper\ApiTimeoutException` 命別名為 `ApiTimeoutException`， 在 `\ServiceWrapper` 命名空間外面的  `catch(ApiTimeoutException $e)` 將永遠捕捉不到例外，即便有例外被拋出。類似的問題在有類型暗示的別名類別模型一樣會發生。 唯一的解決辦法就是放棄別名並用 `use` 在每一個檔案的最上面引入你希望暗示類型的類別。

<a name="mocking-facades"></a>
## 模擬 Facades

單元測試是為什麼現在 facades 採用這樣的工作方式的重要面向。 事實上，可測試性甚至是 facades 存在的主要理由。 想要獲得更多資訊，請查看文件的 [mocking facades](/docs/testing#mocking-facades) 部分。

<a name="facade-class-reference"></a>
## Facade 類別參考

你將會在下面找到每一個 facade 和它的基底類別。 這是個可以從一個給定的 facade 根源快速地深入 API 文件的有用工具。 可應用的 [IoC 綁定](/docs/ioc) 關鍵字也包含在裡面。

Facade  |  Class  |  IoC Binding
------------- | ------------- | -------------
App  |  [Illuminate\Foundation\Application](http://laravel.com/api/4.2/Illuminate/Foundation/Application.html)  | `app`
Artisan  |  [Illuminate\Console\Application](http://laravel.com/api/4.2/Illuminate/Console/Application.html)  |  `artisan`
Auth  |  [Illuminate\Auth\AuthManager](http://laravel.com/api/4.2/Illuminate/Auth/AuthManager.html)  |  `auth`
Auth (Instance)  |  [Illuminate\Auth\Guard](http://laravel.com/api/4.2/Illuminate/Auth/Guard.html)  |
Blade  |  [Illuminate\View\Compilers\BladeCompiler](http://laravel.com/api/4.2/Illuminate/View/Compilers/BladeCompiler.html)  |  `blade.compiler`
Cache  |  [Illuminate\Cache\Repository](http://laravel.com/api/4.2/Illuminate/Cache/Repository.html)  |  `cache`
Config  |  [Illuminate\Config\Repository](http://laravel.com/api/4.2/Illuminate/Config/Repository.html)  |  `config`
Cookie  |  [Illuminate\Cookie\CookieJar](http://laravel.com/api/4.2/Illuminate/Cookie/CookieJar.html)  |  `cookie`
Crypt  |  [Illuminate\Encryption\Encrypter](http://laravel.com/api/4.2/Illuminate/Encryption/Encrypter.html)  |  `encrypter`
DB  |  [Illuminate\Database\DatabaseManager](http://laravel.com/api/4.2/Illuminate/Database/DatabaseManager.html)  |  `db`
DB (Instance)  |  [Illuminate\Database\Connection](http://laravel.com/api/4.2/Illuminate/Database/Connection.html)  |
Event  |  [Illuminate\Events\Dispatcher](http://laravel.com/api/4.2/Illuminate/Events/Dispatcher.html)  |  `events`
File  |  [Illuminate\Filesystem\Filesystem](http://laravel.com/api/4.2/Illuminate/Filesystem/Filesystem.html)  |  `files`
Form  |  [Illuminate\Html\FormBuilder](http://laravel.com/api/4.2/Illuminate/Html/FormBuilder.html)  |  `form`
Hash  |  [Illuminate\Hashing\HasherInterface](http://laravel.com/api/4.2/Illuminate/Hashing/HasherInterface.html)  |  `hash`
HTML  |  [Illuminate\Html\HtmlBuilder](http://laravel.com/api/4.2/Illuminate/Html/HtmlBuilder.html)  |  `html`
Input  |  [Illuminate\Http\Request](http://laravel.com/api/4.2/Illuminate/Http/Request.html)  |  `request`
Lang  |  [Illuminate\Translation\Translator](http://laravel.com/api/4.2/Illuminate/Translation/Translator.html)  |  `translator`
Log  |  [Illuminate\Log\Writer](http://laravel.com/api/4.2/Illuminate/Log/Writer.html)  |  `log`
Mail  |  [Illuminate\Mail\Mailer](http://laravel.com/api/4.2/Illuminate/Mail/Mailer.html)  |  `mailer`
Paginator  |  [Illuminate\Pagination\Factory](http://laravel.com/api/4.2/Illuminate/Pagination/Factory.html)  |  `paginator`
Paginator (Instance)  |  [Illuminate\Pagination\Paginator](http://laravel.com/api/4.2/Illuminate/Pagination/Paginator.html)  |
Password  |  [Illuminate\Auth\Reminders\PasswordBroker](http://laravel.com/api/4.2/Illuminate/Auth/Reminders/PasswordBroker.html)  |  `auth.reminder`
Queue  |  [Illuminate\Queue\QueueManager](http://laravel.com/api/4.2/Illuminate/Queue/QueueManager.html)  |  `queue`
Queue (Instance) |  [Illuminate\Queue\QueueInterface](http://laravel.com/api/4.2/Illuminate/Queue/QueueInterface.html)  |
Queue (Base Class) |  [Illuminate\Queue\Queue](http://laravel.com/api/4.2/Illuminate/Queue/Queue.html)  |
Redirect  |  [Illuminate\Routing\Redirector](http://laravel.com/api/4.2/Illuminate/Routing/Redirector.html)  |  `redirect`
Redis  |  [Illuminate\Redis\Database](http://laravel.com/api/4.2/Illuminate/Redis/Database.html)  |  `redis`
Request  |  [Illuminate\Http\Request](http://laravel.com/api/4.2/Illuminate/Http/Request.html)  |  `request`
Response  |  [Illuminate\Support\Facades\Response](http://laravel.com/api/4.2/Illuminate/Support/Facades/Response.html)  |
Route  |  [Illuminate\Routing\Router](http://laravel.com/api/4.2/Illuminate/Routing/Router.html)  |  `router`
Schema  |  [Illuminate\Database\Schema\Blueprint](http://laravel.com/api/4.2/Illuminate/Database/Schema/Blueprint.html)  |
Session  |  [Illuminate\Session\SessionManager](http://laravel.com/api/4.2/Illuminate/Session/SessionManager.html)  |  `session`
Session (Instance)  |  [Illuminate\Session\Store](http://laravel.com/api/4.2/Illuminate/Session/Store.html)  |
SSH  |  [Illuminate\Remote\RemoteManager](http://laravel.com/api/4.2/Illuminate/Remote/RemoteManager.html)  |  `remote`
SSH (Instance)  |  [Illuminate\Remote\Connection](http://laravel.com/api/4.2/Illuminate/Remote/Connection.html)  |
URL  |  [Illuminate\Routing\UrlGenerator](http://laravel.com/api/4.2/Illuminate/Routing/UrlGenerator.html)  |  `url`
Validator  |  [Illuminate\Validation\Factory](http://laravel.com/api/4.2/Illuminate/Validation/Factory.html)  |  `validator`
Validator (Instance)  |  [Illuminate\Validation\Validator](http://laravel.com/api/4.2/Illuminate/Validation/Validator.html) |
View  |  [Illuminate\View\Factory](http://laravel.com/api/4.2/Illuminate/View/Factory.html)  |  `view`
View (Instance)  |  [Illuminate\View\View](http://laravel.com/api/4.2/Illuminate/View/View.html)  |
