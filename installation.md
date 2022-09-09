# 安裝

- [ 初見 Laravel ](#meet-laravel)
    - [ 為什麼選擇 Laravel ？ ](#why-laravel)
- [ 你的第一個 Laravel 專案 ](#your-first-laravel-project)
- [ Laravel 和 Docker ](#laravel-and-docker)
    - [ 從 macOS 開始 ](#getting-started-on-macos)
    - [ 從 Windows 開始 ](#getting-started-on-windows)
    - [ 從 Linux 開始 ](#getting-started-on-linux)
    - [ 選擇你的 Sail 服務 ](#choosing-your-sail-services)
- [ 初始設定 ](#initial-configuration)
    - [ 環境基本設定 ](#environment-based-configuration)
    - [ 資料庫和資料遷移 ](#databases-and-migrations)
- [ 下一步 ](#next-steps)
    - [ 將 Laravel 作為全端框架 ](#laravel-the-fullstack-framework)
    - [ 將 Laravel 作為API後端 ](#laravel-the-api-backend)


<a name="meet-laravel"></a>
## 初見 Laravel

Laravel 是一款直觀且語法優雅的 web 框架。一個　web　框架能在你建立應用程式時提供結構及起始點，讓你能專心創造些驚人之舉，而其他細節就儘管交給我們處理。

Laravel 致力於提供出色的開發體驗且提供強大的功能，例如全面的依賴注入( Dependency Injection )、直觀的資料庫抽象層( Database Abstraction Layer )、佇列和任務排程、單元和整合測試等等。

不論你是 PHP web 框架的新手還是征戰多年的資深老鳥， Laravel 都是一款能伴隨你成長的框架。我們將會協助你邁出成為 web 開發者的第一步或讓你的專業知識昇華到更高境界。我們迫不及待要看你露一手啦。

<a name="why-laravel"></a>
### 為什麼選擇 Laravel ？

建立一個 web 應用程式有琳瑯滿目的工具和框架供你選擇。但我們相信 Laravel 絕對是先進的全端 web 應用框架首選。

#### 漸進式框架

我們喜歡稱呼 Laravel 為一個「漸進式框架」，意思是 Laravel 會跟你一同進步。如果你剛好是正在起步的 web 開發者， Laravel 大量的文件、指南和 [ 影片教學 ](https://laracasts.com) 將幫助你學習而不至於不知所措。

如果你是資深的開發者， Laravel 提供了 [ 依賴注入 ](/docs/{{version}}/container) 、 [ 單元測試 ](/docs/{{version}}/testing) 、 [ 佇列 ](/docs/{{version}}/queues) 、 [ 廣播事件 ](/docs/{{version}}/broadcasting) 等等。 Laravel 對專業的 web 開發者提供穩定且易於掌控的企業工作量。

#### 可擴展的框架

Laravel 具有令人難以置信的可擴展性。歸功於 PHP 友善的靈活性和 Laravel 內建支援 Redis 等的快速分散式快取系統，讓擴充 Laravel 顯得輕而易舉。事實上， Laravel 的應用程式已經可以很輕鬆地每月數以百萬計個請求。

需要壓縮開發費用嗎？ [ Laravel Vapor ](https://vapor.laravel.com) 允許你在 AWS 最新的無伺服器技術平台上以近乎無限的規模執行 Laravel 的應用程式。

#### 社群框架

Laravel 結合了 PHP 生態系統中最好的套件且提供最強大又對開發者友善的框架。除此之外，世界各地數以千計的大神開發者們 [ 為框架做出了貢獻 ](https://github.com/laravel/framework) 。說不定你也會是為 Laravel 貢獻的大神。

<a name="your-first-laravel-project"></a>
## 你的第一個 Laravel 專案

<<<<<<< HEAD
在你建立第一個 Laravel 專案之前，你要先確保你的電腦已經安裝 PHP 跟 [ Composer ](https://getcomposer.org/) 。如果你是 macOS 的開發者， PHP 跟 Composer 都可以透過 [ Homebrew ](https://brew.sh/) 安裝。除此之外，我們也建議你 [ 安裝 Nodejs 和 NPM ](https://nodejs.org/)

當你已經安裝 PHP 和 Composer 之後，你可以透過 Composer 的 `create-project` 指令建立一個新的 Laravel 專案：
=======

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
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27

```shell
composer create-project laravel/laravel example-app
```

<<<<<<< HEAD
或者，你也可以透過 Composer 全域安裝 Laravel 來建立新的 Laravel 專案：

```shell
composer global require laravel/installer
 
laravel new example-app
```

當專案被建立之後，在 Laravel 本機伺服器使用 Laravel 的 Artisan CLI 指令 `serve` 啟動：

```shell
cd example-app
 
php artisan serve
```

當你已經啟動了 Artisan 開發伺服器，你的應用程式會存取在瀏覽器的 http://localhost:8000 。接下來你已經準備好踏進 Laravel 的生態系統了。當然，你也可能想要設定資料庫。

> {tip} 如果你想要在開發你的 Laravel 應用程式時搶個，考慮看看我們的入門套件。 Laravel 入門套件會為你的 Laravel 應用程式提供前後端驗證的基本結構。

<a name="laravel-and-docker"></a>
## Laravel 和 Docker

我們希望讓你無論從哪種作業系統開始 Laravel 都變得盡可能簡易。所以，這有各種選項讓你在本機開發並執行 Laravel 專案。儘管你可能希望晚點再來探索這些選項， Laravel 提供了 [ Sail ](/docs/{{version}}/sail) ，一款讓你在使用 [ Docker ](https://www.docker.com) 時執行 Laravel 專案的內建方案。

Docker 是一款小型輕量的「容器」工具，用以執行應用程式及服務，而且不會影響你本機已經安裝的軟體或設定。這表示你不需要擔心本機複雜的開發工具設定，例如 web 伺服器和資料庫。想要啟動它，你只需要安裝 [ Docker Desktop ](https://www.docker.com/products/docker-desktop) 。

Laravel Sail 是一款輕量的命令行介面，用來和 Laravel 預設的 Docker 設定進行互動。 Sail 讓你能在沒有 Docker 經驗的情況下使用 PHP, MySQL, 和 Redis 建立 Laravel 應用程式提供了很棒的起頭。

> {tip} 已經是 Docker 專家？不用擔心！關於 Sail 的一切可以在 Laravel 內的 `docker-compose.yml` 檔案自行修改設定。 
=======
> **Note**  
> Already a Docker expert? Don't worry! Everything about Sail can be customized using the `docker-compose.yml` file included with Laravel.
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27

<a name="getting-started-on-macos"></a>
### 從 macOS 開始

如果你正在 Mac 進行開發且已經安裝了[ Docker Desktop ](https://www.docker.com/products/docker-desktop) ，你可以使用簡單的終端機指令建立一個全新的 Laravel 專案。舉個例子，建立一個目錄名稱叫「example-app」的 Laravel 應用，你可以在終端機執行以下指令：

```shell
curl -s "https://laravel.build/example-app" | bash
```

當然，你可以任意修改上面其中的「example-app」部分，只要確定專案名稱必須只能含有字母/數字、連接線、底線 (alpha-numeric characters, dashes, and underscores) ，Laravel 的應用目錄就會在你執行指令時被建立在指定的路徑。

<<<<<<< HEAD
Sail 應用程式容器在你本機上的安裝將會占用數分鐘。

當專案被建立之後，你可以到應用目錄中啟動 Laravel Sail ， Laravel Sail 提供簡易的執行介面與 Laravel 預設的 Docker 設定進行互動：
=======
Sail installation may take several minutes while Sail's application containers are built on your local machine.

After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration:
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27

```shell
cd example-app

./vendor/bin/sail up
```

<<<<<<< HEAD
只要應用程式的 Docker 容器被啟動，你可以在瀏覽器中存取你的應用程式： http://localhost 。

> {tip} 想繼續了解更多關於 Laravel Sail, 可以前往 [ Sail 完整說明文件 ](/docs/{{version}}/sail).
=======
Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost.

> **Note**  
> To continue learning more about Laravel Sail, review its [complete documentation](/docs/{{version}}/sail).
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27

<a name="getting-started-on-windows"></a>
### 從 Windows 開始

在你的 Windows 建立一個新的 Laravel 應用程式之前，先確定你已經安裝了 [ Docker Desktop ](https://www.docker.com/products/docker-desktop) 。接下來，你必須確保 Windows 子系統 Linux 2 版 (WSL2) 已經安裝並啟動。 WSL 會讓你在 Windows 10 可以執行 Linux 的二進位文件。如何安裝並啟動 WSL2 的資訊可以在微軟的 [ 開發者環境說明 ](https://docs.microsoft.com/en-us/windows/wsl/install-win10) 找到。

<<<<<<< HEAD
> {tip} 安裝並啟動 WSL2 之後，你必須確保 Docker Desktop 已經 [ 設定為使用 WSL2後端 ](https://docs.docker.com/docker-for-windows/wsl/)。
=======
> **Note**  
> After installing and enabling WSL2, you should ensure that Docker Desktop is [configured to use the WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/).
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27

接下來，你已經準備好建立你的第一個 Laravel 專案了。啟動 [ Windows 終端機 ](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)並為 WSL2 打開一個終端機程式。然後你可以使用簡單的終端機指令建立一個新的 Laravel 專案。舉個例子，建立一個目錄名稱叫「example-app」的 Laravel 應用，你可以在終端機執行以下指令：

```shell
curl -s https://laravel.build/example-app | bash
```

當然，你可以任意修改上面其中的「example-app」部分，只要確定專案名稱必須只能含有字母/數字、連接線、底線 (alpha-numeric characters, dashes, and underscores) ，Laravel 的應用目錄就會在你執行指令時被建立在指定的路徑。

<<<<<<< HEAD
當專案被建立之後，你可以到應用目錄中啟動 Laravel Sail ， Laravel Sail 提供簡易的執行介面與 Laravel 預設的 Docker 設定進行互動：
=======
Sail installation may take several minutes while Sail's application containers are built on your local machine.

After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration:
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27

```shell
cd example-app

./vendor/bin/sail up
```

<<<<<<< HEAD
只要應用程式的 Docker 容器被啟動，你可以在瀏覽器中存取你的應用程式： http://localhost 。

> {tip} 想繼續了解更多關於 Laravel Sail, 可以前往 [ Sail 完整說明文件 ](/docs/{{version}}/sail).

#### 在 WSL2 中開發
=======
Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost.

> **Note**  
> To continue learning more about Laravel Sail, review its [complete documentation](/docs/{{version}}/sail).
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27

當然，你會需要在 WSL2 中修改被建立的 Laravel 應用程式檔案。為此我們建議使用微軟的 [ Visual Studio Code ](https://code.visualstudio.com) 編輯器和他們的官方擴充套件 [ Remote Development ](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)

這些工具只要安裝過後，你可以在你專案根目錄內開啟 Windows 終端機執行 `code .` 指令來開啟任何一個 Laravel 專案。

<a name="getting-started-on-linux"></a>
### 從 Linux 開始

如果你正在 Linux 開發且已經安裝 [ Docker Compose ](https://docs.docker.com/compose/install/) ，你可以使用簡單的終端機指令建立一個新的 Laravel 專案。舉個例子，建立一個目錄名稱叫「example-app」的 Laravel 應用，你可以在終端機執行以下指令：

```shell
curl -s https://laravel.build/example-app | bash
```

當然，你可以任意修改上面其中的「example-app」部分，只要確定專案名稱必須只能含有字母或數字、連接線、底線 (alpha-numeric characters, dashes, and underscores) ，Laravel 的應用目錄就會在你執行指令時被建立在指定的路徑。

<<<<<<< HEAD
當專案被建立之後，你可以到應用目錄中啟動 Laravel Sail ， Laravel Sail 提供簡易的執行介面與 Laravel 預設的 Docker 設定進行互動：
=======
Sail installation may take several minutes while Sail's application containers are built on your local machine.

After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration:
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27

```shell
cd example-app

./vendor/bin/sail up
```

<<<<<<< HEAD
只要應用程式的 Docker 容器被啟動，你可以在瀏覽器中存取你的應用程式： http://localhost 。

> {tip} 想繼續了解更多關於 Laravel Sail, 可以前往 [ Sail 完整說明文件 ](/docs/{{version}}/sail).
=======
Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost.

> **Note**  
> To continue learning more about Laravel Sail, review its [complete documentation](/docs/{{version}}/sail).
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27

<a name="choosing-your-sail-services"></a>
### 選擇你的 Sail 服務

當你透過 Sail 建立一個新的 Laravel 應用程式，你可以使用 `with` 加上字串參數來選擇要在你新應用程式中的 `docker-compose.yml` 檔案設定哪些服務。目前可用的服務有 `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `minio`, `selenium`, 和 `mailhog`:

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

如果你不想指定這些參數，預設服務就會是 `mysql`, `redis`, `meilisearch`, `mailhog`, and `selenium`。

你可以安裝 [Devcontainer](/docs/{{version}}/sail#using-devcontainers) 後在 URL 加入 `devcontainer` 參數來指定 Sail 預設安裝的服務

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="initial-configuration"></a>
## 初始設定

所有 Laravel 框架的設定檔都被存在 `config` 目錄。每個選項都會被記錄，所以就放輕鬆去瀏覽那些檔案並熟悉哪些可用選項會為你派上用場。

Laravel 幾乎不需要額外的設定。你可以自由地開始開發！然而，你可能會希望觀看 `config/app.php` 檔案和文件。它包含了一些你可能想根據應用程式修改的選項，例如 `timezone` 和 `locale`。 

<a name="environment-based-configuration"></a>
### 環境基本設定

由於 Laravel 的許多選項設定是根據正在你本機執行的應用程式或是生產環境的 web 伺服器而有所不同，許多重要的設定值都是經由根目錄下的 `.env` 檔定義的。

你的 `.env` 檔不應該提交給你的應用程式版控。因為每個使用你的應用程式的開發者或伺服器可能需要不同的環境設定。而且，如果入侵者取得你專案原始碼的控制權限將會是個隱憂。

<<<<<<< HEAD

> {tip} 關於更多 `.env` 和環境基本設定的資訊，請閱讀完整的 [ 設定文件 ](/docs/{{version}}/configuration#environment-configuration)。

<a name="databases-and-migrations"></a>
### 資料庫和資料遷移

現在你已經建立了你的 Laravel 應用程式，你可能想要在一個資料庫儲存一些資料。預設狀態下，應用程式的 `.env` 設定檔會指定 Laravel 和 MySQL 資料庫互動，並將資料庫接駁到 `127.0.0.1` 。如果你正在 macOS 開發且需要本地安裝 MySQL, Postgres, 或 Redis, 你會發現用 [DBngin](https://dbngin.com/) 很方便。

如果你很不想在本機安裝 MySQL 或 PostgreSQL，你隨時可以使用 [SQLite](https://www.sqlite.org/index.html) 資料庫。 SQLite 是一款小型快速且獨立的資料庫引擎。首先，透過新增一個空白的 SQLite 檔案來建立一個 SQLite 資料庫。通常這個檔案會被存在 Laravel 應用程式的 `database` 目錄中：
=======
> **Note**  
> For more information about the `.env` file and environment based configuration, check out the full [configuration documentation](/docs/{{version}}/configuration#environment-configuration).

<a name="databases-and-migrations"></a>
### Databases & Migrations

Now that you have created your Laravel application, you probably want to store some data in a database. By default, your application's `.env` configuration file specifies that Laravel will be interacting with a MySQL database and will access the database at `127.0.0.1`. If you are developing on macOS and need to install MySQL, Postgres, or Redis locally, you may find it convenient to utilize [DBngin](https://dbngin.com/).

If you do not want to install MySQL or Postgres on your local machine, you can always use a [SQLite](https://www.sqlite.org/index.html) database. SQLite is a small, fast, self-contained database engine. To get started, create a SQLite database by creating an empty SQLite file. Typically, this file will exist within the `database` directory of your Laravel application:
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27

```shell
touch database/database.sqlite
```

<<<<<<< HEAD
接下來更新你的 `.env` 設定檔以使用 Laravel 的 `sqlite` 資料庫驅動程式。你可以刪除其他的資料庫設定選項：
=======
Next, update your `.env` configuration file to use Laravel's `sqlite` database driver. You may remove the other database configuration options:
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27

```ini
DB_CONNECTION=sqlite # [tl! add]
DB_CONNECTION=mysql # [tl! remove]
DB_HOST=127.0.0.1 # [tl! remove]
DB_PORT=3306 # [tl! remove]
DB_DATABASE=laravel # [tl! remove]
DB_USERNAME=root # [tl! remove]
DB_PASSWORD= # [tl! remove]
```

<<<<<<< HEAD
只要你設定過你的 SQLite 資料庫，你可以執行應用程式的 [ 資料遷移 ](/docs/{{version}}/migrations) 以建立你應用程式內資料庫的資料表 (tables)：
=======
Once you have configured your SQLite database, you may run your application's [database migrations](/docs/{{version}}/migrations), which will create your application's database tables:
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27

```shell
php artisan migrate
```

<a name="next-steps"></a>
## 下一步

現在你已經建立了你的 Laravel 專案，你可以會想知道接下來該學什麼。首先，我們強烈建議閱讀下列文件去熟悉 Laravel 的運作原理：

<div class="content-list" markdown="1">

<<<<<<< HEAD
- [ 請求的生命週期 ](/docs/{{version}}/lifecycle)
- [ 設定 ](/docs/{{version}}/configuration)
- [ 目錄結構 ](/docs/{{version}}/structure)
- [ 前端 ](/docs/{{version}}/frontend)
- [ 服務容器 ](/docs/{{version}}/container)
- [ Facades ](/docs/{{version}}/facades)
=======
- [Request Lifecycle](/docs/{{version}}/lifecycle)
- [Configuration](/docs/{{version}}/configuration)
- [Directory Structure](/docs/{{version}}/structure)
- [Frontend](/docs/{{version}}/frontend)
- [Service Container](/docs/{{version}}/container)
- [Facades](/docs/{{version}}/facades)
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27

</div>

你想如何使用 Laravel 將會決定你旅程的下一步。這裡有很多 Laravel 的用法，以下我們將探討兩個主要的框架用法：

<a name="laravel-the-fullstack-framework"></a>
### 將 Laravel 作為全端框架

<<<<<<< HEAD
Laravel 可以做為一個全端框架。「全端」框架就是你會使用 Laravel 將路由請求發送到你的應用程式且透過 [ Blade templates ](/docs/{{version}}/blade) 呈現出你的前端，或是像 [ Inertia ](https://inertiajs.com) 的單頁應用混合技術。這是 Laravel 框架最常見的使用方式，在我們看來，這也是 Laravel 最有成效的使用方式。

如果這是你計畫使用 Laravel 的方式，你可以會想要看看我們 [ 前端開發 ](/docs/{{version}}/frontend) 、 [ 路由 ](/docs/{{version}}/routing) 、 [ 視圖 ](/docs/{{version}}/views) ，或 [ Eloquent ORM ](/docs/{{version}}/eloquent) 的文件。此外你也可能想了解 [ Livewire ](https://laravel-livewire.com) 和 [ nertia ](https://inertiajs.com) 社群套件。這些套件允許你使用 Laravel 作為全端框架同時享受單頁式 JavaScript 應用程式提供的許多 UI 優勢。

如果你正在將 Laravel 用作全端框架，我們強烈建議你學習如何使用 [ Vite ](/docs/{{version}}/vite) 編譯你應用程式裡的 CSS 和 JavaScript。

> **Note**  
> 如果你想要快速建立你的應用程式，看看我們官方的 [ 應用程式入門套件 ](/docs/{{version}}/starter-kits)。
=======
Laravel may serve as a full stack framework. By "full stack" framework we mean that you are going to use Laravel to route requests to your application and render your frontend via [Blade templates](/docs/{{version}}/blade) or a single-page application hybrid technology like [Inertia](https://inertiajs.com). This is the most common way to use the Laravel framework, and, in our opinion, the most productive way to use Laravel.

If this is how you plan to use Laravel, you may want to check out our documentation on [frontend development](/docs/{{version}}/frontend), [routing](/docs/{{version}}/routing), [views](/docs/{{version}}/views), or the [Eloquent ORM](/docs/{{version}}/eloquent). In addition, you might be interested in learning about community packages like [Livewire](https://laravel-livewire.com) and [Inertia](https://inertiajs.com). These packages allow you to use Laravel as a full-stack framework while enjoying many of the UI benefits provided by single-page JavaScript applications.

If you are using Laravel as a full stack framework, we also strongly encourage you to learn how to compile your application's CSS and JavaScript using [Vite](/docs/{{version}}/vite).

> **Note**  
> If you want to get a head start building your application, check out one of our official [application starter kits](/docs/{{version}}/starter-kits).
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27

<a name="laravel-the-api-backend"></a>
### 將 Laravel 作為 API 後端

Laravel 也可以作為單頁式 JavaScript 應用程式或 行動應用程式的 API 後端。舉個例子，你可以能會使用 Laravel 作為你的 [ Next.js ](https://nextjs.org) 應用程式的 API 後端。在這種情況下，你可以使用 Laravel 為你的應用程式提供的 [ 身分驗證 ](/docs/{{version}}/sanctum) 和資料儲存、檢索，同時可以用上超有利的 Laravel 服務，例如佇列、電子郵件、通知等。

如果這是你計畫使用 Laravel 的方式，你可以會想要看看我們 [ 路由 ](/docs/{{version}}/routing) 、 [ Laravel Sanctum ](/docs/{{version}}/sanctum) 和 [ Eloquent ORM ](/docs/{{version}}/eloquent) 的文件。

> **Note**  
<<<<<<< HEAD
> 需要搶先建立 Laravel 後端和 Next.js 前端的結構？ Laravel Breeze 提供了 [ API 堆疊 ](/docs/{{version}}/starter-kits#breeze-and-next) 和 [ Next.js 前端實現 ](https://github.com/laravel/breeze-next) 讓你可以在幾分鐘內開始作業。
=======
> Need a head start scaffolding your Laravel backend and Next.js frontend? Laravel Breeze offers an [API stack](/docs/{{version}}/starter-kits#breeze-and-next) as well as a [Next.js frontend implementation](https://github.com/laravel/breeze-next) so you can get started in minutes.
>>>>>>> 5fa0b2b208db9d7fbd00d3b28438df4b7f3b1f27
