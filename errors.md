# 错误与日志

- [设置](#configuration)
- [错误处理](#handling-errors)
- [HTTP 例外](#http-exceptions)
- [日志](#logging)

<a name="configuration"></a>
## 设置

应用程序的日志功能设置在 `Illuminate\Foundation\Bootstrap\ConfigureLogging` 启动类别中。这个类别使用 `config/app.php` 设置档的 `log` 设置选项。

日志工具默认使用每天的日志文件；然而，你可以依照需求客制化这个行为。因为 Laravel 使用受欢迎的 [Monolog](https://github.com/Seldaek/monolog) 日志函式库，你可以利用很多 Monolog 提供的处理进程。

例如，如果你想要使用单一日志档，而不是每天一个日志档，你可以对 `config/app.php` 设置档做下面的变更：

	'log' => 'single'

Laravel 提供立即可用的 `single` 、 `daily` 和 `syslog` 日志模式。然而，你可以借由覆写 `ConfigureLogging` 启动类别，依照需求自由地客制化应用程序的日志。

### 错误细节

`config/app.php` 设置档的 `app.debug` 设置选项控制应用程序透过浏览器显示错误细节。设置选项默认参照 `.env` 文件的 `APP_DEBUG` 环境变量。

进行本地开发时，你应该设置 `APP_DEBUG` 环境变量为 `true` 。 **在上线环境，这个值应该永远为 `false` 。**

<a name="handling-errors"></a>
## 错误处理

所有的例外都由 `App\Exceptions\Handler` 类别处理。这个类别包含两个方法： `report` 和 `render` 。

`report` 方法用来纪录例外或把例外传递到外部服务，例如： [BugSnag](https://bugsnag.com) 。默认情况下， `report`  方法只基本实作简单地传递例外到父类别并于父类别纪录例外。然而，你可以依你所需自由地纪录例外。如果你需要使用不同的方法来回报不同类型的例外，你可以使用 PHP 的 `instanceof` 比较运算子：

	/**
	 * 回报或纪录例外。
	 *
	 * 这是一个送例外到 Sentry、Bugsnag 等服务的好地方。
	 *
	 * @param  \Exception  $e
	 * @return void
	 */
	public function report(Exception $e)
	{
		if ($e instanceof CustomException)
		{
			//
		}

		return parent::report($e);
	}

`render` 方法负责把例外转换成应该被传递回浏览器的 HTTP 回应。默认情况下，例外会被传递到基底类别并帮你产生回应。然而，你可以自由的检查例外类型或回传客制化的回应。

例外处理进程的 `dontReport` 属性是个数组，包含应该不要被纪录的例外类型。由 404 错误导致的例外默认不会被写到日志档。你可以依照需求添加其他类型的例外到这个数组。

<a name="http-exceptions"></a>
## HTTP 例外

有一些例外是描述来自服务器的 HTTP 错误码。例如，这可能是个「找不到页面」错误 (404)、「未授权错误」(401)，或甚至是工程师导致的 500 错误。使用下面的方法来回传这样一个回应：

	abort(404);

或是你可以选择提供一个回应：

	abort(403, 'Unauthorized action.');

你可以在请求的生命周期中任何时间点使用这个方法。

### 客制化 404 错误页面

要让所有的 404 错误回传客制化的视图，请建立一个 `resources/views/errors/404.blade.php` 文件。应用程序将会使用这个视图处理所有发生的 404 错误。

<a name="logging"></a>
## 日志

Laravel 日志工具在强大的 [Monolog](http://github.com/seldaek/monolog) 函式库上提供一层简单的功能。Laravel 默认为应用程序建立每天的日志档在 `storage/logs` 目录。你可以像这样把信息写到日志：

	Log::info('This is some useful information.');

	Log::warning('Something could be going wrong.');

	Log::error('Something is really going wrong.');

日志工具提供定义在 [RFC 5424](http://tools.ietf.org/html/rfc5424)  的七个级别：**debug**、**info**、**notice**、**warning**、**error**、**critical** 和 **alert**。

也可以传入上下文相关的数据数组到日志方法里：

	Log::info('Log message', ['context' => 'Other helpful information']);

Monolog 有很多其他的处理方法可以用在日志上。如有需要，你可以取用 Laravel 底层使用的 Monolog 实例：

	$monolog = Log::getMonolog();

你也可以注册事件来捕捉所有传到日志的消息：

#### 注册日志事件监听器

	Log::listen(function($level, $message, $context)
	{
		//
	});
