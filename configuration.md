# 設定

- [簡介](#introduction)
- [環境設定](#environment-configuration)
- [供應商設定](#provider-configuration)
- [保護敏感設定](#protecting-sensitive-configuration)
- [維護模式](#maintenance-mode)

<a name="introduction"></a>
## 簡介

所有關於 Laravel 框架的設定文件都被放置在 `app/config` 目錄下。每個文件裡的所有選項都有文件，因此你可以輕鬆地察看這些文件，並且熟悉這些選項配置。

有時候，你可能在運行時需要存取這些設定值，你可以使用 `Config` 類別：

#### 存取一個選項的值

	Config::get('app.timezone');

如果選項值不存在，你可以指定一個預設值：

	$timezone = Config::get('app.timezone', 'UTC');

#### 設定選項值

注意，"點"式語法可以用來存取不同設定文件裡的選項。你還可以在運行階段更改設定值:

	Config::set('database.default', 'sqlite');

在運行階段設定的選項值只在該次請求中有效，不會對其他的請求造成影響。

<a name="environment-configuration"></a>
## 環境配置
通常應用程式常常需要根據不同的運行環境而有不同的配置設定值。例如，你會希望在你的本地開發機器上會有與正式環境不同的緩存驅動（cache driver），透過設定檔案，這是非常容易達成的。

在 `config` 目錄下建立與環境名稱相同的目錄，例如 `local`。接下來，創建你想要覆寫的設定文件，並且設定該環境所希望的設定值。例如，你要在 `app/config/local` 建立 `cache.php` 檔案，內容如下：

	<?php

	return array(

		'driver' => 'file',

	);

> **註:** 請勿使用 'testing' 當作環境名稱，它是專門為單元測試保留的。

注意，你不需要為基本設定文件中的_所有_選項設定選項值，只需要指定你需要覆蓋的配置選項即可。環境配置文件將會以 "cascade" 的方式覆蓋基本設定文件。

接下來，我們需要讓框架知道如何確認其運行環境。預設環境是 `production`。然而，你可以在安裝目錄下的 `bootstrap/environment.php` 文件中設定其他環境。在該文件中，你可以找到 `$app->detectEnvironment` 函式。該陣列將會用來偵測當前的運行環境。你可以根據你的需求增加環境或者是機器名稱。

    <?php

    $env = $app->detectEnvironment(array(

        'local' => array('your-machine-name'),

    ));

在這個範例中，'local' 是運行環境的名稱而 'your-machine-name' 是你的服務器的主機名稱。在 Linux 和 Mac 上，你可以透過命令列執行 `hostsname` 查到你的主機名稱。

如果你想要更靈活的環境偵測方式，可以傳遞一個 `閉包（Closure）` 給 `detectEnvironment` 函式，這樣你就可以按照你想要的方式偵測了：

	$env = $app->detectEnvironment(function()
	{
		return $_SERVER['MY_LARAVEL_ENV'];
	});

#### 存取目前的運行環境

你也可以透過 `environment` 函式來取的目前運行階段的環境：

	$environment = App::environment();

你也可以傳遞參數至 `environment` 函式中，來確認目前的環境是否與參數相符合：

	if (App::environment('local'))
	{
		// 當環境為 local 時
	}

	if (App::environment('local', 'staging'))
	{
		// 環境為 local 或 staging...
	}

<a name="provider-configuration"></a>
### 供應商設定

當使用環境設定時，你會想要"附加"環境[服務供應商](/docs/ioc#service-providers) 到你主要的 `app` 設定檔中。然而，如果你這樣做，你會發現環境 `app` 供應商將會覆蓋掉你主要 `app` 設定檔的供應商。如果要附加供應商，在你的環境 `app` 設定檔中使用 `append_config` helper 方法：

	'providers' => append_config(array(
		'LocalOnlyServiceProvider',
	))

<a name="protecting-sensitive-configuration"></a>
## 保護敏感設定

對於一個"實際"的應用程式，讓敏感的設定不要放在你的設定檔中才是明智的抉擇。像是資料庫密碼, Stripe API 金鑰和加密金鑰都應該盡可能地不要存在設定檔中。所以，該放在哪裡？很慶幸的，Laravel 提供了一個非常簡單的方式：使用 "點開頭" 的檔案來保存這種類型的設定。

首先，[設定你的應用程式](/docs/configuration#environment-configuration)來識別你的機器是否在 `local` 環境中。然後創建一個 `.env.local.php` 檔案在你的專案最上層目錄中（一般而言與 `composer.json` 檔案同目錄)。`.env.local.php` 將會回傳一個鍵值組的陣列，類似於一般的 Laravel 設定檔：

	<?php

	return array(

		'TEST_STRIPE_KEY' => 'super-secret-sauce',

	);


所有在這個檔案中的鍵值組將會被回傳，並轉成 PHP 的超級全域變數 `$_ENV` 和 `$_SERVER`。你可以在你的設定檔中透過這些全域變數存取：

	'key' => $_ENV['TEST_STRIPE_KEY']

請確認將 `.env.local.php` 加進你的 	`.gitignore` 檔案中。他可以讓你的團隊成員可以創建自己的本機環境設定檔，也可以將敏感設定從版本控制系統中隱藏。

現在，在你的正式環境中，創建一個包含正式環境敏感設定值的 `.env.php` 於你專案的最上層目錄。如同 `.env.local.php`，正式環境的 `.env.php` 也不應該在版本控制系統中。

> **附註:** 你可以為每個有支援的環境創建所屬的設定檔案。例如，`development` 環境下，如果 `.env.development.php` 檔案若存在將會自動讀取進來。

<a name="maintenance-mode"></a>
## 維護模式

當你的應用程式處於維護模式時，所有的路由都會指向一個自定的視圖。當你要更新或進行維護作業時，“關閉”整個網站是很簡單的。`App::down` 函式已經定義在你的 `app/start/global.php` 檔案中。他將會在你的應用程式處於維護模式時將執行該函式，展現在用戶前。

啟用維護模式，只要執行 Artisan 指令 'down'：

	php artisan down

關閉維護模式，只要執行 Artisan 指令 'up'：

	php artisan up

如果你想要客製化維護模式的視圖，你只需要增加下面內容至應用程式裡的 `app/start/global.php` 檔案中：

	App::down(function()
	{
		return Response::view('maintenance', array(), 503);
	});

如果傳給 `down` 函式的閉包回傳 'NULL' 值，該此請求將會略過維護模式。

### 維護模式與隊列

當應用程式處於維護模式中，將不會處理任何[隊列工作](/docs/queues)。所有的隊列工作將會在應用程式離開維護模式後繼續被進行。