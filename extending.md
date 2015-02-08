# 擴展框架

- [管理者和工廠](#managers-and-factories)
- [快取](#cache)
- [Session](#session)
- [認證](#authentication)
- [基於 IoC 的擴展](#ioc-based-extension)

<a name="managers-and-factories"></a>
## 管理者和工廠

Laravel 有幾個 `Manager` 類別，用來管理創建基於驅動的元件。這些類別包括快取、session 、認證和隊列元件。管理者類別負責基於應用程式的設定建立一個特定的驅動實作。例如，`CacheManager` 類別可以建立 APC 、 Memcached 、檔案和各種其他的快取驅動實作。

這些管理者都擁有 `extend` 方法，可以簡單地用它來注入新的驅動解析功能到管理者。我們將會在下面的例子，隨著如何注入客製化驅動支援給它們，涵蓋這些管理者的內容。

> **注意：** 建議花點時間來探索 Laravel 附帶的各種 `Manager` 類別，例如：`CacheManager` 和 `SessionManager`。看過這些類別將會讓你更徹底了解 Laravel 表面下是如何運作。所有的管理者類別繼承  `Illuminate\Support\Manager` 基底類別，它提供一些有用、常見的功能給每一個管理者。

<a name="cache"></a>
## 快取

為了擴展 Laravel 快取功能，我們將會使用 `CacheManager` 的 `extend` 方法，這方法可以用來綁定一個客製化驅動解析器到管理者，並且是全部的管理者類別通用的。例如，註冊一個新的快取驅動名為「mongo」，我們將執行以下操作：

	Cache::extend('mongo', function($app)
	{
		return Cache::repository(new MongoStore);
	});

傳遞到 `extend` 方法的第一個參數是驅動的名稱。這將會對應到你的 `config/cache.php` 設定檔裡的 `driver` 選項。第二個參數是個應該回傳 `Illuminate\Cache\Repository` 實例的閉包。 `$app` 將會被傳遞到閉包，它是 `Illuminate\Foundation\Application` 和 IoC 容器的實例。

`Cache::extend` 的呼叫可以在新的 Laravel 應用程式預設附帶的 `App\Providers\AppServiceProvider` 的 `boot` 方法中完成，或者你可以建立自己的服務提供者來放置這個擴展 - 記得不要忘記在 `config/app.php` 的提供者陣列註冊提供者。

要建立客製化快取驅動，首先需要實作 `Illuminate\Contracts\Cache\Store` contract 。所以，我們的 MongoDB 快取實作將會看起來像這樣：

	class MongoStore implements Illuminate\Contracts\Cache\Store {

		public function get($key) {}
		public function put($key, $value, $minutes) {}
		public function increment($key, $value = 1) {}
		public function decrement($key, $value = 1) {}
		public function forever($key, $value) {}
		public function forget($key) {}
		public function flush() {}

	}

我們只需要使用 MongoDB 連接來實作這些方法。當實作完成，就可以完成客製化驅動註冊：

	Cache::extend('mongo', function($app)
	{
		return Cache::repository(new MongoStore);
	});

如果你正在考慮要把客製化快取驅動程式碼放在哪裡，請考慮把它放上  Packagist ！或者，你可以在 `app` 的目錄中建立 `Extensions` 命名空間。記得 Laravel 沒有嚴格的應用程式架構，你可以依照喜好自由的組織應用程式。

<a name="session"></a>
## Session

以客製化 session 驅動來擴展 Laravel 跟擴展快取系統一樣簡單。再一次的，我們將會使用 `extend` 方法來註冊客製化程式碼：

	Session::extend('mongo', function($app)
	{
		// Return implementation of SessionHandlerInterface
	});

### 在哪裡擴展 Session

你應該把 session 擴展程式碼放置在 `AppServiceProvider` 的 `boot` 方法裡。

### 實作 Session 擴展

要注意我們的客製化快取驅動應該要實作 `SessionHandlerInterface` 。這個介面只包含少數需要實作的簡單方法。一個基本的 MongoDB 實作會看起來像這樣：

	class MongoHandler implements SessionHandlerInterface {

		public function open($savePath, $sessionName) {}
		public function close() {}
		public function read($sessionId) {}
		public function write($sessionId, $data) {}
		public function destroy($sessionId) {}
		public function gc($lifetime) {}

	}

因為這些方法不像快取的 `StoreInterface` 一樣容易理解，讓我們快速地看過這些方法做些什麼：

- `open` 方法通常會被用在基於檔案的 session 儲存系統。因為 Laravel 附帶一個 `file` session 驅動，幾乎不需要在這個方法放任何東西。你可以讓它留空。PHP 要求我們去實作這個方法，事實上明顯是個差勁的介面設計 (我們將會晚點討論它)。
- `close` 方法，就像 `open` 方法，通常也可以忽略。對大部份的驅動來說，並不需要它。
- `read` 方法應該回傳與給定 `$sessionId` 關聯的 session 資料的字串形態。當你的驅動取回或儲存 session 資料時不需要做任何序列化或進行其他編碼，因為 Laravel 將會為你進行序列化
- `write` 方法應該寫入給定 `$data` 字串與 `$sessionId` 的關聯到一些永久存儲系統，例如：MongoDB、 Dynamo、等等。
- `destroy` 方法應該從永久存儲移除與 `$sessionId` 關聯的資料。
- `gc` 方法應該銷毀所有比給定 `$lifetime` UNIX 時間戳記還舊的 session 資料。對於會自己過期的系統如 Memcached 和 Redis，這個方法可以留空。

當 `SessionHandlerInterface` 實作完成，我們準備好要用 Session 管理者註冊它：

	Session::extend('mongo', function($app)
	{
		return new MongoHandler;
	});

當 session 驅動已經被註冊，我們可以在 `config/session.php` 設定檔使用 `mongo` 驅動。

> **注意：** 記住，如果你寫了個客製化 session 處理器，請在 Packagist 分享它！

<a name="authentication"></a>
## 認證

認證可以用與快取和 session 功能相同的方法擴展。再一次的，使用我們已經熟悉的 `extend` 方法：

	Auth::extend('riak', function($app)
	{
		// 回傳 Illuminate\Contracts\Auth\UserProvider 的實作
	});

`UserProvider` 實作只負責從永久存儲系統抓取 `Illuminate\Contracts\Auth\Authenticatable` 實作，存儲系統例如： MySQL 、 Riak ，等等。這兩個介面讓 Laravel 認證機制無論使用者資料如何儲存或用什麼種類的類別來代表它都能繼續運作。

讓我們來看一下 `UserProvider` contract ：

	interface UserProvider {

		public function retrieveById($identifier);
		public function retrieveByToken($identifier, $token);
		public function updateRememberToken(Authenticatable $user, $token);
		public function retrieveByCredentials(array $credentials);
		public function validateCredentials(Authenticatable $user, array $credentials);

	}

`retrieveById` 函式通常接收一個代表使用者的數字鍵，例如：MySQL 資料庫的自動遞增 ID。這方法應該取得符合 ID 的 `Authenticatable` 實作並回傳。

`retrieveByToken` 函式用使用者唯一的 `$identifier` 和儲存在 `remember_token` 欄位的「記住我」 `$token` 來取得使用者。跟前面的方法一樣，應該回傳 `Authenticatable` 的實作。

`updateRememberToken` 方法用新的 `$token` 更新 `$user` 的 `remember_token` 欄位。新 token 可以是在「記住我」成功地登入時，傳入一個新的 token，或當使用者登出時傳入一個 null。

`retrieveByCredentials` 方法接收當嘗試登入應用程式時，傳遞到 `Auth::attempt` 方法的憑證陣列。這個方法應該接著「查詢」底層使用的永久存儲，找到符合憑證的使用者。這個方法通常會對 `$credentials['username']` 用「 where 」條件查詢。 **這個方法不應該嘗試做任何密碼驗證或認證。**

`validateCredentials` 方法應該藉由比較給定的 `$user` 與 `$credentials` 來驗證使用者。舉例來說，這個方法可以比較 `$user->getAuthPassword()` 字串跟 `Hash::make` 後的 `$credentials['password']`。

現在我們已經看過 `UserProvider` 的每個方法，接著來看一下 `Authenticatable`。記住，提供者應該從 `retrieveById` 和 `retrieveByCredentials` 方法回傳這個介面的實作：

	interface Authenticatable {

		public function getAuthIdentifier();
		public function getAuthPassword();
		public function getRememberToken();
		public function setRememberToken($value);
		public function getRememberTokenName();

	}

這個介面很簡單。 The `getAuthIdentifier` 方法應該回傳使用者的「主鍵」。在 MySQL 後台，同樣，這將會是個自動遞增的主鍵。`getAuthPassword` 應該回傳使用者雜湊過的密碼。這個介面讓認證系統可以與任何使用者類別一起運作，無論你使用什麼 ORM 或儲存抽象層。預設，Laravel 包含一個實作這個介面的 `User` 類別在 `app` 資料夾裡，所以你可以參考這個類別當作實作的例子。

最後，當我們已經實作了 `UserProvider`，我們準備好用 `Auth` facade 來註冊擴展：

	Auth::extend('riak', function($app)
	{
		return new RiakUserProvider($app['riak.connection']);
	});

用 `extend` 方法註冊驅動之後，在你的 `config/auth.php` 設定檔切換到新驅動。

<a name="ioc-based-extension"></a>
## 基於 IoC 的擴展

幾乎每個 Laravel 框架引入的服務提供者都會綁定物件到 IoC 容器中。你可以在 `config/app.php` 設定檔中找到應用程式的服務提供者清單。如果你有時間，你應該瀏覽過這裡面每一個提供者的原始碼。藉由這樣做，你將會更了解每一個提供者添加什麼到框架，以及用什麼鍵值來綁定各種服務到 IoC 容器。

例如， `HashServiceProvider` 綁定 `hash` 做為鍵值到 IoC 容器，它將解析成 `Illuminate\Hashing\BcryptHasher` 實例。你可以在應用程式中覆寫這個 IoC 綁定，輕鬆地擴展並覆寫這個類別。例如：

	<?php namespace App\Providers;

	class SnappyHashProvider extends \Illuminate\Hashing\HashServiceProvider {

		public function boot()
		{
			$this->app->bindShared('hash', function()
			{
				return new \Snappy\Hashing\ScryptHasher;
			});

			parent::boot();
		}

	}

要注意的是這個類別擴展 `HashServiceProvider`，不是預設的 `ServiceProvider` 基底類別。當你擴展了服務提供者，在 `config/app.php` 設定檔把 `HashServiceProvider` 換成你擴展的提供者名稱。

這是被綁定在容器的所有核心類別的一般擴展方法。實際上，每個以這種方式綁定在容器的核心類別都可以被覆寫。再次強調，看過每個框架引入的服務提供者將會使你熟悉：每個類別被綁在容器的哪裡、它們是用什麼鍵值綁定。這是個好方法可以了解更多關於 Laravel 如何結合它們。
