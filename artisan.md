# Artisan 命令列介面

- [介紹](#introduction)
- [用法](#usage)
- [在命令列介面以外的地方呼叫命令](#calling-commands-outside-of-cli)
- [排程 Artisan 命令](#scheduling-artisan-commands)

<a name="introduction"></a>
## 介紹

Artisan 是 Laravel 內建的命令列介面。它提供了一些有用的指令協助您開發，它是由強大的 Symfony Console 元件所驅動。

<a name="usage"></a>
## 用法

#### 列出所有可用的命令

要查看所有可以使用的 Artisan 命令，你可以使用 `list` 命令：

	php artisan list

#### 瀏覽命令的幫助畫面

每個命令都包含一個顯示並描述這個命令能夠接受哪些參數和選項的「幫助畫面」。要瀏覽幫助畫面，只需要在命令名稱前面加上 `help` 即可：

	php artisan help migrate

#### 指定環境設定

您可以指定要使用的環境設定，只要在執行指令時加上 `--env` 即可切換：

	php artisan migrate --env=local

#### 顯示目前的 Laravel 版本

你也可以使用 `--version` 選項，查看目前安裝的 Laravel 版本：

	php artisan --version

<a name="calling-commands-outside-of-cli"></a>
## 在命令列介面以外的地方呼叫命令

有時你會希望在命令列介面以外的地方執行 Artisan 命令。例如，你可能會希望從 HTTP 路由呼叫 Artisan 命令。只要使用 `Artisan` facade 即可：

	Route::get('/foo', function()
	{
		$exitCode = Artisan::call('command:name', ['--option' => 'foo']);

		//
	});

你甚至可以把 Artisan 命令放到隊列，他們會藉由 [隊列工作者](/docs/5.0/queues) 在背景執行：

	Route::get('/foo', function()
	{
		Artisan::queue('command:name', ['--option' => 'foo']);

		//
	});

<a name="scheduling-artisan-commands"></a>
## 排程 Artisan 命令

過去，開發者會對每個他們想要排程的主控台命令建立 Cron 項目。然而，這很令人頭痛。你的主控台排程不再包含在版本控制裡面，並且你必須 SSH 進入你的伺服器以添加 Cron 項目。讓我們來讓生活變得更輕鬆。Laravel 命令排程器允許你順暢地且語義化地定義命令排程在 Laravel 裡面，而且你的伺服器只需要一個 Cron 項目。

你的命令排程儲存在 `app/Console/Kernel.php` 檔案。你會在這個類別裡看到一個 `schedule` 方法。為了幫助您開始，方法裡面包含一個簡單的例子。你可以依照你需要的自由地添加任何數量的預定工作到 `Schedule` 物件。你只需要添加這個 Cron 項目到伺服器：

	* * * * * php /path/to/artisan schedule:run 1>> /dev/null 2>&1

這個 Cron 將會每分鐘呼叫 Laravel 命令排程器。接著，Laravel 評估你的預定工作並在時間到時執行工作。這不能再更簡單了！

### 更多排程的例子

讓我們來多看幾個排程的例子：

#### 排程閉包

	$schedule->call(function()
	{
		// 執行一些任務...

	})->hourly();

#### 排程終端機命令

	$schedule->exec('composer self-update')->daily();

#### 自己設定 Cron 表達式

	$schedule->command('foo')->cron('* * * * *');

#### 頻繁的工作

	$schedule->command('foo')->everyFiveMinutes();

	$schedule->command('foo')->everyTenMinutes();

	$schedule->command('foo')->everyThirtyMinutes();

#### 每天一次的工作

	$schedule->command('foo')->daily();

#### 每天一次在特定時間 (24 小時制) 的工作

	$schedule->command('foo')->dailyAt('15:00');

#### 每天兩次的工作

	$schedule->command('foo')->twiceDaily();

#### 每個工作日執行的工作

	$schedule->command('foo')->weekdays();

#### 每週一次的工作

	$schedule->command('foo')->weekly();

	// 排程每週一次在特定的日子 (0-6) 和時間的工作...
	$schedule->command('foo')->weeklyOn(1, '8:00');

#### 每月一次的工作

	$schedule->command('foo')->monthly();

#### 限制應該執行工作的環境

	$schedule->command('foo')->monthly()->environments('production');

#### 指定工作在當應用程式處於維護模式也應該執行

	$schedule->command('foo')->monthly()->evenInMaintenanceMode();

#### 只允許工作在閉包回傳 true 的時候執行

	$schedule->command('foo')->monthly()->when(function()
	{
		return true;
	});
