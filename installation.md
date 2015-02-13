# Installation

- [安装 Composer](#install-composer)
- [安装 Laravel](#install-laravel)
- [环境需求](#server-requirements)

<a name="install-composer"></a>
## 安装 Composer

Laravel 框架使用 [Composer](http://getcomposer.org) 来管理其相依性。所以，在你使用 Laravel 之前，你必须确认你在你电脑上是否安装了 Composer。

<a name="install-laravel"></a>
## 安装 Laravel

### 透过 Laravel 安装工具

首先，使用 Composer 下载 Laravel 安装包：

	composer global require "laravel/installer=~1.1"

请确定把 `~/.composer/vendor/bin` 路径放置于您的 `PATH` 里， 这样 `laravel` 执行档就会存在你的系统。

一旦安装完成后，就可以使用 `laravel new` 指令建立一份全新安装的 `Laravel` 专案，例如： `laravel new blog` 将会在当前目录下建立一个叫 `blog` 的目录， 此目录里面存放着全新安装的 Laravel 相关代码，此方法跟其他方法不一样的地方在于是提前安装好所有相关代码，不需要再透过 `composer install` 安装，速度变快许多。

	laravel new blog

### 透过 Composer Create-Project

你一样可以透过 Composer 在命令行执行 `create-project` 来安装 Laravel：

	composer create-project laravel/laravel --prefer-dist

<a name="server-requirements"></a>
## 环境需求

Laravel 框架有一些系统上的需求：

- PHP >= 5.4
- Mcrypt PHP Extension
- OpenSSL PHP Extension
- Mbstring PHP Extension

在 PHP 5.5 之后， 有些操作系统需要手动安装 PHP JSON 套件。如果你是使用 Ubuntu，可以透过 `apt-get install php5-json` 来进行安装。

<a name="configuration"></a>
## 设置

在你安装完 Laravel 后，首先需要做的事情是设置一个随机字串到应用程序密钥。假设你安装 Laravel 是透过 Composer，这个密钥会透过 `key:generate` 指令帮你设置完成。

通常这个密钥应该有 32 字符长。这个密钥可以被设置在 `.env` 环境文件中。 **如果这要密钥没有被设置的话，你的用户 sessions 和其他的加密数据都是不安全的！**

Laravel 几乎不需设置就可以马上使用。你可以自由的开始开发！然而，你可以查看 `config/app.php` 文件和其他的文档。你可能希望依据你的应用程序而做更改，文件包含数个选项如 `时区` 和 `语言环境`。

一旦 Laravel 安装完成，你应该同时 [设置本地环境](/docs/5.0/configuration#environment-configuration)。

> **注意：** 你不应该在正式环境中将 `app.debug` 设置为 `true`。绝对！千万不要！

<a name="permissions"></a>
### 权限

Laravel 框架有一个目录需要额外设置权限：`storage` 要让服务器有写入的权限。

<a name="pretty-urls"></a>
## 优雅链结

### Apache

Laravel 框架透过 `public/.htaccess` 文件来让网址中不需要 `index.php`。如果你网页服务器是使用 Apache 的话，请确认是否有开启 `mod_rewrite` 模块。

假设 Laravel 附带的 `.htaccess` 档在 Apache无法作用的话，请尝试下面的方法：

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]

### Nginx

在 Nginx，在你的网站设置增加下面的设置，可以使用「优雅链结」：

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

当然，如果你使用 [Homestead](/docs/5.0/homestead) 的话，优雅链结会自动的帮你设置完成。
