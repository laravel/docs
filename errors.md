# 錯誤與日誌

- [設定](#configuration)
- [錯誤處理](#handling-errors)
- [HTTP 例外](#http-exceptions)
- [日誌](#logging)

<a name="configuration"></a>
## 設定

應用程式的日誌功能設定在 `Illuminate\Foundation\Bootstrap\ConfigureLogging` 啟動類別中。這個類別使用 `config/app.php` 設定檔的 `log` 設定選項。

日誌工具預設使用每天的日誌檔案；然而，你可以依照需求客製化這個行為。因為 Laravel 使用受歡迎的 [Monolog](https://github.com/Seldaek/monolog) 日誌函式庫，你可以利用很多 Monolog 提供的處理程序。

例如，如果你想要使用單一日誌檔，而不是每天一個日誌檔，你可以對 `config/app.php` 設定檔做下面的變更：

	'log' => 'single'

Laravel 提供立即可用的 `single` 、 `daily` 和 `syslog` 日誌模式。然而，你可以藉由覆寫 `ConfigureLogging` 啟動類別，依照需求自由地客製化應用程式的日誌。

### 錯誤細節

`config/app.php` 設定檔的 `app.debug` 設定選項控制應用程式透過瀏覽器顯示錯誤細節。設定選項預設參照 `.env` 檔案的 `APP_DEBUG` 環境變數。

進行本地開發時，你應該設定 `APP_DEBUG` 環境變數為 `true` 。 **在上線環境，這個值應該永遠為 `false` 。**

<a name="handling-errors"></a>
## 錯誤處理

所有的例外都由 `App\Exceptions\Handler` 類別處理。這個類別包含兩個方法： `report` 和 `render` 。

`report` 方法用來紀錄例外或把例外傳遞到外部服務，例如： [BugSnag](https://bugsnag.com) 。預設情況下， `report`  方法只基本實作簡單地傳遞例外到父類別並於父類別紀錄例外。然而，你可以依你所需自由地紀錄例外。如果你需要使用不同的方法來回報不同類型的例外，你可以使用 PHP 的 `instanceof` 比較運算子：

	/**
	 * 回報或紀錄例外。
	 *
	 * 這是一個送例外到 Sentry、Bugsnag 等服務的好地方。
	 *
	 * @param  \Exception  $e
	 * @return void
	 */
	public function report(Exception $e)
	{
		if ($e instanceof CustomException)
		{
			//
		}

		return parent::report($e);
	}

`render` 方法負責把例外轉換成應該被傳遞回瀏覽器的 HTTP 回應。預設情況下，例外會被傳遞到基底類別並幫你產生回應。然而，你可以自由的檢查例外類型或回傳客製化的回應。

例外處理程序的 `dontReport` 屬性是個陣列，包含應該不要被紀錄的例外類型。由 404 錯誤導致的例外預設不會被寫到日誌檔。你可以依照需求添加其他類型的例外到這個陣列。

<a name="http-exceptions"></a>
## HTTP 例外

有一些例外是描述來自伺服器的 HTTP 錯誤碼。例如，這可能是個「找不到頁面」錯誤 (404)、「未授權錯誤」(401)，或甚至是工程師導致的 500 錯誤。使用下面的方法來回傳這樣一個回應：

	abort(404);

或是你可以選擇提供一個回應：

	abort(403, 'Unauthorized action.');

你可以在請求的生命週期中任何時間點使用這個方法。

### 客製化 404 錯誤頁面

要讓所有的 404 錯誤回傳客製化的視圖，請建立一個 `resources/views/errors/404.blade.php` 檔案。應用程式將會使用這個視圖處理所有發生的 404 錯誤。

<a name="logging"></a>
## 日誌

Laravel 日誌工具在強大的 [Monolog](http://github.com/seldaek/monolog) 函式庫上提供一層簡單的功能。Laravel 預設為應用程式建立每天的日誌檔在 `storage/logs` 目錄。你可以像這樣把資訊寫到日誌：

	Log::info('This is some useful information.');

	Log::warning('Something could be going wrong.');

	Log::error('Something is really going wrong.');

日誌工具提供定義在 [RFC 5424](http://tools.ietf.org/html/rfc5424)  的七個級別：**debug**、**info**、**notice**、**warning**、**error**、**critical** 和 **alert**。

也可以傳入上下文相關的資料陣列到日誌方法裡：

	Log::info('Log message', ['context' => 'Other helpful information']);

Monolog 有很多其他的處理方法可以用在日誌上。如有需要，你可以取用 Laravel 底層使用的 Monolog 實例：

	$monolog = Log::getMonolog();

你也可以註冊事件來捕捉所有傳到日誌的訊息：

#### 註冊日誌事件監聽器

	Log::listen(function($level, $message, $context)
	{
		//
	});
