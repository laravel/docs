# 隊列

- [簡介](#introduction)
- [撰寫任務類別](#writing-job-classes)
    - [產生任務類別](#generating-job-classes)
    - [任務類別結構](#job-class-structure)
- [將任務推送到隊列上](#pushing-jobs-onto-the-queue)
    - [延遲性任務](#delayed-jobs)
    - [從請求中派送任務](#dispatching-jobs-from-requests)
    - [任務事件](#job-events)
- [執行隊列監聽器](#running-the-queue-listener)
    - [Supervisor 設定](#supervisor-configuration)
    - [將任務監聽器設為背景服務](#daemon-queue-listener)
    - [隨著在背景服務的任務監聽器進行佈署](#deploying-with-daemon-queue-listeners)
- [處理失敗的任務](#dealing-with-failed-jobs)
    - [任務失敗事件](#failed-job-events)
    - [重新嘗試執行失敗任務](#retrying-failed-jobs)

<a name="introduction"></a>
## 簡介

Laravel 的隊列服務為不同的隊列後端系統提供一個統一的 API 。隊列允許你將一個耗時的任務延遲處理，例如像寄送 e-mail，這會使得你的應用程式對網頁請求有更快的反應。

<a name="configuration"></a>
### 設定

隊列的設定檔被儲存在 `config/queue.php`。在這個檔案裡你可以找到包含在 Laravel 框架中，每一種隊列驅動的連結設定。它們包含了資料庫、[Beanstalkd](http://kr.github.com/beanstalkd)、[IronMQ](http://iron.io)、[Amazon SQS](http://aws.amazon.com/sqs)、[Redis](http://redis.io) 以及提供本機使用的 synchronous 驅動。

另外框架也提供了 `null` 這個隊列驅動，用來丟棄隊列任務。

### 驅動必要設定

#### 資料庫

要使用 `database` 這個隊列驅動的話，需要建立一個資料表來記住任務，你可以用 `queue:table` 這個 Artisan 指令來建立這個資料表的遷移類別。當遷移類別建好後，就可以用 `migrate` 這個指令來將資料表在資料庫中建立起來。

    php artisan queue:table

    php artisan migrate

#### 其他隊列系統的相依套件

要使用列表裡的隊列服務前，必須安裝以下的相依套件：

- Amazon SQS：`aws/aws-sdk-php ~3.0`
- Beanstalkd：`pda/pheanstalk ~3.0`
- IronMQ：`iron-io/iron_mq ~2.0|~4.0`
- Redis：`predis/predis ~1.0`

<a name="writing-job-classes"></a>
## 撰寫任務類別

<a name="generating-job-classes"></a>
### 產生任務類別

在你的應用程式中，所有能放在隊列的任務類別預設放在 `app/Jobs` 目錄下，你可以用以下的 Artisan 指令來產生一個新的隊列任務：

    php artisan make:job SendReminderEmail --queued

這個指令將會在 `app/Jobs` 下產生一個新類別，而這個類別會實作 `Illuminate\Contracts\Queue\ShouldQueue` 介面，讓 Laravel 知道這個任務應該是被放到隊列裡，而不是直接執行。

<a name="job-class-structure"></a>
### 任務類別結構

任務類別的結構很簡單，一般來說只會包含一個讓隊列用來呼叫此任務的 `handle` 方法。我們用以下這個類別來做示範：

    <?php

    namespace App\Jobs;

    use App\User;
    use App\Jobs\Job;
    use Illuminate\Contracts\Mail\Mailer;
    use Illuminate\Queue\SerializesModels;
    use Illuminate\Queue\InteractsWithQueue;
    use Illuminate\Contracts\Bus\SelfHandling;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class SendReminderEmail extends Job implements SelfHandling, ShouldQueue
    {
        use InteractsWithQueue, SerializesModels;

        protected $user;

        /**
         * 建立一個新的任務實例。
         *
         * @param  User  $user
         * @return void
         */
        public function __construct(User $user)
        {
            $this->user = $user;
        }

        /**
         * 執行任務。
         *
         * @param  Mailer  $mailer
         * @return void
         */
        public function handle(Mailer $mailer)
        {
            $mailer->send('emails.reminder', ['user' => $this->user], function ($m) {
                //
            });

            $this->user->reminders()->create(...);
        }
    }

注意，在這個例子裡我們在任務類別的建構子中直接傳遞了一個 [Eloquent 模型](/docs/{{version}}/eloquent)。因為我們在任務類別裡引用了 `SerializesModels` 這個 trait，使得 Eloquent 模型在處理任務的時候可以被優雅地序列化和反序列化。如果你的隊列任務類別在建構子接受一個 Eloquent 模型，那麼只有可識別出該模型的屬性會被序列化至隊列裡。當任務實際被執行時，隊列系統會自動從資料庫中重新取回完整的模型。整個過程對你的應用程式來說是透明的，這樣可以避免序列化完整的 Eloquent 的模式實例所帶來的問題。

在隊列處理任務時，會呼叫 `handle` 方法，而這裡我們也可以透過 `handle` 方法的參數型別提示，讓 Laravel 的[服務容器](/docs/{{version}}/container)自動注入相依物件。

#### 當發生錯誤的時候

如果在任務處理時拋出了一個例外，它會自動被釋放回隊列裡再次嘗試執行。當該任務一直出錯時，它會不斷被釋出再重試，直到超過你的應用程式所允許的最大重試值。最大重試值可以在執行 `queue:listen` 或 `queue:work` 指令時，用 `--tries` 選項來設定；執行隊列監聽器的更多資訊在稍後會有[詳細說明](#running-the-queue-listener)。

#### 手動釋放任務

如果你想手動釋放任務，那麼在產生出來的任務類別已經引用了 `InteractsWithQueue` 這個 trait，它提供了 `release` 方法讓我們可以釋放任務。在 `release` 方法中接受一個數值參數，它表示直到這個任務可以被重新執行之前，你願意等待的秒數。

    public function handle(Mailer $mailer)
    {
        if (condition) {
            $this->release(10);
        }
    }

#### 檢查重試次數

如同前面提到的，當任務被處理時發生了一個例外，它會自動被釋放回隊列中。這時候你可以用 `attempt` 方法來檢查已經重試的次數：

    public function handle(Mailer $mailer)
    {
        if ($this->attempts() > 3) {
            //
        }
    }

<a name="pushing-jobs-onto-the-queue"></a>
## 將任務推送到隊列上

在 `app/Http/Controllers/Controller.php` 中 Laravel 定義了一個預設控制器，它引用了 `DispatchesJob` 這個 trait；而這個 trait 提供了數個可以讓你方便推送任務到隊列的方法，例如 `dispatch` 方法：

    <?php

    namespace App\Http\Controllers;

    use App\User;
    use Illuminate\Http\Request;
    use App\Jobs\SendReminderEmail;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * 寄送提醒的 e-mail 給指定使用者。
         *
         * @param  Request  $request
         * @param  int  $id
         * @return Response
         */
        public function sendReminderEmail(Request $request, $id)
        {
            $user = User::findOrFail($id);

            $this->dispatch(new SendReminderEmail($user));
        }
    }

當然有時你不見得是從應用程式的路由或控制器來派發任務，因此你可以在應用程式中的任何類別裡引用 `DispatchesJobs` 這個 trait ，以便使用它的各種派發方法。以下就是使用該 trait 的類別範例：

    <?php

    namespace App;

    use Illuminate\Foundation\Bus\DispatchesJobs;

    class ExampleClass
    {
        use DispatchesJobs;
    }

#### 指定任務所屬的隊列

你可以指定任務應該要送到哪一個隊列。

要推送任務到不同的隊列上，你要將任務先「分類」，甚至可能要排定每個隊列能有多少作業器可以執行任務。這並不是指任務會推送到你在設定檔所定義的不同隊列連結裡，而是推送到某個有單一連結的隊列。要指定任務執行的隊列，可以用任務實例的 `onQueue` 方法。`onQueue` 是 `Illuminate\Bus\Queueable` trait 所提供的方法，而它已經包含在 `App\Jobs\Job` 基底類別中：

    <?php

    namespace App\Http\Controllers;

    use App\User;
    use Illuminate\Http\Request;
    use App\Jobs\SendReminderEmail;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * 寄送提醒的 e-mail 給指定使用者。
         *
         * @param  Request  $request
         * @param  int  $id
         * @return Response
         */
        public function sendReminderEmail(Request $request, $id)
        {
            $user = User::findOrFail($id);

            $job = (new SendReminderEmail($user))->onQueue('emails');

            $this->dispatch($job);
        }
    }

<a name="delayed-jobs"></a>
### 延遲性任務

有時你可能會希望隊列任務能晚一點再執行，例如在使用者註冊後 15 分鐘後才透過隊列任務寄送提醒信件。你可以透過任務類別引用的 `Illuminate\Bus\Queueable` 這個 trait 所提供的 `delay` 方法來達成這個目的：

    <?php

    namespace App\Http\Controllers;

    use App\User;
    use Illuminate\Http\Request;
    use App\Jobs\SendReminderEmail;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * 寄送提醒的 e-mail 給指定使用者。
         *
         * @param  Request  $request
         * @param  int  $id
         * @return Response
         */
        public function sendReminderEmail(Request $request, $id)
        {
            $user = User::findOrFail($id);

            $job = (new SendReminderEmail($user))->delay(60);

            $this->dispatch($job);
        }
    }

在這個範例裡，我們指定該任務要在交給作業器執行前先延遲 60 秒。

> **注意：**Amazon 的 SQS 服務最大延遲時間是 15 分鐘。

<a name="dispatching-jobs-from-requests"></a>
### 從請求中派送任務

在任務中對應到 HTTP 請求的變數是很常見的，所以與其強制你手動去對每個請求做這件事，Laravel 直接提供了一些輔助方法讓你更容易做到它；像是在 `DispatchesJobs` 這個 trait 就提供了 `dispatchFrom` 方法，而 Laravel 基礎控制器就預設引入了這個 trait：

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use App\Http\Controllers\Controller;

    class CommerceController extends Controller
    {
        /**
         * 處理指定的訂單。
         *
         * @param  Request  $request
         * @param  int  $id
         * @return Response
         */
        public function processOrder(Request $request, $id)
        {
            // 處理該請求...

            $this->dispatchFrom('App\Jobs\ProcessOrder', $request);
        }
    }

這個方法會檢查任務類別的建構子，並且從 HTTP 請求 (或任何 `ArrayAccess` 物件) 中取出變數，來填補建構子中需要的參數。所以如果我們的任務類別建構子接受一個 `productId` 變數的話，那麼隊列就會試著從 HTTP 請求中提出 `productId` 這個參數。

你也可以直接將一個陣列傳入到 `dispatchFrom` 方法的第三個參數裡，這個陣列就會被用來填補建構子中任何不在請求裡的變數：

    $this->dispatchFrom('App\Jobs\ProcessOrder', $request, [
        'taxPercentage' => 20,
    ]);

<a name="job-events"></a>
### Job Events

#### Job Completion Event

The `Queue::after` method allows you to register a callback to be executed when a queued job executes successfully. This callback is a great opportunity to perform additional logging, queue a subsequent job, or increment statistics for a dashboard. For example, we may attach a callback to this event from the `AppServiceProvider` that is included with Laravel:

    <?php

    namespace App\Providers;

    use Queue;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            Queue::after(function ($connection, $job, $data) {
                //
            });
        }

        /**
         * Register the service provider.
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

<a name="running-the-queue-listener"></a>
## 執行隊列監聽器

#### 啟動隊列監聽器

Laravel 引入了一個 Artisan 指令，用來執行被推送到隊列裡的任務。你可以透過 `queue:listen` 指令來執行監聽器：

    php artisan queue:listen

你也可以指定監聽器應該利用哪一個隊列連結：

    php artisan queue:listen connection

要注意的是，一旦這個工作指令啟動後，它會持續運作直到它被手動停止。你可以利用像 [Supervisor](http://supervisord.org/) 這樣的行程監控軟體，來確保隊列監聽器不會停止執行。

#### 隊列優先序

你可以給 `listen` 指令一個以逗號分隔的隊列連結列表，來設定隊列的優先序：

    php artisan queue:listen --queue=high,low

在這個範例裡，在 `high` 這個隊列裡的任務永遠會先被處理，然後才是 `low` 隊列裡的任務。

#### 指定任務的逾時參數

你還可以設定每個任務所被允許執行的時間長度，單位是秒數：

    php artisan queue:listen --timeout=60

#### 指定隊列的休眠期

此外，你可以指定隊列要等幾秒再拿取新的任務來執行：

    php artisan queue:listen --sleep=5

注意這裡是指隊列在沒有任務的狀態下才會休眠；如果已經有多個任務卡在這個隊列上，那麼它會持續運作而不會休眠。

<a name="supervisor-configuration"></a>
### Supervisor 設定

Supervisor 是一個在 Linux 作業系統上的行程監控軟體，它會在 `queue:listen` 或 `queue:work` 指令發生失敗後自動重啟它們。要在 Ubuntu 安裝 Supervisor，可以用以下指令：

    sudo apt-get install supervisor

Supervisor 的設定檔一般是放在 `/etc/supervisor/conf.d` 目錄下，在這個目錄中你可以建立任意數量的設定檔，要求 Supervisor 來監控你的行程。例如我們建立一個 `laravel-worker.conf` 來啟動與監控一個 `queue:work` 行程：

    [program:laravel-worker]
    process_name=%(program_name)s_%(process_num)02d
    command=php /home/forge/app.com/artisan queue:work sqs --sleep=3 --tries=3 --daemon
    autostart=true
    autorestart=true
    user=forge
    numprocs=8
    redirect_stderr=true
    stdout_logfile=/home/forge/app.com/worker.log

在這個範例裡的 `numprocs` 指令會要求 Supervisor 執行並監控 8 個 `queue:work` 行程，並且在它們執行失敗時重新啟動。當然，你必須更改 `command` 指令的 `queue:work sqs` 部分，以顯示你所選擇的隊列驅動。

當這個設定檔建立後，你需要更新 Supervisor 的設定，並用以下指令來啟動該行程：

    sudo supervisorctl reread

    sudo supervisorctl update

    sudo supervisorctl start laravel-worker:*

更多有關 Supervisor 的設定與使用，請參考 [Supervisor 官方文件](http://supervisord.org/index.html)。或是你可以使用 [Laravel Forge](https://forge.laravel.com) 所提供的 Web 介面，來自動設定與管理你的 Supervisor 設定。

<a name="daemon-queue-listener"></a>
### 將任務監聽器設為背景服務

在 `queue:work` Artisan 指令裡包含了 `--daemon` 選項，強迫隊列作業器持續處理任務，而不需要重新啟動整個框架。比起 `queue:listen` 指令，這會顯著減少 CPU 的用量。

用 `--daemon` 旗標在背景服務模式下啟動隊列作業器：

    php artisan queue:work connection --daemon

    php artisan queue:work connection --daemon --sleep=3

    php artisan queue:work connection --daemon --sleep=3 --tries=3

如你所見，`queue:work` 指令提供了多數和 `queue:listen` 指令相同的選項；你可以用 `php artisan help queue:work` 指令來查看所有可用的選項。

### 在背景服務的隊列監聽器中開發所要考量的事項

在背景執行的隊列監聽器在處理完每個任務前，不會重新啟動框架；因此你應該在任務執行完成前，謹慎地釋放任何佔用記憶體較重的資源。例如你利用 GD 函式庫處理影像，就要在結束前用 `imagedestroy` 來釋放記憶體。

相同地，你的資料庫連結也要在使用完後關閉連線；你可以用 `DB::reconnect` 方法來確保有新的資料庫連線。

<a name="deploying-with-daemon-queue-listeners"></a>
### 隨著在背景服務的任務監聽器進行佈署

從背景服務的隊列作業器是長時間執行的行程來看，除非重新啟動，否則它們將不會理會任何程式碼上的變更。所以要佈署一個有用到背景服務的隊列作業器的應用程式，最簡單的方法就是在佈署指令稿中重新啟動作業器。你可以在你的佈署指令裡加上以下指令，來優雅地重新啟動所有作業器：

    php artisan queue:restart

這個指令會優雅地告知所有隊列作業器，在它們完成處理目前任務後重新啟動，所以就不會任務遺失的問題。

> **注意：**這個指令依靠快取系統來安排重新啟動；預設狀況下，APCu 無法在 CLI 的任務上運作；如果你正在使用 APCu 的話，要把 `apc.enable_cli=1` 加到你的 APCu 設定裡。

<a name="dealing-with-failed-jobs"></a>
## 處理失敗的任務

計劃永遠跟不上變化，有時候你的隊列任務就是會失敗。不過別擔心，我們有準備好它發生時的應付方法。Laravel 有個便利的方式可以指定任務的最大重試次數。當任務執行超過該重試次數，它就會被寫入至 `failed_jobs` 這個資料表。而失敗任務的名稱可以在 `config/queue.php` 這個設定檔中設定。

要建立 `failed_jobs` 資料表的遷移類別，你可以用 `queue:failed-table` 指令：

    php artisan queue:failed-table

當你執行[隊列監聽器](#running-the-queue-listener)時，你可以用 `queue:listen` 指令的 `--tries` 參數來指定任務的最大重試次數：

    php artisan queue:listen connection-name --tries=3

<a name="failed-job-events"></a>
### 任務失敗事件

如果你想註冊一個當隊列任務失敗時會被呼叫的事件，你可以用 `Queue::failing` 方法；這樣你就有機會透過這個事件，用 e-mail 或 [HipChat](https://www.hipchat.com) 來通知你的團隊。例如我們可以在 Laravel 內建的 `AppServiceProvider` 中對這個事件附加一個回呼函式：

    <?php

    namespace App\Providers;

    use Queue;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 啟動任何應用程式的服務。
         *
         * @return void
         */
        public function boot()
        {
            Queue::failing(function ($connection, $job, $data) {
                // 通知團隊失敗的任務...
            });
        }

        /**
         * 註冊服務容器。
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

#### 任務類別裡處理失敗的方法

如果想有更細膩的控制，你可以在直接在任務類別裡定義一個 `failed` 方法，這個方法允許你指定在錯誤發生時該怎麼動作。

    <?php

    namespace App\Jobs;

    use App\Jobs\Job;
    use Illuminate\Contracts\Mail\Mailer;
    use Illuminate\Queue\SerializesModels;
    use Illuminate\Queue\InteractsWithQueue;
    use Illuminate\Contracts\Bus\SelfHandling;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class SendReminderEmail extends Job implements SelfHandling, ShouldQueue
    {
        use InteractsWithQueue, SerializesModels;

        /**
         * 執行任務。
         *
         * @param  Mailer  $mailer
         * @return void
         */
        public function handle(Mailer $mailer)
        {
            //
        }

        /**
         * 處理一個失敗的任務
         *
         * @return void
         */
        public function failed()
        {
            // 當任務失敗時會被呼叫...
        }
    }

<a name="retrying-failed-jobs"></a>
### 重新嘗試執行失敗任務

要檢視你在 `failed_jobs` 資料表中所有失敗的任務，你可以用 `queue:failed` 這個 Artisan 指令：

    php artisan queue:failed

`queue:failed` 指令會列出所有任務編號、連結、隊列以及失敗時間，任務編號會用在重試失敗的任務。例如要重試一個編號為 5 的失敗任務，其指令如下：

    php artisan queue:retry 5

To retry all of your failed jobs, use `queue:retry` with `all` as the ID:

    php artisan queue:retry all

如果你想刪除掉一個失敗任務，可以用 `queue:forget` 指令：

    php artisan queue:forget 5

`queue:flush` 指令可以讓你刪除所有失敗的任務：

    php artisan queue:flush
