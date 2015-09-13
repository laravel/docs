# 套件開發

- [簡介](#introduction)
- [服務提供者](#service-providers)
- [路由](#routing)
- [資源](#resources)
    - [視圖](#views)
    - [語言](#translations)
    - [設定檔](#configuration)
- [公用資源檔](#public-assets)
- [發佈分類檔案](#publishing-file-groups)

<a name="introduction"></a>
## 簡介

套件是擴增功能到 Laravel 的主要方式。套件可以包含許多好用的功能，像 [Carbon](https://github.com/briannesbitt/Carbon) 用於處理時間，或像 [Behat](https://github.com/Behat/Behat) 這種完整的 BDD 測試框架。

當然，有非常多不同類型的套件。有些套件是獨立運作的，意思是指他們並不相依於任何框架，包括 Laravel。剛剛所提到的 Carbon 及 Behat 就是這種套件。要使用這種套件只需要在 `composer.json` 檔案裡引入它們即可。

另一方面，有些套件特別指定要與 Laravel 整合。這些套件可能包含路由、控制器、視圖以及套件的相關設定，目標是增強 Laravel 本身的功能。這份指南裡將主要以開發 Laravel 專屬的套件為目標進行說明。

<a name="service-providers"></a>
## 服務提供者

[服務提供者](/docs/{{version}}/providers)是你的套件與 Laravel 連接的重點。服務提供者負責綁定一些東西至 Laravel 的[服務容器](/docs/{{version}}/container)並告知 Laravel 要從哪載入套件的資源，像是視圖，設定檔，與語言檔。

服務提供者繼承了 `Illuminate\Support\ServiceProvider` 類別並包含了兩個方法：`register` 及 `boot`。基底的 `ServiceProvider` 類別被放置在 Composer 的 `illuminate/support` 套件，你必須將它加入至你自己的套件的依賴。

若要瞭解更多關於服務提供者的結構與用途，請查閱[它的文件](/docs/{{version}}/provider)。

<a name="routing"></a>
## 路由

要為你的套件定義路由，只要簡單的在你套件的服務提供者的 `boot` 方法 `require` 路由檔案。在你的路由檔案中，你可以如同在一般的 Laravel 應用程式一樣使用 `Route` facade 來[註冊路由](/docs/{{version}}/routing)：

    /**
     * 在註冊後進行服務的啟動。
     *
     * @return void
     */
    public function boot()
    {
        if (! $this->app->routesAreCached()) {
            require __DIR__.'/../../routes.php';
        }
    }

<a name="resources"></a>
## 資源

<a name="views"></a>
### 視圖

若要在 Laravel 中註冊你套件的[視圖](/docs/{{version}}/views)，你必須告訴 Laravel 你的視圖位置。你可以使用服務提供者的 `loadViewsFrom` 方法來達成。`loadViewsFrom` 方法允許兩個參數：你的視圖模板路徑與你的套件名稱。例如，如果你的套件名稱是「courier」，你可以按照以下方式新增至你的服務提供者的 `boot` 方法：

    /**
     * 在註冊後進行服務的啟動。
     *
     * @return void
     */
    public function boot()
    {
        $this->loadViewsFrom(__DIR__.'/path/to/views', 'courier');
    }

套件視圖可以使用雙分號 `package::view` 語法參照它。所以，你可以如同以下方式從 `courier` 套件載入 `admin` 視圖：

    Route::get('admin', function () {
        return view('courier::admin');
    });

#### 複寫套件視圖

當你使用 `loadViewsFrom` 方法時，Laravel 實際上為了你的視圖註冊了**兩個**位置：一個是應用程式的 `resources/views/vendor` 目錄，另一個是你所指定的目錄。所以，使用我們的 `courier` 為例：當請求一個套件的視圖時，Laravel 會在第一時間檢查 `resources/views/vendor/courier` 是否有開發者提供的自訂版本視圖存在。接著，如果這個路徑沒有自訂的視圖，Laravel 會搜尋你在套件 `loadViewsFrom` 方法裡所指定的視圖路徑。這個方法讓使用者可以方便的自訂或覆寫你的套件裡的視圖。

#### 發佈視圖

若要發佈套件的視圖至 `resources/views/vendor` 目錄，你必須使用服務提供者的 `publishes` 方法。`publishes` 方法允許一個包含套件視圖路徑及對應發佈路徑的陣列。

    /**
     * 在註冊後進行服務的啟動。
     *
     * @return void
     */
    public function boot()
    {
        $this->loadViewsFrom(__DIR__.'/path/to/views', 'courier');

        $this->publishes([
            __DIR__.'/path/to/views' => base_path('resources/views/vendor/courier'),
        ]);
    }

現在，當你套件的使用者執行 Laravel 的 `vendor:publish` Artisan 指令時，你套件的視圖將會被複製到指定的位置。

<a name="translations"></a>
### 語言

如果你的套件包含[語言檔案](/docs/{{version}}/localization)，你可以使用 `loadTranslationsFrom` 方法來告知 Laravel 該如何載入它們。舉個例子，如果你的套件名稱為「courier」，你可以按照以下方式新增至你服務提供者的 `boot` 方法：

    /**
     * 在註冊後進行服務的啟動。
     *
     * @return void
     */
    public function boot()
    {
        $this->loadTranslationsFrom(__DIR__.'/path/to/translations', 'courier');
    }

套件語言可以使用雙分號 `package::file.line` 語法參照它。所以，你可以按照以下方式載入 `courier` 套件中 `messages` 檔案的 `welcome` 語句：

    echo trans('courier::messages.welcome');

#### 發佈語言檔

如果你想將套件的語言檔發佈至應用程式的 `resources/lang/vendor` 目錄，你可以使用服務提供者的 `publishes` 方法。`publishes` 方法接受一個包含套件路徑及對應發佈位置的陣列。例如，若要在我們的範例 `courier` 套件發佈語言檔：

    /**
     * 在註冊後進行服務的啟動。
     *
     * @return void
     */
    public function boot()
    {
        $this->loadTranslationsFrom(__DIR__.'/path/to/translations', 'courier');

        $this->publishes([
            __DIR__.'/path/to/translations' => base_path('resources/lang/vendor/courier'),
        ]);
    }

現在，當你套件的使用者執行 Laravel 的 `vendor:publish` Artisan 指令時，你套件的語言檔將會被複製到指定的位置。

<a name="configuration"></a>
### 設定檔

基本上，你可能想要將你套件的設定檔發佈到應用程式本身的 `config` 目錄。這能夠讓你套件的使用者輕鬆的覆寫這些預設的設定選項。如果要發佈套件的設定檔，只需要在服務提供者裡的 `boot` 方法裡使用 `publishes` 方法：

    /**
     * 在註冊後進行服務的啟動。
     *
     * @return void
     */
    public function boot()
    {
        $this->publishes([
            __DIR__.'/path/to/config/courier.php' => config_path('courier.php'),
        ]);
    }

現在當你套件的使用者使用 Laravel 的 `vendor:publish` 指令時，你的檔案將會被複製到指定的位置。當然，只要你的設定檔案被發佈後，就可以如其他設定檔一樣被存取：

    $value = config('courier.option');

#### 預設套件設定檔

你也可以選擇合併你的套件設定檔和應用程式裡的副本設定檔。這樣能夠讓你的使用者在已經發佈的副本設定檔裡只包含他們想要覆寫的設定選項。如果想要合併設定檔，可在服務提供者裡的 `register` 方法裡使用 `mergeConfigFrom` 方法：

    /**
     * 在容器中註冊綁定。
     *
     * @return void
     */
    public function register()
    {
        $this->mergeConfigFrom(
            __DIR__.'/path/to/config/courier.php', 'courier'
        );
    }

<a name="public-assets"></a>
## 公用資源檔

你的套件內可能會包含許多的資源檔，像是 JavaScript、CSS 和圖片。如果要發布資源檔至應用程式的 `public` 目錄，只需要使用服務提供者的 `publishes` 方法。在這個例子中，我們也會增加一個 `public` 的資源分類標籤，可以被使用於發佈與分類關聯的資源檔：

    /**
     * 在註冊後進行服務的啟動。
     *
     * @return void
     */
    public function boot()
    {
        $this->publishes([
            __DIR__.'/path/to/assets' => public_path('vendor/courier'),
        ], 'public');
    }

現在當你套件的使用者執行 `vendor:publish` 指令時，你的資源檔將會被複製到指定的位置。當每次套件更新需要覆寫資源檔時，你可以使用 `--force` 標記：

    php artisan vendor:publish --tag=public --force

如果你想要確保你的公用資源檔始終保持在最新的版本，可以將此指令加入你的 `composer.json` 檔案中的 `post-update-cmd` 列表。

<a name="publishing-file-groups"></a>
## 發佈分類檔案

你可能想要分別發佈分類的套件資源檔或是資源。舉例來說，你可能想讓使用者不需發佈套件的所有資源檔，只單獨發佈套件的設定檔。你可以在呼叫 `publishes` 方法時使用「標籤」來做到。例如，讓我們在套件的服務提供者中的 `boot` 方法定義兩個發佈群組：

    /**
     * 在註冊後進行服務的啟動。
     *
     * @return void
     */
    public function boot()
    {
        $this->publishes([
            __DIR__.'/../config/package.php' => config_path('package.php')
        ], 'config');

        $this->publishes([
            __DIR__.'/../database/migrations/' => database_path('migrations')
        ], 'migrations');
    }

現在當你的使用者使用 `vendor:publish` Artisan 指令時，可以透過標籤名稱分別發佈不同分類的資源檔：

    php artisan vendor:publish --provider="Vendor\Providers\PackageServiceProvider" --tag="config"
