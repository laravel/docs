# Laravel Sail

- [Introduction](#introduction)
- [Installation and Setup](#installation)
    - [Installing Sail Into Existing Applications](#installing-sail-into-existing-applications)
    - [Rebuilding Sail Images](#rebuilding-sail-images)
    - [Configuring A Shell Alias](#configuring-a-shell-alias)
- [Starting and Stopping Sail](#starting-and-stopping-sail)
- [Executing Commands](#executing-sail-commands)
    - [Executing PHP Commands](#executing-php-commands)
    - [Executing Composer Commands](#executing-composer-commands)
    - [Executing Artisan Commands](#executing-artisan-commands)
    - [Executing Node / NPM Commands](#executing-node-npm-commands)
- [Interacting With Databases](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [MongoDB](#mongodb)
    - [Redis](#redis)
    - [Valkey](#valkey)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [File Storage](#file-storage)
- [Running Tests](#running-tests)
    - [Laravel Dusk](#laravel-dusk)
- [Previewing Emails](#previewing-emails)
- [Container CLI](#sail-container-cli)
- [PHP Versions](#sail-php-versions)
- [Node Versions](#sail-node-versions)
- [Sharing Your Site](#sharing-your-site)
- [Debugging With Xdebug](#debugging-with-xdebug)
  - [Xdebug CLI Usage](#xdebug-cli-usage)
  - [Xdebug Browser Usage](#xdebug-browser-usage)
- [Customization](#sail-customization)

<a name="introduction"></a>
## Introduction

[Laravel Sail](https://github.com/laravel/sail) is a light-weight command-line interface for interacting with Laravel's default Docker development environment. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience.

At its heart, Sail is the `docker-compose.yml` file and the `sail` script that is stored at the root of your project. The `sail` script provides a CLI with convenient methods for interacting with the Docker containers defined by the `docker-compose.yml` file.

Laravel Sail is supported on macOS, Linux, and Windows (via [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)).

<a name="installation"></a>
## Installation and Setup

Laravel Sail is automatically installed with all new Laravel applications so you may start using it immediately.

<a name="installing-sail-into-existing-applications"></a>
### Installing Sail Into Existing Applications

If you are interested in using Sail with an existing Laravel application, you may simply install Sail using the Composer package manager. Of course, these steps assume that your existing local development environment allows you to install Composer dependencies:

```shell
composer require laravel/sail --dev
```

After Sail has been installed, you may run the `sail:install` Artisan command. This command will publish Sail's `docker-compose.yml` file to the root of your application and modify your `.env` file with the required environment variables in order to connect to the Docker services:

```shell
php artisan sail:install
```

Finally, you may start Sail. To continue learning how to use Sail, please continue reading the remainder of this documentation:

```shell
./vendor/bin/sail up
```

> [!WARNING]
> If you are using Docker Desktop for Linux, you should use the `default` Docker context by executing the following command: `docker context use default`.

<a name="adding-additional-services"></a>
#### Adding Additional Services

If you would like to add an additional service to your existing Sail installation, you may run the `sail:add` Artisan command:

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Using Devcontainers

If you would like to develop within a [Devcontainer](https://code.visualstudio.com/docs/remote/containers), you may provide the `--devcontainer` option to the `sail:install` command. The `--devcontainer` option will instruct the `sail:install` command to publish a default `.devcontainer/devcontainer.json ` file to the root of your application:

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Rebuilding Sail Images

Sometimes you may want to completely rebuild your Sail images to ensure all of the image's packages and software are up to date. You may accomplish this using the `build` command:

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### Configuring A Shell Alias

By default, Sail commands are invoked using the `vendor/bin/sail` script that is included with all new Laravel applications:

```shell
./vendor/bin/sail up
```

However, instead of repeatedly typing `vendor/bin/sail` to execute Sail commands, you may wish to configure a shell alias that allows you to execute Sail's commands more easily:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

To make sure this is always available, you may add this to your shell configuration file in your home directory, such as `~/.zshrc` or `~/.bashrc`, and then restart your shell.

Once the shell alias has been configured, you may execute Sail commands by simply typing `sail`. The remainder of this documentation's examples will assume that you have configured this alias:

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Starting and Stopping Sail

Laravel Sail's `docker-compose.yml` file defines a variety of Docker containers that work together to help you build Laravel applications. Each of these containers is an entry within the `services` configuration of your `docker-compose.yml` file. The `laravel.test` container is the primary application container that will be serving your application.

Before starting Sail, you should ensure that no other web servers or databases are running on your local computer. To start all of the Docker containers defined in your application's `docker-compose.yml` file, you should execute the `up` command:

```shell
sail up
```

To start all of the Docker containers in the background, you may start Sail in "detached" mode:

```shell
sail up -d
```

Once the application's containers have been started, you may access the project in your web browser at: http://localhost.

To stop all of the containers, you may simply press Control + C to stop the container's execution. Or, if the containers are running in the background, you may use the `stop` command:

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## Executing Commands

When using Laravel Sail, your application is executing within a Docker container and is isolated from your local computer. However, Sail provides a convenient way to run various commands against your application such as arbitrary PHP commands, Artisan commands, Composer commands, and Node / NPM commands.

**When reading the Laravel documentation, you will often see references to Composer, Artisan, and Node / NPM commands that do not reference Sail.** Those examples assume that these tools are installed on your local computer. If you are using Sail for your local Laravel development environment, you should execute those commands using Sail:

```shell
# Running Artisan commands locally...
php artisan queue:work

# Running Artisan commands within Laravel Sail...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### Executing PHP Commands

PHP commands may be executed using the `php` command. Of course, these commands will execute using the PHP version that is configured for your application. To learn more about the PHP versions available to Laravel Sail, consult the [PHP version documentation](#sail-php-versions):

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Executing Composer Commands

Composer commands may be executed using the `composer` command. Laravel Sail's application container includes a Composer installation:

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
### Executing Artisan Commands

Laravel Artisan commands may be executed using the `artisan` command:

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Executing Node / NPM Commands

Node commands may be executed using the `node` command while NPM commands may be executed using the `npm` command:

```shell
sail node --version

sail npm run dev
```

If you wish, you may use Yarn instead of NPM:

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## Interacting With Databases

<a name="mysql"></a>
### MySQL

As you may have noticed, your application's `docker-compose.yml` file contains an entry for a MySQL container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your database is persisted even when stopping and restarting your containers.

In addition, the first time the MySQL container starts, it will create two databases for you. The first database is named using the value of your `DB_DATABASE` environment variable and is for your local development. The second is a dedicated testing database named `testing` and will ensure that your tests do not interfere with your development data.

Once you have started your containers, you may connect to the MySQL instance within your application by setting your `DB_HOST` environment variable within your application's `.env` file to `mysql`.

To connect to your application's MySQL database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the MySQL database is accessible at `localhost` port 3306 and the access credentials correspond to the values of your `DB_USERNAME` and `DB_PASSWORD` environment variables. Or, you may connect as the `root` user, which also utilizes the value of your `DB_PASSWORD` environment variable as its password.

<a name="mongodb"></a>
### MongoDB

If you chose to install the [MongoDB](https://www.mongodb.com/) service when installing Sail, your application's `docker-compose.yml` file contains an entry for a [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) container which provides the MongoDB document database with Atlas features like [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/). This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your database is persisted even when stopping and restarting your containers.

Once you have started your containers, you may connect to the MongoDB instance within your application by setting your `MONGODB_URI` environment variable within your application's `.env` file to `mongodb://mongodb:27017`. Authentication is disabled by default, but you can set the `MONGODB_USERNAME` and `MONGODB_PASSWORD` environment variables to enable authentication before starting the `mongodb` container. Then, add the credentials to the connection string:

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

For seamless integration of MongoDB with your application, you can install the [official package maintained by MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/).

To connect to your application's MongoDB database from your local machine, you may use a graphical interface such as [Compass](https://www.mongodb.com/products/tools/compass). By default, the MongoDB database is accessible at `localhost` port `27017`.

<a name="redis"></a>
### Redis

Your application's `docker-compose.yml` file also contains an entry for a [Redis](https://redis.io) container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Redis instance is persisted even when stopping and restarting your containers. Once you have started your containers, you may connect to the Redis instance within your application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `redis`.

To connect to your application's Redis database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Redis database is accessible at `localhost` port 6379.

<a name="valkey"></a>
### Valkey

If you choose to install Valkey service when installing Sail, your application's `docker-compose.yml` file will contain an entry for [Valkey](https://valkey.io/). This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Valkey instance is persisted even when stopping and restarting your containers. You can connect to this container in you application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `valkey`.

To connect to your application's Valkey database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Valkey database is accessible at `localhost` port 6379.

<a name="meilisearch"></a>
### Meilisearch

If you chose to install the [Meilisearch](https://www.meilisearch.com) service when installing Sail, your application's `docker-compose.yml` file will contain an entry for this powerful search engine that is integrated with [Laravel Scout](/docs/{{version}}/scout). Once you have started your containers, you may connect to the Meilisearch instance within your application by setting your `MEILISEARCH_HOST` environment variable to `http://meilisearch:7700`.

From your local machine, you may access Meilisearch's web based administration panel by navigating to `http://localhost:7700` in your web browser.

<a name="typesense"></a>
### Typesense

If you chose to install the [Typesense](https://typesense.org) service when installing Sail, your application's `docker-compose.yml` file will contain an entry for this lightning fast, open-source search engine that is natively integrated with [Laravel Scout](/docs/{{version}}/scout#typesense). Once you have started your containers, you may connect to the Typesense instance within your application by setting the following environment variables:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

From your local machine, you may access Typesense's API via `http://localhost:8108`.

<a name="file-storage"></a>
## File Storage

If you plan to use Amazon S3 to store files while running your application in its production environment, you may wish to install the [MinIO](https://min.io) service when installing Sail. MinIO provides an S3 compatible API that you may use to develop locally using Laravel's `s3` file storage driver without creating "test" storage buckets in your production S3 environment. If you choose to install MinIO while installing Sail, a MinIO configuration section will be added to your application's `docker-compose.yml` file.

By default, your application's `filesystems` configuration file already contains a disk configuration for the `s3` disk. In addition to using this disk to interact with Amazon S3, you may use it to interact with any S3 compatible file storage service such as MinIO by simply modifying the associated environment variables that control its configuration. For example, when using MinIO, your filesystem environment variable configuration should be defined as follows:

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

In order for Laravel's Flysystem integration to generate proper URLs when using MinIO, you should define the `AWS_URL` environment variable so that it matches your application's local URL and includes the bucket name in the URL path:

```ini
AWS_URL=http://localhost:9000/local
```

You may create buckets via the MinIO console, which is available at `http://localhost:8900`. The default username for the MinIO console is `sail` while the default password is `password`.

> [!WARNING]
> Generating temporary storage URLs via the `temporaryUrl` method is not supported when using MinIO.

<a name="running-tests"></a>
## Running Tests

Laravel provides amazing testing support out of the box, and you may use Sail's `test` command to run your applications [feature and unit tests](/docs/{{version}}/testing). Any CLI options that are accepted by Pest / PHPUnit may also be passed to the `test` command:

```shell
sail test

sail test --group orders
```

The Sail `test` command is equivalent to running the `test` Artisan command:

```shell
sail artisan test
```

By default, Sail will create a dedicated `testing` database so that your tests do not interfere with the current state of your database. In a default Laravel installation, Sail will also configure your `phpunit.xml` file to use this database when executing your tests:

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk) provides an expressive, easy-to-use browser automation and testing API. Thanks to Sail, you may run these tests without ever installing Selenium or other tools on your local computer. To get started, uncomment the Selenium service in your application's `docker-compose.yml` file:

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    extra_hosts:
      - 'host.docker.internal:host-gateway'
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

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Selenium on Apple Silicon

If your local machine contains an Apple Silicon chip, your `selenium` service must use the `selenium/standalone-chromium` image:

```yaml
selenium:
    image: 'selenium/standalone-chromium'
    extra_hosts:
        - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<a name="previewing-emails"></a>
## Previewing Emails

Laravel Sail's default `docker-compose.yml` file contains a service entry for [Mailpit](https://github.com/axllent/mailpit). Mailpit intercepts emails sent by your application during local development and provides a convenient web interface so that you can preview your email messages in your browser. When using Sail, Mailpit's default host is `mailpit` and is available via port 1025:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

When Sail is running, you may access the Mailpit web interface at: http://localhost:8025

<a name="sail-container-cli"></a>
## Container CLI

Sometimes you may wish to start a Bash session within your application's container. You may use the `shell` command to connect to your application's container, allowing you to inspect its files and installed services as well as execute arbitrary shell commands within the container:

```shell
sail shell

sail root-shell
```

To start a new [Laravel Tinker](https://github.com/laravel/tinker) session, you may execute the `tinker` command:

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP Versions

Sail currently supports serving your application via PHP 8.4, 8.3, 8.2, 8.1, or PHP 8.0. The default PHP version used by Sail is currently PHP 8.4. To change the PHP version that is used to serve your application, you should update the `build` definition of the `laravel.test` container in your application's `docker-compose.yml` file:

```yaml
# PHP 8.4
context: ./vendor/laravel/sail/runtimes/8.4

# PHP 8.3
context: ./vendor/laravel/sail/runtimes/8.3

# PHP 8.2
context: ./vendor/laravel/sail/runtimes/8.2

# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0
```

In addition, you may wish to update your `image` name to reflect the version of PHP being used by your application. This option is also defined in your application's `docker-compose.yml` file:

```yaml
image: sail-8.2/app
```

After updating your application's `docker-compose.yml` file, you should rebuild your container images:

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node Versions

Sail installs Node 22 by default. To change the Node version that is installed when building your images, you may update the `build.args` definition of the `laravel.test` service in your application's `docker-compose.yml` file:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

After updating your application's `docker-compose.yml` file, you should rebuild your container images:

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## Sharing Your Site

Sometimes you may need to share your site publicly in order to preview your site for a colleague or to test webhook integrations with your application. To share your site, you may use the `share` command. After executing this command, you will be issued a random `laravel-sail.site` URL that you may use to access your application:

```shell
sail share
```

When sharing your site via the `share` command, you should configure your application's trusted proxies using the `trustProxies` middleware method in your application's `bootstrap/app.php` file. Otherwise, URL generation helpers such as `url` and `route` will be unable to determine the correct HTTP host that should be used during URL generation:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

If you would like to choose the subdomain for your shared site, you may provide the `subdomain` option when executing the `share` command:

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> The `share` command is powered by [Expose](https://github.com/beyondcode/expose), an open source tunneling service by [BeyondCode](https://beyondco.de).

<a name="debugging-with-xdebug"></a>
## Debugging With Xdebug

Laravel Sail's Docker configuration includes support for [Xdebug](https://xdebug.org/), a popular and powerful debugger for PHP. To enable Xdebug, ensure you have [published your Sail configuration](#sail-customization). Then, add the following variables to your application's `.env` file to configure Xdebug:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

Next, ensure that your published `php.ini` file includes the following configuration so that Xdebug is activated in the specified modes:

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

After modifying the `php.ini` file, remember to rebuild your Docker images so that your changes to the `php.ini` file take effect:

```shell
sail build --no-cache
```

#### Linux Host IP Configuration

Internally, the `XDEBUG_CONFIG` environment variable is defined as `client_host=host.docker.internal` so that Xdebug will be properly configured for Mac and Windows (WSL2). If your local machine is running Linux and you're using Docker 20.10+, `host.docker.internal` is available, and no manual configuration is required.

For Docker versions older than 20.10, `host.docker.internal` is not supported on Linux, and you will need to manually define the host IP. To do this, configure a static IP for your container by defining a custom network in your `docker-compose.yml` file:

```yaml
networks:
  custom_network:
    ipam:
      config:
        - subnet: 172.20.0.0/16

services:
  laravel.test:
    networks:
      custom_network:
        ipv4_address: 172.20.0.2
```

Once you have set the static IP, define the SAIL_XDEBUG_CONFIG variable within your application's .env file:

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI Usage

A `sail debug` command may be used to start a debugging session when running an Artisan command:

```shell
# Run an Artisan command without Xdebug...
sail artisan migrate

# Run an Artisan command with Xdebug...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug Browser Usage

To debug your application while interacting with the application via a web browser, follow the [instructions provided by Xdebug](https://xdebug.org/docs/step_debug#web-application) for initiating an Xdebug session from the web browser.

If you're using PhpStorm, please review JetBrains' documentation regarding [zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html).

> [!WARNING]
> Laravel Sail relies on `artisan serve` to serve your application. The `artisan serve` command only accepts the `XDEBUG_CONFIG` and `XDEBUG_MODE` variables as of Laravel version 8.53.0. Older versions of Laravel (8.52.0 and below) do not support these variables and will not accept debug connections.

<a name="sail-customization"></a>
## Customization

Since Sail is just Docker, you are free to customize nearly everything about it. To publish Sail's own Dockerfiles, you may execute the `sail:publish` command:

```shell
sail artisan sail:publish
```

After running this command, the Dockerfiles and other configuration files used by Laravel Sail will be placed within a `docker` directory in your application's root directory. After customizing your Sail installation, you may wish to change the image name for the application container in your application's `docker-compose.yml` file. After doing so, rebuild your application's containers using the `build` command. Assigning a unique name to the application image is particularly important if you are using Sail to develop multiple Laravel applications on a single machine:

```shell
sail build --no-cache
```
