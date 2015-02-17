# 事件（ Events ）

- [基本用法](#basic-usage)
- [事件處理隊列](#queued-event-handlers)
- [事件訂閱者](#event-subscribers)

<a name="basic-usage"></a>
## 基本用法

Laravel 的 event 功能提供一個簡單的觀察者實作，允許你在應用程式裡訂閱與監聽事件。事件類別通常被儲存在 `app/Events` 目錄下，而它們的處理程式則被儲存在 `app/Handlers/Events` 目錄下。

你可以使用 Artisan 命令列工具產生一個新的事件類別：

	php artisan make:event PodcastWasPurchased

#### 訂閱事件

Laravel 裡的 `EventServiceProvider` 提供了一個方便的地方註冊所有的事件處理程式。`listen` 屬性包含一個所有的事件 (鍵) 和相對應的處理程式 (值) 的 陣列。當然，你可以依應用程式的需求添加任何數量的事件到這個陣列。舉個例子，讓我們來加上 `PodcastWasPurchased` 事件：

	/**
	 * 應用程式的事件處理程式對照。
	 *
	 * @var array
	 */
	protected $listen = [
		'App\Events\PodcastWasPurchased' => [
			'App\Handlers\Events\EmailPurchaseConfirmation@handle',
		],
	];

使用 Artisan 命令列指令 `handler:event`，來產生一個事件的處理程式：

	php artisan handler:event EmailPurchaseConfirmation --event=PodcastWasPurchased

當然，在每次你需要一個處理程式或是事件時，手動地執行 `make:event` 和 `handler:event` 指令很麻煩。作為替代，簡單地添加處理程式跟事件到你的 `EventServiceProvider` 並使用 `event:generate` 指令。這個指令將會產生任何在你的 `EventServiceProvider` 列出的事件跟處理程式：

	php artisan event:generate

#### 觸發事件

現在我們準備好使用 `Event` facade 觸發我們的事件：

	$response = Event::fire(new PodcastWasPurchased($podcast));

`fire` 方法回傳一個回應的陣列，讓你可以用來控制你的應用程式接下來要有什麼反應。

你也可以使用 `event` 輔助方法來觸發事件：

	event(new PodcastWasPurchased($podcast));

#### 監聽器閉包

你甚至可以不需對事件建立對應的處理類別。舉個例子，在你的 `EventServiceProvider` 的 `boot` 方法裡，你可以做下面這件事：

	Event::listen('App\Events\PodcastWasPurchased', function($event)
	{
		// 處理事件...
	});

#### 停止繼續傳遞事件

有時候你會希望停止繼續傳遞事件到其他監聽器。你可以藉由從處理程式回傳 `false` 來做到這件事：

	Event::listen('App\Events\PodcastWasPurchased', function($event)
	{
		// 處理事件...

		return false;
	});

<a name="queued-event-handlers"></a>
## 事件處理隊列

需要把事件處理程式放到 [隊列](/docs/5.0/queues) 嗎？這不能變得再更簡單了。當你產生處理程式，簡單地使用 `--queued` 旗標：

	php artisan handler:event SendPurchaseConfirmation --event=PodcastWasPurchased --queued

這將會產生一個實作了 `Illuminate\Contracts\Queue\ShouldBeQueued` 介面的處理程式類別。這樣就可以了！現在當這個處理程式因為事件發生被呼叫，它將會被事件配送器自動地排進隊列。

當處理程式被隊列執行，如果沒有例外被丟出，在執行後該隊列中的任務將會自動被刪除。你也可以手動取用隊列中的任務的 `delete` 和 `release` 方法。隊列處理程式預設會引入的 `Illuminate\Queue\InteractsWithQueue` trait，讓你可以取用這些方法：

	public function handle(PodcastWasPurchased $event)
	{
		if (true)
		{
			$this->release(30);
		}
	}

如果你想要把一個已存在的處理程式轉換成一個隊列的處理程式，簡單地手動添加 `ShouldBeQueued` 介面到類別。

<a name="event-subscribers"></a>
## 事件訂閱者

#### 定義事件訂閱者

事件訂閱者是個可以從類別自身裡面訂閱多個事件的類別。訂閱者應該定義 `subscribe` 方法，事件配送器實體將會被傳遞到這個方法：

	class UserEventHandler {

		/**
		 * 處理使用者登入事件。
		 */
		public function onUserLogin($event)
		{
			//
		}

		/**
		 * 處理使用者登出事件。
		 */
		public function onUserLogout($event)
		{
			//
		}

		/**
		 * 註冊監聽器給訂閱者。
		 *
		 * @param  Illuminate\Events\Dispatcher  $events
		 * @return array
		 */
		public function subscribe($events)
		{
			$events->listen('App\Events\UserLoggedIn', 'UserEventHandler@onUserLogin');

			$events->listen('App\Events\UserLoggedOut', 'UserEventHandler@onUserLogout');
		}

	}

#### 註冊事件訂閱者

當定義了訂閱者後，可以使用 `Event` 類別註冊。

	$subscriber = new UserEventHandler;

	Event::subscribe($subscriber);

你也可以使用 [Laravel IoC 容器](/docs/5.0/container) 自動解析訂閱者。簡單地傳遞訂閱者的名字給 `subscribe` 方法就可以做到：

	Event::subscribe('UserEventHandler');

