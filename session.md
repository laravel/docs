# Session

- [簡述](#introduction)
- [基本用法](#basic-usage)
    - [暫存資料](#flash-data)
- [增加 Session 驅動](#adding-custom-session-drivers)

<a name="introduction"></a>
## 簡述

由於 HTTP 協定是無狀態（Stateless）的，所以 session 提供一種儲存用戶資料的方法。 Laravel 附帶支援了多種 session 後端驅動，並透過統一的 API 進行使用。 Support 也內建支援像是 [Memcached](http://memcached.org)、[Redis](http://redis.io) 和資料庫的後端驅動。

### 設定

Session 的設定檔配置在 `config/session.php`. 請務必看一下 此設定檔中可用的選項設定及註解。Laravel 預設使用 `file`的 session 驅動，它在大多的應用中可以良好運作。在正式機中，您可能會考慮使用更快的 `memcached ` 或 `redis` 等後端驅動。

Session `driver` 定義了資料將由什麼樣的方式儲存。
Laravel 包裝了幾個後端驅動 : 

<div class="content-list" markdown="1">
- `file` - 將 sessions 儲存在 `storage/framework/sessions`。
- `cookie` - 將 sessions 儲存在安全，加密後的 cookies。
- `database` - 將 sessions 儲存在 應用程式使用的資料庫中。
- `memcached` / `redis` - 將 sessions 儲存在 `memcached` / `redis`高速快取的系統中。
- `array` - 將 sessions 儲存在PHP的 `array` 格式，只存活在當次請求。
</div>

> **注意:** array 驅動典型應用在 [tests](/docs/{{version}}/testing) 環境下，所以不會留下任何 session 資料。

### 驅動介紹

#### 資料庫

當使用 `database` session 驅動時, 你必需先建置儲存 session 的資料表. 下方範例使用 `Schema` 建表:

    Schema::create('sessions', function ($table) {
        $table->string('id')->unique();
        $table->text('payload');
        $table->integer('last_activity');
    });

你也可使用 `session:table` Artisan 指令產生 migration 建表 : 

    php artisan session:table

    composer dump-autoload

    php artisan migrate

#### Redis

在 Laravel 使用 Redis Session 之前，你需要先用 Composer 安裝 `predis/predis`(~1.0) 套件。

### 其它 Session 注意事項

Laravel 框架在內部有使用 `flash` 作為 session 的鍵值，所以應該避免 session 使用此名稱。

如果您的 session 資料需要加密，在設定檔中的 `encrypt` 參數設為 `true`。

<a name="basic-usage"></a>
## 基本用法

#### 訪問 Session

首先，我們可在控制器方法內，實作 HTTP 請求訪問 Session。 請記得，控制器方法相依需從 Laravel 注入 [service container](/docs/{{version}}/container): 

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * Show the profile for the given user.
         *
         * @param  Request  $request
         * @param  int  $id
         * @return Response
         */
        public function showProfile(Request $request, $id)
        {
            $value = $request->session()->get('key');

            //
        }
    }

當你從 session 取出值，你可以在 `get` 方法中的第二個參數內設定一個默認值。如果指定的鍵名不存在時，將會回傳設定的默認值。如果你輸入一個 `Closure` Function 在默認參數中，該`Closure`將被執行並返回它的結果 : 

    $value = $request->session()->get('key', 'default');

    $value = $request->session()->get('key', function() {
        return 'default';
    });

如果你想從 session 中取得所有數據，你可以使用 `all` 方法 : 

    $data = $request->session()->all();

你也可使用全域的PHP方式 存取 session : 

    Route::get('home', function () {
        // Retrieve a piece of data from the session...
        $value = session('key');

        // Store a piece of data in the session...
        session(['key' => 'value']);
    });

#### 判斷項目在 Session 中是否存在

`has` 方法將會確認 session 內是否有存在，如果存在將回傳 true :

    if ($request->session()->has('users')) {
        //
    }

#### 儲存資料到 Session 中

一但你能存取一個 session 實例，你就可以調整裡面的數據，例如 `put`方法能將一個新的數據加入現有的 session 內。

    $request->session()->put('key', 'value');

#### 儲存資料進 Session 陣列值中

`push` 方法可以將一個新的值，丟進一個陣例的 session 數組內。例如 `user.teams` 這個鍵的內容是一組陣列的組名，你可以將一個新的值加入此陣列中 :

    $request->session()->push('user.teams', 'developers');

#### 從 Session 取回資料，並且刪除資料

`pull` 方法將把資料從 session內取出，並且刪除它 : 

    $value = $request->session()->pull('key', 'default');

#### 從 Session 中移除資料

`forget` 方法將會從 session 內刪除鍵名內資料。
如果你想從session內刪除所有的資料，可以使用 `flush` 方法 : 

    $request->session()->forget('key');

    $request->session()->flush();

#### 重新產生 Session ID

如果你想從新產生 session ID，你可以使用 `regenerate` 方法 : 

    $request->session()->regenerate();

<a name="flash-data"></a>
### 閃存資料 (Flash Data)

有時候你想存入一筆暫存的資料，讓它只有在下一次的請求內有效，你可以使用 `flash` 方法。用這個方法儲存，只能將資料保留到下個 HTTP 的請求出現，然後就會自動刪除。閃存資料在短期的狀態中很有用 : 

    $request->session()->flash('status', 'Task was successful!');

如果需要保持住閃存資料給其它的請求，可以使用 `reflash`方法，這將會保持住所有的閃存資料給其它的請求。如果只想保持住一個特定的快內資料，你可以使用 `keep` 方法 : 

    $request->session()->reflash();

    $request->session()->keep(['username', 'email']);

<a name="adding-custom-session-drivers"></a>
## 加入自定 Session 驅動

要加入特定的 session 驅動，可以使用 `extend` [facade](/docs/{{version}}/session)。可以在 `boot` 方法內呼叫 `extend`[service provider](/docs/{{version}}/providers):

    <?php

    namespace App\Providers;

    use Session;
    use App\Extensions\MongoSessionStore;
    use Illuminate\Support\ServiceProvider;

    class SessionServiceProvider extends ServiceProvider
    {
        /**
         * Perform post-registration booting of services.
         *
         * @return void
         */
        public function boot()
        {
            Session::extend('mongo', function($app) {
                // Return implementation of SessionHandlerInterface...
                return new MongoSessionStore;
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

**注意:** 在自定義 session 驅動必需先繼承 `SessionHandlerInterface`。這個介面包含了一些必要的實作。例如使用 MongoDB 驅動看起來像 :

    <?php

    namespace App\Extensions;

    class MongoHandler implements SessionHandlerInterface
    {
        public function open($savePath, $sessionName) {}
        public function close() {}
        public function read($sessionId) {}
        public function write($sessionId, $data) {}
        public function destroy($sessionId) {}
        public function gc($lifetime) {}
    }

由於 `StoreInterface` 這些方法並不是那麼容易理解。所以全部的解釋一下 : 

<div class="content-list" markdown="1">
- `open` 方法通常用在檔內的 session 儲存系統中。像 Larvel 自帶了一個 `file`的驅動，所以你不用把任何東西放到這個法方內，可以把這方法看做是空的也沒關係 ; 這只是因為PHP要求必需要有這個方法的實作。
- `close` 方法跟 `open`方法很像，通常也是被忽略，對大多數的驅動而言，這並不是需要的。
- `read` 方法能返回資料的版本字串 `$session` 。在驅動中這並不需要做任何的編碼跟序列化的動作，在 Laravel 內已自動執行。
- `write` 方法在儲存驅動內寫入 `$data` 時能加入 `$sessionId` (關聯ID)，如 MongoDB, Dynamo, etc。
- `destroy` 方法能刪除 `$sessionId` (關聯ID)的所有相關資料。
- `gc` 方法能刪除給予 `$lifetime` 之前的所有資料，`$lifetime` 是一個 UNIX的時間戳。但在一些系統如 Memcached和 Redis 這個方法可能會留下一段空白的儲存資料。
</div>

一但你在 `config/session.php` 的設定檔內註冊  `mongo` 的驅動，就能使用`mongo`方式的 session 存儲。
