# 佇列

- [設定](#configuration)
- [基本用法](#basic-usage)
- [佇列閉包](#queueing-closures)
- [起動佇列監聽](#running-the-queue-listener)
- [常駐佇列工作](#daemon-queue-worker)
- [推送佇列](#push-queues)
- [失敗的工作](#failed-jobs)

<a name="configuration"></a>
## 設定

Laravel 佇列元件提供一個統一的API整合了許多不同的佇列服務，佇列允許你將一個執行任務延後執行，例如寄送郵件延後至你指定的時間，進而大幅的加快你的網站應用程式的速度。

佇列的設定檔在 `app/config/queue.php`，在這個檔案你將可以找到框架中每種不同的佇列服務的連線設定，其中包含了 [Beanstalkd](http://kr.github.com/beanstalkd)，[IronMQ](http://iron.io)，[Amazon SQS](http://aws.amazon.com/sqs)，[Redis](http://redis.io)，以及同步(本地端使用)驅動設定。

下列的 composer.json 設定可以依照你使用的佇列服務必需在使用前安裝：

- Beanstalkd: `pda/pheanstalk ~3.0`
- Amazon SQS: `aws/aws-sdk-php`
- IronMQ: `iron-io/iron_mq`

<a name="basic-usage"></a>
## 基本用法

#### 推送一個工作至佇列

要推送一個新的工作至佇列，請使用 `Queue::push` 方法：

	Queue::push('SendEmail', array('message' => $message));

#### 宣告一個工作處理程序

`push` 方法的第一個參數為應該處理這個工作的類別方法名稱，第二個參數是一個要傳遞至處理程序的資料陣列，一個工作處理程序應該參照下列宣告：

	class SendEmail {

		public function fire($job, $data)
		{
			//
		}

	}

注意如果你未在第一個參數指定工作處理的類別及方法(如 SendEmail@process)，那 `fire` 為類別中預設必需的方法用來接收被推送至佇列 `Job` 實例以及 `data`。

#### 指定一個特定的處理程序方法

假如你想要用一個 `fire` 以外的方法處理工作，你可以在推送工作時指定方法如下：

	Queue::push('SendEmail@send', array('message' => $message));

#### 指定佇列使用特定連線

你也可指定佇列工作送至指定的連線：

	Queue::push('SendEmail@send', array('message' => $message), 'emails');

#### 傳送相同的資料去多個連線

如果你需要傳送一樣的資料去幾個不同的佇列伺服器，你也可以使用 `Queue::bulk` 方法：

	Queue::bulk(array('SendEmail', 'NotifyUser'), $payload);

#### 延遲執行一個工作

有時後你也希望延遲一個佇列工作的執行，舉例來說你希望一個佇列工作在客戶註冊 15 分鐘後寄送一個 e-mail，你可以使用 `Queue::later` 方法來完成這件事情：

	$date = Carbon::now()->addMinutes(15);

	Queue::later($date, 'SendEmail@send', array('message' => $message));

在這個範例中，我們使用 [Carbon](https://github.com/briannesbitt/Carbon) 日期函式庫來指定我們希望佇列工作希望延遲的時間，另外你也可傳送一個整數來設定你希望延遲的秒數。

#### 刪除一個處理中的工作

當你已經開始處理完成一個佇列工作，它就必需在佇列中刪除，我們可以透過 `Job` 實例中的 `delete` 方法來完成這件事：

	public function fire($job, $data)
	{
		// Process the job...

		$job->delete();
	}

#### 釋放一個工作回到佇列中

假如你希望將一個工作釋放回佇列之中，你可以透過 `release` 方法來完成這件事情：

	public function fire($job, $data)
	{
		// Process the job...

		$job->release();
	}

你也可以指定秒數來讓這個工作延遲釋放：

	$job->release(5);

#### 檢查工作執行次數

當一個工作執行後發生錯誤，這個工作將會自動的釋放回佇列當中，你可以透過 `attempts` 方法來檢查這個工作已經被執行的次數：

	if ($job->attempts() > 3)
	{
		//
	}

#### 取得一個工作的 ID

你也可以取得這個工作的識別碼：

	$job->getJobId();

<a name="queueing-closures"></a>
## 佇列閉包

你也可以推送一個閉包去佇列，這個方法非常的方便及快速的來處理需要使用佇列的簡單的任務：

	Queue::push(function($job) use ($id)
	{
		Account::delete($id);

		$job->delete();
	});

> **註記:** 要讓一個元件變數可以在佇列閉包中可以使用我們會透過 `use` 指令，試著傳送主鍵及重覆使用的相關模組在你的佇列工作中，這可以避免其他的序列化行為。

當使用 Iron.io [push queues](#push-queues) 時,你應該在佇列閉包中采取一些其他的預防措施，我們應該在執行工作收到佇列資料時檢查token是否真來自 Iron.io，舉例來說你推送一個佇列工作到 `https://yourapp.com/queue/receive?token=SecretToken`，接下來在你的工作收到佇列的請求時，你就可以檢查token的值是否正確。

<a name="running-the-queue-listener"></a>
## 執行一個佇列監聽

Laravel 內含一個 Artisan 指令，它將推送到佇列的工作拉來下執行，你可以使用 `queue:listen` 命令，來執行這件常駐任務：

#### 開始佇列監聽

	php artisan queue:listen

你也可以指定特定佇列連線讓監聽器使用：

	php artisan queue:listen connection

注意當這個任務開始時，這將會一直持續執行到他被手動停止，你也可以使用一個處理監控像是 [Supervisor](http://supervisord.org/) 來確保這個佇列監聽不會停止執行。

你也可以在 `listen` 指令中使用逗號分隔不同的佇列連線來設定佇列的重要性：

	php artisan queue:listen --queue=high,low

在這個範列中 `high-connection` 將總是會優先處理佇列的工作，相對於 `low-connection`

#### 指定工作逾時參數

你也可以設定給每個工作允許執行的秒數：

	php artisan queue:listen --timeout=60

#### 指定佇列休息時間

此外，你也可以指定讓監聽器在拉取新工作時要等待幾秒：

	php artisan queue:listen --sleep=5

注意佇列只會佇列上沒有工作時休息，假如有許多可執行的工作，佇列監聽將持續的處理工作不會休息

#### 處理第佇列上的一個工作

當你只想處理佇列上的一個工作你可以使用 `queue:work` 指令：

	php artisan queue:work

<a name="daemon-queue-worker"></a>
## 常駐佇列處理器

`queue:work` 也包含了一個 `--daemon` 選項強迫佇列處理器可以持續處理工作即使重新啟動框架，這個作法相對的比 `queue:listen` 可有效的減少CPU的使用量，但是卻增加了你佈署時正在處理中的佇列任務的複雜性。

當開始一個佇列處理器於常駐模式，使用 `--daemon` 旗標：

	php artisan queue:work connection --daemon

	php artisan queue:work connection --daemon --sleep=3

	php artisan queue:work connection --daemon --sleep=3 --tries=3


如你所見 `queue:work` 指令支援 `queue:listen` 大多相同的選項參數，你也可使用 `php artisan help queue:work` 指令來觀看全部可用的選項參數。

### 佈署常駐佇列處理器

最簡單的方式佈署一個應用程式使用常駐佇列處理器就是將應用程式在開始佈署時使用維護模式，你可以使用 `php artisan down` 指令來完成這件事情，當這個應用程式在維護模式，Laravel 將不會允許任何來自佇列上的新工作，但會持續的處理已存在的工作，當過了足夠的時間所有你正在執行的工作都已處理完(通常不會很久約 30-60 秒)，你可以停止處理器及繼續處理你的佈署工作。

假如你使用 Supervisor 或 Laravel Forge，那你通常就會使用下面的指令來停止處理器：

	php artisan queue:restart

當這些佇列都處理完且你更新完你的伺服器上的程式碼，你應該重啟常駐佇列處理器，假如你使用 Supervisor，通常會使用下面的指令：

<a name="push-queues"></a>
## 推送佇列

你可以利用強大的 Laravel 4 佇列架構來進行推送佇列工作，不需要執行任何的常駐或背景監聽，目前只支援 [Iron.io](http://iron.io) 驅動，在你開始前建立一個 Iron.io 帳號及新增你的 Iron 憑證到 `app/config/queue.php` 設定檔。

#### 註冊一個推送佇列訂閱

接下來，你可以使用 `queue:subscribe` 指令註冊一個URL，這將會接收新的推送佇列工作：

	php artisan queue:subscribe queue_name http://foo.com/queue/receive

現在當你登入你的Iron儀表板，你將會看到你新的推送佇列，以及訂閱的 URL，你可以訂閱許多的URLs給你希望的佇列，接下來建立一個 route 給你的 `queue/receive` 及從 `Queue::marshal` 方法回傳回應：

	Route::post('queue/receive', function()
	{
		return Queue::marshal();
	});

`marshal` 方法會將工作處理到正確的類別，而發送工作到佇列中只要使用一樣的 `Queue::push` 方法。

<a name="failed-jobs"></a>
## 已失敗的工作

事情往往不會如你預期的一樣，有時後你推送工作到佇列會失敗，別擔心，Laravel 包含一個簡單的方法去指定一個工作最多可以被執行幾次，在工作被執行到一定的次數時，他將會新增至 `failed_jobs` 資料表裡，然後失敗工作的資料表名稱可以在 `app/config/queue.php` 裡進行設定：

要新增一個migration建立 `failed_jobs` 資料表，你可以使用 `queue:failed-table` 指令：

	php artisan queue:failed-table

你可以指定一個最大值來限制一個工作應該最多被執行幾次透過 `--tries` 這個選項參數在你執行 `queue:listen` 的時後：

	php artisan queue:listen connection-name --tries=3

假如你會想註冊一個事件，這個事件會將會在佇列失敗時被呼叫，你可以使用 `Queue::failing` 方法，這個事件是一個很好的機會讓你可以通知你的團隊透過 e-mail 或 [HipChat](https://www.hipchat.com)。

	Queue::failing(function($connection, $job, $data)
	{
		//
	});

要看到所有的失敗工作，你可以使用 `queue:failed` 指令：

	php artisan queue:failed

`queue:failed` 指令將會列出工作的 ID、連線、佇列名稱及失敗的時間，工作的 ID 也可以重新執行一個已經失敗的工作，例如一個已經失敗的工作他的 ID 是 5，我們可以使用下面的指令：

	php artisan queue:retry 5

假如你會想刪除一個已失敗的工作，你可以使用 `queue:forget` 指令：

	php artisan queue:forget 5

要刪除全部失敗的工作你可以使用 `queue:flush` 指令：

	php artisan queue:flush
