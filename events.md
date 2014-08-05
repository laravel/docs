# Events

- [基本用法](#basic-usage)
- [萬用字元監聽者](#wildcard-listeners)
- [使用類別作為監聽者](#using-classes-as-listeners)
- [事件隊列](#queued-events)
- [事件訂閱者](#event-subscribers)

<a name="basic-usage"></a>
## 基本用法

Laravel 的 `Event` 類別提供一個簡單的觀察者實作，允許你在應用程式裡訂閱與監聽事件。

#### 訂閱事件

	Event::listen('auth.login', function($user)
	{
		$user->last_login = new DateTime;

		$user->save();
	});

#### 觸發事件

	$event = Event::fire('auth.login', array($user));

#### 訂閱有優先順序的事件

你也可以在訂閱事件的時候指定一個優先順序。 有較高優先權的監聽者會先被執行，當監聽者有一樣的優先權時將會依照訂閱的順序執行.

	Event::listen('auth.login', 'LoginHandler', 10);

	Event::listen('auth.login', 'OtherHandler', 5);

#### 停止繼續傳遞事件

你有時候會希望停止繼續傳遞事件到其他監聽者。 你可以藉由從監聽者回傳 `false` 來做到這件事：

	Event::listen('auth.login', function($event)
	{
		// Handle the event...

		return false;
	});

### 在哪裡註冊事件

現在你知道怎麼註冊事件了，但是你或許會想知道要在 _哪裡_ 註冊它們。 不要擔心，這是一個常見的問題。 不幸地，這是一個很難回答的問題，因為你幾乎可以在任何地方註冊事件！ 但是，這裡有一些提示。 一樣的，你可以在你的其中一個 `start` 檔案註冊事件，就像其他大部份的啟動程式碼，例如： `app/start/global.php`。

如果你的 `start` 檔案變得越來越擁擠，你可以建立一個分離的 `app/events.php` 檔案，並從 `start` 檔案引入它。 這是個簡單的解決方案，它保持你的事件註冊與剩餘的啟動程式碼乾淨地分離。 如果你喜歡基於類別的方法，你可以在 [服務提供者](/docs/ioc#service-providers) 註冊你的事件。 因為這些方法中沒有一個是絕對正確的方案，基於你的應用程式大小選擇一個讓你感到舒服的方法。

<a name="wildcard-listeners"></a>
## 萬用字元監聽者

#### 註冊萬用字元事件監聽者

當註冊事件監聽者，你可以使用星號(*) 指定萬用字元監聽者：

	Event::listen('foo.*', function($param)
	{
		// Handle the event...
	});

這個監聽者將會處理所有 `foo.` 開頭的事件。

你可以使用 `Event::firing` 方法準確的判定是什麼事件被觸發：

	Event::listen('foo.*', function($param)
	{
		if (Event::firing() == 'foo.bar')
		{
			//
		}
	});

<a name="using-classes-as-listeners"></a>
## 使用類別作為監聽者

在一些案例中，你或許會希望使用類別取代閉包來處理事件。 類別事件監聽者將會被 [Laravel IoC container](/docs/ioc) 處理，提供依賴注入的全部功能給你的監聽者。

#### 註冊類別監聽者

	Event::listen('auth.login', 'LoginHandler');

#### 定義事件監聽者類別

`LoginHandler` 類別預設將會呼叫 `handle` 方法：

	class LoginHandler {

		public function handle($data)
		{
			//
		}

	}

#### Specifying 哪個方法 To Subscribe

如果你不希望使用預設的 `handle` 方法, 你可以指定應該被訂閱的方法：

	Event::listen('auth.login', 'LoginHandler@onLogin');

<a name="queued-events"></a>
## 事件隊列

#### 註冊事件隊列

使用 `queue` 和 `flush` 方法， 你可以把事件加到隊列等待觸發，但是不立即觸發它：

	Event::queue('foo', array($user));

你可以執行 "flusher" 並觸發全部的事件隊列，使用 `flush` 方法：

	Event::flush('foo');

<a name="event-subscribers"></a>
## 事件訂閱者

#### 定義事件訂閱者

事件訂閱者是個可以從類別自身裡面訂閱多個事件的類別。 訂閱者應該定義 `subscribe` 方法，它將會被傳遞到事件配送器實體：

	class UserEventHandler {

		/**
		 * Handle user login events.
		 */
		public function onUserLogin($event)
		{
			//
		}

		/**
		 * Handle user logout events.
		 */
		public function onUserLogout($event)
		{
			//
		}

		/**
		 * Register the listeners for the subscriber.
		 *
		 * @param  Illuminate\Events\Dispatcher  $events
		 * @return array
		 */
		public function subscribe($events)
		{
			$events->listen('auth.login', 'UserEventHandler@onUserLogin');

			$events->listen('auth.logout', 'UserEventHandler@onUserLogout');
		}

	}

#### 註冊事件訂閱者

當訂閱者被定義時，它或許會使用 `Event` 類別註冊。

	$subscriber = new UserEventHandler;

	Event::subscribe($subscriber);

你也可以使用 [Laravel IoC container](/docs/ioc) 去處理你的訂閱者。 簡單地傳遞訂閱者的名字給 `subscribe` 方法就可以做到：

	Event::subscribe('UserEventHandler');

