# Installation

- [Install Composer](#install-composer)
- [Install Laravel](#install-laravel)
- [Server Requirements](#server-requirements)

<a name="install-composer"></a>
## Install Composer

Laravel utilizes [Composer](http://getcomposer.org) to manage its dependencies. So, before using Laravel, you will need to make sure you have Composer installed on your machine.

<a name="install-laravel"></a>
## Install Laravel

### Via Laravel Installer

First, download the Laravel installer using Composer.

	composer global require "laravel/installer=~1.1"

Make sure to place the `~/.composer/vendor/bin` directory in your PATH so the `laravel` executable can be located by your system.

Once installed, the simple `laravel new` command will create a fresh Laravel installation in the directory you specify. For instance, `laravel new blog` would create a directory named `blog` containing a fresh Laravel installation with all dependencies installed. This method of installation is much faster than installing via Composer:

	laravel new blog

### Via Composer Create-Project

You may also install Laravel by issuing the Composer `create-project` command in your terminal:

	composer create-project laravel/laravel {directory} "5.0.*" --prefer-dist

Once installed, you should upgrade to the latest packages. First, remove `{directory}/vendor/compiled.php` file then change your current directory to `{directory}` and issue `composer update` command.

### Scaffolding

Laravel ships with scaffolding for user registration and authentication. If you would like to remove this scaffolding, use the `fresh` Artisan command:

	php artisan fresh

<a name="server-requirements"></a>
## Server Requirements

The Laravel framework has a few system requirements:

- PHP >= 5.4, PHP < 7
- Mcrypt PHP Extension
- OpenSSL PHP Extension
- Mbstring PHP Extension
- Tokenizer PHP Extension

As of PHP 5.5, some OS distributions may require you to manually install the PHP JSON extension. When using Ubuntu, this can be done via `apt-get install php5-json`.

<a name="configuration"></a>
## Configuration

The first thing you should do after installing Laravel is set your application key to a random string. If you installed Laravel via Composer, this key has probably already been set for you by the `key:generate` command.

Typically, this string should be 32 characters long. The key can be set in the `.env` environment file. **If the application key is not set, your user sessions and other encrypted data will not be secure!**

Laravel needs almost no other configuration out of the box. You are free to get started developing! However, you may wish to review the `config/app.php` file and its documentation. It contains several options such as `timezone` and `locale` that you may wish to change according to your application.

Once Laravel is installed, you should also [configure your local environment](/docs/{{version}}/configuration#environment-configuration).

> **Note:** You should never have the `app.debug` configuration option set to `true` for a production application.

<a name="permissions"></a>
### Permissions

Laravel may require some permissions to be configured: folders within `storage` and `vendor` require write access by the web server.

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

Of course, when using [Homestead](/docs/{{version}}/homestead), pretty URLs will be configured automatically.
