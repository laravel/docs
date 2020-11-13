# Installation

- [Meet Laravel](#meet-laravel)
    - [Why Laravel?](#why-laravel)
- [Your First Laravel Project](#your-first-laravel-project)
    - [Getting Started On macOS](#getting-started-on-macos)
    - [Getting Started On Windows](#getting-started-on-windows)
    - [Getting Started On Linux](#getting-started-on-linux)
    - [Installation Via Composer](#installation-via-composer)
- [Initial Configuration](#initial-configuration)
- [Laravel Sail](#laravel-sail)
    - [Introduction](#laravel-sail-introduction)
    - [Starting & Stopping](#starting-and-stopping-sail)
    - [Executing Commands](#executing-sail-commands)
    - [Interacting With Databases](#interacting-with-sail-databases)
    - [Running Tests](#running-tests)
    - [Adding Additional Services](#adding-additional-sail-services)
    - [Container CLI](#sail-container-cli)
    - [Customization](#sail-customization)
- [Next Steps](#next-steps)
    - [Laravel The Full Stack Framework](#laravel-the-fullstack-framework)
    - [Laravel The API Backend](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## Meet Laravel

Laravel is a web application framework with expressive, elegant syntax. A web framework provides a structure and starting point for creating your application, allowing you to focus on creating something amazing while we sweat the details.

Laravel strives to provide an amazing developer experience, while providing powerful features such as thorough dependency injection, an expressive database abstraction layer, queues and scheduled jobs, unit and integration testing, and more.

Whether your new to PHP or web frameworks or have years of experience, Laravel is a framework that can grow with you. We'll help you take your first steps as a web developer or give you a boost as you take your expertise to the next level. We can't wait to see what you build.

<a name="why-laravel"></a>
### Why Laravel?

There are a variety of tools and frameworks available to you when building a web application. However, we believe Laravel is the best choice for building modern, full-stack web applications.

#### A Progressive Framework

We like to call Laravel a "progressive" framework. By that, we mean that Laravel grows with you. If you're just taking your first steps into web development, Laravel's vast library of documentation, guides, and [video tutorials](https://laracasts.com) will help you learn the ropes without becoming overwhelmed.

If you're a senior developer, Laravel gives you robust tools for [dependency injection](/docs/{{version}}/container), [unit testing](/docs/{{version}}/testing), [queues](/docs/{{version}}/queues), [real-time events](/docs/{{version}}/broadcasting), and more. Laravel is fine-tuned for building professional web applications and ready to handle enterprise work loads.

#### A Scalable Framework

Laravel is incredibly scalable. Thanks to the scaling-friendly nature of PHP and Laravel's built-in support for fast, distributed cache systems like Redis, horizontal scaling with Laravel is a breeze. In fact, Laravel applications have been easily scaled to handle hundreds of millions of requests per month.

Need extreme scaling? Platforms like [Laravel Vapor](https://vapor.laravel.com) allow you to run your Laravel application at nearly limitless scale on AWS's latest serverless technology.

#### A Community Framework

Laravel combines the best packages in the PHP ecosystem to offer the most robust and developer friendly framework available. In addition, thousands of talented developers from around the world have [contributed to the framework](https://github.com/laravel/framework). Who knows, maybe you'll even become a Laravel contributor.

<a name="your-first-laravel-project"></a>
## Your First Laravel Project

We want it to be as easy as possible to get started with Laravel. There are a variety of options for developing and running a Laravel project on your own computer. While you may wish to explore these options at a later time, Laravel provides [Sail](https://github.com/laravel/sail), a built-in solution for running your Laravel project using [Docker](https://www.docker.com).

Docker is a tool for running applications and services in small, light-weight "containers" which do not interfere with your local computer's installed software or configuration. This means you don't have to worry about configuring or setting up complicated development tools such as web servers and databases on your personal computer. To get started, you only need to install [Docker Desktop](https://www.docker.com/products/docker-desktop).

Laravel Sail is a light-weight command-line interface for interacting with Laravel's default Docker configuration. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience.

> {tip} Already a Docker expert? Don't worry! Everything about Sail can be customized using the `docker-compose.yml` file included with Laravel.

<a name="getting-started-on-macos"></a>
### Getting Started On macOS

If you're developing on a Mac and [Docker Desktop](https://www.docker.com/products/docker-desktop) is already installed, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal:

```bash
curl -s https://laravel.build/example-app | bash
```

Of course, you can change `example-app` in this URL to anything you like. The Laravel application's directory will be created within the directory you execute the command from.

After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration:

```bash
cd example-app

./sail up
```

Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. To continue learning more about Laravel Sail, review its [complete documentation](#laravel-sail).

<a name="getting-started-on-windows"></a>
### Getting Started On Windows

Before we create a new Laravel application on your Windows machine, make sure to install [Docker Desktop](https://www.docker.com/products/docker-desktop). Next, you should ensure that Windows Subsystem for Linux 2 (WSL2) is installed and enabled. WSL allows you to run Linux binary executables natively on Windows 10. Information on how to install and enable WSL2 can be found within Microsoft's [developer environment documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

> {tip} After installing and enabling WSL2, you should ensure that Docker Desktop is [configured to use the WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/).

Next, you are ready to create your first Laravel project. Launch [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab) and begin a new terminal session for your WSL2 Linux operating system. Next, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal:

```bash
curl -s https://laravel.build/example-app | bash
```

Of course, you can change `example-app` in this URL to anything you like. The Laravel application's directory will be created within the directory you execute the command from.

After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration:

```bash
cd example-app

./sail up
```

Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. To continue learning more about Laravel Sail, review its [complete documentation](#laravel-sail).

#### Developing Within WSL2

Of course, you will need to be able to modify the Laravel application files that were created within your WSL2 installation. To accomplish this, we recommend using Microsoft's [Visual Studio Code](https://code.visualstudio.com) editor and their first-party extension for [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack).

Once these tools are installed, you may open any Laravel project by executing the `code .` command from your application's root directory using Windows Terminal.

<a name="getting-started-on-linux"></a>
### Getting Started On Linux

If you're developing on Linux and [Docker](https://www.docker.com) is already installed, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal:

```bash
curl -s https://laravel.build/example-app | bash
```

Of course, you can change `example-app` in this URL to anything you like. The Laravel application's directory will be created within the directory you execute the command from.

After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration:

```bash
cd example-app

./sail up
```

Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. To continue learning more about Laravel Sail, review its [complete documentation](#laravel-sail).

<a name="installation-via-composer"></a>
### Installation Via Composer

If your computer already has PHP and Composer installed, you may create a new Laravel project by using Composer directly. After the application has been created, you may start Laravel's local development server using the Artisan CLI's `serve` command:

    composer create-project laravel/laravel example-app

    cd example-app

    php artisan serve

<a name="the-laravel-installer"></a>
#### The Laravel Installer

Or, you may install the Laravel Installer as a global Composer dependency:

    composer global require laravel/installer

    laravel new example-app

    php artisan serve

Make sure to place Composer's system-wide vendor bin directory in your `$PATH` so the `laravel` executable can be located by your system. This directory exists in different locations based on your operating system; however, some common locations include:

<div class="content-list" markdown="1">
- macOS: `$HOME/.composer/vendor/bin`
- Windows: `%USERPROFILE%\AppData\Roaming\Composer\vendor\bin`
- GNU / Linux Distributions: `$HOME/.config/composer/vendor/bin` or `$HOME/.composer/vendor/bin`
</div>

<a name="initial-configuration"></a>
## Initial Configuration

All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you.

Laravel needs almost no additional configuration out of the box. You are free to get started developing! However, you may wish to review the `config/app.php` file and its documentation. It contains several options such as `timezone` and `locale` that you may wish to change according to your application.

<a name="environment-configuration"></a>
#### Environment Based Configuration

Since many of Laravel's configuration option values may vary depending on whether your application is running on your local computer or on a production web server, many important configuration values are defined using the `.env` file that exists at the root of your application.

Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed.

> {tip} For more information about the `.env` file and environment based configuration, check out the full [configuration documentation](/docs/{{version}}/configuration#environment-configuration).

<a name="laravel-sail"></a>
## Laravel Sail

<a name="laravel-sail-introduction"></a>
### Introduction

Laravel Sail is a light-weight command-line interface for interacting with Laravel's default Docker configuration. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience.

At its heart, Sail is the `docker-compose.yml` file and the `sail` script that is stored at the root of your project. The `sail` script provides a CLI with convenient methods for interacting with the Docker containers defined by the `docker-compose.yml` file.

<a name="starting-and-stopping-sail"></a>
### Starting & Stopping

To start all of the Docker containers defined in your `docker-compose.yml` file, you may run the `up` command:

```bash
./sail up
```

Once the application's containers have been started, you may access the project in your web browser at: http://localhost.

To stop all of the containers, you may simply use Control + C to stop the container's execution. Or, if the containers are running in the background, you may use the `down` command:

```bash
./sail down
```

<a name="executing-sail-commands"></a>
### Executing Commands

When using Laravel Sail, your application is executing within a Docker container and is isolated from your local computer. However, Sail provides a convenient way to run various commands against your application, such as arbitrary PHP commands, Artisan commands, Composer commands, and NPM / Node commands:

```bash
./sail php --version

./sail artisan queue:work

./sail composer require laravel/sanctum

./sail node --version

./sail npm run prod
```

**When reading the Laravel documentation, you will often see references to Artisan and Composer commands that do not reference Sail.** Those examples assume that PHP is installed on your local computer. If you are using Sail for your local Laravel development environment, you should execute those commands using Sail:

```bash
// Running Artisan commands locally...
php artisan queue:work

// Running Artisan commands within Laravel Sail...
./sail artisan queue:work
```

<a name="interacting-with-sail-databases"></a>
### Interacting With Databases

<a name="interacting-with-sail-databases-mysql"></a>
#### MySQL

As you may have noticed, your application's `docker-compose.yml` file contains an entry for a MySQL container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your database is persisted even when stopping and restarting your containers. Once you have started your containers, you may connect to the MySQL instance within your application by setting your `DB_HOST` environment variable within your application's `.env` file to `mysql`.

To connect to your application's MySQL database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the MySQL database is accessible at `localhost` port `3306`.

<a name="interacting-with-sail-databases-redis"></a>
#### Redis

Your application's `docker-compose.yml` file also contains an entry for a [Redis](https://redis.io) container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Redis data is persisted even when stopping and restarting your containers. Once you have started your containers, you may connect to the Redis instance within your application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `redis`.

To connect to your application's Redis database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Redis database is accessible at `localhost` port `6379`.

<a name="running-tests"></a>
### Running Tests

Laravel provides amazing testing support out of the box, and you may use Sail's `test` command to run your applications [feature and unit tests](/docs/{{version}}/testing). Any CLI options that are accepted by PHPUnit may also be passed to the `test` command:

    ./sail test

    ./sail test --group orders

The Sail `test` command is equivalent to running the `test` Artisan command:

    ./sail artisan test

<a name="laravel-dusk"></a>
#### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk) provides an expressive, easy-to-use browser automation and testing API. Thanks to Sail, you may run these tests without ever installing Selenium or other tools on your local computer. To get started, uncomment the Selenium service in your application's `docker-compose.yml` file:

    selenium:
        image: 'selenium/standalone-chrome'
        volumes:
            - '/dev/shm:/dev/shm'
        networks:
            - sail

Next, ensure that the `laravel.test` service in your application's `docker-compose.yml` file has a `depends_on` entry for `selenium`:

        depends_on:
            - mysql
            - redis
            - selenium

Finally, you may run your Dusk test suite by starting Sail and running the `dusk` command:

    ./sail dusk

<a name="adding-additional-sail-services"></a>
### Adding Additional Services

Since Laravel Sail is built using a standard `docker-compose.yml` file, you are free to add additional services to your container configuration based on your application's own needs.

<a name="sharing-services-across-projects"></a>
#### Sharing Services Across Projects

Sometimes you may wish to share a single service such as MySQL across multiple projects. To accomplish this, we recommend using [Takeout](https://github.com/tighten/takeout), an open source tool developed by Tighten. After enabling a Takeout service, you should add the `takeout` network to your `laravel.test` container definition within your `docker-compose.yml` file:

```yaml
networks:
    - sail
    - takeout
```

In addition, you will need to add the `takeout` network to the root level `networks` entry in your `docker-compose.yml` file:

```yaml
networks:
    sail:
        driver: bridge
    takeout:
        external:
            name: takeout
```

Once you have added your container to the `takeout` network, you may start Sail:

```bash
./sail up
```

For more information on using Takeout services and connecting them to Sail, please consult the [official Takeout documentation](https://github.com/tighten/takeout).

<a name="sail-container-cli"></a>
### Container CLI

Sometimes you may wish to start a Bash session within your application's container. You may use the `ssh` command to connect to your application's container, allowing you to inspect its file and installed services:

```bash
./sail ssh
```

<a name="sail-customization"></a>
### Sail Customization

Since Sail is just Docker, you are free to customize nearly everything about it. To publish Sail's own Dockerfiles, you may execute the `sail:install` Artisan command and publish the resources exported by the `Laravel\Sail\SailServiceProvider` service provider:

```bash
./sail artisan sail:install
```

After running this command, the Dockerfiles and other configuration files used by Laravel Sail will be placed within a `docker` directory in your application's root directory. After customizing your Sail installation, you may rebuild your application's containers using the `build` command:

```bash
./sail build
```

<a name="next-steps"></a>
## Next Steps

Now that you have created your Laravel project, you may be wondering what to learn next. First, we strongly recommend becoming familiar with how Laravel works by reading the following documentation:

<div class="content-list" markdown="1">
- [Request Lifecycle](/docs/{{version}}/lifecycle)
- [Configuration](/docs/{{version}}/configuration)
- [Directory Structure](/docs/{{version}}/structure)
- [Service Container](/docs/{{version}}/container)
- [Facades](/docs/{{version}}/facades)
</div>

How you want to use Laravel will also dictate the next steps on your journey. There are a variety of ways to use Laravel, and we'll explore two primary use cases for the framework below.

<a name="laravel-the-fullstack-framework"></a>
### Laravel The Full Stack Framework

Laravel may serve as a full stack framework. By "full stack" framework we mean that you are going to use Laravel to route requests to your application and render your frontend via [Blade templates](/docs/{{version}}/blade) or using an single-page application hybrid technology like [Inertia.js](https://inertiajs.com). This is the most common way to use the Laravel framework.

If this is how you plan to use Laravel, you may want to check out our documentation on [routing](/docs/{{version}}/routing), [views](/docs/{{version}}/views), or the [Eloquent ORM](/docs/{{version}}/eloquent). In addition, you might be interested in learning about community packages like [Livewire](https://laravel-livewire.com) and [Inertia.js](https://inertiajs.com). These packages allow you to use Laravel as a full-stack framework while enjoying many of the UI benefits provided by single-page JavaScript applications.

If you are using Laravel as a full stack framework, we also strongly encourage you to learn how to compile your application's CSS and JavaScript using [Laravel Mix](/docs/{{version}}/mix).

> {tip} If you want to get a head start building your application, check out one of our official [application starter kits](/docs/{{version}}/starter-kits).

<a name="laravel-the-api-backend"></a>
### Laravel The API Backend

Laravel my also serve as an API backend to a JavaScript single-page application or mobile application. For example, you might use Laravel as an API backend for your [Next.js](https://nextjs.org) application. In this context, you may use Laravel to provide [authentication](/docs/{{version}}/sanctum) and data storage / retrieval for your application, while also taking advantage of Laravel's powerful services such as queues, emails, notifications, and more.

If this is how you plan to use Laravel, you may want to check out our documentation on [routing](/docs/{{version}}/routing), [Laravel Sanctum](/docs/{{version}}/sanctum), and the [Eloquent ORM](/docs/{{version}}/eloquent).

