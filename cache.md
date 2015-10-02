# 快取

- [設定](#configuration)
- [快取的使用](#cache-usage)
    - [取得一個快取的實體](#obtaining-a-cache-instance)
    - [從快取中擷取項目](#retrieving-items-from-the-cache)
    - [存放項目到快取中](#storing-items-in-the-cache)
    - [刪除快取中的項目](#removing-items-from-the-cache)
- [加入客製化的快取驅動](#adding-custom-cache-drivers)

<a name="configuration"></a>
## 設定

Laravel 提供了一套統一的 API 給各種不同的快取系統，快取的設定檔都放在 `config/cache.php` 中，在這個檔案中，你可以指定在你的應用程式中，你預設想用哪個快取驅動，Laravel 支援流行的快取後端，如 [Memcached](http://memcached.org) 和 [Redis](http://redis.io)。

快取設定檔還包含了其他的選項，你可以在檔案中找到這些選項，請確保你都有讀過這些選項上方的說明。Laravel 預設採用的快取驅動是 `file`，這個驅動儲存了序列化(serialized) 的快取物件在檔案系統中，對於大型應用程式而言，Laravel 比較建議你使用一個 in-memory 快取，例如 Memcached 或 APC， 你可能也會想為同一個驅動設定多個快取設定檔。

### 快取預先需求

#### 資料庫

當使用 `database` 這個快取驅動，你需要設置一個表格來放置快取項目，你可以看一下範例 `Schema` 如何宣告這樣的表格:

    Schema::create('cache', function($table) {
        $table->string('key')->unique();
        $table->text('value');
        $table->integer('expiration');
    });

#### Memcached

使用 Memcached 做快取需要先安裝 [Memcached PECL package](http://pecl.php.net/package/memcached)。

預設的[設定檔](#configuration) 採用以 [Memcached::addServer](http://php.net/manual/en/memcached.addserver.php) 為基礎的 TCP/IP:

    'memcached' => [
        [
            'host' => '127.0.0.1',
            'port' => 11211,
            'weight' => 100
        ],
    ],

你可能也會設置 `host` 選項到 UNIX 的 socket 路徑中，如果你有這麼做，記得 `port` 選項要設為 `0`:

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
### 取得一個快取的實體

`Illuminate\Contracts\Cache\Factory` 和 `Illuminate\Contracts\Cache\Repository` [contracts](/docs/{{version}}/contracts) 提供了存取 Laravel 快取服務的機制， 而`Factory` contract 則為你的應用程式提供了存取所有快取驅動的機制，`Repository` contract  是典型的快取驅動實作，它會依照你的快取設定檔變化。

然而，你可能也需要使用 `Cache` facade，我們會在整份文件中使用它，`Cache` facade 提供了方便又簡潔的方法存取現行實作的 Laravel cache contracts。

例如，我們試著在一個控制器中引用 `Cache` facade:

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

使用 `Cache` facade，你可能會透過 `store` 方法來存取多個快取儲存，傳入 `store` 方法的鍵值(key)應符合你在快取設定檔中的 `store` 設定項目指定的所有 store 列表其中一項:

    $value = Cache::store('file')->get('foo');

    Cache::store('redis')->put('bar', 'baz', 10);

<a name="retrieving-items-from-the-cache"></a>
### 從快取中擷取項目

在 `Cache` facade 中，`get` 方法可以用來取出快取中的項目，如果要取出的項目不再快取中，`get`方法會回傳 `null` ，如果你想，你也可以傳入第二個參數給 `get` 方法來客製化找不到項目時的預回傳值設值:

    $value = Cache::get('key');

    $value = Cache::get('key', 'default');

你甚至可能傳入一個閉包(`Closure`)作為預設值，當指定的項目不存在快取中十，閉包將會被回傳，傳入一個閉包讓你可以延後存資料庫或外部服務中取出預設值:

    $value = Cache::get('key', function() {
        return DB::table(...)->get();
    });

#### 確認項目存在

`has` 方法可以用來檢查一個項目是否存在於快取中:

    if (Cache::has('key')) {
        //
    }

#### 遞增/遞減值

`increment` 和 `decrement` 方法可以用來調整快取中的整數項目值，這兩個方法都可以選擇性的傳入第二個參數，用來指示要遞增或遞減多少:

    Cache::increment('key');

    Cache::increment('key', $amount);

    Cache::decrement('key');

    Cache::decrement('key', $amount);

#### 取出或更新

有時候，你可能會想從快取中取出一個項目，但也想在取出的項目不存在時存入一個預設值，例如，你可能會想從快取中取出所有使用者，或者當找不到使用者時，從資料庫中將這些使用者取出並放入快取中，則擬將會使用 `Cache::remember` 方法達到目的:

    $value = Cache::remember('users', $minutes, function() {
        return DB::table('users')->get();
    });

If the item does not exist in the cache, the `Closure` passed to the `remember` method will be executed and its result will be placed in the cache.

You may also combine the `remember` and `forever` methods:

    $value = Cache::rememberForever('users', function() {
        return DB::table('users')->get();
    });

#### Retrieve And Delete

If you need to retrieve an item from the cache and then delete it, you may use the `pull` method. Like the `get` method, `null` will be returned if the item does not exist in the cache:

    $value = Cache::pull('key');

<a name="storing-items-in-the-cache"></a>
### Storing Items In The Cache

You may use the `put` method on the `Cache` facade to store items in the cache. When you place an item in the cache, you will need to specify the number of minutes for which the value should be cached:

    Cache::put('key', 'value', $minutes);

Instead of passing the number of minutes until the item expires, you may also pass a PHP `DateTime` instance representing the expiration time of the cached item:

    $expiresAt = Carbon::now()->addMinutes(10);

    Cache::put('key', 'value', $expiresAt);

The `add` method will only add the item to the cache if it does not already exist in the cache store. The method will return `true` if the item is actually added to the cache. Otherwise, the method will return `false`:

    Cache::add('key', 'value', $minutes);

The `forever` method may be used to store an item in the cache permanently. These values must be manually removed from the cache using the `forget` method:

    Cache::forever('key', 'value');

<a name="removing-items-from-the-cache"></a>
### Removing Items From The Cache

You may remove items from the cache using the `forget` method on the `Cache` facade:

    Cache::forget('key');

<a name="adding-custom-cache-drivers"></a>
## Adding Custom Cache Drivers

To extend the Laravel cache with a custom driver, we will use the `extend` method on the `Cache` facade, which is used to bind a custom driver resolver to the manager. Typically, this is done within a [service provider](/docs/{{version}}/providers).

For example, to register a new cache driver named "mongo":

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

The first argument passed to the `extend` method is the name of the driver. This will correspond to your `driver` option in the `config/cache.php` configuration file. The second argument is a Closure that should return an `Illuminate\Cache\Repository` instance. The Closure will be passed an `$app` instance, which is an instance of the [service container](/docs/{{version}}/container).

The call to `Cache::extend` could be done in the `boot` method of the default `App\Providers\AppServiceProvider` that ships with fresh Laravel applications, or you may create your own service provider to house the extension - just don't forget to register the provider in the `config/app.php` provider array.

To create our custom cache driver, we first need to implement the `Illuminate\Contracts\Cache\Store` [contract](/docs/{{version}}/contracts) contract. So, our MongoDB cache implementation would look something like this:

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
    }

We just need to implement each of these methods using a MongoDB connection. Once our implementation is complete, we can finish our custom driver registration:

    Cache::extend('mongo', function($app) {
        return Cache::repository(new MongoStore);
    });

Once your extension is complete, simply update your `config/cache.php` configuration file's `driver` option to the name of your extension.

If you're wondering where to put your custom cache driver code, consider making it available on Packagist! Or, you could create an `Extensions` namespace within your `app` directory. However, keep in mind that Laravel does not have a rigid application structure and you are free to organize your application according to your preferences.
