# 设置

- [简介](#introduction)
- [完成安装后](#after-installation)
- [取得设置值](#accessing-configuration-values)
- [环境设置](#environment-configuration)
- [设置缓存](#configuration-caching)
- [维护模式](#maintenance-mode)
- [优雅链结](#pretty-urls)

<a name="introduction"></a>
## 简介

所有 Laravel 框架的设置文件都放置在 `config` 目录下。 每个选项都有说明，因此你可以轻松地浏览这些文档，并且熟悉这些选项配置。

<a name="after-installation"></a>
## 完成安装后

### 命名你的应用程序

在安装完成 Laravel 后，你可以「命名」你的应用程序。 缺省情况下，`app` 的目录是命名在 `App` 下，透过 Composer 使用 [PSR-4 autoloading standard](http://www.php-fig.org/psr/psr-4/) 自动加载。不过，你可以轻松地透过 Artisan 指令 `app:name` 来修改命名空间，以配合你的应用程序名称。

举例来说，假设你的应用程序叫做「 Horsefly 」，你可以从安装的根目录执行下面的指令：

	php artisan app:name Horsefly

重命名你的应用程序是完全自由的，如果你希望的话也可以保持命名空间为 `App` 。

### 其他设置

Laravel 几乎不需设置就可以马上使用。你可以自由的开始开发！然而，你可以浏览 `config/app.php` 文件和其他的文档。你可能希望依据你的本机而做更改，文件包含数个选项如`时区`和`语言环境`。

一旦 Laravel 安装完成，你应该同时 [设置本机环境](/docs/5.0/configuration#environment-configuration)。

> **注意：** 你不应该在正式环境中将 `app.debug` 设置为 `true` 。绝对！千万不要！

<a name="permissions"></a>
### 权限

Laravel 框架有一个目录需要额外设置权限：`storage` 目录必须让服务器有写入权限。

<a name="accessing-configuration-values"></a>
## 取得设置值

你可以很轻松的使用 `Config` facade 取得你的设置值：

	$value = Config::get('app.timezone');

	Config::set('app.timezone', 'America/Chicago');

你也可以使用 `config` 辅助方法：

	$value = config('app.timezone');

<a name="environment-configuration"></a>
## 环境设置

通常应用程序常常需要根据不同的执行环境而有不同的设置值。例如，你会希望在你的本机开发环境上会有与正式环境不同的暂存驱动（cache driver），透过设置文件，就可以轻松完成。

Laravel 透过 [DotEnv](https://github.com/vlucas/phpdotenv) PHP library by Vance Lucas。 在全新安装好的 Laravel 里，你的应用程序的根目录下会包含一个 `.env.example` 文件。如果你透过 Composer 安装 Laravel，这个文件将自动被命名为 `.env`，不然你应该手动更改文件名。

当你的应用程序收到请求，这个文件所有的变量会被加载到 `$_ENV` PHP 超级全域变量里。你可以使用辅助方法 `env` 查看这些变量。事实上，如果你检阅过 Laravel 设置文件，你会注意到几个选项已经在使用这个辅助方法！

根据你的本机服务器或者上线环境需求，你可以自由的修改你的环境变量。然而， 你的 `.env`  文件不应该被提交到应用程序的版本控制系统，因为每个开发人员或服务器使用你的应用程序可能需要不同的环境设置。

如果你是一个团队的开发者，不妨将 `.env.example` 文件包含到你的应用程序。透过范例设置档里的预留值，你的团队中其他开发人员可以清楚地看到执行你的应用程序所需的哪些环境变量。

#### 取得目前应用程序的环境

你可以透过 `Application` 实例中的 `environment` 方法取得目前应用程序的环境：

	$environment = $app->environment();

你也可以传递参数至 `environment` 方法中，来确认目前的环境是否与参数相符合：

	if ($app->environment('local'))
	{
		// The environment is local
	}

	if ($app->environment('local', 'staging'))
	{
		// The environment is either local OR staging...
	}

如果想取得应用程序的实例，可以透过[服务容器](/docs/5.0/container)的 `Illuminate\Contracts\Foundation\Application`  contract 来取得。当然，如果你想在[服务提供者](/docs/5.0/providers)中使用，应用程序实例可以透过实例变量 `$this->app` 取得。

也能透过 `App` facade 的辅助方法 `app` 取得应用程序实例：

	$environment = app()->environment();

	$environment = App::environment();

<a name="configuration-caching"></a>
## 设置缓存

为了让你的的应用程序提升一些速度，你可以使用 Artisan 指令 `config:cache`  将所有的设置档暂存到单一文件。透过指令会将所有的设置选项合并成一个文件，让框架能够快速加载。

通常来说，你应该将执行 `config:cache` 指令作为部署工作的一部分。

<a name="maintenance-mode"></a>
## 维护模式

当你的应用程序处于维护模式时，所有的路由都会指向一个自定的视图。当你要更新或进行维护作业时，「关闭」整个网站是很简单的。维护模式会检查包含在应用程序的缺省中介层堆叠。如果应用程序处于维护模式，`HttpException` 会抛出 503 的状态码。

启用维护模式，只需要执行 Artisan 指令 `down`：

	php artisan down

关闭维护模式，请使用 Artisan 指令 `up`：

	php artisan up

### 维护模式的回应模板

维护模式回应的缺省模板放在 `resources/views/errors/503.blade.php`。

### 维护模式与队列

当应用程序处于维护模式中，将不会处理任何[队列工作](/docs/5.0/queues)。所有的队列工作将会在应用程序离开维护模式后继续被进行。

<a name="pretty-urls"></a>
## 优雅链结

### Apache

Laravel 框架透过 `public/.htaccess` 文件来让网址中不需要 `index.php`。如果你的服务器是使用，请确认是否有开启 `mod_rewrite` 模块。

假设 Laravel 附带的 `.htaccess` 档在 Apache 无法作用的话，请尝试下面的方法：

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]

### Nginx

若使用 Nginx ，可以在你的网站设置中增加下面的设置，以开启「优雅链接」：

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

当然，如果你使用 [Homestead](/docs/5.0/homestead) 的话，优雅链结会自动的帮你设置完成。
