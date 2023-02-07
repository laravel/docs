# Laravel Pennant

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)

<a name="introduction"></a>
## Introduction

[Laravel Pennant](https://github.com/laravel/pennant) is a simple and lightweight feature flagging package, without the fluff. Feature flags enable you to incrementally roll out new application features with confidence, A/B test new interface designs, compliment a trunk-based development strategy, and much much more.

<a name="installation"></a>
## Installation

First, install Pennant into your project using the Composer package manager:

```shell
composer require laravel/pennant
```

Next, you should publish the Pennant configuration and migration files using the `vendor:publish` Artisan command. The `pennant` configuration file will be placed in your application's `config` directory:

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

Finally, you should run the database migrations. This will create a `features` table that Pennant uses to power the database driver.

```shell
php artisan migrate
```

<a name="configuration"></a>
## Configuration

After publishing Pennant's assets, its configuration file will be located at `config/pennant.php`. This configuration file allows you to configure the default driver and the individual driver options.
