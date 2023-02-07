# Laravel Pennant

- [Introduction](#introduction)
- [Database Migrations](#database-migrations)

<a name="introduction"></a>
## Introduction

[Laravel Pennant](https://github.com/laravel/pennant) is a simple and lightweight feature flagging package, without the fluff. Feature flags enable you to incrementally roll out new application features with confidence, A/B test new interface designs, compliment a trunk-based development strategy, and much much more.

<a name="installation"></a>
### Installation

First, install Pennant into your project using the Composer package manager:

```shell
composer require laravel/pennant
```

## Database Migrations

Pennant's service provider registers its own database migration directory, so remember to migrate your database after installing the package. The migrations will create a `features` table to power Pennant's database driver:

```shell
php artisan migrate
```

If you need to overwrite the migrations that are included with Pennant, you can publish them using the `vendor:publish` Artisan command:

```shell
php artisan vendor:publish --tag=pennant-migrations
```
