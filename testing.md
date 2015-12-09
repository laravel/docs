# 測試

- [簡介](#introduction)
- [測試應用程式](#application-testing)
    - [與你的應用程式進行互動](#interacting-with-your-application)
    - [測試 JSON APIs](#testing-json-apis)
    - [Sessions 和認證](#sessions-and-authentication)
    - [停用中介層](#disabling-middleware)
    - [自訂 HTTP 請求](#custom-http-requests)
- [使用資料庫](#working-with-databases)
    - [每次測試結束後重置資料庫](#resetting-the-database-after-each-test)
    - [模型工廠](#model-factories)
- [模擬](#mocking)
    - [模擬事件](#mocking-events)
    - [模擬任務](#mocking-jobs)
    - [模擬 Facades](#mocking-facades)

<a name="introduction"></a>
## 簡介

Laravel 在建立時就已考慮到測試的部分。事實上，預設就支援以 PHPUnit 做測試，而且已經為你的應用程式建立了 `phpunit.xml` 檔案。框架還提供了一些便利的輔助方法，讓你更直觀的測試你的應用程式。

在 `tests` 目錄中有提供一個 `ExampleTest.php` 的範例檔案。安裝新的 Laravel 應用程式之後，只要在命令列上執行 `phpunit`，就可以進行測試。

### 測試環境

在執行測試時，Laravel 會自動將環境變數設定為 `testing`，並將 Session 及快取存入`陣列`形式，也就是說在測試時不會有任何 Session 或快取資料被儲存。

你可以自由建立其他必要的測試環境設定。`testing` 的環境變數可以在 `phpunit.xml` 檔案中做修改。

### 定義並執行測試

要建立一個測試案例，使用 `make:test` Artisan 指令：

    php artisan make:test UserTest

此指令會放置一個新的 `UserTest` 類別至你的 `tests` 目錄。接著就可以像平常使用 PHPUnit 一樣定義測試方法。要執行測試只需要在終端機上執行 `phpunit` 指令：

    <?php

    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Illuminate\Foundation\Testing\DatabaseTransactions;

    class UserTest extends TestCase
    {
        /**
         * A basic test example.
         *
         * @return void
         */
        public function testExample()
        {
            $this->assertTrue(true);
        }
    }

> **注意：** 如果你要在你的類別定義自己的 `setUp` 方法，請確定有呼叫 `parent::setUp`。

<a name="application-testing"></a>
## 測試應用程式

Laravel 對於產生 HTTP 請求並送至應用程式，檢查輸出，甚至填寫表單，都提供了非常流利的 API。 舉例來說，你可以看看 `tests` 目錄中的 `ExampleTest.php` 檔案：

    <?php

    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Foundation\Testing\DatabaseTransactions;

    class ExampleTest extends TestCase
    {
        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->visit('/')
                 ->see('Laravel 5')
                 ->dontSee('Rails');
        }
    }

`visit` 方法會製造 `GET` 請求至應用程式，`see` 方法則斷言在應用程式回傳的回應中，有指定的文字。The `dontSee` method asserts that the given text is not returned in the application response.這是 Laravel 所提供最基本的應用程式測試。

<a name="interacting-with-your-application"></a>
### 與你的應用程式進行互動

當然，除了斷言文字是否存在於一個給定的回應，你可以做更多的互動。讓我們看看點擊連結及填寫表單的範例：

#### 點擊連結

在這個測試中，我們會產生一個請求送到應用程式，並「點擊」回傳回應中的連結，接著斷言我們會停留在指定的 URI。舉個例子，假設在回應中有個連結，並寫著「About Us」：

    <a href="/about-us">About Us</a>

現在，我們撰寫一個測試，點擊連結並斷言使用者會停留在正確的頁面：

    public function testBasicExample()
    {
        $this->visit('/')
             ->click('About Us')
             ->seePageIs('/about-us');
    }

#### 使用表單

Laravel 還提供了幾種用於測試表單的方法。透過 `type`、`select`、`check`、`attach` 及 `press` 方法讓你與表單所有的輸入欄進行互動。舉個例子，讓我們想像一下有個表單在應用程式的註冊頁面：

    <form action="/register" method="POST">
        {!! csrf_field() !!}

        <div>
            Name: <input type="text" name="name">
        </div>

        <div>
            <input type="checkbox" value="yes" name="terms"> Accept Terms
        </div>

        <div>
            <input type="submit" value="Register">
        </div>
    </form>

我們可以撰寫一個測試來填寫此表單，並檢查結果：

    public function testNewUserRegistration()
    {
        $this->visit('/register')
             ->type('Taylor', 'name')
             ->check('terms')
             ->press('Register')
             ->seePageIs('/dashboard');
    }

當然，如果你的表單包含像是單選欄或下拉式選單的其他輸入欄，你也可以很輕鬆的填入這些類型的區域。以下是每個表單操作方法的列表：

方法  | 說明
------------- | -------------
`$this->type($text, $elementName)`  |  「輸入（type）」文字在一個給定的區域
`$this->select($value, $elementName)`  |  「選擇（select）」一個單選欄或下拉式選單的區域
`$this->check($elementName)`  |  「勾選（Check）」一個複選欄的區域
`$this->attach($pathToFile, $elementName)`  |  「附上（Attach）」一個檔案至表單
`$this->press($buttonTextOrElementName)`  |  「按下（Press）」一個指定文字或名稱的按鈕

#### 使用附件

如果你的表單包含 `file` 的輸入欄類型，可以使用 `attach` 方法附上檔案：

    public function testPhotoCanBeUploaded()
    {
        $this->visit('/upload')
             ->name('File Name', 'name')
             ->attach($absolutePathToFile, 'photo')
             ->press('Upload')
             ->see('Upload Successful!');
    }

<a name="testing-json-apis"></a>
### 測試 JSON APIs

Laravel 也提供了幾個輔助方法測試 JSON APIs 及其回應。舉例來說，`get`、`post`、`put`、`patch` 及 `delete` 方法可以用於發出各種 HTTP 動詞的請求。你也可以很輕鬆的傳入資料或是標頭到這些方法。首先，我們撰寫一個測試，發出 `POST` 請求至 `/user` ，並斷言會回傳JSON 格式的指定陣列：

    <?php

    class ExampleTest extends TestCase
    {
        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->post('/user', ['name' => 'Sally'])
                 ->seeJson([
                     'created' => true,
                 ]);
        }
    }

`seeJson` 方法會將傳入的陣列轉換成 JSON，並驗證該 JSON 片段是否存在於應用程式回傳的 JSON 回應中的**任何位置**。也就是說，即使有其他的屬性在 JSON 回應中，但是只要給定的片段存在，此測試仍然會通過。

#### 驗證 JSON 完全匹配

如果你想驗證傳入的陣列要與應用程式回傳的 JSON **完全**匹配，可以使用 `seeJsonEquals` 方法：

    <?php

    class ExampleTest extends TestCase
    {
        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->post('/user', ['name' => 'Sally'])
                 ->seeJsonEquals([
                     'created' => true,
                 ]);
        }
    }

<a name="sessions-and-authentication"></a>
### Sessions 和認證

Laravel 提供了幾個輔助方法在測試時使用 Session。首先，你需要設定 Session 資料至給定的陣列，並使用 `withSession` 方法。對於要測試送到應用程式的請求之前，先將資料載入 session 上相當有用：

    <?php

    class ExampleTest extends TestCase
    {
        public function testApplication()
        {
            $this->withSession(['foo' => 'bar'])
                 ->visit('/');
        }
    }

當然，一般使用 Session 時都是用於保持使用者的狀態，像是認證使用者。`actingAs`  輔助方法提供了簡單的方式，讓指定的使用者認證為當前的使用者。舉個例子，我們可以使用[模型工廠](#model-factories)來產生並認證使用者：

    <?php

    class ExampleTest extends TestCase
    {
        public function testApplication()
        {
            $user = factory(App\User::class)->create();

            $this->actingAs($user)
                 ->withSession(['foo' => 'bar'])
                 ->visit('/')
                 ->see('Hello, '.$user->name);
        }
    }

<a name="disabling-middleware"></a>
### 停用中介層

測試應用程式時，你會發現，在某些測試中停用[中介層](/docs/{{version}}/middleware)是很方便的。讓你可以隔離任何中介層的影響，來測試路由及控制器。Laravel 包含一個簡潔的 `WithoutMiddleware` trait，你能夠使用它自動在測試類別中停用所有的中介層：

    <?php

    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Foundation\Testing\DatabaseTransactions;

    class ExampleTest extends TestCase
    {
        use WithoutMiddleware;

        //
    }

如果你只想要在某幾個測試方法中停用中介層，你可以在測試方法中呼叫 `withoutMiddleware` 方法：

    <?php

    class ExampleTest extends TestCase
    {
        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->withoutMiddleware();

            $this->visit('/')
                 ->see('Laravel 5');
        }
    }

<a name="custom-http-requests"></a>
### 自訂 HTTP 請求

如果你想要建立一個自訂的 HTTP 請求至你的應用程式，並取得完整的 `Illuminate\Http\Response` 物件，你可以使用 `call` 方法：

    public function testApplication()
    {
        $response = $this->call('GET', '/');

        $this->assertEquals(200, $response->status());
    }

如果你建立的是 `POST`、`PUT`、或是 `PATCH` 請求，你可以在請求時傳入一個陣列作為輸入資料。當然，你可在你的路由及控制器中透過[請求實例](/docs/{{version}}/requests)取用這些資料：

       $response = $this->call('POST', '/user', ['name' => 'Taylor']);

<a name="working-with-databases"></a>
## 使用資料庫

Laravel 也提供了多種有用的工具，讓你更容易測試使用資料庫的應用程式。首先，你可以使用 `seeInDatabase` 輔助方法，來斷言資料庫中是否存在與指定條件互相匹配的資料。舉例來說，如果我們想驗證 `users` 資料表中是否存在 `email` 值為 `sally@example.com` 的資料，我們可以按照以下的方式：

    public function testDatabase()
    {
        // 建立呼叫至應用程式...

        $this->seeInDatabase('users', ['email' => 'sally@foo.com']);
    }

當然，使用 `seeInDatabase` 方法及其他的輔助方法只是基於方便。你可以自由使用任何 PHPUnit 內建的斷言方法來擴充你的測試。

<a name="resetting-the-database-after-each-test"></a>
### 每次測試結束後重置資料庫

在每次測試結束後都重置你的資料是相當有用的，這樣前次的測試資料就不會干擾之後的測試。

#### 使用遷移

其中一種方式就是在每次測試後都還原資料庫，並在下次測試前進行遷移。Laravel 提供了簡潔的 `DatabaseMigrations` trait，它會自動幫你處理這些操作。你只需要在測試類別中使用此 trait：

    <?php

    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Illuminate\Foundation\Testing\DatabaseTransactions;

    class ExampleTest extends TestCase
    {
        use DatabaseMigrations;

        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->visit('/')
                 ->see('Laravel 5');
        }
    }

#### 使用交易

另一個方式，就是將每個測試案例包裝在資料庫交易中。當然，Laravel 提供了一個簡潔的 `DatabaseTransactions` trait，它會自動幫你處理這些操作：

    <?php

    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Illuminate\Foundation\Testing\DatabaseTransactions;

    class ExampleTest extends TestCase
    {
        use DatabaseTransactions;

        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->visit('/')
                 ->see('Laravel 5');
        }
    }

<a name="model-factories"></a>
### 模型工廠

測試時，常常需要在執行測試之前寫入一些資料到資料庫中。建立測試資料時，除了手動設定每個欄位的值，Laravel 讓你可以使用 [Eloquent 模型](/docs/{{version}}/eloquent)的「工廠」設定每個屬性的預設值。開始之前，你可以查看應用程式的 `database/factories/ModelFactory.php` 檔案。此檔案包含一個現成的工廠定義：

    $factory->define(App\User::class, function (Faker\Generator $faker) {
        return [
            'name' => $faker->name,
            'email' => $faker->email,
            'password' => bcrypt(str_random(10)),
            'remember_token' => str_random(10),
        ];
    });

閉包內為工廠的定義，你可以回傳模型所有屬性的預設測試值。該閉包內會接收到 [Faker](https://github.com/fzaninotto/Faker) PHP 函式庫的實例，它可以讓你方便的產生各種隨機的資料以進行測試。

當然，你可以自由的增加自己額外的工廠至 `ModelFactory.php` 檔案。

#### 多個工廠類型

有時你可能希望針對同一個 Eloquent 模型類別，能建立多個工廠。例如，除了一般使用者的工廠之外，還有「管理員」的工廠。你可以使用 `defineAs` 方法定義這個工廠：

    $factory->defineAs(App\User::class, 'admin', function ($faker) {
        return [
            'name' => $faker->name,
            'email' => $faker->email,
            'password' => str_random(10),
            'remember_token' => str_random(10),
            'admin' => true,
        ];
    });

除了從一般使用者工廠複製所有基底屬性，你也可以使用 `raw` 方法來取得基底屬性。一旦你取得這些屬性，就可以輕鬆的增加額外任何你需要的值：

    $factory->defineAs(App\User::class, 'admin', function ($faker) use ($factory) {
        $user = $factory->raw(App\User::class);

        return array_merge($user, ['admin' => true]);
    });

#### 在測試中使用工廠

定義工廠後，就可以在測試或是資料庫填充檔案中，透過全域 `factory` 函式產生模型實例。那麼讓我們來看看幾個建立模型的例子。首先我們會使用 `make` 方法建立模型，但是不將它們儲存至資料庫：

    public function testDatabase()
    {
        $user = factory(App\User::class)->make();

        // 在測試中使用模型...
    }

如果你想覆寫模型中的某些預設值，你可以傳遞一個包含數值的陣列至 `make` 方法。只有指定的數值會被替換，其它剩餘的數值則會按照工廠指定的預設值設定：

    $user = factory(App\User::class)->make([
        'name' => 'Abigail',
       ]);

你也可以建立一個含有多個模型的集合，或建立一個給定類型的模型：

    // 建立三個 App\User 實例...
    $users = factory(App\User::class, 3)->make();

    // 建立一個 App\User「管理員」實例...
    $user = factory(App\User::class, 'admin')->make();

    // 建立三個 App\User「管理員」實例...
    $users = factory(App\User::class, 'admin', 3)->make();

#### 保存工廠模型

`create` 方法不僅建立模型實例，也可以使用 Eloquent 的 `save` 方法將它們儲存至資料庫：

    public function testDatabase()
    {
        $user = factory(App\User::class)->create();

        // 在測試中使用模型...
    }

同樣的，你可以在傳遞陣列至 `create` 方法時覆寫模型的屬性：

    $user = factory(App\User::class)->create([
        'name' => 'Abigail',
       ]);

#### 增加關聯至模型

你甚至能保存多個模型至資料庫。在本例中，我們還會增加關聯至我們建立的模型。當使用 `create` 方法建立多個模型時，它會回傳一個 Eloquent [集合實例](/docs/{{version}}/eloquent-collections)，讓你能夠使用集合所提供的方便函式，像是 `each`：

    $users = factory(App\User::class, 3)
               ->create()
               ->each(function($u) {
                    $u->posts()->save(factory(App\Post::class)->make());
                });


<a name="mocking"></a>
## 模擬

<a name="mocking-events"></a>
### 模擬事件

如果你正在頻繁地使用 Laravel 的事件系統，你可能希望在測試時停止或是模擬某些事件。舉例來說，如果你正在測試使用者註冊功能，你可能不希望所有 `UserRegistered` 事件的處理程序被執行，因為它們會發送「歡迎」的電子郵件等等。

Laravel 提供了簡潔的 `expectsEvents` 方法，驗證預期的事件有被執行，但是防止該事件的任何處理程序被執行：

    <?php

    class ExampleTest extends TestCase
    {
        public function testUserRegistration()
        {
            $this->expectsEvents(App\Events\UserRegistered::class);

            // 測試使用者註冊的程式碼...
        }
    }

如果你希望防止所有事件的處理程序被執行，你可以使用 `withoutEvents` 方法：

    <?php

    class ExampleTest extends TestCase
    {
        public function testUserRegistration()
        {
            $this->withoutEvents();

            // 測試使用者註冊的程式碼...
        }
    }

<a name="mocking-jobs"></a>
### 模擬任務

有時你可能希望當發出請求至你的應用程式時，簡單的測試由你的控制器所派送的任務。這麼做能夠使你隔離並測試你的路由或控制器－設定除了任務以外的邏輯。當然，你之後可以在一個單獨的測試案例測試該任務。

Laravel 提供了一個簡潔的 `expectsJobs` 方法，驗證預期的任務有被派送，但是任務本身不會被執行：

    <?php

    class ExampleTest extends TestCase
    {
        public function testPurchasePodcast()
        {
            $this->expectsJobs(App\Jobs\PurchasePodcast::class);

            // 測試購買 podcast 的程式碼...
        }
    }

> **注意：** 此方法只檢測被 `DispatchesJobs` trait 的派送方法所派送的任務。它並不會檢測直接發送到 `Queue::push` 的任務。

<a name="mocking-facades"></a>
### 模擬 Facades

測試時，你可能時常需要模擬呼叫一個 Laravel [facade](/docs/{{version}}/facades)。舉個例子，參考下方的控制器行為：

    <?php

    namespace App\Http\Controllers;

    use Cache;
    use Illuminate\Routing\Controller;

    class UserController extends Controller
    {
        /**
         * 顯示應用程式所有使用者的列表。
         *
         * @return Response
         */
        public function index()
        {
            $value = Cache::get('key');

            //
        }
    }

我們可以透過 `shouldReceive` 方法模擬呼叫 `Cache` facade，它會回傳一個 [Mockery](https://github.com/padraic/mockery) 模擬的實例。因為 facades 實際上已經被 Laravel [服務容器](/docs/{{version}}/container)解決及管理，它們比起一般的靜態類別更有可測試性。舉個例子，讓我們模擬我們呼叫 `Cache` facade：

    <?php

    class FooTest extends TestCase
    {
        public function testGetIndex()
        {
            Cache::shouldReceive('get')
                        ->once()
                        ->with('key')
                        ->andReturn('value');

            $this->visit('/users')->see('value');
        }
    }

> **注意：** 你不應該模擬 `Request` facade。應該在測試時使用像是 `call` 及 `post` 的 HTTP 輔助方法來傳遞你想要的資料。
