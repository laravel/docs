# 安装

- [安装Composer](#install-composer)
- [安装Laravel](#install-laravel)
- [服务器环境要求](#server-requirements)
- [配置](#configuration)
- [优雅链接](#pretty-urls)

<a name="install-composer"></a>
## 安装Composer

Laravel框架使用[Composer](http://getcomposer.org)（PHP包管理工具）来管理代码依赖性。
首先，你需要下载Composer的PHAR打包文件（ `composer.phar` ），下载完成后把它放在项目目录下或者放到 `usr/local/bin` 目录下以便在系统中全局调用。在Windows操作系统中，你可以使用Composer的[Windows安装工具](https://getcomposer.org/Composer-Setup.exe)。

<a name="install-laravel"></a>
## 安装Laravel

Composer安装完成后，下载[最新版Laravel框架](https://github.com/laravel/laravel/archive/master.zip)，把它解压缩到你服务器上的一个目录中。然后在Laravel应用的根目录下运行命令行命令 `php composer.phar install` （或者 `composer install` ）来安装所有的框架依赖包。在此过程中，为了成功完成安装，你需要在服务器上安装好Git。

当Laravel框架安装好后，你可以使用命令行命令 `php composer.phar update` 来更新框架。

<a name="server-requirements"></a>
## 服务器环境要求

Laravel框架有一些系统要求：

- PHP最低版本： 5.3.7
- MCrypt PHP扩展

<a name="configuration"></a>
## 配置


Laravel框架几乎无需配置就可立即使用。你可以自由地快速开始开发。然而，你也许希望先查看下 `app/config/app.php` 配置文件和相关的文档说明。它包含了一些你也许要修改的配置选项，如 `时区` 和 `地区` 等。

> **注意：** 在 `app/config/app.php` 文件中有一项你需要确认设置的选项就是 `key` 选项。它的值应该是一个32位长度的随机字符串。这个 `key` 选项是用来加密的，为了确保安全你需要正确设置它的值。你可以使用如下 artisan 命令快速设置这个值，`php artisan key:generate`。

<a name="permissions"></a>
### 权限设置
Laravel框架有一处需要设置权限 —— app/storage 目录下的文件需要服务器上的写权限。

<a name="paths"></a>
### 路径设置

一些框架目录路径是可以设置的。如果需要改变这些目录的位置，可以查看 `bootstrap/paths.php` 文件中的设置。

> **注意：** 作为Laravel框架保护项目代码的设计，本地存储中只有 public 目录需要公开访问。推荐将 public 目录设置为文档根目录（documentRoot，又称web root网站根目录）或者把 public 目录放置在网站可访问目录下，把所有其他的目录放到网站可访问目录之外。

<a name="pretty-urls"></a>
## 优雅链接

Laravel框架通过设置 `public/.htaccess` 文件去除链接中的`index.php`。 如果你你的服务器使用的是Apache，请开启`mod_rewrite` 模块。

如果框架附带的 `.htaccess` 文件在你的Apache环境中不起作用，请尝试下面这个版本：

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteRule ^(.+)/$ http://%{HTTP_HOST}/$1 [R=301,L]

	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]
