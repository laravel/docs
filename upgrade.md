# 升級導引

- [從 4.2 升級到 5.0](#upgrade-5.0)
- [從 4.1 升級到 4.2](#upgrade-4.2)
- [從 4.1.x 升級到 4.1.29](#upgrade-4.1.29)
- [從 4.1.25 升級到 4.1.26](#upgrade-4.1.26)
- [從 4.0 升級到 4.1](#upgrade-4.1)

<a name="upgrade-5.0"></a>
## 從 4.2 升級到 5.0

### 全新安裝，然後遷移

推薦的升級方式是建立一個全新的 Laravel `5.0` 專案，然後複製您在 `4.2` 的檔案到此新的應用程式，這將包含控制器、路由、Eloquent 模型、Artisan 命令、資產和關於此應用程式的其他特定檔案。

最開始，[安裝新的 Laravel 5 應用程式](/docs/5.0/installation)到新的本地目錄下，我們將詳細探討遷移各部分的過程。 

### Composer 相依與套件

別忘了將任何附加於 Composer 的相依套件加入 5.0 應用程式內，包含第三方程式碼（例如 SDKs）。

部分套件也許不相容剛釋出的 Laravel 5 版本，請向套件管理者確認該套件支援 Laravel 5 的版本，要在 Composer 內加入任何套件，請執行 `composer update`。

### 命名空間

預設情況下，Laravel 4 沒有在應用程式的程式碼中使用命名空間，所以，舉例來說，所有的 Eloquent 模型和控制器僅在「全域」的命名空間下，為了更快速的遷移，Laravel 5 也允許您可以將這些類別一樣保留在全域的命名空間。

### 設定檔

#### 遷移環境變數

複製新的 `.env.example` 檔案到 `.env`，在 `5.0` 這相當於原本的 `.env.php`。設定適當的值，像是 `APP_ENV` 和 `APP_KEY` （您的加密鑰匙）、資料庫認證和快取驅動與 session 驅動。

此外，複製原先自訂的 `.env.php` 檔案，並修改為 `.env`（本機環境的真實設定值）和 `.env.example` （給其他團隊成員的範本教學）。

更多關於環境設定值，請見[完整文件](/docs/5.0/configuration#environment-configuration)。

> **注意:** 在部署 Laravel 5 應用程式之前，您需要在正式主機上放置 `.env` 檔案並設定適當的值。

#### 設定檔

Laravel 5.0 不再使用 `app/config/{environmentName}/` 目錄結構來提供對應該環境的設定檔，取而代之的是，將環境對應的設定值移到 `.env`，然後在設定檔案使用 `env('key', 'default value')` 來存取，您可以在 `config/database.php` 檔案內看到相關範例。

將設定檔放在 `config/` 目錄下，來表示所有環境共用的設定檔，或是在檔案內使用 `env()` 來取得對應該環境的設定值。

請記住，若您在 `.env` 檔案內增加 key 值，同時也要對應增加到 `.env.example` 檔案中，這將可以幫助團隊成員修改他們的 `.env` 檔案。

### 路由

複製原本的 `routes.php` 檔案到 `app/Http/routes.php`。

### 控制器

下一步，將所有的控制器移到 `app/Http/Controllers` 目錄下。既然在本指南中我們不打算遷移到完整的命名空間，請將 `app/Http/Controllers` 添加到 `composer.json` 的 `classmap`，接下來，您可以從 `app/Http/Controllers/Controller.php` 基底抽象類別中移除命名空間，要確認遷移過來的控制器要繼承這個基底類別。

在 `app/Providers/RouteServiceProvider.php` 檔案中，將 `namespace` 屬性設定為 `null`。

### 路由篩選器

將篩選邏輯綁定從原本的 `app/filters.php` 複製到 `app/Providers/RouteServiceProvider.php` 的 `boot()` 方法中，並在 `app/Providers/RouteServiceProvider.php` 加入 `use Illuminate\Support\Facades\Route;` 來繼續使用 `Route` Facade。

您不需要移動任何 Laravel 4.0 預設的過濾器，像是 `auth` 和 `csrf` 。他們已經內建，只是換作以中介層形式出現。那些在路由或控制器內有參照到舊有的過濾器 (例如 `['before' => 'auth']`) 請修改參照到新的中介層（ 例如 `['middleware' => 'auth'].` ）

Laravel 5 並沒有將過濾器移除，您一樣可以使用 `before` 和 `after` 綁定和使用您自訂的過濾器。

### 全域 CSRF

預設情況下，所有路由都會使用 [CSRF 保護](/docs/5.0/routing#csrf-protection)。若想關閉它們，或是指定在特定路由開啟，請移除 `App\Http\Kernel` 中 `middleware` 陣列內的這一行：

	'App\Http\Middleware\VerifyCsrfToken',

如果您想在其他地方使用它，加入這一行到 `$routeMiddleware`:

	'csrf' => 'App\Http\Middleware\VerifyCsrfToken',

現在，您可於路由內使用 `['middleware' => 'csrf']` 即可個別添加中介層到路由/控制器。了解更多關於中介層，請見[完整文件](/docs/5.0/middleware)。

### Eloquent 模型

你可以建立新的 `app/Models` 目錄放置所有 Eloquent 模型。並且同樣地，在 `composer.json` 將此目錄加到 `classmap`。

在模型內加入 `SoftDeletingTrait` 來使用`Illuminate\Database\Eloquent\SoftDeletes`。

#### Eloquent 快取

Eloquent 不再提供 `remember` 方法來快取查詢。現在你需要手動使用 `Cache::remember` 方法快取查詢。了解更多關於快取，請見[完整文件](/docs/5.0/cache).

### 會員認證模型

要使用 Laravel 5 的會員認證系統，請遵循以下指引來升級您的 `User` 模型：

**從 `use` 區塊刪除以下內容：**

```php
use Illuminate\Auth\UserInterface;
use Illuminate\Auth\Reminders\RemindableInterface;
```

**添加以下內容到 `use` 區塊：**

```php
use Illuminate\Auth\Authenticatable;
use Illuminate\Auth\Passwords\CanResetPassword;
use Illuminate\Contracts\Auth\Authenticatable as AuthenticatableContract;
use Illuminate\Contracts\Auth\CanResetPassword as CanResetPasswordContract;
```

**移除 UserInterface 和 RemindableInterface 介面。**

**標記類別實作以下介面：**

```php
implements AuthenticatableContract, CanResetPasswordContract
```

**在類別宣告引入以下 traits：**

```php
use Authenticatable, CanResetPassword;
```

**如果你引入了上面的 traits，從 use 區塊和類別宣告中移除 `Illuminate\Auth\Reminders\RemindableTrait` 和 `Illuminate\Auth\UserTrait`**

### Cashier 的使用者需要的修改

[Laravel Cashier](/docs/5.0/billing) 的 trait 和介面名稱已作修改。trait 請改用 `Laravel\Cashier\Billable` 取代 `BillableTrait`。介面請改用 `Laravel\Cashier\Contracts\Billable` 取代 `Larave\Cashier\BillableInterface` 。不需要修改任何方法。 

### Artisan 命令

將所有的命令從舊的 `app/commands` 目錄移到新的`app/Console/Commands` 目錄。接下來，把 `app/Console/Commands` 目錄添加到 `composer.json` 的`classmap` 中。

然後，複製 Artisan 命令清單從 `start/artisan.php` 到 `app/Console/Kernel.php` 檔案的 `command` 陣列內。

### 資料庫遷移和資料填充

如果在您的資料庫內已經有 users 表，請移除 Laravel 5 內建的兩個遷移檔。

將所有的遷移檔從舊的 `app/database/migrations` 目錄移到新的 `database/migrations` 。所有的資料填充檔也要從 `app/database/seeds` 移到 `database/seeds`。

### 全域 IoC 綁定

若您在 `start/global.php` 有綁定任何 [IoC](/docs/5.0/container)，請將它們移到 `app/Providers/AppServiceProvider.php` 內的 `register` 方法，你可能需要引入 `App` facade。

你可以選擇將這些綁定，依照類別猜分到不同的服務提供者中。

### 視圖

將所有的視圖從舊的 `app/views` 移到新的`resources/views` 目錄內。

### Blade 標籤修改

基於安全考量，Laravel 5.0 會轉義所有輸出，不論您使用 `{{ }}` 或 `{{{ }}}` 標籤。您可以使用新的 `{!! !!}` 標籤來取消輸出轉義。請務必**確定**輸出內容是安全的才使用 `{!! !!}` 標籤。

然而，如果您**必須**使用舊的 Blade 語法，請在 `AppServiceProvider@register` 的結尾加入以下內容：

```php
\Blade::setRawTags('{{', '}}');
\Blade::setContentTags('{{{', '}}}');
\Blade::setEscapedContentTags('{{{', '}}}');
```

你不該輕易的使用上述設定，這將使您的應用程式更加容易暴露於 XSS 攻擊，而且註解 `{{--` 將無法作用。

### 語言檔

將所有的語言檔從舊的 `app/lang` 目錄移動到新的`resources/lang` 目錄。

### 公開目錄

將 `4.2` 版 public 內的資產移到新應用程式內的 `public` 目錄內。並確認保留 `5.0` 版的 `index.php` 檔案。

### 測試

將所有的測試從舊的 `app/tests` 移到 `tests` 目錄。

### 各式各樣的檔案

複製專案內其他各式各樣的檔案，例如：`.scrutinizer.yml`、`bower.json` 以及其他類似的工具設定檔。

您可以將 Sass、Less 或 CoffeeScript 移動到任何您想放置的地方。`resources/assets` 目錄是一個不錯的預設位置。

### 表單和 HTML 輔助函數

如果您使用表單或 HTML 輔助函數，您將會看到以下錯誤 `class 'Form' not found` 或 `class 'Html' not found`。請加入 `"illuminate/html": "~5.0"` 到 `composer.json` 的 `require` 部分，以修正此錯誤。

您也需要添加表單和 HTML 的 facades 以及服務提供者，編輯 `config/app.php` 檔案，添加此行到 'providers' 陣列內：

    'Illuminate\Html\HtmlServiceProvider',

接著，添加以下到 'aliases' 陣列內：

    'Form'      => 'Illuminate\Html\FormFacade',
    'Html'      => 'Illuminate\Html\HtmlFacade',

### 快取管理員

如果您的程式注入 `Illuminate\Cache\CacheManager` 來取得非 Facade 版本的 Laravel 快取，請改用 `Illuminate\Contracts\Cache\Repository` 注入。

### 分頁

請將所有的 `$paginator->links()` 以 `$paginator->render()` 取代。

### Beanstalk 隊列

Laravel 5.0 使用 `"pda/pheanstalk": "~3.0"` 取代原本的 `"pda/pheanstalk": "~2.1"`。 

### Remote

Remote 元件已不再使用。

### 工作區（ Workbench ）

工作區元件已不再使用。

<a name="upgrade-4.2"></a>
## 從 4.1 升級到 4.2

### PHP 5.4+

Laravel 4.2 需要 PHP 5.4.0 以上。

### 預設加密

增加一個新的 `cipher` 選項在你的 `app/config/app.php` 設定檔中。其選項值應為 `MCRYPT_RIJNDAEL_256`。

	'cipher' => MCRYPT_RIJNDAEL_256

該設置可用於設定所使用的 Laravel 加密工具的預設加密方法。

> **附註:** 在 Laravel 4.2，預設加密方法為`MCRYPT_RIJNDAEL_128` (AES)，被認為是最安全的加密。必須將加密改回`MCRYPT_RIJNDAEL_256` 來解密在 Laravel <= 4.1 下加密的 cookies/values

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

如果你擴展了 `Illuminate\Pagination\Presenter` 類別，抽象方法 `getPageLinkWrapper` 參數列變成要加上 `rel` 參數：

	abstract public function getPageLinkWrapper($url, $page, $rel = null);

### Iron.Io Queue 加密

如果你使用 Iron.io queue 驅動，你將需要增加一個新的 `encrypt` 選項到你的 queue 設定檔中：

    'encrypt' => true

<a name="upgrade-4.1.29"></a>
## 從 4.1.x 升級到 4.1.29

Laravel 4.1.29 對於所有的資料庫驅動加強了 column quoting 的部分。當你的模型中**沒有**使用 `fillable` 屬性，他保護你的應用程式不會受到 mass assignment 漏洞影響。如果你在模型中使用 `fillable` 屬性來防範 mass assignment，你的應用程式將不會有漏洞。如果你使用 `guarded` 且在「更新」或「儲存」類型的函式中，傳遞了末端使用者控制的陣列，那你應該立即升級到 `4.1.29` 以避免 mass assignment 的風險。

升級到 Laravel 4.1.29，只要 `composer update` 即可。在這個發行版本中沒有重大的更新。

<a name="upgrade-4.1.26"></a>
## 從 4.1.25 升級到 4.1.26

Laravel 4.1.26 採用了針對「記得我」cookies 的安全性更新。在此更新之前，如果一個記得我的 cookies 被惡意使用者劫持，該 cookie 將還可以生存很長一段時間，即使真實用戶重設密碼或者登出亦同。

此更動需要在你的 `users` (或者類似的) 的資料表中增加一個額外的 `remember_token` 欄位。在更新之後，當用戶每次登入你的應用程式將會有一個全新的 token 將會被指派。這個 token 也會在使用者登出應用程式後被更新。這個更新的影響為：如果一個「記得我」的 cookie 被劫持，只要使用者登出應用程式將會廢除該 cookie。

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

> **附註:** 所有現存的「記得我」sessions 在此更新後將會失效，所以應用程式的所有使用者將會被迫重新登入。

### 套件管理者

兩個新的方法被加入到 `Illuminate\Auth\UserProviderInterface` 介面。範例實作方式可以在預設驅動中找到：

	public function retrieveByToken($identifier, $token);

	public function updateRememberToken(UserInterface $user, $token);

`Illuminate\Auth\UserInterface` 也加了三個新方法描述在「升級路徑」。

<a name="upgrade-4.1"></a>
## 從 4.0 升級到 4.1

### 升級你的 Composer 相依性

升級你的應用程式至 Laravel 4.1，將 `composer.json` 裡的 `laravel/framework` 版本更改至 `4.1.*`。

### 檔案置換

將你的 `public/index.php` 置換成 [這個 repository 的乾淨版本](https://github.com/laravel/laravel/blob/master/public/index.php)。

同樣的，將你的 `artisan` 置換成 [這個 repository 的乾淨版本](https://github.com/laravel/laravel/blob/master/artisan)。

### 新增設定檔案及選項

更新你在設定檔 `app/config/app.php` 裡的 `aliases` 和 `providers` 陣列。而更新的選項值可以在 [這個檔案](https://github.com/laravel/laravel/blob/master/app/config/app.php) 中找到。請確定將你後來加入自定和套件所需的 providers / aliases 加回陣列中。

從 [這個 repository](https://github.com/laravel/laravel/blob/master/app/config/remote.php) 增加 `app/config/remote.php` 檔案。

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

更新你的 `app/lang/en/reminders.php` 語系檔案來符合 [這個新版檔案](https://github.com/laravel/laravel/blob/master/app/lang/en/reminders.php)。

### 更新環境偵測

為了安全因素，不再使用網域網址來偵測辨別應用程式的環境。因為這些直很容易被偽造欺騙，繼而讓攻擊者透過請求來達到變更環境。所以你必須改為使用機器的 hostname（在 Mac & Ubuntu 下執行 `hostname` 出來的值）

（譯按：的確原有方式有安全性考量，但對於現行 VirtualHost 大量使用下，反而這樣改會造成不便）

### 更簡單的日誌文件

Laravel 目前只會產生單一的日誌文件：`app/storage/logs/laravel.log`。然而，你還是可以透過設定你的 `app/start/global.php` 檔案來更改他的行為。

### 刪除重定向結尾的斜線

在你的 `bootstrap/start.php` 檔案中，移除呼叫 `$app->redirectIfTrailingSlash()`。這個方法已不再需要了，因為之後將會改以框架內的 `.htaccess` 來處理。

然後，用 [新版](https://github.com/laravel/laravel/blob/master/public/.htaccess) 替換掉你 Apache 中的 `.htaccess` 檔案，來處理結尾的斜線問題。

### 取得目前路由

取得目前路由的方法由 `Route::getCurrentRoute()` 改為 `Route::current()`。

### Composer 更新

一旦你完成以上的更新，你可以執行 `composer update` 來更新應用程式的核心檔案。如果有 class load 錯誤，請在 `update` 之後加上 `--no-scripts`，如：`composer update --no-scripts`。

### 萬用字元事件監聽者

萬用字元事件監聽者不再添加事件為參數到你的處理函數。如果你需要尋找你觸發的事件你應該用 `Event::firing()`.
