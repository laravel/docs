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

（

context 不確定怎麼翻
contextual data 不確定怎麼翻

）

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

All exceptions are handled by the `App\Exceptions\Handler` class. This class contains a `register` method where you may register custom exception reporting and rendering callbacks. We'll examine each of these concepts in detail. Exception reporting is used to log exceptions or send them to an external service like [Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com) or [Sentry](https://github.com/getsentry/sentry-laravel). By default, exceptions will be logged based on your [logging](/docs/{{version}}/logging) configuration. However, you are free to log exceptions however you wish.

例如，如果你需要以不同的方式回報不同類型的例外，你可以使用  `reportable` 方法來註冊一個特定型態的例外需要被回報的情況下需要被執行的閉包。 Laravel 會透過檢查閉包的型態提示決定閉包需要回報什麼型態的例外:

For example, if you need to report different types of exceptions in different ways, you may use the `reportable` method to register a closure that should be executed when an exception of a given type needs to be reported. Laravel will deduce what type of exception the closure reports by examining the type-hint of the closure:

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

When you register a custom exception reporting callback using the `reportable` method, Laravel will still log the exception using the default logging configuration for the application. If you wish to stop the propagation of the exception to the default logging stack, you may use the `stop` method when defining your reporting callback or return `false` from the callback:

    $this->reportable(function (InvalidOrderException $e) {
        //
    })->stop();

    $this->reportable(function (InvalidOrderException $e) {
        return false;
    });

> {tip} To customize the exception reporting for a given exception, you may also utilize [reportable exceptions](/docs/{{version}}/errors#renderable-exceptions).

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

當加入 `context` 到每個日誌會變得非常實用，有時候你會想將有特定內容的例外納入到日誌。透過定義 `context` 方法到應用程式中的其中一個自訂例外，你可以指定任何與該例外相關的資料加入例外日誌的端口。

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

When messages are written to your application's [logs](/docs/{{version}}/logging), the messages are written at a specified [log level](/docs/{{version}}/logging#log-levels), which indicates the severity or importance of the message being logged.

As noted above, even when you register a custom exception reporting callback using the `reportable` method, Laravel will still log the exception using the default logging configuration for the application; however, since the log level can sometimes influence the channels on which a message is logged, you may wish to configure the log level that certain exceptions are logged at.

To accomplish this, you may define an array of exception types and their associated log levels within the `$levels` property of your application's exception handler:

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
### 根據型態略例外



When building your application, there will be some types of exceptions you simply want to ignore and never report. Your application's exception handler contains a `$dontReport` property which is initialized to an empty array. Any classes that you add to this property will never be reported; however, they may still have custom rendering logic:

    use App\Exceptions\InvalidOrderException;

    /**
     * A list of the exception types that are not reported.
     *
     * @var array<int, class-string<\Throwable>>
     */
    protected $dontReport = [
        InvalidOrderException::class,
    ];

> {tip} Behind the scenes, Laravel already ignores some types of errors for you, such as exceptions resulting from 404 HTTP "not found" errors or 419 HTTP responses generated by invalid CSRF tokens.

<a name="rendering-exceptions"></a>
### 顯示例外

By default, the Laravel exception handler will convert exceptions into an HTTP response for you. However, you are free to register a custom rendering closure for exceptions of a given type. You may accomplish this via the `renderable` method of your exception handler.

The closure passed to the `renderable` method should return an instance of `Illuminate\Http\Response`, which may be generated via the `response` helper. Laravel will deduce what type of exception the closure renders by examining the type-hint of the closure:

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

You may also use the `renderable` method to override the rendering behavior for built-in Laravel or Symfony exceptions such as `NotFoundHttpException`. If the closure given to the `renderable` method does not return a value, Laravel's default exception rendering will be utilized:

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

Instead of type-checking exceptions in the exception handler's `register` method, you may define `report` and `render` methods directly on your custom exceptions. When these methods exist, they will be automatically called by the framework:

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
            return response(...);
        }
    }

If your exception extends an exception that is already renderable, such as a built-in Laravel or Symfony exception, you may return `false` from the exception's `render` method to render the exception's default HTTP response:

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

If your exception contains custom reporting logic that is only necessary when certain conditions are met, you may need to instruct Laravel to sometimes report the exception using the default exception handling configuration. To accomplish this, you may return `false` from the exception's `report` method:

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

> {tip} You may type-hint any required dependencies of the `report` method and they will automatically be injected into the method by Laravel's [service container](/docs/{{version}}/container).

<a name="http-exceptions"></a>
## HTTP 例外

Some exceptions describe HTTP error codes from the server. For example, this may be a "page not found" error (404), an "unauthorized error" (401) or even a developer generated 500 error. In order to generate such a response from anywhere in your application, you may use the `abort` helper:

    abort(404);

<a name="custom-http-error-pages"></a>
### 自訂 HTTP 錯誤頁面

Laravel makes it easy to display custom error pages for various HTTP status codes. For example, if you wish to customize the error page for 404 HTTP status codes, create a `resources/views/errors/404.blade.php` view template. This view will be rendered on all 404 errors generated by your application. The views within this directory should be named to match the HTTP status code they correspond to. The `Symfony\Component\HttpKernel\Exception\HttpException` instance raised by the `abort` function will be passed to the view as an `$exception` variable:

    <h2>{{ $exception->getMessage() }}</h2>

You may publish Laravel's default error page templates using the `vendor:publish` Artisan command. Once the templates have been published, you may customize them to your liking:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### Fallback HTTP 錯誤頁面

You may also define a "fallback" error page for a given series of HTTP status codes. This page will be rendered if there is not a corresponding page for the specific HTTP status code that occurred. To accomplish this, define a `4xx.blade.php` template and a `5xx.blade.php` template in your application's `resources/views/errors` directory.
