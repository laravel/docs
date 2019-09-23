# 視圖

- [建立視圖](#creating-views)
- [傳遞資料到視圖](#passing-data-to-views)
    - [共享資料給所有視圖](#sharing-data-with-all-views)
- [視圖組件](#view-composers)

<a name="creating-views"></a>
## 建立視圖

> {tip} 想要找到更多如何撰寫 Blade 模板的資訊嗎？查看完整的 [Blade 文件](/docs/{{version}}/blade)來入門。

視圖包含應用程式用到的 HTML，它能夠將呈現邏輯從控制器和應用程式邏輯分離出來。視圖被存在 `resources/views` 目錄下。一個簡單的視圖看起來可能像這樣：

    <!-- 視圖被儲存在 resources/views/greeting.blade.php -->

    <html>
        <body>
            <h1>Hello, {{ $name }}</h1>
        </body>
    </html>

因為這個視圖被儲存在 `resources/views/greeting.blade.php`，我們可以像這樣使用全域的輔助函式 `view` 來回傳：

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });

如你所見，`view` 輔助函式的第一個參數會對應到 `resources/views` 目錄下視圖檔案的名稱；傳遞到 `view` 輔助函式的第二個參數，是一個能夠在視圖內取用的資料陣列。在這個例子中，我們傳遞 `name` 這個變數，然後在視圖裡面我們使用 [Blade 語法](/docs/{{version}}/blade)來顯示。

當然，視圖檔案也可以被存放在 `resources/views` 的子目錄下。`.` （小數點）的表示法可以被用來表示在子目錄內的視圖檔案。舉例來說，如果你的視圖檔案儲存在 `resources/views/admin/profile.blade.php`，你可以用以下的程式碼來回傳：

    return view('admin.profile', $data);

#### 判斷視圖檔案是否存在

如果你需要判斷視圖檔案是否存在，你可以使用 `View` facade。它的 `exists` 方法將會在視圖檔案存在時回傳 `true`：

    use Illuminate\Support\Facades\View;

    if (View::exists('emails.customer')) {
        //
    }

#### 建立第一個可用視圖

使用 `first` 函式，你可以從一個視圖的陣列內選擇第一個存在的視圖來建立畫面。如果你的應用或套件允許客製化或者覆寫視圖的話，這會很有用：

    return view()->first(['custom.admin', 'admin'], $data);

你也可以透過 `View` [facade](/docs/{{version}}/facades) 來呼叫這個函式：

    use Illuminate\Support\Facades\View;

    return View::first(['custom.admin', 'admin'], $data);

<a name="passing-data-to-views"></a>
## 傳遞資料到視圖

如之前的範例所見，你可以簡單的傳遞一個陣列的資料給視圖：

    return view('greetings', ['name' => 'Victoria']);

用上面的方式傳遞資料時，資料必須是一個鍵值對的陣列。在你的視圖中，你可以用相對應的鍵名取用值，如：`<?php echo $key; ?>`；你也可以用另一個替代的語法來傳遞資料陣列，在 `view` 輔助函式使用 `with` 來傳遞額外資料給視圖：

    return view('greeting')->with('name', 'Victoria');

<a name="sharing-data-with-all-views"></a>
#### 共享資料給所有視圖

有時候你可能想要共享某些資料給所有應用程式所渲染的視圖，你可以使用視圖 facade 的 `share` 方法來做到這件事。通常，你應該把些呼叫 `share` 方法的程式碼放在一個服務提供者的 `boot` 方法內。你可以選擇直接寫在 `AppServiceProvider` 或是自己產生一個不同的服務提供者來安置這些程式碼：

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\View;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 啟動任何應用程式的服務。
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * 註冊服務提供者。
         *
         * @return void
         */
        public function boot()
        {
            View::share('key', 'value');
        }
    }

<a name="view-composers"></a>
## 視圖組件

視圖組件就是在視圖被渲染前，會呼叫的回呼或類別方法。如果你想在每次渲染某些視圖時綁定資料，視圖組件可以把這樣的程式邏輯組織在同一個地方。

舉例來說，讓我們在[服務提供者](/docs/{{version}}/providers)內註冊視圖組件。我們將使用 `View` facade 來取得底層 `Illuminate\Contracts\View\Factory` contract 實作。請注意，Laravel 沒有預設的目錄來放置視圖組件。你可以自由的把它們放在你想要的地方。舉例來說，你可以建立一個 `app/Http/ViewComposers` 目錄：

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\View;
    use Illuminate\Support\ServiceProvider;

    class ViewServiceProvider extends ServiceProvider
    {
        /**
         * 註冊服務提供者。
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * 在容器內註冊所有綁定。
         *
         * @return void
         */
        public function boot()
        {
            // 使用物件型態的視圖組件…
            View::composer(
                'profile', 'App\Http\View\Composers\ProfileComposer'
            );

            // 使用閉包型態的視圖組件…
            View::composer('dashboard', function ($view) {
                //
            });
        }
    }

> {note} 記住，如果你建立了一個新的服務提供者來註冊你的視圖組件，你需要把服務提供者加入 `config/app.php` 設定檔內的 `providers` 陣列。

現在我們已經註冊了視圖組件，在每次 `profile` 視圖渲染的時候，`ProfileComposer@compose` 都將會被執行。所以接下來我們來定義這個類別形式的視圖組件：

    <?php

    namespace App\Http\View\Composers;

    use App\Repositories\UserRepository;
    use Illuminate\View\View;

    class ProfileComposer
    {
        /**
         * 使用者儲存庫的實例。
         *
         * @var UserRepository
         */
        protected $users;

        /**
         * 建立一個新的個人檔案視圖組件。
         *
         * @param  UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            // 所有依賴都會自動地被服務容器解析…
            $this->users = $users;
        }

        /**
         * 將資料綁定到視圖。
         *
         * @param  View  $view
         * @return void
         */
        public function compose(View $view)
        {
            $view->with('count', $this->users->count());
        }
    }

在視圖被渲染之前，視圖組件的 `compose` 方法會被呼叫，並傳入一個 `Illuminate\View\View` 實例。你可以使用 `with` 方法把資料綁定到視圖。

> {tip} 所有的視圖組件都會被[服務容器](/docs/{{version}}/container)解析，所以你可以在視圖組件的建構子中，使用型別提示來自動注入你所需的任何相依物件。

#### 在多個視圖中附加同一個視圖組件

你可以在 `composer` 方法的第一個參數傳遞一個視圖陣列，來一次對多個視圖附加同一個視圖組件：

    View::composer(
        ['profile', 'dashboard'],
        'App\Http\View\Composers\MyViewComposer'
    );

The `composer` method also accepts the `*` character as a wildcard, allowing you to attach a composer to all views:

    View::composer('*', function ($view) {
        //
    });

#### 視圖創建者

視圖**創建者**幾乎和視圖組件運作方式一樣；只是視圖創建者會在視圖初始化後就立刻執行，而不是像視圖組件會一直等到視圖即將被渲染時才會執行。要註冊一個創建者，只要使用 `creator` 方法：

    View::creator('profile', 'App\Http\View\Creators\ProfileCreator');
