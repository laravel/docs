# Installation

- [Install Composer](#install-composer)
- [Install Laravel](#install-laravel)
- [Server Requirements](#server-requirements)
- [Configuration](#configuration)
- [Pretty URLs](#pretty-urls)

<a name="install-composer"></a>
## Install Composer

Laravel uses Composer for dependencies. To install Composer on **Mac or Linux**,

1. Get `composer.phar` from the [official website](http://getcomposer.org/).

2. Place it in your /usr/bin/local (or in your project's root directory).

3. Rename the file to simply `composer`.

On **Windows**, use [this installer](https://getcomposer.org/Composer-Setup.exe).

<a name="install-laravel"></a>
## Install Laravel

There's more than one way to install Laravel. Via installer, Composer or download.

### Via Laravel Installer

The Laravel Installer is a simple command-line tool used to build the Laravel environment on your system. It's helpful for creating multiple Laravel projects without heving to go to the web for files each time, and is faster than Composer. To use it on **Mac and Linux**,

1. Download the [Laravel installer](http://laravel.com/laravel.phar). 

2. Rename the file to `laravel` and move it to `/usr/local/bin`. 

3. Open Terminal and enter `laravel new`, followed by a directory, create a fresh Laravel installation. For instance, `laravel new blog` would create a directory named `blog` containing a fresh Laravel installation with all dependencies installed.

### Via Composer Create-Project

You may also install Laravel by issuing the Composer `create-project` command in your terminal:

	composer create-project laravel/laravel --prefer-dist

### Via Download

Laravel files can be downloaded manually, but you must still use Composer to get the dependencies (or manually get them yourself). This method also requires Git.

1. Make sure Composer is installed (see Install Composer above).

2. Download the [latest version](https://github.com/laravel/laravel/archive/master.zip) of Laravel and extract it to your project folder. 

3. In the root of your Laravel project, run `php composer install` (or `composer install`) to install all of the framework's dependencies.

4. If you want to update the Laravel framework, run `php composer update`
<a name="server-requirements"></a>
## Server Requirements

The Laravel framework has a few system requirements:

- PHP >= 5.4
- MCrypt PHP Extension
- Composer (for installation)
- Git (for installation)

As of PHP 5.5, some OS distributions may require you to manually install the PHP JSON extension. For Ubuntu, try `apt-get install php5-json`.

<a name="configuration"></a>
## Configuration

Laravel is capable of multiple different configurations for different environments (development, production, testing, etc). While Laravel should work right away using the global configurations, you should set up your envrionments using the `app/config` subfolders, such as `local` and `testing`. You can switch your active environment using the `artisan` application. See [configure your local environment](/docs/configuration#environment-configuration) for more information.

> **Note:** You should never have `app.debug` set to `true` for a production application.

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
