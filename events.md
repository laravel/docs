# 事件

- [簡介](#introduction)
- [註冊事件或監聽器](#registering-events-and-listeners)
- [定義事件](#defining-events)
- [定義監聽器](#defining-listeners)
    - [隊列事件的監聽器](#queued-event-listeners)
- [觸發事件](#firing-events)
- [廣播事件](#broadcasting-events)
    - [設定](#broadcast-configuration)
    - [將事件標記為廣播](#marking-events-for-broadcast)
    - [廣播資料](#broadcast-data)
    - [消耗事件廣播](#consuming-event-broadcasts)
- [事件訂閱器](#event-subscribers)

<a name="introduction"></a>
## 簡介

Laravel 事件提供了一個簡單的監聽器實作，允許你在應用程式可以訂閱和監聽事件。事件類別通常被儲存在 `app/Events` 目錄下，而它們的監聽器儲存在 `app/Listeners` 目錄下。

<a name="registering-events-and-listeners"></a>
## 註冊事件或監聽器

Laravel 應用程式包含了 `EventServiceProvider` 提供一個方便的位置來註冊所有的事件監聽器。`listen` 屬性包含一個所有事件（鍵）以及他們的監聽器（值）的陣列。當然，你也可以在應用程式根據需求增加許多事件到這個陣列。例如：讓我們增加 `PodcastWasPurchased` 事件：

    /**
     * 應用程式的事件監聽器對映。
     *
     * @var array
     */
    protected $listen = [
        'App\Events\PodcastWasPurchased' => [
            'App\Listeners\EmailPurchaseConfirmation',
        ],
    ];

### 產生事件或監聽器類別

當然，手動建立每個事件以及監聽器檔案是相當麻煩的。相反的，只要增加監聽器和事件到你的 `EventServiceProvider` 以及使用 `event:generate` 指令即可。這個指令會產生所有列出在 `EventServiceProvider` 的事件和監聽器。當然，已經存在的事件和監聽器將保持不變：

    php artisan event:generate

<a name="defining-events"></a>
## 定義事件

一個事件類別只是一個資料容器包含了相關的事件資訊。例如，假設我們產生了 `PodcastWasPurchased` 事件來接收一個 [Eloquent ORM](/docs/{{version}}/eloquent) 物件：

    <?php

    namespace App\Events;

    use App\Podcast;
    use App\Events\Event;
    use Illuminate\Queue\SerializesModels;

    class PodcastWasPurchased extends Event
    {
        use SerializesModels;

        public $podcast;

        /**
         * 建立一個新的事件實例。
         *
         * @param  Podcast  $podcast
         * @return void
         */
        public function __construct(Podcast $podcast)
        {
            $this->podcast = $podcast;
        }
    }

正如你所見的，這個事件類別沒有包含特別的邏輯。它只是一個當 `Podcast` 物件被購買時的容器。如果事件物件是使用 PHP 的 `serialized` 函式進行序列化，那麼事件所使用的 `SerializesModels` trait 將會優雅的序列化任何的 Eloquent 模型。

<a name="defining-listeners"></a>
## 定義監聽器

接下來，讓我們看一下範例事件的監聽器。事件監聽器的 `handle` 方法接收了事件實例。`event:generate` 指令將會在事件的 `handle` 方法自動載入正確的事件類別和類型提示。在 `handle` 方法內，你可以執行任何必要回應該事件的邏輯。

    <?php

    namespace App\Listeners;

    use App\Events\PodcastWasPurchased;
    use Illuminate\Queue\InteractsWithQueue;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class EmailPurchaseConfirmation
    {
        /**
         * 建立事件監聽器。
         *
         * @return void
         */
        public function __construct()
        {
            //
        }

        /**
         * 處理事件。
         *
         * @param  PodcastWasPurchased  $event
         * @return void
         */
        public function handle(PodcastWasPurchased $event)
        {
            // 使用 $event->podcast 存取播客（podcast）...
        }
    }

你的事件監聽器也可以在建構子內對任何依賴使用型別提示。所有事件監聽器經由 Laravel [服務容器](/docs/{{version}}/container)做解析，所以依賴將會自動的被注入：

    use Illuminate\Contracts\Mail\Mailer;

    public function __construct(Mailer $mailer)
    {
        $this->mailer = $mailer;
    }

#### 停止一個事件的傳播

有時候，你可能希望停止一個事件的傳播到其他的監聽器。你可以在監聽器的 `handle` 方法回傳 `false` 達到這項目的。

<a name="queued-event-listeners"></a>
### 隊列事件的監聽器

需要一個[隊列](/docs/{{version}}/queues)事件監聽器嗎？它是再容易不過了。只要增加 `ShouldQueue` 介面到你的監聽器類別。由 `event:generate` Artisan 指令產生的監聽器已經將目前存在的介面載入到命名空間，所以你可以立即的使用它：

    <?php

    namespace App\Listeners;

    use App\Events\PodcastWasPurchased;
    use Illuminate\Queue\InteractsWithQueue;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class EmailPurchaseConfirmation implements ShouldQueue
    {
        //
    }

如此而已！現在，當這個監聽器呼叫事件時，事件發送器會使用 Laravel 的[隊列系統](/docs/{{version}}/queues)自動的進行隊列。如果監聽器是透過隊列執行而沒有拋出任何異常，已處理的隊列任務將自動的被刪除。

#### 手動存取隊列

如果你需要手動存取底層隊列任務的 `delete` 和 `release` 方法，你可以這麼做。在預設產生的監聽器會載入 `Illuminate\Queue\InteractsWithQueue` trait，讓你可以存取這些方法：

    <?php

    namespace App\Listeners;

    use App\Events\PodcastWasPurchased;
    use Illuminate\Queue\InteractsWithQueue;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class EmailPurchaseConfirmation implements ShouldQueue
    {
        use InteractsWithQueue;

        public function handle(PodcastWasPurchased $event)
        {
            if (true) {
                $this->release(30);
            }
        }
    }

<a name="firing-events"></a>
## 觸發事件

如果要觸發一件事件，你可以使用 `Event` [facade](/docs/{{version}}/facades)，傳送一個事件的實例到 `fire` 方法。`fire` 方法將會發送事件到所有已經註冊的監聽器：

    <?php

    namespace App\Http\Controllers;

    use Event;
    use App\Podcast;
    use App\Events\PodcastWasPurchased;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * 顯示給定使用者的基本資料
         *
         * @param  int  $userId
         * @param  int  $podcastId
         * @return Response
         */
        public function purchasePodcast($userId, $podcastId)
        {
            $podcast = Podcast::findOrFail($podcastId);

            // 購買播客（podcast）邏輯...

            Event::fire(new PodcastWasPurchased($podcast));
        }
    }

另外，你也可以使用全域 `event` 輔助函式來觸發事件：

    event(new PodcastWasPurchased($podcast));

<a name="broadcasting-events"></a>
## 廣播事件

在許多現代的 web 應用程式，web sockets 都用在實現即時，即時更新使用者介面。當在伺服器上更新一些資料，websocket 連線通常傳送一個訊息透過客戶端處理。

為了協助你建立這些類型的應用程式，Laravel 讓你可以簡單的經由 websocket 連線來「廣播」你的事件。廣播你的 Laravel 事件讓你能夠在你的伺服器端程式碼和你的客戶端 JavaScript 框架間分享相同的事件名稱。

<a name="broadcast-configuration"></a>
### 設定

所有的事件廣播設定選項都儲存在 `config/broadcasting.php` 設定檔內。Laravel 內建支援多種廣播驅動：[Pusher](https://pusher.com)、[Redis](/docs/{{version}}/redis)，和一個用於本機開發和除錯的 `log` 驅動程式。設定檔範例包含了每個驅動程式。

#### 廣播先決條件

事件廣播需要以下的依賴：

- Pusher: `pusher/pusher-php-server ~2.0`
- Redis: `predis/predis ~1.0`

#### 隊列先決條件

在廣播事件之前，你還需要設定和執行[隊列監聽器](/docs/{{version}}/queues)。所有事件廣播經由隊列任務完成，因此你的應用程式回應時間不會有嚴重影響。

<a name="marking-events-for-broadcast"></a>
### 將事件標記為廣播

為了通知 Laravel 應該廣播一個特定事件，在你的事件類別實作 `Illuminate\Contracts\Broadcasting\ShouldBroadcast`。`ShouldBroadcast` 要求你實作單一方法：`broadcastOn`。`broadcastOn` 方法應該回傳一個必須被廣播的「頻道」名稱陣列：

    <?php

    namespace App\Events;

    use App\User;
    use App\Events\Event;
    use Illuminate\Queue\SerializesModels;
    use Illuminate\Contracts\Broadcasting\ShouldBroadcast;

    class ServerCreated extends Event implements ShouldBroadcast
    {
        use SerializesModels;

        public $user;

        /**
         * 建立一個新的事件實例。
         *
         * @return void
         */
        public function __construct(User $user)
        {
            $this->user = $user;
        }

        /**
         * 取得事件應該被廣播的頻道。
         *
         * @return array
         */
        public function broadcastOn()
        {
            return ['user.'.$this->user->id];
        }
    }

接著，你只需要像往常的[觸發事件](#firing-events)。一旦事件被觸發之後，[隊列任務](/docs/{{version}}/queues)將會自動的廣播事件到你指定的廣播驅動。

<a name="broadcast-data"></a>
### 廣播資料

當事件被廣播時，所有的 `public` 屬性都自動的被序列化和廣播作為事件的有效資料，允許你可以從你的 JavaScript 應用程式中存取任何公開的資料。所以，在這個範例中，假設事件有一個單一公開的 `$user` 屬性且包含了一個 Eloquent 模型，廣播資料將會是：

    {
        "user": {
            "id": 1,
            "name": "Jonathan Banks"
            ...
        }
    }

然而，如果你希望有更多精確的控制在你的廣播資料，你可以增加 `broadcastWith` 方法到你的事件。這個方法應該回傳一個你希望廣播的事件資料陣列：

    /**
     * 取得廣播資料。
     *
     * @return array
     */
    public function broadcastWith()
    {
        return ['user' => $this->user->id];
    }

<a name="consuming-event-broadcasts"></a>
### 消耗事件廣播

#### Pusher

透過 [Pusher](https://pusher.com) 驅動，你可以使用 Pusher 的 JavaScript SDK 方便的消耗事件廣播。例如，讓我們從先前的範例消耗 `App\Events\ServerCreated` 事件：

    this.pusher = new Pusher('pusher-key');

    this.pusherChannel = this.pusher.subscribe('user.' + USER_ID);

    this.pusherChannel.bind('App\\Events\\ServerCreated', function(message) {
        console.log(message.user);
    });

#### Redis

如果你使用 Redis 廣播器，你需要撰寫自己的 Redis pub/sub 消耗器來接收訊息和廣播，並使用你選擇的 websocket 技術。例如，你可能選擇使用 Node 撰寫，很受歡迎的 [Socket.io](http://socket.io) 函式庫。

使用 `socket.io` 和 `ioredis` Node 函式庫，你可以快速的撰寫一個事件廣播器，在你的 Laravel 應用程式發布所有事件的廣播：

    var app = require('http').createServer(handler);
    var io = require('socket.io')(app);

    var Redis = require('ioredis');
    var redis = new Redis();

    app.listen(6001, function() {
        console.log('Server is running!');
    });

    function handler(req, res) {
        res.writeHead(200);
        res.end('');
    }

    io.on('connection', function(socket) {
        //
    });

    redis.psubscribe('*', function(err, count) {
        //
    });

    redis.on('pmessage', function(subscribed, channel, message) {
        message = JSON.parse(message);
        io.emit(channel + ':' + message.event, message.data);
    });

<a name="event-subscribers"></a>
## 事件訂閱器

事件訂閱器是一個類別，讓你可以在該類別內訂閱多個事件，允許你從單一類別內定義多個事件的操作。訂閱器應該定義一個 `subscribe` 方法，可以傳送一個事件發送器實例：

    <?php

    namespace App\Listeners;

    class UserEventListener
    {
        /**
         * 處理使用者登入事件。
         */
        public function onUserLogin($event) {}

        /**
         * 處理使用者登出事件。
         */
        public function onUserLogout($event) {}

        /**
         * 註冊監聽器的訂閱者。
         *
         * @param  Illuminate\Events\Dispatcher  $events
         * @return array
         */
        public function subscribe($events)
        {
            $events->listen(
                'App\Events\UserLoggedIn',
                'App\Listeners\UserEventListener@onUserLogin'
            );

            $events->listen(
                'App\Events\UserLoggedOut',
                'App\Listeners\UserEventListener@onUserLogout'
            );
        }

    }

#### 註冊事件訂閱器

一旦訂閱器被定義，它可以被註冊到事件發送器。你可以在 `EventServiceProvider` 中使用 `$subscribe` 屬性註冊訂閱器。例如，讓我們增加 `UserEventListener`。

    <?php

    namespace App\Providers;

    use Illuminate\Contracts\Events\Dispatcher as DispatcherContract;
    use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

    class EventServiceProvider extends ServiceProvider
    {
        /**
         * 事件監聽器對映到應用程式。
         *
         * @var array
         */
        protected $listen = [
            //
        ];

        /**
         * 訂閱者類別進行註冊。
         *
         * @var array
         */
        protected $subscribe = [
            'App\Listeners\UserEventListener',
        ];
    }
