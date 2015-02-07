# Command Bus

- [簡介](#introduction)
- [建立命令](#creating-commands)
- [派送命令](#dispatching-commands)
- [命令佇列](#queued-commands)
- [命令管線](#command-pipeline)

<a name="introduction"></a>
## 簡介

Command bus 提供一個簡便的方法來封裝任務，使你的程式更加容易閱讀與執行，為了幫助我們更加了解使用「命令」的目的，讓我們來模擬建立一個可以購買 podcast 的網站。

用戶購買 podcasts 的過程中需要做很多事。例如，我們需要從用戶的信用卡扣款，將紀錄新增到資料庫以表示購買，並發送購買確認的電子郵件，或許，我們還需要進行許多驗證來確認使用者是否可以購買。

我們可以將這些邏輯通通放在控制器的方法內，然而，這樣做會有一些缺點，首先，控制器可能還需要處理許多其他的 HTTP 動作，包含複雜的邏輯，這會讓控制器變得很肥大且難易閱讀，第二點，這些邏輯無法在這個控制器以外被重複使用，第三，這些命令無法被單元測試，為此我們還得額外產生一個 HTTP 請求，並向網站進行完整購買 podcast 的流程。

比起將邏輯放在控制器內，我們可以選擇使用一個「命令」物件來封裝它，像是 `PurchasePodcast` 命令。

<a name="creating-commands"></a>
## 建立命令

使用 `make:command` 這個 Artisan 指令可以產生一個新的命令類別 ：

	php artisan make:command PurchasePodcast

新產生的類別會被放在 `app/Commands` 目錄中，命令預設包含了兩個方法：建構子和 `handle` 。當然，`handle` 方法執行命令時，你可以使用建構子傳入相關的物件到這個命令中。例如：

	class PurchasePodcast extends Command implements SelfHandling {

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
	
`handle` 方法也可以使用型別暗示相依，並且藉由 [IoC 容器](/docs/5.0/container) 機制自動進行依賴注入。例如：

		/**
		 * Execute the command.
		 *
		 * @return void
		 */
		public function handle(BillingGateway $billing)
		{
			// Handle the logic to purchase the podcast...
		}

<a name="dispatching-commands"></a>
## 派送命令

所以，我們建立的命令該如何派送它呢？當然，我們可以直接呼叫 `handle` 方法，然而使用 Laravel 的 "command bus" 來派送命令將會有許多優點，待會我們會討論這個部分。

如果你有瀏覽過內建的基本控制器，將會發現 `DispatchesCommands` trait ，它將允許我們在控制器內呼叫 `dispatch` 方法，例如：

	public function purchasePodcast($podcastId)
	{
		$this->dispatch(
			new PurchasePodcast(Auth::user(), Podcast::findOrFail($podcastId))
		);
	}

Command bus 將會負責執行命令和呼叫 IoC 容器來將所需的相依注入到 `handle` 方法。

你也可以將 `Illuminate\Foundation\Bus\DispatchesCommands` trait 加入任何要使用的類別內。若你想要在任何類別的建構子內接收 command bus 的實體 ，你可以使用型別暗示 `Illuminate\Contracts\Bus\Dispatcher` 這個介面。
最後，你也可以使用 `Bus` facade 來快速派發命令：

		Bus::dispatch(
			new PurchasePodcast(Auth::user(), Podcast::findOrFail($podcastId))
		);

### 從請求映射要注入命令的屬性

映射 HTTP 請求到命令是很常見的，所以，與其要你針對每個請求苦命地進行手動對應，Laravel 則提供一些有用的方法來輕鬆達到，讓我們來看一下 `DispatchesCommands` trait 提供的 `dispatchFrom` 方法：

	$this->dispatchFrom('Command\Class\Name', $request);

這個方法將會檢查這個被傳入的命令類別的建構子，並取出來自於 HTTP 請求的變數(或其他任何的 `ArrayAccess` 物件) 並將其填入建構子，所以，若命令類在建構子接受 `firstName` 參數，command bus 將會試圖從 HTTP 請求取出 `firstName` 參數。

`dispatchFrom` 方法的第三個參數允許你傳入陣列，那些不在 HTTP 請求內的參數可用這個陣列來填入建構子：

	$this->dispatchFrom('Command\Class\Name', $request, [
		'firstName' => 'Taylor',
	]);

<a name="queued-commands"></a>
## 命令佇列

Command bus 不僅僅作為當下請求的同步作業，也可以作為 Laravel 佇列任務的主要方法，所以，我們要如何指示 command bus 在背景作業而不是同步處理呢？非常簡單，首先，在建立新的命令時加上 `--queued` 參數：

	php artisan make:command PurchasePodcast --queued

正如你所見的，這讓命令增加了一點功能，即 `Illuminate\Contracts\Queue\ShouldBeQueued` 介面和`SerializesModels` trait 。 他們指示 command bus 使用佇列來執行命令，以及優雅的序列化和反序列化任何在命令內被儲存的 Eloquent 模型。

若你想將已存在的命令轉換為佇列命令，只需手動修改讓命令類別實作 `Illuminate\Contracts\Queue\ShouldBeQueued` 介面，它不包含方法，而是僅僅給調度員作為"標記接口"。

然後，一如往常撰寫你的命令，當你將命令派發到 bus，它將會自動將命令丟到背景佇列執行，沒有比這個更容易的方法了。

想瞭解更多關於佇列命令的方法，請見[佇列文件](/docs/5.0/queues).

<a name="command-pipeline"></a>
## 命令管線

在命令被派發到處理器之前，你也可以將它藉由"命令管線"傳遞到其他類別去。命令管線操作上像是 HTTP 中介層，除了是專門來給命令用的，例如，一個命令管線能夠在資料庫交易期間包裝全部的命令操作，或者僅作為執行紀錄。

要將管線添加到 bus，只要從`App\Providers\BusServiceProvider::boot` 方法呼叫調度員的`pipeThrough` 方法：

	$dispatcher->pipeThrough(['UseDatabaseTransactions', 'LogCommand']);

一個命令管線被定義在 `handle` 方法，就像是個中介層：

	class UseDatabaseTransactions {

		public function handle($command, $next)
		{
			return DB::transaction(function() use ($command, $next)
			{
				return $next($command);
			}
		}

	}

命令管線是透過 IoC 容器來達成，所以請自行在建構子型別暗示所需的相依。

你甚至可以定義一個 `閉包` 來作為命令管線：

	$dispatcher->pipeThrough([function($command, $next)
	{
		return DB::transaction(function() use ($command, $next)
		{
			return $next($command);
		}
	}]);
