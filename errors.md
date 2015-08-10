# 錯誤與日誌

- [簡介](#introduction)
- [設定](#configuration)
- [錯誤處理](#the-exception-handler)
    - [報告方法](#report-method)
    - [呈現方法](#render-method)
- [HTTP 例外](#http-exceptions)
    - [客製化 HTTP 錯誤頁面](#custom-http-error-pages)
- [日誌](#logging)

<a name="introduction"></a>
## 簡介

當你開始一個新的 Laravel 專案時，Laravel 已經幫你設定好錯誤和例外的處理。另外，Laravel 也整合了 [Monolog](https://github.com/Seldaek/monolog) 日誌函式庫，Monolog 支援和提供多種強大的日誌處理。

<a name="configuration"></a>
## 設定

#### 錯誤細節

你的應用程式透過 `config/app.php` 設定檔中的 `debug` 設定選項來控制瀏覽器顯示錯誤的細節。預設情況下，此設定選項是參照於儲存在 `.env` 檔案的 `APP_DEBUG` 環境變數。

在本機開發的時候，你應該將 `APP_DEBUG` 環境變數設定為 `true`。在你的上線環境中，這個值應該永遠為 `false`。

#### 日誌模式

Laravel 提供立即可用的 `single`、`daily`、`syslog` 和 `errorlog` 日誌模式。例如，如果你想要每天儲存一個日誌檔，而不是單一的檔案，你可以簡單地在 `config/app.php` 設定檔內設定 `log` 變數：

    'log' => 'daily'

#### 自訂 Monolog 設定

如果你想要完全控制 Monolog，你可以使用應用程式的 `configureMonologUsing` 方法設定你的應用程式。你應該在 `bootstrap/app.php` 檔案回傳 `$app` 變數之前呼叫這個方法：

    $app->configureMonologUsing(function($monolog) {
        $monolog->pushHandler(...);
    });

    return $app;

<a name="the-exception-handler"></a>
## 錯誤處理

所有的例外處理都是透過 `App\Exceptions\Handler` 類別。這個類別包含了兩個方法：`report` 和 `render`。我們將研究這些方法的細節。

<a name="report-method"></a>
### 報告方法

`report` 方法用來記錄例外或將它們發送到像是 [BugSnag](https://bugsnag.com) 的外部服務。預設情況下，當例外被記錄時，`report` 方法只是簡單的傳送例外到基底的類別。然而，你可以自由的記錄例外。

例如，如果你需要以不同的方式報告不同類型的例外，你可以使用 PHP `instanceof` 比較運算子：

    /**
     * 報告或記錄一個例外。
     *
     * 這裡是個把例外送至 Sentry、Bugsnag 等等的好地方。
     *
     * @param  \Exception  $e
     * @return void
     */
    public function report(Exception $e)
    {
        if ($e instanceof CustomException) {
            //
        }

        return parent::report($e);
    }

#### 藉由類型忽略例外

例外處理中的 `$dontReport` 屬性是一個陣列，包含不需要被記錄的例外類型。預設情況下，由 404 錯誤導致的例外結果並不會被記錄到日誌檔案。你可以根據你的需求增加其他例外類型到這個陣列。

<a name="render-method"></a>
### 呈現方法

`render` 方法負責將給定的例外轉換成 HTTP 回應再傳送到瀏覽器。預設情況下，例外會被傳送到基底類別並幫你產生回應。然而，你可以自由的檢查例外類型或回傳客製化的回應：

    /**
     * 呈現例外到 HTTP 回應。
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Exception  $e
     * @return \Illuminate\Http\Response
     */
    public function render($request, Exception $e)
    {
        if ($e instanceof CustomException) {
            return response()->view('errors.custom', [], 500);
        }

        return parent::render($request, $e);
    }

<a name="http-exceptions"></a>
## HTTP 例外

有一些例外是描述來自伺服器的 HTTP 錯誤碼。例如，這可能是個「找不到頁面」錯誤（404），「未授權錯誤」（401），或甚至是開發者導致的 500 錯誤。你可以使用以下的方法，在你的應用程式任何地方產生回應：

    abort(404);

`abort` 方法透過錯誤處理，將會立即引發例外，並且呈現錯誤。或者，你可以提供回應的文字訊息：

    abort(403, 'Unauthorized action.');

你可以在請求的生命週期中任何時間點使用這個方法。

<a name="custom-http-error-pages"></a>
### 客製化 HTTP 錯誤頁面

Laravel 讓你可以簡單的對於各種不同的 HTTP 狀態碼回傳客製化的錯誤視圖。例如，如果你想要自訂 HTTP 404 狀態碼的錯誤視圖，建立一個 `resources/views/errors/404.blade.php`。應用程式將會使用這個視圖處理所有發生的 404 錯誤。

在這個目錄下的視圖，命名應該匹配對應到 HTTP 狀態碼。

<a name="logging"></a>
## 日誌

Laravel 日誌工具在強大的 [Monolog](http://github.com/seldaek/monolog) 函式庫上提供一層簡單的功能。Laravel 預設為應用程式建立每天的日誌檔並儲存在 `storage/logs` 目錄。你可以使用 `Log` [facade](/docs/{{version}}/facades) 寫入資訊到你的日誌：

    <?php

    namespace App\Http\Controllers;

    use Log;
    use App\User;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * 顯示給定使用者的個人資料。
         *
         * @param  int  $id
         * @return Response
         */
        public function showProfile($id)
        {
            Log::info('Showing user profile for user: '.$id);

            return view('user.profile', ['user' => User::findOrFail($id)]);
        }
    }

日誌工具提供了定義在 [RFC 5424](http://tools.ietf.org/html/rfc5424) 的八個級別： **emergency**、**alert**、**critical**、**error**、**warning**、**notice**、**info** 和 **debug**。

    Log::emergency($error);
    Log::alert($error);
    Log::critical($error);
    Log::error($error);
    Log::warning($error);
    Log::notice($error);
    Log::info($error);
    Log::debug($error);

#### 上下文訊息

傳入上下文相關的資料陣列到日誌方法裡。此上下文的相關資料會進行格式化並顯示在日誌訊息：

    Log::info('User failed to login.', ['id' => $user->id]);

#### 存取 Monolog 底層實例

Monolog 有許多各式的附加處理方法讓你使用在日誌上。如果有需要，你可以存取 Laravel 底層的 Monolog 實例：

    $monolog = Log::getMonolog();
