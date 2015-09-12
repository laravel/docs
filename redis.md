# Redis

- [簡介](#introduction)
- [基本用法](#basic-usage)
    - [管線化指令](#pipelining-commands)
- [發佈與訂閱](#pubsub)

<a name="introduction"></a>
## 簡介

[Redis](http://redis.io) 是開源且先進的鍵值對儲存庫。由於它可用的鍵包含了[字串](http://redis.io/topics/data-types#strings)、[雜湊](http://redis.io/topics/data-types#hashes)、[列表](http://redis.io/topics/data-types#lists)、[集合](http://redis.io/topics/data-types#sets)和[有序集合](http://redis.io/topics/data-types#sorted-sets)，因此常被稱作資料結構伺服器。在 Laravel 使用 Redis 之前，你必須透過 Composer 安裝 `predis/predis` 套件（~1.0）。

<a name="configuration"></a>
### 設定

應用程式的 Redis 設定都在 `config/database.php` 設定檔中。在這個檔案裡，你會看到 `redis` 陣列，裡面有包含了應用程式使用的 Redis 伺服器：

    'redis' => [

        'cluster' => false,

        'default' => [
            'host'     => '127.0.0.1',
            'port'     => 6379,
            'database' => 0,
        ],

    ],

預設的伺服器設定對於開發應該是足夠的。然而，你可以根據使用環境自由修改陣列。只要給每個 Redis 一個名稱，並且指定伺服器使用的的 host 和 port。

`cluster` 選項會讓 Laravel 的 Redis 客戶端在所有 Redis 節點間執行客戶端分片（client-side sharding），讓你建立節點池，並因此擁有大量的可用記憶體。但是請注意，客戶端分片的節點不能執行容錯轉移；因此，此選項主要適用於可從另一台主要資料儲存庫取得的快取資料。

此外，你可以在你的 Redis 連線中定義一個 `options` 陣列值，讓你指定一套 Predis 的[客戶端選項](https://github.com/nrk/predis/wiki/Client-Options)。

如果你的 Redis 伺服器需要認證，你可以在 Redis 伺服器的設定陣列裡加入 `password` 設定項目作為提供的密碼。

> **注意：**如果你是透過 PECL 安裝 Redis PHP extension，則需要重新命名 `config/app.php` 檔案裡的 Redis 別名。

<a name="basic-usage"></a>
## 基本用法

你可以透過呼叫 `Redis` [facade](/docs/{{version}}/facades) 的各種方法與 Redis 進行互動。`Redis` facade 支援動態方法，意思就是指你可以在該 facade 呼叫任何 [Redis 指令](http://redis.io/commands)，該指令會直接傳遞給 Redis。在本例中，我們會透過 `Redis` facade 的 `get` 方法來呼叫 Redis 的 `GET` 指令：

    <?php

    namespace App\Http\Controllers;

    use Redis;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * 顯示給定使用者的個人資料。
         *
         * @param  int  $id
         * @return Response
         */
        public function showProfile($id)
        {
            $user = Redis::get('user:profile:'.$id);

            return view('user.profile', ['user' => $user]);
        }
    }

當然，如上所述，你可以在 `Redis` facade 呼叫任何的 Redis 指令。Laravel 使用魔術方法來傳遞指令至 Redis 伺服器，所以可以簡單的傳遞 Redis 指令所需要的參數：

    Redis::set('name', 'Taylor');

    $values = Redis::lrange('names', 5, 10);

另外，你也可以透過 `command` 方法傳遞指令至伺服器，它接受指令的名稱作為第一個參數，第二個參數則為值的陣列：

    $values = Redis::command('lrange', ['name', 5, 10]);

#### 使用多個 Redis 連結

你可以經由 `Redis::connection` 方法得到 Redis 實例：

    $redis = Redis::connection();

你會得到一個 Redis 預設伺服器的實例。如果你沒有使用伺服器叢集，你可以在 `connection` 方法傳入定義在 Redis 設定檔的伺服器名稱，以取得特定伺服器：

    $redis = Redis::connection('other');

<a name="pipelining-commands"></a>
### 管線化指令

當你想要在單次操作中發送多個指令至伺服器時可以使用管線化。`pipeline` 方法接受一個參數：接收 Redis 實例的`閉包`。你可以發送所有的指令至此 Redis 實例，它們都會在單次操作中執行：

    Redis::pipeline(function ($pipe) {
        for ($i = 0; $i < 1000; $i++) {
            $pipe->set("key:$i", $i);
        }
    });

<a name="pubsub"></a>
## 發佈與訂閱

Laravel 也對 Redis 的 `publish` 及 `subscribe` 提供了方便的介面。這些 Redis 指令讓你可以監聽給定「頻道」的訊息。你可以從另一個應用程式發佈訊息至頻道，甚至使用另一種程式語言，讓應用程式或程序之間容易溝通。

首先，讓我們透過 `Redis` 使用 `subscribe` 方法在一個頻道設定監聽器。我們會將方法呼叫放置於一個 [Artisan 指令](/docs/{{version}}/artisan)中，因為呼叫 `subscribe` 方法會啟動一個長時間執行的程序：

    <?php

    namespace App\Console\Commands;

    use Redis;
    use Illuminate\Console\Command;

    class RedisSubscribe extends Command
    {
        /**
         * 主控台指令的識別名稱。
         *
         * @var string
         */
        protected $signature = 'redis:subscribe';

        /**
         * 主控台指令描述。
         *
         * @var string
         */
        protected $description = 'Subscribe to a Redis channel';

        /**
         * 執行主控台指令。
         *
         * @return mixed
         */
        public function handle()
        {
            Redis::subscribe(['test-channel'], function($message) {
                echo $message;
            });
        }
    }

現在，我們可以透過 `publish` 方法發佈訊息至該頻道：

    Route::get('publish', function () {
        // 路由邏輯...

        Redis::publish('test-channel', json_encode(['foo' => 'bar']));
    });

#### 萬用字元訂閱

你可以使用 `psubscribe` 方法訂閱一個萬用字元頻道，這在要在所有頻道獲取所有訊息時相當有用。`$channel` 名稱會被傳遞至該方法提供的回呼`閉包`的第二個參數：

    Redis::psubscribe(['*'], function($message, $channel) {
        echo $message;
    });

    Redis::psubscribe(['users.*'], function($message, $channel) {
        echo $message;
    });
