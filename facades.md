# Facades

- [簡介](#introduction)
- [使用 Facades](#using-facades)
- [Facade 類別參考](#facade-class-reference)

<a name="introduction"></a>
## 簡介

Facades 為應用程式的[服務容器](/docs/{{version}}/container)中可用的類別提供一個「靜態」介面。Laravel 附帶許多 facades，甚至你可能在不知情的狀況下已經使用他們！Laravel 「facades」作為在服務容器內基底類別的「靜態代理」，提供了一個簡潔、易表達的語法優點，同時維持比傳統的靜態方法更高的可測試性和彈性。

<a name="using-facades"></a>
## 使用 Facades

在 Laravel 應用程式環境（Context）中，facade 是個提供從容器存取物件的類別。`Facade` 類別是讓這個機制可以運作的原因。Laravel 的 facades，以及任何你建立的客製化 facades，會繼承基底 `Illuminate\Support\Facades\Facade` 類別。

facade 類別只需要去實作一個方法：`getFacadeAccessor`。`getFacadeAccessor` 方法的工作定義是從容器中解析出什麼。`Facade` 基底類別利用 `__callStatic()` 魔術方法從你的 facade 延遲呼叫來解析物件。

在下面的範例，呼叫了 Laravel 的快取系統。看了一下這個程式碼，或許有人認為靜態方法 `get` 是被 `Cache` 類別呼叫的：

    <?php

    namespace App\Http\Controllers;

    use Cache;
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
            $user = Cache::get('user:'.$id);

            return view('profile', ['user' => $user]);
        }
    }

注意在檔案的上方，我們「導入」`Cache` facade。這個 facade 做為存取底層實作 `Illuminate\Contracts\Cache\Factory` 介面的代理。我們使用 facade 的任何呼叫將會傳送給 Laravel 快取服務的底層實例。

如果我們查看 `Illuminate\Support\Facades\Cache` 類別，你會發現沒有靜態方法 `get`：

    class Cache extends Facade
    {
        /**
         * 取得元件的註冊名稱。
         *
         * @return string
         */
        protected static function getFacadeAccessor() { return 'cache'; }
    }

相反的，`Cache` facade 繼承了基底 `Facade` 類別以及定義了 `getFacadeAccessor()` 方法。記住，這個方法的工作是回傳服務容器綁定的名稱。當使用者在 `Cache` facade 上參考任何的靜態方法，Laravel 會從[服務容器](/docs/{{version}}/container)解析被綁定的 `cache` 以及針對物件執行請求的方法（在這個範例中是 `get`）。

<a name="facade-class-reference"></a>
## Facade 類別參考

在下方你可以找到每個 facade 及其底層的類別。這個工具對於透過給定 facade 的來源快速尋找 API 文件相當有用。可應用的[服務容器綁定](/docs/{{version}}/container)關鍵字也包含在裡面。

Facade  |  Class  |  Service Container Binding
------------- | ------------- | -------------
App  |  [Illuminate\Foundation\Application](http://laravel.com/api/{{version}}/Illuminate/Foundation/Application.html)  | `app`
Artisan  |  [Illuminate\Console\Application](http://laravel.com/api/{{version}}/Illuminate/Console/Application.html)  |  `artisan`
Auth  |  [Illuminate\Auth\AuthManager](http://laravel.com/api/{{version}}/Illuminate/Auth/AuthManager.html)  |  `auth`
Auth (Instance)  |  [Illuminate\Auth\Guard](http://laravel.com/api/{{version}}/Illuminate/Auth/Guard.html)  |
Blade  |  [Illuminate\View\Compilers\BladeCompiler](http://laravel.com/api/{{version}}/Illuminate/View/Compilers/BladeCompiler.html)  |  `blade.compiler`
Bus  |  [Illuminate\Contracts\Bus\Dispatcher](http://laravel.com/api/{{version}}/Illuminate/Contracts/Bus/Dispatcher.html)  |
Cache  |  [Illuminate\Cache\Repository](http://laravel.com/api/{{version}}/Illuminate/Cache/Repository.html)  |  `cache`
Config  |  [Illuminate\Config\Repository](http://laravel.com/api/{{version}}/Illuminate/Config/Repository.html)  |  `config`
Cookie  |  [Illuminate\Cookie\CookieJar](http://laravel.com/api/{{version}}/Illuminate/Cookie/CookieJar.html)  |  `cookie`
Crypt  |  [Illuminate\Encryption\Encrypter](http://laravel.com/api/{{version}}/Illuminate/Encryption/Encrypter.html)  |  `encrypter`
DB  |  [Illuminate\Database\DatabaseManager](http://laravel.com/api/{{version}}/Illuminate/Database/DatabaseManager.html)  |  `db`
DB (Instance)  |  [Illuminate\Database\Connection](http://laravel.com/api/{{version}}/Illuminate/Database/Connection.html)  |
Event  |  [Illuminate\Events\Dispatcher](http://laravel.com/api/{{version}}/Illuminate/Events/Dispatcher.html)  |  `events`
File  |  [Illuminate\Filesystem\Filesystem](http://laravel.com/api/{{version}}/Illuminate/Filesystem/Filesystem.html)  |  `files`
Gate  |  [Illuminate\Contracts\Auth\Access\Gate](http://laravel.com/api/5.1/Illuminate/Contracts/Auth/Access/Gate.html)  |
Hash  |  [Illuminate\Contracts\Hashing\Hasher](http://laravel.com/api/{{version}}/Illuminate/Contracts/Hashing/Hasher.html)  |  `hash`
Input  |  [Illuminate\Http\Request](http://laravel.com/api/{{version}}/Illuminate/Http/Request.html)  |  `request`
Lang  |  [Illuminate\Translation\Translator](http://laravel.com/api/{{version}}/Illuminate/Translation/Translator.html)  |  `translator`
Log  |  [Illuminate\Log\Writer](http://laravel.com/api/{{version}}/Illuminate/Log/Writer.html)  |  `log`
Mail  |  [Illuminate\Mail\Mailer](http://laravel.com/api/{{version}}/Illuminate/Mail/Mailer.html)  |  `mailer`
Password  |  [Illuminate\Auth\Passwords\PasswordBroker](http://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBroker.html)  |  `auth.password`
Queue  |  [Illuminate\Queue\QueueManager](http://laravel.com/api/{{version}}/Illuminate/Queue/QueueManager.html)  |  `queue`
Queue (Instance) |  [Illuminate\Queue\QueueInterface](http://laravel.com/api/{{version}}/Illuminate/Queue/QueueInterface.html)  |
Queue (Base Class) |  [Illuminate\Queue\Queue](http://laravel.com/api/{{version}}/Illuminate/Queue/Queue.html)  |
Redirect  |  [Illuminate\Routing\Redirector](http://laravel.com/api/{{version}}/Illuminate/Routing/Redirector.html)  |  `redirect`
Redis  |  [Illuminate\Redis\Database](http://laravel.com/api/{{version}}/Illuminate/Redis/Database.html)  |  `redis`
Request  |  [Illuminate\Http\Request](http://laravel.com/api/{{version}}/Illuminate/Http/Request.html)  |  `request`
Response  |  [Illuminate\Contracts\Routing\ResponseFactory](http://laravel.com/api/{{version}}/Illuminate/Contracts/Routing/ResponseFactory.html)  |
Route  |  [Illuminate\Routing\Router](http://laravel.com/api/{{version}}/Illuminate/Routing/Router.html)  |  `router`
Schema  |  [Illuminate\Database\Schema\Blueprint](http://laravel.com/api/{{version}}/Illuminate/Database/Schema/Blueprint.html)  |
Session  |  [Illuminate\Session\SessionManager](http://laravel.com/api/{{version}}/Illuminate/Session/SessionManager.html)  |  `session`
Session (Instance)  |  [Illuminate\Session\Store](http://laravel.com/api/{{version}}/Illuminate/Session/Store.html)  |
Storage  |  [Illuminate\Contracts\Filesystem\Factory](http://laravel.com/api/{{version}}/Illuminate/Contracts/Filesystem/Factory.html)  |  `filesystem`
URL  |  [Illuminate\Routing\UrlGenerator](http://laravel.com/api/{{version}}/Illuminate/Routing/UrlGenerator.html)  |  `url`
Validator  |  [Illuminate\Validation\Factory](http://laravel.com/api/{{version}}/Illuminate/Validation/Factory.html)  |  `validator`
Validator (Instance)  |  [Illuminate\Validation\Validator](http://laravel.com/api/{{version}}/Illuminate/Validation/Validator.html) |
View  |  [Illuminate\View\Factory](http://laravel.com/api/{{version}}/Illuminate/View/Factory.html)  |  `view`
View (Instance)  |  [Illuminate\View\View](http://laravel.com/api/{{version}}/Illuminate/View/View.html)  |
