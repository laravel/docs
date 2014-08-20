# 認證與安全性

- [設定](#configuration)
- [儲存密碼](#storing-passwords)
- [使用者認證](#authenticating-users)
- [手動登入使用者](#manually)
- [保護路由](#protecting-routes)
- [HTTP 簡易認證](#http-basic-authentication)
- [忘記密碼與密碼重設](#password-reminders-and-reset)
- [加密](#encryption)
- [認證驅動](#authentication-drivers)

<a name="configuration"></a>
## 設定

Laravel 的目標就是要讓實作認證機制變得簡單。事實上，幾乎所有的設定預設就已經完成了。有關認證的設定檔都放在 `app/config/auth.php` 裡，而在這些檔案裡也都包含了良好的註解說明每一個選項的所對應的認證行為及動作。

Laravel 預設在 `app/models` 資料夾內就包含了一個使用 Eloquent 認證驅動的`User` 模型。請記得在建立模型結構時，密碼欄位至少要有 60 個字元寬度。

假如您的應用程式並不是使用 Eloquent ，你也可以使用 Laravel 的查尋產生器做  `database` 認證驅動。

> **注意：** 在開始之前，請先確認您的 `users` (或其他同義) 資料表包含一個名為 `remember_token` 的欄位，欄寬 100 字元、字串型態、可接受 null。這個欄位將會被用來儲存「記住我」的 session token。

<a name="storing-passwords"></a>
## 儲存密碼

Laravel 的 `Hash` 類別提供了安全的 Bcrypt 雜湊演算法：

#### 對密碼加密

	$password = Hash::make('secret');

#### 驗證密碼

	if (Hash::check('secret', $hashedPassword))
	{
		// The passwords match...
	}

#### 確認密碼是否需要重新加密

	if (Hash::needsRehash($hashed))
	{
		$hashed = Hash::make('secret');
	}

<a name="authenticating-users"></a>
## 使用者認證

要讓使用者登入，你可以使用 `Auth::attempt` 方法：

	if (Auth::attempt(array('email' => $email, 'password' => $password)))
	{
		return Redirect::intended('dashboard');
	}

需提醒的是 `email`並不是一個必要的欄位，在這裡僅用於示範。你可以使用資料庫裡任何類似於「使用者名稱」的欄位做為帳號值。若使用者尚未登入的話，認證篩選器會使用 `Redirect::intended` 方法重導使用者至指定的 URL。我們可指定一個備用 URI ，假如預定的位置不存在時使用。

當 `attempt` 方法被呼叫時，`auth.attempt` [事件](/docs/events) 將會被觸發。假如認證成功的話，則 `auth.login` 事件會接著被觸發。

#### 判定使用者是否已登入

判定一個使用者是否已經登入您的應用程式，您可以使用 `check` 這個方法：

	if (Auth::check())
	{
		// The user is logged in...
	}

#### 認證一個使用者並且「記住」他

假如您想要在您的應用程式內提供「記住我」的選項，您可以在 `attempt` 方法的第二個參數給 `true` 值，這樣就可以保留使用者的認證身份 (或直到他手動登出為止)。當然，您的 `users` 資料表必需包括一個字串型態的 `remember_token` 欄位來儲存「記住我」的標記。

	if (Auth::attempt(array('email' => $email, 'password' => $password), true))
	{
		// The user is being remembered...
	}

**注意：** 假如 `attempt` 方法回傳 `true` ，則表示使用者已經登入您的應用程式。

#### 透過記住我來認證使用者
假如您讓使用者透過「記住我」的方式來登入，則您可以使用 `viaRemember` 方法來判定使用者是否擁有「記住我」cookie 來認證使用者登入：

	if (Auth::viaRemember())
	{
		//
	}

#### 條件認證使用者

在認證過程中，您可能會想要增加額外的認證條件：

    if (Auth::attempt(array('email' => $email, 'password' => $password, 'active' => 1)))
    {
        // The user is active, not suspended, and exists.
    }

> **注意：** 為了增加對 session 的保護，使用者的 session ID 將會在使用者認證完成後自動重新產生。

#### 取得已登入的使用者資訊

當使用者完成認證後，你就可以透過模型來取得相關的資料：

	$email = Auth::user()->email;

取得登入使用者的 ID，你可以使用 `id` 方法：

	$id = Auth::id();

若想要透過使用者的 ID 來登入應用程式，可直接使用 `loginUsingId` 方法：

	Auth::loginUsingId(1);

#### 驗證使用者資訊而不要登入

`validate` 方法可以讓您驗證使用者資訊而不真的登入應用程式：

	if (Auth::validate($credentials))
	{
		//
	}

#### 在單一請求內登入使用者

您也可以使用 `once` 方法來讓使用者在單一請求內登入。不會有任何 session 或 cookie 被產生：

	if (Auth::once($credentials))
	{
		//
	}

#### 將使用者登出

	Auth::logout();

<a name="manually"></a>
## 手動登入使用者

假如您需要將一個已存在的使用者實體登入您的應用程式，您可以用該實體很簡單的呼叫 `login` 方法：

	$user = User::find(1);

	Auth::login($user);

這個方式和用使用者帳號密碼來 `attempt` 的功能是一樣的。

<a name="protecting-routes"></a>
## 保護路由

路由過濾器可讓特定的路由僅能讓已認證的使用者連結。Laravel 預設提供 `auth` 過濾器，其被定義在 `app/filters.php` 檔案內。

#### 保護特定路由

	Route::get('profile', array('before' => 'auth', function()
	{
		// Only authenticated users may enter...
	}));

### CSRF 保護

Laravel 提供一個簡易的方式來保護您的應用程式免於跨站攻擊。

#### 在表單內引入 CSRF 標記

    <input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">

#### 驗證表單的 CSRF 標記

    Route::post('register', array('before' => 'csrf', function()
    {
        return 'You gave a valid CSRF token!';
    }));

<a name="http-basic-authentication"></a>
## HTTP 簡易認證

HTTP 簡易認證提供了一個快速的方式來認證使用者而不用特定設置一個「登入」頁。在您的路由內設定 `auth.basic` 過濾器則可啟動這個功能：

#### 用 HTTP 簡易認證保護您的路由

	Route::get('profile', array('before' => 'auth.basic', function()
	{
		// Only authenticated users may enter...
	}));

`basic` 過濾器預設將會使用 `email` 欄位來做使用者認證，假如您想要使用其他欄位來做認證的話，可在您的 `app/filters.php` 檔案內將想要拿來做認證的欄位當成第一個參數傳給 `basic` 方法：

	Route::filter('auth.basic', function()
	{
		return Auth::basic('username');
	});

#### 設定無狀態的 HTTP 簡易過濾器

一般在實作 API 認證時，往往會想要使用 HTTP 簡易認證而不要產生任何 session 或 cookie。我們可以透過定義一個過濾器並回傳 `onceBasic` 方法來達成：

	Route::filter('basic.once', function()
	{
		return Auth::onceBasic();
	});

假如您是使用 PHP FastCGI，HTTP 簡易認證預設是無法正常運作的。請在你的 `.htaccess` 檔案內新增以下程式碼來啟動這個功能：

	RewriteCond %{HTTP:Authorization} ^(.+)$
	RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

<a name="password-reminders-and-reset"></a>
## 忘記密碼與重設

### 模型與資料表

大多數的網路應用程式都會提供使用者忘記密碼的功能。為了不讓開發者重複實作這個功能，Laravel 提供了方便的方法來寄送忘記密碼通知及密碼重設的功能。在開始之前，請先確認您的 `User` 模型有實作 `Illuminate\Auth\Reminders\RemindableInterface` 。當然，預設 Laravel 的 `User` 模型本身就已實作，並且引入`Illuminate\Auth\Reminders\RemindableTrait` 來包括所有需要實作的介面方法。

#### 實作 RemindableInterface

	use Illuminate\Auth\Reminders\RemindableTrait;
	use Illuminate\Auth\Reminders\RemindableInterface;

	class User extends Eloquent implements RemindableInterface {

		use RemindableTrait;

	}

#### 產生 Reminder 資料表遷移

接下來，我們需要產生一個資料表來儲存重設密碼標記。為了產生這個資料表的遷移檔，需要執行 `auth:reminders-table` artisan 指令：

	php artisan auth:reminders-table

	php artisan migrate

### 密碼重設控制器

然後我們已經準備好產生密碼重設控制器，您可以使用 `auth:reminders-controller` artisan 指令來自動產生這個控制器，它會產生出一個 `RemindersController.php` 檔案在您的 `app/controllers` 資料夾內。

	php artisan auth:reminders-controller

產生出來的控制器已經具備 `getRemind` 方法來顯示您的忘記密碼表單。您所需要做就是建立一個 `password.remind` [視圖](/docs/responses#views)。這個視圖需要具備一個 `email` 欄位的表單，且這個表單應該要 POST 到 `RemindersController@postRemind` 動作。

一個簡單的 `password.remind` 表單視圖應該看起來像這樣：

	<form action="{{ action('RemindersController@postRemind') }}" method="POST">
		<input type="email" name="email">
		<input type="submit" value="Send Reminder">
	</form>

除了 `getRemind` 外，控制器還包括了一個 `postRemind` 方法來處理寄送忘記密碼通知信給您的使用者。這個方法會預期在 `POST` 參數內會有 `email` 欄位。假如忘記密碼通知信成功的寄發給使用者，則會有一個 `status` 訊息被暫存在 session 內；假如寄發失敗的話，則取而代之的會有一個 `error` 訊息被暫存。

在 `postRemind` 方法內，你可以在發送出去前修改訊息的內容：

	Password::remind(Input::only('email'), function($message)
	{
		$message->subject('Password Reminder');
	});

您的使用者將會收到一封電子郵件內有一個重設密碼的連結指向 `getReset` 控制器方法。忘記密碼標記是用來驗證密碼重設程序是否正確，也會傳遞給對應的控制器方法。這個動作已經設定會回傳一個 `password.reset` 視圖。這個 `token` 會被傳遞給視圖，而您需要將這個 `token` 放在一個隱形的表單欄位內。另外，您的重設密碼表單應該包括 `email`、`password` 和 `password_confirmation` 欄位。這個表單應該 POST 到 `RemindersController@postReset` 方法。

一個 `password.reset` 視圖表單應該看起來像這樣：

	<form action="{{ action('RemindersController@postReset') }}" method="POST">
		<input type="hidden" name="token" value="{{ $token }}">
		<input type="email" name="email">
		<input type="password" name="password">
		<input type="password" name="password_confirmation">
		<input type="submit" value="Reset Password">
	</form>

最後，`postReset` 方法則是專職處理重設過後的密碼。在這個控制器方法裡，Closure 傳遞 `Password::reset` 方法並且設定 `User` 內的 `password` 屬性後呼叫 `save` 方法。當然，這個 Closure 會假定您的 `User` 模型是一個 [Eloquent 模型](/docs/eloquent) 。當然，您可以自由地修改這個 Closure 內容來符合您的應用程式資料庫儲存方式。

假如密碼成功的重設，則使用者會被重導至您的應用程式根目錄。同樣的，您可以自由的更改重導的 URL；假如密碼重設失敗的話，使用者會被重導至重設密碼表單頁，而且會有 `error` 訊息被暫存在 session 內。

### 密碼驗證

預設 `Password::reset` 方法會驗證密碼符合且大於等於六個字元。您可以用 `Password::validator` 方法 (接受 Closure) 來調整這些預設值。透過這個 Closure，您可以用任何方式來做密碼驗證。需提醒的是，你不一定要驗證密碼是否符合，因為框架自動會幫您完成這項工作。

	Password::validator(function($credentials)
	{
		return strlen($credentials['password']) >= 6;
	});

> **注意：** 密碼重設標記預設會在一個小時後過期。您可以透過 `app/config/auth.php` 案內的 `reminder.expire` 選項來調整這個設定。

<a name="encryption"></a>
## 加密

Laravel 透過 mcrypt PHP 外掛來提供 AES 強度的加密演算：

#### 加密一個值

	$encrypted = Crypt::encrypt('secret');

> **注意：** 記得在 `app/config/app.php` 檔案裡設定一個 16, 24 或 32 字元的隨機字做 `key` ，否則這個加密演算結果將不夠安全。

#### 解密一個值

	$decrypted = Crypt::decrypt($encryptedValue);

#### 設定暗號及模式

您可以設定加密器的暗號及模式：

	Crypt::setMode('ctr');

	Crypt::setCipher($cipher);

<a name="authentication-drivers"></a>
## 認證驅動

Laravel 預設提供 `database` 及 `eloquent` 兩種認證驅動。假如您需要更多有關增加額外認證驅動的詳細資訊，請參考 [認證擴充文件](/docs/extending#authentication)
