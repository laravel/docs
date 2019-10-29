# 錯誤

- [介紹](#introduction)
- [設定檔](#configuration)
- [異常處理](#the-exception-handler)
    - [Report 方法](#report-method)
    - [Render 方法](#render-method)
    - [可報告與可見的例外](#renderable-exceptions)
- [HTTP 例外](#http-exceptions)
    - [自訂 HTTP 錯誤頁面](#custom-http-error-pages)

<a name="introduction"></a>
## 介紹

當你開始一個新的 Laravel 專案時，都已經為你設定好錯誤與異常處理。`App\Exceptions\Handler` 類別是記錄應用程式所觸發的所有異常並將其呈現給使用者的地方。在這個文件中，我們將會深入這個類別。

<a name="configuration"></a>
## 設定檔

`config/app.php` 設定檔中的 `debug` 選項會確認實際有多少錯誤資訊顯示給使用者。預設這個選項會遵守存放在 `.env` 檔案的 `APP_DEBUG` 環境變數的值。

在本機開發的時候，你應該將 `APP_DEBUG` 環境變數設定為 `true`。在你的上線環境中，這個值應該永遠為 `false`。如果在正式上線主機上設定為 `true`，你可能會將設定檔的敏感資訊暴露給應用程式末端的使用者。

<a name="the-exception-handler"></a>
## 異常處理

<a name="report-method"></a>
### Report 方法

`App\Exceptions\Handler` 類別會幫你處理所有例外。這個類別會有兩個方法：`report` 和 `render`。我們將詳細的討論這些方法。`report` 方法用於記錄例外或發送它們到外部服務，像是 [Flare](https://flareapp.io)，[Bugsnag](https://bugsnag.com) 或 [Sentry](https://github.com/getsentry/sentry-laravel)。預設的 `report` 方法只是將例外傳給記錄例外的基礎類別。不過，你可以自由的記錄例外。

例如，如果你需要以不同的方式回報不同類型的例外，你可以使用 `instanceof` 類型運算子：

    /**
     * 回報或記錄一個例外。
     *
     * 這是向 Flare，Sentry，Bugsnag 等發送例外的好地方。
     *
     * @param  \Exception  $exception
     * @return void
     */
    public function report(Exception $exception)
    {
        if ($exception instanceof CustomException) {
            //
        }

        parent::report($exception);
    }

> {tip} Instead of making a lot of `instanceof` checks in your `report` method, consider using [reportable exceptions](/docs/{{version}}/errors#renderable-exceptions)

#### Global Log Context

If available, Laravel automatically adds the current user's ID to every exception's log message as contextual data. You may define your own global contextual data by overriding the `context` method of your application's `App\Exceptions\Handler` class. This information will be included in every exception's log message written by your application:

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

#### `report` 輔助函式

有時你一方面要回報例外，另一方面要處理當前的請求。`report` 輔助函式可以讓你使用異常處理器的 `report` 方法快速的回報例外，而不會顯示錯誤頁面：


    public function isValid($value)
    {
        try {
            // 驗證輸入值⋯⋯
        } catch (Exception $e) {
            report($e);

            return false;
        }
    }

#### 依類型忽略例外

異常處理器的 `$dontReport` 屬性會包含一組例外類型的陣列不會被記錄。例如，404 錯誤導致的例外以及其它類型的錯誤將不會寫入你的日誌中。可以根據實際的需要來新增其他例外類型到這組陣列：

    /**
     * 不該被回報的例外類型清單。
     *
     * @var array
     */
    protected $dontReport = [
        \Illuminate\Auth\AuthenticationException::class,
        \Illuminate\Auth\Access\AuthorizationException::class,
        \Symfony\Component\HttpKernel\Exception\HttpException::class,
        \Illuminate\Database\Eloquent\ModelNotFoundException::class,
        \Illuminate\Validation\ValidationException::class,
    ];

<a name="render-method"></a>
### Render 方法

`render` 方法負責將給定的例外轉換成應該回傳給瀏覽器的 HTTP 回應。預設的例外會被傳入產生回應的基礎類別。然而，你可以自由的檢查例外類型或回傳你自訂的回應：

    /**
     * 渲染例外到 HTTP 回應。
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Exception  $exception
     * @return \Illuminate\Http\Response
     */
    public function render($request, Exception $exception)
    {
        if ($exception instanceof CustomException) {
            return response()->view('errors.custom', [], 500);
        }

        return parent::render($request, $exception);
    }

<a name="renderable-exceptions"></a>
### 可報告與可見的例外

想要取代異常處理器用來檢查類型例外的 `report` 和 `render` 方法，你可以直接在你自訂的例外中定義 `report` 和 `render` 方法。當這些方法存在時，它們會被框架自動呼叫：

    <?php

    namespace App\Exceptions;

    use Exception;

    class RenderException extends Exception
    {
        /**
         * 回報例外。
         *
         * @return void
         */
        public function report()
        {
            //
        }

        /**
         * 渲染例外到 HTTP 回應。
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function render($request)
        {
            return response(...);
        }
    }

> {tip} You may type-hint any required dependencies of the `report` method and they will automatically be injected into the method by Laravel's [service container](/docs/{{version}}/container).

<a name="http-exceptions"></a>
## HTTP 例外

有些例外會描述 HTTP 錯誤代碼來自伺服器。例如，這可能是「找不到頁面」的 404 錯誤代碼，「未授權的錯誤」的 401 錯誤代碼或者是開發者產生的 500 錯誤代碼。為了在你應用程式的任何地方產生這樣的回應，你可以使用 `abort` 輔助函式：

    abort(404);

`abort` 輔助函式會馬上發出異常處理器即將渲染的例外。或者，你可以提供回應的文字內容：

    abort(403, 'Unauthorized action.');

<a name="custom-http-error-pages"></a>
### 自訂 HTTP 錯誤頁面

Laravel 很容易為各種的 HTTP 狀態碼設計所要顯示的自訂錯誤頁面。例如，如果你希望自訂 HTTP 404 錯誤代碼頁面，而去建立 `resources/views/errors/404.blade.php`。這個檔案會為應用程式產生所有的 404 錯誤代碼而服務。在這個目錄中的視圖應該命名與 HTTP 狀態碼一致。透過 `abort` 函式發出的 `HttpException` 實例會作為 `$exception` 變數傳入視圖：

    <h2>{{ $exception->getMessage() }}</h2>

You may publish Laravel's error page templates using the `vendor:publish` Artisan command. Once the templates have been published, you may customize them to your liking:

    php artisan vendor:publish --tag=laravel-errors
