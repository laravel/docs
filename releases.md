# 發行說明

- [Laravel 5.0](#laravel-5.0)
- [Laravel 4.2](#laravel-4.2)
- [Laravel 4.1](#laravel-4.1)

<a name="laravel-5.0"></a>
## Laravel 5.0

Laravel 5.0 在預設的專案上引進了新的應用程式架構。新的架構提供了更好的功能建立強健的 Laravel 應用程式，以及在應用程式中全面採用新的自動載入標準（ PSR-4 ）。首先，來檢視一些主要更動：

### 新的目錄結構

舊的 `app/models` 目錄已經完全被移除。相對的，你所有的程式碼都放在 `app` 目錄下，以及預設上使用 `App` 命名空間。這個預設的命名空間可以快速的被更改，使用新的 `app:name` Artisan 命令。

控制器（ controller ），中介層（ middleware ），以及請求（ requests，Laravel 5.0 中新型態的類別），現在分門別類的放在 `app/Http` 目錄下，因為他們都與應用程式的 HTTP 傳輸層相關。除了一個路由設定的檔案外，所有的中介層現在都分開成為獨自的類別檔。

新的 `app/Providers` 目錄取代了舊版 Laravel 4.x `app/start` 裡的檔案。這些服務提供者有很多啟動應用程式相關的方法，像是錯誤處理，日誌紀錄，路由載入，以及更多。當然，你可以自由的建立新的服務提供者到應用程式。

應用程式的語言檔案和視圖都移到 `resources` 目錄下。

### Contracts

所有 Laravel 主要元件實作所用的介面都放在 `illuminate/contracts` 專案下。這個專案沒有其他的外部相依。這些方便、集成的介面，可以讓你用來讓依賴注入變得低耦合，將可以簡單作為 Laravel Facades 的替代選項。

更多關於 contracts 的資訊，參考[完整文件](/docs/5.0/contracts)。

### 路由快取

如果你的應用程式全部都是使用控制器路由，你可以使用新的 `route:cache` Artisan 命令大幅度地加快路由註冊。這對於有 100 個以上路由規則的應用程式很有用，可以**大幅度地**加快應用程式這部分的處理速度。

### 路由中介層（ Middleware ）

除了像 Laravel 4 風格的路由「過濾器（ filters ）」，Laravel 5 現在有 HTTP 中介層，而原本的認證和 CSRF 「過濾器」已經改寫成中介層。中介層提供了單一、一致的介面取代了各種過濾器，讓你在請求進到應用程式前，可以簡單地檢查甚至拒絕請求。

更多關於中介層的資訊，參考[完整文件](/docs/5.0/middleware)。

### 控制器方法依賴注入

除了之前有的控制器依賴注入，你現在可以在控制器方法使用型別提示（ type-hint ）進行依賴注入。[服務容器](/docs/5.0/container)會自動注入依賴，即使路由包含了其他參數也不成問題：

	public function createPost(Request $request, PostRepository $posts)
	{
		//
	}

### 認證基本架構

使用者註冊，認證，以及重設密碼的控制器現在已經預設含括了，包含相對應的視圖，放在 `resources/views/auth`。除此之外， "users" 資料表遷移也已經預設存在框架中了。這些簡單的資源，可以讓你快速開發應用程式的點子，而不用陷在撰寫認證模板的泥淖上。認證相關的視圖可以經由 `auth/login` 以及 `auth/register` 路由訪問。`App\Services\Auth\Registrar` 服務會負責處理使用者認證和新增的相關邏輯。

### 事件物件

你現在可以將事件定義成物件，而不是僅使用字串。例如，瞧瞧以下的事件：

	class PodcastWasPurchased {

		public $podcast;

		public function __construct(Podcast $podcast)
		{
			$this->podcast = $podcast;
		}

	}

這個事件可以像一般使用那樣被派發：

	Event::fire(new PodcastWasPurchased($podcast));

當然，你的事件處理會收到事件的物件而不是資料的列表：

	class ReportPodcastPurchase {

		public function handle(PodcastWasPurchased $event)
		{
			//
		}

	}

更多關於使用事件的資訊，參考[完整文件](/docs/5.0/events)。

### 命令（ Commands ）、隊列（ Queueing ）

除了 Laravel 4 形式的隊列任務，Laravel 5 以簡單的命令物件作為隊列任務。這些命令放在 `app/Commands` 目錄下。下面是個簡單的命令：

	class PurchasePodcast extends Command implements SelfHandling, ShouldBeQueued {

		use SerializesModels;

		protected $user, $podcast;

		/**
		 * Create a new command instance.
		 *
		 * @return void
		 */
		public function __construct(User $user, Podcast $podcast)
		{
			$this->user = $user;
			$this->podcast = $podcast;
		}

		/**
		 * Execute the command.
		 *
		 * @return void
		 */
		public function handle()
		{
			// Handle the logic to purchase the podcast...

			event(new PodcastWasPurchased($this->user, $this->podcast));
		}

	}

Laravel 的基底控制器使用了新的 `DispatchesCommands` trait，讓你可以簡單的派發命令執行。

	$this->dispatch(new PurchasePodcastCommand($user, $podcast));

當然，你也可以將命令視為同步執行（而不會被放到隊列裡）的任務。事實上，使用命令是個好方式，讓你可以封裝應用程式需要執行的複雜任務。更多相關的資訊，參考 [command bus](/docs/5.0/bus) 文件。

### 資料庫隊列

`database` 隊列驅動現在已經包含在 Laravel 中了，提供了簡單的本地端隊列驅動，讓你除了資料庫相關軟體外不需安裝其他套件。

### Laravel 排程（ Scheduler ）

過去，開發者可以產生 Cron 設定，用以排程所有他們想要執行的命令列指令。然而，這是件很頭痛的事情，你的命令列排程不再屬於版本控制的一部分，而你必須 SSH 到伺服器裏加入 Cron 設定。讓生活變得簡單點。Laravel 命令列排程，讓你可以流暢而且具有表達性的定義在 Laravel 裡面，定義你的命令排程，而且伺服器只需要單一個 Cron 設定。

它會看起來如下：

	$schedule->command('artisan:command')->dailyAt('15:00');

當然，快參考[完整文件](/docs/5.0/artisan#scheduling-artisan-commands)學習所有排程相關知識。

### Tinker、Psysh

`php artisan tinker` 命令現在使用 Justin Hileman 的 [Psysh](https://github.com/bobthecow/psysh)，一個 PHP 更強大的 REPL。如果你喜歡 Laravel 4 的 Boris，你也會喜歡上 Psysh。更好的是，它可以跑在 Windows！要開始使用，只要輸入：

	php artisan tinker

### DotEnv

比起一堆令人困惑的、巢狀的環境設定檔目錄，Laravel 5 現在使用了 Vance Lucas 的 [DotEnv](https://github.com/vlucas/phpdotenv)。這個套件提供了超級簡單的方式管理設定檔，並且讓 Laravel 5 環境偵測變得輕鬆。更多的細節，參考完整的[設定檔文件](/docs/5.0/configuration#environment-configuration)。

### Laravel Elixir

Jeffrey Way 的 Laravel Elixir 提供了一個流暢、口語的介面，可以編譯以及合併 assets。如果你曾經在學習 Grunt 或 Gulp 被嚇到，不必再害怕了。Elixir 讓使用 Gulp 編譯 Less、Sass 及 CoffeeScript 變得簡單。它甚至可以幫你執行測試！

更多關於 Elixir 的資訊，參考[完整文件](/docs/5.0/elixir)。

### Laravel Socialite

Laravel Socialite 是個選用的，Laravel 5.0 以上相容的套件，提供了無痛的 OAuth 認證。目前 Socialite 支援 Facebook、Twitter、Google 以及 GitHub。它寫起來可能像這樣：

	public function redirectForAuth()
	{
		return Socialize::with('twitter')->redirect();
	}

	public function getUserFromProvider()
	{
		$user = Socialize::with('twitter')->user();
	}

不用再花上數小時撰寫 OAuth 的認證流程。數分鐘就可開始！查看[完整文件](/docs/5.0/authentication#social-authentication) 裡有所有的細節。

### Flysystem 整合

Laravel 現在包含了強大的 [Flysystem](https://github.com/thephpleague/flysystem)（一個檔案系統的抽象函式庫），提供了無痛的整合，把本地端檔案系統、Amazon S3 和 Rackspace 雲端儲存整合在一起，
有統一且優雅的 API！現在要將檔案存到 Amazon S3 相當簡單：

	Storage::put('file.txt', 'contents');

更多關於 Laravel 檔案系統整合，參考[完整文件](/docs/5.0/filesystem)。

### Form Requests

Laravel 5.0 使用了 **form requests**，是繼承了 `Illuminate\Foundation\Http\FormRequest` 的類別。這些 request 物件可以和控制器方法依賴注入結合，提供一個不需樣板的方法，可以驗證使用者輸入。讓我們深入點，看一個 `FormRequest` 的範例：

	<?php namespace App\Http\Requests;

	class RegisterRequest extends FormRequest {

		public function rules()
		{
			return [
				'email' => 'required|email|unique:users',
				'password' => 'required|confirmed|min:8',
			];
		}

		public function authorize()
		{
			return true;
		}

	}

定義好類別後，我們可以在控制器動作裡使用型別提示：

	public function register(RegisterRequest $request)
	{
		var_dump($request->input());
	}

當 Laravel 的服務容器辨別出要注入的類別是個 `FormRequest` 實例，請求會被**自動驗證**。意味著，當你的控制器動作被呼叫了，你可以安全的假設 HTTP 的請求輸入己經被驗證過，根據你在 form request 類別裡自定的規則。甚至，若這個請求驗證不通過，一個 HTTP 重導（可以自定），會自動發出，錯誤訊息可以被閃存到 session 或是轉換成 JSON 返回。**表單驗證再簡單不過如此。**更多關於 `FormRequest` 驗證，參考[文件](/docs/5.0/validation#form-request-validation)。

### 簡易控制器請求驗證

Laravel 5 基底控制器包含一個 `ValidatesRequests` trait。這個 trait 包含了一個簡單的 `validate` 方法可以驗證請求。如果對應用程式來說 `FormRequests` 太複雜了，參考這個：

	public function createPost(Request $request)
	{
		$this->validate($request, [
			'title' => 'required|max:255',
			'body' => 'required',
		]);
	}

如果驗證失敗，會拋出例外以及回傳適當的 HTTP 回應到瀏覽器。驗證錯誤資訊會被閃存到 session！而如果請求是 AJAX 請求，Laravel 會自動回傳 JSON 格式的驗證錯誤資訊。

更多關於這個新方法的資訊，參考[這個文件](/docs/5.0/validation#controller-validation)。

### 新的 Generators

因應新的應用程式預設架構，框架新增了 Artisan generator 命令。使用 `php artisan list` 瞧瞧更多細節。

### 設定檔快取

你現在可以在單一檔案裡快取所有設定檔了，使用 `config:cache` 命令。

### Symfony VarDumper

出名的 `dd` 輔助函示，其可以在除錯時印出變數資訊，已經升級成使用令人驚豔的 Symfony VarDumper。它提供了顏色標記的輸出，甚至陣列可以自動縮合。在專案中試試下列程式碼：

	dd([1, 2, 3]);

<a name="laravel-4.2"></a>
## Laravel 4.2

此發行版本的完整更動列表可以從一個 4.2 的完整安裝下，執行 `php artisan changes` 命令，或者 [Github 上的更動紀錄](https://github.com/laravel/framework/blob/4.2/src/Illuminate/Foundation/changes.json)。此紀錄僅含括主要的強化更新和此發行的更動部分。

> **附註:** 在 4.2 發佈週期間，許多小的臭蟲修正與功能強化被整併至各個 4.1 的子發行版本中。所以最好確認 Laravel 4.1 版本的更新列表。

### PHP 5.4 需求

Laravel 4.2 需要 PHP 5.4 以上的版本。此 PHP 更新版本讓我們可以使用 PHP 的新功能：traits 來為像是 [Laravel 收銀台](/docs/billing) 來提供更具表達力的介面。PHP 5.4 也比 PHP 5.3 帶來顯著的速度及效能提升。

### Laravel Forge

Larvel Forge，一個網頁應用程式，提供一個簡單的介面去建立管理你雲端上的 PHP 伺服器，像是 Linode、DigitalOcean、Rackspace 和 Amazon EC2。支援自動化 nginx 設定、SSH 金鑰管理、Cron job 自動化、透過 NewRelic & Papertrail 伺服器監控、「推送部署」、Laravel queue worker 設定等等。Forge 提供最簡單且更實惠的方式來部署所有你的 Laravel 應用程式。

預設 Laravel 4.2 的安裝裡，`app/config/database.php` 設定檔預設已為 Forge 設定完成，讓在平台上的全新應用程式更方便部署。

關於 Laravel Forge 的更多資訊可以在[官方 Forge 網站](https://forge.laravel.com)上找到。

### Laravel Homestead

Laravel Homestead 是一個為部署健全的 Laravel 和 PHP 應用程式的官方 Vagrant 環境。絕大多數的封裝包的相依與軟體在發佈前已經部署處理完成，讓封裝包可以極快的被啟用。Homestead 包含 Nginx 1.6、PHP 5.5.12、MySQL、Postres、Redis、Memcached、Beanstalk、Node、Gulp、Grunt 和 Bower。Homestead 包含一個簡單的 `Homestead.yaml` 設定檔，讓你在單一個封裝包中管理多個 Laravel 應用程式。

預設的 Laravel 4.2 安裝中包含的 `app/config/local/database.php` 設定檔使用 Homestead 的資料庫作為預設。讓 Laravel 初始化安裝與設定更為方便。

官方文件已經更新並包含在 [Homestead 文件](/docs/homestead) 中。

### Laravel 收銀台

Laravel 收銀台是一個簡單、具表達性的資源庫，用來管理 Stripe 的訂閱帳務。雖然在安裝中此元件依然是選用，我們依然將收銀台文件包含在主要 Laravel 文件中。此收銀台發布版本帶來了數個錯誤修正、多貨幣支援還有支援最新的 Stripe API。

### Queue Workers 常駐程式

Artisan `queue:work` 命令現在支援 `--daemon` 參數讓 worker 可以以「常駐程式」啟用。代表 worker 可以持續的處理隊列工作不需要重啓框架。這讓一個複雜的應用程式部署過程中，使得 CPU 的使用有顯著的降低。

更多關於 Queue Workers 常駐程式資訊請詳閱 [queue 文件](/docs/queues#daemon-queue-worker)。

### Mail API Drivers

Laravel 4.2 為 `Mail` 函式採用了新的 Mailgun 和 Mandrill API 驅動。對許多應用程式而言，他提供了比 SMTP 更快也更可靠的方法來遞送郵件。新的驅動使用了 Guzzle 4 HTTP 資源庫。

### 軟刪除 Traits

對於軟刪除和全作用域更簡潔的方案
PHP 5.4 的 `traits` 提供了一個更加簡潔的軟刪除架構和全局作用域，這些新架構為框架提供了更有擴展性的功能，並且讓框架更加簡潔。

更多關於軟刪除的文檔請見: [Eloquent documentation](/docs/eloquent#soft-deleting).

### 更為方便的 認證(auth) & Remindable Traits

得益於 PHP 5.4 traits，我們有了一個更簡潔的用戶認證和密碼提醒接口，這也讓 `User` 模型文件更加精簡。

### "簡易分頁"

一個新的 `simplePaginate` 方法已被加入到查詢以及 Eloquent 查詢器中。讓你在分頁視圖中，使用簡單的「上一頁」和「下一頁」連結查詢更為高效。

### 遷移確認

在正式環境中，破壞性的遷移動作將會被再次確認。如果希望取消提示字元確認請使用 `--force` 參數。

<a name="laravel-4.1"></a>
## Laravel 4.1

### 完整更動列表

此發行版本的完整更動列表，可以在版本 4.1 的安裝中命令列執行 `php artisan changes` 取得，或者瀏覽 [Github 更動檔](https://github.com/laravel/framework/blob/4.1/src/Illuminate/Foundation/changes.json) 中了解。其中只記錄了該版本比較主要的強化功能和更動。

### 新的 SSH 元件

一個全新的 `SSH` 元件在此發行版本中登場。此功能讓你可以輕易的 SSH 至遠端伺服器並執行命令。更多資訊，可以參閱 [SSH 元件文件](/docs/ssh)。

新的 `php artisan tail` 指令就是使用這個新的 SSH 元件。更多的資訊，請參閱 `tail` [指令集文件](http://laravel.com/docs/ssh#tailing-remote-logs)。

### Boris In Tinker

如果您的系統支援 [Boris REPL](https://github.com/d11wtq/boris)，`php artisan thinker` 指令將會使用到它。系統中也必須先行安裝好 `readline` 和 `pcntl` 兩個 PHP 套件。如果你沒這些套件，從 4.0 之後將會使用到它。

### Eloquent 強化

Eloquent 新增了新的 `hasManyThrough` 關係鏈。想要了解更多，請參見 [Eloquent 文件](/docs/eloquent#has-many-through)。

一個新的 `whereHas` 方法也同時登場，他將允許[檢索基於關係模型的約束](/docs/eloquent#querying-relations)。

### 資料庫讀寫分離

Query Builder 和 Eloquent 目前透過資料庫層，已經可以自動做到讀寫分離。更多的資訊，請參考 [文件](/docs/database#read-write-connections)。

### 隊列排序

隊列排序已經被支援，只要在 `queue:listen` 命令後將隊列以逗號分隔送出。

### 失敗隊列作業處理

現在隊列將會自動處理失敗的作業，只要在 `queue:listen` 後加上 `--tries` 即可。更多的失敗作業處理可以參見 [隊列文件](/docs/queues#failed-jobs)。

### 緩存標籤

緩存「區塊」已經被「標籤」取代。緩存標籤允許你將多個「標籤」指向同一個緩存物件，而且可以清空所有被指定某個標籤的所有物件。更多使用緩存標籤資訊請見 [緩存文件](/docs/cache#cache-tags)。

### 更具彈性的密碼提醒

密碼提醒引擎已經可以提供更強大的開發彈性，如：認證密碼、顯示狀態訊息等等。使用強化的密碼提醒引擎，更多的資訊 [請參閱文件](/docs/security#password-reminders-and-reset)。

### 強化路由引擎

Laravel 4.1 擁有一個完全重新編寫的路由層。API 一樣不變。然而與 4.0 相比，速度快上 100%。整個引擎大幅的簡化，且對於路由表達式的編譯大大減少對 Symfony Routing 的依賴。

### 強化 Session 引擎

此發行版本中，我們亦發佈了全新的 Session 引擎。如同路由增進的部分，新的 Session 曾更加簡化且更快速。我們不再使用 Symfony 的 Session 處理工具，並且使用更簡單、更容易維護的客製化解法。


### Doctrine DBAL

如果你有在你的遷移中使用到 `renameColumn`，之後你必須在 `composer.json` 裡加 `doctrine/dbal` 進相依套件中。此套件不再預設包含在 Laravel 之中。
