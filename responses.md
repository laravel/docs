# HTTP 回應

- [建立回應](#creating-responses)
    - [附加 Header 到回應](#attaching-headers-to-responses)
    - [附加 Cookie 到回應](#attaching-cookies-to-responses)
    - [Cookie 與加密](#cookies-and-encryption)
- [重導](#redirects)
    - [重導到已命名的路由](#redirecting-named-routes)
    - [重導到控制器行為](#redirecting-controller-actions)
    - [重導到外部域名](#redirecting-external-domains)
    - [重導並加上快閃 Session 資料](#redirecting-with-flashed-session-data)
- [其他回應類型](#other-response-types)
    - [視圖回應](#view-responses)
    - [JSON 回應](#json-responses)
    - [檔案下載](#file-downloads)
    - [檔案回應](#file-responses)
- [回應巨集](#response-macros)

<a name="creating-responses"></a>
## 建立回應

<a name="strings-arrays"></a>
#### 字串與陣列

所有路由與控制器應該回傳一個回應到使用者的瀏覽器。Laravel 提供幾個不同的方式來回傳回應。最基本的回應是只從路由和控制器中簡單地回傳一組字串。Laravel 會自動將字串轉換成完整的 HTTP 回應：

    Route::get('/', function () {
        return 'Hello World';
    });

除了從路由和控制器中回傳字串，你也可以回傳陣列。Laravel 會自動將陣列轉換成 JSON 回應：

    Route::get('/', function () {
        return [1, 2, 3];
    });

> {tip} 你知道你也能從路由和控制器中回傳 [Eloquent 集合](/docs/{{version}}/eloquent-collections) 嗎？它們會自動被轉換成 JSON。快來試試看！

<a name="response-objects"></a>
#### 回應物件

通常你不會只從路由行為中回傳簡單的字串或陣列，反而是回傳完整的 Illuminate\Http\Response 實例或 [視圖](/docs/{{version}}/views).

回傳完整的 `Response` 實例可以讓你自訂 HTTP 狀態碼和 header。 `Response`  實例繼承自 `Symfony\Component\HttpFoundation\Response` 類別，這會附帶各種方法來提供建構 HTTP 回應時使用：

    Route::get('/home', function () {
        return response('Hello World', 200)
                      ->header('Content-Type', 'text/plain');
    });

<a name="eloquent-models-and-collections"></a>
#### Eloquent 模型＆集合

你也可以直接從你的路由和控制器中回傳 [Eloquent ORM](/docs/{{version}}/eloquent) 模型和集合。 當你這樣做時, Laravel 將會自動地轉換模型和集合到 JSON 回應，並遵守模型的 [隱藏屬性](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)：

    use App\Models\User;

    Route::get('/user/{user}', function (User $user) {
        return $user;
    });

<a name="attaching-headers-to-responses"></a>
### 回應附加標頭

請記得，大多數的方法是可以被鏈結的，這可以讓你優雅的建構回應實例。例如，在發送回應給使用者前，你可以使用 `header` 方法來新增一系列的 header 到回應中：

    return response($content)
                ->header('Content-Type', $type)
                ->header('X-Header-One', 'Header Value')
                ->header('X-Header-Two', 'Header Value');

或是你使用 `withHeaders` 方法來指定一組 header 陣列，並新增到回應中：

    return response($content)
                ->withHeaders([
                    'Content-Type' => $type,
                    'X-Header-One' => 'Header Value',
                    'X-Header-Two' => 'Header Value',
                ]);

<a name="cache-control-middleware"></a>
#### 快取控制中介層

Laravel 包含一個 `cache.headers` 中介層，可以被使用來快速地設定一組路由的 `Cache-Control` 標頭。指事詞需要使用「蛇行命名法」的相應 Cache-Control 指事詞，並以分號分隔。 如果在指事詞列表裡設置了 `etag`，則回應內容的 MD5 雜湊將會設置 ETag：

    Route::middleware('cache.headers:public;max_age=2628000;etag')->group(function () {
        Route::get('/privacy', function () {
            // ...
        });

        Route::get('/terms', function () {
            // ...
        });
    });

<a name="attaching-cookies-to-responses"></a>
### 回應附加 Cookie

你可以使用 `cookie` 方法附加 cookie 到回傳的 `Illuminate\Http\Response` 執行個體。你應該傳入 cookie 的名稱、值以及有效分鐘到此方法：

    return response('Hello World')->cookie(
        'name', 'value', $minutes
    );

`cookie` 方法也接受一些不常使用的參數。通常這些參數會和 PHP 原生的 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 方法的參數具有相同的意義和目的：

    return response('Hello World')->cookie(
        'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
    );

如果你尚未有回應的執行個體，但想要確保 cookie 與傳出的回應一起送出，你可以使用 `Cookie` facade將 cookie 加入佇列，當回應被送出時一起附帶在回應上。`queue` 方法接受創建 cookie 執行個體時需要的引數。在回應被發送到瀏覽器前，這些 cookie 將附加到回傳的回應上：

    use Illuminate\Support\Facades\Cookie;

    Cookie::queue('name', 'value', $minutes);

<a name="generating-cookie-instances"></a>
#### 創建 Cookie 執行個體

如果想要創建可以稍後附加到回應上的 `Symfony\Component\HttpFoundation\Cookie` 執行個體，你可以使用全域的 `cookie` 輔助函式。 這個 cookie 不會發送回客戶端，除非它被附帶在回應的執行個體：

    $cookie = cookie('name', 'value', $minutes);

    return response('Hello World')->cookie($cookie);

<a name="expiring-cookies-early"></a>
#### 提早過期 Cookie

你可以藉由回應的 `withoutCookie` 方法使 cookie 過期以刪除它：

    return response('Hello World')->withoutCookie('name');

如果你尚未有回應的執行個體，你可以使用 `Cookie` facade 的 `expire` 方法去使 cookie 過期：

    Cookie::expire('name');

<a name="cookies-and-encryption"></a>
### Cookie 與加密

預設所有 Laravel 產生的 Cookie 會被加密與簽署，使它無法在客戶端被串改或讀取。如果你想要停用應用程式所產生部分的 Cookie 加密，你可以使用 `App\Http\Middleware\EncryptCookies` 中介層的 `$except` 屬性，它位在 `app/Http/Middleware` 目錄中：

    /**
     * The names of the cookies that should not be encrypted.
     *
     * @var array
     */
    protected $except = [
        'cookie_name',
    ];

<a name="redirects"></a>
## 重導

重導回應是 `Illuminate\Http\RedirectResponse` 類別的實例，並包含需要被重導到使用者另一個 URL 所需要的正確 header。這有幾種方式來產生 `RedirectResponse` 實例。最簡單的方法是使用全域的 `redirect` 輔助函式：

    Route::get('/dashboard', function () {
        return redirect('home/dashboard');
    });

有時你可能希望將使用者重導到他們先前使用的頁面，像是在送出的表單是無效的時候。你可以使用全域的 `back` 輔助函式。由於這個功能會用到 [Session](/docs/{{version}}/session)，請確認使用 `back` 函式的路由有使用 `web` 中介層群組：

    Route::post('/user/profile', function () {
        // Validate the request...

        return back()->withInput();
    });

<a name="redirecting-named-routes"></a>
### 重導到已命名的路由

當你不使用參數的呼叫 `redirect` 輔助函式，就會回傳 `Illuminate\Routing\Redirector` 實例，可以讓你呼叫任何在 `Redirector` 實例上的方法。例如，要產生一個 `RedirectResponse` 到已命名的路由，你可以使用 `route` 方法：

    return redirect()->route('login');

如果你的路由帶有其他參數，你可以將它們作為第二個參數傳入 `route` 方法：

    // 以下路由會對應到這組 URI： /profile/{id}

    return redirect()->route('profile', ['id' => 1]);

<a name="populating-parameters-via-eloquent-models"></a>
#### 透過 Eloquent 模型填入參數

如果你正要重導到需要從 Eloquent 模型填入「ID」參數的路由，你可以只傳入模型本身。該 ID 會被自動取出：

    // 以下路由會對應到這組 URI： /profile/{id}

    return redirect()->route('profile', [$user]);

如果你想要自定義位在路由參數中的值，你可以指定路由參數 (`/profile/{id:slug}`) 或在 Eloquent 模型上覆寫 `getRouteKey` 方法：

    /**
     * 取得模型的路由鍵的值。
     *
     * @return mixed
     */
    public function getRouteKey()
    {
        return $this->slug;
    }

<a name="redirecting-controller-actions"></a>
### 重導到控制行為

你也可以產生重導到[控制器行為](/docs/{{version}}/controllers)。可以將控制器和行為名稱傳入 `action` 方法來做到：

    use App\Http\Controllers\UserController;

    return redirect()->action([UserController::class, 'index']);

如果你的控制器路由需要參數，你可以將它們作為第二個參數來傳入 `action` 方法：

    return redirect()->action(
        [UserController::class, 'profile'], ['id' => 1]
    );

<a name="redirecting-external-domains"></a>
### 重導到外部域名

有時會需要重導到你的應用外的域名。你可以呼叫 `away` 方法，它會創建不帶有任何額外 URL 編碼、驗證、認證的 `RedirectResponse`：

    return redirect()->away('https://www.google.com');

<a name="redirecting-with-flashed-session-data"></a>
### 重導並加上快閃 Session 資料

通常重導到新的 URL 並同時加上[快閃資料到 Session](/docs/{{version}}/session#flash-data) 幾乎是在同一時間完成的。通常是用在成功執行一個行為後，將成功的訊息快閃到 Session。為了方便，你可以建立一個 `RedirectResponse` 實例，並使用一個優雅的方法鏈結將資料快閃到 Session：

    Route::post('/user/profile', function () {
        // ...

        return redirect('dashboard')->with('status', 'Profile updated!');
    });

使用者被重導後，你可以從 [Session](/docs/{{version}}/session) 中顯示被快閃的訊息。例如，使用 [Blade 語法](/docs/{{version}}/blade)：

    @if (session('status'))
        <div class="alert alert-success">
            {{ session('status') }}
        </div>
    @endif

<a name="redirecting-with-input"></a>
#### Redirecting With Input

You may use the `withInput` method provided by the `RedirectResponse` instance to flash the current request's input data to the session before redirecting the user to a new location. This is typically done if the user has encountered a validation error. Once the input has been flashed to the session, you may easily [retrieve it](/docs/{{version}}/requests#retrieving-old-input) during the next request to repopulate the form:

    return back()->withInput();

<a name="other-response-types"></a>
## 其他回應類型

`response` 輔助函式可以被用於產生其他回應實例的類型。當 `response` 輔助函式不帶參數的方式被呼叫時，會回傳 `Illuminate\Contracts\Routing\ResponseFactory` [Contract](/docs/{{version}}/contracts) 實作。這個 Contract 提供幾個好用的方法來產生回應。

<a name="view-responses"></a>
### 視圖回應

如果你需要掌控回應的狀態與標頭，同時也需要回傳一個[視圖](/docs/{{version}}/views)作為回應的內容，你應該使用 `view` 方法：

    return response()
                ->view('hello', $data, 200)
                ->header('Content-Type', $type);

當然，如果你不需要傳入一個自訂的 HTTP 狀態碼或自訂的 header，就直接使用 `view` 輔助函式。

<a name="json-responses"></a>
### JSON 回應

`json` 方法會自動設定 `Content-Type` header 到 `application/json`，以及使用 PHP 的 `json_encode` 函式將陣列轉換成 JSON：

    return response()->json([
        'name' => 'Abigail',
        'state' => 'CA',
    ]);

如果你想要建立一個 JSONP 回應，你可以使用 `json` 方法並加上 `withCallback` 方法：

    return response()
                ->json(['name' => 'Abigail', 'state' => 'CA'])
                ->withCallback($request->input('callback'));

<a name="file-downloads"></a>
### 檔案下載

`download` 方法可被用於產生一個會強制使用者的瀏覽器去下載給定路徑的檔案的回應。`download` 方法接受一個檔案名稱作為該方法的第二個參數，這會確認下載該檔案的使用者所看到的檔案名稱。最後，你可以將一組 HTTP header 的陣列作為第三個參數傳入到該方法：

    return response()->download($pathToFile);

    return response()->download($pathToFile, $name, $headers);

> **Warning**  
> 管理檔案下載的套件 Symfony HttpFoundation，要求被下載的檔案名稱必須為 ASCII。

<a name="streamed-downloads"></a>
#### Streamed Downloads

Sometimes you may wish to turn the string response of a given operation into a downloadable response without having to write the contents of the operation to disk. You may use the `streamDownload` method in this scenario. This method accepts a callback, filename, and an optional array of headers as its arguments:

    use App\Services\GitHub;

    return response()->streamDownload(function () {
        echo GitHub::api('repo')
                    ->contents()
                    ->readme('laravel', 'laravel')['contents'];
    }, 'laravel-readme.md');

<a name="file-responses"></a>
### 檔案回應

`file` 方法可直接被用於顯示一個檔案在使用者的瀏覽器，像是一個圖像或 PDF，而不是去下載。這個方法接受檔案的路徑作為它的第一個參數，並將一組標頭的陣列作為它的第二個參數：

    return response()->file($pathToFile);

    return response()->file($pathToFile, $headers);

<a name="response-macros"></a>
## 回應巨集

如果你想要定義一個自訂一個可以在各種路由和控制器上重複使用的回應，你可以在 `Response` facade 上使用 `macro` 方法。 Typically, you should call this method from the `boot` method of one of your application's [service providers](/docs/{{version}}/providers), 例如 `App\Providers\AppServiceProvider` 服務提供者:

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Response;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 引導任何應用服務.
         *
         * @return void
         */
        public function boot()
        {
            Response::macro('caps', function ($value) {
                return Response::make(strtoupper($value));
            });
        }
    }

`macro` 函式接受一個名稱作為它的第一個參數，並將閉包作為它的第二個參數。從一個 `ResponseFactory` 實作或 `response` 輔助函式中呼叫巨集名稱時，該巨集的閉包會被執行：

    return response()->caps('foo');
