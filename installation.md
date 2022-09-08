# 安裝

- [初見 Laravel](#meet-laravel)
    - [為什麼選擇 Laravel ?](#why-laravel)
- [你的第一個 Laravel 專案](#your-first-laravel-project)
- [Laravel & Docker](#laravel-and-docker)
    - [從 macOS 開始](#getting-started-on-macos)
    - [從 Windows 開始](#getting-started-on-windows)
    - [從 Linux 開始](#getting-started-on-linux)
    - [選擇你的 Sail 服務](#choosing-your-sail-services)
    - [透過 Composer 安裝](#installation-via-composer)
- [初始化設定](#initial-configuration)
    - [環境基本設定](#environment-based-configuration)
    - [目錄設定](#directory-configuration)
- [下一步](#next-steps)
    - [將 Laravel 作為全端框架](#laravel-the-fullstack-framework)
    - [將 Laravel 作為API後端](#laravel-the-api-backend)


<a name="meet-laravel"></a>
## 初見 Laravel

Laravel 是一款直觀且語法優雅的 web 框架。 一個　web　框架能在你建立應用程式時提供結構及起始點，讓你能專心創造些驚人之舉，而其他細節就儘管交給我們處理。

Laravel 致力於提供出色的開發體驗且提供強大的功能，例如全面的依賴注入( Dependency Injection )、直觀的資料庫抽象層( Database Abstraction Layer )、佇列和任務排程、單元和整合測試等等。

不論你是 PHP web 框架的新手還是征戰多年的資深老鳥， Laravel 都是一款能伴隨你成長的框架。我們將會協助你邁出成為 web 開發者的第一步或讓你的專業知識昇華到更高境界。我們迫不及待要看你露一手啦。

<a name="why-laravel"></a>
### 為什麼選擇 Laravel ?

建立一個 web 應用程式有琳瑯滿目的工具和框架供你選擇。但我們相信 Laravel 絕對是先進的全端 web 應用框架首選。

#### 漸進式框架

我們喜歡稱呼 Laravel 為一個「漸進式框架」，意思是 Laravel 會跟你一同進步。如果你剛好是正在起步的 web 開發者， Laravel 大量的文件、指南和 [影片教學](https://laracasts.com) 將幫助你學習而不至於不知所措。

如果你是資深的開發者， Laravel 提供了 [依賴注入](/docs/{{version}}/container) 、 [單元測試](/docs/{{version}}/testing) 、 [佇列](/docs/{{version}}/queues) 、 [廣播事件](/docs/{{version}}/broadcasting) 等等。 Laravel 對專業的 web 開發者提供穩定且易於掌控的企業工作量。

#### 可擴展的框架

Laravel 具有令人難以置信的可擴展性。歸功於 PHP 友善的靈活性和 Laravel 內建支援 Redis 等的快速分散式快取系統，讓擴充 Laravel 顯得輕而易舉。事實上， Laravel 的應用程式已經可以很輕鬆地每月處理幾億個請求。

需要壓縮開發費用嗎? [Laravel Vapor](https://vapor.laravel.com) 允許你在 AWS 最新的無伺服器技術平台上以近乎無限的規模執行 Laravel 的應用程式。

#### 社群框架

Laravel 結合了 PHP 生態系統中最好的套件且提供最強大又對開發者友善的框架。除此之外，世界各地數以千計的大神開發者們 [為框架做出了貢獻](https://github.com/laravel/framework) 。說不定你也會是為 Laravel 貢獻的大神。

<a name="your-first-laravel-project"></a>
## 你的第一個 Laravel 專案


我們希望讓開始 Laravel 變得盡可能容易。這邊有各種選項讓你在本機開發並執行專案。儘管你可能希望晚點再來探索這些選項， Laravel 在你使用 [Docker](https://www.docker.com) 時提供內建執行 Laravel 專案的方法： [Sail](/docs/{{version}}/sail) 。

Before creating your first Laravel project, you should ensure that your local machine has PHP and [Composer](https://getcomposer.org) installed. If you are developing on macOS, PHP and Composer can be installed via [Homebrew](https://brew.sh/). In addition, we recommend [installing Node and NPM](https://nodejs.org).

After you have installed PHP and Composer, you may create a new Laravel project via the Composer `create-project` command:

```nothing
composer create-project laravel/laravel example-app
```

Or, you may create new Laravel projects by globally installing the Laravel installer via Composer:

```nothing
composer global require laravel/installer

laravel new example-app
```

After the project has been created, start Laravel's local development server using the Laravel's Artisan CLI `serve` command:

```nothing
cd example-app

php artisan serve
```

Once you have started the Artisan development server, your application will be accessible in your web browser at `http://localhost:8000`. Next, you're ready to [start taking your next steps into the Laravel ecosystem](#next-steps). Of course, you may also want to [configure a database](#databases-and-migrations).

> **Note**  
> If you would like a head start when developing your Laravel application, consider using one of our [starter kits](/docs/{{version}}/starter-kits). Laravel's starter kits provide backend and frontend authentication scaffolding for your new Laravel application.

<a name="laravel-and-docker"></a>
## Laravel & Docker

We want it to be as easy as possible to get started with Laravel regardless of your preferred operating system. So, there are a variety of options for developing and running a Laravel project on your local machine. While you may wish to explore these options at a later time, Laravel provides [Sail](/docs/{{version}}/sail), a built-in solution for running your Laravel project using [Docker](https://www.docker.com).

Docker is a tool for running applications and services in small, light-weight "containers" which do not interfere with your local machine's installed software or configuration. This means you don't have to worry about configuring or setting up complicated development tools such as web servers and databases on your local machine. To get started, you only need to install [Docker Desktop](https://www.docker.com/products/docker-desktop).

Laravel Sail is a light-weight command-line interface for interacting with Laravel's default Docker configuration. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience.

> **Note**  
> Already a Docker expert? Don't worry! Everything about Sail can be customized using the `docker-compose.yml` file included with Laravel.

<a name="getting-started-on-macos"></a>
### Getting Started On macOS

If you're developing on a Mac and [Docker Desktop](https://www.docker.com/products/docker-desktop) is already installed, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal:

```shell
curl -s "https://laravel.build/example-app" | bash
```

Of course, you can change "example-app" in this URL to anything you like - just make sure the application name only contains alpha-numeric characters, dashes, and underscores. The Laravel application's directory will be created within the directory you execute the command from.

Sail installation may take several minutes while Sail's application containers are built on your local machine.

After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration:

```shell
cd example-app

./vendor/bin/sail up
```

Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost.

> **Note**  
> To continue learning more about Laravel Sail, review its [complete documentation](/docs/{{version}}/sail).

<a name="getting-started-on-windows"></a>
### Getting Started On Windows

Before we create a new Laravel application on your Windows machine, make sure to install [Docker Desktop](https://www.docker.com/products/docker-desktop). Next, you should ensure that Windows Subsystem for Linux 2 (WSL2) is installed and enabled. WSL allows you to run Linux binary executables natively on Windows 10. Information on how to install and enable WSL2 can be found within Microsoft's [developer environment documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

> **Note**  
> After installing and enabling WSL2, you should ensure that Docker Desktop is [configured to use the WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/).

Next, you are ready to create your first Laravel project. Launch [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab) and begin a new terminal session for your WSL2 Linux operating system. Next, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal:

```shell
curl -s https://laravel.build/example-app | bash
```

Of course, you can change "example-app" in this URL to anything you like - just make sure the application name only contains alpha-numeric characters, dashes, and underscores. The Laravel application's directory will be created within the directory you execute the command from.

Sail installation may take several minutes while Sail's application containers are built on your local machine.

After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration:

```shell
cd example-app

./vendor/bin/sail up
```

Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost.

> **Note**  
> To continue learning more about Laravel Sail, review its [complete documentation](/docs/{{version}}/sail).

#### Developing Within WSL2

Of course, you will need to be able to modify the Laravel application files that were created within your WSL2 installation. To accomplish this, we recommend using Microsoft's [Visual Studio Code](https://code.visualstudio.com) editor and their first-party extension for [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack).

Once these tools are installed, you may open any Laravel project by executing the `code .` command from your application's root directory using Windows Terminal.

<a name="getting-started-on-linux"></a>
### Getting Started On Linux

If you're developing on Linux and [Docker Compose](https://docs.docker.com/compose/install/) is already installed, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal:

```shell
curl -s https://laravel.build/example-app | bash
```

Of course, you can change "example-app" in this URL to anything you like - just make sure the application name only contains alpha-numeric characters, dashes, and underscores. The Laravel application's directory will be created within the directory you execute the command from.

Sail installation may take several minutes while Sail's application containers are built on your local machine.

After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration:

```shell
cd example-app

./vendor/bin/sail up
```

Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost.

> **Note**  
> To continue learning more about Laravel Sail, review its [complete documentation](/docs/{{version}}/sail).

<a name="choosing-your-sail-services"></a>
### Choosing Your Sail Services

When creating a new Laravel application via Sail, you may use the `with` query string variable to choose which services should be configured in your new application's `docker-compose.yml` file. Available services include `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `minio`, `selenium`, and `mailhog`:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

If you do not specify which services you would like configured, a default stack of `mysql`, `redis`, `meilisearch`, `mailhog`, and `selenium` will be configured.

You may instruct Sail to install a default [Devcontainer](/docs/{{version}}/sail#using-devcontainers) by adding the `devcontainer` parameter to the URL:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="initial-configuration"></a>
## Initial Configuration

All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you.

Laravel needs almost no additional configuration out of the box. You are free to get started developing! However, you may wish to review the `config/app.php` file and its documentation. It contains several options such as `timezone` and `locale` that you may wish to change according to your application.

<a name="environment-based-configuration"></a>
### Environment Based Configuration

Since many of Laravel's configuration option values may vary depending on whether your application is running on your local machine or on a production web server, many important configuration values are defined using the `.env` file that exists at the root of your application.

Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed.

> **Note**  
> For more information about the `.env` file and environment based configuration, check out the full [configuration documentation](/docs/{{version}}/configuration#environment-configuration).

<a name="databases-and-migrations"></a>
### Databases & Migrations

Now that you have created your Laravel application, you probably want to store some data in a database. By default, your application's `.env` configuration file specifies that Laravel will be interacting with a MySQL database and will access the database at `127.0.0.1`. If you are developing on macOS and need to install MySQL, Postgres, or Redis locally, you may find it convenient to utilize [DBngin](https://dbngin.com/).

If you do not want to install MySQL or Postgres on your local machine, you can always use a [SQLite](https://www.sqlite.org/index.html) database. SQLite is a small, fast, self-contained database engine. To get started, create a SQLite database by creating an empty SQLite file. Typically, this file will exist within the `database` directory of your Laravel application:

```shell
touch database/database.sqlite
```

Next, update your `.env` configuration file to use Laravel's `sqlite` database driver. You may remove the other database configuration options:

```ini
DB_CONNECTION=sqlite # [tl! add]
DB_CONNECTION=mysql # [tl! remove]
DB_HOST=127.0.0.1 # [tl! remove]
DB_PORT=3306 # [tl! remove]
DB_DATABASE=laravel # [tl! remove]
DB_USERNAME=root # [tl! remove]
DB_PASSWORD= # [tl! remove]
```

Once you have configured your SQLite database, you may run your application's [database migrations](/docs/{{version}}/migrations), which will create your application's database tables:

```shell
php artisan migrate
```

<a name="next-steps"></a>
## Next Steps

Now that you have created your Laravel project, you may be wondering what to learn next. First, we strongly recommend becoming familiar with how Laravel works by reading the following documentation:

<div class="content-list" markdown="1">

- [Request Lifecycle](/docs/{{version}}/lifecycle)
- [Configuration](/docs/{{version}}/configuration)
- [Directory Structure](/docs/{{version}}/structure)
- [Frontend](/docs/{{version}}/frontend)
- [Service Container](/docs/{{version}}/container)
- [Facades](/docs/{{version}}/facades)

</div>

How you want to use Laravel will also dictate the next steps on your journey. There are a variety of ways to use Laravel, and we'll explore two primary use cases for the framework below.

<a name="laravel-the-fullstack-framework"></a>
### Laravel The Full Stack Framework

Laravel may serve as a full stack framework. By "full stack" framework we mean that you are going to use Laravel to route requests to your application and render your frontend via [Blade templates](/docs/{{version}}/blade) or a single-page application hybrid technology like [Inertia](https://inertiajs.com). This is the most common way to use the Laravel framework, and, in our opinion, the most productive way to use Laravel.

If this is how you plan to use Laravel, you may want to check out our documentation on [frontend development](/docs/{{version}}/frontend), [routing](/docs/{{version}}/routing), [views](/docs/{{version}}/views), or the [Eloquent ORM](/docs/{{version}}/eloquent). In addition, you might be interested in learning about community packages like [Livewire](https://laravel-livewire.com) and [Inertia](https://inertiajs.com). These packages allow you to use Laravel as a full-stack framework while enjoying many of the UI benefits provided by single-page JavaScript applications.

If you are using Laravel as a full stack framework, we also strongly encourage you to learn how to compile your application's CSS and JavaScript using [Vite](/docs/{{version}}/vite).

> **Note**  
> If you want to get a head start building your application, check out one of our official [application starter kits](/docs/{{version}}/starter-kits).

<a name="laravel-the-api-backend"></a>
### Laravel The API Backend

Laravel may also serve as an API backend to a JavaScript single-page application or mobile application. For example, you might use Laravel as an API backend for your [Next.js](https://nextjs.org) application. In this context, you may use Laravel to provide [authentication](/docs/{{version}}/sanctum) and data storage / retrieval for your application, while also taking advantage of Laravel's powerful services such as queues, emails, notifications, and more.

If this is how you plan to use Laravel, you may want to check out our documentation on [routing](/docs/{{version}}/routing), [Laravel Sanctum](/docs/{{version}}/sanctum), and the [Eloquent ORM](/docs/{{version}}/eloquent).

> **Note**  
> Need a head start scaffolding your Laravel backend and Next.js frontend? Laravel Breeze offers an [API stack](/docs/{{version}}/starter-kits#breeze-and-next) as well as a [Next.js frontend implementation](https://github.com/laravel/breeze-next) so you can get started in minutes.
