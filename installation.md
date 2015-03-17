# Installation

- [Install Composer](#install-composer)
- [Install Laravel](#install-laravel)
- [Server Requirements](#server-requirements)
- [Configuration](#configuration)
- [Pretty URLs](#pretty-urls)

<a name="install-composer"></a>
## Install Composer

Laravel utilizes [Composer](http://getcomposer.org) to manage its dependencies. First, download a copy of the `composer.phar`. Once you have the PHAR archive, you can either keep it in your local project directory or move to `usr/local/bin` to use it globally on your system. On Windows, you can use the Composer [Windows installer](https://getcomposer.org/Composer-Setup.exe).

<a name="install-laravel"></a>
## Install Laravel

### Via Laravel Installer

First, download the Laravel installer using Composer.

	composer global require "laravel/installer=~1.1"

Make sure to place the `~/.composer/vendor/bin` directory in your PATH so the `laravel` executable is found when you run the `laravel` command in your terminal.

Once installed, the simple `laravel new` command will create a fresh Laravel installation in the directory you specify. For instance, `laravel new blog` would create a directory named `blog` containing a fresh Laravel installation with all dependencies installed. This method of installation is much faster than installing via Composer.

### Via Composer Create-Project

You may also install Laravel by issuing the Composer `create-project` command in your terminal:

	composer create-project laravel/laravel {directory} 4.2 --prefer-dist

### Via Download

Once Composer is installed, download the [4.2 version](https://github.com/laravel/laravel/archive/v4.2.11.zip) of the Laravel framework and extract its contents into a directory on your server. Next, in the root of your Laravel application, run the `php composer.phar install` (or `composer install`) command to install all of the framework's dependencies. This process requires Git to be installed on the server to successfully complete the installation.

If you want to update the Laravel framework, you may issue the `php composer.phar update` command.

<a name="server-requirements"></a>
## Server Requirements

The Laravel framework has a few system requirements:

- PHP >= 5.4
- MCrypt PHP Extension

As of PHP 5.5, some OS distributions may require you to manually install the PHP JSON extension. When using Ubuntu, this can be done via `apt-get install php5-json`.

<a name="configuration"></a>
## Configuration

The first thing you should do after installing Laravel is set your application key to a random string. If you installed Laravel via Composer, this key has probably already been set for you by the `key:generate` command. Typically, this string should be 32 characters long. The key can be set in the `app.php` configuration file. **If the application key is not set, your user sessions and other encrypted data will not be secure.**

Laravel needs almost no other configuration out of the box. You are free to get started developing! However, you may wish to review the `app/config/app.php` file and its documentation. It contains several options such as `timezone` and `locale` that you may wish to change according to your application.

Once Laravel is installed, you should also [configure your local environment](/docs/4.2/configuration#environment-configuration). This will allow you to receive detailed error messages when developing on your local machine. By default, detailed error reporting is disabled in your production configuration file.

> **Note:** You should never have `app.debug` set to `true` for a production application. Never, ever do it.

<a name="permissions"></a>
### Permissions
Laravel may require one set of permissions to be configured: folders within `app/storage` require write access by the web server.

<a name="paths"></a>
### Paths

Several of the framework directory paths are configurable. To change the location of these directories, check out the `bootstrap/paths.php` file.

<a name="pretty-urls"></a>
## Pretty URLs

### Apache

The framework ships with a `public/.htaccess` file that is used to allow URLs without `index.php`. If you use Apache to serve your Laravel application, be sure to enable the `mod_rewrite` module.

If the `.htaccess` file that ships with Laravel does not work with your Apache installation, try this one:

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]

### Nginx

On Nginx, the following directive in your site configuration will allow "pretty" URLs:

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
