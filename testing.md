# 測試：準備開始

- [前言](#introduction)
- [環境](#environment)
- [建立測試](#creating-tests)
- [執行測試](#running-tests)
    - [平行執行測試](#running-tests-in-parallel)
    - [回報測試覆蓋範圍](#reporting-test-coverage)

<a name="introduction"></a>
## 前言

Laravel 在建立時就已經考慮到測試。事實上，本來就支援以 PHPUnit 來進行測試，同時已經為你的應用程式建立了一份 `phpunit.xml` 檔案。框架也提供了便利的輔助函式，讓你能更直觀地測試你的應用程式。

在預設下，你的應用程式的 `tests` 資料夾下會有兩個資料夾：`Feature` 及 `Unit`。單元測試 (Unit tests) 會專注在測試非常小、獨立的程式碼。事實上，大部分的單元測試通常只專注在單一方法上。在你的「Unit」資料夾裡的測試不會去初始化你的 Laravel 應用程式，因此也沒辦法存取你應用程式的資料庫和其他的框架服務。

功能測試 (Feature tests) 會測試相對大範圍的程式碼，包含數個元件如何互動，甚或是從 HTTP 開始到 JSON 端點的完整請求。 **一般來說，多數的測試應該要是功能測試。因為這種測試會提升可信度，讓你的整體系統如所預期的運作。**

在 `Feature` 和 `Unit` 這兩個資料夾裡同時有提供一個叫 `ExampleTest.php` 的檔案。在安裝新的 Laravel 應用程式之後，執行指令 `vendor/bin/phpunit` 或 `php artisan test` 會執行你的測試。

<a name="environment"></a>
## 環境

當在執行測試的時候，Laravel 會自動將 [組態環境](/docs/{{version}}/configuration#environment-configuration) 設定成 `testing`，這是因為該環境變數事先被定義在 `phpunit.xml` 檔案裡了。Laravel 在測試的時候也自動將 session 和快取設置到 `array` 驅動裡，即測試時的 session 或快取的資料之後不會留存。

必要的話你可以自行定義其他的測試用環境組態值。`testing` 環境變數可以被設置在應用程式的 `phpunit.xml` 檔案中，不過在執行測試前，請先確認組態的快取已經清除，使用 Artisan 指令 `config:clear` 來清除快取！

<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 環境檔

另外，你也可新增一個 `.env.testing` 檔案在你專案的根目錄。當執行 PHPUnit 測試或是運作 Artisan 指令的時候，加上 `--env=testing` 選項則 `.env.testing` 檔案會取代 `.env` 被使用。

<a name="the-creates-application-trait"></a>
#### The `CreatesApplication` Trait

Laravel 包含一個叫做 `CreatesApplication` 的 trait，它被應用程式的基礎類別 `TestCase` 所套用。這個 trait 包含一個叫做 `createApplication` 的方法，在執行你的測試之前， `createApplication` 方法會啟動 Laravel 應用程式。將這個 trait 保留在原處非常重要，因為有些功能仰賴它，例如 Laravel 的平行測試功能。

<a name="creating-tests"></a>
## 建立測試

要建立一個新的測試，要使用 `make:test` Artisan 指令。預設下，測試會被放在 `tests/Feature` 資料夾中：

```shell
php artisan make:test UserTest
```

如果你想要在 `tests/Unit` 資料夾裡新增測試，你可以在執行 `make:test` 指令的時候，加上 `--unit` 選項：

```shell
php artisan make:test UserTest --unit
```

如果你想要建立一個 [Pest PHP](https://pestphp.com) 測試，你可以在 `make:test` 指令加上 `--pest` 選項：

```shell
php artisan make:test UserTest --pest
php artisan make:test UserTest --unit --pest
```

> {小訣竅} 可以使用 [stub publishing](/docs/{{version}}/artisan#stub-customization) 來客製化測試 stubs 。

一旦測試建立好了之後，你可以照一般的方式用 [PHPUnit](https://phpunit.de) 來定義測試方法。在你的終端機執行 `vendor/bin/phpunit` 或 `php artisan test` 指令來運作你的測試：

    <?php

    namespace Tests\Unit;

    use PHPUnit\Framework\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * A basic test example.
         *
         * @return void
         */
        public function test_basic_test()
        {
            $this->assertTrue(true);
        }
    }

> {備註} 如果你在測試類別中定義了你自己的 `setUp` / `tearDown` 方法，請記得在父類別去個別呼叫 `parent::setUp()` / `parent::tearDown()` 方法。

<a name="running-tests"></a>
## 執行測試

如同之前提到的，一旦寫好了測試，你就可以用 `phpunit` 來執行他們：

```shell
./vendor/bin/phpunit
```

除了 `phpunit` 指令之外，你也可以使用 `test` Artisan 指令來執行你的測試。為了開發及測試方便，Artisan 測試運行器提供詳細測試報告：

```shell
php artisan test
```

所有能夠被傳給 `phpunit` 指令的引數，也同樣能被傳給 Artisan 的 `test` 指令：

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### 平行執行測試

預設下，在單一程序中 Laravel 和 PHPUnit 會按順序地執行你的測試。不過，你也可以藉由同時執行多個跨程序的測試，來大大降低多個測試所花費的時間。先從確認你的應用程式是否套用版本 `^5.3` 或以上的 `nunomaduro/collision` 套件開始。然後，在執行 `test` Artisan 指令的時候，加上 `--parallel` 選項：

```shell
php artisan test --parallel
```

預設下，Laravel 會建立你機器的處理器核心所能提供的最大程序量。不過，你也可以用  `--processes` 選項來調整程序量：

```shell
php artisan test --parallel --processes=4
```

> {備註} 當執行平行測試的時候，有些 PHPUnit 選項是無效的。（例如 `--do-not-cache-result`）

<a name="parallel-testing-and-databases"></a>
#### 平行測試與資料庫

針對每個執行測試的平行程序，Laravel 會自動協助建立和遷徙一個測試用的資料庫。每個程序會有獨一無二的程序標記，被作為測試用資料庫的接尾詞。例如，如果你有兩個平行的測試程序，Laravel 會建立並使用 `your_db_test_1` 和 `your_db_test_2` 這兩個測試資料庫。

預設下，測試資料庫會在 `test` Artisan 指令的呼叫之間被保留，這樣他們才能被接下來的 `test` 調用所使用。不過，你也可以用 `--recreate-databases` 選項來重建測試資料庫：

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### 平行測試掛勾

有時候，你會需要準備被你的應用程式的測試所使用的特定資源，這些測試才能被多個測試程序安全地使用。

藉由使用 `ParallelTesting` facade，你可以在程序或測試項目的 `setUp` 和 `tearDown` 中指派要被執行的程式碼。給定的閉包會分別接收包含程序標記的 `$token` 和 `$testCase` 變數以及目前的測試項目：

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Artisan;
    use Illuminate\Support\Facades\ParallelTesting;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            ParallelTesting::setUpProcess(function ($token) {
                // ...
            });

            ParallelTesting::setUpTestCase(function ($token, $testCase) {
                // ...
            });

            // Executed when a test database is created...
            ParallelTesting::setUpTestDatabase(function ($database, $token) {
                Artisan::call('db:seed');
            });

            ParallelTesting::tearDownTestCase(function ($token, $testCase) {
                // ...
            });

            ParallelTesting::tearDownProcess(function ($token) {
                // ...
            });
        }
    }

<a name="accessing-the-parallel-testing-token"></a>
#### 存取平行測試標記

如果你想要從你的應用程式測試碼去存取目前平行程序的「標記」的話，你可以使用 `token` 方法。這個標記是針對一個獨立測試程序的一個獨一無二的字串識別符，可用來區隔跨平行程序的測試程序資源：

    $token = ParallelTesting::token();

<a name="reporting-test-coverage"></a>
### 回報測試覆蓋範圍

> {備註} 這個功能需要安裝 [Xdebug](https://xdebug.org) or [PCOV](https://pecl.php.net/package/pcov) 。

當執行你的應用程式測試時，你可能會想要確定你的測試項目是否真的涵蓋到應用程式，以及多少的應用程式碼被測試使用到。要確認這些資訊，你可以在呼叫 `test` 指令時加上 `--coverage` 選項：

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 實施最低覆蓋臨界值

你可以為你的應用程式使用 `--min` 選項來定義最低測試覆蓋臨界值。如果沒有達到臨界值，測試套件就會失敗：

```shell
php artisan test --coverage --min=80.3
```
