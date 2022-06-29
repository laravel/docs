# 跨站偽造請求攻擊 (Cross-site request forgery) 保護措施

- [介紹](#csrf-introduction)
- [避免 CSRF 攻擊](#preventing-csrf-requests)
    - [排除特定網址](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 介紹

跨站偽造請求是一種惡意的攻擊，會偽造已驗證的使用者執行未授權的指令。幸好Laravel有簡單的方式來保護你的應用程式免於[跨站偽造請求攻擊 (CSRF)](https://en.wikipedia.org/wiki/Cross-site_request_forgery)(CSRF)。

<a name="csrf-explanation"></a>
#### 漏洞來源解釋

為避免你對於CSRF不太熟悉，我們先來討論攻擊者會如何利用漏洞。假設你的應用程式有這樣一條路徑 `/user/email`，你可以送出 `POST` 請求來更改使用者的電子信箱地址。更精確來說，`email` 這個欄位會預期放的是新的電子郵件地址。

如果沒有CSRF的保護措施，有心人士就可以架一個惡意的網站，並創建一個HTML表單，將使用者輸入的資料傳送到你的 `/user/email` 路徑，並把電子郵件地址改成惡意人士所想要的地址。

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

假設這個惡意網站會自動提交表單，那麼有心人士就只需要引誘沒有戒心的使用者造訪他們的惡意網站，這樣一來使用者在你的應用程式中的電子信箱就會被竄改了。

要補起這個漏洞，我們要檢視每個 `POST`，`PUT`，`PATCH`，或者 `DELETE` 請求的祕密 session，而這個暗號是惡意程式無法得到的。

<a name="preventing-csrf-requests"></a>
## 避免 CSRF 攻擊

Laravel對於每個應用程式收到的[用戶 session](/docs/{{version}}/session)會自動生成一個 CSRF 標記。這個標記是拿來檢驗這個請求是不是真的由已驗證的使用者本人所發出的。因為標記儲存在用戶 session 中，並且在每次活動時都會重新生成，因此惡意程式是無法取得這個標記的。

現在 CRSF 標記可以從請求的 session 中取得，或者用這個 `csrf_token` 這個輔助函式: 

    use Illuminate\Http\Request;

    Route::get('/token', function (Request $request) {
        $token = $request->session()->token();

        $token = csrf_token();

        // ...
    });

每當你在你的應用程式建立一個 `POST`，`PUT`，`PATCH`，或 `DELETE` 表單，你都應該把一個隱藏參數CSRF `_token` 放進你的表單中，好讓中介層 (middleware) 可以驗證你的請求。為了方便起見，你可以用 `@csrf` Blade 引擎來幫你在表單中生成隱藏標記。

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- Equivalent to... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

`App\Http\Middleware\VerifyCsrfToken` [中介層 (middleware)](/docs/{{version}}/middleware)預設被包含在 `web` 中介層群組中，會自動比對請求中的標記與儲存在 session 的標記是否相符。如果這兩個標記相同的話，我們就可以認定就是這個使用者發起這個請求。

<a name="csrf-tokens-and-spas"></a>
### CSRF 標記們與單頁式網站應用程式（SPAs）

如果你正在開發一個利用Laravel當作 API 後端的單頁式網站的話，你應該去[Laravel Sanctum documentation](/docs/{{version}}/sanctum)尋找關於驗證 API 與避免 CSRF 漏洞的相關資訊。

<a name="csrf-excluding-uris"></a>
### 排除特定 URIs 在 CSRF 保護名單之外

有時候你會希望某些 URIs 能夠不用被放在 CSRF 的保護中。例如，你正在使用[ Stripe ](https??stripe.com)來處理付款並利用他們的 webhook 系統，你會需要排除 Stripe webhook 路徑在 CSRF 保護之外，這是因為 Stripe 並不知道要傳送什麼標記給你的路徑。

`App\Providers\RouteServiceProvider` 會套用到所有在 `routes/web.php` 這個檔案中的路徑，所以，通常來說，你應該把想排除的路徑放在 `web` 中介層群組之外。或者是，你也可以把那些 URIs 加到 `VerifyCsrfToken` 中介層的 `$except` 屬性中以排除特定路徑。

    <?php

    namespace App\Http\Middleware;

    use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as Middleware;

    class VerifyCsrfToken extends Middleware
    {
        /**
         * The URIs that should be excluded from CSRF verification.
         *
         * @var array
         */
        protected $except = [
            'stripe/*',
            'http://example.com/foo/bar',
            'http://example.com/foo/*',
        ];
    }

> {小技巧} 為了方便起見，CSRF 中介層在[測試時 (running tests) ](/docs/{{version}}/testing}})會自動取消對所有路徑進行驗證。

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

除了檢查 POST 請求中的 CSRF 參數，`App\Http\Middleware\VerifyCsrfToken` 中介層也會檢查 `X-CSRF-TOKEN` 的請求標頭。例如，你可以把標記儲存在 HTML 的 `meta` 標籤中。

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

接著，你可以指示像 jQuery 這樣的函式庫自動新增標記到所有的請求標頭中。如此一來就可以利用繼承 Jacascript 的技巧來提供 AJAX based 的應用程式一個簡單、方便的 CSRF 保護措施。

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel把當前的 CSRF 標記存在加密`XSRF-TOKEN` cookie 中，而每個由框架所生成的回應都會包含這些 cookie。你可以利用 cookie 的值去設定 `X-XSRF-TOKEN` 的請求標頭。

有些 Javascript 框架與函式庫，像是 Angular 和 Axios，會自動把值放在原請求的 `X-XSRF-TOKEN` 標頭中，因此這個 cookie 主要是傳送來便利開發者的。

> {小技巧} 預設情況下，`resources/js/bootstrap.js` 引入了 Axios HTTP 函式庫，它會自動幫你傳送 `X-XSRF-TOKEN` 的標頭。