# 錯誤與日誌

- [設定檔](#configuration)
- [錯誤處理](#handling-errors)
- [HTTP例外](#http-exceptions)
- [處理404錯誤](#handling-404-errors)
- [日誌](#logging)

<a name="configuration"></a>
## 設定檔

日誌處理程序註冊在[開始設定檔](/docs/lifecycle#start-files) `app/start/global.php`。日誌預設儲存在單一檔案，你可以依照需求自定。既然 Laravel使用廣為人用的 Monolog日誌，你可以利用很多 Monolog提供的處理器程序。

例如，如果你想每天使用一個日誌檔案而不是使用單一的龐大檔案，你可以照著下面的範例更改開始設定檔：

	$logFile = 'laravel.log';

	Log::useDailyFiles(storage_path().'/logs/'.$logFile);

### 錯誤顯示

錯誤顯示預設為開啓，意味著當錯誤發生時，將有錯誤頁面顯示詳細的堆疊追蹤和錯誤訊息。你可以關掉錯誤顯示的選項，把`app/config/app.php` 裡的`debug`選項改成`false`。

> **注意：**強烈建議在 production環境中關掉錯誤顯示。

<a name="handling-errors"></a>
## 錯誤處理

`app/start/global.php`裡預設有一個處理所有例外的例外處理程序：

	App::error(function(Exception $exception)
	{
		Log::error($exception);
	});

這是最基本的例外處理程序，然而你可以依照需求設定更多例外處理程序。例外處理程序會依照例外的型別提示(type-hint)被呼叫。例如，你可以創造一個只處理`RuntimeException`的例外處理程序：

	App::error(function(RuntimeException $exception)
	{
		// Handle the exception...
	});

如果例外處理程序回傳一個 response，response會直接回傳到瀏覽器，而其他例外處理程序將不會被呼叫：

	App::error(function(InvalidUserException $exception)
	{
		Log::error($exception);

		return 'Sorry! Something is wrong with this account!';
	});

為了監聽 PHP fetal errors，你可以利用`App::fatal`方法：

	App::fatal(function($exception)
	{
		//
	});

如果你有很多例外處理程序，他們應該依照從最通用到最特定的順序被定義。例如，一個對應處理型別為`Exception`的例外處理程序，應該被定義在一個對應處理自定例外型別，如`Illuminate\Encryption\DecryptException`的例外處理程序之前。

### 何處定義例外處理程序

預設上沒有註冊例外處理程序的地方。Laravel可以讓你自由設定。選擇之一是定義程序在 `start/global.php`中，一般來說，這是一個讓你方便寫入任何"bootstrapping" 程式碼的地方。如果檔案變得很擁擠，可以建立一個 `app/errors.php`檔案，並且在 `start/global.php`中引入。第三個選擇是建立 [service provider](/docs/ioc#service-providers)以註冊程序。再一次地，並沒有正確的答案，選擇一個讓你覺得舒適的地方。

<a name="http-exceptions"></a>
## HTTP 例外處理

一些例外處理表示來自伺服器的 HTTP錯誤碼，例如可能是「找不到頁面」錯誤(404)，未授權錯誤(401)，或甚至是工程師導致的500錯誤。使用下列方法以回傳這些回應：

	App::abort(404);

或是你可以選擇提供一個回應：

	App::abort(403, 'Unauthorized action.');

你可以在請求回應的生命週期中任何時間點使用這個方法。

<a name="handling-404-errors"></a>
## 404錯誤處理

你可以註冊一個錯誤處理程序處理所有"404 Not Found"錯誤，讓你可以簡單的回傳自定的404錯誤頁面。

	App::missing(function($exception)
	{
		return Response::view('errors.missing', array(), 404);
	});

<a name="logging"></a>
## 日誌

Laravel提供一個建立在強大的 [Monolog](http://github.com/seldaek/monolog)上的日誌工具。Laravel預設設定在應用程式裡建立單一日誌檔案，這個檔案儲存在`app/storage/logs/laravel.log`. 你可以像下面這樣寫入訊息：

	Log::info('This is some useful information.');

	Log::warning('Something could be going wrong.');

	Log::error('Something is really going wrong.');

日誌工具提供了七種定義在 [RFC 5424](http://tools.ietf.org/html/rfc5424)的級別：**debug**, **info**, **notice**, **warning**, **error**, **critical**, and **alert**

可以在傳入上下文相關的資料陣列到 log的方法裡：

	Log::info('Log message', array('context' => 'Other helpful information'));

Monolog提供很多額外的方法可以記錄。若有需要，你可以使用 Laravel裡使用的 Monolog實例：

	$monolog = Log::getMonolog();

你可以註冊事件捕捉所有傳到日誌的訊息：

#### 註冊日誌監聽程序

	Log::listen(function($level, $message, $context)
	{
		//
	});
