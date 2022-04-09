# 快取

- [介紹](#introduction)
- [設定](#configuration)
    - [快取預先需求](#driver-prerequisites)
- [快取的使用](#cache-usage)
    - [取得一個快取的實例](#obtaining-a-cache-instance)
    - [從快取中取得項目](#retrieving-items-from-the-cache)
    - [存放項目到快取中](#storing-items-in-the-cache)
    - [刪除快取中的項目](#removing-items-from-the-cache)
    - [快取輔助函式](#the-cache-helper)
- [快取標籤](#cache-tags)
    - [寫入被標記的快取項目](#storing-tagged-cache-items)
    - [取得被標記的快取項目](#accessing-tagged-cache-items)
    - [刪除被標記的快取項目](#removing-tagged-cache-items)
- [原子鎖](#atomic-locks)
    - [驅動程式的先決條件](#lock-driver-prerequisites)
    - [管理鎖](#managing-locks)
    - [在不同進程內管理鎖](#managing-locks-across-processes)
- [加入客製化的快取驅動](#adding-custom-cache-drivers)
    - [撰寫一個驅動](#writing-the-driver)
    - [註冊快取驅動](#registering-the-driver)
- [快取事件](#events)

<a name="introduction"></a>
## 介紹

在應用內所執行的某些資料存取或任務處理，可能會佔用大量 CPU 資源，或需要幾秒鐘才能完成。這種情況下，通常會將存取的資料快取一段時間，以便在之後請求相同資料時能快速存取。快取的資料通常儲存在非常快的資料儲存方式內，例如 [Memcached](https://memcached.org) 或 [Redis](https://redis.io)。

幸好，Laravel 提供了一個表達性強、統一的 API 方法給各式各樣的快取後端，讓你可以利用快取極快的資料存取速度，使網頁應用的效能更加提升。

<a name="configuration"></a>
## 設定

Laravel 提供一個快速、統一的 API 方法給各式各樣不同的快取驅動。這些設定放置在 `config/cache.php` 當中。在這個設定檔裡面，可以自由指定你想要用哪一個來當作你應用程式的預設快取伺服器。Laravel 支援許多熱門的快取驅動，像是 [Memcached](https://memcached.org) 、 [Redis](http://redis.io) 和 [DynamoDB](https://aws.amazon.com/dynamodb)，以及其他更多的選擇。另外，可以使用基於檔案的快取驅動方式，而 `array` 和 "null"  快取驅動可以為您的自動化測試提供方便的快取後端。

這個快取的設定檔同時也包含了其他的選項，請確保你都有讀過這些選項的說明。Laravel 使用 `file` 作為預設快取的驅動。這個驅動儲存了序列化的快取物件在檔案系統中。建議你為大型的應用程式選用一套強勁的快取驅動，像是 Memcached 或是 Redis 等等。你可能也會想為同一個驅動設定多個設定檔。

<a name="driver-prerequisites"></a>
### 快取預先需求

<a name="prerequisites-database"></a>
#### 資料庫

當使用 `database` 這個快取驅動，你需要設置一個資料表來放置快取的內容，你可以看一下範例 `Schema` 如何宣告這樣的資料表：

    Schema::create('cache', function ($table) {
        $table->string('key')->unique();
        $table->text('value');
        $table->integer('expiration');
    });

> {tip} 你可以使用 `php artisan cache:table` 這個 Artisan 指令來產生一個較合適的資料庫遷移結構。

<a name="memcached"></a>
#### Memcached

使用 Memcached 驅動需要先安裝 [Memcached PECL 套件](https://pecl.php.net/package/memcached)。 你可以在 `config/cache.php` 設定檔中列出你所有的 Memcached 伺服器。該檔案已經預先包含了 `memcached.servers` 來協助你開始撰寫：

    'memcached' => [
        'servers' => [
            [
                'host' => env('MEMCACHED_HOST', '127.0.0.1'),
                'port' => env('MEMCACHED_PORT', 11211),
                'weight' => 100,
            ],
        ],
    ],

你可能也會設置 `host` 選項到 UNIX 的 socket 路徑中，如果你有這麼做，記得 `port` 選項要設為 `0`：

    'memcached' => [
        [
            'host' => '/var/run/memcached/memcached.sock',
            'port' => 0,
            'weight' => 100
        ],
    ],

<a name="redis"></a>
#### Redis

在選擇使用 Redis 作為 Laravel 的快取前，你需要先經由 Composer 安裝 `predis/predis` 套件（~1.0），或是經由 PECL 安裝 PhpRedis 擴充功能。

 [Laravel Sail](/docs/{{version}}/sail) 已經包含這個擴充。另外，在官方的 Laravel 部署平台上，像是 [Laravel Forge](https://forge.laravel.com) 和 [Laravel Vapor](https://vapor.laravel.com) 已經預設安裝了 PhpRedis 擴充。

更多有關設定 Redis 的資訊，請參考 [Laravel 的文件頁面](/docs/{{version}}/redis#configuration)。

<a name="dynamodb"></a>
#### DynamoDB

在使用 [DynamoDB](https://aws.amazon.com/dynamodb) 快取驅動之前，您必須創建一個 DynamoDB 資料表來儲存所有快取的內容。通常，此表會以 `cache` 命名。不過，您可以根據應用內 `cache` 文件中 `stores.dynamodb.table` 的值來設定該資料表的名稱。

該資料表還應該有一個型態為字串的分區鍵，其名稱對應於應用程序 `cache`  文件中 `stores.dynamodb.attributes.key`的值。預設情況下，分區鍵應命名為 `key`。

<a name="cache-usage"></a>
## 快取的使用

<a name="obtaining-a-cache-instance"></a>
### 取得一個快取的實例

要取得快取實例，您可以使用 `Cache` facade，在這份文件裡，我們都會使用該 facade。 `Cache` facade 能方便、簡潔的存取  Laravel 快取合約的底層實作：

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Support\Facades\Cache;

    class UserController extends Controller
    {
        /**
         * Show a list of all users of the application.
         *
         * @return Response
         */
        public function index()
        {
            $value = Cache::get('key');

            //
        }
    }

<a name="accessing-multiple-cache-stores"></a>
#### 存取多個快取儲存

使用 `Cache` facade，你可能會透過 `store` 存取多個快取儲存。被傳送到 `store` 的鍵，應該會對應到你的 `cache` 設定檔中的 `stores` 設定陣列的其中一項：

    $value = Cache::store('file')->get('foo');

    Cache::store('redis')->put('bar', 'baz', 600); // 10 分鐘

<a name="retrieving-items-from-the-cache"></a>
### 從快取中取得項目

在 `Cache` facade 中，`get` 方法可以用來取得快取中的項目。如果快取中沒有這個項目，那麼將會回傳 `null`。如果你希望的話，也可以傳遞第二個參數給 `get` 方法來指定找不到項目時的預設回傳值：

    $value = Cache::get('key');

    $value = Cache::get('key', 'default');

你甚至可以傳入一個`閉包`作為預設值，當指定的項目不存在快取中時，閉包將會被回傳。傳入一個閉包讓你可以延後存取資料庫，或從外部服務中取出資料作為找不到快取時的預設值：

    $value = Cache::get('key', function () {
        return DB::table(...)->get();
    });

<a name="checking-for-item-existence"></a>
#### 確認項目存在

`has` 方法可以用來檢查一個項目是否存在於快取中。如果項目的值是 `null` 或是 `false`，那麼將會回傳 `false`：

    if (Cache::has('key')) {
        //
    }

<a name="incrementing-decrementing-values"></a>
#### 遞增或遞減值

`increment` 和 `decrement` 方法都可以用來調整快取中的整數項目值，這兩個方法都可以選擇性的傳入第二個參數，用來指示要遞增或遞減多少：

    Cache::increment('key');
    Cache::increment('key', $amount);
    Cache::decrement('key');
    Cache::decrement('key', $amount);

<a name="retrieve-store"></a>
#### 取出或更新

有時候，你可能會想從快取中取出一個項目，但也想在取出的項目不存在時存入一個預設值。例如，你可能會想從快取中取出所有使用者，或者當找不到使用者時，從資料庫中將這些使用者取出並放入快取中。你可以透過使用 `Cache::remember` 方法：

    $value = Cache::remember('users', $seconds, function () {
        return DB::table('users')->get();
    });

如果那個項目不存在快取中，則傳遞給 `remember` 方法的`閉包`將會被執行，而且閉包的執行結果將會被存放在快取中。

你也可以使用 `rememberForever` 方法去取得快取中的項目，並且將這個項目永遠的儲存：

    $value = Cache::rememberForever('users', function () {
        return DB::table('users')->get();
    });

<a name="retrieve-delete"></a>
#### 取出與刪除

如果你需要從快取中取出一個項目並刪除它，你可以使用 `pull` 方法。與 `get` 相似，如果物件不存在快取中，`pull` 方法將會回傳 `null`：

    $value = Cache::pull('key');

<a name="storing-items-in-the-cache"></a>
### 存放項目到快取中

你可能會在 `Cache` facade 中使用 `put` 方法來存放項目到快取中。當你將一個項目放進快取時，你需要指定「幾秒鐘」給將要存放的值：

    Cache::put('key', 'value', $seconds = 10);

如果你沒有指定存放的時間，物件將會被永久存放：

    Cache::put('key', 'value');

如果不指定過期的秒數，你也可以傳遞一個 PHP 的 `DateTime` 實例，來表示該快取項目過期的時間點：

    Cache::put('key', 'value', now()->addMinutes(10));

<a name="store-if-not-present"></a>
#### 項目不存在時才新增

`add` 方法只會把還不存在快取中的項目放入快取。如果成功存放到快取，會回傳 `true`，否回傳 `false`，`add` 方法是一種原子操作（atomic operation）：

    Cache::add('key', 'value', $seconds);

<a name="storing-items-forever"></a>
#### 永久地儲存項目

`forever` 方法可以用來存放永久的項目到快取中。但是因為這些項目並不會過期，所以必須被手動刪除，這可以透過 `forget` 方法達成：

    Cache::forever('key', 'value');

> {tip} 如果你是使用 Memcached 驅動，永久儲存的項目會在到達大小限制時被刪除。

<a name="removing-items-from-the-cache"></a>
### 刪除快取中的項目

你可能會使用 `forget` 方法移除在快取中的一個項目。

    Cache::forget('key');

你也可以通過輸入零或負數的過期秒數來刪除項目：

    Cache::put('key', 'value', -5);

你也可以使用 `flush` 方法來清除所有項目：

    Cache::flush();

> {note} 在清除所有快取時，將會直接清除快取中的所有項目，與你設定的任何前輟字串都沒有關係。如果你有與其他應用程式共用快取中的項目，請特別注意到這點。

<a name="the-cache-helper"></a>
### 快取輔助函式

除了使用 `Cache` facade ，你還可以使用全域的 `cache` 函式來從快取中取得或是儲存資料。當 `cache` 函式被呼叫並且只有一個字串的參數時，將會傳回快取中這個項目的值：

    $value = cache('key');

如果你對這個函式提供了一組鍵和值的陣列以及過期的秒數，則會把這個項目存進快取中，並設定為你指定的到期時間：

    cache(['key' => 'value'], $seconds);

    cache(['key' => 'value'], now()->addMinutes(10));

當不帶任何參數呼叫 `cache` 函數時，它會返回實現`Illuminate\Contracts\Cache\Factory` 的實例，允許您調用其他快取方法：

    cache()->remember('users', $seconds, function () {
        return DB::table('users')->get();
    });

> {tip} 當你在測試中呼叫這個全域的 `cache` 輔助函式，你可以使用 `Cache::shouldReceive` 方法就像你在[測試一個 facade](/docs/{{version}}/mocking#mocking-facades) 一樣。

<a name="cache-tags"></a>
## 快取標籤

> {note} 快取標籤並不支援 `file`、`dynamodb`及 `database` 驅動。此外，當使用多個標籤以及將快取儲存成「永久」時，使用像是 memcached 這樣性能較好的驅動，可以自動清除舊的歷史記錄。

<a name="storing-tagged-cache-items"></a>
### 寫入被標記的快取項目

快取標籤允許你在快取中標記關聯的項目，並清空所有已分配指定標籤的快取值。你可以透過傳遞一組標籤名稱的有序陣列，以存取被標記的快取。舉例來說，讓我們存取一個被標記的快取並 `put` 值給它：

    Cache::tags(['people', 'artists'])->put('John', $john, $seconds);

    Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);

<a name="accessing-tagged-cache-items"></a>
### 取得被標記的快取項目

若要取得一個被標記的快取項目，只要傳遞一樣的標籤有序列表至 `tags` 方法，然後傳遞你想取得的項目給 `get` 方法：

    $john = Cache::tags(['people', 'artists'])->get('John');

    $anne = Cache::tags(['people', 'authors'])->get('Anne');

<a name="removing-tagged-cache-items"></a>
### 刪除被標記的快取項目

你可以清空已分配單一標籤或是一組標籤列表中的所有項目。例如，下方的語法會將被標記 `people`、`authors`，或兩者的快取給移除。所以，`Anne` 與 `John` 都從快取中被移除：

    Cache::tags(['people', 'authors'])->flush();

相反的，下方的語法只會刪除被標記為 `authors` 的快取，所以 `Anne` 會被移除，但 `John` 不會：

    Cache::tags('authors')->flush();

<a name="atomic-locks"></a>
## 原子鎖

> {note} 要使用此功能，你的應用必須使用 `memcached`、`redis`、`dynamodb`、`database`、`file` 或 `array` 快取驅動作為應用的預設快取驅動。此外，所有伺服器都必須與同一個中央快取伺服器進行溝通。

<a name="lock-driver-prerequisites"></a>
### 驅動程式的先決條件

<a name="atomic-locks-prerequisites-database"></a>
#### 資料庫

使用 `database` 快取驅動時，您需要設置一個資料表來包含應用程序的快取鎖。你將在下表中找到一個 `Schema` 宣告的範例：

    Schema::create('cache_locks', function ($table) {
        $table->string('key')->primary();
        $table->string('owner');
        $table->integer('expiration');
    });

<a name="managing-locks"></a>
### 管理鎖
原子鎖允許操作分佈式鎖而不用擔心競爭條件。例如，[Laravel Forge](https://forge.laravel.com) 使用原子鎖來確保伺服器上一次只執行一個遠程任務。您可以使用 `Cache::lock` 方法建立和管理原子鎖：

    use Illuminate\Support\Facades\Cache;

    $lock = Cache::lock('foo', 10);

    if ($lock->get()) {
        // Lock acquired for 10 seconds...

        $lock->release();
    }

`get` 方法也接受閉包。閉包執行後，Laravel 會自動釋放鎖：

    Cache::lock('foo')->get(function () {
        // Lock acquired indefinitely and automatically released...
    });

  
如果在您請求時鎖不可用，您可以指示 Laravel 等待指定的秒數。如果在指定的時間限制內無法取得鎖，則會拋出 `Illuminate\Contracts\Cache\LockTimeoutException`：

    use Illuminate\Contracts\Cache\LockTimeoutException;

    $lock = Cache::lock('foo', 10);

    try {
        $lock->block(5);

        // Lock acquired after waiting a maximum of 5 seconds...
    } catch (LockTimeoutException $e) {
        // Unable to acquire lock...
    } finally {
        optional($lock)->release();
    }

上面的例子可以通過將閉包傳遞給 `block` 方法來簡化。當一個閉包被傳遞給這個方法時，Laravel 將嘗試在指定的秒數內取得鎖，並在閉包執行後自動釋放鎖：

    Cache::lock('foo', 10)->block(5, function () {
        // Lock acquired after waiting a maximum of 5 seconds...
    });

<a name="managing-locks-across-processes"></a>
### 在不同進程內管理鎖

有時，你可能希望在一個進程中獲取鎖並在另一個進程中釋放。例如，你可能在網頁請求期間獲取鎖，並希望在由該請求觸發的佇列作業結束時釋放鎖。在這種情況下，您應該將鎖作用域內的「所有者令牌」傳遞給佇列的作業，以便作業可以使用給定的令牌重新實例化鎖。

在下面的範例中，如果成功取得鎖，我們將調度一個佇列的作業。此外，我們將通過鎖的 `owner` 方法將鎖的所有者令牌傳遞給佇列的作業：

    $podcast = Podcast::find($id);

    $lock = Cache::lock('processing', 120);

    if ($lock->get()) {
        ProcessPodcast::dispatch($podcast, $lock->owner());
    }

在應用的 `ProcessPodcast`任務中，我們可以使用所有者標記恢復和釋放鎖：

    Cache::restoreLock('processing', $this->owner)->release();

如果你想釋放一個鎖，而不考慮鎖的目前擁有者，你可以使用 `forceRelease` 方法：

    Cache::lock('processing')->forceRelease();

<a name="adding-custom-cache-drivers"></a>
## 加入客製化的快取驅動

<a name="writing-the-driver"></a>
### 撰寫一個驅動

為了建立一個客製化的快取驅動，首先我們要實作一個 `Illuminate\Contracts\Cache\Store` [contract](/docs/{{version}}/contracts)。因此，一個 `MongoDB` 快取的實作會看起來像這樣：

    <?php

    namespace App\Extensions;

    use Illuminate\Contracts\Cache\Store;

    class MongoStore implements Store
    {
        public function get($key) {}
        public function many(array $keys) {}
        public function put($key, $value, $seconds) {}
        public function putMany(array $values, $seconds) {}
        public function increment($key, $value = 1) {}
        public function decrement($key, $value = 1) {}
        public function forever($key, $value) {}
        public function forget($key) {}
        public function flush() {}
        public function getPrefix() {}
    }

我們只需要透過一個 MongoDB 的連線來實作這些方法。那麼要如何實作這些方法呢？讓我們看一下 Laravel 框架中 `Illuminate\Cache\MemcachedStore` 的[原始程式碼](https://github.com/laravel/framework)。一旦我們完成實作之後，我們就可以接著透過呼叫 `Cache` 的 `extend` 方法，完成註冊我們的客製化驅動：

    Cache::extend('mongo', function ($app) {
        return Cache::repository(new MongoStore);
    });

> {tip} 如果你不知道要將你的客製化快取驅動程式碼放置在何處，你可以在你的 `app` 目錄下建立一個 `Extension` 的命名空間。但是請記住，Laravel 沒有硬性規定的應用程式結構，你可以依照你的喜好任意組織你的應用程式。

<a name="registering-the-driver"></a>
### 註冊快取驅動

為了註冊一個客製化的快取驅動，我們將會使用到 `Cache` facade 的 `extend` 方法。

要對 Laravel 註冊自定義的快取驅動，我們將使用 `Cache` facade 的 `extend` 方法。由於其他服務提供者可能會嘗試在他們的 `boot` 方法中讀取快取，我們將在 `booting` 回呼中註冊我們的自定義快取驅動。通過使用 `booting` 回呼，我們可以確保在應用程式的服務提供者呼叫 `boot` 方法之前，但在所有服務提供者調用 `register` 方法之後，註冊自定義驅動程式。我們將在應用內 `App\Providers\AppServiceProvider` 類別的 `register` 方法中，註冊我們的 `booting` 回呼：

    <?php

    namespace App\Providers;

    use App\Extensions\MongoStore;
    use Illuminate\Support\Facades\Cache;
    use Illuminate\Support\ServiceProvider;

    class CacheServiceProvider extends ServiceProvider
    {
        /**
         * 在容器中註冊綁定。
         *
         * @return void
         */
        public function register()
        {
            $this->app->booting(function () {
                 Cache::extend('mongo', function ($app) {
                     return Cache::repository(new MongoStore);
                 });
             });
        }

        /**
         * 執行註冊後的啟動服務。
         *
         * @return void
         */
        public function boot()
        {
            //
        }
    }

第一個傳遞給 `extend` 方法的參數是驅動的名稱，這個名稱要與你在 `config/cache.php` 設定檔中，`driver` 選項指定的名稱相同，第二個參數是一個應該要回傳一個 `Illuminate\Cache\Repository` 實例的閉包，這個閉包會被傳入一個 `$app` 實例，這個實例是屬於[服務容器](/docs/{{version}}/container)。

一旦你的擴充功能完成，你只需要簡單的更新 `config/cache.php` 設定檔中的 `driver` 選項為你的擴充功能名稱即可。

<a name="events"></a>
## 快取事件

如果要在每次操作快取時執行一段程式碼，你可以監聽由快取所觸發的[事件](/docs/{{version}}/events)。一般來說，你必須將事件監聽器放置在 `App\Providers\EventServiceProvider` 類別中：

    /**
     * 應用程式的事件監聽器列表。
     *
     * @var array
     */
    protected $listen = [
        'Illuminate\Cache\Events\CacheHit' => [
            'App\Listeners\LogCacheHit',
        ],

        'Illuminate\Cache\Events\CacheMissed' => [
            'App\Listeners\LogCacheMissed',
        ],

        'Illuminate\Cache\Events\KeyForgotten' => [
            'App\Listeners\LogKeyForgotten',
        ],

        'Illuminate\Cache\Events\KeyWritten' => [
            'App\Listeners\LogKeyWritten',
        ],
    ];
