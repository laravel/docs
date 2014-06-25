# Upgrade Guide

- [從 4.1 升級到 4.2](#upgrade-4.2)
- [從 4.1.x 升級到 4.1.29](#upgrade-4.1.29)
- [從 4.1.25 升級到 4.1.26](#upgrade-4.1.26)
- [從 4.0 升級至 4.1](#upgrade-4.1)

<a name="upgrade-4.2"></a>
## 從 4.1 升級到 4.2

### PHP 5.4+

Laravel 4.2 需要 PHP 5.4.0 以上。

### 預設加密

增加一個新的 `cipher` 選項在你的 `app/config/app.php` 設定檔中。其選項值應為 `MCRYPT_RIJNDAEL_256`。

	'cipher' => MCRYPT_RIJNDAEL_256

該設置可用於設定所使用的 Laravel 加密工具的預設加密方法。

> **附註:** 在 Laravel 4.2，預設加密方法為`MCRYPT_RIJNDAEL_128` (AES), 被認為是最安全的加密. 必須將加密改回`MCRYPT_RIJNDAEL_256` 來解密在 Laravel <= 4.1 下加密的 cookies/values 

### 軟刪除模型現在改使用特性

如果你在模型下有使用軟刪除，現在 `softDeletes` 的屬性已經被移除。你現在要使用 `SoftDeletingTrait` 如下：

	use Illuminate\Database\Eloquent\SoftDeletingTrait;

	class User extends Eloquent {
		use SoftDeletingTrait;
	}

你一樣必須手動增加 `deleted_at` 欄位到你的 `dates` 屬性中：

	class User extends Eloquent {
		use SoftDeletingTrait;

		protected $dates = ['deleted_at'];
	}

而所有軟刪除的 API 使用方式維持相同。

> **附註:** `SoftDeletingTrait` 無法在基本模型下被使用。他只能在一個實際模型類別中使用。

### 視圖 / 分頁 / 環境 類別改名

如果你直接使用 `Illuminate\View\Environment` 或 `Illuminate\Pagination\Environment` 類別，請更新你的程式碼將其改為參照 `Illuminate\View\Factory` 和 `Illuminate\Pagination\Factory`。改名後的這兩個類別更可以代表他們的功能。

### Additional Parameter On Pagination Presenter

If you are extending the `Illuminate\Pagination\Presenter` class, the abstract method `getPageLinkWrapper` signature has changed to add the `rel` argument:

	abstract public function getPageLinkWrapper($url, $page, $rel = null);

### Iron.Io Queue 加密

如果你使用 Iron.io queue 驅動，你將需要增加一個新的 `encrypt` 選項到你的 queue 設定檔中：

    'encrypt' => true

<a name="upgrade-4.1.29"></a>
## 從 4.1.x 升級到 4.1.29

Laravel 4.1.29 對於所有的資料庫驅動加強了 column quoting 的部分。當你的模型中**沒有**使用 `fillable` 屬性，他保護你的應用程式不會受到 mass assignment 漏洞影響。如果你在模型中使用 `fillable` 屬性來防範 mass assignment, 你的應用程式將不會有漏洞。如果你使用 `guarded` 且在 "更新" 或 "儲存" 類型的函式中，傳遞了末端使用者控制的陣列，那你應該立即升級到 `4.1.29` 以避免 mass assignment 的風險。

升級到 Laravel 4.1.29，只要 `composer update` 即可。在這個發行版本中沒有重大的更新。

<a name="upgrade-4.1.26"></a>
## 從 4.1.25 升級到 4.1.26

Laravel 4.1.26 採用了爭對 "記得我" cookies 的安全性更新。在此更新之前，如果一個記得我的 cookies 被惡意使用者劫持，該 cookie 將還可以生存很長一段時間，即使真實用戶重設密碼或者登出亦同。

此更動需要在你的 `users` (或者類似的) 的資料表中增加一個額外的 `remember_token` 欄位。在更新之後，當用戶每次登入你的應用程式將會有一個全新的 token 將會被指派。這個 token 也會在使用者登出應用程式後被更新。這個更新的影響為：如果一個"記得我"的 cookie 被劫持，只要使用者登出應用程式將會廢除該 cookie。

### 升級路徑

首先，增加一個新的欄位，可空值、屬性為 VARCHAR(100)、TEXT 或同類型的欄位 `remember_token` 到你的 `users` 資料表中。

然後，如果你使用 Eloquent 認證驅動，依照下面更新你的 `User` 類別的三個方法：

	public function getRememberToken()
	{
		return $this->remember_token;
	}

	public function setRememberToken($value)
	{
		$this->remember_token = $value;
	}

	public function getRememberTokenName()
	{
		return 'remember_token';
	}

> **附註:** 所有現存的 "記得我" sessions 在此更新後將會失效，所以應用程式的所有使用者將會被迫重新登入。

### 套件管理者

兩個新的方法被加入到 `Illuminate\Auth\UserProviderInterface` interface. 範例實作方式可以在預設驅動中找到:

	public function retrieveByToken($identifier, $token);

	public function updateRememberToken(UserInterface $user, $token);

The `Illuminate\Auth\UserInterface` also received the three new methods described in the "Upgrade Path".

<a name="upgrade-4.1"></a>
## 從 4.0 升級至 4.1

### 升級你的 Composer 相依性

升級你的應用程式至 Laravel 4.1，將 `composer.json` 裡的 `laravel/framework` 版本更改至 `4.1.*`。

### 檔案置換

將你的 `public/index.php` 置換成 [這個 repository 的乾淨版本](https://github.com/laravel/laravel/blob/master/public/index.php)。

同樣的，將你的 `artisan` 置換成 [這個 repository 的乾淨版本](https://github.com/laravel/laravel/blob/master/artisan)。

### 新增設定檔案及選項

更新你在設定檔 `app/config/app.php` 裡的 `aliases` 和 `providers` 陣列。而更新的選項值可以在[這個檔案](https://github.com/laravel/laravel/blob/master/app/config/app.php)中找到。請確定將你後來加入自定和套件所需的 providers / aliases 加回陣列中。

從 [這個 repository](https://github.com/laravel/laravel/blob/master/app/config/remote.php)增加 `app/config/remote.php` 檔案。

在你的 `app/config/session.php` 增加新的選項 `expire_on_close`。而預設值為 `false`。

在你的 `app/config/queue.php` 檔案裡新增 `failed` 設定區塊。以下為區塊的預設值：

	'failed' => array(
		'database' => 'mysql', 'table' => 'failed_jobs',
	),

**（非必要）** 在你的 `app/config/view.php` 裡，將 `pagination` 設定選項更新為 `pagination::slider-3`。

### 更新控制器（Controllers）

如果 `app/controllers/BaseController.php` 有 `use` 語句在最上面，將 `use Illuminate\Routing\Controllers\Controller;` 改為 `use Illuminate\Routing\Controller;`。

### 更新密碼提醒

密碼提醒功能已經大幅修正擁有更大的彈性。你可以執行 Artisan 指令 `php artisan auth:reminders-controller` 來檢查新的存根控制器。你也可以瀏覽 [更新文檔](/docs/security#password-reminders-and-reset) 然後相應的更新你的應用程式。

更新你的 `app/lang/en/reminders.php` 語系檔案來符合[這個新版檔案](https://github.com/laravel/laravel/blob/master/app/lang/en/reminders.php)。

### 更新環境偵測

為了安全因素，不再使用網域網址來偵測辨別應用程式的環境。因為這些直很容易被偽造欺騙，繼而讓攻擊者透過請求來達到變更環境。所以你必須改為使用機器的 hostname（在 Mac & Ubuntu 下執行 `hostname` 出來的值）

（譯按：的確原有方式有安全性考量，但對於現行 VirtualHost 大量使用下，反而這樣改會造成不便）

### 更簡單的日誌文件

Laravel 目前只會產生單一的日誌文件: `app/storage/logs/laravel.log`。然而，你還是可以透過設定你的 `app/start/global.php` 檔案來更改他的行為。

### 刪除重定向結尾的斜線

在你的 `bootstrap/start.php` 檔案中，移除呼叫 `$app->redirectIfTrailingSlash()`。這個方法已不再需要了，因為之後將會改以框架內的 `.htaccess` 來處理。

然後，用[新版](https://github.com/laravel/laravel/blob/master/public/.htaccess)替換掉你 Apache 中的 `.htaccess` 檔案，來處理結尾的斜線問題。

### 取得目前路由

取得目前路由的方法由 `Route::getCurrentRoute()` 改為 `Route::current()`。

### Composer 更新

一旦你完成以上的更新，你可以執行 `composer update` 來更新應用程式的核心檔案。如果有 class load 錯誤，請在 `update` 之後加上 `--no-scripts`，如: `composer update --no-scripts`。

### Wildcard Event Listeners

The wildcard event listeners no longer append the event to your handler functions parameters. If you require finding the event that was fired you should use `Event::firing()`.