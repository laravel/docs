# Installation

- [Install Composer](#install-composer)
- [Install Laravel](#install-laravel)
- [Server Requirements](#server-requirements)

<a name="install-composer"></a>
## Install Composer

Laravel utilizes [Composer](http://getcomposer.org) to manage its dependencies. First, download a copy of the `composer.phar`. Once you have the PHAR archive, you can either keep it in your local project directory or move to `usr/local/bin` to use it globally on your system. On Windows, you can use the Composer [Windows installer](https://getcomposer.org/Composer-Setup.exe).

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

	composer create-project laravel/laravel --prefer-dist

<a name="server-requirements"></a>
## Server Requirements

The Laravel framework has a few system requirements:

- PHP >= 5.4
- mcrypt PHP Extension
- mbstring PHP Extension

> **Note:** As of PHP 5.5, some OS distributions may require you to manually install the PHP JSON extension. When using Ubuntu, this can be done via `apt-get install php5-json`.
