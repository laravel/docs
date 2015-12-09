# Envoy 任務執行器

- [簡介](#introduction)
- [撰寫任務](#writing-tasks)
    - [任務變數](#task-variables)
    - [多個伺服器](#envoy-multiple-servers)
    - [任務巨集](#envoy-task-macros)
- [執行任務](#envoy-running-tasks)
- [通知](#envoy-notifications)
    - [HipChat](#hipchat)
    - [Slack](#slack)

<a name="introduction"></a>
## 簡介

[Laravel Envoy](https://github.com/laravel/envoy) 提供了簡潔、輕量的語法，定義在遠端伺服器執行的共同任務。使用 Blade 風格的語法，你可以簡單的設置部署任務，執行 Artisan 指令或是更多。目前，Envoy 只支援 Mac 及 Linux 作業系統。

<a name="envoy-installation"></a>
### 安裝

首先，使用 Composer 的 `global` 指令安裝 Envoy：

    composer global require "laravel/envoy=~1.0"

記得將 `~/.composer/vendor/bin` 目錄加入至你的 PATH，如此一來當你在終端機執行 `envoy` 指令時 `envoy` 才可被執行。

#### 更新 Envoy

你也可以使用 Composer 讓你的 Envoy 保持安裝最新版本：

    composer global update

<a name="writing-tasks"></a>
## 撰寫任務

你所有的 Envoy 任務必須定義在專案根目錄的 `Envoy.blade.php` 檔案中。這裡有個範例可以幫助你瞭解：

    @servers(['web' => 'user@192.168.1.1'])

    @task('foo', ['on' => 'web'])
        ls -la
    @endtask

如你所見，`@servers` 的陣列被定義在檔案的起始，讓你可以在宣告任務時，在 `on` 選項裡參照這些伺服器。在你的 `@task` 宣告裡，你必須放置當任務執行時想要在遠端伺服器執行的 Bash 程式碼。

#### 啟動

有時，你可能想在啟動任務前執行一些 PHP 程式碼。你可以使用 ```@setup``` 指令在 Envoy 檔案理宣告變數及執行一般的 PHP 程式：

    @setup
        $now = new DateTime();

        $environment = isset($env) ? $env : "testing";
    @endsetup

你也可以使用 ```@include``` 來引入任何外部 PHP 檔案：

    @include('vendor/autoload.php');

#### 任務確認

如果你想要在伺服器執行你指定的任務之前進行確認，你可以增加 `confirm` 指令至你的任務宣告：

    @task('deploy', ['on' => 'web', 'confirm' => true])
        cd site
        git pull origin {{ $branch }}
        php artisan migrate
    @endtask

<a name="task-variables"></a>
### 任務變數

如果需要，你可以透過命令列選項傳遞變數至 Envoy 檔案，讓你能夠自訂你的任務：

    envoy run deploy --branch=master

你可以透過 Blade 的「echo」語法使用這些選項：

    @servers(['web' => '192.168.1.1'])

    @task('deploy', ['on' => 'web'])
        cd site
        git pull origin {{ $branch }}
        php artisan migrate
    @endtask

<a name="envoy-multiple-servers"></a>
### 多個伺服器

你可以簡單的在多個伺服器執行任務。首先，增加額外的伺服器至你的 `@server` 宣告。每個伺服器必須分配一個唯一的名稱。一旦你已經定義好額外的伺服器，就能簡單的在任務宣告的 `on` 陣列中列出這些伺服器：

    @servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

    @task('deploy', ['on' => ['web-1', 'web-2']])
        cd site
        git pull origin {{ $branch }}
        php artisan migrate
    @endtask

預設上，任務會循序的在每個伺服器上執行。意味著任務會在第一個伺服器執行完後，才換到下一個。

#### 平行執行

如果你想在多個伺服器上同時執行任務，只要簡單的在任務宣告裡加上 `parallel` 選項：

    @servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

    @task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
        cd site
        git pull origin {{ $branch }}
        php artisan migrate
    @endtask

<a name="envoy-task-macros"></a>
### 任務巨集

巨集讓你可以使用一個命令定義要循序執行的一組任務。以實例來說，一個 `deploy` 巨集可能會執行 `git` 及 `composer` 任務：

    @servers(['web' => '192.168.1.1'])

    @macro('deploy')
        git
        composer
    @endmacro

    @task('git')
        git pull origin master
    @endtask

    @task('composer')
        composer install
    @endtask

一旦該巨集被定義之後，你可以透過簡單的一行指令執行它們：

    envoy run deploy

<a name="envoy-running-tasks"></a>
## 執行任務

要從你的 `Envoy.blade.php` 檔案執行一個任務，只要執行 Envoy 的 `run` 指令，傳遞你想執行的任務或巨集指令名稱。Envoy 會執行該任務並顯示任務執行時的伺服器輸出。

    envoy run task

<a name="envoy-notifications"></a>
<a name="envoy-hipchat-notifications"></a>
## 通知

<a name="hipchat"></a>
### HipChat

在任務執行之後，你可以使用 Envoy 的 `@hipchat` 發送通知到團隊的 HipChat 聊天室。該指令接收 API token、聊天室名稱、及發送訊息時顯示的使用者名稱：

    @servers(['web' => '192.168.1.1'])

    @task('foo', ['on' => 'web'])
        ls -la
    @endtask

    @after
        @hipchat('token', 'room', 'Envoy')
    @endafter

如果你希望，你也可以自定發送到 HipChat 聊天室的訊息。任何在你的 Envoy 任務裡可用的變數都可以使用在訊息裡：

    @after
        @hipchat('token', 'room', 'Envoy', "{$task} ran in the {$env} environment.")
    @endafter

<a name="slack"></a>
### Slack

除了 HipChat 之外，Envoy 也支援發送通知至[Slack](https://slack.com)。`@slack` 指令接收 Slack hook 網址、頻道名稱、及你想發送至頻道的訊息：

    @after
        @slack('hook', 'channel', 'message')
    @endafter

當你在 Slack 的網站建立 `Incoming WebHooks` 時會取得一組 webhook 的網址。`hook` 參數必須是 Slack 的 Incoming WebHooks 所提供的整串網址。例如：

    https://hooks.slack.com/services/ZZZZZZZZZ/YYYYYYYYY/XXXXXXXXXXXXXXX

你可以提供下方的其中一種作為 channel 參數：

- 如果要發送通知至一個頻道：`#channel`
- 如果要發送通知給一位使用者：`@user`

