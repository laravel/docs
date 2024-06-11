# Laravel Sail

- [介紹](#介紹)
- [安裝和設置](#安裝和設置)
    - [將 Sail 安裝到現有應用程式](#將-sail-安裝到現有應用程式)
    - [重建 Sail 映像](#重建-sail-映像)
    - [配置 Shell 別名](#配置-shell-別名)
- [啟動和停止 Sail](#啟動和停止-sail)
- [執行指令](#執行指令)
    - [執行 PHP 指令](#執行-php-指令)
    - [執行 Composer 指令](#執行-composer-指令)
    - [執行 Artisan 指令](#執行-artisan-指令)
    - [執行 Node / NPM 指令](#執行-node-npm-指令)
- [與資料庫互動](#與資料庫互動)
    - [MySQL](#mysql)
    - [Redis](#redis)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [文件存儲](#文件存儲)
- [運行測試](#運行測試)
    - [Laravel Dusk](#laravel-dusk)
- [預覽電子郵件](#預覽電子郵件)
- [容器 CLI](#容器-cli)
- [PHP 版本](#php-版本)
- [Node 版本](#node-版本)
- [分享您的網站](#分享您的網站)
- [使用 Xdebug debug](#使用-xdebug-debug)
  - [Xdebug CLI 用法](#xdebug-cli-用法)
  - [Xdebug 瀏覽器用法](#xdebug-瀏覽器用法)
- [定制化](#定制化)

<a name="介紹"></a>
## 介紹

[Laravel Sail](https://github.com/laravel/sail) 是一個輕量級的指令行工具，用於與 Laravel 的預設 Docker 開發環境進行互動。Sail 提供了一個很好的起點，用於使用 PHP、MySQL 和 Redis 構建 Laravel 應用程式，而不需要事先了解 Docker。

Sail 的核心是 `docker-compose.yml` 文件和儲存在專案根目錄中的 `sail` 腳本。`sail` 腳本提供了一個方便的方法來與 `docker-compose.yml` 文件定義的 Docker 容器進行互動。

Laravel Sail 支援 macOS、Linux 和 Windows（透過 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)）。

<a name="安裝和設置"></a>
## 安裝和設置

Laravel Sail 會自動安裝在所有新建的 Laravel 應用程式中，因此您可以立即開始使用它。要了解如何創建新的 Laravel 應用程式，請參考 Laravel 的 [安裝文檔](/docs/{{version}}/installation#docker-installation-using-sail) 以了解您作業系統的具體步驟。在安裝過程中，您將被要求選擇應用程式將與哪些 Sail 支援的服務進行互動。

<a name="將-sail-安裝到現有應用程式"></a>
### 將 Sail 安裝到現有應用程式

如果您希望在現有的 Laravel 應用程式中使用 Sail，您可以使用 Composer 套件管理器安裝 Sail。當然，這些步驟假設您的現有本地開發環境允許您安裝 Composer 依賴：

```shell
composer require laravel/sail --dev
```

安裝 Sail 後，您可以運行 `sail:install` Artisan 指令。此指令將會將 Sail 的 `docker-compose.yml` 文件發布到應用程式的根目錄，並修改 `.env` 文件以包含連接到 Docker 服務所需的環境變數：

```shell
php artisan sail:install
```

最後，您可以啟動 Sail。要繼續學習如何使用 Sail，請繼續閱讀本文檔的其餘部分：

```shell
./vendor/bin/sail up
```

> [!WARNING]  
> 如果您使用的是 Docker Desktop for Linux，應使用 `default` Docker 上下文，方法是執行以下指令：`docker context use default`。

<a name="添加其他服務"></a>
#### 添加其他服務

如果您希望在現有的 Sail 安裝中添加其他服務，可以運行 `sail:add` Artisan 指令：

```shell
php artisan sail:add
```

<a name="使用-devcontainers"></a>
#### 使用 Devcontainers

如果您希望在 [Devcontainer](https://code.visualstudio.com/docs/remote/containers) 中進行開發，可以在 `sail:install` 指令中提供 `--devcontainer` 選項。該選項將指示 `sail:install` 指令將預設的 `.devcontainer/devcontainer.json` 文件發布到應用程式的根目錄：

```shell
php artisan sail:install --devcontainer
```

<a name="重建-sail-映像"></a>
### 重建 Sail 映像

有時您可能希望完全重建 Sail 映像，以確保所有映像中的軟體套件和軟體都是最新的。您可以使用 `build` 指令來完成這個操作：

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="配置-shell-別名"></a>
### 配置 Shell 別名

預設情況下，Sail 指令是使用包含在所有新的 Laravel 應用程式中的 `vendor/bin/sail` 腳本來呼叫的：

```shell
./vendor/bin/sail up
```

但是，與其反覆輸入 `vendor/bin/sail` 來執行 Sail 指令，您可能希望配置一個 shell 別名，以便更輕鬆地執行 Sail 的指令：

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

為了確保這一直可用，您可以將此添加到主目錄中的 shell 配置檔案中，例如 `~/.zshrc` 或 `~/.bashrc`，然後重新啟動您的 shell。

配置好 shell 別名後，您可以通過簡單輸入 `sail` 來執行 Sail 指令。本檔接下來的範例將假定您已配置此別名：

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## 啟動和停止 Sail

Laravel Sail 的 `docker-compose.yml` 文件定義了多個 Docker 容器，它們協同工作以幫助您構建 Laravel 應用程式。這些容器中的每一個都是 `docker-compose.yml` 文件中 `services` 配置的一部分。`laravel.test` 容器是主要的應用程式容器，將為您的應用程式提供服務。

在啟動 Sail 之前，您應確保本地電腦上沒有其他網頁伺服器或資料庫在運行。要啟動應用程式的 `docker-compose.yml` 文件中定義的所有 Docker 容器，您應該執行 `up` 指令：

```shell
sail up
```

要在背景中啟動所有 Docker 容器，您可以以「分離」模式啟動 Sail：

```shell
sail up -d
```

一旦應用程式的容器啟動後，您可以在網頁瀏覽器中訪問該專案： http://localhost。

要停止所有容器，您可以簡單地按 Control + C 來停止容器的運行。或者，如果容器在背景中運行，您可以使用 `stop` 指令：

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 執行指令

使用 Laravel Sail 時，您的應用程式在 Docker 容器中執行，與本地電腦隔離。然而，Sail 提供了一種方便的方法來對應用程式運行各種指令，例如任意的 PHP 指令、Artisan 指令、Composer 指令和 Node / NPM 指令。

**在閱讀 Laravel 文檔時，您經常會看到提到 Composer、Artisan 和 Node / NPM 指令而未提及 Sail。** 這些範例假設這些工具已安裝在您的本地電腦上。如果您在本地 Laravel 開發環境中使用 Sail，您應該使用 Sail 執行這些指令：

```shell
# 在本地運行 Artisan 指令...
php artisan queue:work

# 在 Laravel Sail 中運行 Artisan 指令...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### 執行 PHP 指令

PHP 指令可以使用 `php` 指令來執行。當然，這些指令將使用為您的應用程式配置的 PHP 版本來執行。要了解有關 Laravel Sail 可用的 PHP 版本的更多信息，請參閱 [PHP 版本文檔](#sail-php-versions)：

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### 執行 Composer 指令

Composer 指令可以使用 `composer` 指令來執行。Laravel Sail 的應用程式容器包括一個 Composer 安裝：

```nothing
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
#### 為現有應用程式安裝 Composer 依賴項

如果您正在與團隊一起開發應用程式，您可能不是最初創建 Laravel 應用程式的人。因此，在您將應用程式的資料倉儲（repository）克隆（clone）到本地電腦後，應用程式的任何 Composer 依賴項，包括 Sail，都不會被安裝。

您可以通過導航到應用程式的目錄並執行以下指令來安裝應用程式的依賴項。此指令使用一個包含 PHP 和 Composer 的小型 Docker 容器來安裝應用程式的依賴項：

```shell
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    laravelsail/php83-composer:latest \
    composer install --ignore-platform-reqs
```

使用 `laravelsail/phpXX-composer` 映像時，應使用您計劃用於應用程式的相同 PHP 版本（`80`、`81`、`82` 或 `83`）。

<a name="executing-artisan-commands"></a>
### 執行 Artisan 指令

Laravel Artisan 指令可以使用 `artisan` 指令來執行：

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### 執行 Node / NPM 指令

Node 指令可以使用 `node` 指令來執行，而 NPM 指令可以使用 `npm` 指令來執行：

```shell
sail node --version

sail npm run dev
```

如果您願意，您可以使用 Yarn 替代 NPM：

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 與資料庫互動

<a name="mysql"></a>
### MySQL

如您所見，您的應用程式的 `docker-compose.yml` 文件中包含一個 MySQL 容器的條目。此容器使用 [Docker volume](https://docs.docker.com/storage/volumes/)，因此即使在停止和重啟容器時，存儲在資料庫中的資料也會被持久化。

此外，MySQL 容器首次啟動時，將為您創建兩個資料庫。第一個資料庫使用您的 `DB_DATABASE` 環境變數的值命名，用於本地開發。第二個是名為 `testing` 的專用測試資料庫，將確保您的測試不會干擾您的開發資料。

啟動容器後，您可以通過將應用程式的 `.env` 文件中的 `DB_HOST` 環境變數設置為 `mysql` 來連接到應用程式內的 MySQL 實例。

要從本地電腦連接到應用程式的 MySQL 資料庫，您可以使用圖形化資料庫管理應用程式，如 [TablePlus](https://tableplus.com)。預設情況下，MySQL 資料庫可在 `localhost` port 3306 訪問，訪問憑證對應於您的 `DB_USERNAME` 和 `DB_PASSWORD` 環境變數的值。或者，您可以作為 `root` 用戶連接，該用戶也使用您的 `DB_PASSWORD` 環境變數的值作為密碼。

<a name="redis"></a>
### Redis

您的應用程式的 `docker-compose.yml` 文件中還包含一個 [Redis](https://redis.io) 容器的條目。此容器使用 [Docker volume](https://docs.docker.com/storage/volumes/)，因此即使在停止和重啟容器時，存儲在 Redis 中的資料也會被持久化。啟動容器後，您可以通過將應用程式的 `.env` 文件中的 `REDIS_HOST` 環境變數設置為 `redis` 來連接到應用程式內的 Redis 實例。

要從本地電腦連接到應用程式的 Redis 資料庫，您可以使用圖形化資料庫管理應用程式，如 [TablePlus](https://tableplus.com)。預設情況下，Redis 資料庫可在 `localhost` port 6379 訪問。

<a name="meilisearch"></a>
### Meilisearch

如果您在安裝 Sail 時選擇安裝 [Meilisearch](https://www.meilisearch.com) 

服務，則您的應用程式的 `docker-compose.yml` 文件中將包含這個強大搜索引擎的條目，該引擎與 [Laravel Scout](/docs/{{version}}/scout) [相容](https://github.com/meilisearch/meilisearch-laravel-scout)。啟動容器後，您可以通過將 `MEILISEARCH_HOST` 環境變數設置為 `http://meilisearch:7700` 來連接到應用程式內的 Meilisearch 實例。

從本地電腦，您可以在網頁瀏覽器中導航到 `http://localhost:7700` 訪問 Meilisearch 的基於網頁的管理面板。

<a name="typesense"></a>
### Typesense

如果您在安裝 Sail 時選擇安裝 [Typesense](https://typesense.org) 服務，則您的應用程式的 `docker-compose.yml` 文件中將包含這個超快的開源搜索引擎的條目，該引擎與 [Laravel Scout](/docs/{{version}}/scout#typesense) 原生整合。啟動容器後，您可以通過設置以下環境變數來連接到應用程式內的 Typesense 實例：

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

從本地電腦，您可以通過 `http://localhost:8108` 訪問 Typesense 的 API。

<a name="file-storage"></a>
## 文件存儲

如果您計劃在應用程式的正式環境中使用 Amazon S3 來存儲文件，您可能希望在安裝 Sail 時安裝 [MinIO](https://min.io) 服務。MinIO 提供了一個與 S3 相容的 API，您可以使用它在本地使用 Laravel 的 `s3` 文件存儲驅動進行開發，而無需在正式 S3 環境中創建「測試」存儲桶。如果您選擇在安裝 Sail 時安裝 MinIO，則會在應用程式的 `docker-compose.yml` 文件中添加 MinIO 配置部分。

預設情況下，您的應用程式的 `filesystems` 配置文件已包含一個 `s3` 磁碟配置。除了使用此磁碟與 Amazon S3 互動外，您還可以通過簡單地修改控制其配置的相關環境變數，使用它與任何與 S3 相容的文件存儲服務（如 MinIO）互動。例如，在使用 MinIO 時，您的文件系統環境變數配置應如下所示：

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

為了讓 Laravel 的 Flysystem 集成在使用 MinIO 時生成正確的 URL，您應該定義 `AWS_URL` 環境變數，以使其匹配應用程式的本地 URL 並在 URL 路徑中包含存儲桶名稱：

```ini
AWS_URL=http://localhost:9000/local
```

您可以通過 MinIO 控制台創建存儲桶，該控制台可在 `http://localhost:8900` 訪問。MinIO 控制台的預設用戶名為 `sail`，預設密碼為 `password`。

> [!WARNING]  
> 使用 `temporaryUrl` 方法生成臨時存儲 URL 時，不支援使用 MinIO。

<a name="running-tests"></a>
## 運行測試

Laravel 開箱即提供了令人驚嘆的測試支援，您可以使用 Sail 的 `test` 指令來運行您的應用程式的[功能和單元測試](/docs/{{version}}/testing)。Pest / PHPUnit 接受的任何 CLI 選項也可以傳遞給 `test` 指令：

```shell
sail test

sail test --group orders
```

Sail 的 `test` 指令等同於運行 `test` Artisan 指令：

```shell
sail artisan test
```

預設情況下，Sail 會創建一個專用的 `testing` 資料庫，以確保您的測試不會干擾當前資料庫的狀態。在預設的 Laravel 安裝中，Sail 還會配置您的 `phpunit.xml` 文件，以便在執行測試時使用此資料庫：

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk) 提供了一個表達性強且易於使用的瀏覽器自動化和測試 API。多虧了 Sail，您可以在不安裝 Selenium 或其他工具的情況下運行這些測試。要開始，請取消註釋應用程式的 `docker-compose.yml` 文件中的 Selenium 服務：

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

接下來，確保應用程式的 `docker-compose.yml` 文件中的 `laravel.test` 服務具有 `depends_on` 條目來依賴 `selenium`：

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

最後，您可以啟動 Sail 並運行 `dusk` 指令來運行您的 Dusk 測試套件：

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon 上的 Selenium

如果您的本地機器包含 Apple Silicon 晶片，則您的 `selenium` 服務必須使用 `seleniarm/standalone-chromium` 映像：

```yaml
selenium:
    image: 'seleniarm/standalone-chromium'
    extra_hosts:
        - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<a name="previewing-emails"></a>
## 預覽電子郵件

Laravel Sail 的預設 `docker-compose.yml` 文件包含 [Mailpit](https://github.com/axllent/mailpit) 服務的條目。Mailpit 會攔截應用程式在本地開發期間發送的電子郵件，並提供一個方便的網頁界面，讓您可以在瀏覽器中預覽電子郵件訊息。使用 Sail 時，Mailpit 的預設主機是 `mailpit`，並通過 1025 port可用：

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

當 Sail 運行時，您可以訪問 Mailpit 網頁界面：http://localhost:8025

<a name="sail-container-cli"></a>
## 容器 CLI

有時您可能希望在應用程式的容器內啟動一個 Bash session。您可以使用 `shell` 指令連接到應用程式的容器，允許您檢查其文件和已安裝的服務，以及在容器內執行任意的 shell 指令：

```shell
sail shell

sail root-shell
```

要啟動一個新的 [Laravel Tinker](https://github.com/laravel/tinker) session，您可以執行 `tinker` 指令：

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 版本

Sail 目前支援通過 PHP 8.3、8.2、8.1 或 PHP 8.0 來提供應用程式服務。Sail 目前使用的預設 PHP 版本是 PHP 8.3。要更改用於提供應用程式服務的 PHP 版本，您應該更新應用程式的 `docker-compose.yml` 文件中的 `laravel.test` 容器的 `build` 定義：

```yaml
# PHP 8.3
context: ./vendor/laravel/sail/runtimes/8.3

# PHP 8.2
context: ./vendor/laravel/sail/runtimes/8.2

# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0
```

此外，您可能希望更新您的 `image` 名稱以反映應用程式使用的 PHP 版本。此選項也在應用程式的 `docker-compose.yml` 文件中定義：

```yaml
image: sail-8.2/app
```

更新應用程式的 `docker-compose.yml` 文件後，您應該重新構建您的容器映像：

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 版本

Sail 預設安裝 Node 20。要更改構建映像時安裝的 Node 版本，您可以更新應用程式的 `docker-compose.yml` 文件中的 `laravel.test` 服務的 `build.args` 定義：

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

更新應用程式的 `docker-compose.yml` 文件後，您應該重新構建您的容器映像：

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 分享您的網站

有時您可能需要公開分享您的網站，以便為同事預覽或測試應用程式的 Webhook 集成。要分享您的網站，您可以使用 `share` 指令。執行此指令後，您將獲得一個隨機的 `laravel-sail.site` URL，您可以使用該 URL 訪問您的應用程式：

```shell
sail share
```

通過 `share` 指令分享您的網站時，您應該使用應用程式的 `bootstrap/app.php` 文件中的 `trustProxies` 中介軟體方法配置應用程式的受信代理。否則，`url` 和 `route` 等 URL 生成助手將無法確定在 URL 生成期間應使用的正確 HTTP 主機：

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->trustProxies(at: [
            '*',
        ]);
    })

如果您希望選擇共享網站的子域名，可以在執行 `share` 指令時提供 `subdomain` 選項：

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]  
> `share` 指令由 [Expose](https://github.com/beyondcode/expose) 提供支援，這是一個由 [BeyondCode](https://beyondco.de) 開發的開源隧道服務。

<a name="debugging-with-xdebug"></a>
## 使用 Xdebug debugging

Laravel Sail 的 Docker 配置包括對 [Xdebug](https://xdebug.org/) 的支援，這是一個流行且強大的 PHP debugger。為了啟用 Xdebug，您需要將一些變數添加到應用程式的 `.env` 文件中來 [配置 Xdebug](https://xdebug.org/docs/step_debug#mode)。要啟用 Xdebug，您必須在啟動 Sail 之前設置適當的模式：

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

#### Linux 主機 IP 配置

在內部，`XDEBUG_CONFIG` 環境變數被定義為 `client_host=host.docker.internal`，以便為 Mac 和 Windows（WSL2）正確配置 Xdebug。如果您的本地機器運行的是 Linux，您應確保正在運行 Docker Engine 17.06.0+ 和 Compose 1.16.0+。否則，您將需要手動定義此環境變數，如下所示。

首先，您應該通過運行以下指令確定要添加到環境變數的正確主機 IP 地址。通常，`<container-name>` 應為提供應用程式服務的容器的名稱，通常以 `_laravel.test_1` 結尾：

```shell
docker inspect -f {{range.NetworkSettings.Networks}}{{.Gateway}}{{end}} <container-name>
```

獲得正確的主機 IP 地址後，您應在應用程式的 `.env` 文件中定義 `SAIL_XDEBUG_CONFIG` 變數：

```ini
SAIL_XDEBUG_CONFIG="client_host=<host-ip-address>"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 用法

可以使用 `sail debug` 指令在運行 Artisan 指令時啟動debug session：

```shell
# 在沒有 Xdebug 的情況下運行 Artisan 指令...
sail artisan migrate

# 在有 Xdebug 的情況下運行 Artisan 指令...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 瀏覽器用法

要在通過網頁瀏覽器與應用程式互動時debug應用程式，請按照 [Xdebug 提供的說明](https://xdebug.org/docs/step_debug#web-application) 從網頁瀏覽器啟動 Xdebug session。

如果您使用的是 PhpStorm，請查看 JetBrain 關於 [零配置debug](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) 的文檔。

> [!WARNING]  
> Laravel Sail 依賴於 `artisan serve` 來提供應用程式服務。`artisan serve` 指令僅接受 `XDEBUG_CONFIG` 和 `XDEBUG_MODE` 變數，從 Laravel 版本 8.53.0 開始。較早版本的 Laravel（8.52.0 及以下）不支援這些變數，將不接受debug連接。

<a name="sail-customization"></a>
## 自訂

由於 Sail 只是 Docker，您可以自由地自訂幾乎所有內容。要發佈 Sail 的 Dockerfile，您可以執行 `sail:publish` 指令：

```shell
sail artisan sail:publish
```

運行此指令後，用於 Laravel Sail 的 Dockerfile 和其他配置文件將被放置在應用程式根目錄中的 `docker` 目錄中。自訂 Sail 安裝後，您可能希望更改應用程式容器的映像名稱，這可以在應用程式的 `docker-compose.yml` 文件中完成。完成後，使用 `build` 指令重新構建應用程式的容器。為應用程式映像分配一個唯一名稱特別重要，如果您在單台機器上使用 Sail 開發多個 Laravel 應用程式：

```shell
sail build --no-cache
```
