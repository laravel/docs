# HTTP 回應

- [基本回應](#basic-responses)
    - [附加標頭至回應](#attaching-headers-to-responses)
    - [附加 Cookies 至回應](#attaching-cookies-to-responses)
- [其它回應類型](#other-response-types)
    - [視圖回應](#view-responses)
    - [JSON 回應](#json-responses)
    - [檔案下載](#file-downloads)
- [重導](#redirects)
    - [重導至命名路由](#redirecting-named-routes)
    - [重導至控制器行為](#redirecting-controller-actions)
    - [重導並加上快閃 Session 資料](#redirecting-with-flashed-session-data)
- [回應巨集](#response-macros)

<a name="basic-responses"></a>
## 基本回應

當然，所有的路由及控制器必須回傳某個類型的回應，並發送回使用者的瀏覽器。Laravel 提供了幾種不同的方法來回傳回應。最基本的回應就是從路由或控制器簡易的回傳一個字串：

    Route::get('/', function () {
        return 'Hello World';
    });

給定的字串會被框架自動轉換成 HTTP 回應。

但是以大部分的路由及控制器所執行的動作來說，你需要回傳完整的 `Illuminate\Http\Response` 實例或是一個[視圖](/docs/{{version}}/views)。回傳一個完整的 `Response` 實例時，你能夠自定回應的 HTTP 狀態碼以及標頭。`Response` 實例繼承了 `Symfony\Component\HttpFoundation\Response` 類別，其提供了很多方法建立 HTTP 回應：

    use Illuminate\Http\Response;

    Route::get('home', function () {
        return (new Response($content, $status))
                      ->header('Content-Type', $value);
    });

為了方便起見，你可以使用輔助方法 `response`：

    Route::get('home', function () {
        return response($content, $status)
                      ->header('Content-Type', $value);
    });

> **注意：**有關 `Response` 方法的完整列表可以參照 [API 文件](http://laravel.com/api/master/Illuminate/Http/Response.html)以及 [Symfony API 文件](http://api.symfony.com/2.7/Symfony/Component/HttpFoundation/Response.html)。

<a name="attaching-headers-to-responses"></a>
#### 附加標頭至回應

請記得，大部份的回應方法是可鏈結的，讓你建立流利的回應。舉例來說，你可以在回應送出給使用者之前，使用 `header` 方法增加一系列的標頭至回應：

    return response($content)
                ->header('Content-Type', $type)
                ->header('X-Header-One', 'Header Value')
                ->header('X-Header-Two', 'Header Value');


<a name="attaching-cookies-to-responses"></a>
#### 附加 Cookies 至回應

透過回應實例的 `withCookie` 輔助方法可以讓你輕鬆的附加 cookies 至回應。舉個例子，你可以使用 `withCookie` 方法來產生 cookie 並附加至回應實例：

    return response($content)->header('Content-Type', $type)
                     ->withCookie('name', 'value');

`withCookie` 方法可以接受額外的可選參數，讓你進一步定義自訂 cookies 的屬性：

    ->withCookie($name, $value, $minutes, $path, $domain, $secure, $httpOnly)

預設情況下，所有 Laravel 產生的 cookies 都會被加密並加上認證記號，所以無法被使用者讀取及修改。如果你想將應用程式產生的 cookies 中某個子集的加密停用，你可以使用 `App\Http\Middleware\EncryptCookies` 中介層的 `$except` 屬性：

    /**
     * 不需被加密的 cookies 名稱。
     *
     * @var array
     */
    protected $except = [
        'cookie_name',
    ];

<a name="other-response-types"></a>
## 其它回應類型

使用輔助方法 `response` 可以輕鬆的產生其他類型的回應實例。當你呼叫輔助方法 `response` 且不帶任何參數時，將會回傳 `Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/{{version}}/contracts) 的實作。此 Contract 提供了一些有用的方法來產生回應。

<a name="view-responses"></a>
#### 視圖回應

如果你想要控制回應狀態碼及標頭，但是也想要回傳一個[視圖](/docs/{{version}}/views)作為回傳的內容時，你可以使用 `view` 方法：

    return response()->view('hello', $data)->header('Content-Type', $type);

當然，如果你沒有自定 HTTP 狀態碼及標頭的需求，你可以簡單的使用全域的 `view` 輔助方法。

<a name="json-responses"></a>
#### JSON 回應

`json` 方法會自動將標頭的 `Content-Type` 設定為 `application/json`，並透過 PHP 的 `json_encode` 函式將給定的陣列轉換為 JSON：

    return response()->json(['name' => 'Abigail', 'state' => 'CA']);

如果你想建立一個 JSONP 回應，你可以使用 `json` 方法並加上 `setCallback`：

    return response()->json(['name' => 'Abigail', 'state' => 'CA'])
                     ->setCallback($request->input('callback'));

<a name="file-downloads"></a>
#### 檔案下載

`download` 方法可以用於產生強制讓使用者的瀏覽器下載給定路徑檔案的回應。`download` 方法接受檔案名稱作為方法的第二個參數，此名稱為使用者下載檔案時看見的檔案名稱。最後，你可以傳遞一個 HTTP 標頭的陣列作為第三個參數傳入該方法：

    return response()->download($pathToFile);

    return response()->download($pathToFile, $name, $headers);

> **注意：**管理檔案下載的套件 Symfony HttpFoundation，要求下載檔名必須為 ASCII。

<a name="redirects"></a>
## 重導

重導回應是類別 `Illuminate\Http\RedirectResponse` 的實例，並且包含使用者要重導至另一個 URL 所需的標頭。有幾種方法可以產生 `RedirectResponse` 的實例。最簡單的方式就是透過全域的 `redirect` 輔助方法：

    Route::get('dashboard', function () {
        return redirect('home/dashboard');
    });

有時你可能希望將使用者重導至前一個位置，例如當提交一個無效的表單之後。你可以使用全域的 `back` 輔助方法來達成這個目的：

    Route::post('user/profile', function () {
        // 驗證該請求...

        return back()->withInput();
    });

<a name="redirecting-named-routes"></a>
#### 重導至命名路由

當你呼叫輔助方法 `redirect` 且不帶任何參數時，將會回傳 `Illuminate\Routing\Redirector` 的實例，你可以對該 `Redirector` 的實例呼叫任何的方法。舉個例子，要產生一個 `RedirectResponse` 到一個命名路由，你可以使用 `route` 方法：

    return redirect()->route('login');

如果你的路由有參數，你可以將參數放進 `route` 方法的第二個參數：

    // For a route with the following URI: profile/{id}

    return redirect()->route('profile', [1]);

如果你要重導至路由且路由的參數為 Eloquent 模型的「ID」，你可以直接將模型傳入，ID 將會自動被提取：

    return redirect()->route('profile', [$user]);

<a name="redirecting-controller-actions"></a>
#### 重導至控制器行為

你可能會希望產生重導至[控制器行為](/docs/{{version}}/controllers)。要做到這一點，只需傳遞控制器及行為名稱至 `action` 方法。請記得，你不需要指定完整的命名空間，因為 Laravel 的 `RouteServiceProvider` 會自動設定預設的控制器命名空間：

    return redirect()->action('HomeController@index');

當然，如果你的控制器路由需要參數的話，你可以傳遞它們至 `action` 方法的第二個參數：

    return redirect()->action('UserController@profile', [1]);

<a name="redirecting-with-flashed-session-data"></a>
#### 重導並加上快閃 Session 資料

通常重導至新的 URL 時會一併[寫入快閃資料至 session](/docs/{{version}}/session#flash-data)。所以為了方便，你可以利用方法鏈結的方式創建一個 `RedirectResponse` 的實例**並**快閃資料至 Session。這對於在一個動作之後儲存狀態訊息相當方便：

    Route::post('user/profile', function () {
        // 更新使用者的個人資料...

        return redirect('dashboard')->with('status', 'Profile updated!');
    });

當然，在使用者重導至新的頁面後，你可以取得並顯示 [session](/docs/{{version}}/session) 的快閃資料。舉個例子，使用 [Blade 的語法](/docs/{{version}}/blade)：

    @if (session('status'))
        <div class="alert alert-success">
            {{ session('status') }}
        </div>
    @endif

<a name="response-macros"></a>
## 回應巨集

如果你想要自訂可以在很多路由和控制器重複使用的回應，你可以使用 `Illuminate\Contracts\Routing\ResponseFactory` 實作的方法 `macro`。

舉個例子，來自[服務提供者的](/docs/{{version}}/providers) `boot` 方法：

    <?php

    namespace App\Providers;

    use Illuminate\Support\ServiceProvider;
    use Illuminate\Contracts\Routing\ResponseFactory;

    class ResponseMacroServiceProvider extends ServiceProvider
    {
        /**
         * 提供註冊後執行的服務。
         *
         * @param  ResponseFactory  $factory
         * @return void
         */
        public function boot(ResponseFactory $factory)
        {
            $factory->macro('caps', function ($value) use ($factory) {
                return $factory->make(strtoupper($value));
            });
        }
    }

`macro` 函式第一個參數為巨集名稱，第二個參數為閉包函式。巨集的閉包函式會在 `ResponseFactory` 的實作或者輔助方法 `response` 呼叫巨集名稱的時候被執行：

    return response()->caps('foo');
