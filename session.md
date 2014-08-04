# Session

- [組態](#configuration)
- [Session 用法](#session-usage)
- [快閃資料（Flash Data）](#flash-data)
- [資料庫 Sessions](#database-sessions)
- [Session 驅動](#session-drivers)

<a name="configuration"></a>
## 組態

由於 HTTP 協定是無狀態（Stateless）的，所以 session 提供一種儲存用戶需要資料的方法。Laravel 制作了多種 session 後端驅動並透過清楚、統一的 API 提供使用。也內建支援像是 [Memcached](http://memcached.org), [Redis](http://redis.io) 等流行的後端驅動以及資料庫。

session 的設定檔配置在 `app/config/session.php` 中，請務必看一下 session 設定檔中可用的選項設定及註解。Laravel 預設使用 `file` 的 session 驅動，它在大多的應用中可以良好運作。

#### 保留 Keys

Laravel framework 在內部有使用 `flash` 作為 session key，所以應該避免 session 使用此名稱。


<a name="session-usage"></a>
## Session 用法

#### 儲存變數到 Session

	Session::put('key', 'value');

#### 在 Session 中儲存變數進陣列

	Session::push('user.teams', 'developers');

#### 從 Session 取回變數

	$value = Session::get('key');

#### 從 Session 取回變數，若無則回傳預設值

	$value = Session::get('key', 'default');

	$value = Session::get('key', function() { return 'default'; });

#### 從 Session 取回變數，並刪除

	$value = Session::pull('key', 'default');

#### 從 Session 取回所有變數

	$data = Session::all();

#### 判斷變數在 Session 中是否存在

	if (Session::has('users'))
	{
		//
	}

#### 移除 Session 中指定的變數

	Session::forget('key');

#### 清空整個 Session

	Session::flush();

#### 重新產生 Session ID

	Session::regenerate();

<a name="flash-data"></a>
## 快閃資料（Flash Data）

有時你可能希望暫存一些資料，並只在下次請求有效。你可以使用 `Session::flash` 方法來達成目的：

	Session::flash('key', 'value');

#### 刷新當前快閃資料，延長到下次請求

	Session::reflash();

#### 只刷新指定快閃資料

	Session::keep(array('username', 'email'));

<a name="database-sessions"></a>
## 資料庫 Sessions

當使用 `database` session 驅動時，你必需建置一張儲存 session 的表。下方範例使用 `Schema` 來建表：

	Schema::create('sessions', function($table)
	{
		$table->string('id')->unique();
		$table->text('payload');
		$table->integer('last_activity');
	});

當然你也可以使用 Artisan 指令 `session:table` 來建表：

	php artisan session:table

	composer dump-autoload

	php artisan migrate

<a name="session-drivers"></a>
## Session 驅動

session 設定檔中的 "drive" 定義了 session 資料將以哪種方式被儲存。Laravel 提供了許多良好的驅動：

- `file` - sessions 將儲存在 `app/storage/sessions` 資料夾中。
- `cookie` - sessions 將安全儲存在加密的 cookies 中。
- `database` - sessions 將儲存在你的應用程式資料庫中。
- `memcached` / `redis` - sessions 將儲存在一個高速快取的系統中。
- `array` - sessions 將單純的以 PHP 陣列儲存，只存在當次請求。

> **注意：** 運行 [unit tests](/docs/testing) 時，session 驅動會被設定為 `array`，所以不會留下任何 session 資料。
