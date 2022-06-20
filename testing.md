# 測試：準備開始

- [前言](#introduction)
- [環境](#environment)
- [建立測試](#creating-tests)
- [執行測試](#running-tests)
    - [同步執行測試](#running-tests-in-parallel)
    - [回報測試覆蓋範圍](#reporting-test-coverage)

<a name="introduction"></a>
## 前言

Laravel 在建立時就已經考慮到測試。事實上，本來就支援以 PHPUnit 來進行測試，同時已經為你的應用程式建立了一份 `phpunit.xml` 檔案。框架也提供了便利的輔助函式，讓你能更直觀地測試你的應用程式。

在預設下，你的應用程式的 `tests` 資料夾下會有兩個資料夾：`Feature` 及 `Unit`。單元測試 (Unit tests) 會專注在測試非常小、獨立的程式碼。事實上，大部分的單元測試通常只專注在單一方法上。在你的「Unit」資料夾裡的測試不會去驅動你的 Laravel 應用程式，因此也沒辦法存取你應用程式的資料庫和其他的框架服務。

功能測試 (Feature tests) 會測試相對大範圍的程式碼，包含數個元件如何互動，甚或是從 HTTP 開始到 JSON 端點的完整請求。 **一般來說，多數的測試應該要是功能測試。因為這種測試會提升可信度，讓你的整體系統如所預期的運作。**

在 `Feature` 和 `Unit` 這兩個資料夾裡同時有提供一個叫 `ExampleTest.php` 的檔案。在安裝新的 Laravel 應用程式之後，執行指令 `vendor/bin/phpunit` 或 `php artisan test` 會驅動你的測試。

<a name="environment"></a>
## Environment

When running tests, Laravel will automatically set the [configuration environment](/docs/{{version}}/configuration#environment-configuration) to `testing` because of the environment variables defined in the `phpunit.xml` file. Laravel also automatically configures the session and cache to the `array` driver while testing, meaning no session or cache data will be persisted while testing.

You are free to define other testing environment configuration values as necessary. The `testing` environment variables may be configured in your application's `phpunit.xml` file, but make sure to clear your configuration cache using the `config:clear` Artisan command before running your tests!

<a name="the-env-testing-environment-file"></a>
#### The `.env.testing` Environment File

In addition, you may create a `.env.testing` file in the root of your project. This file will be used instead of the `.env` file when running PHPUnit tests or executing Artisan commands with the `--env=testing` option.

<a name="the-creates-application-trait"></a>
#### The `CreatesApplication` Trait

Laravel includes a `CreatesApplication` trait that is applied to your application's base `TestCase` class. This trait contains a `createApplication` method that bootstraps the Laravel application before running your tests. It's important that you leave this trait at its original location as some features, such as Laravel's parallel testing feature, depend on it.

<a name="creating-tests"></a>
## Creating Tests

To create a new test case, use the `make:test` Artisan command. By default, tests will be placed in the `tests/Feature` directory:

```shell
php artisan make:test UserTest
```

If you would like to create a test within the `tests/Unit` directory, you may use the `--unit` option when executing the `make:test` command:

```shell
php artisan make:test UserTest --unit
```

If you would like to create a [Pest PHP](https://pestphp.com) test, you may provide the `--pest` option to the `make:test` command:

```shell
php artisan make:test UserTest --pest
php artisan make:test UserTest --unit --pest
```

> {tip} Test stubs may be customized using [stub publishing](/docs/{{version}}/artisan#stub-customization).

Once the test has been generated, you may define test methods as you normally would using [PHPUnit](https://phpunit.de). To run your tests, execute the `vendor/bin/phpunit` or `php artisan test` command from your terminal:

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

> {note} If you define your own `setUp` / `tearDown` methods within a test class, be sure to call the respective `parent::setUp()` / `parent::tearDown()` methods on the parent class.

<a name="running-tests"></a>
## Running Tests

As mentioned previously, once you've written tests, you may run them using `phpunit`:

```shell
./vendor/bin/phpunit
```

In addition to the `phpunit` command, you may use the `test` Artisan command to run your tests. The Artisan test runner provides verbose test reports in order to ease development and debugging:

```shell
php artisan test
```

Any arguments that can be passed to the `phpunit` command may also be passed to the Artisan `test` command:

```shell
php artisan test --testsuite=Feature --stop-on-failure
```

<a name="running-tests-in-parallel"></a>
### Running Tests In Parallel

By default, Laravel and PHPUnit execute your tests sequentially within a single process. However, you may greatly reduce the amount of time it takes to run your tests by running tests simultaneously across multiple processes. To get started, ensure your application depends on version `^5.3` or greater of the `nunomaduro/collision` package. Then, include the `--parallel` option when executing the `test` Artisan command:

```shell
php artisan test --parallel
```

By default, Laravel will create as many processes as there are available CPU cores on your machine. However, you may adjust the number of processes using the `--processes` option:

```shell
php artisan test --parallel --processes=4
```

> {note} When running tests in parallel, some PHPUnit options (such as `--do-not-cache-result`) may not be available.

<a name="parallel-testing-and-databases"></a>
#### Parallel Testing & Databases

Laravel automatically handles creating and migrating a test database for each parallel process that is running your tests. The test databases will be suffixed with a process token which is unique per process. For example, if you have two parallel test processes, Laravel will create and use `your_db_test_1` and `your_db_test_2` test databases.

By default, test databases persist between calls to the `test` Artisan command so that they can be used again by subsequent `test` invocations. However, you may re-create them using the `--recreate-databases` option:

```shell
php artisan test --parallel --recreate-databases
```

<a name="parallel-testing-hooks"></a>
#### Parallel Testing Hooks

Occasionally, you may need to prepare certain resources used by your application's tests so they may be safely used by multiple test processes.

Using the `ParallelTesting` facade, you may specify code to be executed on the `setUp` and `tearDown` of a process or test case. The given closures receive the `$token` and `$testCase` variables that contain the process token and the current test case, respectively:

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
#### Accessing The Parallel Testing Token

If you would like to access the current parallel process "token" from any other location in your application's test code, you may use the `token` method. This token is a unique, string identifier for an individual test process and may be used to segment resources across parallel test processes. For example, Laravel automatically appends this token to the end of the test databases created by each parallel testing process:

    $token = ParallelTesting::token();

<a name="reporting-test-coverage"></a>
### Reporting Test Coverage

> {note} This feature requires [Xdebug](https://xdebug.org) or [PCOV](https://pecl.php.net/package/pcov).

When running your application tests, you may want to determine whether your test cases are actually covering the application code and how much application code is used when running your tests. To accomplish this, you may provide the `--coverage` option when invoking the `test` command:

```shell
php artisan test --coverage
```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### Enforcing A Minimum Coverage Threshold

You may use the `--min` option to define a minimum test coverage threshold for your application. The test suite will fail if this threshold is not met:

```shell
php artisan test --coverage --min=80.3
```
