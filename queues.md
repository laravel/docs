# 隊列

- [設定](#configuration)
- [基本用法](#basic-usage)
- [隊列閉包](#queueing-closures)
- [啟動隊列監聽](#running-the-queue-listener)
- [常駐隊列工作](#daemon-queue-worker)
- [推送隊列](#push-queues)
- [失敗的工作](#failed-jobs)

<a name="configuration"></a>
## 設定

Laravel 隊列元件提供一個統一的 API 整合了許多不同的隊列服務，隊列允許你延後執行一個耗時的任務，例如延後至指定的時間才寄送郵件，進而大幅的加快對應用程式請求回應的速度。

隊列的設定檔在 `config/queue.php`，在這個檔案你將可以找到框架中每種不同的隊列服務的連線設定，其中包含了 [Beanstalkd](http://kr.github.com/beanstalkd)、[IronMQ](http://iron.io)、[Amazon SQS](http://aws.amazon.com/sqs)、[Redis](http://redis.io)、`null`，以及同步 (本地端使用) 驅動設定。驅動 `null` 只是簡單的捨棄隊列工作，因此那些工作永遠不會執行。

### 隊列資料表

為了能夠使用 `database` 驅動，你需要建立一個資料表來儲存工作。要使用一個遷移建立這個資料表，可以執行 `queue:table`  Artisan 命令：

	php artisan queue:table

### 其他隊列依賴

下面的依賴是使用對應的隊列驅動所需的套件：

- Amazon SQS: `aws/aws-sdk-php`
- Beanstalkd: `pda/pheanstalk ~3.0`
- IronMQ: `iron-io/iron_mq`
- Redis: `predis/predis ~1.0`

<a name="basic-usage"></a>
## 基本用法

#### 推送一個工作至隊列

所有你的應用程式中能夠放進隊列的工作都存放在 `App\Commands` 目錄下，你可以藉由下列 Artisan 命令產生一個可使用隊列的指令：

	php artisan make:command SendEmail --queued

要推送一個新的工作至隊列，請使用 `Queue::push` 方法：

	Queue::push(new SendEmail($message));

> **注意:** 在這個範例當中，我們直接使用 `Queue` Facade，然而，常見的作法是藉由 [Command Bus](/docs/5.0/bus) 是分派隊列指令。我們將會在整篇文章中繼續使用 `Queue` Facade，不過，也要熟悉使用 command bus，因為它能夠同時分派你的網站應用程式中隊列與同步的指令。

預設上，由 `make:command` Artisan 命令會產生一個 "self-handling" 的指令，意味著指令裡會包含一個 `handle` 方法。這個方法將會在隊列執行時被呼叫。你可以在 `handle` 方法使用型別提示傳入任何你需要的依賴，而 [服務容器](/docs/5.0/container)會自動注入他們：

	public function handle(UserRepository $users)
	{
		//
	}

如果你希望你的指令有獨立的處理類別，你可以在使用 `make:command` 命令時加上 `--handler` 旗標。

	php artisan make:command SendEmail --queued --handler

這個被產生出來的處理類別將會放在 `App\Handlers\Commands` 目錄下面，並且服務容器會自動解析。

#### 指定隊列使用特定連線

你也可指定隊列工作送至指定的連線：

	Queue::pushOn('emails', new SendEmail($message));

#### 傳送相同的資料去多個隊列工作

如果你需要傳送一樣的資料去幾個不同的隊列工作，你可以使用 `Queue::bulk` 方法：

	Queue::bulk(array(new SendEmail($message), new AnotherCommand));

#### 延遲執行一個工作

有時候你可能想要延遲執行一個隊列工作，舉例來說你希望一個隊列工作在客戶註冊 15 分鐘後才寄送 e-mail，你可以使用 `Queue::later` 方法來完成這件事情：

	$date = Carbon::now()->addMinutes(15);

	Queue::later($date, new SendEmail($message));

在這個範例中，我們使用 [Carbon](https://github.com/briannesbitt/Carbon) 日期函式庫來指定我們希望隊列工作希望延遲的時間，另外你也可傳送一個整數來設定你希望延遲的秒數。

> **注意:** 在 Amazon SQS 服務中，有最大 900 秒（ 15 分鐘 ）的限制。

#### 將 Eloquent 模型放進隊列

如果你隊列工作的建構式接收一個 Eloquent 模型，只有這個模型的標記（ identifier ） 會被序列化後放到隊列中。當工作真正開始被處理的時候，隊列系統會自動從資料庫中重新取得完整的模型實例。這個對你的網站應用程式來說是完全透明的，並且預防一些在序列化完整 Eloquent 模型實例時可能遇到的問題。

#### 刪除一個處理中的工作

一旦一個工作被處理過後，這個工作必須從隊列中刪除。假如在工作執行後沒有發生錯誤，這個將會自動完成。

如果你希望能夠手動刪除或著釋放工作，在 `Illuminate\Queue\InteractsWithQueue` trait 中提供 `release` 以及 `delete` 方法的接口。其中 `release` 方法接受單一一個值：你想要等待工作再次能夠執行的秒數。

	public function handle(SendEmail $command)
	{
		if (true)
		{
			$this->release(30);
		}
	}

#### 釋放一個工作回到隊列中

假如在工作執行後發生錯誤，這個工作將會自動被釋放回到隊列之中，如此一來便能夠再次嘗試執行工作。工作會一直被釋放回隊列直到到達應用程式的嘗試上限。這個上限數值可以在使用 `queue:listen` 或 `queue:work` Artisan 命令時候藉由 `--tries` 開關來設定。

#### 檢查工作執行次數

當一個工作執行後發生錯誤，這個工作將會自動的釋放回隊列當中，你可以透過 `attempts` 方法來檢查這個工作已經被執行的次數：

	if ($this->attempts() > 3)
	{
		//
	}

> **注意:** 你的指令處理類別必須使用 `Illuminate\Queue\InteractsWithQueue` 這個 trait 才能夠使用這個方法。

<a name="queueing-closures"></a>
## 隊列閉包

你也可以推送一個閉包去隊列，這個方法非常的方便及快速的來處理需要使用隊列的簡單的任務：

#### 推送一個閉包至隊列

	Queue::push(function($job) use ($id)
	{
		Account::delete($id);

		$job->delete();
	});

> **注意:** 要讓一個元件變數可以在隊列閉包中可以使用我們會透過 `use` 指令，試著傳送主鍵及重覆使用的相關模組在你的隊列工作中，這可以避免其他的序列化行為。

當使用 Iron.io [push queues](#push-queues) 時,你應該在隊列閉包中採取一些其他的預防措施，我們應該在執行工作收到隊列資料時檢查token是否真來自 Iron.io，舉例來說你推送一個隊列工作到 `https://yourapp.com/queue/receive?token=SecretToken`，接下來在你的工作收到隊列的請求時，你就可以檢查token的值是否正確。

<a name="running-the-queue-listener"></a>
## 執行一個隊列監聽

Laravel 內含一個 Artisan 命令，它將推送到隊列的工作拉來下執行，你可以使用 `queue:listen` 命令，來執行這件常駐任務：

#### 開始隊列監聽

	php artisan queue:listen

你也可以指定特定隊列連線讓監聽器使用：

	php artisan queue:listen connection

注意當這個任務開始時，這將會一直持續執行到他被手動停止，你也可以使用一個處理監控像是 [Supervisor](http://supervisord.org/) 來確保這個隊列監聽不會停止執行。

你也可以在 `listen` 指令中使用逗號分隔的隊列連線，來設定不同隊列連線的優先層級：

	php artisan queue:listen --queue=high,low

在這個範列中，總是會優先處理 `high-connection` 中的工作，然後才處理 `low-connection`。

#### 指定工作逾時參數

你也可以設定給每個工作允許執行的秒數：

	php artisan queue:listen --timeout=60

#### 指定隊列休息時間

此外，你也可以指定讓監聽器在拉取新工作時要等待幾秒：

	php artisan queue:listen --sleep=5

注意隊列只會在工作時休息，假如有許多可執行的工作，隊列會持續的處理工作而不會休息

#### 處理隊列上的第一個工作

當你只想處理隊列上的一個工作你可以使用 `queue:work` Artisan 命令：

	php artisan queue:work

<a name="daemon-queue-worker"></a>
## 常駐隊列處理器

在 `queue:work` 中也包含了一個 `--daemon` 選項，強迫隊列處理器持續處理工作，而不會每次都重新啟動框架，這個作法比起 `queue:listen` 可有效減少 CPU 使用量，但是卻增加了佈署時，對於處理中隊列任務的複雜性。

要啟動一個常駐的隊列處理器，使用 `--daemon`：

	php artisan queue:work connection --daemon

	php artisan queue:work connection --daemon --sleep=3

	php artisan queue:work connection --daemon --sleep=3 --tries=3

如你所見 `queue:work` 指令支援 `queue:listen` 大多相同的選項參數，你也可使用 `php artisan help queue:work` 指令來觀看全部可用的選項參數。

### 佈署常駐隊列處理器

最簡單佈署一個應用程式使用常駐隊列處理器的方式，就是將應用程式在開始佈署時轉成維護模式，你可以使用 `php artisan down` 指令來完成這件事情，當這個應用程式在維護模式，Laravel 將不會允許任何來自隊列上的新工作，但會持續的處理已存在的工作。

要重新啟動 `queue` 也是非常容易，請將底下命令加到部署指令：

	php artisan queue:restart

上述指令會在執行完目前的工作後，重新啟動隊列。

> **注意:** 這個指令依賴快取系統來排定重新啟動任務。預設 APCu 無法在命令提示字元中工作。如果你正在使用 APCu 請將 `apc.enable_cli=1` 加到你的 APCu 設定當中。

### 撰寫常駐隊列處理器

常駐隊列處理器不會在處理每一個工作之前都重新啟動框架。因此，你應該注意並小心地在工作處理完成之前釋放佔用的資源。例如，如果你正在使用 GD 函式庫操作圖片，當你完成工作的時候，你應該使用 `imagedestroy` 方法來釋放佔用的記憶體。

同樣地，資料庫連線可能在長時間執行的隊列處理器中斷線，你可以使用 `DB::reconnect` 方法來確保你每次都有一個全新的連線。

<a name="push-queues"></a>
## 推送隊列

你可以利用強大的 Laravel 4 隊列架構來進行推送隊列工作，不需要執行任何的常駐或背景監聽，目前只支援 [Iron.io](http://iron.io) 驅動，在你開始前建立一個 Iron.io 帳號及新增你的 Iron 憑證到 `config/queue.php` 設定檔。

#### 註冊一個推送隊列訂閱

接下來，你可以使用 `queue:subscribe` Artisan 指令註冊一個 URL，這將會接收新的推送隊列工作：

	php artisan queue:subscribe queue_name http://foo.com/queue/receive

現在當你登入你的 Iron 儀表板，你將會看到你新的推送隊列，以及訂閱的 URL，你可以訂閱許多的 URLs 給你希望的隊列，接下來建立一個 route 給你的 `queue/receive` 及從 `Queue::marshal` 方法回傳回應：

	Route::post('queue/receive', function()
	{
		return Queue::marshal();
	});

這裡的 `marshal` 方法會將觸發正確的處理類別，而發送工作到隊列中只要使用一樣的 `Queue::push` 方法。

<a name="failed-jobs"></a>
## 已失敗的工作

事情往往不會如你預期的一樣，有時候你推送工作到隊列會失敗，別擔心，Laravel 包含一個簡單的方法去指定一個工作最多可以被執行幾次，在工作被執行到一定的次數時，他將會新增至 `failed_jobs` 資料表裡，然後失敗工作的資料表名稱可以在 `config/queue.php` 裡進行設定：

要產生一個遷移來建立 `failed_jobs` 資料表，你可以使用 `queue:failed-table` Artisan 指令：

	php artisan queue:failed-table

你可以指定一個最大值來限制一個工作應該最多被執行幾次，在你執行 `queue:listen` 時加上 `--tries`：

	php artisan queue:listen connection-name --tries=3

假如你會想註冊一個事件，這個事件會將會在隊列失敗時被呼叫，你可以使用 `Queue::failing` 方法，這個事件是一個很好的機會讓你可以通知你的團隊透過 e-mail 或 [HipChat](https://www.hipchat.com)。

	Queue::failing(function($connection, $job, $data)
	{
		//
	});

你可能夠直接在隊列工作類別中定義一個 `failed` 方法，這讓你能夠在工作失敗時候，執行一些特定的動作：

	public function failed()
	{
		// 當工作失敗的時候會被呼叫……
	}

### 重新嘗試失敗的工作

要看到所有失敗的工作，你可以使用 `queue:failed` 指令：

	php artisan queue:failed

這個 `queue:failed` 指令將會列出工作 ID、連線、隊列名稱及失敗的時間，可以使用工作 ID 重新執行一個失敗的工作，例如一個已經失敗的工作的 ID 是 5，我們可以使用下面的指令：

	php artisan queue:retry 5

假如你想刪除一個失敗的工作，可以使用 `queue:forget` 指令：

	php artisan queue:forget 5

要刪除全部失敗的工作，可以使用 `queue:flush` 指令：

	php artisan queue:flush
