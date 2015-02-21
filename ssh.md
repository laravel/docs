# SSH

- [設定檔](#configuration)
- [基本用法](#basic-usage)
- [任務](#tasks)
- [SFTP 下載](#sftp-downloads)
- [SFTP 上傳](#sftp-uploads)
- [編輯遠端日誌](#tailing-remote-logs)
- [Envoy 任務執行](#envoy-task-runner)

<a name="configuration"></a>
## 設定檔

Laravel 可以簡單的方式 SSH 連線到遠端伺服器並執行命令，讓你可以簡單在遠端執行的建立 Artisan 任務。`SSH` facade 提供了使用方式讓你連線到遠端伺服器並執行命令。

設定檔放在 `config/remote.php`，裡面包含所有需要設定的遠端連線設定，`connections` 陣列裡有以伺服器名稱作為鍵值的列表。只要在 `connections` 陣列設定好認證，你就準備好可以執行遠端任務了。記得 `SSH` 可以經由密碼或 SSH key 認證。

> **提示：** 需要在遠端伺服器執行很多任務嗎？瞧瞧 [Envoy 任務執行](#envoy-task-runner)！

<a name="basic-usage"></a>
## 基本用法

#### 在在預設伺服器執行命令

使用 `SSH::run` 方法，在預設的遠端伺服器執行命令：

	SSH::run([
		'cd /var/www',
		'git pull origin master',
	]);

#### 在特定伺服器執行命令

你也可以使用 `into` 方法在特定的伺服器上執行命令：

	SSH::into('staging')->run([
		'cd /var/www',
		'git pull origin master',
	]);

#### 捕捉命令的輸出

你可以經由傳入閉合函數到 `run` 方法，捕捉遠端命令的即時輸出：

	SSH::run($commands, function($line)
	{
		echo $line.PHP_EOL;
	});

<a name="tasks"></a>
## 任務

如果你需要定義一組一起執行的命令，你可以用 `define` 方法定義一個「任務」：

	SSH::into('staging')->define('deploy', [
		'cd /var/www',
		'git pull origin master',
		'php artisan migrate',
	]);

你可以用 `task` 方法執行定義過的任務：

	SSH::into('staging')->task('deploy', function($line)
	{
		echo $line.PHP_EOL;
	});

<a name="sftp-downloads"></a>
## SFTP 下載

`SSH` 類別裡有簡單的方式可以下載檔案，使用 `get` 和 `getString` 方法：

	SSH::into('staging')->get($remotePath, $localPath);

	$contents = SSH::into('staging')->getString($remotePath);

<a name="sftp-uploads"></a>
## SFTP 上傳

`SSH` 類別裡也有簡單的方式可以上傳檔案或甚至是字串到遠端伺服器，使用 `put` 和 `putString` 方法：

	SSH::into('staging')->put($localFile, $remotePath);

	SSH::into('staging')->putString($remotePath, 'Foo');

<a name="tailing-remote-logs"></a>
## 編輯遠端日誌

Laravel 有一個有用的命令，可以讓你在任何遠端伺服器的 `laravel.log` 尾端附加日誌內容。使用 Artisan 的 `tail` 命令以及指定遠端連線的伺服器名稱：

	php artisan tail staging

	php artisan tail staging --path=/path/to/log.file

<a name="envoy-task-runner"></a>
## Envoy 任務執行

- [安裝](#envoy-installation)
- [執行任務](#envoy-running-tasks)
- [多伺服器](#envoy-multiple-servers)
- [平行執行](#envoy-parallel-execution)
- [任務巨集](#envoy-task-macros)
- [提醒通知](#envoy-notifications)
- [更新 Envoy](#envoy-updating-envoy)

Laravel Envoy 提供了簡潔，輕量的語法，定義在遠端伺服器執行的共同任務。使用 [Blade](/docs/templates#blade-templating) 風格的語法，你可以簡單的設置部署任務，執行 Artisan 命令或是更多。

> **提醒:** Envoy 需要 PHP 5.4 或更高的版本，並且只能在 Mac / Linux 作業系統下執行。

<a name="envoy-installation"></a>
### 安裝

首先，使用 Composer `global` 命令安裝 Envoy：

	composer global require "laravel/envoy=~1.0"

記得將 `~/.composer/vendor/bin` 路徑加入 PATH，如此在終端機執行 `envoy` 命令時才找得到。

再來，在專案根目錄建立 `Envoy.blade.php` 檔案。這裡有個範例可以讓你作為起頭：

	@servers(['web' => '192.168.1.1'])

	@task('foo', ['on' => 'web'])
		ls -la
	@endtask

如你所見，`@servers` 陣列建立在檔案的起始。你可以在宣告任務時，在 `on` 選項裡參照這些伺服器。在你的 `@task` 宣告裡，寫入想要在遠端伺服器執行的 Bash code。

`init` 命令可以簡單的建立一個基本的 Envoy 檔：

	envoy init user@192.168.1.1

<a name="envoy-running-tasks"></a>
### 執行任務

使用 `run` 命令去執行設定的任務：

	envoy run foo

如有需要，你可以傳入參數到 Envoy 檔案：

	envoy run deploy --branch=master

利用你所熟悉的 Blade 語法使用這些參數：

	@servers(['web' => '192.168.1.1'])

	@task('deploy', ['on' => 'web'])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

#### 啟動碼

你可以使用 ```@setup``` 語法，然後就能夠在 Envoy 檔案裡宣告 PHP 變數，以及執行一般的 PHP 程式碼：

	@setup
		$now = new DateTime();

		$environment = isset($env) ? $env : "testing";
	@endsetup

你也可以使用 ```@include``` 引入 PHP 檔案：

	@include('vendor/autoload.php');

<a name="envoy-multiple-servers"></a>
### 多伺服器

你可以簡單的在多個伺服器執行任務。只要在任務宣告裡列出伺服器名稱：

	@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

	@task('deploy', ['on' => ['web-1', 'web-2']])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

預設上，任務會循序的在每個伺服器上執行。意味著任務會在第一個伺服器執行完後，才換到下一個。

<a name="envoy-parallel-execution"></a>
### 平行執行

如果你想在多個伺服器上同時執行任務，只要簡單的在任務宣告裡加上 `parallel` 選項：

	@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

	@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
		cd site
		git pull origin {{ $branch }}
		php artisan migrate
	@endtask

<a name="envoy-task-macros"></a>
### 任務巨集

巨集讓你可以只要使用一個命令，就能夠循序執行一組任務。例如：

	@servers(['web' => '192.168.1.1'])

	@macro('deploy')
		foo
		bar
	@endmacro

	@task('foo')
		echo "HELLO"
	@endtask

	@task('bar')
		echo "WORLD"
	@endtask

現在 `deploy` 巨集可以經由一個簡單的命令執行：

	envoy run deploy

<a name="envoy-notifications"></a>
<a name="envoy-hipchat-notifications"></a>
### 提醒通知

#### HipChat

你可能想要在執行完任務後，發送通知到團隊的 HipChat 聊天室，使用簡單的 `@hipchat` 宣告：

	@servers(['web' => '192.168.1.1'])

	@task('foo', ['on' => 'web'])
		ls -la
	@endtask

	@after
		@hipchat('token', 'room', 'Envoy')
	@endafter

你也可以自定發送到 hipchat 聊天室的訊息，任何在 ```@setup``` 裡宣告，或是經由 ```@include``` 引入的變數都可以使用在訊息裡：

	@after
		@hipchat('token', 'room', 'Envoy', "$task ran on [$environment]")
	@endafter

這是一個令人驚豔的簡單方式，讓你的團隊保持通知在伺服器執行的任務。

#### Slack

下面的語法可以發送通知到 [Slack](https://slack.com)：

	@after
		@slack('team', 'token', 'channel')
	@endafter

<a name="envoy-updating-envoy"></a>
### 更新 Envoy

執行 `self-update` 命令即可簡單的更新 Envoy：

	envoy self-update

如果你的 Envoy 安裝在 `/usr/local/bin`，你可能需要加上 `sudo`：

	composer global update
