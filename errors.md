# 錯誤與日誌

- [介紹](#introduction)
- [設定](#configuration)
- [異常處理](#the-exception-handler)
    - [回報例外](#reporting-exceptions)
    - [日誌的嚴重性級別](#exception-log-levels)
    - [根據形態忽略例外](#ignoring-exceptions-by-type)
    - [顯示例外](#rendering-exceptions)
    - [可回報 & 可見的例外](#renderable-exceptions)
- [HTTP 例外](#http-exceptions)
    - [自訂 HTTP 錯誤頁面](#custom-http-error-pages)

<a name="introduction"></a>
## 介紹

當你開始一個新的 Laravel 專案時，都已經為你設定好錯誤與異常處理。 `App\Exceptions\Handler` 類別是記錄應用程式所觸發的所有異常並將其呈現給使用者的地方。 在這個文件中，我們將會深入這個類別。

<a name="configuration"></a>
## 設定

`config/app.php` 設定檔中的 `debug` 選項會確認實際有多少錯誤資訊顯示給使用者。預設這個選項會遵守存放在 `.env` 檔案的 `APP_DEBUG` 環境變數的值。

在本機開發的時候，你應該將 `APP_DEBUG` 環境變數設定為 `true`。 **在你的上線環境中，這個值應該永遠為 `false`。如果在正式上線主機上設定為 `true`，你可能會將設定檔的敏感資訊暴露給應用程式末端的使用者。**

<a name="the-exception-handler"></a>
## 異常處理

<a name="reporting-exceptions"></a>
### 回報例外

`App\Exceptions\Handler` 類別會幫你處理所有例外。這個類別有 `register` 方法可以讓你註冊自訂例外的可回報和可見回調函式。我們將詳細的討論這些方法。 `report` 方法用於記錄例外或發送它們到外部服務，像是[Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com) 或 [Sentry](https://github.com/getsentry/sentry-laravel). 預設的例外會根據[logging](/docs/{{version}}/logging) 的設定檔被紀錄。不過，你可以自由的紀錄例外。

例如，如果你需要以不同的方式回報不同類型的例外，你可以使用  `reportable` 方法來註冊一個當特定型態的例外需要被回報的情況下需要被執行的閉包。 Laravel 會透過檢查閉包的型態提示來決定閉包需要回報什麼型態的例外:

    use App\Exceptions\InvalidOrderException;

    /**
     * Register the exception handling callbacks for the application.
     *
     * @return void
     */
    public function register()
    {
        $this->reportable(function (InvalidOrderException $e) {
            //
        });
    }

當你註冊一個使用 `reportable` 方法的自訂例外回調函式， Laravel 會套用預設設定檔持續紀錄例外。如果你希望例外不要傳到預設的日誌棧，則可以在定義回報回調函式時使用 `stop` 方法或從回調函式回傳 `false` :

    $this->reportable(function (InvalidOrderException $e) {
        //
    })->stop();

    $this->reportable(function (InvalidOrderException $e) {
        return false;
    });

> **Note**  
> 要自訂回報特定例外時，也可以使用[可回報例外](/docs/{{version}}/errors#renderable-exceptions).

<a name="global-log-context"></a>
#### 全域日誌 context

如果允許，Laravel會自動將當前的用戶ID加入每個錯誤日誌訊息當作上下文數據。你也可以透過覆載程式中`App\Exceptions\Handler`類別的`context`方法來定義自己的全域上下文數據。這個資訊會被納入每個錯誤日誌:

    /**
     * Get the default context variables for logging.
     *
     * @return array
     */
    protected function context()
    {
        return array_merge(parent::context(), [
            'foo' => 'bar',
        ]);
    }

<a name="exception-log-context"></a>
#### 錯誤日誌 context

當加入 `context` 到每個日誌會變得非常實用，有時候你會想將有特定內容的例外納入到日誌。透過定義 `context` 方法到應用程式中的其中一個自訂例外，你可以指定任何與該例外相關的資料加入例外日誌的端口：

    <?php

    namespace App\Exceptions;

    use Exception;

    class InvalidOrderException extends Exception
    {
        // ...

        /**
         * Get the exception's context information.
         *
         * @return array
         */
        public function context()
        {
            return ['order_id' => $this->orderId];
        }
    }

<a name="the-report-helper"></a>
#### `report`輔助函式

有時候你需要回報一個例外但繼續處理當前的請求。`report`

有時你一方面要回報例外，另一方面要處理當前的請求。 `report` 輔助函式可以讓你使用異常處理器的 `report` 方法快速的回報例外，而不會顯示錯誤頁面：

    public function isValid($value)
    {
        try {
            // Validate the value...
        } catch (Throwable $e) {
            report($e);

            return false;
        }
    }

<a name="exception-log-levels"></a>
### 日誌的嚴重性級別

訊息會以特定的嚴重性級別寫在[日誌](/docs/{{version}}/logging)中，用來表示訊息的嚴重性火或重要程度。

When messages are written to your application's [logs](/docs/{{version}}/logging), the messages are written at a specified [log level](/docs/{{version}}/logging#log-levels), which indicates the severity or importance of the message being logged.

如上文所及，即使當你註冊一個使用 `reportable` 方法的自訂例外回調函式， Laravel 仍會套用預設設定檔持續紀錄例外；因為日誌的嚴重性級別有時可以影響紀錄訊息的頻道，所以你可以設定紀錄特定例外的日誌的嚴重性級別。

要達到此功能，你可以在例外處理器的 `$levels` 屬性定義一個有例外型態和分別對應的日誌的嚴重性級別的陣列：

    use PDOException;
    use Psr\Log\LogLevel;

    /**
     * A list of exception types with their corresponding custom log levels.
     *
     * @var array<class-string<\Throwable>, \Psr\Log\LogLevel::*>
     */
    protected $levels = [
        PDOException::class => LogLevel::CRITICAL,
    ];

<a name="ignoring-exceptions-by-type"></a>
### 根據型態忽略例外

在開發時，你想忽略某些型態的例外。例外處理器的 `$dontReport` 屬性初始為一個空陣列。你可以加入任何類別進入這個屬性讓它不會被回報；然而，它們可能仍然保留自訂的可渲染邏輯：

    use App\Exceptions\InvalidOrderException;

    /**
     * A list of the exception types that are not reported.
     *
     * @var array<int, class-string<\Throwable>>
     */
    protected $dontReport = [
        InvalidOrderException::class,
    ];

> **Note**  
> 在背後, Laravel 已經為你忽略一些錯誤, 如「找不到頁面」的 404 錯誤代碼或因為無效的 CSRF 憑證造成的 419 錯誤代碼。

<a name="rendering-exceptions"></a>
### 顯示例外

在預設情況下，Laravel 例外處理器會將例外轉成 HTTP 回應給你。不過，你可以註冊一個自訂渲染閉包給特定的例外。你可以透過例外處理器的 `renderable` 方法來達成。

閉包傳到 `renderable` 方法時會回傳一個 `Illuminate\Http\Response` 的實例，這可以透過  `response` 協助函式來生成。Laravel 會透過檢查閉包的型態提示來決定什麼型態的例外要被渲染:

    use App\Exceptions\InvalidOrderException;

    /**
     * Register the exception handling callbacks for the application.
     *
     * @return void
     */
    public function register()
    {
        $this->renderable(function (InvalidOrderException $e, $request) {
            return response()->view('errors.invalid-order', [], 500);
        });
    }

你也可以透過 `renderable` 方法來覆載 Laravel 內建或 Symfony 例外的可渲染行為如 `NotFoundHttpException` 。如果給 `renderable` 方法的閉包沒有回傳值， Laravel 預設的渲染例外會被使用：

    use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

    /**
     * Register the exception handling callbacks for the application.
     *
     * @return void
     */
    public function register()
    {
        $this->renderable(function (NotFoundHttpException $e, $request) {
            if ($request->is('api/*')) {
                return response()->json([
                    'message' => 'Record not found.'
                ], 404);
            }
        });
    }

<a name="renderable-exceptions"></a>
### 可回報 & 可顯示的例外

除了在例外處理器的 `register` 方法中的型態檢查例外，你可以直接在自訂例外定義 `report` 和 `render` 方法。如果這些方法存在，它們會自動被框架拿來使用：

    <?php

    namespace App\Exceptions;

    use Exception;

    class InvalidOrderException extends Exception
    {
        /**
         * Report the exception.
         *
         * @return bool|null
         */
        public function report()
        {
            //
        }

        /**
         * Render the exception into an HTTP response.
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function render($request)
        {
            return response(/* ... */);
        }
    }

如果你的例外展開的例外是可見的，如 Laravel 內建或 Symfony 例外，你可以從例外的 `render` 方法回傳 `false` 來渲染例外預設的 HTTP 回應：

    /**
     * Render the exception into an HTTP response.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function render($request)
    {
        // Determine if the exception needs custom rendering...

        return false;
    }

如果你的例外含有只有在特定情況才需要的自訂回報邏輯，你需要命令 Laravel 有時候透過預的設例外設定檔來回報例外。 要達成此功能，你可以從例外的 `report` 方法回傳 `false` : 

    /**
     * Report the exception.
     *
     * @return bool|null
     */
    public function report()
    {
        // Determine if the exception needs custom reporting...

        return false;
    }

> **Note**  
> 你可以將任何需要依賴 `report` 方法 type-hint 並且它們會被自動加入 Laravel的 [服務容器](/docs/{{version}}/container) 方法中

<a name="http-exceptions"></a>
## HTTP 例外

有些例外會描述 HTTP 錯誤代碼來自伺服器。例如，這可能是「找不到頁面」的 404 錯誤代碼，「未授權的錯誤」的 401 錯誤代碼或者是開發者產生的 500 錯誤代碼。為了在你應用程式的任何地方產生這樣的回應，你可以使用 `abort` 輔助函式：

    abort(404);

<a name="custom-http-error-pages"></a>
### 自訂 HTTP 錯誤頁面

Laravel 很容易為各種的 HTTP 狀態碼設計所要顯示的自訂錯誤頁面。例如，如果你希望自訂 HTTP 404 錯誤代碼頁面，而去建立 `resources/views/errors/404.blade.php` 。這個檔案會為應用程式產生所有的 404 錯誤代碼而服務。在這個目錄中的視圖應該命名與 HTTP 狀態碼一致。透過 `abort` 函式發出的 `HttpException` 實例會作為 `$exception` 變數傳入視圖：

    <h2>{{ $exception->getMessage() }}</h2>

你也可以使用 `vender:publish` Artisan 指令來發布 Laravel 的預設錯誤頁面模板。一旦模板被發布，你可以進行客製化:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### Fallback HTTP 錯誤頁面

你也可以定義一個給一系列HTTP狀態碼的 "fallback" 錯誤頁面。當特定的 HTTP 狀態發生並且沒有相對應的頁面時，這個頁面會被渲染。要達成此功能，可以透過定義一個 `4xx.blade.php` 模板和 `5xx.blade.php` 模板在專案中的 `resources/views/errors` 目錄。
