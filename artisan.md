# Artisan 命令行接口

- [介绍](#introduction)
- [用法](#usage)
- [在命令行接口以外的地方调用命令](#calling-commands-outside-of-cli)
- [调度 Artisan 命令](#scheduling-artisan-commands)

<a name="introduction"></a>
## 介绍

Artisan 是 Laravel 内置的命令行接口。它提供了一些有用的指令协助您开发，它是由强大的 Symfony Console 组件所驱动。

<a name="usage"></a>
## 用法

#### 列出所有可用的命令

要查看所有可以使用的 Artisan 命令，你可以使用 `list` 命令：

	php artisan list

#### 浏览命令的帮助画面

每个命令都包含一个显示并描述这个命令能够接受哪些参数和选项的「帮助画面」。要浏览帮助画面，只需要在命令名称前面加上 `help` 即可：

	php artisan help migrate

#### 指定环境设置

您可以指定要使用的环境设置，只要在执行指令时加上 `--env` 即可切换：

	php artisan migrate --env=local

#### 显示目前的 Laravel 版本

你也可以使用 `--version` 选项，查看目前安装的 Laravel 版本：

	php artisan --version

<a name="calling-commands-outside-of-cli"></a>
## 在命令行接口以外的地方调用命令

有时你会希望在命令行接口以外的地方执行 Artisan 命令。例如，你可能会希望从 HTTP 路由调用 Artisan 命令。只要使用 `Artisan` facade 即可：

	Route::get('/foo', function()
	{
		$exitCode = Artisan::call('command:name', ['--option' => 'foo']);

		//
	});

你甚至可以把 Artisan 命令放到队列，他们会借由 [队列工作者](/docs/5.0/queues) 在背景执行：

	Route::get('/foo', function()
	{
		Artisan::queue('command:name', ['--option' => 'foo']);

		//
	});

<a name="scheduling-artisan-commands"></a>
## 调度 Artisan 命令

过去，开发者会对每个他们想要调度的主控台命令建立 Cron 项目。然而，这很令人头痛。你的主控台调度不再包含在版本控制里面，并且你必须 SSH 进入你的服务器以添加 Cron 项目。让我们来让生活变得更轻松。Laravel 命令调度器允许你顺畅地且语义化地定义命令调度在 Laravel 里面，而且你的服务器只需要一个 Cron 项目。

你的命令调度保存在 `app/Console/Kernel.php` 文件。你会在这个类别里看到一个 `schedule` 方法。为了帮助您开始，方法里面包含一个简单的例子。你可以依照你需要的自由地添加任何数量的预定工作到 `Schedule` 对象。你只需要添加这个 Cron 项目到服务器：

	* * * * * php /path/to/artisan schedule:run 1>> /dev/null 2>&1

这个 Cron 将会每分钟调用 Laravel 命令调度器。接着，Laravel 评估你的预定工作并在时间到时执行工作。这不能再更简单了！

### 更多调度的例子

让我们来多看几个调度的例子：

#### 调度闭包

	$schedule->call(function()
	{
		// 执行一些任务...

	})->hourly();

#### 调度终端机命令

	$schedule->exec('composer self-update')->daily();

#### 自己设置 Cron 表达式

	$schedule->command('foo')->cron('* * * * *');

#### 频繁的工作

	$schedule->command('foo')->everyFiveMinutes();

	$schedule->command('foo')->everyTenMinutes();

	$schedule->command('foo')->everyThirtyMinutes();

#### 每天一次的工作

	$schedule->command('foo')->daily();

#### 每天一次在特定时间 (24 小时制) 的工作

	$schedule->command('foo')->dailyAt('15:00');

#### 每天两次的工作

	$schedule->command('foo')->twiceDaily();

#### 每个工作日执行的工作

	$schedule->command('foo')->weekdays();

#### 每周一次的工作

	$schedule->command('foo')->weekly();

	// 调度每周一次在特定的日子 (0-6) 和时间的工作...
	$schedule->command('foo')->weeklyOn(1, '8:00');

#### 每月一次的工作

	$schedule->command('foo')->monthly();

#### 限制应该执行工作的环境

	$schedule->command('foo')->monthly()->environments('production');

#### 指定工作在当应用程序处于维护模式也应该执行

	$schedule->command('foo')->monthly()->evenInMaintenanceMode();

#### 只允许工作在闭包回传 true 的时候执行

	$schedule->command('foo')->monthly()->when(function()
	{
		return true;
	});
