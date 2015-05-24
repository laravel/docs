# 套件開發

- [簡介](#introduction)
- [視圖](#views)
- [語言](#translations)
- [設定檔](#configuration)
- [公用資源](#public-assets)
- [發佈分類檔案](#publishing-file-groups)
- [路由](#routing)

<a name="introduction"></a>
## 簡介

套件是擴增功能到 Laravel 的主要方式。套件可以包含許多好用的功能，像 [Carbon](https://github.com/briannesbitt/Carbon) 用於處理時間，或像 [Behat](https://github.com/Behat/Behat) 這種完整的 BDD 測試框架。

當然，有非常多不同類型的套件。有些套件是獨立運作的，意思是指他們並不相依於任何框架，包括 Laravel。剛剛所提到的 Carbon 及 Behat 就是這種套件。要使用這種套件只需要在 `composer.json` 檔案裡引入它們即可。

另一方面，有些套件特別指定要與 Laravel 整合。這些套件可能包含路由、控制器、視圖以及套件的相關設定，目標是增強 Laravel 本身的功能。這份指南裡將主要以開發 Laravel 專屬的套件為目標進行說明。

所有的 Laravel 套件都會透過 [Packagist](http://packagist.org) 及 [Composer](http://getcomposer.org) 進行發佈，因此學習如何使用這些美好的 PHP 套件發佈工具是一個必經的過程。

<a name="views"></a>
## 視圖

你的套件內部之架構完全取決於你；但是，原則上每個套件都會有一個或多個[服務提供者](/docs/{{version}}/providers)。服務提供者包含著所有[服務容器](/docs/{{version}}/container)的綁定，也定義了所有套件的相關設定、視圖以及語言檔案的所在位置。

### 視圖

套件的視圖基本上使用雙冒號「命名空間」語法來引用：

	return view('package::view.name');

你所需要做的就是告訴 Laravel ，給定的命名空間所對應的視圖位置。如果你的套件取名為「courier」，你可以按照以下方式新增至你的服務提供者的 `boot` 方法：

	public function boot()
	{
		$this->loadViewsFrom(__DIR__.'/path/to/views', 'courier');
	}

現在你可以使用下方的語法來載入套件的視圖：

	return view('courier::view.name');

當你使用 `loadViewsFrom` 方法時，Laravel 實際上為了你的視圖註冊了**兩個位置**。一個是應用程式的 `resources/views/vendor` 目錄，另一個是你所指定的目錄。以我們使用的 `courier` 為例：當請求一個套件的視圖時，Laravel 會在第一時間檢查 `resources/views/vendor/courier` 是否有一個開發者自訂的視圖存在。如果這個路徑沒有自訂的視圖，Laravel 會搜尋你在套件 `loadViewsFrom` 方法裡所指定的視圖路徑。這個方法讓使用者可以方便的自訂或覆寫你的套件裡的視圖。

#### 視圖的發佈

若要發佈套件的視圖至 `resources/views/vendor` 目錄，你必須在服務提供者裡的 `boot` 方法裡使用 `publishes` 方法：

	public function boot()
	{
		$this->loadViewsFrom(__DIR__.'/path/to/views', 'courier');

		$this->publishes([
			__DIR__.'/path/to/views' => base_path('resources/views/vendor/courier'),
		]);
	}

現在當你套件的使用者使用 Laravel 的 `vendor:publish` 指令時，你的視圖目錄將會被複製到指定的目錄。

如果您想要覆寫已存在的檔案，可以使用 `--force` 切換：

	php artisan vendor:publish --force

> **注意：** 你可以使用 `publishes` 方法發佈**任何**類型的檔案到任何你想要的地方。

<a name="translations"></a>
## 語言

套件的語言檔案基本上使用雙冒號語法來引用：

	return trans('package::file.line');

你所要做的只有告訴 Laravel ，給定的命名空間所對應的語言檔案位置。如果你的套件取名為「courier」，你可以按照以下方式新增至你的服務提供者的 `boot` 方法：

	public function boot()
	{
		$this->loadTranslationsFrom(__DIR__.'/path/to/translations', 'courier');
	}

請注意，在你的 `translations` 目錄裡，必須對每個語言有更下一層的目錄，例如 `en`、`es`、`ru`、等等。

現在你可以使用下方的語法來載入你的套件語言:

	return trans('courier::file.line');

<a name="configuration"></a>
## 設定檔

基本上，您可能想要將你套件的設定檔發佈到應用程式本身的 `config` 目錄。這能夠讓您套件的使用者輕鬆的覆寫這些預設的設定選項。

如果要發佈套件的設定檔，只需要在服務提供者裡的 `boot` 方法裡使用 `publishes` 方法:

	$this->publishes([
		__DIR__.'/path/to/config/courier.php' => config_path('courier.php'),
	]);

現在當你套件的使用者使用 Laravel 的 `vendor:publish` 指令時，你的檔案將會被複製到指定的位置。當然，只要你的設定檔案被發佈後，就可以如其他設定檔一樣被存取：

	$value = config('courier.option');

你也可以選擇合併你的套件設定檔和應用程式裡的副本設定檔。這樣能夠讓你的使用者在已經發佈的副本設定檔裡只包含他們想要覆寫的設定選項。如果想要合併設定檔，可在服務提供者裡的 `register` 方法裡使用 `mergeConfigFrom`方法：

	$this->mergeConfigFrom(
		__DIR__.'/path/to/config/courier.php', 'courier'
	);

<a name="public-assets"></a>
## 公用資源

你的套件可能會有像是 JavaScript，CSS，及圖片的資源。如果要發布資源，只需要在服務提供者裡的 `boot` 方法裡使用 `publishes` 方法。在這個例子中，我們也會增加一個「Public」的資源分類標籤。

	$this->publishes([
		__DIR__.'/path/to/assets' => public_path('vendor/courier'),
	], 'public');

現在當你套件的使用者使用 `vendor:publish` 指令時，你的檔案將會被複製到指定的位置。當每次套件更新需要複寫資源時，你可以使用 `--force` 標記：

	php artisan vendor:publish --tag=public --force

如果你想要確保你的公用資源始終保持在最新的版本，可以將此指令加入你的 `composer.json` 中的 `post-update-cmd` 列表。

<a name="publishing-file-groups"></a>
## 發佈分類檔案

您可能想要分別的發佈一些分類的檔案。舉例來說，你可能想要你的使用者可以分別發佈套件的設定檔與資源檔。你可以使用 `tagging` 來達成:

	// Publish a config file
	$this->publishes([
		__DIR__.'/../config/package.php' => config_path('package.php')
	], 'config');

	// Publish your migrations
	$this->publishes([
		__DIR__.'/../database/migrations/' => database_path('/migrations')
	], 'migrations');

你可以使用這些 `tag`，來分別發佈這些套件裡的檔案。

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
