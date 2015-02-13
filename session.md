# Session

- [设置](#configuration)
- [使用 Session](#session-usage)
- [暂存数据（Flash Data）](#flash-data)
- [数据库 Sessions](#database-sessions)
- [Session 驱动](#session-drivers)

<a name="configuration"></a>
## 设置

由于 HTTP 协定是无状态（Stateless）的，所以 session 提供一种保存用户数据的方法。Laravel 支持了多种 session 后端驱动，并透过清楚、统一的 API 提供使用。也内置支持像是 [Memcached](http://memcached.org)、[Redis](http://redis.io) 和数据库的后端驱动。

session 的设置档配置在 `config/session.php` 中，请务必看一下 session 设置档中可用的选项设置及注解。Laravel 默认使用 `file` 的 session 驱动，它在大多的应用中可以良好运作。

如果你想在 Laravel 中使用 `Redis` sessions，你需要先透过 Composer 安装 `predis/predis` 套件 (~1.0)。

> **注意：** 如果你需要加密所有的 session 数据，就将选项 `encrypt` 设置为 `true` 。

#### 保留键值

Laravel 框架在内部有使用 `flash` 作为 session 的键值，所以应该避免 session 使用此名称。

<a name="session-usage"></a>
## 使用 Session

#### 保存项目到 Session 中

	Session::put('key', 'value');

#### 保存项目进 Session 数组值中

	Session::push('user.teams', 'developers');

#### 从 Session 取回项目

	$value = Session::get('key');

#### 从 Session 取回项目，若无则返回默认值

	$value = Session::get('key', 'default');

	$value = Session::get('key', function() { return 'default'; });

#### 从 Session 取回项目，并删除

	$value = Session::pull('key', 'default');

#### 从 Session 取出所有项目

	$data = Session::all();

#### 判断项目在 Session 中是否存在

	if (Session::has('users'))
	{
		//
	}

#### 从 Session 中移除项目

	Session::forget('key');

#### 清空所有 Session

	Session::flush();

#### 重新产生 Session ID

	Session::regenerate();

<a name="flash-data"></a>
## 暂存数据（Flash Data）

有时你可能希望暂存一些数据，并只在下次请求有效。你可以使用 `Session::flash` 方法来达成目的：

	Session::flash('key', 'value');

#### 刷新当前暂存数据，延长到下次请求

	Session::reflash();

#### 只刷新指定快闪数据

	Session::keep(array('username', 'email'));

<a name="database-sessions"></a>
## 数据库 Sessions

当使用 `database` session 驱动时，你必需建置一张保存 session 的数据表。下方范例使用 `Schema` 来建表：

	Schema::create('sessions', function($table)
	{
		$table->string('id')->unique();
		$table->text('payload');
		$table->integer('last_activity');
	});

当然你也可以使用 Artisan 指令 `session:table` 来建 migration 表：

	php artisan session:table

	composer dump-autoload

	php artisan migrate

<a name="session-drivers"></a>
## Session 驱动

session 设置档中的「driver」定义了 session 数据将以哪种方式被保存。Laravel 提供了许多良好的驱动：

- `file` - sessions 将保存在 `app/storage/sessions`。
- `cookie` - sessions 将安全保存在加密的 cookies 中。
- `database` - sessions 将保存在你的应用程序数据库中
- `memcached` / `redis` - sessions 将保存在一个高速缓存的系统中。
- `array` - sessions 将单纯的以 PHP 数组保存，只存活在当次请求。

> **注意：** array 驱动典型应用在 [unit tests](/docs/5.0/testing) 环境下，所以不会留下任何 session 数据。
