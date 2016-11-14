# Contracts

- [簡介](#introduction)
    - [Contracts Vs. Facades](#contracts-vs-facades)
- [何時使用 Contracts](#when-to-use-contracts)
    - [低耦合](#loose-coupling)
    - [簡單性](#simplicity)
- [如何使用 Contracts](#how-to-use-contracts)
- [Contract 參考](#contract-reference)

<a name="introduction"></a>
## 簡介

Laravel 的 Contracts 是一組定義了框架核心服務的介面（ interfaces ）。例如，`Illuminate\Contracts\Queue\Queue` contract 定義了隊列任務所需要的方法，而 `Illuminate\Contracts\Mail\Mailer` contract 定義了寄送 e-mail 需要的方法。

框架對於每個 contract 都有提供對應的實作，例如，Laravel 提供各種驅動程式的隊列實作，以及由 [SwiftMailer](http://swiftmailer.org/) 提供的 mailer 實作。

Laravel 所有的 contracts 都放在 [各自的 GitHub 儲存庫](https://github.com/illuminate/contracts)。除了提供所有可用的 contracts 一個快速的參考，也可以單獨作為一個低耦合的套件讓其他套件開發者使用。

<a name="contracts-vs-facades"></a>
### Contracts Vs. Facades

Laravel 的 [facades](/docs/{{version}}/facades) 和輔助方法提供一個簡單的方法來使用服務，而不需要使用型別提示和在服務容器之外解析 contracts。在大部分情況下，facade 有等價的 contract。

facade 不需要在類別的建構子中注入，而 contract 提供你在類別的建構子中明確地注入依賴。有些開發者更喜歡這種明確地定義相依性的方式，而有些開發者希歡 facade 的便利性。

> {tip} 大部分的程式不介意你使用的是 facades 或 contracts。然而，如果你正在開發套件的話，強烈建議使用 contracts，它在你的套件中將更容易地被測試。

<a name="when-to-use-contracts"></a>
## 何時使用 Contracts

如上所討論的，大部分決定使用 facades 或 contracts 取決於個人或開發團隊的喜好。facades 或 contracts 這兩者都可以建立強健的、好測試的 Laravel 應用程式。只要保持的類別專注單一職責，你會發現使用 facades 或 contracts 沒有多大的實質差別。

然而，你可能對於 contracts 仍舊有許多的疑惑。例如，為何全部使用介面？使用介面的話不是更複雜嗎？讓我們用下面的論點來解釋使用介面的原因：低耦合和簡單性。

<a name="loose-coupling"></a>
### 低耦合

首先，讓我們來檢視這一段和快取功能有高耦合的程式碼，如下：

    <?php

    namespace App\Orders;

    class Repository
    {
        /**
         * 快取實例
         */
        protected $cache;

        /**
         * 建立一個新的儲存庫實例
         *
         * @param  \SomePackage\Cache\Memcached  $cache
         * @return void
         */
        public function __construct(\SomePackage\Cache\Memcached $cache)
        {
            $this->cache = $cache;
        }

        /**
         * 藉由 ID 取得訂單資訊
         *
         * @param  int  $id
         * @return Order
         */
        public function find($id)
        {
            if ($this->cache->has($id))    {
                //
            }
        }
    }

在此類別中，程式和快取實作之間是高耦合。因為它是依賴於套件庫的特定快取類別。一旦這個套件的 API 更改了，我們的程式碼也要跟著改變。

同樣的，如果想要將底層的快取技術（比如 Memcached ）抽換成另一種（像 Redis ），又一次的我們必須修改這個 repository 類別。我們的儲存庫不應該知道這麼多關於誰提供了資料，或是如何提供等等細節。

**比起上面的做法，我們可以改用一個簡單、和套件無關的介面來改進程式碼：**

    <?php

    namespace App\Orders;

    use Illuminate\Contracts\Cache\Repository as Cache;

    class Repository
    {
        /**
         * The cache instance.
         */
        protected $cache;

        /**
         * Create a new repository instance.
         *
         * @param  Cache  $cache
         * @return void
         */
        public function __construct(Cache $cache)
        {
            $this->cache = $cache;
        }
    }

現在上面的程式碼沒有跟任何套件耦合，甚至是 Laravel。既然 contracts 套件沒有包含實作和任何依賴，你可以很簡單的對任何 contract 進行實作，你可以很簡單的寫一個替換的實作，甚至是替換 contracts，讓你可以替換快取實作而不用修改任何用到快取的程式碼。

<a name="simplicity"></a>
### 簡單性

當所有的 Laravel 服務都簡潔的使用簡單的介面定義，就能夠很簡單的決定一個服務需要提供的功能。**可以將 contracts 視為說明框架特色的簡潔文件**。

除此之外，當你依賴簡潔的介面，你的程式碼能夠很簡單的被瞭解和維護。比起搜尋一個大型複雜的類別裡有哪些可用的方法，你有一個簡單，乾淨的介面可以參考。

<a name="how-to-use-contracts"></a>
## 如何使用 Contracts

所以，要如何實作一個 contract 呢？實際上非常的簡單。

很多 Laravel 的類別都是經由[服務容器](/docs/{{version}}/container)來解析，包含控制器，事件監聽，中介層，隊列任務，甚至是路由閉包。所以，要實作一個 contract，你可以在類別的建構子使用「型別提示」解析類別。

例如，我們來看看這個事件監聽程式：

    <?php

    namespace App\Listeners;

    use App\User;
    use App\Events\OrderWasPlaced;
    use Illuminate\Contracts\Redis\Database;

    class CacheOrderInformation
    {
        /**
         * 實作 Redis 資料庫
         */
        protected $redis;

        /**
         * 建立一個新的事件處理物件
         *
         * @param  Database  $redis
         * @return void
         */
        public function __construct(Database $redis)
        {
            $this->redis = $redis;
        }

        /**
         * 處理事件
         *
         * @param  OrderWasPlaced  $event
         * @return void
         */
        public function handle(OrderWasPlaced $event)
        {
            //
        }
    }

當事件監聽被解析時，服務容器會經由類別建構子參數的型別提示，注入適當的值。要知道怎麼註冊更多服務容器，參考[這份文件](/docs/{{version}}/container)。

<a name="contract-reference"></a>
## Contract 參考

下表是 Laravel Contracts 的快速參考，以及其對應的 facade：

Contract  |  References Facade
------------- | -------------
[Illuminate\Contracts\Auth\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Auth/Factory.php)  |  Auth
[Illuminate\Contracts\Auth\PasswordBroker](https://github.com/illuminate/contracts/blob/{{version}}/Auth/PasswordBroker.php)  |  Password
[Illuminate\Contracts\Bus\Dispatcher](https://github.com/illuminate/contracts/blob/{{version}}/Bus/Dispatcher.php)  |  Bus
[Illuminate\Contracts\Broadcasting\Broadcaster](https://github.com/illuminate/contracts/blob/{{version}}/Broadcasting/Broadcaster.php)  | &nbsp;
[Illuminate\Contracts\Cache\Repository](https://github.com/illuminate/contracts/blob/{{version}}/Cache/Repository.php) | Cache
[Illuminate\Contracts\Cache\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Cache/Factory.php) | Cache::driver()
[Illuminate\Contracts\Config\Repository](https://github.com/illuminate/contracts/blob/{{version}}/Config/Repository.php) | Config
[Illuminate\Contracts\Container\Container](https://github.com/illuminate/contracts/blob/{{version}}/Container/Container.php) | App
[Illuminate\Contracts\Cookie\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Cookie/Factory.php) | Cookie
[Illuminate\Contracts\Cookie\QueueingFactory](https://github.com/illuminate/contracts/blob/{{version}}/Cookie/QueueingFactory.php) | Cookie::queue()
[Illuminate\Contracts\Encryption\Encrypter](https://github.com/illuminate/contracts/blob/{{version}}/Encryption/Encrypter.php) | Crypt
[Illuminate\Contracts\Events\Dispatcher](https://github.com/illuminate/contracts/blob/{{version}}/Events/Dispatcher.php) | Event
[Illuminate\Contracts\Filesystem\Cloud](https://github.com/illuminate/contracts/blob/{{version}}/Filesystem/Cloud.php) | &nbsp;
[Illuminate\Contracts\Filesystem\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Filesystem/Factory.php) | File
[Illuminate\Contracts\Filesystem\Filesystem](https://github.com/illuminate/contracts/blob/{{version}}/Filesystem/Filesystem.php) | File
[Illuminate\Contracts\Foundation\Application](https://github.com/illuminate/contracts/blob/{{version}}/Foundation/Application.php) | App
[Illuminate\Contracts\Hashing\Hasher](https://github.com/illuminate/contracts/blob/{{version}}/Hashing/Hasher.php) | Hash
[Illuminate\Contracts\Logging\Log](https://github.com/illuminate/contracts/blob/{{version}}/Logging/Log.php) | Log
[Illuminate\Contracts\Mail\MailQueue](https://github.com/illuminate/contracts/blob/{{version}}/Mail/MailQueue.php) | Mail::queue()
[Illuminate\Contracts\Mail\Mailer](https://github.com/illuminate/contracts/blob/{{version}}/Mail/Mailer.php) | Mail
[Illuminate\Contracts\Queue\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Queue/Factory.php) | Queue::driver()
[Illuminate\Contracts\Queue\Queue](https://github.com/illuminate/contracts/blob/{{version}}/Queue/Queue.php) | Queue
[Illuminate\Contracts\Redis\Database](https://github.com/illuminate/contracts/blob/{{version}}/Redis/Database.php) | Redis
[Illuminate\Contracts\Routing\Registrar](https://github.com/illuminate/contracts/blob/{{version}}/Routing/Registrar.php) | Route
[Illuminate\Contracts\Routing\ResponseFactory](https://github.com/illuminate/contracts/blob/{{version}}/Routing/ResponseFactory.php) | Response
[Illuminate\Contracts\Routing\UrlGenerator](https://github.com/illuminate/contracts/blob/{{version}}/Routing/UrlGenerator.php) | URL
[Illuminate\Contracts\Support\Arrayable](https://github.com/illuminate/contracts/blob/{{version}}/Support/Arrayable.php) | &nbsp;
[Illuminate\Contracts\Support\Jsonable](https://github.com/illuminate/contracts/blob/{{version}}/Support/Jsonable.php) | &nbsp;
[Illuminate\Contracts\Support\Renderable](https://github.com/illuminate/contracts/blob/{{version}}/Support/Renderable.php) | &nbsp;
[Illuminate\Contracts\Validation\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Validation/Factory.php) | Validator::make()
[Illuminate\Contracts\Validation\Validator](https://github.com/illuminate/contracts/blob/{{version}}/Validation/Validator.php) | &nbsp;
[Illuminate\Contracts\View\Factory](https://github.com/illuminate/contracts/blob/{{version}}/View/Factory.php) | View::make()
[Illuminate\Contracts\View\View](https://github.com/illuminate/contracts/blob/{{version}}/View/View.php) | &nbsp;
