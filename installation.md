# Installation

## Install Composer

Laravel utilizes [Composer](http://getcomposer.org) to manage its dependencies. First, download a copy of the `composer.phar`. Once you have the PHAR archive, you can either keep it in your local project directory or move to `usr/local/bin` to use it globally on your system. On Windows, you can use the Composer [Windows installer](https://getcomposer.org/Composer-Setup.exe).

## Install Laravel

Once Composer is installed, download the [latest version](https://github.com/laravel/laravel/archive/4.0.zip) of the Laravel framework and extract its contents into a directory on your server. Next, in the root of your Laravel application, run the `php composer.phar install` command to install all of the framework's dependencies.

## Configuration

Laravel needs almost no configuration out of the box. You are free to get started developing! However, you may wish to review the `app/config/app.php` file and its documentation. It contains several options such as `timezone` and `locale` that you may wish to change according to your application.

> **Note:** One configuration option you should be sure to set is the `key` option within `app/config/app.php`. This value should be set to a 32 character, random sring. This key is used when encrypting values, and encrypted values will not be safe until it is properly set.