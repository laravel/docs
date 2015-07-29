# 隊列

- [簡介](#introduction)
- [撰寫任務類別](#writing-job-classes)
    - [產生任務類別](#generating-job-classes)
    - [任務類別結構](#job-class-structure)
- [將任務推送到隊列上](#pushing-jobs-onto-the-queue)
    - [延遲性任務](#delayed-jobs)
    - [從請求中派送任務](#dispatching-jobs-from-requests)
- [執行隊列監聽器](#running-the-queue-listener)
    - [Supervisor 設定](#supervisor-configuration)
    - [將任務監聽器設為背景服務](#daemon-queue-listener)
    - [隨著在背景服務的任務監聽器進行佈署](#deploying-with-daemon-queue-listeners)
- [處理失敗的任務](#dealing-with-failed-jobs)
    - [任務失敗事件](#failed-job-events)
    - [重新嘗試執行失敗任務](#retrying-failed-jobs)

<a name="introduction"></a>
## 簡介

The Laravel queue service provides a unified API across a variety of different queue back-ends. Queues allow you to defer the processing of a time consuming task, such as sending an e-mail, until a later time which drastically speeds up web requests to your application.

Laravel 的隊列服務為不同的隊列後端系統提供一個統一的 API 。隊列允許你將一個耗時的任務延遲處理，例如像寄送 Email ，這會使得你的應用程式對網頁請求有更快的反應。

<a name="configuration"></a>
### Configuration
### 設定

The queue configuration file is stored in `config/queue.php`. In this file you will find connection configurations for each of the queue drivers that are included with the framework, which includes a database, [Beanstalkd](http://kr.github.com/beanstalkd), [IronMQ](http://iron.io), [Amazon SQS](http://aws.amazon.com/sqs), [Redis](http://redis.io),  and synchronous (for local use) driver.

隊列的設定檔為 `config/queue.php` ，在這個檔案裡你可以找到包含在 Laravel 框架中，每一種隊列驅動的連結設定。它們包含了資料庫、 [Beanstalkd](http://kr.github.com/beanstalkd) 、 [IronMQ](http://iron.io) 、 [Amazon SQS](http://aws.amazon.com/sqs) 、 [Redis](http://redis.io) 以及提供本機使用的 synchronous 驅動。

A `null` queue driver is also included which simply discards queued jobs.

另外框架也提供了 `null` 這個隊列驅動，用來丟棄隊列任務。

### Driver Prerequisites
### 驅動必要設定

#### Database
#### 資料庫

In order to use the `database` queue driver, you will need a database table to hold the jobs. To generate a migration that creates this table, run the `queue:table` Artisan command. Once the migration is created, you may migrate your database using the `migrate` command:

要使用 `database` 這個隊列驅動的話，需要建立一個資料表來記住任務，你可以用 `queue:table` 這個 Artisan 指令來建立這個資料表的遷移類別。當遷移類別建好後，就可以用 `migrate` 這個指令來將資料表在資料庫中建立起來。

    php artisan queue:table

    php artisan migrate

#### Other Queue Dependencies
#### 其他隊列系統的相依套件

The following dependencies are needed for the listed queue drivers:

要使用列表裡的隊列服務前，必須安裝以下的相依套件：

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~3.0`
- IronMQ: `iron-io/iron_mq ~2.0`
- Redis: `predis/predis ~1.0`

<a name="writing-job-classes"></a>
## Writing Job Classes
## 撰寫任務類別

<a name="generating-job-classes"></a>
### Generating Job Classes
### 產生任務類別

By default, all of the queueable jobs for your application are stored in the `app/Jobs` directory. You may generate a new queued job using the Artisan CLI:

在你的應用程式中，所有能放在隊列的任務類別預設放在 `app/Jobs` 目錄下，你可以用以下的 Artisan 指令來產生一個新的隊列任務：

    php artisan make:job SendReminderEmail --queued

This command will generate a new class in the `app/Jobs` directory, and the class will implement the `Illuminate\Contracts\Queue\ShouldQueue` interface, indicating to Laravel that the job should be pushed onto the queue instead of run synchronously.

這個指令將會在 `app/Jobs` 下產生一個新類別，而這個類別會實作 `Illuminate\Contracts\Queue\ShouldQueue` 介面，讓 Laravel 知道這個任務應該是被放到隊列裡，而不是直接執行。

<a name="job-class-structure"></a>
### Job Class Structure

Job classes are very simple, normally containing only a `handle` method which is called when the job is processed by the queue. To get started, let's take a look at an example job class:

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
         * Create a new job instance.
         *
         * @param  User  $user
         * @return void
         */
        public function __construct(User $user)
        {
            $this->user = $user;
        }

        /**
         * Execute the job.
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

In this example, note that we were able to pass an [Eloquent model](/docs/{{version}}/eloquent) directly into the queued job's constructor. Because of the `SerializesModels` trait that the job is using, Eloquent models will be gracefully serialized and unserialized when the job is processing. If your queued job accepts an Eloquent model in its constructor, only the identifier for the model will be serialized onto the queue. When the job is actually handled, the queue system will automatically re-retrieve the full model instance from the database. It's all totally transparent to your application and prevents issues that can arise from serializing full Eloquent model instances.

注意，在這個例子裡我們在任務類別的建構子中直接傳遞了一個 [Eloquent 模型](/docs/{{version}}/eloquent) 。因為我們在任務類別裡引用了 `SerializesModels` 這個 trait ，使得 Eloquent 模型在處理任務的時候可以被優雅地序列化和反序列化。如果你的隊列任務類別在建構子接受一個 Eloquent 模型，那麼只有可識別出該模型的屬性會被序列化至隊列裡。當任務實際被執行時，隊列系統會自動從資料庫中重新取回完整的模型。整個過程對你的應用程式來說是透明的，這樣可以避免序列化完整的 Eloquent 的模式實例所帶來的問題。

The `handle` method is called when the job is processed by the queue. Note that we are able to type-hint dependencies on the `handle` method of the job. The Laravel [service container](/docs/{{version}}/container) automatically injects these dependencies.

在隊列處理任務時，會呼叫 `handle` 方法，而這裡我們也可以透過 `handle` 方法的參數型別提示，來讓 Laravel 的 [service container](/docs/{{version}}/container) 自動注入相依物件。

#### When Things Go Wrong
#### 當發生錯誤的時候

If an exception is thrown while the job is being processed, it will automatically be released back onto the queue so it may be attempted again. The job will continue to be released until it has been attempted the maximum number of times allowed by your application. The number of maximum attempts is defined by the `--tries` switch used on the `queue:listen` or `queue:work` Artisan jobs. More information on running the queue listener [can be found below](#running-the-queue-listener).

如果在任務處理時拋出了一個異常，它會自動被釋放回隊列裡再次嘗試執行。當該任務一直出錯時，它會不斷被釋出再重試，直到超過你的應用程式所允許的最大重試值。最大重試值可以在執行 `queue:listen` 或 `queue:work` 指令時，用 `--tries` 選項來設定；執行隊列監聽器的更多資訊在稍後會有[詳細說明](#running-the-queue-listener)。

#### Manually Releasing Jobs
#### 手動釋放任務

If you would like to `release` the job manually, the `InteractsWithQueue` trait, which is already included in your generated job class, provides access to the queue job `release` method. The `release` method accepts one argument: the number of seconds you wish to wait until the job is made available again:

如果你想手動釋放任務，那麼在產生出來的任務類別已經引用了 `InteractsWithQueue` 這個 Trait ，它提供了 `release` 方法讓我們可以釋放任務。在 `release` 方法中接受一個數值參數，它表示直到這個任務可以被重新執行之前，你願意等待的秒數。

    public function handle(Mailer $mailer)
    {
        if (condition) {
            $this->release(10);
        }
    }

#### Checking The Number Of Run Attempts
#### 檢查重試次數

As noted above, if an exception occurs while the job is being processed, it will automatically be released back onto the queue. You may check the number of attempts that have been made to run the job using the `attempts` method:

如同前面提到的，當任務被處理時發生了一個異常，它會自動被釋放回隊列中。這時候你可以用 `attempt` 方法來檢查已經重試的次數：

    public function handle(Mailer $mailer)
    {
        if ($this->attempts() > 3) {
            //
        }
    }

<a name="pushing-jobs-onto-the-queue"></a>
## Pushing Jobs Onto The Queue
## 將任務推送到隊列上

The default Laravel controller located in `app/Http/Controllers/Controller.php` uses a `DispatchesJobs` trait. This trait provides several methods allowing you to conveniently push jobs onto the queue, such as the `dispatch` method:

在 `app/Http/Controllers/Controller.php` 中 Laravel 定義了一個預設控制器，它引用了 `DispatchesJob` 這個 Trait ；而這個 Trait 提供了數個可以讓你方便推送任務到隊列的方法，例如 `dispatch` 方法：

    <?php

    namespace App\Http\Controllers;

    use App\User;
    use Illuminate\Http\Request;
    use App\Jobs\SendReminderEmail;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * Send a reminder e-mail to a given user.
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

Of course, sometimes you may wish to dispatch a job from somewhere in your application besides a route or controller. For that reason, you can include the `DispatchesJobs` trait on any of the classes in your application to gain access to its various dispatch methods. For example, here is a sample class that uses the trait:

當然有時你不見得是從應用程式的路由或控制器來派發任務，因此你可以在應用程式中的任何類別裡引用 `DispatchesJobs` 這個 trait ，以便使用它的各種派發方法。以下就是使用該 trait 的類別範例：

    <?php

    namespace App;

    use Illuminate\Foundation\Bus\DispatchesJobs;

    class ExampleClass
    {
        use DispatchesJobs;
    }

#### Specifying The Queue For A Job
#### 指定任務所屬的隊列

You may also specify the queue a job should be sent to.

你可以指定任務應該要送到哪一個隊列。

By pushing jobs to different queues, you may "categorize" your queued jobs, and even prioritize how many workers you assign to various queues. This does not push jobs to different queue "connections" as defined by your queue configuration file, but only to specific queues within a single connection. To specify the queue, use the `onQueue` method on the job instance. The `onQueue` method is provided by the base `App\Jobs\Job` class included with Laravel:

要推送任務到不同的隊列上，你要將任務先分類，甚至可能要排定每個隊列能有多少 woker 可以執行任務。這並不是指任務會推送到你在設定檔所定義的不同隊列連結裡，而是推送到某個有單一連結的隊列。要指定任務執行的隊列，可以用任務實體的 `onQueue` 方法，這個方法是定義在 Laravel 內建的 `App\Jobs\Job` 類別裡：

    <?php

    namespace App\Http\Controllers;

    use App\User;
    use Illuminate\Http\Request;
    use App\Jobs\SendReminderEmail;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * Send a reminder e-mail to a given user.
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
### Delayed Jobs
### 延遲性任務

Sometimes you may wish to delay the execution of a queued job. For instance, you may wish to queue a job that sends a customer a reminder e-mail 15 minutes after sign-up. You may accomplish this using the `delay` method on your job class, which is provided by the `Illuminate\Bus\Queueable` trait:

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
         * Send a reminder e-mail to a given user.
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

In this example, we're specifying that the job should be delayed in the queue for 60 seconds before being made available to workers.

在這個範例裡，我們指定該任務要在交給 workers 執行前先延遲 60 秒。

> **Note:** The Amazon SQS service has a maximum delay time of 15 minutes.
> **註：** Amazon 的 SQS 服務最大延遲時間是 15 分鐘。

<a name="dispatching-jobs-from-requests"></a>
### Dispatching Jobs From Requests
### 從請求中派送任務

It is very common to map HTTP request variables into jobs. So, instead of forcing you to do this manually for each request, Laravel provides some helper methods to make it a cinch. Let's take a look at the `dispatchFrom` method available on the `DispatchesJobs` trait. By default, this trait is included on the base Laravel controller class:

在任務中對應到 HTTP 請求的變數是很常見的，所以與其強制你手動去對每個請求做這件事， Laravel 直接提供了一些輔助方法讓你更容易做到它；像是在 `DispatchesJobs` 這個 trait 就提供了 `dispatchFrom` 方法，而 Laravel 基礎控制器就預設引入了這個 trait ：

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use App\Http\Controllers\Controller;

    class CommerceController extends Controller
    {
        /**
         * Process the given order.
         *
         * @param  Request  $request
         * @param  int  $id
         * @return Response
         */
        public function processOrder(Request $request, $id)
        {
            // Process the request...

            $this->dispatchFrom('App\Jobs\ProcessOrder', $request);
        }
    }

This method will examine the constructor of the given job class and extract variables from the HTTP request (or any other `ArrayAccess` object) to fill the needed constructor parameters of the job. So, if our job class accepts a `productId` variable in its constructor, the job bus will attempt to pull the `productId` parameter from the HTTP request.

這個方法會檢查任務類別的建構子，並且從 HTTP 請求 (或任何 `ArrayAccess` 物件) 中取出變數，來填補建構子中需要的參數。所以如果我們的任務類別建構子接受一個 `productId` 變數的話，那麼隊列就會試著從 HTTP 請求中提出 `productId` 這個參數。

You may also pass an array as the third argument to the `dispatchFrom` method. This array will be used to fill any constructor parameters that are not available on the request:

你也可以直接將一個陣列傳入到 `dispatchFrom` 方法的第三個參數裡，這個陣列就會被用來填補建構子中任何不在請求裡的變數：

    $this->dispatchFrom('App\Jobs\ProcessOrder', $request, [
        'taxPercentage' => 20,
    ]);

<a name="running-the-queue-listener"></a>
## Running The Queue Listener
## 執行隊列監聽器

#### Starting The Queue Listener
#### 啟動隊列監聽器

Laravel includes an Artisan command that will run new jobs as they are pushed onto the queue. You may run the listener using the `queue:listen` command:

Laravel 引入了一個 Artisan 指令，用來執行被推送到隊列裡的任務。你可以透過 `queue:listen` 指令來執行監聽器：

    php artisan queue:listen

You may also specify which queue connection the listener should utilize:

你也可以指定監聽器應該利用哪一個隊列連結：

    php artisan queue:listen connection

Note that once this task has started, it will continue to run until it is manually stopped. You may use a process monitor such as [Supervisor](http://supervisord.org/) to ensure that the queue listener does not stop running.

要注意的是，一旦這個工作指令啟動後，它會持續運作直到它被手動停止。你可以利用像 [Supervisor](http://supervisord.org/) 這樣的行程監控軟體，來確保隊列監聽器不會停止執行。

#### Queue Priorities
#### 隊列優先序

You may pass a comma-delimited list of queue connections to the `listen` job to set queue priorities:

你可以給 `listen` 指令一個以逗號分隔的隊列連結列表，來設定隊列的優先序：

    php artisan queue:listen --queue=high,low

In this example, jobs on the `high` queue will always be processed before moving onto jobs from the `low` queue.

在這個範例裡，在 `high` 這個隊列裡的任務永遠會先被處理，然後才是 `low` 隊列裡的任務。

#### Specifying The Job Timeout Parameter

#### 指定任務的逾時參數

You may also set the length of time (in seconds) each job should be allowed to run:

你還可以設定每個任務所被允許執行的時間長度，單位是秒數：

    php artisan queue:listen --timeout=60

#### Specifying Queue Sleep Duration

#### 指定隊列的休眠期

In addition, you may specify the number of seconds to wait before polling for new jobs:

此外，你可以指定隊列要等幾秒再拿取新的任務來執行：

    php artisan queue:listen --sleep=5

Note that the queue only "sleeps" if no jobs are on the queue. If more jobs are available, the queue will continue to work them without sleeping.

注意這裡是指隊列在沒有任務的狀態下才會休眠；如果已經有多個任務卡在這個隊列上，那麼它會持續運作而不會休眠。

<a name="supervisor-configuration"></a>
### Supervisor Configuration

### Supervisor 設定

Supervisor is a process monitor for the Linux operating system, and will automatically restart your `queue:listen` or `queue:work` commands if they fail. To install Supervisor on Ubuntu, you may use the following command:

Supervisor 是一個在 Linux 作業系統上的行程監控軟體，它會在 `queue:listen` 或 `queue:work` 指令發生失敗後自動重啟它們。要在 Ubuntu 安裝 Supervisor ，可以用以下指令：

    sudo apt-get install supervisor

Supervisor configuration files are typically stored in the `/etc/supervisor/conf.d` directory. Within this directory, you may create any number of configuration files that instruct supervisor how your processes should be monitored. For example, let's create a `laravel-worker.conf` file that starts and monitors a `queue:work` process:

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

In this example, the `numprocs` directive will instruct Supervisor to run 8 `queue:work` processes and monitor all of them, automatically restarting them if they fail. Of course, you should change the `queue:work sqs` portion of the `command` directive to reflect your chosen queue driver.

Once the configuration file has been created, you may update the Supervisor configuration and start the processes using the following commands:

在這個範例裡的 `numprocs` 指令會要求 Supervisor 執行並監控 8 個 `queue:work` 行程，並且在它們執行失敗時重新啟動。當這個設定檔建立後，你需要更新 Supervisor 的設定，並用以下指令來啟動該行程：

    sudo supervisorctl reread

    sudo supervisorctl update

    sudo supervisorctl start laravel-worker:*

For more information on configuring and using Supervisor, consult the [Supervisor documentation](http://supervisord.org/index.html). Alternatively, you may use [Laravel Forge](https://forge.laravel.com) to automatically configure and manage your Supervisor configuration from a convenient web interface.

更多有關 Supervisor 的設定與使用，請參考 [Supervisor 官方文件](http://supervisord.org/index.html) 。或是你可以使用 [Laravel Forge](https://forge.laravel.com) 所提供的 Web 介面，來自動設定與管理你的 Supervisor 設定。

<a name="daemon-queue-listener"></a>
### Daemon Queue Listener
### 將任務監聽器設為背景服務

The `queue:work` Artisan command includes a `--daemon` option for forcing the queue worker to continue processing jobs without ever re-booting the framework. This results in a significant reduction of CPU usage when compared to the `queue:listen` command:

在 `queue:work` Artisan 指令裡包含了 `--daemon` 選項，強迫隊列 worker 持續處理任務，而不需要重新啟動整個 framework 。比起 `queue:listen` 指令，這會顯著減少 CPU 的用量。

To start a queue worker in daemon mode, use the `--daemon` flag:

用 `--daemon` 旗標在背景服務模式下啟動隊列 worker ：

    php artisan queue:work connection --daemon

    php artisan queue:work connection --daemon --sleep=3

    php artisan queue:work connection --daemon --sleep=3 --tries=3

As you can see, the `queue:work` job supports most of the same options available to `queue:listen`. You may use the `php artisan help queue:work` job to view all of the available options.

如你所見， `queue:work` 指令提供了多數和 `queue:listen` 指令相同的選項；你可以用 `php artisan help queue:work` 指令來查看所有可用的選項。

#### Coding Considerations For Daemon Queue Listeners

### 在背景服務的隊列監聽器中開發所要考量的事項

Daemon queue workers do not restart the framework before processing each job. Therefore, you should be careful to free any heavy resources before your job finishes. For example, if you are doing image manipulation with the GD library, you should free the memory with `imagedestroy` when you are done.

在背景執行的隊列監聽器在處理完每個任務前，不會重新啟動 framework ；因此你應該在任務執行完成前，謹慎地釋放任何佔用記憶體較重的資源。例如你利用 GD 函式庫處理影像，就要在結束前用 `imagedestroy` 來釋放記憶體。

Similarly, your database connection may disconnect when being used by a long-running daemon. You may use the `DB::reconnect` method to ensure you have a fresh connection.

相同地，你的資料庫連結也要在使用完後關閉連線；你可以用 `DB::reconnect` 方法來確保有新的資料庫連線。

<a name="deploying-with-daemon-queue-listeners"></a>
### Deploying With Daemon Queue Listeners

### 隨著在背景服務的任務監聽器進行佈署

Since daemon queue workers are long-lived processes, they will not pick up changes in your code without being restarted. So, the simplest way to deploy an application using daemon queue workers is to restart the workers during your deployment script. You may gracefully restart all of the workers by including the following command in your deployment script:

從背景服務的隊列 worker 是長時間執行的行程來看，除非重新啟動，否則它們將不會理會任何程式碼上的變更。所以要佈署一個有用到背景服務的隊列 worker 的應用程式，最簡單的方法就是在佈署指令稿中重新啟動 worker 。你可以在你的佈署指令裡加上以下指令，來優雅地重新啟動所有 worker ：

    php artisan queue:restart

This command will gracefully instruct all queue workers to restart after they finish processing their current job so that no existing jobs are lost.

這個指令會優雅地告知所有隊列 worker ，在它們完成處理目前任務後重新啟動，所以就不會任務遺失的問題。

> **Note:** This command relies on the cache system to schedule the restart. By default, APCu does not work for CLI jobs. If you are using APCu, add `apc.enable_cli=1` to your APCu configuration.

> **注意：**這個指令依靠快取系統來安排重新啟動；預設狀況下， APCu 無法在 CLI 的任務上運作；如果你正在使用 APCu 的話，要把 `apc.enable_cli=1` 加到你的 APCu 設定裡。

<a name="dealing-with-failed-jobs"></a>
## Dealing With Failed Jobs
## 處理失敗的任務

Since things don't always go as planned, sometimes your queued jobs will fail. Don't worry, it happens to the best of us! Laravel includes a convenient way to specify the maximum number of times a job should be attempted. After a job has exceeded this amount of attempts, it will be inserted into a `failed_jobs` table. The name of the failed jobs can be configured via the `config/queue.php` configuration file.

計劃永遠跟不上變化，有時候你的隊列任務就是會失敗。不過別擔心，我們有準備好它發生時的應付方法。 Laravel 有個便利的方式可以指定任務的最大重試次數，如果超過了這個重試次數，它就會被插入 `failed_jobs` 這個資料表。而失敗任務的名稱可以在 `config/queue.php` 這個設定檔中設定。

To create a migration for the `failed_jobs` table, you may use the `queue:failed-table` command:

要建立 `failed_jobs` 資料表的遷移類別，你可以用 `queue:failed-table` 指令：

    php artisan queue:failed-table

When running your [queue listener](#running-the-queue-listener), you may specify the maximum number of times a job should be attempted using the `--tries` switch on the `queue:listen` command:

當你執行[隊列監聽器](#running-the-queue-listener)時，你可以用 `queue:listen` 指令的 `--tries` 參數來指定任務的最大重試次數：

    php artisan queue:listen connection-name --tries=3

<a name="failed-job-events"></a>
### Failed Job Events
### 任務失敗事件

If you would like to register an event that will be called when a queued job fails, you may use the `Queue::failing` method. This event is a great opportunity to notify your team via e-mail or [HipChat](https://www.hipchat.com). For example, we may attach a callback to this event from the `AppServiceProvider` that is included with Laravel:

如果你想註冊一個當隊列任務失敗時會被呼叫的事件，你可以用 `Queue::failing` 方法；這樣你就有機會透過這個事件，用 e-mail 或 [HipChat](https://www.hipchat.com) 來通知你的團隊。例如我們可以在 Laravel 內建的 `AppServiceProvider` 中對這個事件附加一個回呼函式：

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
            Queue::failing(function ($connection, $job, $data) {
                // Notify team of failing job...
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

#### Failed Method On Job Classes

#### 任務類別裡處理失敗的方法

For more granular control, you may define a `failed` method directly on a queue job class, allowing you to perform job specific actions when a failure occurs:

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
         * Execute the job.
         *
         * @param  Mailer  $mailer
         * @return void
         */
        public function handle(Mailer $mailer)
        {
            //
        }

        /**
         * Handle a job failure.
         *
         * @return void
         */
        public function failed()
        {
            // Called when the job is failing...
        }
    }

<a name="retrying-failed-jobs"></a>
### Retrying Failed Jobs

### 重新嘗試執行失敗任務

To view all of your failed jobs that have been inserted into your `failed_jobs` database table, you may use the `queue:failed` Artisan command:

要檢視你在 `failed_jobs` 資料表中所有失敗的任務，你可以用 `queue:failed` 這個 Artisan 指令：

    php artisan queue:failed

The `queue:failed` command will list the job ID, connection, queue, and failure time. The job ID may be used to retry the failed job. For instance, to retry a failed job that has an ID of 5, the following command should be issued:

`queue:failed` 指令會列出所有任務編號、連結、隊列以及失敗時間，任務編號會用在重試失敗的任務。例如要重試一個編號為 5 的失敗任務，其指令如下：

    php artisan queue:retry 5

If you would like to delete a failed job, you may use the `queue:forget` command:

如果你想刪除掉一個失敗任務，可以用 `queue:forget` 指令：

    php artisan queue:forget 5

To delete all of your failed jobs, you may use the `queue:flush` command:

`queue:flush` 指令可以讓你刪除所有失敗的任務：

    php artisan queue:flush
