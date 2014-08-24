# 擴展框架

- [介紹](#introduction)
- [管理者和工廠](#managers-and-factories)
- [在哪裡擴展](#where-to-extend)
- [快取](#cache)
- [Session](#session)
- [認證](#authentication)
- [基於 IoC 的擴展](#ioc-based-extension)
- [擴展請求](#request-extension)

<a name="introduction"></a>
## 介紹

Laravel 提供許多可擴展的地方讓你客製化框架核心元件的行為，或甚至完全地取代它們。 例如，`HasherInterface` 契約定義了雜湊工具，你可以基於應用程式的需求實作它。 你也可以擴展 `Request` 物件，讓你加入自己的便利 "輔助" 方法。 甚至你可以加入全新的認證、快取和 session 驅動！

Laravel 元件一般以兩種方式來擴展： 在 IoC 容器裡綁定新的實作，或用 "工廠" 設計模式實作的 `Manager` 類別來註冊擴展。 在這個章節我們將會探索多種擴展框架的方法和查看必要的程式碼。

> **備註:** 記住， Laravel 元件通常用兩種方法的其中之一來擴展： IoC 綁定和 `Manager` 類別。 管理者類別作為 "工廠" 設計模式的實作，並負責實體化基於驅動的工具，例如：快取和 session。

<a name="managers-and-factories"></a>
## 管理者和工廠

Laravel 有幾個 `Manager` 類別用來管理基於驅動的元件建立。 這些類別包括快取、session、認證和隊列元件。 管理者類別負責基於應用程式的設定建立一個特定的驅動實作。 例如， `CacheManager` 類別可以建立 APC、 Memcached 、檔案和各種其他的快取驅動實作.

這些管理者都擁有 `extend` 方法，它可以簡單地用來注入新的驅動解析功能到管理者。 我們將會在下面隨著如何注入客製化驅動支援給它們的例子，涵蓋這些管理者的內容。

> **備註:** 花點時間來探索 Laravel 附帶的各種 `Manager` 類別，例如： `CacheManager` 和 `SessionManager`。 看過這些類別將會讓你更徹底了解 Laravel 表面下是如何運作。 所有的管理者類別繼承 `Illuminate\Support\Manager` 基底類別， 它提供一些有用、常見的功能給每一個管理者。

<a name="where-to-extend"></a>
## 在哪裡擴展

這份文件涵蓋如何擴展各種 Laravel 的元件，但是你可能想知道要在哪裡放置你的擴展程式碼。 就像其他大部分的啟動程式碼，你可以自由的在你的 `start` 檔案放置一些擴展，快取和認證擴展是這個方法的好例子。 其他擴展，像 `Session`，必須放置到服務提供者的 `register` 方法中，因為他們在請求生命週期的非常早期就被需要。

<a name="cache"></a>
## 快取

為了擴展 Laravel 快取工具，我們將會對 `CacheManager` 使用 `extend` 方法，它被用來綁定一個客製化驅動解析器到管理者，並且是全部的管理者類別通用的。 例如，註冊一個新的快取驅動命名為 "mongo"，我們將執行以下操作：

	Cache::extend('mongo', function($app)
	{
		// Return Illuminate\Cache\Repository instance...
	});

傳遞到 `extend` 方法的第一個參數是驅動的名稱。 這將會對應到你 `app/config/cache.php` 設定檔裡的 `driver` 選項。 第二個參數是個應該回傳 `Illuminate\Cache\Repository` 實體的閉包。 `$app` 實體將被傳遞到閉包 ，它是 `Illuminate\Foundation\Application` 和 IoC 容器的實體。

要建立我們的客製化快取驅動，首先需要實作 `Illuminate\Cache\StoreInterface` 契約。 所以，我們的 MongoDB 快取實作將會看起來像這樣：

	class MongoStore implements Illuminate\Cache\StoreInterface {

		public function get($key) {}
		public function put($key, $value, $minutes) {}
		public function increment($key, $value = 1) {}
		public function decrement($key, $value = 1) {}
		public function forever($key, $value) {}
		public function forget($key) {}
		public function flush() {}

	}

我們只需要使用 MongoDB 連接實作這些方法。 當我們的實作完成，我們可以完成我們的客製化驅動註冊：

	use Illuminate\Cache\Repository;

	Cache::extend('mongo', function($app)
	{
		return new Repository(new MongoStore);
	});

就像你可以在上面的例子看到的，當在建立客製化快取驅動的時候，你可以使用基本的 `Illuminate\Cache\Repository` 類別。 通常不需要建立你自己的儲存庫類別。

如果你在考慮要把你的客製化快取驅動程式碼放在哪裡，請考慮把它放上 Packagist！ 或者，你可以在你的應用程式的主要資料夾中建立一個 `Extensions` 命名空間。 例如，如果應用程式命名為 `Snappy`，你可以在 `app/Snappy/Extensions/MongoStore.php` 放置快取擴展。 然而，必須牢記在心 Laravel 沒有嚴格的應用程式架構，你可以依照喜好自由的組織你的應用程式。

> **備註:** 如果你曾經考慮要在哪放置一段程式碼，請總是考慮服務提供者。 就像我們曾經討論過的，用服務提供者來組織框架擴展是個組織你的程式碼的好方法.

<a name="session"></a>
## Session

以客製化 session 驅動來擴展 Laravel 跟擴展快取系統一樣簡單。 再一次的，我們將會使用 `extend` 方法來註冊我們的客製化程式碼：

	Session::extend('mongo', function($app)
	{
		// Return implementation of SessionHandlerInterface
	});

### 在哪裡擴展 Session

Session 需要與其他擴展如 Cache 和 Auth 不同地擴展。 因為 sessions 在請求生命週期的非常早期就被啟用， 註冊擴展在 `start` 檔案將會太晚。 作為替代，將會被需要[服務提供者](/docs/ioc#service-providers) 。 你應該放置你的 session 擴展程式碼在你的服務提供者的 `register` 方法，並且提供者應該被放置在 `providers` 設定陣列裡、 預設的 `Illuminate\Session\SessionServiceProvider` **下面**。

### 實作 Session 擴展

要注意我們的客製化快取驅動應該實作 `SessionHandlerInterface`。 這個介面在 PHP 5.4+ 核心被引入。 如果你使用 PHP 5.3，Laravel 將會為你定義這個介面，所以你可以向下相容。 這個介面只包含少數我們需要實作的簡單方法。 一個空的 MongoDB 實作將會看起來像這樣：

	class MongoHandler implements SessionHandlerInterface {

		public function open($savePath, $sessionName) {}
		public function close() {}
		public function read($sessionId) {}
		public function write($sessionId, $data) {}
		public function destroy($sessionId) {}
		public function gc($lifetime) {}

	}

因為這些方法不像快取 `StoreInterface` 一樣容易理解，讓我們快速地看過這些方法做些什麼：

- `open` 方法通常會被用在基於檔案的 session 儲存系統。 因為 Laravel 附帶一個 `file` session 驅動，你幾乎不需要在這個方法放任何東西。 你可以讓它留空。 PHP 要求我們去實作這個方法，事實上明顯的是差勁的介面設計 (我們將會晚點討論它)。
- `close` 方法，就像 `open` 方法，通常也可以忽略。 對大部份的驅動來說，並不需要它。
- `read` 方法應該回傳與給定 `$sessionId` 關聯的 session 資料的字串形態。 當在你的驅動取回或儲存 session 資料時不需要做任何序列化或其他編碼，因為 Laravel 將會為你進行序列化。
- `write` 方法應該寫入給定 `$data` 字串與 `$sessionId` 的關聯到一些永久存儲系統，例如 MongoDB、 Dynamo、等等。
- `destroy` 方法應該從永久存儲移除與 `$sessionId` 關聯的資料。
- `gc` 方法應該銷毀所有比給定 `$lifetime` UNIX 時間戳記還舊的 session 資料。 對於會自己到期的系統如 Memcached 和 Redis，這個方法可以留空。

當 `SessionHandlerInterface` 被實作完成，我們已經準備好用 Session 管理者註冊它：

	Session::extend('mongo', function($app)
	{
		return new MongoHandler;
	});

當 session 驅動已經被註冊，我們可以在我們的 `app/config/session.php` 設定檔使用 `mongo` 驅動 。

> **備註:** 記住，如果你寫了個客製化 session 處理器，請在 Packagist 分享它！

<a name="authentication"></a>
## 認證

認證可以用跟快取和 session 工具相同的方法擴展。 再一次的，我們將會使用我們已經熟悉的 `extend` 方法：

	Auth::extend('riak', function($app)
	{
		// Return implementation of Illuminate\Auth\UserProviderInterface
	});

`UserProviderInterface` 實作只負責從永久存儲系統抓取 `UserInterface` 實作，例如： MySQL、 Riak，等等。 這兩個介面讓 Laravel 認證機制無論使用者資料如何儲存或用什麼種類的類別來代表它都能繼續運作。

讓我們來看一下 `UserProviderInterface`：

	interface UserProviderInterface {

		public function retrieveById($identifier);
		public function retrieveByToken($identifier, $token);
		public function updateRememberToken(UserInterface $user, $token);
		public function retrieveByCredentials(array $credentials);
		public function validateCredentials(UserInterface $user, array $credentials);

	}

`retrieveById` 函式通常接收一個代表使用者的數字鍵，例如： MySQL 資料庫的自動遞增 ID。 符合 ID 的 `UserInterface` 實作應該被取回並被方法回傳。

`retrieveByToken` 函式用使用者唯一的 `$identifier` 和儲存在 `remember_token` 欄位的 "記住我" `$token` 取得使用者。 跟前面的方法一樣，應該回傳 `UserInterface` 實作。

`updateRememberToken` 方法用新的 `$token` 更新 `$user` 的 `remember_token` 欄位。 新 token 可以是在 "記住我" 成功地登入時發一個新的 token，或當使用者登出為 null.

`retrieveByCredentials` 方法接收當嘗試登入應用程式時，傳遞到 `Auth::attempt` 方法的憑證陣列。 這個方法應該接著 "查詢" 背後的永久存儲使用者是否符合這些憑證。 這個方法通常會對 `$credentials['username']` 用 "where" 條件查詢。 **這個方法不應該嘗試做任何密碼驗證或認證。**

`validateCredentials` 方法應該比較給定 `$user` 與 `$credentials` 來驗證使用者。 舉例來說，這個方法可以比較 `$user->getAuthPassword()` 字串跟 `Hash::make` 後的 `$credentials['password']`。

現在我們已經看過 `UserProviderInterface` 的每個方法，接著我們來看一下 `UserInterface`。 記住，提供者應該從 `retrieveById` 和 `retrieveByCredentials` 方法回傳這個介面的實作：

	interface UserInterface {

		public function getAuthIdentifier();
		public function getAuthPassword();

	}

這個介面很簡單。 `getAuthIdentifier` 方法應該回傳使用者的 "主鍵"。 在 MySQL 後台，同樣，這將會是個自動遞增的主鍵。 `getAuthPassword` 應該回傳使用者雜湊過的密碼。 這個介面讓認證系統可以與任何使用者類別一起運作，無論你使用什麼 ORM 或儲存抽象層。 預設， Laravel 包含一個實作這個介面的 `User` 類別在 `app/models` 資料夾裡，所以你可以參考這個類別當作實作例子。

最後，當我們已經實作了 `UserProviderInterface`，我們準備好用 `Auth` facade 來註冊我們的擴展：

	Auth::extend('riak', function($app)
	{
		return new RiakUserProvider($app['riak.connection']);
	});

在你用 `extend` 方法註冊驅動之後，在你的 `app/config/auth.php` 設定檔切換到新驅動。
<a name="ioc-based-extension"></a>
## 基於 IoC 的擴展

幾乎每個 Laravel 框架引入的服務提供者會綁定物件到 IoC 容器中。 你可以在 `app/config/app.php` 設定檔中找到應用程式的服務提供者清單。 當你有時間的時候，你應該瀏覽過這裡面每一個提供者的原始碼。 借由這樣做，你將會對應加更多的了解每一個提供者加了什麼到框架，以及什麼鍵被用來綁定各種服務到 IoC 容器。

舉個例子， `HashServiceProvider` 綁定一個 `hash` 鍵到 IoC 容器，它將解析成 `Illuminate\Hashing\BcryptHasher` 實體。 你可以輕鬆地在你的應用程式借由覆寫這個 IoC 綁定擴展並覆寫這個類別。 例如：

	class SnappyHashProvider extends Illuminate\Hashing\HashServiceProvider {

		public function boot()
		{
			App::bindShared('hash', function()
			{
				return new Snappy\Hashing\ScryptHasher;
			});

			parent::boot();
		}

	}

要注意的是這個類別擴展 `HashServiceProvider`，不是預設的 `ServiceProvider` 基底類別。 當你擴展了服務提供者，在你的 `app/config/app.php` 設定檔把 `HashServiceProvider` 換成你擴展的提供者名稱。

這是擴展任何被綁定在容器的核心類別的普遍方法。 實際上，每個被以這種方式綁定在容器的核心類別都可以被覆寫。 再次強調，看過被框架引入的服務提供者將會使你熟悉每個類別被綁在容器的哪裡，還有它們是用什麼鍵綁。 這是個好方法了解更多關於 Laravel 如何結合它們。

<a name="request-extension"></a>
## 擴展請求

因為它是框架非常基礎的部件並且在請求週期的非常早期就被實體化，擴展 `Request` 類別跟前面的例子有一點不同。

首先，像一般一樣擴展類別：

	<?php namespace QuickBill\Extensions;

	class Request extends \Illuminate\Http\Request {

		// Custom, helpful methods here...

	}

當你擴展了類別，打開 `bootstrap/start.php` 檔案。 這個檔案是當應用程式受到請求後非常早被引入的檔案之一。 需要注意的是第一個被執行的動作是建立 Laravel `$app` 實體：

	$app = new \Illuminate\Foundation\Application;

當一個新的應用程式實體被建立，它將會建立一個新的 `Illuminate\Http\Request` 實體並用 `request` 鍵把它綁定到 IoC 容器。 所以，我們需要一個方法去指定一個 應該被用作 "預設" 請求類型的客製化類別，對吧？ 並且值得慶幸的是，應用程式實體的 `requestClass` 方法就做了這件事！ 所以，我們可以在 `bootstrap/start.php` 檔案的最上面加這行：

	use Illuminate\Foundation\Application;

	Application::requestClass('QuickBill\Extensions\Request');

每當你指定了客製化請求類別， Laravel 將會在任何建立 `Request` 實體的時候使用這個類別，便利地讓你總是有一個可用的你的客製化請求類別實體，甚至在單元測試也有！
