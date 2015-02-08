# Session

- [設定](#configuration)
- [使用 Session](#session-usage)
- [暫存資料（Flash Data）](#flash-data)
- [資料庫 Sessions](#database-sessions)
- [Session 驅動](#session-drivers)

<a name="configuration"></a>
## 設定

由於 HTTP 協定是無狀態（Stateless）的，所以 session 提供一種儲存用戶資料的方法。Laravel 支援了多種 session 後端驅動，並透過清楚、統一的 API 提供使用。也內建支援像是 [Memcached](http://memcached.org)、[Redis](http://redis.io) 和資料庫的後端驅動。

session 的設定檔配置在 `config/session.php` 中，請務必看一下 session 設定檔中可用的選項設定及註解。Laravel 預設使用 `file` 的 session 驅動，它在大多的應用中可以良好運作。

如果你想在 Laravel 中使用 `Redis` sessions，你需要先透過 Composer 安裝 `predis/predis` 套件 (~1.0)。

> **注意：** 如果你需要加密所有的 session 資料，就將選項 `encrypt` 設定為 `true` 。

#### 保留鍵值

Laravel 框架在內部有使用 `flash` 作為 session 的鍵值，所以應該避免 session 使用此名稱。

<a name="session-usage"></a>
## 使用 Session

#### 儲存項目到 Session 中

	Session::put('key', 'value');

#### 儲存項目進 Session 陣列值中

	Session::push('user.teams', 'developers');

#### 從 Session 取回項目

	$value = Session::get('key');

#### 從 Session 取回項目，若無則回傳預設值

	$value = Session::get('key', 'default');

	$value = Session::get('key', function() { return 'default'; });

#### 從 Session 取回項目，並刪除

	$value = Session::pull('key', 'default');

#### 從 Session 取出所有項目

	$data = Session::all();

#### 判斷項目在 Session 中是否存在

	if (Session::has('users'))
	{
		//
	}

#### 從 Session 中移除項目

	Session::forget('key');

#### 清空所有 Session

	Session::flush();

#### 重新產生 Session ID

	Session::regenerate();

<a name="flash-data"></a>
## 暫存資料（Flash Data）

有時你可能希望暫存一些資料，並只在下次請求有效。你可以使用 `Session::flash` 方法來達成目的：

	Session::flash('key', 'value');

#### 刷新當前暫存資料，延長到下次請求

	Session::reflash();

#### 只刷新指定快閃資料

	Session::keep(array('username', 'email'));

<a name="database-sessions"></a>
## 資料庫 Sessions

當使用 `database` session 驅動時，你必需建置一張儲存 session 的資料表。下方範例使用 `Schema` 來建表：

	Schema::create('sessions', function($table)
	{
		$table->string('id')->unique();
		$table->text('payload');
		$table->integer('last_activity');
	});

當然你也可以使用 Artisan 指令 `session:table` 來建 migration 表：

	php artisan session:table

	composer dump-autoload

	php artisan migrate

<a name="session-drivers"></a>
## Session 驅動

session 設定檔中的「driver」定義了 session 資料將以哪種方式被儲存。Laravel 提供了許多良好的驅動：

- `file` - sessions 將儲存在 `app/storage/sessions`。
- `cookie` - sessions 將安全儲存在加密的 cookies 中。
- `database` - sessions 將儲存在你的應用程式資料庫中
- `memcached` / `redis` - sessions 將儲存在一個高速快取的系統中。
- `array` - sessions 將單純的以 PHP 陣列儲存，只存活在當次請求。

> **注意：** array 驅動典型應用在 [unit tests](/docs/5.0/testing) 環境下，所以不會留下任何 session 資料。
