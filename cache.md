# 快取

- [設定](#configuration)
- [快取的使用](#cache-usage)
    - [取得一個快取的實例](#obtaining-a-cache-instance)
    - [從快取中擷取項目](#retrieving-items-from-the-cache)
    - [存放項目到快取中](#storing-items-in-the-cache)
    - [刪除快取中的項目](#removing-items-from-the-cache)
- [加入客製化的快取驅動](#adding-custom-cache-drivers)
- [Cache Tags](#cache-tags)
    - [Storing Tagged Cache Items](#storing-tagged-cache-items)
    - [Accessing Tagged Cache Items](#accessing-tagged-cache-items)
- [Cache Events](#cache-events)

<a name="configuration"></a>
## 設定

Laravel 提供了一套統一的 API 給各種不同的快取系統，快取的設定檔都放在 `config/cache.php` 中，在這個檔案中，你可以指定在你的應用程式中，你預設想用哪個快取驅動，Laravel 支援流行的快取後端，如 [Memcached](http://memcached.org) 和 [Redis](http://redis.io)。

快取設定檔還包含了其他的選項，你可以在檔案中找到這些選項，請確保你都有讀過這些選項上方的說明。Laravel 預設採用的快取驅動是 `file`，這個驅動儲存了序列化(serialized) 的快取物件在檔案系統中，對於大型應用程式而言，Laravel 比較建議你使用一個 in-memory 快取，例如 Memcached 或 APC， 你可能也會想為同一個驅動設定多個快取設定檔。

### 快取預先需求

#### 資料庫

當使用 `database` 這個快取驅動，你需要設置一個表格來放置快取項目，你可以看一下範例 `Schema` 如何宣告這樣的表格：

    Schema::create('cache', function($table) {
        $table->string('key')->unique();
        $table->text('value');
        $table->integer('expiration');
    });

#### Memcached

使用 Memcached 做快取需要先安裝 [Memcached PECL package](http://pecl.php.net/package/memcached)。

預設的[設定檔](#configuration) 採用以 [Memcached::addServer](http://php.net/manual/en/memcached.addserver.php) 為基礎的 TCP/IP：

    'memcached' => [
        [
            'host' => '127.0.0.1',
            'port' => 11211,
            'weight' => 100
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

#### Redis

在你選擇使用 Redis 作為 Laravel 的快取前，你需要透過 Composer 預先安裝 `predis/predis` 套件 (~1.0)。

更多有關設定 Redis 的訊息，請參考 [Laravel documentation page](/docs/{{version}}/redis#configuration).

<a name="cache-usage"></a>
## 快取的使用

<a name="obtaining-a-cache-instance"></a>
### 取得一個快取的實例

`Illuminate\Contracts\Cache\Factory` 和 `Illuminate\Contracts\Cache\Repository` [contracts](/docs/{{version}}/contracts) 提供了存取 Laravel 快取服務的機制， 而`Factory` contract 則為你的應用程式提供了存取所有快取驅動的機制，`Repository` contract  是典型的快取驅動實作，它會依照你的快取設定檔變化。

然而，你可能也需要使用 `Cache` facade，我們會在整份文件中使用它，`Cache` facade 提供了方便又簡潔的方法存取現行實作的 Laravel cache contracts。

例如，我們試著在一個控制器中引用 `Cache` facade：

    <?php

    namespace App\Http\Controllers;

    use Cache;
    use Illuminate\Routing\Controller;

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

#### 存取多個快取儲存

使用 `Cache` facade，你可能會透過 `store` 方法來存取多個快取儲存，傳入 `store` 方法的鍵(key)應符合你在快取設定檔中的 `store` 設定項目指定的所有 store 列表其中一項：

    $value = Cache::store('file')->get('foo');

    Cache::store('redis')->put('bar', 'baz', 10);

<a name="retrieving-items-from-the-cache"></a>
### 從快取中擷取項目

在 `Cache` facade 中，`get` 方法可以用來取出快取中的項目，如果要取出的項目不再快取中，`get`方法會回傳 `null` ，如果你想，你也可以傳入第二個參數給 `get` 方法來客製化找不到項目時的預回傳值設值：

    $value = Cache::get('key');

    $value = Cache::get('key', 'default');


你甚至可能傳入一個閉包(`Closure`)作為預設值，當指定的項目不存在快取中十，閉包將會被回傳，傳入一個閉包讓你可以延後存資料庫或外部服務中取出預設值：

    $value = Cache::get('key', function() {
        return DB::table(...)->get();
    });

#### 確認項目存在

`has` 方法可以用來檢查一個項目是否存在於快取中：

    if (Cache::has('key')) {
        //
    }

#### 遞增/遞減值

`increment` 和 `decrement` 方法可以用來調整快取中的整數項目值，這兩個方法都可以選擇性的傳入第二個參數，用來指示要遞增或遞減多少：

    Cache::increment('key');

    Cache::increment('key', $amount);

    Cache::decrement('key');

    Cache::decrement('key', $amount);

#### 取出或更新

有時候，你可能會想從快取中取出一個項目，但也想在取出的項目不存在時存入一個預設值，例如，你可能會想從快取中取出所有使用者，或者當找不到使用者時，從資料庫中將這些使用者取出並放入快取中，則擬將會使用 `Cache::remember` 方法達到目的：

    $value = Cache::remember('users', $minutes, function() {
        return DB::table('users')->get();
    });

如果那個項目不存在快取中，則回傳給 `remember` 方法的閉包將會被執行，而且閉包的執行結果將會被存放在快取中。

你可能也會結合 `remember` 和 `forever` 這兩個方法：

    $value = Cache::rememberForever('users', function() {
        return DB::table('users')->get();
    });

#### 取出與刪除

如果你需要從快取中取出一個項目並刪除它，你可能會使用 `pull` 方法，與 `get` 相似，如果物件不存在快取中，`pull` 方法將會回傳 `null`：

    $value = Cache::pull('key');

<a name="storing-items-in-the-cache"></a>
### 存放項目到快取中

你可能會在 `Cache` facade 中使用 `put` 方法來存放項目到快取中，當你將一個項目放進快取時，你需要指定『幾分鐘』給將要存放的值：

    Cache::put('key', 'value', $minutes);

如果不指定分鐘數直到存放的項目過期，你也可能傳遞一個 PHP 的 `DateTime` 實例來表示該快取項目過期的時間點：

    $expiresAt = Carbon::now()->addMinutes(10);

    Cache::put('key', 'value', $expiresAt);

`add` 方法只會把還不存在快取中的項目放入快取，如果成功存放，會回傳 `true`，否回傳 `false`：

    Cache::add('key', 'value', $minutes);

`forever` 方法可以用來存放永久的項目到快取中，這些值必須被手動的刪除，這可以透過 `forget` 方法達成：

    Cache::forever('key', 'value');

<a name="removing-items-from-the-cache"></a>
### 刪除快取中的項目

你可能會使用 `forget` 方法在 `Cache` facade 下從快取中移除一個項目：

    Cache::forget('key');

You may clear the entire caching using the `flush` method:

    Cache::flush();

Flushing the cache **does not** respect the cache prefix and will remove all entries from the cache. Consider this carefully when clearing a cache which is shared by other applications.

<a name="adding-custom-cache-drivers"></a>
## 加入客製化的快取驅動

為了要透過客製化的驅動來擴充 Laravel 快取，我們將會在 `Cache` facade 中使用 `extend` 方法，它被用來綁定(bind)一個客製化驅動的解析器(resolver)到管理者(manager)上，通常這可以透過[service provider](/docs/{{version}}/providers)來完成。

例如，要註冊一個名為 “mongo” 的快取驅動：

    <?php

    namespace App\Providers;

    use Cache;
    use App\Extensions\MongoStore;
    use Illuminate\Support\ServiceProvider;

    class CacheServiceProvider extends ServiceProvider
    {
        /**
         * Perform post-registration booting of services.
         *
         * @return void
         */
        public function boot()
        {
            Cache::extend('mongo', function($app) {
                return Cache::repository(new MongoStore);
            });
        }

        /**
         * Register bindings in the container.
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

第一個傳給 `extend` 方法的參數是驅動的名稱，這個名稱要與你在 `config/cache.php` 設定檔中，`driver` 選項指定的名稱相同，第二個參數是一個應回傳一個 `Illuminate\Cache\Repository` 實例的閉包，這個閉包會被傳入一個 `$app` 實例，這個實例是屬於類別 [service container](/docs/{{version}}/container)。

呼叫 `Cache::extend` 的工作可以在新加入的 Laravel 應用程式中預設的 `App\Providers\AppServiceProvider` 的 `boot` 方法中完成，或者你可以建立你自己的服務提供者(service provider)來管理擴充功能(只是請別忘了在 `config/app.php` 中的 provider array 註冊這個提供者)。

為了建立我們的客製化快取驅動，首先需要實作 `Illuminate\Contracts\Cache\Store` [contract](/docs/{{version}}/contracts) contract。因此我們的 MongoDB 快取實作大概會長這樣子：

    <?php

    namespace App\Extensions;

    class MongoStore implements \Illuminate\Contracts\Cache\Store
    {
        public function get($key) {}
        public function put($key, $value, $minutes) {}
        public function increment($key, $value = 1) {}
        public function decrement($key, $value = 1) {}
        public function forever($key, $value) {}
        public function forget($key) {}
        public function flush() {}
        public function getPrefix() {}
    }

我們只需要透過一個 MongoDB 的連線來實作這些方法，一旦我們完成實作，我們就可以接著完成註冊我們的客製化驅動：

    Cache::extend('mongo', function($app) {
        return Cache::repository(new MongoStore);
    });

一旦你的擴充功能完成，你只需要簡單的更新 `config/cache.php` 設定檔中的 `driver` 選項為你的擴充功能名稱即可。

如果你不知道要將你的客製化快取驅動程式碼放置在何處，可以考慮將它放在 Packagist 上！或者你可以在你的 `app` 目錄下建立一個 `Extension` 的命名空間。但是請記住，Laravel 沒有硬性規定的應用程式結構，你可以依照你的喜好任意組織你的應用程式。

<a name="cache-tags"></a>
## Cache Tags

> **Note:** Cache tags are not supported when using the `file` or `database` cache drivers. Furthermore, when using multiple tags with caches that are stored "forever", performance will be best with a driver such as `memcached`, which automatically purges stale records.

<a name="storing-tagged-cache-items"></a>
### Storing Tagged Cache Items

Cache tags allow you to tag related items in the cache and then flush all cached values that assigned a given tag. You may access a tagged cache by passing in an ordered array of tag names. For example, let's access a tagged cache and `put` value in the cache:

	Cache::tags(['people', 'artists'])->put('John', $john, $minutes);

	Cache::tags(['people', 'authors'])->put('Anne', $anne, $minutes);

However, you are not limited to the `put` method. You may use any cache storage method while working with tags.

<a name="accessing-tagged-cache-items"></a>
### Accessing Tagged Cache Items

To retrieve a tagged cache item, pass the same ordered list of tags to the `tags` method:

	$john = Cache::tags(['people', 'artists'])->get('John');

    $anne = Cache::tags(['people', 'authors'])->get('Anne');

You may flush all items that are assigned a tag or list of tags. For example, this statement would remove all caches tagged with either `people`, `authors`, or both. So, both `Anne` and `John` would be removed from the cache:

	Cache::tags(['people', 'authors'])->flush();

In contrast, this statement would remove only caches tagged with `authors`, so `Anne` would be removed, but not `John`.

	Cache::tags('authors')->flush();

<a name="cache-events"></a>
## Cache Events

To execute code on every cache operation, you may listen for the events fired by the cache. Typically, you would place these event handlers within the `boot` method of your `EventServiceProvider`:

    /**
     * Register any other events for your application.
     *
     * @param  \Illuminate\Contracts\Events\Dispatcher  $events
     * @return void
     */
    public function boot(DispatcherContract $events)
    {
        parent::boot($events);

        $events->listen('cache.hit', function ($key, $value) {
            //
        });

        $events->listen('cache.missed', function ($key) {
            //
        });

        $events->listen('cache.write', function ($key, $value, $minutes) {
            //
        });

        $events->listen('cache.delete', function ($key) {
            //
        });
    }
