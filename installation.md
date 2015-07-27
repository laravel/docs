# 安装

- [安装](#installation)
- [配置](#configuration)
    - [基本配置](#basic-configuration)
    - [环境配置](#environment-configuration)
    - [配置缓存](#configuration-caching)
    - [获取配置项](#accessing-configuration-values)
    - [应用程序命名](#naming-your-application)
- [维护模式](#maintenance-mode)

<a name="installation"></a>
## 安装

### 服务器要求

Laravel 框架对系统有一些要求. 当然, 如果使用 [Laravel Homestead](/docs/{{version}}/homestead) 虚拟机已经满足这些要求。

<div class="content-list" markdown="1">
- PHP >= 5.5.9
- OpenSSL PHP Extension
- PDO PHP Extension
- Mbstring PHP Extension
- Tokenizer PHP Extension
</div>

<a name="install-laravel"></a>
### 安装 Laravel

Laravel 使用 [Composer](http://getcomposer.org/) 来管理依赖关系。因此，在使用 Laravel 前，请确认 Composer 已安装在你的计算机上。

#### 通过 Laravel 安装程序

首先, 通过 Composer 下载 Laravel 安装程序:

    composer global require "laravel/installer=~1.1"

请确保 `~/.composer/vendor/bin` 目录在你的 `PATH` 中。这样，Laravel 可执行文件才会被系统定位并执行。

一但安装后, 你可以使用一个简单的命令 `laravel new` 来创建一个全新的 Laravel 在你指定的目录中。例如，`laravel new blog` 将创建一个名为 `blog` 的目录，并在该目录中创建一个全新安装的 Laravel，并且，所有 Laravel 的依赖已被安装。这个方法比通过 Composer 安装更快:

    laravel new blog

#### 通过 Composer 创建项目

你也可以通过 Composer 的 `create-project` 命令来安装 Laravel:

    composer create-project laravel/laravel --prefer-dist

<a name="configuration"></a>
## 配置

<a name="basic-configuration"></a>
### 基本配置

所有配置文件都储存在 Laravel 框架的 `config` 目录中。每个选项都有注释，因此你可以轻松的阅读并且熟悉这些配置项。

#### 目录权限

安装 Laravle 后，你可能需要配置一些权限。目录内的 `storage` 和 `bootstrap/cache` 目录在你的 Web 服务器中应有写权限。如果你使用 [Homestead](/docs/{{version}}/homestead) 虚拟机，那么相关的权限已配置好。

#### 应用密钥

安装完 Laravel 后，你应该设置一个随机字符串作为应用密钥。如果你是通过 Composer 或 Laravel 安装程序进行安装的，这个密钥已通过 `key:generate` 命令被设置。通常，这个字符串长度应该为 32 位。这个密钥被设置在 `.env` 环境配置文件中。如果你还没有将 `.env.example` 重命名为 `.env`，那你现在应该去改名。**如果应用密钥没有被设置，那么你的用户 Session 与其他加密数据将不会是安全的！**

#### 其他配置

Laravel 安装后几乎不需要任何配置即可开始使用。你可以立即开始进行开发！然而，你不妨去查看 `config/app.php` 文件与其中的选项说明。它包含了几个选项，例如 `timezone` 和 `locale`。你可以根据你自己的需求来更改它们。

你也可能希望更改一些其他 Laravel 组件的配置，例如:

- [Cache](/docs/{{version}}/cache#configuration)
- [Database](/docs/{{version}}/database#configuration)
- [Session](/docs/{{version}}/session#configuration)

一旦 Laravel 被安装，你同样应该配置你的 [环境配置](/docs/{{version}}/installation#environment-configuration)

<a name="pretty-urls"></a>
#### 优雅链接

**Apache**

框架自带了 `public/.htaccess` 文件，它将允许 URLs 中省略 `index.php`。如果你的 Laravel 应用运行在 Apache 上，请确认启用了 `mod_rewrite` 模块。

如果这个 `.htaccess` 不起作用，你可以尝试如下:

    Options +FollowSymLinks
    RewriteEngine On

    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteRule ^ index.php [L]

**Nginx**

在 Nginx 中，以下配置将允许你使用优雅链接：

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

当然，在使用 [Homestead](/docs/{{version}}/homestead) 时，优雅链接已被自动配置好。

<a name="environment-configuration"></a>
### 环境配置

通常应用程序需要根据不同的执行环境有不同的配置选项。例如，你可能希望在你的本机开发环境上与生产服务器环境有不同的缓存驱动，通过环境配置文件，就可以轻松完成。

为了使它更轻松，Laravel 使用了 Vance Lucas 写的 [DotEnv](https://github.com/vlucas/phpdotenv) 类库。在全新安装的 Laravel 中，你应用的根目录下会有一个 `.env.example` 文件，如果你是通过 Composer 安装的 Laravel，这个文件已被自动重命名为 `.env`。如果没有，你应该手动重命名。

当你的应用程序收到请求，这个文件的所有变量将会被加载到 `$_ENV` PHP 超全局变量中。你可以使用 `env` 辅助函数来取出变量的值。事实上，如果你查看 Laravel 配置的文件，你会发现有几个选项已经使用这个辅助方法了！

根据你自己的本地服务器或线上环境需求，你可以轻松地修改你的环境配置，然而，你的 `.env` 文件不应该被提交到应用程序代码的版本控制中，因为每个开发者 / 服务器使用你的应用程序可能需要不同的环境配置。

如果你是一个团队的开发者，不妨将 `.env.example` 文件包含到你的应用。通过在配置文件中预留值，团队中的其他开发人员可以很清楚地看到执行你的应用程序所需的环境变量配置。

#### 获取当前应用环境

当前应用环境是通过 `.env` 文件中的 `APP_ENV` 变量决定的。如果你需要访问当前应用环境，可以通过 `App` [facade](/docs/{{version}}/facades):

    $environment = App::environment();

你也可以传递参数给 `environment` 来确认当前环境是否符合一个指定的值，你也可以传递多个值:

    if (App::environment('local')) {
        // The environment is local
    }

    if (App::environment('local', 'staging')) {
        // The environment is either local OR staging...
    }

一个应用实例也可以被通过 `app` 辅助函数访问到:

    $environment = app()->environment();

<a name="configuration-caching"></a>
### 配置缓存

为了提升你的应用速度，你应该使用 `config:cache` Artisan 命令缓存你所有的配置文件到一个单一文件中。这将合并你应用中的所有配置选项到单一文件中，以便被框架更快的加载。

通常你应该将 `config:cache` 命令作为应用部署时的一个步骤。这个命令在开发环境下不推荐使用，因为在开发流程中配置项会经常的变更。

<a name="accessing-configuration-values"></a>
### 获取配置项

你可以使用 `config` 全局辅助函数很容易地访问你的配置项。这个配置的值可以使用 "点" 语法来访问，其中包括你要访问的配置名，与该配置项所在的文件名。如果配置项不存在，你也可以指定一个默认值来返回:

    $value = config('app.timezone');

要在程序运行时设置一个配置项，需传递一个数组到 `config` 辅助函数:

    config(['app.timezone' => 'America/Chicago']);

<a name="naming-your-application"></a>
### 应用程序命名

在安装 Laravel 后，你可能希望重命名你的应用。默认情况下，`app` 目录下的命名空间为 `App`，且 Compsoer 已经使用 [PSR-4 自动载入标准](http://www.php-fig.org/psr/psr-4/) 来自动加载。然而，你可能会希望将命名空间改成与你应用程序相匹配的名字。你可以很容易地通过 `app:name` Artisan 命令来更改。

例如，如果你的应用被命名为 "Horsefly"，你可以在框架根目录下执行以下命令:

    php artisan app:name Horsefly

重命名你的应用不是必须的。你完全可以保留默认的命名空间 `App`。

<a name="maintenance-mode"></a>
## 维护模式

如果你的应用处于维护模式，当有请求传入时，将显示一个自定义的视图。当你的应用在更新或者维护时，可以方便的做到 "关闭" 站点。默认的中间件中包含了维护模式的检查。如果当前应用处于维护模式，一个 带有  503 状态码 的 `HttpException` 异常将被抛出。

要开启维护模式，你可以简单地使用 `down` Artisan 命令:

    php artisan down

要关闭维护模式，你可以简单地使用 `up` Artisan 命令:

    php artisan up

### 维护模式响应模板

默认的维护模式模板文件位于: `resources/views/errors/503.blade.php`

### 维护模式和队列

当你的应用处于维护模式，将不会有 [队列 Jobs](/docs/{{version}}/queues) 被处理。这些 Jobs 将在应用关闭维护模式后继续正常处理。
