# HTTP 請求

- [取得請求](#accessing-the-request)
    - [基本請求資訊](#basic-request-information)
    - [PSR-7 請求](#psr7-requests)
- [取得輸入資料](#retrieving-input)
    - [舊輸入資料](#old-input)
    - [Cookies](#cookies)
    - [上傳檔案](#files)

<a name="accessing-the-request"></a>
## 取得請求

要透過依賴注入的方式取得 HTTP 請求的實例，你必須在控制器的建構函子或方法中，使用 `Illuminate\Http\Request` 型別提示。當前的請求實例就會自動由[服務容器](/docs/{{version}}/container)注入：

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use Illuminate\Routing\Controller;

    class UserController extends Controller
    {
        /**
         * Store a new user.
         *
         * @param  Request  $request
         * @return Response
         */
        public function store(Request $request)
        {
            $name = $request->input('name');

            //
        }
    }

如果你的控制器方法也有從路由參數傳入的輸入資料，只需要將路由參數置於其他依賴之後。舉例來說，如果你的路由定義像是：

    Route::put('user/{id}', 'UserController@update');

只要像下方一樣定義控制器方法，一樣可以使用 `Illuminate\Http\Request` 型別提示，同時取得你的路由參數 `id`：

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use Illuminate\Routing\Controller;

    class UserController extends Controller
    {
        /**
         * Update the specified user.
         *
         * @param  Request  $request
         * @param  int  $id
         * @return Response
         */
        public function update(Request $request, $id)
        {
            //
        }
    }

<a name="basic-request-information"></a>
### 基本請求資訊

`Illuminate\Http\Request` 的實例提供了多種方法，用於檢查應用程式的 HTTP 請求。Larevel 的 `Illuminate\Http\Request` 繼承了 `Symfony\Component\HttpFoundation\Request` 類別。下方是該類別的幾個有用的方法：

#### 取得請求的 URI

`path` 方法會回傳請求的 URI。所以，如果接收到的請求目標是 `http://domain.com/foo/bar`，那麼 `path` 方法就會回傳 `foo/bar`：

    $uri = $request->path();

`is` 方法可以驗證接收到的請求 URI 與給定的規則是否相匹配。使用此方法時你可以將 `*` 符號作為萬用字元：

    if ($request->is('admin/*')) {
        //
    }

若要取得完整的網址，而不只有路徑資訊，你可以對請求實例使用 `url` 方法：

    $url = $request->url();

#### 取得請求的方法

`method` 方法會回傳當次請求的 HTTP 動詞。你也可以透過 `isMethod` 方法來驗證 HTTP 動詞和給定的字串是否互相匹配：

    $method = $request->method();

    if ($request->isMethod('post')) {
        //
    }

<a name="psr7-requests"></a>
### PSR-7 請求

PSR-7 標準制定的 HTTP 訊息介面包含了請求及回應。如果你想獲得一個 PSR-7 的請求實例，你必須先安裝幾個函式庫。Laravel 使用 Symfony 的 HTTP 訊息橋接元件，將原 Laravel 的請求及回應轉換至 PSR-7 所支援的實作：

    composer require symfony/psr-http-message-bridge

    composer require zendframework/zend-diactoros

只要你安裝完這些函式庫，你就可以在你的路由或控制器中，簡單的對請求類型使用型別提示取得 PSR-7 的請求：

    use Psr\Http\Message\ServerRequestInterface;

    Route::get('/', function (ServerRequestInterface $request) {
        //
    });

如果你從路由或控制器回傳一個 PSR-7 的回應實例，它會被框架自動轉換回 Laravel 的回應實例並顯示。

<a name="retrieving-input"></a>
## 取得輸入資料

#### 取得特定輸入值

你可以透過 `Illuminate\Http\Request` 的實例，經由幾個簡潔的方法取得所有的使用者輸入資料。不需要擔心發出請求時使用的 HTTP 動詞，取得輸入資料的方式都是相同的。

    $name = $request->input('name');

Alternatively, you may access user input using the properties of the `Illuminate\Http\Request` instance. For example, if one of your application's forms contains a `name` field, you may access the value of the posted field like so:

    $name = $request->name;

你可以在 `input` 方法的第二個參數傳入一個預設值。當請求的輸入資料不存在於當次請求，就會回傳預設值：

    $name = $request->input('name', 'Sally');

如果是「陣列」形式的輸入資料，可以使用「點」語法取得陣列：

    $input = $request->input('products.0.name');

#### 確認是否有輸入值

要判斷資料是否存在於當次請求，你可以使用 `has` 方法。當該資料存在**而且**不為空字串時，`has` 方法就會傳回 `true`：

    if ($request->has('name')) {
        //
    }

#### 取得所有輸入資料

你也可以使用 `all` 方法以`陣列`形式取得所有輸入資料的：

    $input = $request->all();

#### 取得部分輸入資料

如果你想取得輸入資料的子集，你可以使用 `only` 及 `except` 方法。這兩個方法都接受單一`陣列`或是動態列表作為參數：

    $input = $request->only(['username', 'password']);

    $input = $request->only('username', 'password');

    $input = $request->except(['credit_card']);

    $input = $request->except('credit_card');

<a name="old-input"></a>
### 舊輸入資料

Laravel 可以讓你保留這次的輸入資料，直到下一次請求發送前。對於在表單驗證失敗後重新填入表單值相當有用。當然，如果你使用 Laravel 的[驗證服務](/docs/{{version}}/validation)，你就不需要手動使用這些方法，因為一些 Laravel 內建的驗證功能會自動呼叫它們。

#### 將輸入資料快閃至 Session

`Illuminate\Http\Request` 實例的 `flash` 方法會將當前的輸入資料存進 [Session](/docs/{{version}}/session) 中，所以下次使用者發出請求至應用程式時就可以使用它們：

    $request->flash();

你也可以使用 `flashOnly` 及 `flashExcept` 方法將請求資料的子集儲存至 Session：

    $request->flashOnly('username', 'email');

    $request->flashExcept('password');

#### 快閃輸入資料至 Session 後重導

你可能常常想要將輸入資料快閃並重導至前一頁，你只要在重導方法後串接 `withInput` 就行了：

    return redirect('form')->withInput();

    return redirect('form')->withInput($request->except('password'));

#### 取得舊輸入資料

若要取得前次請求所快閃的輸入資料，你可以使用 `Request` 實例中的 `old` 方法。`old` 方法提供一個簡便的方式從 [Session](/docs/{{version}}/session) 取出被快閃的輸入資料：

    $username = $request->old('username');

Laravel 也提供了全域輔助方法 `old`。如果你要在 [Blade 模板](/docs/{{version}}/blade)顯示舊輸入資料，可以使用更加方便的輔助方法 `old`：

    {{ old('username') }}

<a name="cookies"></a>
### Cookies

#### 從請求取的 Cookie 值

Laravel 框架建立的每個 cookie 會加密並且加上認證記號，這代表著被使用者擅自更改的 cookie 會失效。若要從當次請求取得 cookie 值，你可以使用 `Illuminate\Http\Request` 實例中的 `cookie` 方法：

    $value = $request->cookie('name');

#### 加上新的 Cookie 至回應

Laravel 提供了全域輔助方法 `cookie`，透過簡易的工廠來產生新的 `Symfony\Component\HttpFoundation\Cookie` 實例。可以在 `Illuminate\Http\Response` 實例之後連接 `withCookie` 方法帶入 cookie 至回應：

    $response = new Illuminate\Http\Response('Hello World');

    $response->withCookie(cookie('name', 'value', $minutes));

    return $response;

如果要建立一個長期存在，為期五年的 cookie，你可以先呼叫 `cookie` 輔助方法且不帶入任何參數，再使用 cookie 工廠的 `forever` 方法，接著將 `forever` 方法串接在回傳的 cookie 工廠：

    $response->withCookie(cookie()->forever('name', 'value'));

<a name="files"></a>
### 上傳檔案

#### 取得上傳檔案

你可以使用 `Illuminate\Http\Request` 實例中的 `file` 方法取得上傳的檔案。file 方法回傳的物件是 `Symfony\Component\HttpFoundation\File\UploadedFile` 類別的實例，該類別繼承了 PHP 的 `SplFileInfo` 類別並提供了許多和檔案互動的方法：

    $file = $request->file('photo');

#### 確認檔案是否有上傳

你可以使用請求的 `hasFile` 方法確定上傳的檔案是否存在：

    if ($request->hasFile('photo')) {
        //
    }

#### 確認上傳的檔案是否有效

除了檢查上傳的檔案是否存在外，你也可以透過 `isValid` 方法驗證上傳的檔案是否有效：

    if ($request->file('photo')->isValid()) {
        //
    }

#### 移動上傳的檔案

若要移動上傳的檔案至新的位置，你必須使用 `move` 方法。該方法會將檔案從暫存位置（由你的 PHP 設定來決定）移動至你指定的永久保存位置：

    $request->file('photo')->move($destinationPath);

    $request->file('photo')->move($destinationPath, $fileName);

#### 其他上傳檔案的方法

`UploadedFile` 的實例還有許多可用的方法，可以至[該物件的 API 文件](http://api.symfony.com/2.7/Symfony/Component/HttpFoundation/File/UploadedFile.html)瞭解有關這些方法的詳細資訊。
