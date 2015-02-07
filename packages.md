# 套件開發

- [介紹](#introduction)
- [視圖](#views)
- [語言](#translations)
- [設定檔](#configuration)
- [發佈分類檔案](#publishing-file-groups)
- [路由](#routing)

<a name="introduction"></a>
## 介紹

開發套件是新增功能到 Laravel 最主要的方法。套件可以是任何處理日期的方式。例如，[Carbon](https://github.com/briannesbitt/Carbon)，或是一個全套的 BDD testing 框架。例如，[Behat](https://github.com/Behat/Behat)

當然，有非常多不同類型的套件。有些套件是獨立的，意思是此套件運作且相容於任何的框架，不只有 Laravel。Carbon 以及 Behat 都是這類的套件。任何這類的套件只需要在您的 `composer.json` 檔案裡設定就可以使用。

另一方面，其他的套件所設計的目的是只要在 Laravel 上使用。這些套件可能包含路由、控制器、視圖以及套件的相關設定，目的是為了增加 Laravel 的應用。接下來的說明主要涵蓋了 Laravel 開發這些套件的重點。

所有 Laravel 套件都發佈到 [Packagist](http://packagist.org) 以及 [Composer](http://getcomposer.org)，所以學習這些美好的 PHP 套件管理工具是必須的。

<a name="views"></a>
## 視圖

您套件內部的架構全部由您自己規劃。然而，原則上會有一個或更多的 [服務提供者](/docs/5.0/providers). 服務提供者包含著所有的 [IoC](/docs/5.0/container) 綁定，也定義了所有您套件的相關設定、視圖以及語言檔案在什麼地方。

### 視圖

套件的視圖基本上的指定使用兩個雙冒號:

	return view('package::view.name');

所有您所要做的只有告訴 Laravel 您所設定套件名稱視圖的位置在哪裡。如果您的套件取名為 “courier” 您可能需要新增如下到您的服務提供者的 `boot` 方法:

	public function boot()
	{
		$this->loadViewsFrom(__DIR__.'/path/to/views', 'courier');
	}

現在您可以使用如下的語法來載入套件的視圖:

	return view('courier::view.name');

當您使用 `loadViewsFrom` 方法，Laravel 實際上為了您的視圖註冊了**兩個位置**。一個是您應用程式的 `resources/views/vendor` 目錄，一個是您指定的目錄。所以使用我們的範例 `courier` 當要求一個套件的視圖時，Laravel 會第一時間檢查是否有一個開發者自行自訂在 `resources/views/vendor/courier` 的視圖存在。然而如果還沒有這個路徑的視圖被自訂。Laravel 會搜尋您在套件 `loadViewsFrom` 方法裡所指定的視圖。這個方法讓個別的使用者可以方便的自訂且覆寫您在套件裡的視圖。

#### 視圖的發佈

發佈套件的視圖到 `resources/views/vendor` 目錄，您必須在服務提供者裡的 `boot` 方法裡使用 `publishes` 方法:

	public function boot()
	{
		$this->loadViewsFrom(__DIR__.'/path/to/views', 'courier');

		$this->publishes([
			__DIR__.'/path/to/views' => base_path('resources/views/vendor/courier'),
		]);
	}

現在當您套件的使用者使用 Laravel 的指令 `vendor:publish` 您的視圖目錄將會被複製到所特定的目錄

如果您想要覆寫已存在的檔案，可以使用 `--force`:

	php artisan vendor:publish --force

> **注意:** 您可以使用 `publishes` 方法，發佈任何您的檔案到**任何**您想要的地方。

<a name="translations"></a>
## 語言

套件的語言檔案基本上的指定使用兩個雙冒號:

	return trans('package::file.line');

所有您所要做的只有告訴 Laravel 您所設定套件名稱的語言位置在哪裡。如果您的套件取名為 "courier" 您可能需要新增如下的語法到您的服務提供者的 `boot` 方法:

	public function boot()
	{
		$this->loadTranslationsFrom(__DIR__.'/path/to/translations', 'courier');
	}

注意在您的 `translations` 目錄裡，必須要有更下一層的目錄，例如 `en` `es` `ru`。

現在您可以使用下方的語法來載入您套件的語言:

	return trans('courier::file.line');

<a name="configuration"></a>
## 設定檔

基本上，您可能想要將您套件相關設定的檔案發佈到應用程式本身的設定目錄 `config`。這將允許您套件的使用者簡單的覆寫這些預設的設定檔案。

發佈套件的設定檔只需要在服務提供者裡的 `boot` 方法裡使用 `publishes` 方法:

	$this->publishes([
		__DIR__.'/path/to/config/courier.php' => config_path('courier.php'),
	]);

現在當套件的使用者執行 `vendor:publish` 指令，您的檔案將會被複製到特定的位置。當然只要設定檔案已經被發佈，就可以如其他設定檔一樣被存取:

	$value = config('courier.option');

您可能也選擇想要合併您套件的設定檔和應用程式裡的副本設定檔。這允許您的使用者在已經被發佈的副本設定檔裡只包含任何他們想要覆寫的設定選項。如果想要合併設定檔，可在服務提供者裡的 `register` 方法裡使用 `mergeConfigFrom`方法

	$this->mergeConfigFrom(
		__DIR__.'/path/to/config/courier.php', 'courier'
	);

<a name="publishing-file-groups"></a>
## 發佈分類檔案

您可能想要分別的發佈一些分類的檔案。舉例，您可能想要您的使用者可以分別發佈套件的設定檔與資產檔。您可以使用 `tagging` 來達成:

	// Publish a config file
	$this->publishes([
		__DIR__.'/../config/package.php', config_path('package.php')
	], 'config');

	// Publish your migrations
	$this->publishes([
		__DIR__.'/../database/migrations/' => base_path('/database/migrations')
	], 'migrations');

您可以使用這些 `tag`，來分別發佈這些套件裡的檔案。

	php artisan vendor:publish --provider="Vendor\Providers\PackageServiceProvider" --tag="config"

<a name="routing"></a>
## 路由

在套件裡載入一個路由檔案，只需要在服務提供者裡的 `boot` 方法裡使用 `include` :

#### 根據服務提供者來包含一個路由檔

	public function boot()
	{
		include __DIR__.'/../../routes.php';
	}

> **注意:** 如果您的套件裡使用了控制器，您必須要確認您在 `composer.json` 檔案裡的 auto-load 區塊裡，是否適當的設定這些控制器。
