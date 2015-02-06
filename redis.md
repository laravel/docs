# Redis

- [介紹](#introduction)
- [設定檔](#configuration)
- [使用方式](#usage)
- [管線](#pipelining)

<a name="introduction"></a>
## 介紹

[Redis](http://redis.io) 是開源，先進的鍵值對儲存庫。由於它可用的鍵包含了 [字串](http://redis.io/topics/data-types#strings)、[雜湊](http://redis.io/topics/data-types#hashes)、[列表](http://redis.io/topics/data-types#lists)、[集合](http://redis.io/topics/data-types#sets) 和 [有序集合](http://redis.io/topics/data-types#sorted-sets)，因此常被稱作資料結構伺服器。

在使用 Redis 之前，你需要經由 Composer 將 `predis/predis` 套件裝在 Laravel 中。

> **提醒：** 如果你用 PECL 安裝了 Redis PHP extension，則需要重新命名 `config/app.php` 裡的 Redis 別名。

<a name="configuration"></a>
## 設定檔

應用程式的 Redis 設定檔在 `config/database.php`。在這個檔案裡，你會看到 **redis** 陣列，裡面有應用程式使用的 Redis 伺服器資料：

	'redis' => array(

		'cluster' => true,

		'default' => array('host' => '127.0.0.1', 'port' => 6379),

	),

預設的伺服器設定對於開發應該是足夠的。然而，你可以根據使用環境自由修改陣列資料。只要給每個 Redis 一個名稱，並且設定伺服器的 host 和 port。

`cluster` 選項會讓 Laravel 的 Redis 客戶端在所有 Redis 節點間執行客戶端分片（ client-side sharding ），讓你建立節點池，並因此擁有大量的 RAM 可用。然而，客戶端分片的節點不能執行容錯轉移；因此，這主要適合用可以從另一台主要資料儲存庫取得的快取資料。

如果你的 Redis 伺服器需要認證，你可以在 Redis 伺服器設定檔裡加入 `password` 為鍵值的參數設定。

<a name="usage"></a>
## 使用方式

你可以經由 `Redis::connection` 方法得到 Redis 實例：

	$redis = Redis::connection();

你會得到一個使用 Redis 預設伺服器的實例。如果你沒有使用伺服器叢集，你可以在 `connection` 方法傳入定義在 Redis 設定檔的伺服器名稱，以連到特定伺服器：

	$redis = Redis::connection('other');

一旦你有了 Redis 客戶端實例，就可以使用實例發出任何 [Redis 命令](http://redis.io/commands)。Laravel 使用魔術方法傳遞命令到伺服器：

	$redis->set('name', 'Taylor');

	$name = $redis->get('name');

	$values = $redis->lrange('names', 5, 10);

注意，傳入命令的參數僅只是傳遞到魔術方法裡。當然，你不一定要使用魔術方法，你也可以使用 `command` 方法傳遞命令到伺服器：

	$values = $redis->command('lrange', array(5, 10));

若你只想對預設伺服器下命令，可以使用 `Redis` 類別的靜態魔術方法：

	Redis::set('name', 'Taylor');

	$name = Redis::get('name');

	$values = Redis::lrange('names', 5, 10);

> **提示：** 也可以使用 Redis 作為 Laravel 的 [快取](/docs/5.0/cache) 和 [session](/docs/5.0/session) 驅動。

<a name="pipelining"></a>
## 管線

當你想要一次發送很多命令到伺服器時可以使用管線。使用 `pipeline` 方法：

#### 發送多個命令到伺服器

	Redis::pipeline(function($pipe)
	{
		for ($i = 0; $i < 1000; $i++)
		{
			$pipe->set("key:$i", $i);
		}
	});
