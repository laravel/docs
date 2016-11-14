# Facades

- [簡介](#introduction)
- [何時使用 Facades](#when-to-use-facades)
    - [Facades Vs. 依賴注入](#facades-vs-dependency-injection)
    - [Facades Vs. 輔助方法](#facades-vs-helper-functions)
- [Facades 如何運作](#how-facades-work)
- [Facade 類別參考](#facade-class-reference)

<a name="introduction"></a>
## 簡介

Facades 為應用程式的[服務容器](/docs/{{version}}/container)中可用的類別提供一個「靜態」介面。Laravel 附帶許多 facades，甚至你可能在不知情的狀況下已經使用他們！Laravel 「facades」作為在服務容器內基底類別的「靜態代理」，提供了一個簡潔、易表達的語法優點，同時維持比傳統的靜態方法更高的可測試性和彈性。

Laravel 的所有 facade 定義在 `Illuminate\Support\Facades` 命名空間裡，所以我們可以簡單地取出 facade：

    use Illuminate\Support\Facades\Cache;

    Route::get('/cache', function () {
        return Cache::get('key');
    });

在 Laravel 的文件中，許多範例處處地都使用了 facade 來展示這個框架的特性。

<a name="when-to-use-facades"></a>
## 何時使用 Facades

Facade 有許多優點，它提供了簡潔、易表達的語法。當你注入或設定類別時，無需記住冗長的類別名稱，即可使用 Laravel 提供的功能特性，此外，由於他們對 PHP 動態方法的獨特用法，使得它們很容易測試。

然而，有些細節在使用 facade 時需注意。最主要的威脅就是類別的職責範疇蔓延擴大，由於 facade 容易使用且不需注入，在單個類別中使用愈多愈容易地讓你的類別逐漸增大。改用依賴注入會讓這情況減輕，因為看到巨大的建構子，會讓你注意到類別變大了。因此，使用 facade 的時候，要特別注意到類別的大小，以及限縮類別的職責範疇。

> {tip} 建立 Laravel 的第三方套件時，最好是注入 [Laravel contracts](/docs/{{version}}/contracts) 而不是使用 facade，因為套件是建構在 Laravel 外面，無法使用 Laravel 的 facade 測試輔助方法。

<a name="facades-vs-dependency-injection"></a>
### Facades Vs. 依賴注入

依賴注入的一個最大優點是可以替換注入類別的實作，這在測試時很有用，因為你可以注入一個 mock 或 stub，並且斷言（assert）被此 stub 呼叫的不同方法。

但是對於靜態類別方法上進行 mock 或 stub 卻行不通。不過，由於 facade 使用了動態方法對服務容器中解析出來的物件方法進行了代理，我們也可以像測試注入類別實例那樣測試 facade。例如，給定以下路由：
    use Illuminate\Support\Facades\Cache;

    Route::get('/cache', function () {
        return Cache::get('key');
    });

我們可以這樣編寫測試來驗證，呼叫 `Cache::get` 方法且傳入我們期望的參數：

    use Illuminate\Support\Facades\Cache;

    /**
     * 基本的函式測試範例
     *
     * @return void
     */
    public function testBasicExample()
    {
        Cache::shouldReceive('get')
             ->with('key')
             ->andReturn('value');

        $this->visit('/cache')
             ->see('value');
    }

<a name="facades-vs-helper-functions"></a>
### Facades Vs. 輔助方法

除了 facades 之外，Laravel 還包含了許多執行通用任務的輔助方法函式，比如生成視圖、觸發事件、分配任務，以及發送 HTTP 回應等。很多輔助方法提供了和 facade 一樣的功能，例如，呼叫下面這個 facade 和輔助方法是等價的：

    return View::make('profile');

    return view('profile');

facade 和輔助方法並沒有實質的差別，使用輔助方法的時候，可以像測試 facade 那樣測試它們。例如，給定以下路由：

    Route::get('/cache', function () {
        return cache('key');
    });

在底層，`cache` 輔助方法會去呼叫 `Cache` facade 上的 `get` 方法，因此，儘管我們使用這個輔助方法，我們還是可以編寫如下測試，驗證這個方法以我們期望的參數被呼叫：

    use Illuminate\Support\Facades\Cache;

    /**
     * 基本的函式測試範例
     *
     * @return void
     */
    public function testBasicExample()
    {
        Cache::shouldReceive('get')
             ->with('key')
             ->andReturn('value');

        $this->visit('/cache')
             ->see('value');
    }

<a name="how-facades-work"></a>
## Facades 如何運作

在 Laravel 應用程式中，facade 是個提供從容器存取物件的類別，`Facade` 類別是讓這個機制可以運作的原因。Laravel 的 facades，以及任何你建立的客製化 facades，會繼承基底 `Illuminate\Support\Facades\Facade` 類別。

`Facade` 基底類別利用 `__callStatic()` 魔術方法從你的 facade 延遲呼叫來解析物件。在下面的範例，呼叫了 Laravel 的快取系統。看了一下這個程式碼，或許有人認為靜態方法 `get` 是在 `Cache` 類別中被呼叫的：

    <?php

    namespace App\Http\Controllers;

    use Cache;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * 顯示給定使用者的個人資料
         *
         * @param  int  $id
         * @return Response
         */
        public function showProfile($id)
        {
            $user = Cache::get('user:'.$id);

            return view('profile', ['user' => $user]);
        }
    }

注意在檔案的上方，我們「導入」`Cache` facade。這個 facade 做為存取底層實作 `Illuminate\Contracts\Cache\Factory` 介面的代理。我們使用 facade 的任何呼叫將會傳送給 Laravel 快取服務的底層實例。

如果我們查看 `Illuminate\Support\Facades\Cache` 類別，你會發現沒有靜態方法 `get`：

    class Cache extends Facade
    {
        /**
         * 取得元件的註冊名稱
         *
         * @return string
         */
        protected static function getFacadeAccessor() { return 'cache'; }
    }

相反的，`Cache` facade 繼承了基底 `Facade` 類別以及定義了 `getFacadeAccessor()` 方法。這個方法的工作是回傳服務容器綁定的名稱。當使用者在 `Cache` facade 上參考任何的靜態方法，Laravel 會從[服務容器](/docs/{{version}}/container)解析被綁定的 `cache` 以及回傳執行請求的方法（在這個範例中是 `get`）。

<a name="facade-class-reference"></a>
## Facade 類別參考

在下方你可以找到每個 facade 及其底層的類別。這個工具對於透過給定 facade 的來源快速尋找 API 文件相當有用。可應用的[服務容器綁定](/docs/{{version}}/container)關鍵字也包含在裡面。

Facade  |  類別  |  服務容器綁定
------------- | ------------- | -------------
App  |  [Illuminate\Foundation\Application](https://laravel.com/api/{{version}}/Illuminate/Foundation/Application.html)  | `app`
Artisan  |  [Illuminate\Contracts\Console\Kernel](https://laravel.com/api/{{version}}/Illuminate/Contracts/Console/Kernel.html)  |  `artisan`
Auth  |  [Illuminate\Auth\AuthManager](https://laravel.com/api/{{version}}/Illuminate/Auth/AuthManager.html)  |  `auth`
Blade  |  [Illuminate\View\Compilers\BladeCompiler](https://laravel.com/api/{{version}}/Illuminate/View/Compilers/BladeCompiler.html)  |  `blade.compiler`
Bus  |  [Illuminate\Contracts\Bus\Dispatcher](https://laravel.com/api/{{version}}/Illuminate/Contracts/Bus/Dispatcher.html)  |  &nbsp;
Cache  |  [Illuminate\Cache\Repository](https://laravel.com/api/{{version}}/Illuminate/Cache/Repository.html)  |  `cache`
Config  |  [Illuminate\Config\Repository](https://laravel.com/api/{{version}}/Illuminate/Config/Repository.html)  |  `config`
Cookie  |  [Illuminate\Cookie\CookieJar](https://laravel.com/api/{{version}}/Illuminate/Cookie/CookieJar.html)  |  `cookie`
Crypt  |  [Illuminate\Encryption\Encrypter](https://laravel.com/api/{{version}}/Illuminate/Encryption/Encrypter.html)  |  `encrypter`
DB  |  [Illuminate\Database\DatabaseManager](https://laravel.com/api/{{version}}/Illuminate/Database/DatabaseManager.html)  |  `db`
DB (Instance)  |  [Illuminate\Database\Connection](https://laravel.com/api/{{version}}/Illuminate/Database/Connection.html)  |  &nbsp;
Event  |  [Illuminate\Events\Dispatcher](https://laravel.com/api/{{version}}/Illuminate/Events/Dispatcher.html)  |  `events`
File  |  [Illuminate\Filesystem\Filesystem](https://laravel.com/api/{{version}}/Illuminate/Filesystem/Filesystem.html)  |  `files`
Gate  |  [Illuminate\Contracts\Auth\Access\Gate](https://laravel.com/api/{{version}}/Illuminate/Contracts/Auth/Access/Gate.html)  |  &nbsp;
Hash  |  [Illuminate\Contracts\Hashing\Hasher](https://laravel.com/api/{{version}}/Illuminate/Contracts/Hashing/Hasher.html)  |  `hash`
Lang  |  [Illuminate\Translation\Translator](https://laravel.com/api/{{version}}/Illuminate/Translation/Translator.html)  |  `translator`
Log  |  [Illuminate\Log\Writer](https://laravel.com/api/{{version}}/Illuminate/Log/Writer.html)  |  `log`
Mail  |  [Illuminate\Mail\Mailer](https://laravel.com/api/{{version}}/Illuminate/Mail/Mailer.html)  |  `mailer`
Notification  |  [Illuminate\Notifications\ChannelManager](https://laravel.com/api/{{version}}/Illuminate/Notifications/ChannelManager.html)  |  &nbsp;
Password  |  [Illuminate\Auth\Passwords\PasswordBrokerManager](https://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBrokerManager.html)  |  `auth.password`
Queue  |  [Illuminate\Queue\QueueManager](https://laravel.com/api/{{version}}/Illuminate/Queue/QueueManager.html)  |  `queue`
Queue (Instance)  |  [Illuminate\Contracts\Queue\Queue](https://laravel.com/api/{{version}}/Illuminate/Contracts/Queue/Queue.html)  |  `queue`
Queue (Base Class) |  [Illuminate\Queue\Queue](https://laravel.com/api/{{version}}/Illuminate/Queue/Queue.html)  |  &nbsp;
Redirect  |  [Illuminate\Routing\Redirector](https://laravel.com/api/{{version}}/Illuminate/Routing/Redirector.html)  |  `redirect`
Redis  |  [Illuminate\Redis\Database](https://laravel.com/api/{{version}}/Illuminate/Redis/Database.html)  |  `redis`
Request  |  [Illuminate\Http\Request](https://laravel.com/api/{{version}}/Illuminate/Http/Request.html)  |  `request`
Response  |  [Illuminate\Contracts\Routing\ResponseFactory](https://laravel.com/api/{{version}}/Illuminate/Contracts/Routing/ResponseFactory.html)  |  &nbsp;
Route  |  [Illuminate\Routing\Router](https://laravel.com/api/{{version}}/Illuminate/Routing/Router.html)  |  `router`
Schema  |  [Illuminate\Database\Schema\Blueprint](https://laravel.com/api/{{version}}/Illuminate/Database/Schema/Blueprint.html)  |  &nbsp;
Session  |  [Illuminate\Session\SessionManager](https://laravel.com/api/{{version}}/Illuminate/Session/SessionManager.html)  |  `session`
Session (Instance)  |  [Illuminate\Session\Store](https://laravel.com/api/{{version}}/Illuminate/Session/Store.html)  |  &nbsp;
Storage  |  [Illuminate\Contracts\Filesystem\Factory](https://laravel.com/api/{{version}}/Illuminate/Contracts/Filesystem/Factory.html)  |  `filesystem`
URL  |  [Illuminate\Routing\UrlGenerator](https://laravel.com/api/{{version}}/Illuminate/Routing/UrlGenerator.html)  |  `url`
Validator  |  [Illuminate\Validation\Factory](https://laravel.com/api/{{version}}/Illuminate/Validation/Factory.html)  |  `validator`
Validator (Instance)  |  [Illuminate\Validation\Validator](https://laravel.com/api/{{version}}/Illuminate/Validation/Validator.html) |  &nbsp;
View  |  [Illuminate\View\Factory](https://laravel.com/api/{{version}}/Illuminate/View/Factory.html)  |  `view`
View (Instance)  |  [Illuminate\View\View](https://laravel.com/api/{{version}}/Illuminate/View/View.html)  |  &nbsp;
