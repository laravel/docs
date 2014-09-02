# 套件開發

- [簡介](#introduction)
- [建立一個套件](#creating-a-package)
- [套件結構](#package-structure)
- [服務提供者](#service-providers)
- [緩載提供者](#deferred-providers)
- [套件慣例](#package-conventions)
- [開發工作流程](#development-workflow)
- [套件路由](#package-routing)
- [套件設定](#package-configuration)
- [套件視圖](#package-views)
- [套件遷移](#package-migrations)
- [套件資產](#package-assets)
- [發佈套件](#publishing-packages)

<a name="introduction"></a>
## 簡介

套件是擴增 Laravel 的主要方式。套件可以是任何功能，比方說處理時間像 [Carbon](https://github.com/briannesbitt/Carbon) 或是 BDD 測試框架如 [Behat](https://github.com/Behat/Behat)。

當然，有各式各樣的套件。有些套件是獨立運作 (stand-alone) 的，意思是指他們並不相依任何框架，包括 Laravel 。剛提到的 Carbon 及 Behat 就是這種套件。要使用這種套件只需要在 `composer.json` 檔案裡引入它們即可。

另一方面，有些套件特別指定要與 Laravel 整合。這種型式的套件在前一代的 Laravel 裡稱做 Bundle。這種套件可能有路由、控制器、視圖、設定以及遷移，目標是增強 Laravel 本身的功能。由於沒有特別需求要開發獨立運作的套件，因此在這份指南裡將主要以開發 Laravel 專屬的套件為目標進行說明。

所有的 Laravel 套件都透過 [Packagist](http://packagist.org) 及 [Composer](http://getcomposer.org) 進行散佈，因此學習如何使用這些美好的 PHP 散佈工具是一個必經的過程。

<a name="creating-a-package"></a>
## 建立一個套件

建立一個新套件最簡單的方式就是透過 `workbench` 這個 artisan 指令。首先，你需要先在 `app/config/workbench.php` 裡設定一些選項。在這個檔案裡，你會找到 `name` 及 `email` 這兩個選項。這些選項裡的值將會被用來產生套件裡的 `composer.json` 檔。當您設定好這些前置作業後，就已經可以開始打造您的 workbench 套件了！

#### 啟始一個 workbench artisan 指令

	php artisan workbench vendor/package --resources

發行商 (vendor) 名稱是為了識別不同作者發行相同名稱的套件而設計。比方說，我 (Taylor Otwell) 建立了一個新的套件名稱為 "Zapper" ，而發行商的名稱就是 `Taylor`。預設 workbench 指令會建立框架獨立 (framework agnostic) 的套件結構；然後，`resources` 參數則會讓 workbench 在產生套件結構時，額外針對 Laravel 產生特定的資料夾，包括 `migrations`、`views`、`config` 等。

當 `workbench` 指令被執行後，你的套件就可以在 `workbench` 資料夾內存取。接著，您需要為您的套件`註冊服務提供者 (ServiceProvider)`。您可以透過在 `app/config/app.php` 的 `providers` 陣列裡新增您套件的服務提供者名稱進行註冊，這個動作將會讓 Laravel 啟動時載入您的套件。服務提供者使用 `[Package]ServiceProvider` 這種命名慣例來為程式命名，以上述的例子來說，我們將會新增一行 `Taylor\Zapper\ZapperServiceProvider` 到 `providers` 陣列裡。

當提供者被註冊後，你就已經完成套件開發的前置作業了！不過，建議您在深入開發工作前，先熟悉一下以下章節要介面的套件資料結構及開發工作流程。

> **注意：** 假如您的服務提供者無法被載入，記得在你的應用程式根目錄底下執行 `php artisan dump-autoload` 指令。

<a name="package-structure"></a>
## 套件結構

當使用 `workbench` 指令後，您的套件將依照以下慣例進行初始化，這是為了讓您的套件能與 Laravel 協同工作：

#### 基本的套件結構

	/src
		/Vendor
			/Package
				PackageServiceProvider.php
		/config
		/lang
		/migrations
		/views
	/tests
	/public

讓我們繼續探索下去。`src/Vendor/Package` 資料夾是存放這個套件所有的相關類別程式碼，包括 `ServiceProvider`。而 `config`、`lang`、`migrations`、`views` 資料夾，就如同您預想的一樣，存放關於您的套件的相關資源，一個套件可以包含任何種類的資源，就像「一般」的應用程式一樣。

<a name="service-providers"></a>
## 服務提供者

服務提供者就是一個套件的啟始類別。預設來說，他包含兩個方法：`boot` 和 `register`。透過這兩個方法，你可以做任何你需要做的事，比方說：引入路由檔、註冊 IoC 容器、銜接事件或是任何其他您想要做的事。

`register` 這個方法則是當服務提供者被註冊時馬上被呼叫，而 `boot` 指令則是僅當一個請求被路由時才會被執行。所以，假如您的服務提供者相依於其他已經註冊的服務提供者，或是你想要覆寫由其他服務提供者所做的綁定，則您應該使用 `boot` 方法。

當使用 `workbench` 新建一個套件時， `boot` 指令就已經包括以下動作：

	$this->package('vendor/package');

這個方法讓 Laravel 知道如何載入視圖、設定及其他您的應用程式所需的資源。在大多數的情況下，跟隨這個 workbench 的慣例即可，並不需要特別修改這一行。

在預設的情況下，當註冊完套件後，其資源就可以透過 `vendor/package` 取得。然後，您可以透過 package 方法的第二個參數來覆寫其動作，就方說：

	// 將 custom-namespace 傳給 package 方法
	$this->package('vendor/package', 'custom-namespace');

	// 則套件資源可透過 custom-namespace 取得
	$view = View::make('custom-namespace::foo');

服務提供者類別並沒有「預設」的存放位置，您可以把它放在任何您喜歡的地方，或許可以將它們統一整理在 `Providers` 命名空間後，放到您的 `app` 資料夾裡。只要 Composer [知道如何載入它們的話](http://getcomposer.org/doc/01-basic-usage.md#autoloading)，您就可以把這些檔案放在任何地方。

假如您更改了您套件資源存放的位置，可能是設定檔或是視圖，那您就應該在 `package` 方法呼叫時，傳第第三個參考來指定您的資源位置：

	$this->package('vendor/package', null, '/path/to/resources');

<a name="deferred-providers"></a>
## 緩載提供者

假如您正在開發的服務提供者並沒有註冊任何型式的資源如設定檔或視圖等，那您就可以考慮將您的服務提供者設定為「緩載」提供者。一個緩載提供者的特性就是只有需要它的功能時才載入，假如在當次的請求循環內不需要這個服務，則這個提供者就不會被載入。

要設定您的服務提供者採用緩載設定，只需要將 `defer` 屬性設定為 `true` 即可：

	protected $defer = true;

接下來你應該從 `Illuminate\Support\ServiceProvider` 基礎類別覆寫 provides 方法，並回傳一個陣列包含所有您需要綁定到 IoC 容器的服務。舉例來說，假如您的提供者註冊 `package.service` 和 `package.another-service` 給 IoC 容器，您的 `provides` 方法應該長得像這樣：

	public function provides()
	{
		return array('package.service', 'package.another-service');
	}

<a name="package-conventions"></a>
## 套件慣例

當想要取用套件的資源如設定檔或是視圖時，需要如下的方法使用雙分號來取得：

#### 載入套件的視圖

	return View::make('package::view.name');

#### 取得套件的設定檔

	return Config::get('package::group.option');

> **注意：** 假如您的套件包括遷移，可以考慮在套件的遷移檔命名時加上您的套件名稱，以避開遷移檔與其他套件在類別命名時可能產生的衝突。

<a name="development-workflow"></a>
## 開發工作流程

當您開發一個套件時，透過如同開發一個應用程式一樣的脈絡來進行往往是很有幫助的，這樣能讓您簡單的觀看及實驗您的樣板…等。因此，安裝一個新的 Laravel 框架，然後使用 `workbench` 指令來建立您的套件結構。

當 `workbench` 指令建立好您的套件結構後，您可以直接在 `workbench/[vendor]/[package]` 資料夾底下執行 `git init` 和 `git push` 進行開發過程的版本控制。這樣可以讓你很方便的在一個完整的應用程式脈絡下開發您的套件，而不會受到 `composer update` 干擾而越陷越深。

既然您的套件在 `workbench` 資料夾內，您可能會很好奇 Composer 是怎麼知道該如何載入您的套件檔案？當 `workbench` 資料夾存在的話，Laravel 會很聰明的掃描底下的套件內容，並在應用程式啟動時自動載入！

假如您需要重新產生您的套件自動載入檔案，您可以使用 `php artisan dump-autoload` 指令。這個指令會重新產生自動載入檔案在您的根目錄專案內。

#### 執行 artisan 自動載入指令

	php artisan dump-autoload

<a name="package-routing"></a>
## 套件路由

在早先的 Laravel 裡是使用 `handles` 的方式來指定哪些 URI 會由套件進行回應。但在 Laravel 4 裡，一個套件可以對任何 URI 進行回應。在您的套件裡載入路由檔案，只需要在您的服務提供者的 `boot` 方法裡 `include` 即可。

#### 從服務提供者引入一個路由檔

	public function boot()
	{
		$this->package('vendor/package');

		include __DIR__.'/../../routes.php';
	}

> **注意：** 假如您的套件有使用控制器，您會需要確定您的 `composer.json` 裡的 auto-load 區塊有正確的設定。

<a name="package-configuration"></a>
## 套件設定

#### 取用套件設定檔案

有些套件需要設定檔，這些檔案就如同應用程式設定檔一樣的方式定義。而當您的服務提供者在註冊資源時，透過 `$this->package` 方法後，即可透過「雙冒號」語法取得其值：

	Config::get('package::file.option');

#### 取得套件的單一設定檔

假如您的套件僅包括一個單一設定檔，則您可以直接將檔案名稱命名為 `config.php`。當您完成這個步驟後，您就可以直接取得值而不需要指定名：

	Config::get('package::option');

#### 手動註冊資源的命名空間

有時候您或許會希望可以 `$this->package` 方法外，註冊一個套件資源 (或許是視圖等)。一般來說，這通常只有在資源不是放在慣例的位置時才需要這樣做。您可以在使用 `View`、`Lang`、`Config` 等類別時，透過呼叫 `addNamespace` 方法來手動註冊資源：

	View::addNamespace('package', __DIR__.'/path/to/views');

當命名空間被註冊後，您就可以透過「雙冒號」來取得資源：

	return View::make('package::view.name');

`addNamespace` 方法在 `View`、`Lang`、`Config` 等類別上的實作是相同的。

### 串接設定

當其他的開發者安裝了您的套件後，他們或許會希望可以覆寫部份的設定值。但假如他們直接修改您的套件原始碼，則當他們下次次執行 composer update 時，這些設定值就又會被覆寫回來。取而代之，應該使用 `config:publish` 指令來發佈設定檔：

	php artisan config:publish vendor/package

當這個指令被執行後，所有您的套件的設定檔都會被複製一份到 `app/config/packages/vendor/package` 底下，這樣設定檔的內容就可以安全的被其他開發人員修改！

> **注意：** 開發者也有可能會建立環境設定檔，這些設定檔則會被放在 `app/config/package/vendor/package/environment` 底下。


<a name="package-views"></a>
## 套件視圖

假如您在應用程式裡使用套件，你偶爾會希望可以客製化套件的視圖。您可以非常容易的透過 `view:publish` 指令將套件的視圖輸出到您的 `app/views` 資料夾底下。

	php artisan view:publish vendor/package

這個指令會將套件的視圖移到 `app/views/packages` 資料夾內。假如這個資料夾還不存在的話，這個指令會自動幫您建立。當這些視圖被輸出後，你就可以依您所意進行調整。而當應用程式執行時，這些被調整過的視圖就會被優先使用於套件的預設值。

<a name="package-migrations"></a>
## 套件遷移

#### 為套件進行遷移檔

您的套件可以非常容易的建立與執行遷移。當您想要為您的套件新增遷移檔時，只需要在指令後面加上 `--bench` 參數：

	php artisan migrate:make create_users_table --bench="vendor/package"

#### 為套件執行遷移

	php artisan migrate --bench="vendor/package"

#### 為已安裝的套件執行遷移

為透過 Composer 安裝的套件 (安裝於 `vendor` 資料夾底下) 執行遷移，僅需加上 `--package` 參數：

	php artisan migrate --package="vendor/package"

<a name="package-assets"></a>
## 套件資產

#### 把套件資產移到 public

有些套件會帶有諸多資產如 Javascript、CSS 和圖片。然而，我們沒有辦法取用這些在 `vendor` 或 `workbench` 資料夾裡的資產，所以我們需要一個把它們移到 `public` 資料夾的方法。而 `asset:publish` 這個指令就是為了這個目的而存在：

	php artisan asset:publish

	php artisan asset:publish vendor/package

假如套件仍在 `workbench` 階段，記得加上 `--bench` 參數

	php artisan asset:publish --bench="vendor/package"

這個指令將會把資產依照供應商及套件名稱移至 `public/packages` 底下。因此，一個叫 `userscape/kudos` 的套件資產就會被移到 `public/packages/userscape/kudos`。使用這個慣例可以讓您安全地在您的套件視圖引入資產。

<a name="publishing-packages"></a>
## 發佈套件

當您的套件已經準備好可以發佈時，您應該先將您的套件送至 [Packagist](http://packagist.org) 。假如這個套件是專屬於 Laravel 的話，您可以考慮在您的 `composer.json` 檔裡加上 `laravel` 的標籤。

同時，標記您的版本對其他開發者來說也是很有用的。當開發者安裝您的套件時，可以設定其偏好的版本 (stable, dev)。假如您的套件還沒有穩定的版本，您可以考慮使用 `branch-alias`。

當您的套件發佈後，仍可以繼續透過原本的 `workbench` 應用程式脈絡持續開發。這是當一個套件發佈後，持續更新的最好方法。

有些組織選擇自行建立他們內部使用的私有套件儲存庫給他們的開發者。假如您對這種作法也有興趣，歡迎瀏覽由 Composer 釋出的 [Satis](http://github.com/composer/satis) 專案文件。

