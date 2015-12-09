# Session

- [簡介](#introduction)
- [基本用法](#basic-usage)
    - [快閃資料](#flash-data)
- [增加 Session 驅動](#adding-custom-session-drivers)

<a name="introduction"></a>
## 簡介

由於 HTTP 協定是無狀態的，所以 session 提供一種儲存用戶資料的方法。Laravel 附帶支援了多種 session 後端驅動，並透過統一的 API 進行使用。也內建支援像是 [Memcached](http://memcached.org)、[Redis](http://redis.io) 和資料庫的後端驅動。

### 設定

Session 的設定檔配置在 `config/session.php`。請務必看一下此設定檔中可用的選項設定及註解。Laravel 預設使用 `file` 的 session 驅動，它在大多的應用中可以良好運作。在上線的應用程式中，你可能會考慮使用更快的 `memcached ` 或 `redis` 等驅動。

Session `driver` 定義了資料將由什麼樣的方式儲存。Laravel 附帶了幾個不錯且可立即使用的驅動：

<div class="content-list" markdown="1">
- `file` - 將 sessions 儲存在 `storage/framework/sessions` 中。
- `cookie` - 將 sessions 安全的儲存在加密後的 cookies 中。
- `database` - 將 sessions 儲存在應用程式使用的資料庫中。
- `memcached` / `redis` - 將 sessions 儲存在其中一個快速並基於快取的儲存系統中。
- `array` - 將 sessions 儲存在簡單的 PHP 陣列中，並只存活在當次請求。
</div>

> **注意：**陣列驅動一般應使用在[測試](/docs/{{version}}/testing)環境下，以防止 session 資料持續存在。

### 驅動介紹

#### 資料庫

當使用 `database` session 驅動時，你必需先建置儲存 session 項目的資料表。下方範例使用 `Schema` 語法建表：

    Schema::create('sessions', function ($table) {
        $table->string('id')->unique();
        $table->text('payload');
        $table->integer('last_activity');
    });

你也可使用 `session:table` Artisan 指令產生遷移檔！

    php artisan session:table

    composer dump-autoload

    php artisan migrate

#### Redis

在 Laravel 使用 Redis Session 之前，你需要先透過 Composer 安裝 `predis/predis`(~1.0) 套件。

### 其它 Session 注意事項

Laravel 框架在內部有使用 `flash` 作為 session 的鍵，所以應該避免 session 使用此名稱。

如果你的 session 資料需要加密，在設定檔中的 `encrypt` 選項設為 `true`。

<a name="basic-usage"></a>
## 基本用法

#### 存取 Session

首先，讓我們存取 session。我們可以在控制器方法內，透過對 HTTP 請求使用型別提示存取 session 實例。請記得，控制器方法的依賴是透過 Laravel 的[服務容器](/docs/{{version}}/container)注入：

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * 顯示給定使用者的個人檔案。
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

當你從 session 取出值，你可以在 `get` 方法中的第二個參數內設定一個預設值。如果指定的鍵名不存在時，將會回傳設定的預設值。如果你傳入一個 `閉包` 作為 `get` 方法的預設值，該 `必包` 將被執行並回傳它的結果：

    $value = $request->session()->get('key', 'default');

    $value = $request->session()->get('key', function() {
        return 'default';
    });

如果你想從 session 中取得所有資料，你可以使用 `all` 方法：

    $data = $request->session()->all();

你也可使用全域的 `session` PHP 函式取得 session 中儲存的資料：

    Route::get('home', function () {
        // 取得 session 中的一筆資料...
        $value = session('key');

        // 寫入一筆資料至 session 中...
        session(['key' => 'value']);
    });

#### 判斷項目在 Session 中是否存在

`has` 方法被用於檢查項目是否存在於 session 內。如果存在將會回傳 `true`：

    if ($request->session()->has('users')) {
        //
    }

#### 儲存資料到 Session 中

只要你可以存取 session 實例，你就可以呼叫多種函式調整裡面的資料。例如，`put` 方法能將一個新的資料加入現有的 session 內。

    $request->session()->put('key', 'value');

#### 儲存資料進 Session 陣列值中

`push` 方法可以將一個新的值，加入至一個 session 的陣列。例如，假設 `user.teams` 這個鍵是包含團隊名稱的陣列，你可以將一個新的值加入此陣列中：

    $request->session()->push('user.teams', 'developers');

#### 從 Session 取回資料，並且刪除資料

`pull` 方法將把資料從 session 內取出，並且刪除它：

    $value = $request->session()->pull('key', 'default');

#### 從 Session 中移除資料

`forget` 方法可以從 session 內刪除一筆資料。如果你想刪除 session 內所有的資料，可以使用 `flush` 方法：

    $request->session()->forget('key');

    $request->session()->flush();

#### 重新產生 Session ID

如果你想重新產生 session ID，你可以使用 `regenerate` 方法：

    $request->session()->regenerate();

<a name="flash-data"></a>
### 快閃資料

有時候你想存入一筆暫存的資料，讓它只有在下一次的請求內有效。你可以使用 `flash` 方法達到這個目的。史用這個方法儲存，只能將資料保留到下個 HTTP 請求，然後就會自動刪除。快閃資料在短期的狀態訊息中很有用：

    $request->session()->flash('status', 'Task was successful!');

如果需要保留閃存資料給更多的請求，可以使用 `reflash` 方法，這將會保留所有的快閃資料給額外的請求。如果只想留一個特定的快內資料，你可以使用 `keep` 方法：

    $request->session()->reflash();

    $request->session()->keep(['username', 'email']);

<a name="adding-custom-session-drivers"></a>
## 加入自定的 Session 驅動

要加入額外驅動至 Laravel 的 session 中，你可以使用 `Session` [facade](/docs/{{version}}/session) 的 `extend` 方法。你可以在[服務提供者](/docs/{{version}}/providers) 的 `boot` 方法內呼叫 `extend` 方法：

    <?php

    namespace App\Providers;

    use Session;
    use App\Extensions\MongoSessionStore;
    use Illuminate\Support\ServiceProvider;

    class SessionServiceProvider extends ServiceProvider
    {
        /**
         * 提供註冊後執行的服務。
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
         * 在容器中註冊綁定。
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

請注意，你的自定義 session 驅動必需實作 `SessionHandlerInterface`。這個介面包含了一些需要實作的方法。一個基本的 MongoDB 實作看起來像：

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

由於這些方法就像快取的 `StoreInterface` 一樣並不是那麼容易理解，讓我們快速的了解每個方法的做用：

<div class="content-list" markdown="1">
- `open` 方法通常用在基於檔案的 session 儲存系統中。像 Larvel 附帶了一個 `file` 的驅動，所以你不用把任何東西放到這個方法內。你可以把這方法看做是空的也沒關係；很簡單的事實只是因為不佳的介面設計（我們將在之後討論），所以 PHP 要求必需要有這個方法的實作。
- `close` 方法跟 `open` 方法很像，通常也是被忽略，對大多數的驅動而言，這並不是需要的。
- `read` 方法必須根據給予的 `$sessionId` 回傳關聯的 session 資料的字串版本。在驅動中這並不需要做任何的編碼跟序列化的動作，在 Laravel 內已自動執行。
- `write` 方法必須在大部分儲存系統內寫入 `$data` 字串時關聯至 `$sessionId`，如 MongoDB、Dynamo 等等。
- `destroy` 方法能刪除與 `$sessionId` 關聯的資料。
- `gc` 方法能刪除給予 `$lifetime` 之前的所有資料，`$lifetime` 是一個 UNIX 的時間戳記。但在一些系統如 Memcached 和 Redis 這個方法可能會留下一段空白的儲存資料。
</div>

一但 session 驅動被註冊後，你必須在 `config/session.php` 的設定檔內使用 `mongo` 驅動。
