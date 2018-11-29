# Laravel Telescope

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
    - [Data Pruning](#data-pruning)
- [Dashboard Authorization](#dashboard-authorization)

<a name="introduction"></a>
## Introduction

Laravel Telescope is an elegant debug assistant for the Laravel framework. Telescope provides insight into the requests coming into your application, exceptions, log entries, database queries, queued jobs, mail, notifications, cache operations, scheduled tasks, variable dumps and more. Telescope makes a wonderful companion to your local Laravel development environment.

<p align="center">
<img src="https://res.cloudinary.com/dtfbvvkyp/image/upload/v1539110860/Screen_Shot_2018-10-09_at_1.47.23_PM.png" width="600" height="347">
</p>

<a name="installation"></a>
## Installation

> {note} Telescope requires Laravel 5.7.7+.

You may use Composer to install Telescope into your Laravel project:

    composer require laravel/telescope

After installing Telescope, publish its assets using the `telescope:install` Artisan command. After installing Telescope, you should also run the `migrate` command:

    php artisan telescope:install

    php artisan migrate

#### Updating Telescope

When updating Telescope, you should re-publish Telescope's assets:

    php artisan telescope:publish

### Installing Only In Specific Environments

If you plan to only use Telescope to assist your local development. You may install Telescope using the `--dev` flag:

    composer require laravel/telescope --dev

After running `telescope:install`, you should remove the `TelescopeServiceProvider` service provider registration from your `app` configuration file. Instead, manually register the service provider in the `register` method of your `AppServiceProvider`:

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        if ($this->app->isLocal()) {
            $this->app->register(TelescopeServiceProvider::class);
        }
    }

<a name="configuration"></a>
### Configuration

After publishing Telescope's assets, its primary configuration file will be located at `config/telescope.php`. This configuration file allows you to configure your watcher options and each configuration option includes a description of its purpose, so be sure to thoroughly explore this file.

If desired, you may disable Telescope's data collection entirely using the `enabled` configuration option:

    'enabled' => env('TELESCOPE_ENABLED', true),

<a name="data-pruning"></a>
### Data Pruning

Without pruning, the `telescope_entries` table can accumulate records very quickly. To mitigate this, you should schedule the `telescope:prune` Artisan command to run daily:

    $schedule->command('telescope:prune')->daily();

By default, all entries older than 24 hours will be pruned. You may use the `hours` option when calling the command to determine how long to retain Telescope data. For example, the following command will delete all records created over 48 hours ago:

    $schedule->command('telescope:prune --hours=48')->daily();

<a name="dashboard-authorization"></a>
## Dashboard Authorization

Telescope exposes a dashboard at `/telescope`. By default, you will only be able to access this dashboard in the `local` environment. Within your `app/Providers/TelescopeServiceProvider.php` file, there is a `gate` method. This authorization gate controls access to Telescope in **non-local** environments. You are free to modify this gate as needed to restrict access to your Telescope installation:

    /**
     * Register the Telescope gate.
     *
     * This gate determines who can access Telescope in non-local environments.
     *
     * @return void
     */
    protected function gate()
    {
        Gate::define('viewTelescope', function ($user) {
            return in_array($user->email, [
                'taylor@laravel.com',
            ]);
        });
    }
