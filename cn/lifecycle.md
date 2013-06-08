# Request的生命周期

- [概述](#overview)
- [启动文件](#start-files)
- [应用程序事件](#application-events)

<a name="overview"></a>
## 概述

Laravel中的request的生命周期相当简单。当一个request进入到你应用程序时，它被调度到适当的路由或控制器。从该路由输出的response将返回到浏览器并显示在屏幕上。有时你想在路由执行之前或后做一些其他处理。有几种办法可以达到该目的，其中两种办法是"start"文件和应用程序事件。

<a name="start-files"></a>
## 启动文件

应用程序的启动文件被存放在`app/start`目录中。默认情况下，该目录下包含三个文件：`global.php`、`local.php` 和 `artisan.php`文件。需要获取更多关于`artisan.php`的信息，可以参考文档[Artisan 命令行](/docs/commands#registering-commands)。

`global.php`启动文件默认包含一些基本项目，例如[Logger](/docs/errors)的注册以及载入`app/filters.php` 文件。然而，你可以在该文件里做任何你想做的事情。无论在什么环境下，它都将会被自动包含进_每一个_request中。而`local.php` 文件仅在`local`环境下被执行。获取更多关于环境的信息，请查看文档[配置](/docs/configuration)。

当然，如果除了`local`环境你还有其他环境的话，你也可以为针对这些环境创建启动文件。这些文件将在应用程序运行在该环境中时被自动包含。


<a name="application-events"></a>
## 应用程序事件

你还可以通过注册 `before`、`after`、`close`、`finish` 和 `shutdown`应用程序事件以便在处理request之前或后做一些操作：

**注册应用程序事件**

	App::before(function()
	{
		//
	});

	App::after(function($request, $response)
	{
		//
	});

上述事件的监听器将会在每个request `之前（before）` 和 `之后（after）`运行 。

译者：王赛  [（Bootstrap中文网）](http://www.bootcss.com)