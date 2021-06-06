# Laravel Sail

- [Introduction](#introduction)
- [Installation & Setup](#installation)
    - [Installing Sail Into Existing Applications](#installing-sail-into-existing-applications)
    - [Configuring A Bash Alias](#configuring-a-bash-alias)
- [Starting & Stopping Sail](#starting-and-stopping-sail)
- [Executing Commands](#executing-sail-commands)
    - [Executing PHP Commands](#executing-php-commands)
    - [Executing Composer Commands](#executing-composer-commands)
    - [Executing Artisan Commands](#executing-artisan-commands)
    - [Executing Node / NPM Commands](#executing-node-npm-commands)
- [Interacting With Databases](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [Redis](#redis)
    - [MeiliSearch](#meilisearch)
- [Running Tests](#running-tests)
    - [Laravel Dusk](#laravel-dusk)
- [Previewing Emails](#previewing-emails)
- [Container CLI](#sail-container-cli)
- [PHP Versions](#sail-php-versions)
- [Sharing Your Site](#sharing-your-site)
- [Queue Workers](#queue-workers)
- [Customization](#sail-customization)

<a name="introduction"></a>
## Introduction

Laravel Sail is a light-weight command-line interface for interacting with Laravel's default Docker development environment. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience.

At its heart, Sail is the `docker-compose.yml` file and the `sail` script that is stored at the root of your project. The `sail` script provides a CLI with convenient methods for interacting with the Docker containers defined by the `docker-compose.yml` file.

Laravel Sail is supported on macOS, Linux, and Windows (via WSL2).

<a name="installation"></a>
## Installation & Setup

Laravel Sail is automatically installed with all new Laravel applications so you may start using it immediately. To learn how to create a new Laravel application, please consult Laravel's [installation documentation](/docs/{{version}}/installation) for your operating system. During installation, you will be asked to choose which Sail supported services your application will be interacting with.

<a name="installing-sail-into-existing-applications"></a>
### Installing Sail Into Existing Applications

If you are interested in using Sail with an existing Laravel application, you may simply install Sail using the Composer package manager. Of course, these steps assume that your existing local development environment allows you to install Composer dependencies:

    composer require laravel/sail --dev

After Sail has been installed, you may run the `sail:install` Artisan command. This command will publish Sail's `docker-compose.yml` file to the root of your application:

    php artisan sail:install

Finally, you may start Sail. To continue learning how to use Sail, please continue reading the remainder of this documentation:

    ./vendor/bin/sail up

<a name="configuring-a-bash-alias"></a>
### Configuring A Bash Alias

By default, Sail commands are invoked using the `vendor/bin/sail` script that is included with all new Laravel applications:

```bash
./vendor/bin/sail up
```

However, instead of repeatedly typing `vendor/bin/sail` to execute Sail commands, you may wish to configure a Bash alias that allows you to execute Sail's commands more easily:

```bash
alias sail='bash vendor/bin/sail'
```

Once the Bash alias has been configured, you may execute Sail commands by simply typing `sail`. The remainder of this documentation's examples will assume that you have configured this alias:

```bash
sail up
```

<a name="starting-and-stopping-sail"></a>
## Starting & Stopping Sail

Laravel Sail's `docker-compose.yml` file defines a Docker variety of containers that work together to help you build Laravel applications. Each of these containers is an entry within the `services` configuration of your `docker-compose.yml` file. The `laravel.test` container is the primary application container that will be serving your application.

Before starting Sail, you should ensure that no other web servers or databases are running on your local computer. To start all of the Docker containers defined in your application's `docker-compose.yml` file, you should execute the `up` command:

```bash
sail up
```

To start all of the Docker containers in the background, you may start Sail in "detached" mode:

```bash
sail up -d
```

Once the application's containers have been started, you may access the project in your web browser at: http://localhost.

To stop all of the containers, you may simply press Control + C to stop the container's execution. Or, if the containers are running in the background, you may use the `down` command:

```bash
sail down
```

<a name="executing-sail-commands"></a>
## Executing Commands

When using Laravel Sail, your application is executing within a Docker container and is isolated from your local computer. However, Sail provides a convenient way to run various commands against your application such as arbitrary PHP commands, Artisan commands, Composer commands, and Node / NPM commands.

**When reading the Laravel documentation, you will often see references to Composer, Artisan, and Node / NPM commands that do not reference Sail.** Those examples assume that these tools are installed on your local computer. If you are using Sail for your local Laravel development environment, you should execute those commands using Sail:

```bash
# Running Artisan commands locally...
php artisan queue:work

# Running Artisan commands within Laravel Sail...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### Executing PHP Commands

PHP commands may be executed using the `php` command. Of course, these commands will execute using the PHP version that is configured for your application. To learn more about the PHP versions available to Laravel Sail, consult the [PHP version documentation](#sail-php-versions):

```bash
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Executing Composer Commands

Composer commands may be executed using the `composer` command. Laravel Sail's application container includes a Composer 2.x installation:

```nothing
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
#### Installing Composer Dependencies For Existing Applications

If you are developing an application with a team, you may not be the one that initially creates the Laravel application. Therefore, none of the application's Composer dependencies, including Sail, will be installed after you clone the application's repository to your local computer.

You may install the application's dependencies by navigating to the application's directory and executing the following command. This command uses a small Docker container containing PHP and Composer to install the application's dependencies:

```nothing
docker run --rm \
    -v $(pwd):/opt \
    -w /opt \
    laravelsail/php80-composer:latest \
    composer install
```

<a name="executing-artisan-commands"></a>
### Executing Artisan Commands

Laravel Artisan commands may be executed using the `artisan` command:

```bash
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Executing Node / NPM Commands

Node commands may be executed using the `node` command while NPM commands may be executed using the `npm` command:

```nothing
sail node --version

sail npm run prod
```

<a name="interacting-with-sail-databases"></a>
## Interacting With Databases

<a name="mysql"></a>
### MySQL

As you may have noticed, your application's `docker-compose.yml` file contains an entry for a MySQL container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your database is persisted even when stopping and restarting your containers. In addition, when the MySQL container is starting, it will ensure a database exists whose name matches the value of your `DB_DATABASE` environment variable.

Once you have started your containers, you may connect to the MySQL instance within your application by setting your `DB_HOST` environment variable within your application's `.env` file to `mysql`.

To connect to your application's MySQL database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the MySQL database is accessible at `localhost` port 3306.

<a name="redis"></a>
### Redis

Your application's `docker-compose.yml` file also contains an entry for a [Redis](https://redis.io) container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Redis data is persisted even when stopping and restarting your containers. Once you have started your containers, you may connect to the Redis instance within your application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `redis`.

To connect to your application's Redis database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Redis database is accessible at `localhost` port 6379.

<a name="meilisearch"></a>
### MeiliSearch

If you chose to install the [MeiliSearch](https://www.meilisearch.com) service when installing Sail, your application's `docker-compose.yml` file will contain an entry for this powerful search-engine that is [compatible](https://github.com/meilisearch/meilisearch-laravel-scout) with [Laravel Scout](/docs/{{version}}/scout). Once you have started your containers, you may connect to the MeiliSearch instance within your application by setting your `MEILISEARCH_HOST` environment variable to `http://meilisearch:7700`.

From your local machine, you may access MeiliSearch's web based administration panel by navigating to `http://localhost:7700` in your web browser.

<a name="running-tests"></a>
## Running Tests

Laravel provides amazing testing support out of the box, and you may use Sail's `test` command to run your applications [feature and unit tests](/docs/{{version}}/testing). Any CLI options that are accepted by PHPUnit may also be passed to the `test` command:

    sail test

    sail test --group orders

The Sail `test` command is equivalent to running the `test` Artisan command:

    sail artisan test

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk) provides an expressive, easy-to-use browser automation and testing API. Thanks to Sail, you may run these tests without ever installing Selenium or other tools on your local computer. To get started, uncomment the Selenium service in your application's `docker-compose.yml` file:

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

Next, ensure that the `laravel.test` service in your application's `docker-compose.yml` file has a `depends_on` entry for `selenium`:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

Finally, you may run your Dusk test suite by starting Sail and running the `dusk` command:

    sail dusk

<a name="previewing-emails"></a>
## Previewing Emails

Laravel Sail's default `docker-compose.yml` file contains a service entry for [MailHog](https://github.com/mailhog/MailHog). MailHog intercepts emails sent by your application during local development and provides a convenient web interface so that you can preview your email messages in your browser. When using Sail, MailHog's default host is `mailhog` and is available via port 1025:

```bash
MAIL_HOST=mailhog
MAIL_PORT=1025
```

When Sail is running, you may access the MailHog web interface at: http://localhost:8025

<a name="sail-container-cli"></a>
## Container CLI

Sometimes you may wish to start a Bash session within your application's container. You may use the `shell` command to connect to your application's container, allowing you to inspect its files and installed services as well execute arbitrary shell commands within the container:

```nothing
sail shell
```

To start a new [Laravel Tinker](https://github.com/laravel/tinker) session, you may execute the `tinker` command:

```bash
sail tinker
```

<a name="sail-php-versions"></a>
## PHP Versions

Sail currently supports serving your application via PHP 8.0 or PHP 7.4. To change the PHP version that is used to serve your application, you should update the `build` definition of the `laravel.test` container in your application's `docker-compose.yml` file:

```yaml
# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0

# PHP 7.4
context: ./vendor/laravel/sail/runtimes/7.4
```

In addition, you may wish to update your `image` name to reflect the version of PHP being used by your application. This option is also defined in your application's `docker-compose.yml` file:

```yaml
image: sail-8.0/app
```

After updating your application's `docker-compose.yml` file, you should rebuild your container images:

    sail build --no-cache

    sail up

<a name="sharing-your-site"></a>
## Sharing Your Site

Sometimes you may need to share your site publicly in order to preview your site for a colleague or to test webhook integrations with your application. To share your site, you may use the `share` command. After executing this command, you will be issued a random `laravel-sail.site` URL that you may use to access your application:

    sail share

If you would like to choose the subdomain for your shared site, you may provide the `subdomain` option when executing the `share` command:

    sail share --subdomain=my-sail-site

> {tip} The `share` command is powered by [Expose](https://github.com/beyondcode/expose), an open source tunneling service by [BeyondCode](https://beyondco.de).

<a name="sail-customization"></a>
## Queue Workers

Working with queues in a local environment is not an easy task, because there are problems with the installation of the Supervisor for the Docker environment. A simple solution is to run the command in a new console tab every time:

```bash
sail artisan queue:work
```

Or use a separate Docker service for this:

```yaml
    queue-worker:
        image: sail-8.0/app
        container_name: queue-worker
        depends_on:
            - redis
        networks:
            - sail
        volumes:
            - '.:/var/www/html'
        restart: unless-stopped
        entrypoint: [ 'php', 'artisan', 'queue:work' ]
```

This worker listens to all queues. If you need to customize any of the queues, then you can create a new service in `docker-compose.yml`:

```yaml
    queue-emails-worker:
        image: sail-8.0/app
        container_name: queue-emails-worker
        depends_on:
            - redis
        networks:
            - sail
        volumes:
            - '.:/var/www/html'
        restart: unless-stopped
        entrypoint: [ 'php', 'artisan', 'queue:work', '--queue=emails', '--tries=3', '--timeout=30' ]
```

Please note that to update the code executed in the worker, you need to run the following command or restart the entire environment:

```bash
sail artisan queue:restart
```

Configuration `restart: unless-stopped` will automatically restart the container with new changes.

<a name="queue-workers"></a>
## Customization

Since Sail is just Docker, you are free to customize nearly everything about it. To publish Sail's own Dockerfiles, you may execute the `sail:publish` command:

```bash
sail artisan sail:publish
```

After running this command, the Dockerfiles and other configuration files used by Laravel Sail will be placed within a `docker` directory in your application's root directory. After customizing your Sail installation, you may rebuild your application's containers using the `build` command:

```bash
sail build --no-cache
```
